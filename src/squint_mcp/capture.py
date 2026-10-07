"""Capture production: the only module allowed to import `playwright` (ADR-0002)."""

import asyncio
import io
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlsplit

from mcp.server.mcpserver.exceptions import ToolError
from PIL import Image
from playwright.async_api import Browser, Playwright, async_playwright
from playwright.async_api import Error as PlaywrightError
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
            # A browser that crashed or was closed is launched again.
            if self._browser is None or not self._browser.is_connected():
                try:
                    self._playwright = (
                        self._playwright or await async_playwright().start()
                    )
                    self._browser = await self._playwright.chromium.launch()
                except PlaywrightError as error:
                    raise ToolError(
                        f"Could not launch Chromium: {_first_line(error)}. "
                        "If it is not installed, run: playwright install chromium"
                    ) from error
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


def _first_line(error: PlaywrightError) -> str:
    """Playwright appends call logs and banners; the first line says what failed."""
    return error.message.splitlines()[0]


async def capture(
    session: BrowserSession, url: str, viewport: Viewport, selector: str
) -> Capture:
    """Open `url` in a fresh context, stabilize it and capture it.

    The Capture holds the elements matched by `selector`, which reaches into
    open shadow roots; `*` is every element of the page.
    """
    scheme = urlsplit(url).scheme
    if scheme not in ("http", "https", "file"):
        raise ToolError(
            f'Unsupported URL scheme "{scheme}"; use http://, https:// or file://.'
        )
    browser = await session.browser()
    context = await browser.new_context(
        viewport={"width": viewport.width, "height": viewport.height},
        device_scale_factor=1,
    )
    try:
        # The tool's total timeout is the only clock; Playwright's own would race it.
        context.set_default_timeout(0)
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="load")
        except PlaywrightError as error:
            raise ToolError(f"Could not load {url}: {_first_line(error)}") from error
        await page.evaluate(_STABILIZE)
        try:
            await page.wait_for_load_state(
                "networkidle", timeout=config.NETWORK_IDLE_TIMEOUT_S * 1000
            )
            stabilized = True
        except PlaywrightTimeoutError:
            # Polling and analytics keep some pages busy forever: capture them anyway.
            stabilized = False
        matches = page.locator(f"css={selector}")
        try:
            # count() only parses and runs the selector: a failure is its syntax.
            await matches.count()
        except PlaywrightError as error:
            raise ToolError(f'Invalid selector "{selector}".') from error
        collected = await matches.evaluate_all(
            _COLLECT_ELEMENTS,
            {
                "properties": list(config.CAPTURE_COMPUTED_PROPERTIES),
                "textLimit": config.TEXT_EXCERPT_MAX_CHARS,
                "transformMinSizeDiffPx": config.TRANSFORM_MIN_SIZE_DIFF_PX,
            },
        )
        screenshot = await page.screenshot(full_page=True)
    finally:
        # A client cancellation keeps cancelling every await: shield the close.
        await asyncio.shield(context.close())
    return Capture(
        viewport=viewport,
        stabilized=stabilized,
        elements=[Element.model_validate(element) for element in collected],
        pixels=Image.open(io.BytesIO(screenshot)).convert("RGB"),
    )
