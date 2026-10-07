# PR #7 review fixes Verification

**Verdict**: PASS - 9 of 9 checks proven. One regression was reproduced outside the checklist (gap 1); no check covers it, so it does not change a check's result, but it should be settled before merge.
**Profile**: light (default - `AGENTS.md` declares none)
**Diff range**: 9500a19..bc20192
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Steps run: 2 (every proof), 3 (assertions, `Swept` rows resolving to existing), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`), 4 (fault injection, `standard`, `ui`).
Run beyond the profile, in a scratch worktree (`C:\tmp\squint-pr7-verify`, removed): the new tests against the pre-fix `src/`, and probes of the new code. See "Discrimination" and "Gaps".

## Binding sources

None marked binding. Both reviews and their seven inline comments were opened with `gh api repos/sh4wty1/squint-mcp/pulls/7/reviews` and `.../comments` and read as context:

| Source item | Maps to | Note |
|---|---|---|
| F1 (`text_clipped.py:84`) | C6, C7, C8 | the review offers two fixes; the checklist records the user's choice of the first |
| F2 (`text_clipped.py:89`) | C1 | the clause is the one the review proposes |
| F3 (`docs/ROADMAP.md:74`, stale status lines) | nothing | not a check and not listed under `Out of scope` - see gap 3 |
| F4 (`collect_elements.js:55`) | C2, C4 | `CSS.escape`, as proposed |
| F5 (`config.py:70`) | C5 | passed next to `textLimit`, as proposed |
| Codex P2, line breaks (`collect_elements.js:17`) | C3, C4 | |
| Codex P2, order between Checks (`detect_visual_bugs.py:99`) | `Out of scope` | "an issue is opened for slice 4" - see gap 4 |

## Checks

Every pytest proof ran in one invocation at bc20192: `uv run pytest -v` - 131 collected, 131 PASSED, exit 0. Each test named below appears individually as PASSED in that output.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `#hidden-over-pattern` yields no Finding | `tests/test_text_clipped.py::test_hidden_text_over_a_pattern_is_not_reported PASSED` | `tests/test_text_clipped.py:98` - `assert await reported(client, ("#hidden-over-pattern",)) == []` (test added in 7910fe3) | PASS |
| C2 | clipped `<o:p>` gets `body > main > o\:p` | `tests/test_selectors.py::test_a_tag_name_with_a_colon_is_escaped_in_the_css_path PASSED` | `tests/test_selectors.py:66` - `assert await selector_of(client, 24) == "body > main > o\\:p"` (added in 1827675) | PASS |
| C3 | `data-testid` with a line break gets `[data-testid="line\a break"]` | `tests/test_selectors.py::test_a_line_break_in_an_attribute_value_is_escaped PASSED` | `tests/test_selectors.py:103` - `assert await selector_of(client, 25) == '[data-testid="line\\a break"]'` (added in 8c144c8) | PASS |
| C4 | all 21 Finding selectors of `selectors.html` resolve in `inspect_element` to the Finding's box | `tests/test_selectors.py::test_every_finding_selector_resolves_to_its_element_in_inspect_element PASSED` | `tests/test_selectors.py:138,140` - `(SELECTORS, 21)` / `assert len(findings) == count`; `:150` - `assert result.structured_content["box"] == finding["box"]` | PASS |
| C5 | collector has no literal tolerance; reads the one from config | `grep -c "< 1" src/squint_mcp/js/collect_elements.js` -> `0`; `grep -c "TRANSFORM_MIN_SIZE_DIFF_PX" src/squint_mcp/capture.py` -> `1`; `tests/test_inspect_element.py::test_box_model_content_keeps_the_fractional_size_of_an_untransformed_element PASSED` | `src/squint_mcp/capture.py:117` - `"transformMinSizeDiffPx": config.TRANSFORM_MIN_SIZE_DIFF_PX,`; `src/squint_mcp/js/collect_elements.js:109` - `Math.abs(painted - offset) < transformMinSizeDiffPx`; `tests/test_inspect_element.py:162` - `assert content["boxModel"]["content"] == {"w": 100.5, "h": 60}` | PASS |
| C6 | `#child-overflows` yields no Finding | `tests/test_text_clipped.py::test_fitting_text_beside_an_overflowing_child_is_not_reported PASSED` | `tests/test_text_clipped.py:105` - `assert await reported(client, ("#child-overflows",)) == []` (added in 706c11e) | PASS |
| C7 | `findings[0]` of the bug fixture still equals the literal of DVB-14 | `tests/test_selectors.py::test_first_finding_of_the_bug_fixture_is_the_documented_one PASSED` | `tests/test_selectors.py:110` - `assert findings[0] == {...}`, `:127` - `"measured": {"overflowPx": 50, "scrollWidth": 200, "clientWidth": 150}`; the test is not in the range's diff | PASS |
| C8 | `spec.md` records the decision and DVB-71, traced | `grep -c "DVB-71" .specs/features/detect-visual-bugs-text-clipped/spec.md` -> `5` | `spec.md:67` (Assumptions row "Own text against the edge"), `:182` (criterion 18, `<!-- DVB-71 -->`), `:370` (traceability row, `Implemented`) | PASS |
| C9 | type check, lint, format, whole suite green; only the two enumerating assertions changed | see Gate | `git diff 9500a19..HEAD -- tests` removes three lines: the count `(SELECTORS, 19)` -> `21` (`tests/test_selectors.py:138`), `range(19, 24)` -> `range(19, 26)` (`tests/test_detect_visual_bugs.py:188`), and an HTML comment in `tests/fixtures/selectors.html` ("from 8 to 23" -> "25"). Everything else is added | PASS |

C5: the grep for `"< 1"` would also print 0 for a literal written `<1`; line 109 was read and holds no literal. The `#frac` test does discriminate the wiring: a missing or misspelled key makes the comparison false and the content 101, not 100.5.

C7 resolves to a test the range did not touch. It is a regression proof over code the range changed (`text_clipped.py:95-96`).

## Discrimination (beyond the profile)

HEAD tests against `src/` of 9500a19, one invocation in the scratch worktree:

| Test | With pre-fix `src/` |
|---|---|
| C1 `test_hidden_text_over_a_pattern_is_not_reported` | FAILED - `['#hidden-over-pattern'] == []` |
| C6 `test_fitting_text_beside_an_overflowing_child_is_not_reported` | FAILED - `['#child-overflows'] == []` |
| C2 `test_a_tag_name_with_a_colon_is_escaped_in_the_css_path` | FAILED - `'body > main > o:p'` |
| C3 `test_a_line_break_in_an_attribute_value_is_escaped` | FAILED - raw line break in the selector |
| C4 `test_every_finding_selector_resolves_...` | FAILED - `Invalid selector "body > main > o:p"` |
| C5 `test_box_model_content_keeps_the_fractional_size_...` | PASSED - expected, the checklist says no failing case exists for C5 |
| C7 `test_first_finding_of_the_bug_fixture_is_the_documented_one` | PASSED - expected, a regression proof |

So each fix starts from a case that fails without it, as the checklist's Sources line requires.

## Swept rows resolving to existing

| Row | Cited constraint | In the code |
|---|---|---|
| validation: C2, C3 - a generated selector must be accepted back by `inspect_element` | round trip asserted | yes - `tests/test_selectors.py:147-150`, over all 21 Findings |
| failure modes: C6 - no text rect serialises `null`, not `NaN` (`-Infinity` guarded) | empty-array guard | yes - `src/squint_mcp/js/collect_elements.js:146`, `textRights.length ? Math.max(...textRights) + window.scrollX : null`; the Check reads it at `src/squint_mcp/checks/text_clipped.py:95`, `element.own_text_right is not None`. No test asserts the `null` branch |

All other rows say *not in scope* and were not judged.

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section either.

## Faults injected

Skipped by profile. The "Discrimination" table is a whole-`src/` revert, not a per-surface mutation.

## Gaps and notes (ranked)

1. **Regression, reproduced: one element with very many text rects now fails both tools.** `src/squint_mcp/js/collect_elements.js:146` spreads every text rect into `Math.max(...textRights)`. A short page holding `<pre style="height:300px;overflow:auto">` with 100,000 lines (one text node, one rect per line) makes `detect_visual_bugs` and `inspect_element` return `Locator.evaluate_all: RangeError: Maximum call stack size exceeded`. 60,000 lines still works; 100,000 and 200,000 fail. With `src/` of 9500a19 the same page returns normally (1 Finding, about 1s). Introduced by 706c11e. It also reaches `inspect_element`, which the checklist's `Out of scope` and `spec.md` ("Any change to the behaviour of `inspect_element`") say this change does not touch. The fix is a reduce, or a running maximum inside the loop, in place of the spread.
2. **Behaviour change the checklist does not name: text cut inside an inline child is no longer reported when the parent's own text fits.** `<div class="clipped">Save <b>all the changes right now</b></div>` (150px box, `overflowPx` 180) gave a Finding before the range and gives none at HEAD, because only direct text nodes are measured. `<div class="clipped"><b>Sa</b>ve all the changes right now</div>` is still reported. This follows from the fix F1 asks for and sits next to the existing Out of Scope row "Text clipped by an ancestor that holds no text itself", but that row does not cover a parent that does hold text, and neither DVB-71 nor the new Assumptions row says it. Not judged as a defect; it is a decision somebody should record.
3. F3 of the review (stale status lines in `docs/ROADMAP.md`, `.specs/STATE.md`, `validation.md`, the PR description) has no check and no `Out of scope` line. Nothing in the range touches those files.
4. `Out of scope` says an issue "is opened" for the order between Checks. `gh issue list -R sh4wty1/squint-mcp --state all` shows issues 1, 4 and 5 only; none is about Check order.
5. Line-break coverage: the test covers a line feed in `data-testid` only. Probed here and working at HEAD, with the selector resolving in `inspect_element` to the Finding's box: carriage return (`[data-testid="cr\d x"]`), form feed (`[data-testid="ff\c x"]`), and a line feed in `aria-label` (`div[aria-label="a\a b"]`). All three failed as `Invalid selector` before the range.
6. `spec.md:176` (DVB-30) still names only `#invisible`; `#hidden-over-pattern` is tied to it in the fixtures paragraph (`spec.md:102`), not in the criterion.
7. C5 and C8 rest partly on grep proofs: they prove a string is present or absent. The cited lines were read and say what the checks claim.

## Gate

At bc20192. `git status --porcelain` before and after is the same three files of another session (`.specs/LESSONS.md`, `.specs/lessons.json`, `.specs/features/detect-visual-bugs-text-clipped/validation.md`), untouched, plus this report after.

- `uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
- `uv run ruff check` - All checks passed!, exit 0
- `uv run ruff format --check` - 63 files already formatted, exit 0
- `uv run pytest -v` - 131 passed, 0 failed, 140.93s, exit 0
