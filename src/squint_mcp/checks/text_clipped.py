"""The `text-clipped` Check: text cut off horizontally by its own box."""

from PIL import Image

from squint_mcp import config
from squint_mcp.models import Box, Capture, Element, Evidence, Finding, Viewport
from squint_mcp.vision import is_flat

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


def _edge_strip(element: Element) -> Box:
    """The part of the padding box within one font-size of its right edge.

    A cut glyph is painted there. One font-size is wider than any gap between
    two letters, so the strip cannot fall entirely between glyphs.
    """
    border = element.box_model.border
    font_size = float(element.computed["font-size"].removesuffix("px"))
    padding_left = element.box.x + border.left
    right = padding_left + element.client_width
    left = max(padding_left, right - font_size)
    return Box(
        x=left,
        y=element.box.y + border.top,
        w=right - left,
        h=element.box.h - border.top - border.bottom,
    )


def _is_clipped(element: Element, pixels: Image.Image) -> bool:
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
        # The DOM says text overflows; the pixels say whether any of it is seen
        # being cut. A strip of one colour is hidden text or blank overflow.
        and not is_flat(pixels, _edge_strip(element))
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
        if _is_clipped(element, capture.pixels)
    ]
