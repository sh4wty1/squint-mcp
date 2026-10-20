# Say when a page has no style of its own (`authorStyles`) - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 1a10de9..7fecc96
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Inputs: `plan.md`, `checks.md` (11 checks, `Profile: light`), issue #36 (`gh issue view 36 --json`, opened: body only, no comments), and the diff `1a10de9..7fecc96`, two commits: `2e7d8b2` (plan and checks) and `7fecc96` (the build: `src/squint_mcp/capture.py`, `src/squint_mcp/js/author_styles.js` new, `src/squint_mcp/js/stabilize.js`, `src/squint_mcp/models.py`, `src/squint_mcp/tools/extract_tokens.py`, `tests/test_extract_tokens.py`, `tests/fixtures/tokens-author.html` and `tokens-author.css` new, `README.md`, `CHANGELOG.md`). The working tree is clean at `7fecc96`.

## Binding sources

Step 1 runs only under `ui`; not run. For the record: issue #36 leaves "Expected" open between an `origin` per token and a notice when the page has no author style rule at all. The plan records the notice as the maintainer's choice on 2026-10-19 (door 1), and the checks follow it. The issue's three example values (`Times New Roman`, `#efefef`, `13.333px`) are told in the CHANGELOG entry. No contradiction found.

## Checks

Verified at 7fecc96. C1-C8 ran in one invocation:
`uv run pytest tests/test_extract_tokens.py -v -p no:cacheprovider -k "author or no_style or other_tools or description_tells"` - exit 0, **18 passed, 87 deselected in 17.62s**, each listed individually as PASSED: `test_author_styles_is_in_the_output_schema`, `test_a_page_with_no_style_says_its_values_are_the_defaults`, `test_a_style_element_is_an_author_style`, `test_each_author_style_turns_the_notice_off[link]`, `[attribute]`, `[adopted]`, `[shadow-style]`, `[shadow-adopted]`, `[cross-origin]`, `[print]`, `test_what_is_no_author_style_leaves_the_notice_on[empty-style]`, `[empty-attribute]`, `[missing-link]`, `[disabled]`, `[bgcolor]`, `test_author_styles_describes_the_whole_page_whatever_the_scope`, `test_the_other_tools_gain_no_field`, `test_the_description_tells_author_styles`. All eight test functions are added by this diff (`tests/test_extract_tokens.py` hunk `@@ -958,3 +958,107 @@`); `rg -n "def test_..."` finds them at `:973`, `:980`, `:991`, `:1014`, `:1024`, `:1031`, `:1039`, `:1060`. The fixture cases they name exist in `tests/fixtures/tokens-author.html` (`const cases = {...}`, 13 keys: 1 for C3, 7 for C4, 5 for C5).

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | output schema has `authorStyles`, `boolean`, in `required` | one invocation above, PASSED | `tests/test_extract_tokens.py:976` - `assert schema["properties"]["authorStyles"]["type"] == "boolean"`; `:977` - `assert "authorStyles" in schema["required"]` | PASS |
| C2 | no-style page: `authorStyles` false, summary ends with the exact notice | one invocation above, PASSED | `tests/test_extract_tokens.py:986` - `assert result.structured_content["authorStyles"] is False`; `:988` - `assert text.endswith(NO_STYLE_NOTICE), text`, with `NO_STYLE_NOTICE` literal at `:964`, character-identical to the AC 2 sentence | PASS |
| C3 | case `style`: `authorStyles` true, summary lacks `no style of its own` | one invocation above, PASSED | `tests/test_extract_tokens.py:997` - `assert result.structured_content["authorStyles"] is True`; `:999` - `assert "no style of its own" not in text` | PASS |
| C4 | `authorStyles` true on 7 cases (link, attribute, adopted, shadow-style, shadow-adopted, cross-origin, print) | one invocation above, 7 cases PASSED | `tests/test_extract_tokens.py:1005` - parametrize list beginning `"link",` over the 7 names; `:1018` - `assert result["authorStyles"] is True` | PASS |
| C5 | `authorStyles` false on 5 cases (empty-style, empty-attribute, missing-link, disabled, bgcolor) | one invocation above, 5 cases PASSED | `tests/test_extract_tokens.py:1022` - `"case", ["empty-style", "empty-attribute", "missing-link", "disabled", "bgcolor"]`; `:1028` - `assert result["authorStyles"] is False` | PASS |
| C6 | `scope` `#inside` on case `style` (rule styles `#other`): `authorStyles` true | one invocation above, PASSED | `tests/test_extract_tokens.py:1035` - `assert result["elements"] == 1` (the scope did narrow); `:1036` - `assert result["authorStyles"] is True` | PASS |
| C7 | `inspect_element` keys exactly the six; `detect_visual_bugs` exactly `findings`, `captures`, each capture `viewport`, `stabilized` | one invocation above, PASSED | `tests/test_extract_tokens.py:1045` - `assert set(inspected.structured_content) == {` `box`, `boxModel`, `computed`, `sampledColors`, `stabilized`, `viewport` `}`; `:1055` - `assert set(detected.structured_content) == {"findings", "captures"}`; `:1057` - `assert set(captured) == {"viewport", "stabilized"}` | PASS |
| C8 | description names `authorStyles`, whole page whatever `scope`, `false` means browser's defaults | one invocation above, PASSED | `tests/test_extract_tokens.py:1062` - ``assert "`authorStyles`" in description``; `:1063` - ``assert "the whole page, whatever `scope` is" in description``; `:1064` - `assert "the browser's defaults" in description`; source at `src/squint_mcp/tools/extract_tokens.py:65-69`. Neither phrase was in the base description: a count of them in `git show 1a10de9:src/squint_mcp/tools/extract_tokens.py` gives 0 | PASS |
| C9 | README `extract_tokens` paragraph names `authorStyles` and the default `<button>` | `grep -c "authorStyles.*<button>" README.md`, literally: `1` | `README.md:55` - "`authorStyles` is false when the page has no style of its own ... such as a default `<button>` and its `#efefef` background", inside the `extract_tokens` prose (`README.md:48-55`, before `## Pages behind a login` at `:57`) | PASS |
| C10 | `[Unreleased]` `### Added` entry names `authorStyles`, links #36 | the sed/sed/grep pipeline, literally: `1` | `CHANGELOG.md:11` - entry beginning `` `authorStyles` in the result of `extract_tokens` `` and ending `([#36](https://github.com/sh4wty1/squint-mcp/issues/36))`, under `### Added` at `CHANGELOG.md:9`, within `## [Unreleased]` (`:7`) before `### Changed` (`:19`) | PASS |
| C11 | pyright, ruff check, ruff format --check, whole suite green | see Gate | gate outputs, this run at HEAD `7fecc96` | PASS |

## Coverage

Not recomputed: the `Coverage` join runs only under `standard` and `ui`. Read for the record: the counted sources (7) are table-driven in C3 + C4, the not-counted set and assumption defaults in C2, C5 and C6, and the three places the field is told in C8-C10; each name in the table matches a fixture case key and a parametrize id above.

## Test policy rows

None: `checks.md` carries no `Test policy` section.

## Faults injected

None: fault injection runs only under `standard` and `ui`. (`checks.md` Handoff records two builder-injected faults; they are the author's, not counted here.)

## Level and sampling

C1-C8 go through the MCP boundary: `client.list_tools()` (`tests/test_extract_tokens.py:29`) for C1 and C8, `client.call_tool("extract_tokens", ...)` (`:37`) for C2-C6, `client.call_tool("inspect_element"/"detect_visual_bugs", ...)` for C7 - the level the checks' Coverage note claims. C4 and C5 are table-driven over all 7 and 5 members.

The implementation read against the checks:
- `src/squint_mcp/js/author_styles.js` walks the document and every open shadow root, returns true on any element with a non-empty `style` (AC 5, AC 11), then on any non-`disabled` sheet in `styleSheets` + `adoptedStyleSheets` with `cssRules.length > 0`, treating a throwing `cssRules` as true (AC 9). Squint's own sheets are skipped by `[data-squint-stabilize], [data-squint-fill]`; `stabilize.js` now tags its `<style>` with `data-squint-stabilize`.
- Order in `capture()`: the read is at `src/squint_mcp/capture.py:403`, after `_STABILIZE` (`:371`), the collector, `_srgb_colors` and `_SCROLL_WIDTH`, and before the text fills (`:409-411`), `_measure_fonts` (`:416`) and `_measure_covered_text` (`:419`). The other page scripts that write inline styles or add `<style>` elements (`covered_text.js:55`, `:145`; `font_widths.js:76`; `fill_text.js:18`) all run after it, so none can turn the field true; C2 is the test that would catch a regression in that order.
- `ExtractTokensResult` gains `alias_generator=to_camel`. Every field it and `Tokens` declare (`elements`, `colors`, `typography`, `spacing`, `radii`, `shadows`, `viewport`, `stabilized`, `scope`) is a single word, so no existing key is renamed; nested models keep their own config.

Observations (not gaps under `light`):
- `checks.md` describes the fixture's script as run "in `<head>`"; it sits at the end of `<body>` (it needs `#other` to exist). It still runs before `load`, which is what the checks rely on. Prose drift only.
- The `cross-origin` case relies on Chromium resolving `localhost` to the `127.0.0.1` the fixture server binds (`tests/conftest.py:79`). If it did not load, the link would behave as the 404 case and C4 `[cross-origin]` would go red, so a green run shows the sheet loaded from the other origin.

## Swept existing

`checks.md` `## Swept` has no `existing` rows; every row is `n/a` or cites C2, C5, C8, C10, all proven above. The failure-mode row's claim that a throwing `cssRules` is caught and counted is the `try`/`catch { return true; }` in `src/squint_mcp/js/author_styles.js`.

## Gate

All run by the Verifier at HEAD `7fecc96`, working tree clean.

- `uv run pyright` - exit 0, `0 errors, 0 warnings, 0 informations`
- `uv run ruff check` - exit 0, `All checks passed!`
- `uv run ruff format --check` - exit 0, `140 files already formatted`
- `uv run pytest -q -p no:cacheprovider` - exit 0, `556 passed in 1452.01s (0:24:12)`. The known wall-clock bound `tests/test_low_contrast_real.py::test_many_texts_over_millions_of_colours_add_little_to_the_call` passed within this full run; no rerun was needed. The targeted invocation and the static checks shared the machine during the first minutes of this run.
