# Say when a page has no style of its own checks

Profile: light
Plan: `.specs/features/tokens-author-styles/plan.md`

11 checks in 2 slices · 1 one-way door · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. The pages are one new fixture, `tests/fixtures/tokens-author.html`, served by the existing `local_server` over HTTP, and a sheet beside it, `tests/fixtures/tokens-author.css`, of one rule. The page holds a `#inside` and a `#other` element with text and no style; the query string names one case, and a script of the page, run in `<head>` before `load`, adds that case's Author style and nothing else. With no query the page has no style. The cross-origin case links the sheet on `localhost` from the page on `127.0.0.1`, the same server.

The Capture's own stabilize script appends a `<style>` of its own to every root before anything is read: C2 fails if that style is counted.

## Checks

### S1 - the result says whether the page styles itself · 7 files · 68 KB · ~17k

**C1** - The output schema of `extract_tokens` has a property `authorStyles` of type `boolean`, listed in `required` (AC 1)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_author_styles_is_in_the_output_schema" -v`

**C2** - On the page with no style, `authorStyles` is `false` and the summary ends with ` The page has no style of its own: these values are the browser's defaults.` (AC 2)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_a_page_with_no_style_says_its_values_are_the_defaults" -v`

**C3** - On the case `style` (one `<style>` element with the rule `#other { color: #aa0000 }`), `authorStyles` is `true` and the summary does not contain `no style of its own` (AC 3)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_a_style_element_is_an_author_style" -v`

**C4** - `authorStyles` is `true` on each of 7 cases, each the only Author style of the page: a same-origin `<link rel="stylesheet">` of one rule (AC 4), one `style` attribute of one declaration (AC 5), a sheet of one rule adopted by the document (AC 6), a `<style>` of one rule in an open shadow root (AC 7), a sheet of one rule adopted by an open shadow root (AC 8), a `<link rel="stylesheet">` to the sheet on another origin (AC 9), a `<style media="print">` of one rule (plan assumption)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_each_author_style_turns_the_notice_off" -v` runs 7 cases

**C5** - `authorStyles` is `false` on each of 5 cases, each the only style-like thing on the page: an empty `<style>` (AC 10), an empty `style=""` (AC 11), a `<link rel="stylesheet">` that answers 404 (AC 12), a `<style>` of one rule whose sheet is `disabled` (plan assumption), a `bgcolor` attribute on `body` (plan assumption)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_what_is_no_author_style_leaves_the_notice_on" -v` runs 5 cases

**C6** - With `scope` `#inside` on the case `style`, whose only rule styles `#other`, `authorStyles` is `true` (AC 13)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_author_styles_describes_the_whole_page_whatever_the_scope" -v`

**C7** - On the page with no style, the structured result of `inspect_element` has exactly the keys `box`, `boxModel`, `computed`, `sampledColors`, `stabilized`, `viewport`; that of `detect_visual_bugs` exactly `findings`, `captures`, and each of its `captures` exactly `viewport`, `stabilized` (AC 14)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_the_other_tools_gain_no_field" -v`

### S2 - the record and the gate · 3 files · 23 KB · ~6k

**C8** - The published description of `extract_tokens` names `authorStyles`, says it describes the whole page whatever `scope` is, and says that `false` means the values are the browser's defaults (AC 15)
Proof: `uv run pytest "tests/test_extract_tokens.py::test_the_description_tells_author_styles" -v`

**C9** - The `extract_tokens` paragraph of `README.md` names `authorStyles` and says that a default `<button>` on a page with some style is still reported (AC 16)
Proof: `grep -c "authorStyles.*<button>" README.md` prints `1` or more

**C10** - The `[Unreleased]` section of `CHANGELOG.md` has an entry under `### Added` that names `authorStyles` and links issue #36 (AC 17)
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### Changed/p' | grep "authorStyles" | grep -c "issues/36"` prints `1` or more

**C11** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Author style sources, counted (7) | `<style>` C3 · same-origin `<link>` C4 · `style` attribute C4 · document adopted sheet C4 · shadow `<style>` C4 · shadow adopted sheet C4 · unreadable cross-origin `<link>` C4 | - |
| assumption defaults (4) | print-media sheet counts C4 · disabled sheet does not C5 · presentational attribute does not C5 · rule matching outside `scope` counts C6 | - |
| not an Author style (4) | nothing at all, Squint's own style present C2 · empty `<style>` C5 · empty `style=""` C5 · 404 `<link>` C5 | - |
| door 1, `authorStyles` (3 places) | output schema C1 · structured result C2, C3 · summary sentence C2, C3 | - |
| tools whose result must not change (2) | `inspect_element` C7 · `detect_visual_bugs` C7 | - |
| where the field is told (3) | tool description C8 · README C9 · CHANGELOG C10 | - |

- C1 to C8 cross the MCP boundary through the tools. C4 and C5 are table-driven over their sets, size 7 and 5
- The plan's `Surface` names no route

## Swept

- validation: n/a - no new input; the fact is read from the page as loaded
- failure modes: n/a - a read of `cssRules` that throws is caught and counted (C4, cross-origin); nothing else in the script can fail on a loaded page
- idempotency: n/a - a read-only call, as today
- authorization: n/a - a local stdio server, unchanged
- concurrency: n/a - nothing shared between calls; each Capture has its own context
- data lifecycle: n/a - nothing is persisted
- dependency failure: C5 - a sheet whose request fails (404) is no Author style
- state transitions: n/a - no state
- observability: C2, C8, C10 - the notice is said in the summary an agent reads; no log requirement

## Handoff

- S1-S2 = `capture.py` 18 KB + `models.py` 6 KB + `js/stabilize.js` 1 KB + a new page script ~1 KB + `tools/extract_tokens.py` 5 KB + `tests/test_extract_tokens.py` 38 KB + the two fixtures ~2 KB (S1, 71 KB) and `README.md` 7 KB + `CHANGELOG.md` 12 KB + the tool again 5 KB (S2, 24 KB) = 95 KB / 4 ≈ 24k tokens, one surface (`extract_tokens`), under the 150k budget - one builder

- **Boundary:** C1-C11 closed at the build commit of this branch. The whole suite ran 555 passed, 1 failed: `test_many_texts_over_millions_of_colours_add_little_to_the_call`, a wall-clock bound (`painted - bare < 10`s) missed during a 30-minute run while other commands shared the machine. It passed alone (9s), and this change adds one page script to both calls it compares
- **Settled mid-build:** the stabilize script's own `<style>` now carries `data-squint-stabilize`, so the page script can leave it out with the text fill's `data-squint-fill`; the page script runs before the text fills. Two faults injected by the builder were caught: counting Squint's own style (C2 red) and treating an unreadable sheet as no style (C4 `cross-origin` red)
- **Abandoned:** nothing
