# PR #7 F3: status lines Verification

**Verdict**: PASS - 9 of 9 checks proven. No claim in the four documents was shown to be false. Six gaps are listed below; none changes a check's result. Gaps 1 and 2 are the ones worth a look before merge.
**Profile**: light (default - `AGENTS.md` declares none)
**Diff range**: b768c98..1760b89 (two commits, documents only; `git diff 883b661..HEAD -- src tests` is empty)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Steps run: 2 (every proof), 3 (assertions, `Swept` rows resolving to existing), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`).
Step 4 (fault injection) is skipped by profile as a step, but C1 to C4 are themselves mutant proofs and were run as the checklist states them, in a scratch worktree of `1760b89` (`<scratchpad>/verify-f3`, removed). Under `PYTHONPATH=<worktree>/src`, `squint_mcp.__file__` resolved to `<worktree>/src/squint_mcp/__init__.py`.

## Binding sources

None marked binding. Opened as context:

| Source item | Opened | Note |
|---|---|---|
| Review `5449173369` of PR #7 | yes - `gh api repos/sh4wty1/squint-mcp/pulls/7/reviews`: `COMMENTED`, on `b768c98` | F3 names four places; each has a check (C5, C6, C7, C8) |
| `validation.md`, "For the maintainer", option (a) | yes - `validation.md:419` | "apply Fix 16 to Fix 19 ... and accept the feature on a re-run of M1, M4, M5 and M6 alone"; C1 to C4 are that re-run |
| `spec.md:284`, DVB-68 | yes | "WHEN the Verifier reports PASS ... `concluída` in both the table and the slice 3 section" - see gap 2 |

## Checks

Unmutated, the four named tests ran in one invocation in the worktree: `4 passed in 8.85s`. Each mutation was applied alone, confirmed with `git diff -U0 -- src` (one line changed, shown below), the named test run, then `git checkout -- src` with an empty `git status --porcelain` before the next.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | M1 (`reversed(names)`) makes the test fail | `git diff`: `detect_visual_bugs.py @@ -73 +73 @@` `-    for name in names:` / `+    for name in reversed(names):`; `pytest -q tests/test_detect_visual_bugs.py::test_the_first_unknown_check_in_the_order_given_is_the_one_named` -> `1 failed` | `tests/test_detect_visual_bugs.py:354` - `assert 'Unknown check "zzz". Valid checks: text-clipped.' in text`; under the mutant the text names `"nope"` | PASS - killed |
| C2 | M4 (`- element.box_model.padding.right` in `_padding_right`) makes the test fail | `git diff`: `text_clipped.py @@ -57 +57 @@ def _padding_right` `+    return element.box.x + element.box_model.border.left + element.client_width - element.box_model.padding.right`; `pytest -q tests/test_text_clipped.py::test_the_strip_ends_at_the_padding_edge_not_at_the_content_edge` -> `1 failed` | `tests/test_text_clipped.py:140` - `assert await findings_on(client, STRIP, "#padded", findings) == []`; under the mutant one Finding, "Text clipped by 190px by its container width" | PASS - killed |
| C3 | M5 (`TRANSFORM_MIN_SIZE_DIFF_PX = 2`) makes the test fail | `git diff`: `config.py @@ -70 +70 @@` `-TRANSFORM_MIN_SIZE_DIFF_PX = 1` / `+... = 2`; `pytest -q tests/test_text_clipped.py::test_an_element_painted_at_another_size_than_laid_out_is_not_reported` -> `1 failed` | `tests/test_text_clipped.py:111-112` - `resized = (..., "#nudged")` / `assert await reported(client, resized) == []`; under the mutant `['#nudged'] == []` | PASS - killed |
| C4 | M6 (`/"/g` in place of `/[\\"]/g`) makes the test fail | `git diff`: `collect_elements.js @@ -20 +20 @@` `-      .replace(/[\\"]/g, "\\$&")` / `+      .replace(/"/g, "\\$&")`; `pytest -q tests/test_selectors.py::test_a_backslash_in_an_attribute_value_is_escaped` -> `1 failed` | `tests/test_selectors.py:107` - `assert await selector_of(client, 26) == '[data-testid="a\\\\b"]'`; under the mutant the selector is `[data-testid="a\b"]` | PASS - killed |
| C5 | `validation.md` records the re-run, one row per mutant, verdict PASS | the three greps print `1`, `1`, `0` | `validation.md:33` (section heading), `:39-44` (table, rows M1, M4, M5, M6), `:8` - `**Verdict**: ✅ PASS (pass 3 itself was ❌ FAIL; ...)`. The four rows state the same mutation, test and failure this run observed | PASS |
| C6 | ROADMAP shows slice 3 `concluída` in table and section; no "no code" line | the three greps print `1`, `3`, `0` | `docs/ROADMAP.md:19` - `\| 3 \| ... \| concluída \|`; `:73` - `- **Status:** concluída. Spec, design e relatório de validação em ...` (inside `## 3.`, which starts at `:60`); the `Andamento` line is gone | PASS |
| C7 | Handoff no longer says no production code; next step is the merge of PR #7 | the two greps print `0`, `1` | `.specs/STATE.md:32` - "Execute done (T1 to T9) and validated ..."; `:35` - "**Next step**: the maintainer merges PR #7. Then slice 4 ..." | PASS |
| C8 | PR description no longer says the Verifier is running or "112 tests"; gives the count at `HEAD` | `gh pr view 7 --json body --jq .body \| grep -c "Still pending\|112 tests"` -> `0`; `... \| grep -c "135 tests"` -> `1` | body: "- [x] `uv run pytest` passes (135 tests)"; the suite at `1760b89` gives 135 passed (Gate) | PASS |
| C9 | type check, lint, format, whole suite green at `HEAD`, 135 tests | see Gate | see Gate | PASS |

C6: the second grep counts three `concluída` status lines without saying which; lines 39, 58 and 73 were read, and 73 is slice 3.

C1 to C4 resolve to tests the range did not touch (added by `6ffb1c7` and `ea482ef`, before `b768c98`). That is what the checks claim: the range records a re-run, it does not add tests.

## Swept rows resolving to existing

| Row | Cited constraint | Holds |
|---|---|---|
| failure modes: C1-C4 - a mutation that does not apply is reported as not applied | each mutation asserted to match exactly once and shown by `git diff` | yes, in this run; the author's own run cannot be inspected |
| authorization: C8 - the PR edit was asked for by the maintainer | conversation | not verifiable from the repo |
| state transitions: C6 - `concluída` only after C1-C4 hold | C1 to C4 hold at `1760b89` | yes |

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section.

## Faults injected

The four mutants of C1 to C4, all killed (table above). No other fault was injected.

## Reading of the documents

- **`validation.md`, who ran the re-run and what it covers**: stated honestly. `:48` says it was not the Verifier of passes 1 to 3 but the session that resolved F3; `:49` names the five commits that changed `src/` after `9500a19`, says M4 and M6 now sit in `_padding_right` and `quoted` (both true: `text_clipped.py:55-57`, `collect_elements.js:18-21`), and ends "No sensor was run on the new source beyond these four mutants". The commits it cites exist and do what it says (`6ffb1c7`, `ea482ef` touch tests and fixtures; `6e952a2` one spec file). The claim that the session "wrote none of Fix 16 to Fix 19" cannot be checked: every commit has the same git author.
- **`docs/ROADMAP.md`**: `concluída` at `:19` and `:73`; slices 4 and 5 still `pendente`. Correct.
- **`.specs/STATE.md` Handoff**: matches the branch. Issue #8 exists and is the order across Checks; slice 4 is `tlc-spec-lean` in the roadmap; the tree is clean. See gaps 3 and 4.
- **PR description**: no claim shown to be wrong. The five review-fix commits exist; issue #8 exists; the tool-list assertion starts at `tests/test_inspect_element.py:421` and is the only change to that file in `389230a..HEAD`. See gap 1.

## Gaps and notes (ranked)

1. **The PR description describes files that are local only.** The branch is two commits ahead of `origin` (`1591a98`, `1760b89`); the PR head is `b768c98`. There, `docs/ROADMAP.md:19` still reads `pendente`, `validation.md:8` still reads `❌ FAIL` and `.specs/STATE.md:32` still says no production code is written. The sentence "`validation.md` records the PASS and `docs/ROADMAP.md` shows slice 3 as `concluída`" becomes true on the PR once the two commits are pushed. A fact, not a failure of a check.
2. **The PASS of `validation.md:8` is not a Verifier's verdict, and the header above it says it is.** `validation.md:6` still reads "**Verifier**: independent sub-agent (author ≠ verifier), verification pass 3 of 3", two lines above a verdict the F3 session wrote. `:10` then says "The verdict is FAIL because ..." right under the line that says PASS. DVB-68 (`spec.md:284`) and `validation.md:181` are worded "WHEN the Verifier reports PASS". The section at `:48` discloses who ran it, so nothing is hidden, and this report now gives the four kills an independent run. It covers those four mutants and nothing else: no spec-anchored check and no sensor ran on the source changed by `7910fe3` to `bc80575`. The PR description says "kill on a re-run" without saying who ran it.
3. **`.specs/STATE.md:32` says "PR #7 is open with both rounds of review answered".** The answer to round 2 (F3) is the two unpushed commits; nothing was posted to the PR after review `5449173369`. `:37` says "Uncommitted files: none" (true) and nothing in the Handoff says a push is due; only `docs/tasks/2026-10-07-pr7-f3-status-lines.md:7` does.
4. **Three places cited this report before it existed.** `validation.md:48`, `docs/tasks/2026-10-07-pr7-f3-status-lines.md:6` ("verificação independente em ...") and `.specs/STATE.md:33` (F3 listed under Completed) were committed in `1760b89`, when `.checks/pr7-f3-status-lines.verified.md` was not in the tree. They hold only once this file is committed.
5. **Pass 3 lines left unmarked inside a PASS report.** `validation.md:183` and `:402` are marked as history; these are not: `:294` ("55/59 killed, 4 survived - FAIL ❌"), `:329` ("❌ 4 surviving mutants"), `:391-393` ("❌ Needs Fix", contradicted by the row added at `:395`), `:405` ("DVB-68 pending on verdict"), `:406` ("127 passed"), `:414` ("the decision goes to the maintainer"). The checklist's one-way door keeps the body of pass 3 as written, so this is the chosen shape; a reader who lands mid-file sees FAIL.
6. **The gate of `validation.md:51` is stated at `883b661`; it was run here at `1760b89`.** Same `src/` and `tests/` (empty diff), same 135. Not re-run at `883b661`.

Could not verify: the author's own mutant run (only the result was reproduced); which session wrote Fix 16 to Fix 19; that the maintainer asked for the PR edit.

## Gate

At `1760b89`. `git status --porcelain` was empty before, and empty after the worktree was removed (`git worktree list` shows the main tree only); this report is the one new file.

- `.venv/bin/pyright` - 0 errors, 0 warnings, 0 informations
- `.venv/bin/ruff check` - All checks passed!, exit 0
- `.venv/bin/ruff format --check` - 69 files already formatted, exit 0
- `.venv/bin/pytest -q` - 135 passed, 0 failed, 172.21s
