"""The `detect_visual_bugs` tool: runs Checks on a page and returns their Findings."""

import asyncio
from collections import Counter
from typing import Annotated, get_args

from mcp.server.mcpserver import Context, Image
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel, Field

from squint_mcp import config
from squint_mcp.capture import BrowserSession, capture
from squint_mcp.checks import CHECKS
from squint_mcp.models import Finding, Severity, Viewport
from squint_mcp.vision import crop_png

# Most severe first.
_SEVERITIES: tuple[Severity, ...] = get_args(Severity)


class CaptureSummary(BaseModel):
    viewport: Viewport
    stabilized: bool


class DetectVisualBugsResult(BaseModel):
    findings: list[Finding]
    captures: list[CaptureSummary]


def _count(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _summary(findings: list[Finding], viewports: int) -> str:
    where = f"in {_count(viewports, 'viewport')}"
    if not findings:
        return f"No findings {where}."
    by_severity = Counter(finding.severity for finding in findings)
    severities = ", ".join(
        f"{by_severity[severity]} {severity}"
        for severity in _SEVERITIES
        if by_severity[severity]
    )
    return f"Found {_count(len(findings), 'finding')} {where}: {severities}."


async def detect_visual_bugs(
    url: str,
    ctx: Context[BrowserSession],
    viewports: Annotated[list[Viewport], Field(min_length=1)] | None = None,
    checks: Annotated[list[str], Field(min_length=1)] | None = None,
) -> Annotated[CallToolResult, DetectVisualBugsResult]:
    """Find visual bugs in a rendered page, without a baseline.

    Opens `url` (http://, https:// or file://) once per viewport, waits for the
    page to settle and runs Checks that cross what the DOM reports with what is
    painted. `viewports` defaults to one of 1440x900. `checks` names the Checks
    to run and defaults to all of them: `text-clipped` (text cut off
    horizontally by its own box). Returns `findings`, most severe first, and
    `captures`, one per viewport, whose `stabilized` is false when the network
    never went idle. Each Finding names its element by a `selector` that is
    unique on the page and works in `inspect_element`, and carries the styles
    and measurements that back it. The five most severe Findings also get a
    crop of their element: `evidence.cropIndex` is the position of that image
    among the images of the response, or null. A call that takes longer than
    30s, all viewports together, fails.
    """
    # A repeated Check name or viewport counts once, at its first place.
    names = list(dict.fromkeys(checks or CHECKS))
    # Before any browser work: a wrong call should not pay for a page load.
    for name in names:
        if name not in CHECKS:
            valid = ", ".join(sorted(CHECKS))
            raise ToolError(f'Unknown check "{name}". Valid checks: {valid}.')
    viewports = viewports or [
        Viewport(
            width=config.DEFAULT_VIEWPORT_WIDTH, height=config.DEFAULT_VIEWPORT_HEIGHT
        )
    ]
    viewports = list({(v.width, v.height): v for v in viewports}.values())
    session = ctx.request_context.lifespan_context
    try:
        # One clock for the whole call. asyncio.timeout cancels once, so the
        # cleanup of the capture under way still gets to run.
        async with asyncio.timeout(config.TOTAL_TIMEOUT_S):
            # ponytail: one viewport after another, each paying a page load and
            # the idle wait; capture them concurrently if calls get slow.
            captures = [
                await capture(session, url, viewport, "*") for viewport in viewports
            ]
    except TimeoutError as error:
        raise ToolError(f"Timed out after {config.TOTAL_TIMEOUT_S:g}s.") from error
    found = [
        (finding, captured)
        for captured in captures
        for name in names
        for finding in CHECKS[name](captured)
    ]
    # A stable sort: within a severity, viewport order then document order remain.
    found.sort(key=lambda pair: _SEVERITIES.index(pair[0].severity))
    # Only here is every Finding of the call known: the most severe get the crops.
    crops = [
        Image(data=crop_png(captured.pixels, finding.box), format="png")
        for finding, captured in found[: config.MAX_CROPS]
    ]
    findings = [finding for finding, _ in found]
    for index, finding in enumerate(findings[: config.MAX_CROPS]):
        finding.evidence.crop_index = index
    result = DetectVisualBugsResult(
        findings=findings,
        captures=[
            CaptureSummary(viewport=captured.viewport, stabilized=captured.stabilized)
            for captured in captures
        ],
    )
    return CallToolResult(
        content=[
            TextContent(type="text", text=_summary(findings, len(captures))),
            *(crop.to_image_content() for crop in crops),
        ],
        structured_content=result.model_dump(mode="json", by_alias=True),
    )
