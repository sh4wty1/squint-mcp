"""The pure arithmetic of `vision`, called directly. No browser."""

import math

from squint_mcp.vision import count_limit


def test_a_text_under_the_limit_leaves_what_it_does_not_use_to_the_others() -> None:
    # 262,144 less the 100 counted whole, split between the two that are sampled.
    assert count_limit([100, 300_000, 300_000]) == 131022.0


def test_texts_that_fit_together_have_no_limit() -> None:
    assert count_limit([100, 200]) == math.inf
