# Offscreen overflow verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 9923762..cd7adf2
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

23 of 23 checks are proven with located evidence.

Every proof was run at `cd7adf2` (`cd7adf28ab9f6502e77064ad939a6350ed553ddf`, branch `feat/offscreen-overflow`). The `light` profile leaves out step 1 (binding sources), the `Coverage` recompute, the `Test policy` verdicts and fault injection; none of them ran. `checks.md` declares `Profile: light`, and this report is written under the same profile.

## Checks

verified at cd7adf2 - every proof run at this commit; every cited line read at this commit.

The gate script splits a table row on every pipe character, so a shell pipeline inside a cell is written "piped to". `uv` is not on the path, so `uv run <tool>` ran as `.venv/bin/<tool>`, as `checks.md` allows.

The pytest proofs ran in one invocation: `.venv/bin/pytest tests/test_offscreen_overflow.py tests/test_detect_visual_bugs.py -k "<the 22 test names of C1-C19, joined by or>" -v`. Result: 31 passed, 40 deselected in 40.77s, exit 0. Each test named below appears in that output individually as `PASSED`, and C11 and C12 appear once per case (7 and 4). All 18 tests of `tests/test_offscreen_overflow.py` are new in the diff. The four tests of C18 sit in `tests/test_detect_visual_bugs.py`, and the diff edits their assertions.

Four tests use the helper `the_finding_on` (`tests/test_offscreen_overflow.py:23-28`). It asserts `len(found) == 1` at `:26` and unpacks `(finding,) = await findings_on(client, page(name), selector, found)` at `:27`, so a call that passes means exactly one Finding, and that Finding is on `selector`. These two lines settle "the one Finding is on X". The fixtures that the claims name as preconditions were read and match: `overflow-bug.html` (`#first`, `#second`, 1640px), `overflow-near.html` (1639px, then 1640px), `overflow-nested.html`, `overflow-child.html` (400px, then 1640px), `overflow-fraction.html` (1639.6px), `overflow-word.html` (100 Ahem glyphs at 20px in a 400px box) and `overflow-moved.html` (200px, `translateX(1400px)`).

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | 1640px page at 1440 and 390: two Findings in viewport order, door-1 values, overflowPx 200 and 1250 | `test_a_page_that_scrolls_sideways_yields_one_finding_per_viewport` PASSED | `tests/test_offscreen_overflow.py:35` - `assert [finding["viewport"] for finding in found] == [DESKTOP, MOBILE]` · `:37` - `assert overflows == [200, 1250]` · `:39-42` - `finding["check"] == "offscreen-overflow"`, `finding["category"] == "responsive"`, `finding["severity"] == "major"`, `finding["source"] == "Squint heuristic"` | PASS |
| C2 | of two 1640px siblings, the one Finding is on `#first` | `test_the_first_of_two_elements_on_the_edge_is_the_one_named` PASSED | `tests/test_offscreen_overflow.py:48` - `await the_finding_on(client, "bug", "#first")`, which settles it at `:26` `assert len(found) == 1` and at `:27` `(finding,) = await findings_on(..., selector, found)` | PASS |
| C3 | measured, computed and message of the Finding on a 1640px block | `test_the_finding_carries_the_widths_the_styles_and_the_message` PASSED | `tests/test_offscreen_overflow.py:55-59` - `assert finding["evidence"]["measured"] == {"overflowPx": 200, "pageWidth": 1640, "viewportWidth": 1440}` · `:60-65` - `assert finding["evidence"]["computed"] == {"display": "block", "position": "static", "width": "1640px", "white-space": "normal"}` · `:66-68` - `assert finding["message"] == ("Extends 200px past the 1440px viewport, so the page scrolls horizontally")` | PASS |
| C4 | parent and child both at 1640px: the parent is named | `test_a_parent_on_the_edge_is_named_instead_of_its_child` PASSED | `tests/test_offscreen_overflow.py:74` - `await the_finding_on(client, "nested", "#parent")` (`:26`, `:27`) | PASS |
| C5 | 400px parent, 1640px child: the child is named | `test_a_child_past_a_parent_that_fits_is_the_one_named` PASSED | `tests/test_offscreen_overflow.py:78` - `await the_finding_on(client, "child", "#child")` (`:26`, `:27`) | PASS |
| C6 | `#near` of 1639px before `#edge` of 1640px: `#edge` is named | `test_an_element_1px_short_of_the_edge_is_not_named` PASSED | `tests/test_offscreen_overflow.py:82` - `await the_finding_on(client, "near", "#edge")` (`:26`, `:27`) | PASS |
| C7 | 1639.6px element: reported, pageWidth 1640, overflowPx 200 | `test_an_element_under_1px_short_of_the_edge_is_named` PASSED | `tests/test_offscreen_overflow.py:86` - `the_finding_on(client, "fraction", "#fraction")` · `:87` - `assert finding["evidence"]["measured"]["pageWidth"] == 1640` · `:88` - `assert finding["evidence"]["measured"]["overflowPx"] == 200` | PASS |
| C8 | unbreakable word: `#word` named, box.w 400, measured 560/2000/1440 | `test_a_word_that_cannot_break_names_the_element_that_holds_it` PASSED | `tests/test_offscreen_overflow.py:94` - `the_finding_on(client, "word", "#word")` · `:95` - `assert finding["box"]["w"] == 400` · `:96-100` - `assert finding["evidence"]["measured"] == {"overflowPx": 560, "pageWidth": 2000, "viewportWidth": 1440}` | PASS |
| C9 | translated `#moved`: box.x 1400, box.w 200, overflowPx 160 | `test_a_translated_element_is_reported_where_it_is_painted` PASSED | `tests/test_offscreen_overflow.py:107` - `assert finding["box"]["x"] == 1400` · `:108` - `assert finding["box"]["w"] == 200` · `:109` - `assert finding["evidence"]["measured"]["overflowPx"] == 160` | PASS |
| C10 | 400px element at 399 and 400: exactly one Finding, at 399, measured 1/400/399 | `test_one_pixel_past_the_viewport_is_reported_and_none_is_not` PASSED | `tests/test_offscreen_overflow.py:117` - `(finding,) = await findings(client, "400", viewports=[narrow, exact])` · `:118` - `assert finding["viewport"] == narrow` · `:119-123` - `assert finding["evidence"]["measured"] == {"overflowPx": 1, "pageWidth": 400, "viewportWidth": 399}` | PASS |
| C11 | seven pages as wide as the viewport: no Finding | `test_a_page_as_wide_as_the_viewport_is_not_reported[left]`, `[fixed]`, `[hidden-ancestor]`, `[scroll-container]`, `[shadow]`, `[margin]`, `[taller]` all PASSED (7 cases) | `tests/test_offscreen_overflow.py:128-136` - the 7 cases · `:141` - `assert await findings(client, f"none-{case}") == []` | PASS |
| C12 | `overflow-x` hidden or clip on `html`, or on `body` under a visible `html`: no Finding | `test_a_page_that_hides_its_horizontal_overflow_is_not_reported[html-hidden]`, `[html-clip]`, `[body-hidden]`, `[body-clip]` all PASSED (4 cases) | `tests/test_offscreen_overflow.py:145` - `["html-hidden", "html-clip", "body-hidden", "body-clip"]` · `:150` - `assert await findings(client, case) == []` | PASS |
| C13 | `html` auto, `body` 1640px hidden: `body` reported, overflowPx 200 | `test_a_hidden_overflow_on_body_under_a_scrolling_html_is_reported` PASSED | `tests/test_offscreen_overflow.py:156` - `the_finding_on(client, "body-under-html", "body")` · `:157` - `assert finding["evidence"]["measured"]["overflowPx"] == 200` | PASS |
| C14 | `direction: rtl` on `body`: no Finding | `test_a_right_to_left_page_is_not_reported` PASSED | `tests/test_offscreen_overflow.py:161` - `assert await findings(client, "rtl") == []` | PASS |
| C15 | page widened by `body::after` alone: no Finding | `test_a_page_widened_by_no_element_is_not_reported` PASSED | `tests/test_offscreen_overflow.py:165` - `assert await findings(client, "pseudo") == []` | PASS |
| C16 | `checks: ["offscreen-overflow"]` on the page with a clipped text: exactly that Finding | `test_naming_the_check_returns_its_finding_alone` PASSED | `tests/test_offscreen_overflow.py:170` - `assert [finding["check"] for finding in found] == ["offscreen-overflow"]` | PASS |
| C17 | no `checks`: two Findings in order, cropIndex 0 and 1 | `test_omitting_checks_returns_the_finding_among_the_others` PASSED | `tests/test_offscreen_overflow.py:177-180` - `assert [finding["check"] for finding in found] == ["offscreen-overflow", "text-clipped"]` · `:181` - `assert [finding["evidence"]["cropIndex"] for finding in found] == [0, 1]` | PASS |
| C18 | the unknown-name error holds the list of three in the four existing tests | the four tests PASSED · `grep -c` of the new list in `tests/test_detect_visual_bugs.py` prints `1` · `grep -c` of the old list prints `0` | `tests/test_detect_visual_bugs.py:338` - `VALID_CHECKS = "Valid checks: low-contrast-real, offscreen-overflow, text-clipped."` · `:343`, `:350`, `:357` - `assert f'Unknown check "nope". {VALID_CHECKS}' in text` (`"zzz"` at `:357`) · `:365` - `assert f'Unknown check "nope". {VALID_CHECKS}' in text` | PASS |
| C19 | the tool description holds `` `offscreen-overflow` `` and `scroll` | `test_the_tool_description_names_the_check_and_what_it_reports` PASSED | `tests/test_offscreen_overflow.py:193` - `assert "`offscreen-overflow`" in tool.description` · `:194` - `assert "scroll" in tool.description` | PASS |
| C20 | every test of the base passes; the only lines removed from `tests/` are the four old-list lines and their parentheses | `.venv/bin/pytest` - 239 passed in 470.51s, exit 0 · `git diff 9923762..HEAD -- tests` piped to `grep -c "^-.*Valid checks: low-contrast-real, text-clipped\."` prints `4` · the same diff piped to `grep "^-[^-]"` piped to `grep -Evc` of the allowed lines prints `0` | the diff of `tests/test_detect_visual_bugs.py`: one hunk `@@ -335,27 +335,26 @@`, which replaces the four `assert (` blocks with `assert f'...{VALID_CHECKS}' in text` and adds the constant; no other file under `tests/` has a removed line | PASS |
| C21 | `[Unreleased]` `Added` entry: `offscreen-overflow`, one element per viewport, `major`, hides its horizontal overflow | the `sed -n` range of `[Unreleased]`, then of `### Added`, piped to the four `grep`s prints `1` | `CHANGELOG.md:11` - "`offscreen-overflow` Check: ... It reports one element per viewport, always with severity `major` ... It reports nothing while the page hides its horizontal overflow"; under `### Added` (`:9`), between `## [Unreleased]` (`:7`) and `## [0.1.0]` (`:18`) | PASS |
| C22 | README says `runs three Checks` naming `offscreen-overflow`; `runs two Checks` gone | `grep "runs three Checks" README.md` piped to `grep -c "offscreen-overflow"` prints `1` · `grep -c "runs two Checks" README.md` prints `0` | `README.md:45` - "`detect_visual_bugs` runs three Checks: `text-clipped` ..., `low-contrast-real` ... and `offscreen-overflow` (the element that makes a page wider than its viewport, so that it scrolls horizontally)" | PASS |
| C23 | type check, lint, format and the whole suite are green | `.venv/bin/pyright --pythonpath .venv/bin/python` - 0 errors, 0 warnings, exit 0 · `.venv/bin/ruff check` - All checks passed!, exit 0 · `.venv/bin/ruff format --check` - 94 files already formatted, exit 0 · `.venv/bin/pytest` - 239 passed in 470.51s, exit 0 | the four command outputs under `## Gate` | PASS |

## Level and sampling

- Every check from C1 to C19 is proven through the MCP tool boundary (`detect`/`client.list_tools` against a real Chromium), the same level as the claim. Nothing is mocked under it.
- C11 and C12 are table-driven over all 7 and all 4 members of the sets their claims name. No claim names more cases than its proof runs.
- The negative checks (C11, C12, C14, C15) assert `== []` and nothing else, so on their own they would pass if the Check returned nothing. The positive checks C1 to C10, C13, C16 and C17, which run on the same code path, rule that implementation out. No fault was injected, because the `light` profile does not inject faults.

## Precision notes

These do not block, and the verdict does not depend on them.

- AC 16 of the plan says that the error SHALL **end with** the list, while C18 says that it **holds** the list, and the tests assert `in text`. The code ends the message with the list (`src/squint_mcp/tools/detect_visual_bugs.py:80` - `raise ToolError(f'Unknown check "{name}". Valid checks: {valid}.')`), so AC 16 holds. However, no test would catch a suffix added after the list.
- `Element.tag` (`src/squint_mcp/models.py:49`, set at `src/squint_mcp/js/collect_elements.js:152` - `tag: element.localName`) has no check of its own, as `checks.md` says. C12, C13 and C14 depend on it, because `_computed` at `src/squint_mcp/checks/offscreen_overflow.py:15` selects `html` and `body` by `element.tag`.

## Swept existing

- idempotency - `tests/test_detect_visual_bugs.py::test_the_same_call_returns_the_same_structured_content` exists at `tests/test_detect_visual_bugs.py:126-129` - `assert await detect(client, BUG) == await detect(client, BUG)`. It passed in the full run. The constraint it cites, "a Check is a function of the Capture and holds nothing", holds in the code. `src/squint_mcp/checks/offscreen_overflow.py` keeps only module constants (`_EVIDENCE_PROPERTIES`, `_HIDDEN`, at `:7` and `:9`) and reads only `capture` and `config` in `check` (`:40-84`). Nothing is written to module state. The cited test runs the new Check, because a call with no `checks` runs all three. Its `BUG` page does not scroll sideways at 1440, so the test exercises the Check's empty branch only. That is enough for a pure function. Constraint present.
- The rows marked `n/a` (authorization, concurrency, data lifecycle, dependency failure, state transitions, observability) are policy the user approved, and there is nothing in the code for them to be wrong about.

## Gate

verified at cd7adf2.

- `.venv/bin/pytest` - 239 passed, 0 failed in 470.51s, exit 0
- `.venv/bin/ruff check` - All checks passed!, exit 0
- `.venv/bin/ruff format --check` - 94 files already formatted, exit 0
- `.venv/bin/pyright --pythonpath .venv/bin/python` - 0 errors, 0 warnings, 0 informations, exit 0
