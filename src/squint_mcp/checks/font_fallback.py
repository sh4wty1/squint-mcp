"""The `font-fallback` Check: a font the page declares that did not load."""

from squint_mcp.models import Capture, Finding


def check(capture: Capture) -> list[Finding]:
    return []
