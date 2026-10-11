import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).parent

HTML = """<!doctype html><html><body style="margin:0;font:16px/1.5 Arial">
<p>some <code id="c">inline_code()</code> and <span id="m" style="font-family:monospace">inline_code()</span>
<span id="k" style="font-family:Consolas, monospace">inline_code()</span> <kbd id="kbd">inline_code()</kbd></p>
<pre id="pre">inline_code()</pre><textarea id="ta">inline_code()</textarea>
<div style="height:%dpx"></div></body></html>"""

PROBE = """() => Object.fromEntries(['c','m','k','kbd','pre','ta'].map(id => { const e = document.getElementById(id); const r = e.getBoundingClientRect();
  return [id, [Math.round(r.width*100)/100, Math.round(r.height*100)/100, getComputedStyle(e).fontSize, getComputedStyle(e).fontFamily]]; }))"""

async def fonts(cdp, page):
    doc = await cdp.send("DOM.getDocument")
    node = await cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": "#c"})
    got = await cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]})
    return [(f["familyName"], f["glyphCount"]) for f in got["fonts"]]

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for tall, how in ((3000, "full"), (3000, "viewport"), (100, "full"), (3000, "clip"), (3000, "resize")):
            context = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            page = await context.new_page()
            await page.set_content(HTML % tall)
            cdp = await context.new_cdp_session(page)
            await cdp.send("DOM.enable"); await cdp.send("CSS.enable")
            before, fb = await page.evaluate(PROBE), await fonts(cdp, page)
            if how == "full": await page.screenshot(full_page=True)
            elif how == "viewport": await page.screenshot()
            elif how == "clip": await page.screenshot(full_page=True, clip={"x": 0, "y": 0, "width": 100, "height": 100})
            else:
                await page.set_viewport_size({"width": 1440, "height": 901})
            after, fa = await page.evaluate(PROBE), await fonts(cdp, page)
            print(f"page {tall}px, {how}: fonts {fb} -> {fa}")
            for k in before:
                if before[k] != after[k]: print("    ", k, before[k], "->", after[k])
            await context.close()
        await browser.close()
asyncio.run(main())
