"""The Checks, by name. A Check turns one Capture into Findings, in the order of the
Capture's elements, and never touches the browser (ADR-0002).

Adding a Check is one module in this package and one entry in `CHECKS`.
"""

from collections.abc import Callable

from squint_mcp.checks import low_contrast_real, offscreen_overflow, text_clipped
from squint_mcp.models import Capture, Finding

Check = Callable[[Capture], list[Finding]]

CHECKS: dict[str, Check] = {
    "text-clipped": text_clipped.check,
    "low-contrast-real": low_contrast_real.check,
    "offscreen-overflow": offscreen_overflow.check,
}
