"""The `low-contrast-real` Check: text too close in colour to what is painted behind it.

The background is read from the pixels, not from `background-color`, so it is right
over an image or a gradient (WCAG 2.2 SC 1.4.3).
"""

import math
import re

from squint_mcp import config
from squint_mcp.models import Capture, Element, Evidence, Finding, Viewport
from squint_mcp.vision import text_backgrounds

type Rgb = tuple[int, int, int]

# The styles that explain the contrast. `background-color` is what a tool that
# reads only the DOM would have compared the text with.
_EVIDENCE_PROPERTIES = (
    "color",
    "background-color",
    "background-image",
    "font-size",
    "font-weight",
)

# How Chromium serializes a computed sRGB colour.
# ponytail: a colour in another space (`oklch(...)`, `color(display-p3 ...)`) keeps
# its own syntax and the element is skipped; convert it if such text gets common.
_COLOR = re.compile(r"rgba?\((\d+), (\d+), (\d+)(?:, ([\d.]+))?\)")


def _luminance(color: Rgb) -> float:
    """The relative luminance of WCAG 2.2."""

    def linear(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = color
    return 0.2126 * linear(red) + 0.7152 * linear(green) + 0.0722 * linear(blue)


def _contrast(one: Rgb, other: Rgb) -> float:
    """The contrast ratio of WCAG 2.2, from 1 to 21."""
    lighter, darker = sorted((_luminance(one), _luminance(other)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _over(color: Rgb, alpha: float, behind: Rgb) -> Rgb:
    """`color` at `alpha` as seen over `behind`."""
    red, green, blue = (
        math.floor(alpha * front + (1 - alpha) * back + 0.5)
        for front, back in zip(color, behind, strict=True)
    )
    return red, green, blue


def _hex(color: Rgb) -> str:
    return "#{:02x}{:02x}{:02x}".format(*color)


def _worst_part(element: Element, capture: Capture) -> tuple[float, Rgb, Rgb] | None:
    """The contrast of the least readable part of the element's own text, with the
    text colour and the background there; None when the element has no text to judge.

    Text covered by another element's text is judged on that text's ink: the ink
    layer does not say whose glyph a pixel belongs to.
    """
    if not element.own_text:
        return None
    # A faded text is blended with what is behind its faded ancestor, which the
    # Capture does not hold: its real colour is not known.
    if element.opacity < 1:
        return None
    color = _COLOR.fullmatch(element.computed["color"])
    if color is None:
        return None
    text: Rgb = (int(color[1]), int(color[2]), int(color[3]))
    alpha = 1.0 if color[4] is None else float(color[4])
    # Text made transparent is hidden on purpose, as when an image replaces it.
    if alpha == 0:
        return None
    behind = text_backgrounds(capture.background, capture.ink, element.own_text_boxes)
    if not behind:
        return None
    # A translucent text is as dark as what shows through it.
    parts = sorted(
        (_contrast(seen, background), count, seen, background)
        for count, background in behind
        for seen in (_over(text, alpha, background),)
    )
    total = sum(count for _, count, _, _ in parts)
    # From the least readable colour up, the first one at which the share of the
    # text reached is the worst part. In integers: "exactly a tenth" is exact.
    reached = 0
    for ratio, count, seen, background in parts:
        reached += count
        if reached * 100 >= config.LOW_CONTRAST_WORST_PART_PERCENT * total:
            return ratio, seen, background
    raise AssertionError("the whole text is always reached")


def _required_ratio(element: Element) -> float:
    font_size = float(element.computed["font-size"].removesuffix("px"))
    bold = float(element.computed["font-weight"]) >= config.BOLD_MIN_WEIGHT
    large = font_size >= config.LARGE_TEXT_MIN_PX or (
        bold and font_size >= config.LARGE_BOLD_TEXT_MIN_PX
    )
    return config.CONTRAST_MIN_RATIO_LARGE if large else config.CONTRAST_MIN_RATIO


def _finding(
    element: Element,
    viewport: Viewport,
    ratio: float,
    required: float,
    text: Rgb,
    background: Rgb,
) -> Finding:
    # WCAG: a ratio is not rounded up to meet a threshold, so 4.478 is shown as 4.47.
    shown = math.floor(ratio * 100) / 100
    major = ratio < config.LOW_CONTRAST_MAJOR_BELOW_RATIO
    return Finding(
        check="low-contrast-real",
        category="a11y",
        severity="major" if major else "minor",
        message=(
            f"Text contrast {shown:.2f}:1 against the painted background "
            f"{_hex(background)} is below the {required:g}:1 minimum"
        ),
        selector=element.selector,
        text=element.text,
        box=element.box,
        viewport=viewport,
        evidence=Evidence(
            computed={name: element.computed[name] for name in _EVIDENCE_PROPERTIES},
            measured={
                "contrastRatio": shown,
                "requiredRatio": required,
                "textColor": _hex(text),
                "sampledBackground": _hex(background),
            },
        ),
        suggestion=(
            "Change the text colour or put a solid background behind the text "
            f"to reach {required:g}:1"
        ),
        source="WCAG 2.2 SC 1.4.3",
    )


def check(capture: Capture) -> list[Finding]:
    findings: list[Finding] = []
    for element in capture.elements:
        worst = _worst_part(element, capture)
        if worst is None:
            continue
        ratio, text, background = worst
        required = _required_ratio(element)
        if ratio < required:
            findings.append(
                _finding(element, capture.viewport, ratio, required, text, background)
            )
    return findings
