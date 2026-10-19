# Shaded border colours in `extract_tokens` - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 867feec..3892f0a
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Inputs: `checks.md` (no `plan.md`; its `## Intent` stands in), issue #33 (`gh issue view 33`, opened), the diff `867feec..3892f0a` (7 files: `src/squint_mcp/tokens.py`, `src/squint_mcp/tools/extract_tokens.py`, `tests/test_extract_tokens.py`, `tests/fixtures/tokens-borders.html`, `README.md`, `CHANGELOG.md`, `checks.md`). The uncommitted `docs/ROADMAP.md` change is outside the range and was not read.

## Binding sources

Step 1 runs only under `ui`; not run. For the record: issue #33 leaves "Expected" open with three options; the third ("shaded borders are left out of the border role") is the one `## Intent` records the maintainer choosing on 2026-10-19, and the checks follow it. The issue's measured case (default `<button>`, computed `outset rgb(0, 0, 0)`) is what C1 pins. No contradiction found.

## Checks

Verified at 3892f0a. C1-C5 ran in one invocation:
`uv run pytest tests/test_extract_tokens.py -v -p no:cacheprovider -k "test_a_default_button_gives_no_border_color or test_a_shaded_border_gives_no_color or test_only_the_shaded_sides_of_a_border_are_left_out or test_a_border_of_any_other_style_gives_its_color or test_the_description_says_a_shaded_border_is_not_counted"` - exit 0, **11 passed, 76 deselected in 9.68s**, each listed individually as PASSED: `test_a_default_button_gives_no_border_color`, `test_a_shaded_border_gives_no_color[#aa0000]`, `[#00aa00]`, `[#0000aa]`, `[#aa00aa]`, `test_only_the_shaded_sides_of_a_border_are_left_out`, `test_a_border_of_any_other_style_gives_its_color[#cc6600]`, `[#0066cc]`, `[#66cc00]`, `[#cc0066]`, `test_the_description_says_a_shaded_border_is_not_counted`. All five tests are added by this diff (`tests/test_extract_tokens.py` hunk `@@ -318,6 +319,41 @@`), and all four fixture-driven ones read the new `BORDERS = "tokens-borders.html"` (`tests/test_extract_tokens.py:23`). `values()` (`tests/test_extract_tokens.py:119`) collects token values and variant values, so an absence assertion also rules out a colour merged into a neighbour as a variant.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | no colour token is `#000000` (default `<button>`'s computed border) | one invocation above, PASSED | `tests/test_extract_tokens.py:325` - `assert "#000000" not in values(colors)` | PASS |
| C2 | `#aa0000` outset, `#00aa00` inset, `#0000aa` groove, `#aa00aa` ridge absent, 4 cases | one invocation above, 4 cases PASSED | `tests/test_extract_tokens.py:328` - `@pytest.mark.parametrize("value", ["#aa0000", "#00aa00", "#0000aa", "#aa00aa"])`; `:331` - `assert value not in values(colors)` | PASS |
| C3 | `#112233` (solid top) uses 1, roles.border 1; `#445566` (outset sides) absent | one invocation above, PASSED | `tests/test_extract_tokens.py:336-337` - `token = held(colors, "#112233")` / `assert (token["uses"], token["roles"]["border"]) == (1, 1)`; `:338` - `assert "#445566" not in values(colors)` | PASS |
| C4 | `#cc6600` solid, `#0066cc` dashed, `#66cc00` dotted, `#cc0066` double each uses 1, roles.border 1, 4 cases | one invocation above, 4 cases PASSED | `tests/test_extract_tokens.py:341` - `@pytest.mark.parametrize("value", ["#cc6600", "#0066cc", "#66cc00", "#cc0066"])`; `:347` - `assert (token["uses"], token["roles"]["border"]) == (1, 1)` | PASS |
| C5 | description names the four styles and says such a side is not counted | one invocation above, PASSED | `tests/test_extract_tokens.py:354` - ``assert "`outset`, `inset`, `groove` or `ridge` is not counted" in description`` (whitespace-collapsed at `:353`, as `checks.md` Handoff records); source text at `src/squint_mcp/tools/extract_tokens.py:41-42` | PASS |
| C6 | README `extract_tokens` paragraph names the four styles as not counted in `border` | `grep -c "outset.*inset.*groove.*ridge" README.md`, literally: `1` | `README.md:48` - "A border side counts in the `border` role only when it has a width and its style is not `outset`, `inset`, `groove` or `ridge`", inside the `extract_tokens` paragraph | PASS |
| C7 | `[Unreleased]` `### Fixed` entry links issue #33 | the sed/sed/grep pipeline, literally: `1` | `CHANGELOG.md:26` - entry ending `([#33](https://github.com/sh4wty1/squint-mcp/issues/33))`, under `### Fixed` at `CHANGELOG.md:24`, within `## [Unreleased]` (`:7`) before `## [0.1.0]` (`:31`) | PASS |
| C8 | pyright, ruff check, ruff format --check, whole suite green | see Gate | gate outputs, this run at HEAD `3892f0a` | PASS |

## Coverage

Not recomputed: the `Coverage` join runs only under `standard` and `ui`. Read for the record: both size-4 sets (shaded styles, other styles) are table-driven in C2 and C4 over all four members each.

## Test policy rows

None: `checks.md` carries no `Test policy` section.

## Faults injected

None: fault injection runs only under `standard` and `ui`.

## Level and sampling

C1-C5 go through the MCP boundary (`client.call_tool("extract_tokens", ...)` at `tests/test_extract_tokens.py:37`; `client.list_tools()` at `:29` for C5), the level the checks' Coverage note claims. The implementation is one predicate at `src/squint_mcp/tokens.py:221` - `if width > 0 and computed[f"border-{side}-style"] not in SHADED_STYLES`, with `SHADED_STYLES = ("outset", "inset", "groove", "ridge")` at `:121`; the four `border-*-style` properties are already in the captured set (`src/squint_mcp/config.py:72-75`), so the lookup cannot `KeyError`.

Observation (not a gap under `light`): C1 and C2 are pure absence assertions, which would also pass if the elements were not read at all. C2 is anchored by C3 and C4, whose positive assertions read sibling `div`s of the same size on the same page. C1 has no positive anchor on the `<button>` in any test. A read-only probe at HEAD (scratch script calling `extract_tokens` on the fixture) shows the button is read: `elements` 12 (html, body, button, 9 divs) and a `#f0f0f0` token with `roles.background` 1, the button's own background. So C1 holds today, but a future change that dropped an empty `<button>` from the read would leave C1 green. A one-line `assert held(colors, "#f0f0f0")` would pin it (Chromium-version dependent value).

## Swept existing

`checks.md` `## Swept` has no `existing` rows; every row is `n/a` or cites C5/C7. The Coverage note's claim that `none`/`hidden` are already left out by the width rule cites `test_a_border_color_is_counted_only_on_a_side_that_has_a_width`, present at `tests/test_extract_tokens.py:306`, and the width predicate `width > 0` remains at `src/squint_mcp/tokens.py:221`.

## Gate

All run by the Verifier at HEAD `3892f0a`. The working tree differs from HEAD only in the out-of-scope `docs/ROADMAP.md`.

- `uv run pyright` - exit 0, `0 errors, 0 warnings, 0 informations`
- `uv run ruff check` - exit 0, `All checks passed!`
- `uv run ruff format --check` - exit 0, `137 files already formatted`
- `uv run pytest -q` - exit 0, `538 passed in 1415.28s (0:23:35)`. A first background run died after 56 tests with no result line and no pytest process left. It was discarded, and this second run is the one recorded.
