# PR #6 review fixes

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/6#pullrequestreview-5443894564 - the three findings (F1 should-fix, F2 and F3 nits), with the repro and the fix each one asks for
- conversation - F1 is settled as option A: use the rect when `|rect - offsetWidth| < 1`, the offset size otherwise; fix F1, F2 and F3

## Out of scope

- Fixing `content` for a transformed SVG or MathML element - still issue #5's open half; F2 only makes the description say so
- A fractional element under a transform - it still reads the integer `offsetWidth`; the review asks for main's values where main was right, and main was wrong there
- Rewriting `.checks/issue5-box-model-layout-content.md` - its `Landing` row is the shape that was approved then; the new shape gets its row here
- `git push`, replying to the review - needs an explicit go-ahead

## Landing

Touches `js/collect_elements.js` (one helper replacing two `??`), `tests/fixtures/box.html` (one absolutely positioned element, so nothing in flow moves), `tests/test_inspect_element.py`, the `inspect_element` docstring, ADR-0003 and one figure in the issue #5 verification report. Reuses the `client` fixture and the `inspect` helper.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Where the layout size is read | `offset === undefined \|\| Math.abs(painted - offset) < 1 ? painted : offset`, per axis | `offset ?? painted`, the shape on this branch - it rounds every untransformed fractional size, which main reported exactly, and can round up past the real box. Decided by the user (option A) |

- A transform that changes a size by less than 1px is read as no transform: `content` is then off by that amount, under 1.5px with the rounding. Reversible (nothing persisted), marked in the code
- Nothing else in this change is hard to reverse

## Checks

### S1 - Fractional layout sizes (F1) · 3 files · 19 KB · ~5k

**C1** - `#frac` (100.5x60, no border, no padding, no transform) reports `boxModel.content == {"w": 100.5, "h": 60}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_keeps_the_fractional_size_of_an_untransformed_element" -v`

**C2** - `#scaled` still reports `boxModel.content == {"w": 50, "h": 30}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_is_the_layout_size_of_a_scaled_element" -v`

**C3** - `#rotated` still reports `boxModel.content == {"w": 50, "h": 30}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_is_the_layout_size_of_a_rotated_element" -v`

**C4** - `#vector` (no `offsetWidth`) still reports `boxModel.content == {"w": 40, "h": 20}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_of_an_svg_element_falls_back_to_its_rect" -v`

**C5** - ADR-0003 says the rect is kept when it is within 1px of the offset size
Proof: `grep -c "within 1px" docs/adr/0003-box-model-content-is-layout-size.md` prints 1 or more

### S2 - Wording (F2, F3) · 2 files · 12 KB · ~3k

**C6** - The `inspect_element` description limits "layout, before transforms" to HTML elements
Proof: `grep -c "for HTML elements" src/squint_mcp/tools/inspect_element.py` prints 1

**C7** - The issue #5 verification report cites 150x90 for the scaled case before the fix, not 150x70
Proof: `grep -c "150x70" .checks/issue5-box-model-layout-content.verified.md` prints 0
Proof: `grep -c "150x90" .checks/issue5-box-model-layout-content.verified.md` prints 1

### S3 - Gate

**C8** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: not in scope - no input surface changes
- failure modes: C4 - an element with no `offsetWidth` must not serialise `NaN`
- idempotency: not in scope - the tool is read-only
- authorization: not in scope
- concurrency: not in scope - the script runs once inside one page
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope - no log requirement

## Handoff

S1-S3 = ~8k of reading, one surface. One agent, no handoff.
