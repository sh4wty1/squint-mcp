"""Capture production: the only module allowed to import `playwright` (ADR-0002)."""

import asyncio
import io
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from PIL import Image
from playwright.async_api import Browser, Playwright, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from squint_mcp import config
from squint_mcp.models import Capture, Element, Viewport

_JS = Path(__file__).parent / "js"
_STABILIZE = (_JS / "stabilize.js").read_text(encoding="utf-8")
_COLLECT_ELEMENTS = (_JS / "collect_elements.js").read_text(encoding="utf-8")


class BrowserSession:
    """The one Chromium of a server run: launched on first use, then reused."""

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._lock = asyncio.Lock()

    async def browser(self) -> Browser:
        # The lock keeps two concurrent first calls from launching two browsers.
        async with self._lock:
            if self._browser is None:
                self._playwright = self._playwright or await async_playwright().start()
                self._browser = await self._playwright.chromium.launch()
            return self._browser

    async def close(self) -> None:
        if self._browser is not None:
            await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()


@asynccontextmanager
async def browser_lifespan(_: object) -> AsyncGenerator[BrowserSession]:
    """Server lifespan: the session lives, and its browser dies, with the server."""
    session = BrowserSession()
    try:
        yield session
    finally:
        await session.close()


async def capture(
    session: BrowserSession, url: str, viewport: Viewport, selector: str
) -> Capture:
    """Open `url` in a fresh context, stabilize it and capture it.

    The Capture holds the elements matched by `selector`, which reaches into
    open shadow roots.
    """
    browser = await session.browser()
    context = await browser.new_context(
        viewport={"width": viewport.width, "height": viewport.height},
        device_scale_factor=1,
    )
    try:
        # The tool's total timeout is the only clock; Playwright's own would race it.
        context.set_default_timeout(0)
        page = await context.new_page()
        await page.goto(url, wait_until="load")
        await page.evaluate(_STABILIZE)
        try:
            await page.wait_for_load_state(
                "networkidle", timeout=config.NETWORK_IDLE_TIMEOUT_S * 1000
            )
            stabilized = True
        except PlaywrightTimeoutError:
            # Polling and analytics keep some pages busy forever: capture them anyway.
            stabilized = False
        collected = await page.locator(f"css={selector}").evaluate_all(
            _COLLECT_ELEMENTS, list(config.INSPECT_COMPUTED_PROPERTIES)
        )
        screenshot = await page.screenshot(full_page=True)
    finally:
        await context.close()
    return Capture(
        viewport=viewport,
        stabilized=stabilized,
        elements=[Element.model_validate(element) for element in collected],
        pixels=Image.open(io.BytesIO(screenshot)).convert("RGB"),
    )
