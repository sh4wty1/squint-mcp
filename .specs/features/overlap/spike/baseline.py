"""Today's capture() against the spike's layers taken after it on the same page (fills still applied)."""
import asyncio, sys, time
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import spike
import cases
from squint_mcp import capture as cap
from squint_mcp.models import Viewport
from playwright.async_api import async_playwright

FIX = Path(__file__).parents[4] / "tests" / "fixtures"

async def main():
    expected = cases.build()
    session = cap.BrowserSession()
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--disable-lcd-text"])
        for path in (HERE / "cases.html", HERE / "real.html", HERE / "many1.html", HERE / "many4.html", FIX / "selectors.html", FIX / "pixel-cost.html"):
            url = path.as_uri()
            await cap.capture(session, url, Viewport(width=1440, height=900), "*")
            t = time.perf_counter()
            await cap.capture(session, url, Viewport(width=1440, height=900), "*")
            today = time.perf_counter() - t
            # the layers, taken where the Capture would take them: after the fills
            context = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            page = await context.new_page()
            await page.goto(url, wait_until="load")
            await page.evaluate(cap._STABILIZE)
            await page.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": 1, "height": 1})
            await page.evaluate(cap._FILL_TEXT, "rgb(255, 255, 255)")
            stats = spike.Stats()
            spike.HIT_TEST_MAX = 20_000
            t = time.perf_counter()
            texts = await spike.measure(page, stats)
            layers = time.perf_counter() - t
            await context.close()
            got = {x["sel"]: spike.verdict(x) for x in texts if spike.verdict(x)}
            note = ""
            if path.name == "cases.html":
                note = f" cases right after the fill: {got == expected}"
                if got != expected:
                    note += f" diff {set(got.items()) ^ set(expected.items())}"
            print(f"{path.name:18} {stats.size} today {today:.2f}s, layers +{layers:.2f}s ({', '.join(f'{k} {s:.2f}' for k, s in stats.times.items())}), "
                  f"{stats.texts} texts, {stats.candidates} cand, {stats.shots} shots, {stats.hit_tests} hits step {stats.step}, {len(got)} found.{note}")
        await browser.close()
    await session.close()
asyncio.run(main())
