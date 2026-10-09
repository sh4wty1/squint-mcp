# PR #16 review fixes Verification

**Verdict**: PASS - 9 of 9 checks proven. The diff stays inside the four findings. Five gaps are listed below; none changes a check's result. Gap 1 is the one worth a decision before merge.
**Profile**: light (default - `AGENTS.md` declares none)
**Diff range**: 0b4e767..82c689b (five commits: the checklist, then one per finding F1 to F4)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Steps run: 2 (every proof), 3 (assertions, `Swept` rows resolving to existing), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`).
Step 4 (fault injection) is skipped by profile as a step, but C3 and C4 are themselves mutant proofs and were run as the checklist states them, each in its own copy of `src/` under `<scratchpad>/verify-pr16/` (`c3`, `c4`; the author's `mutA`/`mutB` were not used). Two more mutants were tried there for gap 1 (`x1`, `x2`). The real tree was never mutated and `git stash` was not used.

## Binding sources

None marked binding. Opened as context:

| Source item | Opened | Note |
|---|---|---|
| Review `5471882870` of PR #16 | yes - `gh api repos/sh4wty1/squint-mcp/pulls/16/reviews`: `COMMENTED`, on `0b4e767` | four findings, F1 should-fix, F2 to F4 nits |
| Its four inline comments | yes - `gh api .../pulls/16/comments`: `4231596831` (F1, `vision.py:49`), `4231596841` (F2, `vision.py:137`), `4231596856` (F3, `STATE.md:43`), `4231596865` (F4, `CHANGELOG.md:11`) | each fix asked for has a check: F1 -> C1 to C4, F2 -> C5, C6, F3 -> C7, F4 -> C8. The values of C1 and C2 and the clause of C8 are the ones the review gives, verbatim |
| conversation | no - not available to the Verifier | see "Could not verify" |

## Checks

Unmutated, `uv run pytest tests/test_vision.py -p no:cacheprovider -v` gives `2 passed`, exit 0, both tests named in the output. Both tests are new in the range (`0a43763`).

Each mutation was applied by exact byte replacement (CRLF included, asserted to match once), then shown with `git diff --no-index` against the real file; `diff -rq src <copy>/src` reports `vision.py` as the only source file that differs. Under each `PYTHONPATH`, `python -c "import squint_mcp.vision as v; print(v.__file__)"` printed `<scratchpad>\verify-pr16\<copy>\src\squint_mcp\vision.py`.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `count_limit([100, 300_000, 300_000]) == 131022.0` | whole suite, `-v`: `tests/test_vision.py::test_a_text_under_the_limit_leaves_what_it_does_not_use_to_the_others PASSED` | `tests/test_vision.py:10` - `assert count_limit([100, 300_000, 300_000]) == 131022.0`; (262144 - 100) / 2 is exact in a float | PASS |
| C2 | `count_limit([100, 200]) == math.inf` | whole suite, `-v`: `tests/test_vision.py::test_texts_that_fit_together_have_no_limit PASSED` | `tests/test_vision.py:14` - `assert count_limit([100, 200]) == math.inf` | PASS |
| C3 | `left / larger / 16` at `vision.py:60` makes `tests/test_vision.py` fail | diff: `@@ -59,3 +59,3 @@` `-            return left / larger` / `+            return left / larger / 16`; `PYTHONPATH=<c3>/src uv run pytest tests/test_vision.py -p no:cacheprovider -v` -> `1 failed, 1 passed`, exit 1 | `tests/test_vision.py:10` - `assert 8188.875 == 131022.0`. The test of C2 passes under this mutant, as it must: it never reaches line 60 | PASS - killed |
| C4 | body replaced by `return config.COLOR_COUNT_MAX_PIXELS / len(areas)` makes `tests/test_vision.py` fail | diff: `@@ -55,9 +55,3 @@`, lines 56 to 62 removed, `+    return config.COLOR_COUNT_MAX_PIXELS / len(areas)`; same command with `<c4>/src` -> `2 failed`, exit 1 | `tests/test_vision.py:10` - `assert 87381.33333333333 == 131022.0`; `:14` - `assert 131072.0 == inf` | PASS - killed |
| C5 | `text_backgrounds` takes `together` from `area(background, boxes)` | the two greps print `1` and `0` | `src/squint_mcp/vision.py:137` - `together = area(background, boxes)`. Same value as the sum it replaces: `area` (`:40-46`) and `_region(.., 0)` (`:35-37`, `:135`) both take their sides from `_bounds(pixels, box, 0)` | PASS |
| C6 | the parameter of `_countable` is `together`; nothing in `vision.py` shadows `area` | the grep prints `1`; whole suite, `-v`: `tests/test_low_contrast_real.py` 64 PASSED, `tests/test_inspect_element.py` 55 PASSED | `src/squint_mcp/vision.py:83` - `def _countable(region: Image.Image, together: int, limit: float) -> Image.Image:`. `grep -n "\barea\b" src/squint_mcp/vision.py` hits `:40` (the def), `:86` (docstring prose), `:137` (the call) and nothing else, so no parameter or local is named `area` | PASS |
| C7 | Handoff names slice 7 as next step, no blocker, no open question | the two greps print `0` and `1` | `.specs/STATE.md:43` - "**Next step**: the next roadmap slice, 7 (`offscreen-overflow`, `tlc-spec-lean`)."; `:44` - "**Blockers**: none."; matches `docs/ROADMAP.md:109` (`7`, `offscreen-overflow`, `tlc-spec-lean`, `pendente`) | PASS |
| C8 | the `low-contrast-real` entry under Unreleased has the clause | the grep prints `1` | `CHANGELOG.md:11`, the first entry under `## [Unreleased]` (`:7`) / `### Changed` (`:9`): "... their contrast comes from a sample, and a text of very little ink may not be judged on such a page ([#11](...))" | PASS |
| C9 | type check, lint, format, whole suite green; no approved check, fixture or existing test changed | see Gate; `git diff --stat 0b4e767..HEAD -- tests/fixtures tests/conftest.py tests/helpers.py "tests/test_[!v]*.py" .specs/features/capture-pixel-budget/checks.md` prints nothing | `git diff --name-only 0b4e767..HEAD -- tests .specs/features` prints `tests/test_vision.py` alone, status `A` | PASS |

C6: the listed proofs do not by themselves settle "nothing shadows `area`" (gap 4); the `\barea\b` search above does. The two test files of its second proof were not run as a separate invocation: they ran once, inside the whole suite, and each is counted from the `-v` output.

## Scope

Inside what the review and `Out of scope` allow.

`git diff --name-status 0b4e767..HEAD`: `A .checks/pr16-review-fixes.md`, `M .specs/STATE.md`, `M CHANGELOG.md`, `M src/squint_mcp/vision.py`, `A tests/test_vision.py`.

- `src/squint_mcp/vision.py`: the expression at `:137` (F2), the parameter name at `:83` with its two uses at `:89` and `:91` and the docstring at `:84-87` reworded to the new name (F2). `count_limit` (`:49-62`) is untouched, so F1 added a test and changed no code.
- `tests/test_vision.py`: new, 14 lines, no fixture, imports `count_limit` only (the one-way door of `Landing`).
- `.specs/STATE.md`: lines 43 and 44 only (F3). `CHANGELOG.md`: one clause in line 11 (F4).
- No file under `tests/fixtures`, no `conftest.py`, `helpers.py` or existing `test_*.py`, and not `.specs/features/capture-pixel-budget/checks.md`.
- `docs/tasks/2026-10-08-capture-pixel-budget.md:11` is unedited, as declared (gap 3).
- One commit per finding (`0a43763` F1, `86d4471` F2, `e5034c0` F3, `82c689b` F4) after the checklist (`ef08dec`). Nothing pushed: the branch is `ahead 5` of `origin`, and `gh pr view 16` gives head `0b4e767`.

## Swept rows resolving to existing

| Row | Cited constraint | Holds |
|---|---|---|
| failure modes: C2 - no area over the budget returns `inf`, not a division | `src/squint_mcp/vision.py:62` - `return math.inf`, reached when the loop at `:57-61` never returns | yes; asserted at `tests/test_vision.py:14` |

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section.

## Faults injected

The two mutants of C3 and C4, both killed (table above). Two more, tried for gap 1 and outside any check:

| Mutation | Location | Killed |
|---|---|---|
| `enumerate(sorted(areas))` -> `enumerate(areas)` | `src/squint_mcp/vision.py:57` | no - `2 passed` |
| `pixels * larger > left` -> `>=` | `src/squint_mcp/vision.py:59` | no - `2 passed`; close to equivalent, see gap 1 |

## Gaps and notes (ranked)

1. **`count_limit` without its sort passes the new tests** (`src/squint_mcp/vision.py:57`, `tests/test_vision.py:10`, `:14`). Both inputs are already in ascending order, so dropping `sorted` leaves `2 passed`. The docstring promises the result "whatever the order they come in" (`vision.py:54`), and the one caller passes the areas in the order of the elements (`src/squint_mcp/checks/low_contrast_real.py:174-176`), not sorted. Without the sort, `[300_000, 300_000, 100]` gives 87381.33 where the function gives 131022.0. F1 asked for the two cases that kill its two mutants and the checklist records them as the minimum, so no check fails; the cap is pinned against those two mutants, not against this one. One more input in `tests/test_vision.py`, in descending order, closes it. The `>=` mutant at `:59` also survives, but it only differs when a text exactly uses up its share, where it returns that text's own area in place of going on; no text is sampled differently, so that is not worth a test.
2. **The Handoff says nothing of the five commits that are local only** (`.specs/STATE.md:43-45`). It reads next step slice 7, no blocker, no uncommitted file, which is what F3 asked for and what C7 checks. The branch is five commits ahead of `origin` and PR #16 still shows `0b4e767`; a session that starts from this Handoff has no line telling it a push is due. `:40` also still describes the state at `70fd50b` and does not mention the review of PR #16 or these fixes.
3. **`docs/tasks/2026-10-08-capture-pixel-budget.md:11` still says the push and the pull request wait for the maintainer, and that closing the `count_limit` gap changes an approved check.** Both are now stale: the PR is open, and `0a43763` closed the gap without touching `checks.md`. Declared out of scope in the checklist ("reported, not edited"); reported here.
4. **Precision gap in C6: neither proof settles "nothing in `vision.py` shadows `area`".** The grep matches one signature and the two test files cannot see a shadowing name. A parameter named `area` elsewhere in the file would pass both. Settled here by `grep -n "\barea\b" src/squint_mcp/vision.py` (three hits, none a binding). A proof such as `grep -c "area: \|area = " src/squint_mcp/vision.py` printing 0 would state it.
5. **C5, C7 and C8 are proven by text search, and F2 by reading.** That fits what they claim (a source line, two documents). For C5 no test would tell `area(background, boxes)` from the old sum, because the two are equal by construction (`vision.py:44`, `:37`); the 119 tests of C6 show the behaviour of the Check and of `inspect_element` did not move, not that the two expressions agree.

Could not verify: the conversation the checklist cites (that the maintainer accepted a direct test of `vision.count_limit`, the two minimum cases, the wording of F4, one commit per finding, no push) - the repo shows the outcome matches, not that it was said; the author's own mutant runs in `mutA`/`mutB` (only the result was reproduced, in separate copies); CI on these five commits, which are not on the remote.

## Gate

At `82c689b`. `git status --porcelain` was empty before the first command and empty after the last; this report is the one new file. The suite ran once, alone.

- `uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
- `uv run ruff check` - All checks passed!, exit 0
- `uv run ruff format --check` - 87 files already formatted, exit 0
- `uv run pytest -v -p no:cacheprovider` - 212 passed, 0 failed, 354.36s (210 at `0b4e767` in the review, plus the two of `tests/test_vision.py`). Per file: `test_detect_visual_bugs` 44, `test_inspect_element` 55, `test_low_contrast_real` 64, `test_ping` 12, `test_selectors` 18, `test_text_clipped` 17, `test_vision` 2
