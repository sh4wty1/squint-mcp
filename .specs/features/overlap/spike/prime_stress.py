import asyncio, time
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent

async def main():
    async with async_playwright() as pw:
        for args in (["--disable-lcd-text"],):
            for size in (1, 16, 100):
                fails, took = 0, 0.0
                browser = await pw.chromium.launch(args=args)
                for n in range(150):
                    context = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
                    page = await context.new_page()
                    await page.goto((HERE / "real.html").as_uri(), wait_until="load")
                    t = time.perf_counter()
                    try:
                        await page.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": size, "height": size})
                    except Exception as e:
                        fails += 1
                        first = str(e).splitlines()[0]
                    took += time.perf_counter() - t
                    await context.close()
                await browser.close()
                print(f"args {args} clip {size}x{size}: {fails}/150 failed, mean {took / 150 * 1000:.0f} ms" + (f" ({first})" if fails else ""))
asyncio.run(main())
