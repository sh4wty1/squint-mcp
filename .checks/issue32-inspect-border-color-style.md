# Issue #32 - `inspect_element` reports border colour and style

Sources:

- https://github.com/sh4wty1/squint-mcp/issues/32 - the defect (`computed` of `inspect_element` holds no border property), the measurement (a default `<button>` on Chromium 153 computes `border-top-color: rgb(0, 0, 0)`, `border-top-style: outset`), the expected eight keys, and the fix: add them to `INSPECT_COMPUTED_PROPERTIES` (the styles also to `CAPTURE_COMPUTED_PROPERTIES` if absent), a test on a fixture of known borders, a CHANGELOG entry
- conversation - `/tlc-implement issue #32`

## Out of scope

- The painted colour of a shaded border (`outset`, `inset`, `groove`, `ridge`) in `extract_tokens` - issue #33
- Converting the border colours to sRGB or hex - `computed` reports what Chromium resolved, as it already does for `color` and `background-color`; a border written in `oklch()` is reported in that notation
- Border widths in `computed` - they are in `boxModel.border` already
- `detect_visual_bugs` Findings - they carry no `computed` map from this list
- `git push` and the PR - need a go-ahead

## Landing

Touches `config.py` (eight names move into `INSPECT_COMPUTED_PROPERTIES`; the four border colours leave the explicit tail of `CAPTURE_COMPUTED_PROPERTIES`, which inherits them, so no property is collected twice) and `CHANGELOG.md`. `inspect_element.py` is unchanged: it already reports every name of the inspect list. Reuses `box.html` and the `inspect` helper.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Eight keys added to `computed` of `inspect_element`, a contract agents read | the CSS longhands `border-{top,right,bottom,left}-{color,style}`, each the string `getComputedStyle` returns | the shorthands `border-color` / `border-style` - one string of up to four values the reader has to split, and the issue names the longhands |

- Additive: the CHANGELOG preamble says adding a field is not breaking. Nothing else here is hard to reverse

## Checks

### S1 - Border colour and style in `inspect_element` · 5 files · 47 KB · ~12k

**C1** - On `#borders` (4px, red top, green right, blue bottom, orange left) `computed` holds `border-top-color == "rgb(255, 0, 0)"`, `border-right-color == "rgb(0, 128, 0)"`, `border-bottom-color == "rgb(0, 0, 255)"`, `border-left-color == "rgb(255, 165, 0)"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_computed_holds_the_colour_of_each_border" -v`

**C2** - On `#borders` (solid top, dashed right, dotted bottom, double left) `computed` holds `border-top-style == "solid"`, `border-right-style == "dashed"`, `border-bottom-style == "dotted"`, `border-left-style == "double"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_computed_holds_the_style_of_each_border" -v`

**C3** - On an unstyled `<button>` `computed["border-top-style"] == "outset"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_computed_holds_the_border_of_a_default_button" -v`

**C4** - On an unstyled `<button>` `computed["border-top-color"] == "rgb(0, 0, 0)"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_computed_holds_the_border_of_a_default_button" -v`

**C5** - `computed` holds exactly the 20 keys it held before plus the eight border keys, 28 in all
Proof: `uv run pytest "tests/test_inspect_element.py::test_computed_holds_exactly_the_configured_properties" -v`
Proof: `git diff main..HEAD -- tests/test_inspect_element.py` removes no line of the expected set

**C6** - `CHANGELOG.md` has an entry under `## [Unreleased]` naming `border-*-style` on `inspect_element`
Proof: `grep -n "border-\*-style" CHANGELOG.md` prints a line above `## [0.1.0]`

### S2 - Gate

**C7** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: not in scope - no input changes
- failure modes: every inspect name is read from the Capture's `computed`, which holds every Capture name; the inspect list is the head of the Capture list, so a name cannot be missing - existing `config.py` `*INSPECT_COMPUTED_PROPERTIES`
- idempotency: not in scope - read-only
- authorization: not in scope
- concurrency: not in scope
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope

## Handoff

S1-S2 = ~12k of reading, one surface (`inspect_element`). One agent, no handoff.
