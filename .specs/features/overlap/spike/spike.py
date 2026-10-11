"""Spike: Text ink, Hidden ink and the Coverer of every text of a page, in two phases.

Phase 1, four full-page screenshots: the ink of every text as painted and with
only glyphs painted. A text that loses under the threshold there is done.
Phase 2, clipped screenshots: the texts that are left, each alone with what is
inside it, and with its Silent layers. Then hit testing at the Hidden ink.
"""

import asyncio
import io
import math
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
JS = (HERE / "overlap.js").read_text("utf-8")
ROLES = ["menu", "listbox", "tooltip", "dialog", "alertdialog"]
THRESHOLD_PERCENT = 10
HIT_TEST_MAX = int(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 10**9
HALF = 128

IS_TEXT = [255 if v >= HALF else 0 for v in range(256)]
DOUBLE = [min(255, 2 * v) for v in range(256)]
NONZERO = [255 if v else 0 for v in range(256)]
# The masks of a red and of a black glyph differ by a little at their edges.
IS_OTHER = [255 if v >= 64 else 0 for v in range(256)]


class Stats:
    def __init__(self) -> None:
        self.shots = 0
        self.megapixels = 0.0
        self.hit_tests = 0
        self.times: dict[str, float] = {}


def ibox(b, w, h):
    return (
        max(0, math.floor(b[0])),
        max(0, math.floor(b[1])),
        min(w, math.ceil(b[2])),
        min(h, math.ceil(b[3])),
    )


def union(boxes):
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


def crosses(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def count(mask):
    return mask.histogram()[255]


def unseen(alone, shown):
    """Where less than half of the ink of the pixel alone shows."""
    return ImageChops.subtract(alone, shown.point(DOUBLE)).point(NONZERO)


async def shot(page, stats, clip=None):
    kw = {"full_page": True}
    if clip:
        kw["clip"] = {"x": clip[0], "y": clip[1], "width": clip[2] - clip[0], "height": clip[3] - clip[1]}
    img = Image.open(io.BytesIO(await page.screenshot(**kw))).convert("RGB")
    stats.shots += 1
    stats.megapixels += img.width * img.height / 1e6
    return img


async def layers(page, stats, clip=None):
    await page.evaluate("window.__sq.ink(true)")
    on = await shot(page, stats, clip)
    await page.evaluate("window.__sq.ink(false)")
    off = await shot(page, stats, clip)
    red, green, blue = ImageChops.subtract(on, off).split()
    # A bright green glyph is painted fatter than a black one: green is dimmed to 64.
    return red, green.point([min(255, 4 * v) for v in range(256)]), blue


def colour(texts):
    """A round and a channel for each text: texts whose boxes cross never share both."""
    cell = 64
    grid: dict[tuple[int, int], list[int]] = {}
    for n, t in enumerate(texts):
        for b in t["ib"]:
            for gx in range(b[0] // cell, (b[2] - 1) // cell + 1):
                for gy in range(b[1] // cell, (b[3] - 1) // cell + 1):
                    grid.setdefault((gx, gy), []).append(n)
    near: list[set[int]] = [set() for _ in texts]
    for members in grid.values():
        for a in members:
            for b in members:
                if a < b and b not in near[a]:
                    if any(crosses(x, y) for x in texts[a]["ib"] for y in texts[b]["ib"]):
                        near[a].add(b)
                        near[b].add(a)
    colours: list[int] = []
    for n in range(len(texts)):
        used = {colours[m] for m in near[n] if m < n}
        colours.append(next(c for c in range(len(texts) + 1) if c not in used))
    for t, c in zip(texts, colours, strict=True):
        t["round"], t["channel"] = divmod(c, 3)
    return max(colours, default=-1) // 3 + 1


def region_mask(t, bbox):
    mask = Image.new("L", (bbox[2] - bbox[0], bbox[3] - bbox[1]), 0)
    for b in t["ib"]:
        mask.paste(255, (b[0] - bbox[0], b[1] - bbox[1], b[2] - bbox[0], b[3] - bbox[1]))
    return mask


async def measure(page, stats):
    started = time.perf_counter()
    # The first screenshot beyond the viewport can change the layout (on Windows
    # the generic monospace font changes): take it before anything is measured.
    await page.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": 1, "height": 1})
    texts = await page.evaluate(JS, {"roles": ROLES})
    size = await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]")
    probe = await shot(page, stats)
    stats.shots -= 1
    stats.megapixels -= probe.width * probe.height / 1e6
    width, height = probe.size
    for t in texts:
        t["ib"] = [b for b in (ibox(b, width, height) for b in t["boxes"]) if b[0] < b[2] and b[1] < b[3]]
    texts = [t for t in texts if t["ib"]]
    for t in texts:
        t["bbox"] = union(t["ib"])
        t["text_ink"] = t["hidden"] = 0
        t["covers"] = []
    rounds = colour(texts)
    stats.times["install"] = time.perf_counter() - started

    # Phase 1.
    started = time.perf_counter()
    painted, glyphs = [], []
    for r in range(rounds):
        members = [t for t in texts if t["round"] == r]
        await page.evaluate("a => window.__sq.mark(a)", {str(t["idx"]): t["channel"] for t in members})
        await page.evaluate("window.__sq.show('page', [], false)")
        painted.append(await layers(page, stats))
        await page.evaluate("a => window.__sq.show('glyphs', a, false)", [t["idx"] for t in members])
        glyphs.append(await layers(page, stats))
    candidates = []
    for t in texts:
        bbox, c = t["bbox"], t["channel"]
        region = region_mask(t, bbox)
        alone = [layer.crop(bbox) for layer in glyphs[t["round"]]]
        t["painted"] = painted[t["round"]][c].crop(bbox)
        ink = ImageChops.darker(alone[c].point(IS_TEXT), region)
        lost = count(ImageChops.darker(ink, unseen(alone[c], t["painted"])))
        others = ImageChops.lighter(alone[(c + 1) % 3], alone[(c + 2) % 3]).point(IS_OTHER)
        collide = count(ImageChops.darker(ImageChops.darker(others, region), ImageChops.invert(ink)))
        total = count(ink)
        t["phase1"] = (total, lost, collide)
        if total + collide and (lost + collide) * 100 >= THRESHOLD_PERCENT * total:
            candidates.append(t)
    stats.times["phase1"] = time.perf_counter() - started

    # Phase 2: groups in which nothing one text shows touches the text of another.
    started = time.perf_counter()
    groups: list[list[dict]] = []
    for t in candidates:
        for group in groups:
            if not any(
                t["idx"] in o["anc"] or o["idx"] in t["anc"]
                or crosses(t["region"], o["bbox"]) or crosses(o["region"], t["bbox"])
                for o in group
            ):
                group.append(t)
                break
        else:
            groups.append([t])
    for group in groups:
        await page.evaluate("a => window.__sq.mark(a)", {str(t["idx"]): 0 for t in group})
        clip = union([t["bbox"] for t in group])
        await page.evaluate("a => window.__sq.show('alone', a, false)", [t["idx"] for t in group])
        alone = (await layers(page, stats, clip))[0]
        for t in group:
            t["alone"] = alone.crop(tuple(v - clip[i % 2] for i, v in enumerate(t["bbox"])))
            t["layered"] = t["alone"]
        for key in sorted({t["layers"] for t in group if t["layers"]}):
            members = [t for t in group if t["layers"] == key]
            clip = union([t["bbox"] for t in members])
            await page.evaluate("a => window.__sq.show('alone', a, true)", [t["idx"] for t in members])
            layered = (await layers(page, stats, clip))[0]
            for t in members:
                t["layered"] = layered.crop(tuple(v - clip[i % 2] for i, v in enumerate(t["bbox"])))
    await page.evaluate("window.__sq.show('page', [], false)")
    jobs = []
    for t in candidates:
        ink = ImageChops.darker(t["alone"].point(IS_TEXT), region_mask(t, t["bbox"]))
        hidden = ImageChops.darker(
            ImageChops.darker(ink, unseen(t["alone"], t["painted"])),
            ImageChops.invert(unseen(t["alone"], t["layered"])),
        )
        t["text_ink"], t["hidden"] = count(ink), count(hidden)
        if t["text_ink"] and t["hidden"] * 100 >= THRESHOLD_PERCENT * t["text_ink"]:
            runs = []
            data, w = hidden.tobytes(), hidden.width
            for row in range(hidden.height):
                line = data[row * w : (row + 1) * w]
                x = line.find(b"\xff")
                while x >= 0:
                    end = line.find(b"\x00", x)
                    end = w if end < 0 else end
                    runs.append([t["bbox"][1] + row, t["bbox"][0] + x, t["bbox"][0] + end])
                    x = line.find(b"\xff", end)
            jobs.append({"idx": t["idx"], "runs": runs})
    stats.times["phase2"] = time.perf_counter() - started

    started = time.perf_counter()
    total = sum(t["hidden"] for t in candidates if any(j["idx"] == t["idx"] for j in jobs))
    step = max(1, math.ceil(math.sqrt(total / HIT_TEST_MAX)))
    if jobs:
        result = await page.evaluate("([jobs, step]) => window.__sq.hit(jobs, step)", [jobs, step])
        stats.hit_tests += result["tests"]
        by_idx = {t["idx"]: t for t in candidates}
        for idx, covers in result["covers"].items():
            by_idx[int(idx)]["covers"] = sorted(covers, key=lambda c: (-c["n"], c["idx"]))
    stats.times["hit"] = time.perf_counter() - started
    stats.step = step
    stats.texts, stats.candidates, stats.groups, stats.rounds = len(texts), len(candidates), len(groups), rounds
    stats.size = (width, height)
    return texts


def verdict(t):
    """(percent, coverer, raised) of a text that would get a Finding, or None."""
    if not t["text_ink"] or t["hidden"] * 100 < THRESHOLD_PERCENT * t["text_ink"] or not t["covers"]:
        return None
    top = t["covers"][0]
    return (t["hidden"] * 100 // t["text_ink"], top["sel"], top["raised"])


async def run(url, viewport=(1440, 900), verbose=True):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--disable-lcd-text"])
        context = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]}, device_scale_factor=1)
        page = await context.new_page()
        started = time.perf_counter()
        await page.goto(url, wait_until="load")
        await page.evaluate("document.fonts.ready")
        loaded = time.perf_counter() - started
        stats = Stats()
        started = time.perf_counter()
        texts = await measure(page, stats)
        took = time.perf_counter() - started
        await browser.close()
    if verbose:
        print(
            f"{url.rsplit('/', 1)[-1]}: page {stats.size[0]}x{stats.size[1]}, load {loaded:.2f}s, layers {took:.2f}s "
            f"({', '.join(f'{k} {v:.2f}' for k, v in stats.times.items())}); {stats.texts} texts, {stats.rounds} round(s), "
            f"{stats.candidates} candidates in {stats.groups} group(s), {stats.shots} screenshots / {stats.megapixels:.1f} MP, "
            f"{stats.hit_tests} hit tests at step {stats.step}"
        )
    return texts, stats


if __name__ == "__main__":
    target = sys.argv[1]
    url = target if "://" in target else Path(target).resolve().as_uri()
    texts, _ = asyncio.run(run(url))
    for t in texts:
        v = verdict(t)
        if v or "-v" in sys.argv:
            print(f"  {t['sel']:22} ink {t['text_ink']:6} hidden {t['hidden']:6} phase1 {t['phase1']} -> {v} {t['covers'][:3] if '-v' in sys.argv else ''}")
