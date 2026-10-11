import asyncio, io, time
from pathlib import Path
from PIL import Image, ImageChops
from playwright.async_api import async_playwright
HERE = Path(__file__).parent
W = "() => document.querySelector('code').getBoundingClientRect().width"

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = await context.new_page()
        await page.goto((HERE / "real.html").as_uri())
        print("code width at load", await page.evaluate(W))
        one = Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")
        two = Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")
        print("first == second full-page screenshot:", one.size, two.size, ImageChops.difference(one, two).getbbox())
        print("code width after", await page.evaluate(W))
        page = await context.new_page()
        await page.goto((HERE / "real.html").as_uri())
        t = time.perf_counter()
        await page.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": 1, "height": 1})
        print(f"1x1 priming screenshot {time.perf_counter() - t:.3f}s, code width", await page.evaluate(W))
        three = Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")
        print("primed == second:", three.size, ImageChops.difference(three, two).getbbox())
        await browser.close()
asyncio.run(main())
