"""The `offscreen-overflow` Check: the element that makes the page scroll sideways."""

from squint_mcp import config
from squint_mcp.models import Capture, Element, Evidence, Finding

# The styles that explain the width.
_EVIDENCE_PROPERTIES = ("display", "position", "width", "white-space")


def _styles(capture: Capture, tag: str) -> dict[str, str]:
    """The computed styles of the first `tag` element; none where the page has none."""
    for element in capture.elements:
        if element.tag == tag:
            return element.computed
    return {}


def _scrolls_right(capture: Capture) -> bool:
    """Whether what passes the right edge of the viewport is reached by scrolling."""
    # The viewport takes the overflow of `html`, or that of `body` while `html`
    # leaves its own `visible`.
    overflow_x = _styles(capture, "html").get("overflow-x", "visible")
    body = _styles(capture, "body")
    if overflow_x == "visible":
        overflow_x = body.get("overflow-x", "visible")
    return (
        # The full-page pixels are as wide as the content even when the page hides
        # it. Off-canvas menus are built that way on purpose.
        overflow_x not in ("hidden", "clip")
        # A right-to-left page scrolls to the left, where the pixels do not reach.
        and body.get("direction") != "rtl"
    )


def _reach(element: Element) -> float:
    """How far right the element goes: its box or its own text, whichever is further."""
    right = element.box.x + element.box.w
    if element.own_text_right is None:
        return right
    return max(right, element.own_text_right)


def _finding(element: Element, capture: Capture) -> Finding:
    page_width = capture.pixels.width
    viewport_width = capture.viewport.width
    overflow_px = page_width - viewport_width
    return Finding(
        check="offscreen-overflow",
        category="responsive",
        severity="major",
        message=(
            f"Extends {overflow_px}px past the {viewport_width}px viewport, "
            "so the page scrolls horizontally"
        ),
        selector=element.selector,
        text=element.text,
        box=element.box,
        viewport=capture.viewport,
        evidence=Evidence(
            computed={name: element.computed[name] for name in _EVIDENCE_PROPERTIES},
            measured={
                "overflowPx": overflow_px,
                "pageWidth": page_width,
                "viewportWidth": viewport_width,
            },
        ),
        suggestion="Keep it within the viewport width or let its content wrap",
        source="Squint heuristic",
    )


def check(capture: Capture) -> list[Finding]:
    # The full-page pixels are as wide as the page scrolls.
    page_width = capture.pixels.width
    if page_width <= capture.viewport.width or not _scrolls_right(capture):
        return []
    # One Finding: the first element in document order that ends on the page's
    # right edge is the one that sets the width, not the children that fill it.
    # ponytail: an element clipped by an ancestor or fixed to the viewport that
    # happens to end there, before the real one, is named instead; the Capture
    # would need the clip chain of each element to tell them apart.
    for element in capture.elements:
        distance = abs(page_width - _reach(element))
        if distance < config.OFFSCREEN_OVERFLOW_EDGE_TOLERANCE_PX:
            return [_finding(element, capture)]
    return []
