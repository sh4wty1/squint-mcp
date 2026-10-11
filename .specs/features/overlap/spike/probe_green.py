"""Which highlight colours give the mask of a black glyph, over light and dark backdrops?"""
import asyncio, io
from PIL import Image, ImageChops
from playwright.async_api import async_playwright

HTML = """<!doctype html><html><body style="margin:0;background:%s;font:16px/1.5 Georgia, serif">
<p id="t" style="margin:40px;width:600px">The quick brown fox jumps over the lazy dog, and then it does it again
because one line of real glyphs is not enough to count edges.</p></body></html>"""
SET = "c => document.querySelector('#sq').textContent = `::highlight(sq){color:${c}}`"

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--disable-lcd-text"])
        for name, on, ch in [(f"green {g}", (0, g, 0), 1) for g in (88, 80, 72, 64, 48, 32)]:
            out = []
            for bg in ("white", "#111", "#888"):
                page = await browser.new_page(viewport={"width": 800, "height": 300})
                await page.set_content(HTML % bg)
                await page.evaluate("""() => { const r = document.createRange(); r.selectNodeContents(document.querySelector('#t').firstChild);
                    CSS.highlights.set('sq', new Highlight(r)); const s = document.createElement('style'); s.id = 'sq'; document.head.append(s); }""")
                await page.evaluate(SET, "rgb(%d,%d,%d)" % on)
                a = Image.open(io.BytesIO(await page.screenshot())).convert("RGB")
                await page.evaluate(SET, "rgb(0,0,0)")
                b = Image.open(io.BytesIO(await page.screenshot())).convert("RGB")
                amp = max(on)
                h = ImageChops.subtract(a, b).split()[ch].histogram()
                out.append((sum(h[(amp + 1) // 2:]), round(sum(i * n for i, n in enumerate(h)) / amp)))
                await page.close()
            print(f"{name:10} text pixels / ink on white, dark, gray: {out}")
        await browser.close()
asyncio.run(main())
