"""Builds cases.html, the cases of the overlap spec, and checks the spike against them."""

import asyncio
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
REPO = Path(__file__).parents[4]
shutil.copy(REPO / "tests/fixtures/Ahem.ttf", HERE / "Ahem.ttf")

T = "XXXXXXXXXX"
RED = "background:rgb(200,0,0)"


def cover(ident, left, width, extra="", top=0, height=30, tag="div", attrs=""):
    return (
        f'<{tag} id="{ident}" {attrs} class="cover" style="left:{left}px;top:{top}px;'
        f'width:{width}px;height:{height}px;{extra}"></{tag}>'
    )


def row(inner, extra="", attrs=""):
    return f'<div class="row" {attrs} style="{extra}">{inner}</div>'


def text(ident, content=T, extra=""):
    return f'<div id="{ident}" class="text" style="{extra}">{content}</div>'


# (html, {selector: (percent, coverer, raised)}); a selector absent from the dict gets no Finding.
CASES: list[tuple[str, dict]] = [
    # Fixed elements first: they sit in the first viewport.
    (row(text("under-fixed") + '<div id="fx" class="pin" style="position:fixed;width:100px;height:30px;' + RED + '"></div>'), {}),
    (row(text("under-fixed-child") + '<div class="pin" style="position:fixed"><div id="fxc" style="width:100px;height:30px;' + RED + '"></div></div>'), {}),
    ('<div id="fixed-box" style="position:fixed;left:500px;top:20px;width:300px;height:30px">'
     + text("in-fixed", extra="margin-left:40px") + cover("in-fixed-cover", 140, 100) + "</div>",
     {"#in-fixed": (50, "#in-fixed-cover", False)}),
    (row(text("half") + cover("half-cover", 140, 100)), {"#half": (50, "#half-cover", False)}),
    (row(text("corner") + cover("corner-cover", 220, 20)), {"#corner": (10, "#corner-cover", False)}),
    (row(text("quarter") + cover("quarter-cover", 190, 50)), {"#quarter": (25, "#quarter-cover", False)}),
    (row(text("collision") + '<div id="stray" class="cover" style="left:80px;top:0;background:none">XX</div>'),
     {"#collision": (20, "#stray", False)}),
    (row(text("left") + cover("left-cover", 40, 20)), {"#left": (10, "#left-cover", False)}),
    (row(text("top") + cover("top-cover", 40, 200, height=7)), {"#top": (10, "#top-cover", False)}),
    (row(text("bottom") + cover("bottom-cover", 40, 200, top=23, height=7)), {"#bottom": (10, "#bottom-cover", False)}),
    (row(text("three-lines", f"{T} {T} {T}") + cover("lines-cover", 40, 60, top=30), "height:90px"),
     {"#three-lines": (10, "#lines-cover", False)}),
    (row(text("split", "XXXXX<b></b>XXXXX") + cover("split-cover", 220, 20)), {"#split": (10, "#split-cover", False)}),
    (row(text("veil-55") + cover("veil-55-cover", 40, 200, "background:rgba(255,255,255,0.55)")),
     {"#veil-55": (100, "#veil-55-cover", False)}),
    (row(text("veil-45") + cover("veil-45-cover", 40, 200, "background:rgba(255,255,255,0.45)")), {}),
    ('<div id="host"></div>', {"shadow-text": (50, "shadow-cover", False)}),
    (row(text("in-dialog") + cover("in-dialog-cover", 140, 100), attrs='role="dialog"'),
     {"#in-dialog": (50, "#in-dialog-cover", False)}),
    (row(text("almost-quarter") + cover("aq-cover", 191, 49)), {"#almost-quarter": (24, "#aq-cover", False)}),
    (row(text("layered-half") + cover("lh-cover", 140, 100, "z-index:1")), {"#layered-half": (50, "#lh-cover", True)}),
    (row(text("layered-corner") + cover("lc-cover", 220, 20, "z-index:1")), {"#layered-corner": (10, "#lc-cover", True)}),
    (row(text("layer-ancestor") + '<div style="position:relative;z-index:2;margin:-30px 0 0 140px;width:100px">'
         '<div id="la-cover" style="height:30px;' + RED + '"></div></div>'),
     {"#layer-ancestor": (50, "#la-cover", True)}),
    (row(text("shared-layer") + cover("sl-cover", 140, 100), "z-index:3"), {"#shared-layer": (50, "#sl-cover", False)}),
    (row(text("z-zero") + cover("zz-cover", 140, 100, "z-index:0")), {"#z-zero": (50, "#zz-cover", False)}),
    (row(text("z-static") + '<div id="zs-next" style="margin:-30px 0 0 140px;z-index:5">XXXXX</div>'),
     {"#z-static": (50, "#zs-next", False)}),
    (row(text("mixed") + cover("mixed-menu", 40, 100, attrs='role="menu"') + cover("mixed-card", 200, 40)),
     {"#mixed": (20, "#mixed-card", False)}),
    (row(text("two-covers") + cover("small-cover", 40, 40) + cover("large-cover", 160, 80)),
     {"#two-covers": (60, "#large-cover", False)}),
    (row(text("tie") + cover("tie-first", 200, 40) + cover("tie-second", 40, 40)), {"#tie": (40, "#tie-first", False)}),
    # Meant, or out of reach: no Finding.
    (row(text("stretched") + '<a id="slink" href="#"></a>'), {}),
    (row(text("under-faded") + cover("faded-cover", 140, 100, "opacity:0")), {}),
    *[(row(text(f"under-{role}") + cover(f"{role}-cover", 140, 100, attrs=f'role="{role}"')), {})
      for role in ("menu", "listbox", "tooltip", "dialog", "alertdialog")],
    (row(text("under-open-dialog") + cover("od-cover", 140, 100, tag="dialog", attrs="open")), {}),
    (row(text("under-popover") + '<div id="pop" popover="manual" class="pin" style="width:100px;height:30px;' + RED + '"></div>'), {}),
    (row(text("under-sticky") + '<div id="st" style="position:sticky;top:0;margin:-30px 0 0 140px;width:100px;height:30px;' + RED + '"></div>'), {}),
    (row(text("under-menu-item") + '<div role="menu" class="cover" style="left:140px;top:0;background:none">'
         '<div id="item" style="width:100px;height:30px;' + RED + '"></div></div>'), {}),
    (row(text("under-shadow-menu") + '<div id="menu-host" role="menu" class="cover" style="left:140px;top:0;background:none"></div>'), {}),
    (row(text("nick") + cover("nick-cover", 221, 19)), {}),
    (row(text("skim") + cover("skim-cover", 40, 200, height=6)), {}),
    (row(text("parent-text", T + '<span style="position:absolute;left:100px;top:0;width:100px;height:30px;' + RED + '"></span>',
              "position:relative")), {}),
    (row(text("under-ghost") + cover("ghost-cover", 140, 100, "pointer-events:none")), {}),
    (row('<div id="picture" style="margin-left:40px;width:200px;height:30px;background:rgb(120,120,120)"></div>'
         '<div id="caption" class="cover" style="left:60px;top:0;background:none">XXXX</div>'), {}),
    (row('<div id="inbox" class="text" style="position:relative;width:100px;padding:0 20px;background:rgb(220,220,220)">XXXXX'
         '<span id="badge" style="position:absolute;right:0;top:0;width:12px;height:12px;' + RED + '"></span></div>'), {}),
    (row(text("hidden-text", extra="visibility:hidden") + cover("ht-cover", 140, 100)), {}),
    (row(text("faded-text", extra="opacity:0") + cover("ft-cover", 140, 100)), {}),
    # The Check drops this one by its fill colour; the Capture reports it covered.
    (row(text("transparent-text", extra="color:transparent") + cover("tt-cover", 140, 100)),
     {"#transparent-text": (50, "#tt-cover", False)}),
]

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>overlap spike</title><style>
@font-face { font-family: Ahem; src: url("Ahem.ttf"); }
html, body { margin: 0; }
body { background: rgb(255,255,255); color: rgb(0,0,0); font: 20px/30px Ahem; }
.row { position: relative; margin-top: 20px; height: 30px; }
.text { margin-left: 40px; width: 200px; }
.cover { position: absolute; background: rgb(200,0,0); }
dialog.cover { margin: 0; padding: 0; border: 0; right: auto; bottom: auto; }
#pop { position: absolute; margin: 0; padding: 0; border: 0; inset: auto; }
#slink::after { content: ""; position: absolute; inset: 0; }
</style></head><body>
"""

TAIL = """
<script>
  // A fixed element and a popover are placed from the viewport or the page, not from their row.
  for (const pin of document.querySelectorAll(".pin")) {
    const rect = pin.parentElement.getBoundingClientRect();
    pin.style.left = "140px";
    pin.style.top = rect.top + "px";
  }
  document.querySelector("#pop").showPopover();
  const box = (id, extra) => `<div data-testid="${id}" style="${extra}">`;
  document.querySelector("#host").attachShadow({ mode: "open" }).innerHTML =
    `<div style="position:relative;margin-top:20px;height:30px">` +
    `<div data-testid="shadow-text" style="margin-left:40px;width:200px">XXXXXXXXXX</div>` +
    `<div data-testid="shadow-cover" style="position:absolute;left:140px;top:0;width:100px;height:30px;background:rgb(200,0,0)"></div></div>`;
  document.querySelector("#menu-host").attachShadow({ mode: "open" }).innerHTML =
    `<div data-testid="shadow-item" style="width:100px;height:30px;background:rgb(200,0,0)"></div>`;
</script></body></html>
"""


def build() -> dict:
    (HERE / "cases.html").write_text(HEAD + "\n".join(html for html, _ in CASES) + TAIL, encoding="utf-8")
    expected: dict = {}
    for _, want in CASES:
        expected.update(want)
    return expected


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    import spike

    expected = build()
    texts, _ = asyncio.run(spike.run((HERE / "cases.html").as_uri()))
    got = {t["sel"]: spike.verdict(t) for t in texts}
    bad = 0
    for sel in sorted(set(expected) | {s for s, v in got.items() if v}):
        want, have = expected.get(sel), got.get(sel)
        mark = "ok " if want == have else "BAD"
        bad += want != have
        if want != have or "-v" in sys.argv:
            t = next((t for t in texts if t["sel"] == sel), None)
            detail = (t["text_ink"], t["hidden"], t["phase1"], t["covers"][:3]) if t else None
            print(f"  {mark} {sel:20} want {want} got {have} {detail}")
    print(f"{len(expected)} expected Findings, {sum(1 for v in got.values() if v)} got, {bad} wrong")
