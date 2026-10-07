"""The `inspect_element` tool: one element as resolved and as painted."""

import asyncio
from typing import Annotated

from mcp.server.mcpserver import Context, Image
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from squint_mcp import config
from squint_mcp.capture import BrowserSession, capture
from squint_mcp.models import Box, BoxModel, Viewport
from squint_mcp.vision import SampledColor, crop_png, sample_colors


class InspectElementResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    viewport: Viewport
    stabilized: bool
    box: Box
    box_model: BoxModel
    computed: dict[str, str]
    sampled_colors: list[SampledColor]


async def inspect_element(
    url: str,
    selector: str,
    ctx: Context[BrowserSession],
    viewport: Viewport | None = None,
) -> Annotated[CallToolResult, InspectElementResult]:
    """Inspect one element of a rendered page.

    Opens `url` (http://, https:// or file://), waits for the page to settle and
    returns the element's computed styles, its box model in CSS pixels, the
    colours actually painted inside its box and a crop of it. `selector` is a CSS
    selector that must match exactly one element; it reaches into open shadow
    roots. `viewport` defaults to 1440x900. `stabilized` is false when the network
    never went idle. A call that takes longer than 30s fails. `box` is the element
    as painted, after transforms; `boxModel` is its layout, before them,
    for HTML elements. For SVG and MathML elements `boxModel.content` is still
    derived from the painted size.
    """
    viewport = viewport or Viewport(
        width=config.DEFAULT_VIEWPORT_WIDTH, height=config.DEFAULT_VIEWPORT_HEIGHT
    )
    try:
        # asyncio.timeout cancels once, so the capture's cleanup still gets to run.
        async with asyncio.timeout(config.TOTAL_TIMEOUT_S):
            captured = await capture(
                ctx.request_context.lifespan_context, url, viewport, selector
            )
    except TimeoutError as error:
        raise ToolError(f"Timed out after {config.TOTAL_TIMEOUT_S:g}s.") from error
    if not captured.elements:
        raise ToolError(f'Selector "{selector}" matched no elements.')
    if len(captured.elements) > 1:
        raise ToolError(
            f'Selector "{selector}" matched {len(captured.elements)} elements; '
            "it must match exactly one."
        )
    element = captured.elements[0]
    box = element.box
    sampled_colors = sample_colors(captured.pixels, box)
    if not sampled_colors:
        # No pixels to sample or crop: `display: none`, zero area, or off the page.
        raise ToolError(
            f'Selector "{selector}" matched an element with no rendered box.'
        )
    result = InspectElementResult(
        viewport=captured.viewport,
        stabilized=captured.stabilized,
        box=box,
        box_model=element.box_model,
        computed=element.computed,
        sampled_colors=sampled_colors,
    )
    state = "stabilized" if captured.stabilized else "not stabilized"
    summary = f"{selector}: {box.w:g}x{box.h:g} at ({box.x:g}, {box.y:g}), {state}"
    return CallToolResult(
        content=[
            TextContent(type="text", text=summary),
            Image(data=crop_png(captured.pixels, box), format="png").to_image_content(),
        ],
        structured_content=result.model_dump(mode="json", by_alias=True),
    )
