# Issue #5 - boxModel.content under a transform

Sources:

- https://github.com/sh4wty1/squint-mcp/issues/5 - the defect (transformed rect minus untransformed border and padding), the first step (a fixture and a failing test through the MCP boundary), the direction
- conversation - the decision the issue left open: `boxModel.content` is the layout size, not the painted size; `box` stays the transformed rect

## Out of scope

- A painted content size next to the layout one - the decision picked one meaning for `content`; nobody asked for both
- `margin`, `border`, `padding` - already read from computed style, which is untransformed
- Rewriting `.specs/features/capture-inspect-element/spec.md` - a closed feature's record; the decision goes to an ADR instead
- The other two Codex comments on PR #3 (deadline during pixel processing, crop clamp) - not this issue
- `git push`, a PR, closing the issue - needs an explicit go-ahead

## Landing

Touches `js/collect_elements.js` (two lines), `tests/fixtures/box.html` (three absolutely positioned elements, so nothing in flow moves), `tests/test_inspect_element.py`, and the `inspect_element` docstring. Reuses the `client` fixture and the `inspect` helper. The decision is appended to `docs/adr/` as 0003.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Meaning of `boxModel.content` on the wire | layout size: `offsetWidth`/`offsetHeight` minus border and padding; `box` stays `getBoundingClientRect()` | painted size (rect scaled back through the transform) - decided by the user; and it has no single answer under a rotation or skew |
| Where the layout size is read | `element.offsetWidth ?? rect.width` (same for height) | `clientWidth - padding`, the issue's example - it is 0 for inline elements and drops the scrollbar, both regressions against today; computed `width` - it is `auto` for inline elements and needs a `box-sizing` branch |

- `offsetWidth` is an integer: a fractional layout width is rounded in `content` and not in `box`. Reversible (nothing persisted), marked in the code
- Elements without `offsetWidth` (SVG, MathML) keep today's rect-based value, transform included - C4 pins the untransformed case
- Nothing else in this change is hard to reverse

## Checks

### S1 - Layout content size · 3 files · 21 KB · ~5k

**C1** - `#scaled` (border-box 100x60, border 5, padding 10px 20px, `transform: scale(2)`) reports `boxModel.content == {"w": 50, "h": 30}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_is_the_layout_size_of_a_scaled_element" -v`

**C2** - The same element reports `box == {"x": 40, "y": 1000, "w": 200, "h": 120}` (the transformed rect, `transform-origin: 0 0`)
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_of_a_scaled_element_is_the_transformed_rect" -v`

**C3** - `#rotated` (the same box, `transform: rotate(90deg)`) reports `boxModel.content == {"w": 50, "h": 30}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_is_the_layout_size_of_a_rotated_element" -v`

**C4** - `#vector` (an `<svg>` of 40x20, which has no `offsetWidth`) reports `boxModel.content == {"w": 40, "h": 20}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_of_an_svg_element_falls_back_to_its_rect" -v`

**C5** - `#solid` (no transform) still reports `boxModel.content == {"w": 80, "h": 40}`
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_reports_margin_border_padding_and_content" -v`

### S2 - The decision is recorded · 1 file · ~1k

**C6** - `docs/adr/0003-box-model-content-is-layout-size.md` exists and says `content` is the layout size while `box` is the transformed rect
Proof: `grep -c -i -E "layout size|transformed rect" docs/adr/0003-box-model-content-is-layout-size.md` prints 2 or more

### S3 - Gate

**C7** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: not in scope - no input surface changes
- failure modes: C4 - an element with no `offsetWidth` would otherwise serialise `NaN` and fail the result model
- idempotency: not in scope - the tool is read-only
- authorization: not in scope
- concurrency: not in scope - the script runs once inside one page
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope - no log requirement

## Handoff

S1-S3 = ~6k of reading, one surface. One agent, no handoff.
