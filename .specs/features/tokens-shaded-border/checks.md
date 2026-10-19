# Shaded border colours in `extract_tokens` checks

Profile: light
Plan: none - a change under three files of code with no one-way door (`## Intent` below)

## Intent

`extract_tokens` counts the computed `border-*-color` of every side with a width as a border colour. A side whose style is `outset`, `inset`, `groove` or `ridge` is never painted in that colour. With the native look switched off, Chromium 153 paints a black `outset` border `#a8a8a8` on its light sides and `#545454` on its dark ones, and a `#3366cc` one `#3f7fff` and `#1e3c78`. A default `<button>` keeps its native look and computes `outset rgb(0, 0, 0)`, but the theme paints it `#767676`. Its computed `appearance` stays `auto` even when author styling has turned the native look off, so the painter cannot be told from the computed style. An agent reading the tokens of an unstyled page gets a border colour `#000000` that is nowhere on the screen (issue #33).

When this ships, a side of one of those four styles adds no Use to the `border` role. The other sides of the same element still count, and so do the other styles. The maintainer chose this on 2026-10-19 over keeping the computed colour with a flag (it still lists `#000000`) and over computing the shades (wrong for the reported button, which the theme paints). The known cost: a default `<input>` computes `inset rgb(118, 118, 118)` and the theme paints it `#767676`, yet its border is no longer counted.

8 checks in 2 slices · 0 one-way doors · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. Their page is a new fixture, `tests/fixtures/tokens-borders.html`. It holds no text and no colour other than those named here, on a white `body`:

- an unstyled empty `<button>`
- four `div`s with a 4px border of `outset #aa0000`, `inset #00aa00`, `groove #0000aa` and `ridge #aa00aa`
- one `div` with `border-top: 4px solid #112233` and its other three sides `4px outset #445566`
- four `div`s with a 4px border of `solid #cc6600`, `dashed #0066cc`, `dotted #66cc00` and `double #cc0066`

## Checks

### S1 - a shaded side is not a border colour · 3 files · 53 KB · ~13k

**C1** - On the fixture, no colour token of `extract_tokens` has the value `#000000`, the computed border colour of the default `<button>`
Proof: `uv run pytest "tests/test_extract_tokens.py::test_a_default_button_gives_no_border_color" -v`

**C2** - Each of `#aa0000` (`outset`), `#00aa00` (`inset`), `#0000aa` (`groove`) and `#aa00aa` (`ridge`) is absent from the colour tokens
Proof: `uv run pytest "tests/test_extract_tokens.py::test_a_shaded_border_gives_no_color" -v` runs 4 cases

**C3** - On the element whose top is `solid #112233` and whose other sides are `outset #445566`, `#112233` is a token with `uses` 1 and `roles.border` 1, and `#445566` is absent
Proof: `uv run pytest "tests/test_extract_tokens.py::test_only_the_shaded_sides_of_a_border_are_left_out" -v`

**C4** - Each of `#cc6600` (`solid`), `#0066cc` (`dashed`), `#66cc00` (`dotted`) and `#cc0066` (`double`) is a token with `uses` 1 and `roles.border` 1
Proof: `uv run pytest "tests/test_extract_tokens.py::test_a_border_of_any_other_style_gives_its_color" -v` runs 4 cases

### S2 - the record and the gate · 3 files · 22 KB · ~6k

**C5** - The published description of `extract_tokens` names `outset`, `inset`, `groove` and `ridge` and says a border side of those styles is not counted
Proof: `uv run pytest "tests/test_extract_tokens.py::test_the_description_says_a_shaded_border_is_not_counted" -v`

**C6** - The `extract_tokens` paragraph of `README.md` names the four styles as not counted in the `border` role
Proof: `grep -c "outset.*inset.*groove.*ridge" README.md` prints `1` or more

**C7** - The `[Unreleased]` section of `CHANGELOG.md` has an entry under `### Fixed` that links issue #33
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Fixed/,/^## /p' | grep -c "issues/33"` prints `1` or more

**C8** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| shaded styles, left out (4) | `outset` C2 · `inset` C2 · `groove` C2 · `ridge` C2 | - |
| other styles with a width, still counted (4) | `solid` C4 · `dashed` C4 · `dotted` C4 · `double` C4 | - |
| who paints a shaded border (2) | the native theme, default `<button>` C1 · Chromium's shading, author `div`s C2 | - |
| sides of one element (2 kinds) | a plain side counted C3 · a shaded side left out C3 | - |
| where the rule is told (3) | tool description C5 · README C6 · CHANGELOG C7 | - |

- C1 to C5 cross the MCP boundary through `extract_tokens`. C2 and C4 are table-driven over their sets, size 4 each
- `none` and `hidden` compute a width of 0 and are already left out by the width rule (`test_a_border_color_is_counted_only_on_a_side_that_has_a_width`)

## Swept

- validation: n/a - no new input; the styles are read from the Capture as computed
- failure modes: n/a - a filter over computed values, nothing can fail halfway
- idempotency: n/a - a read-only call, as today
- authorization: n/a - a local stdio server, unchanged
- concurrency: n/a - nothing shared between calls
- data lifecycle: n/a - nothing is persisted
- dependency failure: n/a - no new dependency; a style Chromium does not compute is not one of the four and counts as today
- state transitions: n/a - no state
- observability: C5, C7 - the rule is said where an agent reads the result; no log requirement

## Out of scope

- Counting the colours a shaded or native border is painted in - the maintainer chose to leave such sides out. The pixels of an element are `inspect_element`'s `sampledColors`
- Detecting the native look of a form control - its computed `appearance` cannot tell it (probed: `auto` on a button styled `border: 3px solid red`, painted `#ff0000`)

## Handoff

- S1-S2 = `tokens.py` 15 KB + `tests/test_extract_tokens.py` 36 KB + a new fixture ~2 KB (S1, 53 KB) and `tools/extract_tokens.py` 4 KB + `README.md` 7 KB + `CHANGELOG.md` 11 KB (S2, 22 KB) = 75 KB / 4 ≈ 19k tokens, one surface (`extract_tokens`), under the 150k budget - one builder
