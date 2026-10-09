# Pixel budget per Capture verification

**Verdict**: PASS
**Profile**: light
**Diff range**: f2c6213..70fd50b
**Round**: 2 - scoped
**Verifier**: independent sub-agent (author != verifier)

15 of 15 checks are proven. C14, the one FAIL of round 1 (written at `30e671a`), now prints `0`.

Scope of this round: the fix `70fd50b` and the one verdict that was not PASS. `git diff --stat 30e671a..70fd50b` shows three files: `src/squint_mcp/vision.py` (one comment line, 1 insertion and 1 deletion, no line moved), `.specs/LESSONS.md` and `.specs/lessons.json` (two lessons recorded, no code). No test, fixture, `config.py`, `CHANGELOG.md` or Check file was touched.

Every proof was re-run at `70fd50b`. `git status --porcelain` before and after shows only this report, untracked. Steps that the `light` profile leaves out did not run: step 1 (binding sources), the `Coverage` recompute, `Test policy` verdicts and fault injection.

## Checks

verified at 70fd50b - every proof re-run; every cited line re-read at this commit.

The gate script splits a table row on every pipe character, escaped or not, so a shell pipeline inside a cell is written "piped to". The commands run were the proofs of `checks.md` verbatim, in Git Bash.

Pytest proofs ran in one invocation: `uv run pytest tests/test_low_contrast_real.py tests/test_inspect_element.py -v` - 119 passed in 248.59s, exit 0, each test named below shown individually as `PASSED`.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | 55 texts over noise: succeeds, each reported, under 10s more than without them | `test_many_texts_over_millions_of_colours_add_little_to_the_call` PASSED | `tests/test_low_contrast_real.py:518` - `assert with_texts == without + 55` · `:519` - `assert painted - bare < 10` | PASS |
| C2 | under the budget together, a text is still judged on exactly a tenth of its pixels | `test_a_tenth_of_the_text_at_its_right_edge_is_enough` PASSED · `test_under_a_tenth_of_the_text_at_its_left_edge_is_not_reported` PASSED | `tests/test_low_contrast_real.py:245` - `assert finding["evidence"]["measured"]["contrastRatio"] == 1.6` · `:256` - `assert await bounds(client, "#left") == []` | PASS |
| C3 | `#small` among the 55 texts keeps `2.84` and `#ffffff` | `test_a_small_text_among_many_large_ones_keeps_its_ratio` PASSED | `tests/test_low_contrast_real.py:528` - `assert finding["evidence"]["measured"]["contrastRatio"] == 2.84` · `:529` - `assert finding["evidence"]["measured"]["sampledBackground"] == "#ffffff"` | PASS |
| C4 | `#big-text` next to `#over-noise` keeps `1.6` and `#cccccc` | `test_a_text_over_the_limit_next_to_another_is_still_judged_on_its_worst_part` PASSED | `tests/test_low_contrast_real.py:536` - `assert finding["evidence"]["measured"]["contrastRatio"] == 1.6` · `:537` - `assert finding["evidence"]["measured"]["sampledBackground"] == "#cccccc"` | PASS |
| C5 | two calls on the 55 texts return the same content | `test_the_same_call_on_many_texts_returns_the_same_content` PASSED | `tests/test_low_contrast_real.py:544` - `assert await detect(client, f"{PIXEL_BUDGET}#texts", checks=ONLY) == first` | PASS |
| C6 | every `low-contrast-real` test of `f2c6213` passes unedited | `tests/test_low_contrast_real.py` - 64 passed (57 from the base, 7 new) · `git diff f2c6213..HEAD -- tests/test_low_contrast_real.py` piped to `grep -c "^-[^-]"` prints `0` | the diff of `tests/test_low_contrast_real.py` holds two hunks, `@@ -24,6 +24,8 @@` and `@@ -498,3 +500,54 @@`, with no removed line | PASS |
| C7 | `#rows`, `#columns`, `#checker`: exactly red and blue, each share 0.4 to 0.6 | `test_a_sampled_pattern_keeps_both_its_colours[#rows]`, `[#columns]`, `[#checker]` all PASSED (3 cases) | `tests/test_inspect_element.py:336` - `assert sorted(color["hex"] for color in colors) == ["#0000ff", "#ff0000"]` · `:337` - `assert all(0.4 <= color["share"] <= 0.6 for color in colors)` | PASS |
| C8 | `#halves`: exactly red and blue, within 0.01 of 0.499 and 0.501 | `test_a_region_over_the_limit_keeps_its_painted_colours_and_shares` PASSED | `tests/test_inspect_element.py:324` - `assert len(colors) == 2` · `:325-328` - `assert {color["hex"]: color["share"] for color in colors} == {"#ff0000": pytest.approx(0.499, abs=0.01), "#0000ff": pytest.approx(0.501, abs=0.01)}` | PASS |
| C9 | text over 1px rows, either first row: `1.6` and `#cccccc` | `test_text_over_one_pixel_rows_is_judged_on_both_colours[#text-dark-first]` and `[#text-light-first]` PASSED (2 cases) | `tests/test_low_contrast_real.py:552` - `assert measured["contrastRatio"] == 1.6` · `:553` - `assert measured["sampledBackground"] == "#cccccc"` | PASS |
| C10 | two calls on `#rows` return the same `sampledColors` | `test_a_sampled_pattern_is_the_same_on_every_call` PASSED | `tests/test_inspect_element.py:342` - `assert await inspect(client, PATTERNS, "#rows") == first` | PASS |
| C11 | a region within the limit reports the shares of all its pixels, tests unedited | `test_sampled_colors_are_the_painted_colors_by_share` PASSED · `test_sampled_colors_keep_the_three_most_frequent` PASSED | `tests/test_inspect_element.py:297` - `assert content["sampledColors"] == [{"hex": "#ff0000", "share": 0.7857}, {"hex": "#0000ff", "share": 0.2143}]` · `:305` - `assert content["sampledColors"] == [{"hex": "#0a0a0a", "share": 0.4}, {"hex": "#141414", "share": 0.3}, {"hex": "#1e1e1e", "share": 0.2}]`; the diff of the file touches neither test | PASS |
| C12 | `[Unreleased]` names the 262,144 pixels across the texts of a page and the 1px or 2px pattern | the `sed -n` range of `[Unreleased]` piped to `grep -c "262,144"` prints `1` · the same range piped to `grep -c "pattern"` prints `1` | `CHANGELOG.md:11` - "counts at most 262,144 pixels (512x512) across the texts of a page at one viewport" · `CHANGELOG.md:12` - "no longer loses a colour of a 1px or 2px pattern"; both between `## [Unreleased]` (line 7) and `## [0.1.0]` (line 14) | PASS |
| C13 | the `# Source:` comment of `COLOR_COUNT_MAX_PIXELS` says the limit is per Capture for text | `grep -B8 "^COLOR_COUNT_MAX_PIXELS" src/squint_mcp/config.py` piped to `grep -c "Capture"` prints `1` | `src/squint_mcp/config.py:28` - "For text the limit is per Capture: the texts a"; the constant is at `:30` | PASS |
| C14 | `vision.py` no longer points at #11 | `grep -c "#11" src/squint_mcp/vision.py` prints `0` | `src/squint_mcp/vision.py:69` - `# pattern whose period divides the step.`, the issue number removed by `70fd50b`; `grep -n -e ponytail -e issue src/squint_mcp/vision.py` shows `:87` (issue #4), `:92` and `:170` only, none pointing at #11 | PASS |
| C15 | type check, lint, format and the whole suite are green | `uv run pyright` - 0 errors, 0 warnings, exit 0 · `uv run ruff check` - All checks passed, exit 0 · `uv run ruff format --check` - 85 files already formatted, exit 0 · `uv run pytest` - 210 passed in 397.03s, exit 0 | the four command outputs above | PASS |

## Findings

verified at 70fd50b.

None open. The round 1 finding on C14 is closed: the reference the build had added at `src/squint_mcp/vision.py:69` lost its issue number, the check and its proof are as approved, and the `ponytail:` comment of `text_backgrounds` that AC 15 names stays gone.

One observation, not a failure: `ruff format --check` counted 84 files in round 1 and counts 85 now, while `70fd50b` adds no file. The cause was not looked into; the command exits 0 either way.

## Precision gaps

carried from 30e671a - the fix touched no test and no check, and each cited line was re-read at 70fd50b and still stands. These are findings about the checks, not failures of their proofs.

1. **AC 3 and door 1, the cap itself, have no assertion.** `vision.count_limit` (`src/squint_mcp/vision.py:49`) decides "the largest `c` with `sum(min(area, c)) <= budget`" and no test asserts a value it returns. C3 is its only named proof, and `#small` sits on a flat white: it reports `2.84` / `#ffffff` whether it is counted whole or sampled, so C3 does not tell a correct cap from a smaller one, nor from one flat scale for the Capture. C1's timing bound catches a cap that is far too large and nothing else. `70fd50b` records this as lesson L-046 and changes no proof.
2. **C2 does not show that the texts were counted whole.** Its two proofs are tests that existed at `f2c6213` and that the feature did not touch; they hold because the bounds fixture is under the budget. The 57,000 text pixels the claim cites appear in no assertion.
3. **C1 does not assert that the call succeeds** at the cited lines; that rests on the `detect` helper, which was not opened. The count `without + 55` is the nearest located assertion.
4. **C5 and C10 compare two calls inside one process.** They prove the fixed seed is re-applied on every call; they say nothing about a difference between runs or platforms, which `random.Random(0)` makes unlikely but which no proof covers.

## Swept, rows resolving to existing

verified at 70fd50b - `vision.py` is the file the fix touched, so its lines were re-read; they did not move.

| Row | Cited constraint | Found |
| --- | --- | --- |
| failure modes | `tests/test_low_contrast_real.py::test_text_without_a_box_is_not_reported` | yes - `tests/test_low_contrast_real.py:306`, ran and PASSED; the guard is `src/squint_mcp/checks/low_contrast_real.py:97` - `if not behind:` |
| failure modes | a sampled side never rounds down to 0 (`max(1, ...)`) | yes - `src/squint_mcp/vision.py:94` and `:95` |

## Not run or not verified

- Step 1, the `Coverage` recompute, `Test policy` verdicts and fault injection: out of the `light` profile (verified at 70fd50b against the `Profile:` line of `checks.md`).
- carried from 30e671a: the plan marks no source as binding. Of its `Sources`, `.checks/issue4-pixel-work-bound.md` was read in round 1; the GitHub issue #11 and `docs/ROADMAP.md` section 6 were not opened in either round.
- The seconds measured by C1 are not printed by the test; only that the difference was under 10.
- The two lesson entries `70fd50b` adds to `.specs/LESSONS.md` and `.specs/lessons.json` were read in the diff and not validated with `scripts/lessons.py`; no check covers them.

## Gate

verified at 70fd50b.

`uv run pytest` - 210 passed, 0 failed
