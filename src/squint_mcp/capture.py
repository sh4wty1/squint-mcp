"""Capture production: the only module allowed to import `playwright` (ADR-0002)."""

import asyncio
import io
import json
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from mcp.server.mcpserver.exceptions import ToolError
from PIL import Image, ImageChops
from playwright.async_api import (
    Browser,
    FloatRect,
    Page,
    Playwright,
    StorageState,
    async_playwright,
)
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from squint_mcp import config, covered
from squint_mcp.models import (
    Capture,
    Cover,
    CoveredText,
    Element,
    Face,
    LineWidths,
    Viewport,
)

_JS = Path(__file__).parent / "js"
_STABILIZE = (_JS / "stabilize.js").read_text(encoding="utf-8")
_COLLECT_ELEMENTS = (_JS / "collect_elements.js").read_text(encoding="utf-8")
_FILL_TEXT = (_JS / "fill_text.js").read_text(encoding="utf-8")
_SCROLL_WIDTH = (_JS / "scroll_width.js").read_text(encoding="utf-8")
_COVERED_TEXT = (_JS / "covered_text.js").read_text(encoding="utf-8")
_FONT_WIDTHS = (_JS / "font_widths.js").read_text(encoding="utf-8")
_SRGB_COLORS = (_JS / "srgb_colors.js").read_text(encoding="utf-8")
# Calls a method of the object the cover script leaves on the page.
_COVERED_CALL = "([method, ...args]) => globalThis.__squintCovered[method](...args)"
# Resolves once the page has painted two frames: whatever changed before the call
# is on the screen by then. `requestAnimationFrame` is the one of the page's own
# world, and a page can put a function there that never calls back: the timer
# ends the wait then, `most` milliseconds on.
_PAINTED = (
    "(most) => new Promise((done) => {"
    " requestAnimationFrame(() => requestAnimationFrame(done));"
    " setTimeout(done, most); })"
)


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
                    self._browser = await self._playwright.chromium.launch(
                        args=list(config.CHROMIUM_ARGS)
                    )
                except PlaywrightError as error:
                    raise ToolError(
                        f"Could not launch Chromium: {_first_line(error)}. "
                        # This interpreter, so the fix reaches the environment
                        # the server runs in, uvx cache or checkout alike.
                        "If it is not installed, run: "
                        f'"{sys.executable}" -m playwright install chromium'
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


def _read_storage_state(path: str) -> StorageState:
    """The storage state of the file at `path`, read whole. No message quotes the
    file: it holds the cookies of a session."""
    if not Path(path).is_absolute():
        raise ToolError(f'storageState must be an absolute path: "{path}".')
    try:
        data = Path(path).read_bytes()
    except OSError as error:
        reason = error.strerror or type(error).__name__
        raise ToolError(
            f'Could not read the storage state "{path}": {reason}.'
        ) from None
    try:
        # Bytes that are not UTF-8 raise a ValueError too.
        state = json.loads(data.decode("utf-8"))
    except ValueError:
        state = None
    if not isinstance(state, dict):
        raise ToolError(f'"{path}" is not a Playwright storage state.')
    # Its shape is Playwright's to judge, when the context is created.
    return cast(StorageState, state)


def _first_line(error: PlaywrightError) -> str:
    """Playwright appends call logs and banners; the first line says what failed."""
    return error.message.splitlines()[0]


async def _settle_layout(page: Page) -> None:
    """Have Chromium lay the page out as its screenshots will show it.

    On Windows the first screenshot that reaches beyond the viewport changes the
    font of the generic `monospace` family, and the page is laid out again: boxes
    read before it are of another layout than the pixels (issue #18, AD-006). A
    small one taken first, and thrown away, leaves one layout for both. Linux does
    not show the fault, so no test holds this.
    """
    corner = FloatRect(x=0, y=0, width=16, height=16)
    try:
        await page.screenshot(full_page=True, clip=corner)
    except PlaywrightError:
        # Chromium now and then fails to capture a small clip: once more.
        await page.screenshot(full_page=True, clip=corner)


async def _screenshot(page: Page, clip: covered.Bounds | None = None) -> Image.Image:
    """The full page, or the part of it inside `clip`, in page coordinates.

    Taken right after a change of style, a screenshot now and then shows a part
    of the page beyond the viewport not painted yet, and what is read there is
    a page with nothing on it (AD-007): the page paints two frames first.
    """
    await page.evaluate(_PAINTED, config.PAINT_WAIT_MAX_S * 1000)
    if clip is None:
        shot = await page.screenshot(full_page=True)
    else:
        left, top, right, bottom = clip
        part = FloatRect(x=left, y=top, width=right - left, height=bottom - top)
        shot = await page.screenshot(full_page=True, clip=part)
    return Image.open(io.BytesIO(shot)).convert("RGB")


async def _filled(page: Page, color: str) -> Image.Image:
    """The page with every glyph painted in `color`."""
    await page.evaluate(_FILL_TEXT, color)
    return await _screenshot(page)


async def _covered(page: Page, method: str, *arguments: object) -> Any:
    """Call `method` of the object the cover script left on the page."""
    return await page.evaluate(_COVERED_CALL, [method, *arguments])


async def _ink_layers(page: Page, clip: covered.Bounds | None = None) -> covered.Layers:
    """The ink of the glyphs marked on each channel, in what the page now shows:
    a screenshot with them in the colour of their channel against one with them
    in black.
    """
    await _covered(page, "ink", True)
    on = await _screenshot(page, clip)
    await _covered(page, "ink", False)
    return covered.ink_layers(on, await _screenshot(page, clip))


async def _alone(
    page: Page, texts: list[covered.Text], with_layers: bool
) -> dict[int, Image.Image]:
    """The ink of each of `texts`, by its index, with only them and what is inside
    them painted, and their Silent layers `with_layers`: one pair of screenshots,
    clipped to them.
    """
    await _covered(page, "show", "alone", [text.index for text in texts], with_layers)
    clip = covered.bounds_of(texts)
    # The texts of a group are all marked on the first channel.
    ink = (await _ink_layers(page, clip))[0]
    return {text.index: covered.part(ink, clip, text.bounds) for text in texts}


async def _measure_covered_text(
    page: Page, elements: list[Element], pixels: Image.Image
) -> None:
    """Give the elements whose own text may be covered their `covered_text` (AD-005).

    Phase 1 reads the ink of every text from full-page screenshots and leaves
    out the texts that cannot reach the reporting threshold. Phase 2 measures
    the others alone, in screenshots clipped to them. Hit testing then says
    what is over the Hidden ink of those at or over the threshold.
    """
    found = await page.evaluate(
        _COVERED_TEXT, {"roles": list(config.SILENT_LAYER_ROLES)}
    )
    texts = covered.read_texts(found, elements, pixels)
    # Phase 1: the ink of every text on the page as it is, and with only the
    # glyphs painted.
    painted: list[covered.Layers] = []
    glyphs: list[covered.Layers] = []
    for turn in range(covered.assign_channels(texts)):
        members = [text for text in texts if text.round == turn]
        await _covered(
            page, "mark", {str(text.index): text.channel for text in members}
        )
        await _covered(page, "show", "page")
        painted.append(await _ink_layers(page))
        await _covered(page, "show", "glyphs", [text.index for text in members])
        glyphs.append(await _ink_layers(page))
    candidates = [
        text
        for text in texts
        if covered.may_be_covered(text, glyphs[text.round], painted[text.round])
    ]

    # Phase 2: the ink of each text left, alone and with its Silent layers.
    alone: dict[int, Image.Image] = {}
    layered: dict[int, Image.Image] = {}
    for group in covered.groups(candidates):
        await _covered(page, "mark", {str(text.index): 0 for text in group})
        alone |= await _alone(page, group, False)
        # The texts with the same Silent layers are painted with them together.
        for layers in sorted({text.layers for text in group if text.layers}):
            members = [text for text in group if text.layers == layers]
            layered |= await _alone(page, members, True)

    # Hit testing asks the page as it is painted.
    await _covered(page, "show", "page")
    tested: list[CoveredText] = []
    jobs: list[dict[str, object]] = []
    for text in candidates:
        ink, hidden, where = covered.hidden_ink(
            text,
            alone[text.index],
            painted[text.round][text.channel].crop(text.bounds),
            # A text with no Silent layer is as seen with them as alone.
            layered.get(text.index, alone[text.index]),
        )
        measured = CoveredText(ink=ink, hidden=hidden, covers=[])
        elements[text.index].covered_text = measured
        # Under the reporting threshold nothing asks what covers the text.
        if hidden and hidden * 100 >= config.OVERLAP_MIN_HIDDEN_PERCENT * ink:
            tested.append(measured)
            jobs.append(
                {"index": text.index, "runs": covered.runs(where, text.bounds[:2])}
            )
    if not jobs:
        return
    step = covered.hit_step(sum(measured.hidden for measured in tested))
    hits = await _covered(page, "hit", jobs, step)
    for measured, covers in zip(tested, hits, strict=True):
        for cover in covers:
            place: int = cover["index"]
            measured.covers.append(
                Cover(
                    selector=elements[place].selector,
                    pixels=cover["pixels"],
                    raised=cover["raised"],
                )
            )


async def _measure_fonts(page: Page, elements: list[Element]) -> list[Face]:
    """Give the elements whose own text asks first for a family with a face that
    failed their `line_widths`, and return the faces of the page (AD-008).
    """
    found = await page.evaluate(
        _FONT_WIDTHS, {"shaping": list(config.TEXT_SHAPING_PROPERTIES)}
    )
    for index, widths in found["widths"].items():
        elements[int(index)].line_widths = LineWidths.model_validate(widths)
    return [Face.model_validate(face) for face in found["faces"]]


async def _srgb_colors(page: Page, elements: list[Element]) -> dict[str, str]:
    """The computed colours of `elements` that Chromium does not write as `rgb()`
    or `rgba()`, each as the browser converts it to sRGB (AD-009).

    A text the browser does not convert is left out, and a page with no such
    colour is asked nothing.
    """
    texts = sorted(
        {
            color
            for element in elements
            for name in config.CAPTURE_COLOR_PROPERTIES
            if not (color := element.computed[name]).startswith("rgb")
        }
    )
    if not texts:
        return {}
    converted = await page.evaluate(_SRGB_COLORS, texts)
    return {
        text: srgb
        for text, srgb in zip(texts, converted, strict=True)
        if srgb is not None
    }


async def capture(
    session: BrowserSession,
    url: str,
    viewport: Viewport,
    selector: str,
    *,
    covered_text: bool = False,
    fonts: bool = False,
    descendants: bool = False,
    storage_state: str | None = None,
) -> Capture:
    """Open `url` in a fresh context, stabilize it and capture it.

    The Capture holds the elements matched by `selector`, which reaches into
    open shadow roots; `*` is every element of the page. With `descendants`, it
    also holds every element under a match, each once. With `covered_text`,
    the elements whose own text may be covered also say how much of it is. With
    `fonts`, the Capture holds the faces of the page, and the elements whose
    font may not have loaded say how wide their own text is on one line. With
    `storage_state`, the path of a Playwright storage state file, the context
    starts with its cookies and `localStorage`; the file is never written.
    """
    scheme = urlsplit(url).scheme
    if scheme not in ("http", "https", "file"):
        raise ToolError(
            f'Unsupported URL scheme "{scheme}"; use http://, https:// or file://.'
        )
    state = None if storage_state is None else _read_storage_state(storage_state)
    browser = await session.browser()
    try:
        context = await browser.new_context(
            viewport={"width": viewport.width, "height": viewport.height},
            device_scale_factor=1,
            storage_state=state,
        )
    except PlaywrightError:
        if state is None:
            raise
        # Playwright's message may quote the file.
        raise ToolError(
            f'"{storage_state}" is not a Playwright storage state.'
        ) from None
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
        # Before anything is measured: boxes and pixels are of one layout.
        await _settle_layout(page)
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
                "descendants": descendants,
            },
        )
        elements = [Element.model_validate(element) for element in collected]
        # Right after the collector and before the pixels: it changes nothing
        # on the page.
        srgb = await _srgb_colors(page, elements)
        scroll_width = await page.evaluate(_SCROLL_WIDTH)
        pixels = await _screenshot(page)
        # After the collector, which reads the page's own styles, and after the
        # pixels: from here on the text is not painted as the page asked (AD-004).
        # ponytail: every Capture pays for the three layers, whatever reads them;
        # take them on request, as covered text is, if calls get slow.
        background = await _filled(page, "transparent")
        black = await _filled(page, "rgb(0, 0, 0)")
        white = await _filled(page, "rgb(255, 255, 255)")
        faces = None
        if fonts:
            # After the pixels, so that nothing it does can reach them; before
            # covered text, which scrolls the page.
            faces = await _measure_fonts(page, elements)
        if covered_text:
            # Last: it repaints the page, hides parts of it and scrolls it.
            await _measure_covered_text(page, elements, pixels)
    finally:
        # A client cancellation keeps cancelling every await: shield the close.
        await asyncio.shield(context.close())
    return Capture(
        viewport=viewport,
        stabilized=stabilized,
        elements=elements,
        srgb=srgb,
        scroll_width=scroll_width,
        pixels=pixels,
        background=background,
        # Only glyphs differ between the two fills, by how much they cover a pixel.
        ink=ImageChops.difference(black, white).convert("L"),
        faces=faces,
    )
