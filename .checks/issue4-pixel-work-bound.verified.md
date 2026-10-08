# Issue #4 pixel work bound Verification

**Verdict**: PASS
**Profile**: light (AGENTS.md declares none; default applies)
**Diff range**: b26d672..989a6cb (HEAD of `fix/pixel-work-timeout`)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

Checks proven: 10 of 10. All proofs were run by the Verifier at `989a6cb`; `git status --short` was empty before the runs. Seven gaps are listed below; none fails a check, three of them are proofs that a wrong implementation would also pass.

## Not run because of the profile

- Step 1, binding sources: `ui` only. The checklist marks no source binding. Issue #4 was read for context (`gh issue view 4 --repo sh4wty1/squint-mcp --json title,body`): the checks follow its direction (bound the cost by reducing the region), and the per-element ceiling was taken as declared policy.
- `Coverage` join, `Test policy` verdicts: `standard`/`ui` only. The checklist carries neither section.
- Fault injection: `standard`/`ui` only. No mutant was run and the tree was never reverted to the pre-fix code, so no proof here was seen to fail. See "Residual risk". What was done instead, outside the tree and without touching it: a scratch script that calls the two tools and the two `vision` functions to observe durations, and that resizes a red/blue 1024x1024 image with each Pillow filter (gap 1).

## Checks

The pytest proofs of C1 to C6 ran in one invocation: `uv run pytest tests/test_low_contrast_real.py <the five named tests of tests/test_inspect_element.py> tests/test_inspect_element.py::test_element_with_no_rendered_box_is_an_error -v --durations=12` - 63 collected, 63 passed in 108.61s, exit 0, each name listed individually as PASSED. The four new tests are added by the range; the three C3 tests and the 55 older tests of `test_low_contrast_real.py` predate it, which is right for "unchanged" claims.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `inspect_element` on `#noise` (1440x10000) succeeds and takes less than 3s longer than on `#big-text` | `...::test_an_element_of_millions_of_colours_adds_little_to_the_call` PASSED (4.59s for both calls) | `tests/test_inspect_element.py:342` - `assert await seconds("#noise", 10000) - small < 3`; `:336` - `assert content["box"]["h"] == height` pins the 10000px element; success by `inspect` at `:72`. Observed by the Verifier over three pairs: -0.16s, +0.25s, +0.31s (2.1-2.5s against 2.3-2.4s) | PASS (see gap 5) |
| C2 | `#halves` (1024x1024) reports `[{"hex": "#ff0000", "share": 0.5}, {"hex": "#0000ff", "share": 0.5}]` | `...::test_a_region_over_the_limit_keeps_its_painted_colours_and_shares` PASSED | `tests/test_inspect_element.py:323-326` - `assert content["sampledColors"] == [{"hex": "#ff0000", "share": 0.5}, {"hex": "#0000ff", "share": 0.5}]`; fixture `tests/fixtures/pixel-cost.html:36-46` | PASS (see gap 1) |
| C3 | The colours sampled from the existing fixtures are unchanged, tests unedited | the three named tests PASSED; `git diff b26d672..HEAD -- tests/test_inspect_element.py` | `tests/test_inspect_element.py:296-299`, `:304-308`, `:316` - the three literals; `git diff --numstat` gives `27 0` for the file and the diff holds no `-` line | PASS |
| C4 | `detect_visual_bugs` with `low-contrast-real` and `#over-noise` painted succeeds and takes less than 10s longer than without it | `...::test_text_over_millions_of_colours_adds_little_to_the_call` PASSED (5.08s for both calls) | `tests/test_low_contrast_real.py:485` - `assert painted - bare < 10`; `:483-484` - `"#over-noise" not in without` / `in with_text` show the text was judged only in the second call; success by `detect` at `tests/helpers.py:34`. Observed over three pairs: +0.78s, +0.78s, +0.83s (2.1s against 2.9s) | PASS (see gaps 2, 3) |
| C5 | `#big-text` reports `contrastRatio == 1.6` and `sampledBackground == "#cccccc"` | `...::test_a_text_over_the_limit_is_still_judged_on_its_worst_part` PASSED | `tests/test_low_contrast_real.py:465-466` - `assert measured["contrastRatio"] == 1.6` / `assert measured["sampledBackground"] == "#cccccc"`; fixture `tests/fixtures/pixel-cost.html:49-61` | PASS (see gap 4) |
| C6 | Every existing test of `low-contrast-real` passes unedited | `uv run pytest tests/test_low_contrast_real.py -v` - 57 passed (55 older, 2 new); `git diff ... -- tests/test_low_contrast_real.py` | `git diff --numstat` gives `31 0` for the file, no `-` line | PASS |
| C7 | `config.py` defines `COLOR_COUNT_MAX_PIXELS` under a `# Source:` comment, and `vision.py` reads it from `config` | both greps, exit 0 | `src/squint_mcp/config.py:24` - `# Source: Squint default, measured for issue #4.` above `:29` - `COLOR_COUNT_MAX_PIXELS = 512 * 512`; `src/squint_mcp/vision.py:40` and `:42` read `config.COLOR_COUNT_MAX_PIXELS` | PASS |
| C8 | `CHANGELOG.md` has an `[Unreleased]` entry saying a region of more than 262,144 pixels is sampled before its colours are counted | `grep -n "262,144" CHANGELOG.md` printed line 25 | `CHANGELOG.md:25` - "of more than 262,144 pixels (512x512) is sampled down to that many before its colours are counted"; `## [Unreleased]` at `:7` is the only `## [` heading in the file, so `:25` is under it | PASS |
| C9 | The files held for the release are not in the diff | `git diff --name-only b26d672..HEAD -- README.md pyproject.toml` printed nothing, exit 0 | `git diff --numstat b26d672..HEAD` lists seven files, neither among them; `CHANGELOG.md` is `4 0` | PASS |
| C10 | Type check, lint, format and the whole suite are green | four commands, see Gate | exit 0 on each | PASS |

## Swept rows resolving to existing code

| Row | Cited | Found | Result |
|---|---|---|---|
| failure modes - a region with no pixels still yields nothing | `tests/test_inspect_element.py::test_element_with_no_rendered_box_is_an_error` | ran, PASSED; `tests/test_inspect_element.py:415` asserts the error that `src/squint_mcp/tools/inspect_element.py:67-72` raises when `sample_colors` returns `[]` (`src/squint_mcp/vision.py:113-114`, before `_countable`) | holds |
| failure modes - a text box with no pixels still yields nothing | `tests/test_low_contrast_real.py::test_text_without_a_box_is_not_reported` | ran, PASSED; `tests/test_low_contrast_real.py:306`; the skip is at `src/squint_mcp/vision.py:88-89` | holds |
| failure modes - a reduced side never rounds down to 0 | `max(1, ...)` | `src/squint_mcp/vision.py:43` | there, but no test reaches it (gap 6) |
| idempotency - the reduction has no randomness | `tests/test_low_contrast_real.py::test_the_same_call_returns_the_same_content` | ran, PASSED, but `:73` calls the `BUG` fixture, whose regions are under the limit: the reduction never runs in it | weak (gap 6) |
| concurrency - holds the loop for a fraction of a second per element | C1, C4 | C1 and C4 pass; the phrase is contradicted by the checklist's own Handoff (gap 7) | holds as a bound, not as worded |

Rows marked *not in scope* are policy and were not judged.

## Gaps (ranked; none blocks the verdict)

1. **C2 does not prove "no blend", and does not prove the reduction either.** `tests/test_inspect_element.py:323-326` passes with no reduction at all (an exact count of `#halves` is 0.5/0.5), and it passes with the alternative the checklist rejects at `.checks/issue4-pixel-work-bound.md:41`: the red/blue edge of `tests/fixtures/pixel-cost.html:43-44` sits at row 512 and the scale is exactly one half, so `reduce(2)` and `resize(..., BOX)` average only like with like. Resizing that image outside the tree: NEAREST, BOX and `reduce(2)` each give two colours at 0.5; BILINEAR, BICUBIC and `thumbnail` give four colours at 0.498. So the test rejects `thumbnail` and nothing else. An odd offset of the edge (511px) would make every averaging filter fail.
2. **No check asserts that the limit applies to the boxes of an element together** (Landing, third choice, `.checks/issue4-pixel-work-bound.md:43`; `src/squint_mcp/vision.py:86`). C4 is the only proof with more than one box and it asserts time alone: reducing each of the three 1440x1440 boxes on its own would cost three counts and still pass under 10s. C5 has one box. "Each keeps its weight" is unasserted.
3. **That weight is approximate, not kept.** `src/squint_mcp/vision.py:43` truncates each box's sides on its own: 500 line boxes of 1440x20 over the limit came out as 194,000 counted pixels, not 262,144, each 20px line reduced to 2 rows where the scale says 2.7. Boxes of mixed heights therefore lose different shares (20px -> 2 of 2.7, 30px -> 4 of 4.0), and a box under `1/scale` pixels high is held at one row by `max(1, ...)`. On a long text over the limit that moves the "a tenth of the text" boundary of `src/squint_mcp/checks/low_contrast_real.py:103`. The comment at `vision.py:82` and the checklist say the weight is kept.
4. **C5 passes without the fix.** `tests/test_low_contrast_real.py:465-466` hold on an exact count too, so the test guards against the reduction losing the band, which is what the claim says ("still"), and is no evidence that `#big-text` was reduced. Same for C2. Only C1 and C4 can tell the fix from its absence, and the profile did not run that experiment.
5. **The timing bounds are loose and the first baseline is warm-up biased.** C1 allows 3s where 0.3s was observed, C4 allows 10s where 0.8s was observed, so a regression of an order of magnitude passes both. In C1, `tests/test_inspect_element.py:341` measures the small element first: run alone, as the Proof line does, that call carried about 0.4s of first-call cost here (2.47s against 2.08s later), which is subtracted from the noise call. The Handoff's "2.3s longer" for C4 (`.checks/issue4-pixel-work-bound.md:111`) was not reproduced: three pairs gave 0.78-0.83s. It errs on the safe side.
6. **Two Swept rows cite tests that do not exercise the reduction.** `test_the_same_call_returns_the_same_content` (`tests/test_low_contrast_real.py:72-73`) runs on regions under the limit; determinism of NEAREST holds by reading `src/squint_mcp/vision.py:47`, not by that test. `max(1, ...)` at `vision.py:43` is reached by no test: every reduced region in `tests/fixtures/pixel-cost.html` is hundreds of pixels a side.
7. **The checklist contradicts itself on how long the loop is held.** `.checks/issue4-pixel-work-bound.md:26` and `:101` say a fraction of a second; `:111-112` and `src/squint_mcp/config.py:26-27` say about two seconds for a text. Observed here: 0.2s for either count on 14.4M noise pixels, 0.8s for the whole Check on `#over-noise`.

## Residual risk

- No fault was injected (profile `light`). That C1 and C4 fail without the fix rests on the checklist's own measurements (5s at half the height, 45s) and was not observed.
- The declared ceiling is real: 54 text elements of 512x512 over noise took 8.25s in `text_backgrounds` alone, before the Check computes a contrast per colour. The issue's "a call never takes much longer than `TOTAL_TIMEOUT_S`" holds per element, not per page; the checklist says so at `:45` and `src/squint_mcp/vision.py:83-85` marks it.
- `sampledColors` of an element over the limit come from a regular NEAREST grid, so a fine periodic pattern can alias. Declared in the docstring (`src/squint_mcp/vision.py:109-110`) and the CHANGELOG; no test covers it.

## Gate

At `989a6cb`:

- `uv run pyright` - 0 errors, 0 warnings, exit 0
- `uv run ruff check` - All checks passed, exit 0
- `uv run ruff format --check` - 77 files already formatted, exit 0
- `uv run pytest` - 199 passed, 0 failed in 287.98s, exit 0
