"""The `overlap` Check: text that another element is painted over.

How much of a text is hidden is read from the pixels, by the Capture (AD-005):
the boxes of two elements cross on most pages without either hiding the other.
"""

import re

from squint_mcp import config
from squint_mcp.models import (
    Capture,
    Cover,
    CoveredText,
    Element,
    Evidence,
    Finding,
    Severity,
    Viewport,
)

# The styles of the covered element that decide what is painted above it.
_EVIDENCE_PROPERTIES = ("position", "z-index")

# How Chromium serializes a computed sRGB colour, as in `low_contrast_real`.
_COLOR = re.compile(r"rgba?\((\d+), (\d+), (\d+)(?:, ([\d.]+))?\)")


def _is_transparent(element: Element) -> bool:
    """Whether the glyphs of the element are painted with a colour of alpha 0."""
    color = _COLOR.fullmatch(element.computed["-webkit-text-fill-color"])
    return color is not None and color[4] is not None and float(color[4]) == 0


def _coverer(element: Element) -> tuple[CoveredText, Cover] | None:
    """What is measured of the own text of the element and the Other element that
    covers it; None when the text is not covered enough to be reported.
    """
    covered = element.covered_text
    # Text that is clipped away, hidden or faded out has no ink to cover.
    if covered is None or covered.ink == 0:
        return None
    # Text made transparent is hidden on purpose, as when an image replaces it.
    if _is_transparent(element):
        return None
    # In integers: "exactly a tenth" is exact.
    if covered.hidden * 100 < config.OVERLAP_MIN_HIDDEN_PERCENT * covered.ink:
        return None
    # Hit testing gave nothing over the hidden ink, as under a cover of
    # `pointer-events: none`: there is no element to name.
    if not covered.covers:
        return None
    # The covers are in document order and `max` keeps the first of the largest.
    return covered, max(covered.covers, key=lambda cover: cover.pixels)


def _finding(
    element: Element, viewport: Viewport, covered: CoveredText, coverer: Cover
) -> Finding:
    major = covered.hidden * 100 >= config.OVERLAP_MAJOR_HIDDEN_PERCENT * covered.ink
    severity: Severity = "major" if major else "minor"
    # A cover given a positive `z-index` was more often than not put on top on
    # purpose: one level lower.
    if coverer.raised:
        severity = "minor" if major else "info"
    # Truncated, so the share shown never contradicts the severity next to it.
    percent = covered.hidden * 100 // covered.ink
    return Finding(
        check="overlap",
        category="visual-bug",
        severity=severity,
        message=f"{percent}% of the text is covered by another element",
        selector=element.selector,
        text=element.text,
        box=element.box,
        viewport=viewport,
        evidence=Evidence(
            computed={name: element.computed[name] for name in _EVIDENCE_PROPERTIES},
            measured={"hiddenPercent": percent, "coveredBy": coverer.selector},
        ),
        suggestion="Move one of the two elements or give the text its own space",
        source="Squint heuristic",
    )


def check(capture: Capture) -> list[Finding]:
    return [
        _finding(element, capture.viewport, *found)
        for element in capture.elements
        if (found := _coverer(element)) is not None
    ]
