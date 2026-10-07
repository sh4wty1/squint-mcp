"""The `text-clipped` Check: text cut off horizontally by its own box."""

from squint_mcp import config
from squint_mcp.models import Capture, Element, Evidence, Finding, Viewport

# The styles that explain the cut.
_EVIDENCE_PROPERTIES = (
    "overflow-x",
    "white-space",
    "text-overflow",
    "width",
    "font-size",
)


def _overflow_px(element: Element) -> int:
    return element.scroll_width - element.client_width


def _is_clipped(element: Element) -> bool:
    computed = element.computed
    return (
        element.own_text
        # `auto` and `scroll` leave the text reachable by scrolling.
        and computed["overflow-x"] in ("hidden", "clip")
        # An ellipsis is a cut the author asked for.
        and computed["text-overflow"] == "clip"
        # Right-to-left text is cut on the other edge.
        and computed["direction"] == "ltr"
        and _overflow_px(element) >= config.TEXT_CLIPPED_MIN_OVERFLOW_PX
    )


def _finding(element: Element, viewport: Viewport) -> Finding:
    overflow_px = _overflow_px(element)
    major = overflow_px >= config.TEXT_CLIPPED_MAJOR_OVERFLOW_PX
    return Finding(
        check="text-clipped",
        category="visual-bug",
        severity="major" if major else "minor",
        message=f"Text clipped by {overflow_px}px by its container width",
        selector=element.selector,
        text=element.text,
        box=element.box,
        viewport=viewport,
        evidence=Evidence(
            computed={name: element.computed[name] for name in _EVIDENCE_PROPERTIES},
            measured={
                "overflowPx": overflow_px,
                "scrollWidth": element.scroll_width,
                "clientWidth": element.client_width,
            },
        ),
        suggestion="Allow wrapping or reduce font-size at this width",
        source="Squint heuristic",
    )


def check(capture: Capture) -> list[Finding]:
    return [
        _finding(element, capture.viewport)
        for element in capture.elements
        if _is_clipped(element)
    ]
