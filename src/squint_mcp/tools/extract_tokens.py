"""The `extract_tokens` tool: the design tokens a page uses."""

import asyncio
from typing import Annotated

from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent

from squint_mcp import config
from squint_mcp.capture import BrowserSession, capture
from squint_mcp.models import Viewport
from squint_mcp.tokens import Tokens, extract


class ExtractTokensResult(Tokens):
    viewport: Viewport
    stabilized: bool
    scope: str | None


async def extract_tokens(
    url: str,
    ctx: Context[BrowserSession],
    scope: str | None = None,
    viewport: Viewport | None = None,
) -> Annotated[CallToolResult, ExtractTokensResult]:
    """Extract the design tokens a rendered page uses.

    Opens `url` (http://, https:// or file://), waits for the page to settle and
    returns the values its elements are styled with, each with the number of
    elements that use it: `colors` (by role: text, background, border),
    `typography` (`families`, `sizes`, `weights`, `lineHeights`), `spacing` in
    px (by role: margin, padding, gap), `radii` (the computed text of a corner:
    `4px`, `50%`, `10px 20px`) and `shadows` (the whole computed text, with a
    `kind`: `box` or `text`).

    A colour is `#rrggbb` in sRGB whatever notation the page wrote it in, or
    `#rrggbbaa` when it is not opaque, and a text colour is the one the text is
    filled with. Colours of one alpha whose ΔE2000 is below 2 are one token, and
    so are font sizes, line heights, spacings and px radii less than 1px apart:
    its `value` is the most used of them, and `variants` lists each with its own
    count. A line height of `normal` is
    not counted, nor a margin of `auto`, nor the gap of an element that is not a
    flex or grid container.

    `scope`, a CSS selector that reaches into open shadow roots, narrows the
    reading to its matches and every element under them. `elements` is the
    number of elements read: those that paint a box, are visible and are not
    under an opacity of 0. `viewport` defaults to 1440x900.
    `stabilized` is false when the network never went idle. A call that takes
    longer than 30s fails.
    """
    viewport = viewport or Viewport(
        width=config.DEFAULT_VIEWPORT_WIDTH, height=config.DEFAULT_VIEWPORT_HEIGHT
    )
    try:
        # asyncio.timeout cancels once, so the capture's cleanup still gets to run.
        async with asyncio.timeout(config.TOTAL_TIMEOUT_S):
            captured = await capture(
                ctx.request_context.lifespan_context,
                url,
                viewport,
                "*" if scope is None else scope,
                descendants=scope is not None,
            )
    except TimeoutError as error:
        raise ToolError(f"Timed out after {config.TOTAL_TIMEOUT_S:g}s.") from error
    result = ExtractTokensResult(
        **dict(extract(captured)),
        viewport=captured.viewport,
        stabilized=captured.stabilized,
        scope=scope,
    )
    typography = result.typography
    totals = {
        "colors": result.colors.total,
        "font families": typography.families.total,
        "font sizes": typography.sizes.total,
        "font weights": typography.weights.total,
        "line heights": typography.line_heights.total,
        "spacing": result.spacing.total,
        "radii": result.radii.total,
        "shadows": result.shadows.total,
    }
    counts = ", ".join(f"{name} {total}" for name, total in totals.items())
    state = "stabilized" if captured.stabilized else "not stabilized"
    summary = f"Tokens: {counts}; elements {result.elements}; {state}."
    return CallToolResult(
        content=[TextContent(type="text", text=summary)],
        structured_content=result.model_dump(mode="json", by_alias=True),
    )
