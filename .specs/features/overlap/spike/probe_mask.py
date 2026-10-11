"""Does the ink mask of a text depend on its backdrop and on the highlight colour?"""
import asyncio, io, sys
from PIL import Image, ImageChops
from playwright.async_api import async_playwright

HTML = """<!doctype html><html><head><style>
html { background: %(root)s; }
body { margin: 0; font: 16px/1.5 Georgia, serif; }
.card { margin: 40px; padding: 20px; width: 600px; background: %(card)s; color: %(fg)s; }
</style></head><body><div class="card"><p id="t">The quick brown fox jumps over the lazy dog, and then
it does it again because one line of real glyphs is not enough to count edges.</p></div></body></html>"""

JS_HL = """() => {
  const p = document.querySelector('#t');
  const r = document.createRange(); r.selectNodeContents(p.firstChild);
  CSS.highlights.set('sq', new Highlight(r));
  const s = document.createElement('style'); s.id = 'sq'; document.head.append(s);
}"""

async def shot(page):
    return Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")

async def ink(page, on, off, channel):
    await page.evaluate("c => document.querySelector('#sq').textContent = `::highlight(sq){color:${c}}`", on)
    a = await shot(page)
    await page.evaluate("c => document.querySelector('#sq').textContent = `::highlight(sq){color:${c}}`", off)
    b = await shot(page)
    return ImageChops.subtract(a, b).split()[channel]

def count(img, amp):
    h = img.histogram()
    return sum(h[(amp + 1) // 2:]), sum(i * n for i, n in enumerate(h))

async def main():
    async with async_playwright() as pw:
        for args in ([], ["--disable-lcd-text"]):
            browser = await pw.chromium.launch(args=args)
            print("args", args)
            for on, off, ch, amp in (("rgb(255,0,0)", "rgb(0,0,0)", 0, 255), ("rgb(96,0,0)", "rgb(0,0,0)", 0, 96),
                                     ("rgb(0,0,96)", "rgb(0,0,0)", 2, 96), ("rgb(0,36,0)", "rgb(0,0,0)", 1, 36),
                                     ("rgb(255,255,255)", "rgb(0,0,0)", 0, 255)):
                row = []
                for root, card, fg in (("white", "white", "black"), ("#111", "white", "black"), ("#111", "#111", "white"),
                                       ("white", "#777", "black")):
                    page = await browser.new_page(viewport={"width": 800, "height": 400})
                    await page.set_content(HTML % {"root": root, "card": card, "fg": fg})
                    await page.evaluate(JS_HL)
                    painted = await ink(page, on, off, ch)
                    # alone: everything hidden but the text
                    await page.add_style_tag(content="* { visibility: hidden !important } #t { visibility: visible !important }")
                    alone = await ink(page, on, off, ch)
                    await page.add_style_tag(content="html { background: white !important }")
                    alone_white = await ink(page, on, off, ch)
                    row.append((count(painted, amp), count(alone, amp), count(alone_white, amp)))
                    await page.close()
                print(on, "\n   " + "\n   ".join(f"painted {p}  alone {a}  alone-white-canvas {w}" for p, a, w in row))
            await browser.close()

asyncio.run(main())
