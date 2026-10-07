"""The `detect_visual_bugs` tool: runs Checks on a page and returns their Findings."""

from collections import Counter
from typing import Annotated, get_args

from mcp.server.mcpserver import Context
from mcp.types import CallToolResult, TextContent
from pydantic import BaseModel

from squint_mcp import config
from squint_mcp.capture import BrowserSession, capture
from squint_mcp.checks import CHECKS
from squint_mcp.models import Finding, Severity, Viewport

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
    viewports: list[Viewport] | None = None,
    checks: list[str] | None = None,
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
    and measurements that back it.
    """
    selected = [CHECKS[name] for name in checks or CHECKS]
    viewports = viewports or [
        Viewport(
            width=config.DEFAULT_VIEWPORT_WIDTH, height=config.DEFAULT_VIEWPORT_HEIGHT
        )
    ]
    session = ctx.request_context.lifespan_context
    # ponytail: one viewport after another, each paying a page load and the idle
    # wait; capture them concurrently if calls get slow.
    captures = [await capture(session, url, viewport, "*") for viewport in viewports]
    findings = [
        finding
        for captured in captures
        for check in selected
        for finding in check(captured)
    ]
    # A stable sort: within a severity, viewport order then document order remain.
    findings.sort(key=lambda finding: _SEVERITIES.index(finding.severity))
    result = DetectVisualBugsResult(
        findings=findings,
        captures=[
            CaptureSummary(viewport=captured.viewport, stabilized=captured.stabilized)
            for captured in captures
        ],
    )
    return CallToolResult(
        content=[TextContent(type="text", text=_summary(findings, len(captures)))],
        structured_content=result.model_dump(mode="json", by_alias=True),
    )
