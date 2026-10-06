"""The `inspect_element` tool: what the browser resolved for one element."""

from typing import Annotated

from mcp.server.mcpserver import Context
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from squint_mcp import config
from squint_mcp.capture import BrowserSession, capture
from squint_mcp.models import Box, BoxModel, Viewport


class InspectElementResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    viewport: Viewport
    stabilized: bool
    box: Box
    box_model: BoxModel
    computed: dict[str, str]


async def inspect_element(
    url: str,
    selector: str,
    ctx: Context[BrowserSession],
    viewport: Viewport | None = None,
) -> Annotated[CallToolResult, InspectElementResult]:
    """Inspect one element of a rendered page.

    Opens `url` (http://, https:// or file://), waits for the page to settle and
    returns the element's computed styles and box model in CSS pixels. `selector`
    is a CSS selector that must match exactly one element; it reaches into open
    shadow roots. `viewport` defaults to 1440x900. `stabilized` is false when the
    network never went idle.
    """
    viewport = viewport or Viewport(
        width=config.DEFAULT_VIEWPORT_WIDTH, height=config.DEFAULT_VIEWPORT_HEIGHT
    )
    captured = await capture(
        ctx.request_context.lifespan_context, url, viewport, selector
    )
    element = captured.elements[0]
    box = element.box
    result = InspectElementResult(
        viewport=captured.viewport,
        stabilized=captured.stabilized,
        box=box,
        box_model=element.box_model,
        computed=element.computed,
    )
    state = "stabilized" if captured.stabilized else "not stabilized"
    summary = f"{selector}: {box.w:g}x{box.h:g} at ({box.x:g}, {box.y:g}), {state}"
    return CallToolResult(
        content=[TextContent(type="text", text=summary)],
        structured_content=result.model_dump(mode="json", by_alias=True),
    )
