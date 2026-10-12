"""The `font-fallback` Check: a font the page declares that did not load."""

from squint_mcp.models import Capture, Element, Evidence, Finding

# The styles that say which face the element asked for.
_EVIDENCE_PROPERTIES = ("font-family", "font-weight", "font-style")


def _finding(
    capture: Capture, family: str, fallen: list[tuple[Element, float]]
) -> Finding:
    """The Finding of a family, on the first of the elements that fall back in it."""
    element, width = fallen[0]
    noun = "element" if len(fallen) == 1 else "elements"
    return Finding(
        check="font-fallback",
        category="visual-bug",
        severity="minor",
        message=(
            f'The font "{family}" did not load: the text of {len(fallen)} {noun} '
            "is rendered in a fallback font"
        ),
        selector=element.selector,
        text=element.text,
        box=element.box,
        viewport=capture.viewport,
        evidence=Evidence(
            computed={name: element.computed[name] for name in _EVIDENCE_PROPERTIES},
            measured={
                "family": family,
                "elements": len(fallen),
                "textWidthPx": round(width, 2),
            },
        ),
        suggestion=(
            f'Fix the source the page loads "{family}" from, or take the family out '
            "of font-family"
        ),
        source="Squint heuristic",
    )


def check(capture: Capture) -> list[Finding]:
    if capture.faces is None:
        return []
    failed = {face.family for face in capture.faces if face.status == "error"}
    # Each family with the elements that fall back in it, both in document order.
    fallen: dict[str, list[tuple[Element, float]]] = {}
    for element in capture.elements:
        widths = element.line_widths
        if widths is None or widths.family not in failed:
            continue
        # Judged: its own text paints a box, and is not hidden on purpose.
        if not element.own_text_boxes or element.computed["visibility"] != "visible":
            continue
        # The family changes nothing: the text is as wide without it. The two
        # widths are of one text laid out twice in one page, so they are compared
        # as they are.
        if widths.own == widths.tail:
            fallen.setdefault(widths.family, []).append((element, widths.own))
    return [_finding(capture, family, found) for family, found in fallen.items()]
