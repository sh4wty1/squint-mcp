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


def _is_resized(element: Element) -> bool:
    """Whether the element is painted at another size than it is laid out.

    `box` is painted and the box model is layout (ADR-0003): the two differ
    under a transform that scales, rotates or skews, on the element or on an
    ancestor. Scroll and client width are layout pixels, so the cut has no
    known place in the painted ones.
    """
    model = element.box_model
    layout_w = (
        model.content.w
        + model.padding.left
        + model.padding.right
        + model.border.left
        + model.border.right
    )
    layout_h = (
        model.content.h
        + model.padding.top
        + model.padding.bottom
        + model.border.top
        + model.border.bottom
    )
    # ponytail: a mirror or a half turn keeps both sizes and is read as no
    # transform, so the strip is read at the painted start of the text. The text
    # is still cut there; compare positions too if such a Finding proves wrong.
    return (
        abs(element.box.w - layout_w) >= config.TRANSFORM_MIN_SIZE_DIFF_PX
        or abs(element.box.h - layout_h) >= config.TRANSFORM_MIN_SIZE_DIFF_PX
    )


def _padding_right(element: Element) -> float:
    """The right edge of the padding box, in page coordinates."""
    return element.box.x + element.box_model.border.left + element.client_width


def _edge_strip(element: Element) -> Box:
    """The part of the padding box within one font-size of its right edge.

    A cut glyph is painted there. One font-size is wider than any gap between
    two letters, so the strip cannot fall entirely between glyphs.
    """
    border = element.box_model.border
    font_size = float(element.computed["font-size"].removesuffix("px"))
    right = _padding_right(element)
    left = max(element.box.x + border.left, right - font_size)
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
        # Hidden text is not cut for anyone, whatever is painted behind it.
        and computed["visibility"] == "visible"
        and _overflow_px(element) >= config.TEXT_CLIPPED_MIN_OVERFLOW_PX
        # Before the pixels: the strip is only where layout and paint coincide.
        and not _is_resized(element)
        # scrollWidth also counts an overflowing child: the text itself has to
        # pass the edge.
        and element.own_text_right is not None
        and element.own_text_right > _padding_right(element)
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
