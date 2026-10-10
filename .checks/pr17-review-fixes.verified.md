# PR #17 review fixes Verification

**Verdict**: PASS - 10 of 10 checks proven, each with its own located line. The PASS is about the ten checks as written. Outside every check, a measurement found that the fix of F1 trades the false positive the review reported for a false negative on one kind of page in quirks mode (gap 1); that one is worth a decision before the push.
**Profile**: light (the checklist says so; `AGENTS.md` declares none)
**Diff range**: b987904..450cfd7 (five commits: the checklist `eb4cfd5`, then `dc43088` F3, `3d0899c` F1, `2655b2a` F2, `450cfd7` F4)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier). It did not write these fixes and had no context beyond the files the brief named.

Steps run: 2 (every proof, at `450cfd7`), 3 (assertions, `Swept` rows resolving to existing), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`), 4 (fault injection, `standard`, `ui`).
Two measurements were made beyond the profile, both from `<scratchpad>` and reading the tree only: the four named tests against the Check module of `b987904` (a copy of `src/` with that one file swapped, selected by `PYTHONPATH`, `__file__` printed to confirm), and a script that calls `capture()` and `check()` on eleven scratch pages at 400x300. The real tree was never mutated; `git stash` was not used.

## Binding sources

None marked binding. Opened as context:

| Source item | Opened | Note |
|---|---|---|
| Review `5477643823` of PR #17 | yes - `gh api repos/sh4wty1/squint-mcp/pulls/17/reviews`: one review, `COMMENTED`, on `b987904` | F1 should-fix, F2 to F4 nits |
| Its four inline comments | yes - `gh api .../pulls/17/comments`: `4236444517` (F1, `offscreen_overflow.py:74`), `4236444522` (F2, `:79`), `4236444523` (F3, `tests/test_offscreen_overflow.py:44`), `4236444525` (F4, `.specs/STATE.md:46`) | every finding has a check: F1 -> C1 to C5, F2 -> C6, F3 -> C7, F4 -> C8, C9. F1 is fixed where the review says (the `scroll_width` of `html`, once, passed on to `_finding`); the two nits the review withheld on `:44` and `:73` are gone with the rewrite. F3 is met in part, as the checklist declares |
| `.specs/features/offscreen-overflow/plan.md`, `checks.md` | yes | `checks.md` is unedited in the range; `plan.md` is edited at `:13` and `:17` only, which is C5 |
| conversation | no - not available to the Verifier | see "Could not verify" |

## Checks

One invocation for the four named tests: `uv run pytest <4 node ids> -v -p no:cacheprovider` -> `4 passed in 6.11s`, exit 0, each named as `PASSED`. The same four show as `PASSED` again in the whole suite. The `grep` and `git diff` proofs were run in Git Bash from the repo root, as written.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `own-scroller` at 400x300: no Finding, and the crop of `#wide` is 480px wide | `...::test_a_body_that_clips_its_own_overflow_yields_no_finding PASSED` | `tests/test_offscreen_overflow.py:174` - `assert await small(client, "own-scroller") == []`; `:176` - `assert await crop_width(client, "own-scroller", "#wide") == 480`. Test and fixture are new in the range (`3d0899c`). Against the module of `b987904` this test fails at `:174` (`Extends 80px past the 400px viewport`), so it tells the fix from what it replaced | PASS |
| C2 | `body-under-html`: the one Finding is still on `body` | `...::test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named PASSED` | `tests/test_offscreen_overflow.py:167` - `assert [finding["selector"] for finding in findings] == ["body"]`. The test and its fixture predate the range; the code under it changed (`offscreen_overflow.py:76`), which is what "still" claims. It also passes against the module of `b987904`: a guard, not a proof of the fix | PASS |
| C3 | `quirks` at 400x300: one Finding on `#wide`, `measured == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}` | `...::test_a_page_in_quirks_mode_is_measured_like_any_other PASSED` | `tests/test_offscreen_overflow.py:183` - `assert finding["selector"] == "#wide"`; `:184-188` - `assert finding["evidence"]["measured"] == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`; the single Finding by the unpacking at `:182`. New in the range. Passes against the module of `b987904` too: a guard on the new source of the width. See gap 1 for what its one page does not sample | PASS |
| C4 | the Check takes no width from the pixels | `grep -c "pixels.width" src/squint_mcp/checks/offscreen_overflow.py` prints `0` | `src/squint_mcp/checks/offscreen_overflow.py:76` - `page_width = html.scroll_width`. `grep -n "pixels"` on the file hits `:74` alone, a comment, so no other spelling reads them either | PASS |
| C5 | the `Flow` of the plan names the scroll width of `html` and no longer the pixels | first grep prints `2` (`1` or more asked), second prints `0` | `.specs/features/offscreen-overflow/plan.md:13` - "the width of the page is the scroll width of `html`, which every Capture already holds ... so the width is no longer read from `pixels`"; `:17` - "compares the scroll width of `html` with the viewport's width" | PASS |
| C6 | the `ponytail` note of `check` says a line ending in an inline child names that child | the grep prints `1` | `src/squint_mcp/checks/offscreen_overflow.py:85-87` - "A line that ends in an inline child names that child, whose text it is, and not the block that keeps the line from wrapping.", inside the comment that opens with `ponytail:` at `:83`, in `check` (`:69`). Measured on the repro of F2: the Finding is on `#tail`, so the note describes the code | PASS |
| C7 | `tests/helpers.py` holds the decode and `tests/test_offscreen_overflow.py` uses it instead of its own | the greps print `1` and `0`; `...::test_a_page_as_wide_as_its_viewport_yields_no_finding PASSED` | `tests/helpers.py:30-32` - `def decode(image: ImageContent) -> Image.Image:` / `return Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")`; `tests/test_offscreen_overflow.py:6` imports `decode`, `:41` - `return decode(image).width`, reached by the named test at `:148` - `assert await crop_width(client, "clean", "#fixed", DESKTOP) == 116`. "The one decode" holds for these two files only: see gap 3 | PASS |
| C8 | the Handoff names slice 8 as the next step and no longer says the commits are local or the PR is to be opened | the greps print `1` and `0` | `.specs/STATE.md:43` - "**Next step**: the next roadmap slice, 8 (`overlap`, `tlc-spec-driven`)."; `:46` - "**Branch**: `feat/offscreen-overflow`, from `origin/main` at `9923762`, in pull request #17."; matches `docs/ROADMAP.md:110` (`8`, `overlap`, `tlc-spec-driven`, `pendente`) | PASS |
| C9 | the task record holds the review of PR #17 and no longer lists the push and the PR as pending | the greps print `1` and `0` | `docs/tasks/2026-10-09-offscreen-overflow.md:11` - "**Review:** PR [#17](https://github.com/sh4wty1/squint-mcp/pull/17). O `the-judge` ... deu COMMENT na rodada 1, com um should-fix e três nits."; `:13` - "**Pendências:** o F3 do review foi atendido em parte ...", with no push or pull request in it | PASS |
| C10 | type check, lint, format and the whole suite green; the test files of `9923762` still lose exactly four lines | see Gate; the `git diff ... \| grep -c "^-[^-]"` proof prints `4` | the four removed lines are the four old `Valid checks: low-contrast-real, text-clipped.` assertions of `tests/test_detect_visual_bugs.py`; `tests/helpers.py` only gains lines (`:3-4`, `:10`, `:30-32`). The nine paths of the proof are every file `git ls-tree 9923762 tests/` lists outside `fixtures` | PASS |

## Scope

Inside what the review asks for and what `Out of scope` allows.

`git diff --name-status b987904..HEAD`: `A .checks/pr17-review-fixes.md`, `M .specs/STATE.md`, `M .specs/features/offscreen-overflow/plan.md`, `M docs/tasks/2026-10-09-offscreen-overflow.md`, `M src/squint_mcp/checks/offscreen_overflow.py`, `A` two fixtures, `M tests/helpers.py`, `M tests/test_offscreen_overflow.py`.

- `offscreen_overflow.py`: the width (`:70-80`), `_finding` taking it as a parameter (`:41`), `_styles` replaced by `_first` (`:10-14`) and `_scrolls_right` reading `computed[...]` in place of `.get(..., default)` (`:21-29`). The last is the same behaviour: every element of a Capture holds `overflow-x` and `direction` (`src/squint_mcp/config.py:46`, `:64`), and `text_clipped.py:83`, `:87` index them the same way. One new branch, `:72-73`, returns nothing where there is no `html`.
- No existing fixture, `conftest.py` or older `test_*.py` is touched; `checks.md` and `verification.md` of the slice are unedited.
- Nothing pushed: the branch is `ahead 5` of `origin/feat/offscreen-overflow`, and `gh pr view 17` gives head `b987904`.

## The slice's `checks.md` (C1 to C21)

No claim of it was made false by the diff. Its 23 tests in `tests/test_offscreen_overflow.py` (21 of the slice plus the two new ones), the four of C16 and the one of C18 each show as `PASSED` in the whole suite at `450cfd7`; the C18 proof prints `4`; its line 10 ("each of them is wider than that in the full-page `pixels`") still holds, since no fixture of the slice changed and C11 to C13 still assert the crop widths. Its C19 and C20 were not re-run: `CHANGELOG.md` and `README.md` are not in the diff.

## Swept rows resolving to existing

| Row | Cited constraint | Holds |
|---|---|---|
| failure modes: C1 - a width the page cannot scroll to yields nothing | `src/squint_mcp/checks/offscreen_overflow.py:76-78` - `page_width = html.scroll_width` / `if page_width <= capture.viewport.width: return []` | yes; asserted at `tests/test_offscreen_overflow.py:174` |
| failure modes: a document with no `html` yields nothing instead of an error | `src/squint_mcp/checks/offscreen_overflow.py:72-73` - `if html is None: return []` | the line is there; no proof, as the row says. One attempt to reach it from the scratch script, an SVG file by `file://`, ended in `Page.screenshot: Target crashed` inside `capture()`, so the branch stayed unreached. That crash is in code this diff does not touch and was not investigated |

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section.

## Faults injected

Skipped by profile. The one experiment of that kind is the run against the module of `b987904`: `1 failed, 3 passed` - the test of C1 fails, those of C2, C3 and C7 pass.

## Gaps and notes (ranked)

1. **In quirks mode the `scrollWidth` of `html` is not the width the page scrolls, and the fix now misses a page it used to report** (`src/squint_mcp/checks/offscreen_overflow.py:76`). Measured at 400x300 on a page with no doctype, `html, body { margin: 0 }` and one `position: absolute; left: 500px; width: 100px` element: `compatMode` is `BackCompat`, the page scrolls (`scrollTo(100000, 0)` leaves `scrollX` at 200), the full-page pixels are 600 wide, `body.scrollWidth` is 600 and `documentElement.scrollWidth` is 400. `check()` at `450cfd7` returns nothing; the module of `b987904` names `#abs` with `pageWidth: 600`. The same page with a doctype is reported by both. This is criterion 1 of the approved plan (`plan.md:58`) not met on a page no fixture holds, where it was met before the fix. The review's own research line says the root returns the viewport's scrolling width "outside quirks mode"; C3 was written for that risk, but its page widens `html` with a block in flow, where the two widths agree, and its test name ("measured like any other") says more than one page shows. Neither `html.scroll_width` nor `body.scroll_width` alone is right in quirks mode: on the repro of F1 without a doctype `body.scrollWidth` is 600 and the page does not scroll. The Capture does not hold the mode of the document. No check fails; a decision is due on whether quirks pages matter enough for one more fact in the Capture, or for a labelled limit.
2. **C2 and C3 do not tell the fix from the code it replaced.** Both pass against the module of `b987904`. They are guards on the new source of the width, which is what their claims say ("still", "measured like any other"), and C1 is the only test of the range that fails without the fix. Under `light` no fault was injected into the new code, so nothing shows that the suite catches, for instance, `body.scroll_width` in place of `html.scroll_width` at `:76`.
3. **F3 is half done, and two records say more than that** (`tests/helpers.py:32`, `tests/test_inspect_element.py:82`, `tests/test_detect_visual_bugs.py:212`, `:298`). `grep -rn b64decode tests` finds four copies of the expression where the review asked for one. The checklist declares it and the task record says so (`docs/tasks/2026-10-09-offscreen-overflow.md:13`), but `.specs/STATE.md:41` lists "the review fixes F1 to F4 of pull request #17" as completed and `:44` names no open decision for it.
4. **The Handoff is silent on the five local commits** (`.specs/STATE.md:43-46`). It reads next step slice 8, no uncommitted file, branch in PR #17. PR #17 still shows `b987904`; a session starting from this Handoff has no line telling it a push is due. This is what F4 asked for (what `main` carries after the merge), and the same gap the verification of the PR #16 fixes recorded.
5. **The task record still opens its `Como` with the old mechanism** (`docs/tasks/2026-10-09-offscreen-overflow.md:7`: "a largura da página vem dos `pixels` de página inteira do Capture", "17 fixtures"). The `Review` paragraph at `:11` corrects it four lines down, and there are 19 fixtures now. History read in order, but a reader who stops at `:7` has the wrong source.
6. **C4 to C9 are proven by text search.** That fits what they claim (a source line, a comment, three documents). C4 holds beyond its own grep only because a second search for `pixels` was made here.

### Precision gaps

- **C7**: "holds the one decode of a tool image" is true of the two files its greps read and false of `tests/`, where three more stand. "The decode the new module uses" is what the proofs show.
- **C3**: the claim names one page; "quirks" as a set has at least the member of gap 1, which no proof covers. The test name generalises where the claim does not.
- **C1**: the claim pins the fixture at 480px; the review's repro and the checklist's own measurement are at 600px. Measured here: on the 600px repro `check()` returns nothing at `450cfd7` and named `#wide` at `b987904`, so the two agree.
- **C9**: its second grep proves one Portuguese phrase is gone, not that the push is no longer pending; settled by reading `:13`.
- **C10**: `uv run ruff format --check` reports 95 files against the review's 94. The 95th is `.checks/pr17-review-fixes.md` (24 Python files and 71 Markdown files are tracked, and this ruff formats both); this report makes 96.

### `Out of scope`

- The three older copies of the decode: agreed as a deferral, not as an end state. The conflict is real and mechanical: the three lines sit in two of the nine files whose removed lines C18 of the slice counts, so converting them makes that proof print 7 or more. It is the user's call whether criterion 18 was meant to stop a refactor a reviewer asked for; until then gap 3 stands.
- The fix of F2: agreed, the review says "Skip the fix".
- Precision gaps 1a, 2 and 3 of `verification.md`: agreed, the review reads them as disclosed and does not raise them.
- `checks.md` of the slice unedited, `git push` waiting: both confirmed.
- Not listed and should have been weighed: what "quirks" covers (gap 1).

Could not verify: the conversation the checklist cites (local commits only, the push waiting for the user) - the repo shows the outcome matches, not that it was said; CI on these five commits, which are not on the remote. The two measurements the checklist opens with were reproduced on scratch pages (the F1 repro: pixels 600, `scrollWidth` of `html` 400, `scrollX` 0; no doctype with a 600px child: `scrollWidth` 600, scrolls 200), at `450cfd7` and not at `b987904`, which changes nothing a browser measures.

## Gate

At `450cfd7`. `git status --porcelain` was empty before the first command and empty after the last; this report is the one new file. The suite ran once, alone.

- `uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
- `uv run ruff check` - All checks passed!, exit 0
- `uv run ruff format --check` - 95 files already formatted, exit 0
- `uv run pytest -v -p no:cacheprovider` - 235 passed, 0 failed, 0 skipped, 370.81s (233 at `b987904` in the review, plus the two of C1 and C3). Per file: `test_detect_visual_bugs` 44, `test_inspect_element` 55, `test_low_contrast_real` 64, `test_offscreen_overflow` 23, `test_ping` 12, `test_selectors` 18, `test_text_clipped` 17, `test_vision` 2
- `git diff 9923762..HEAD -- <the nine test files> | grep -c "^-[^-]"` - 4
