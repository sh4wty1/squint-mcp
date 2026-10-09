"""The `offscreen-overflow` Check: the element that makes the page scroll sideways."""

from squint_mcp import config
from squint_mcp.models import Capture, Element, Evidence, Finding

# The styles that explain the width.
_EVIDENCE_PROPERTIES = ("display", "position", "width", "white-space")

_HIDDEN = ("hidden", "clip")


def _computed(capture: Capture, tag: str, name: str) -> str | None:
    """A computed style of the first `tag` element of the page."""
    for element in capture.elements:
        if element.tag == tag:
            return element.computed[name]
    return None


def _scrolls_to_the_right(capture: Capture) -> bool:
    """Whether what passes the viewport's right edge can be scrolled to.

    The `overflow-x` of the viewport is that of `html`, or that of `body` while
    that of `html` is `visible`. A right-to-left page scrolls to the left.
    """
    html = _computed(capture, "html", "overflow-x")
    body = _computed(capture, "body", "overflow-x")
    hidden = html in _HIDDEN or (html == "visible" and body in _HIDDEN)
    return not hidden and _computed(capture, "body", "direction") != "rtl"


def _reach(element: Element) -> float:
    """How far right the element goes: its box or its own text, whichever is further."""
    right = element.box.x + element.box.w
    if element.own_text_right is None:
        return right
    return max(right, element.own_text_right)


def check(capture: Capture) -> list[Finding]:
    # The full-page pixels are as wide as the page scrolls.
    page_width = capture.pixels.width
    viewport_width = capture.viewport.width
    if page_width <= viewport_width or not _scrolls_to_the_right(capture):
        return []
    overflow_px = page_width - viewport_width
    for element in capture.elements:
        # The first in document order: of a wide element and the children that
        # fill it, the element.
        # ponytail: an element cut by an ancestor, or fixed, that ends on the
        # page's edge by coincidence is named too; the Capture holds no clip
        # chain to tell it apart.
        distance = abs(page_width - _reach(element))
        if distance < config.OFFSCREEN_OVERFLOW_EDGE_TOLERANCE_PX:
            return [
                Finding(
                    check="offscreen-overflow",
                    category="responsive",
                    severity="major",
                    message=(
                        f"Extends {overflow_px}px past the {viewport_width}px "
                        "viewport, so the page scrolls horizontally"
                    ),
                    selector=element.selector,
                    text=element.text,
                    box=element.box,
                    viewport=capture.viewport,
                    evidence=Evidence(
                        computed={
                            name: element.computed[name]
                            for name in _EVIDENCE_PROPERTIES
                        },
                        measured={
                            "overflowPx": overflow_px,
                            "pageWidth": page_width,
                            "viewportWidth": viewport_width,
                        },
                    ),
                    suggestion="Keep the element within the viewport width",
                    source="Squint heuristic",
                )
            ]
    # A pseudo-element sets the width: no element to name.
    return []
