# PR #17 review fixes Verification

**Verdict**: PASS - 11 of 11 checks proven, each with its own located line. The gap round 1 ranked first is closed for the page it named: the width now comes from the element that scrolls the viewport, and a test of the range fails without that. What is left is notes, the first of them an arm of the new page script that no fixture runs (gap 1 below). None fails a check.
**Profile**: light (the checklist says so; `AGENTS.md` declares none)
**Diff range**: b987904..be5af2a (nine commits). Scoped this round by 450cfd7..be5af2a (four commits: `0c25b6b` the round 1 report, `ff25190` the checklist with C5 rewritten and C11 added, `4305aac` the code, `be5af2a` the records) and by every round 1 observation that was not a clean PASS.
**Round**: 2 - scoped
**Verifier**: independent sub-agent (author != verifier). It did not write these fixes and had no context beyond the files the brief named. It holds nothing of round 1 beyond its report: what is marked `carried from 450cfd7` is that round's finding, re-read here and not re-derived.

Steps run: 2 (every proof of C1 to C11, at `be5af2a`), 3 (assertions; C5 and C11 in full for the first time; `Swept` rows resolving to existing), the re-verification rules (citations of every touched file refreshed, `Landing` and `Out of scope` against the diff), 5 (report).
Steps skipped by profile: 1 (binding-source comparison, `ui`), the `Coverage` join and `Test policy` verdicts (`standard`, `ui`), 4 (fault injection, `standard`, `ui`).
Three measurements were made beyond the profile, all from `<scratchpad>` and reading the tree only: a script that calls `capture()` and `check()` on 12 fixtures and 11 scratch pages at 400x300 and asks Chromium 153.0.8010.12 for `compatMode`, `scrollingElement`, the two scroll widths and how far `scrollTo(100000, 0)` gets; the same Captures given to the Check module of `450cfd7` and of `b987904`; and the five named tests against a copy of `src/` with the module of `450cfd7` swapped in (selected by `PYTHONPATH`, `__file__` printed to confirm). The real tree was never mutated; `git stash` was not used.
The profile in one line: `light` fits the eleven checks as written, and it is thin for `4305aac` in one place - a `Coverage` row for "which element scrolls the viewport" (`html`, `body`, none) would have shown that the third member has no proof.

## Binding sources

Carried from 450cfd7, with two rows re-opened at be5af2a. None is marked binding.

| Source item | Opened | Note |
|---|---|---|
| Review `5477643823` of PR #17 | carried from 450cfd7; re-opened at be5af2a with `gh pr view 17 --json headRefOid,state,reviews`: still one review, `COMMENTED`, on `b987904`, PR open | F1 should-fix, F2 to F4 nits |
| Its four inline comments | carried from 450cfd7 | every finding has a check: F1 -> C1 to C5 and C11, F2 -> C6, F3 -> C7, F4 -> C8, C9. Since `4305aac` F1 is no longer fixed the way the review suggests (the `scroll_width` of `html`): the width is that of `document.scrollingElement`. The review's own research line (re-opened at be5af2a: "outside quirks mode the root element returns the width of the scrolling area of the viewport") limits its suggestion to that mode, so the change answers the finding and departs from the suggestion; the checklist says the user chose it on 2026-10-10 |
| `.specs/features/offscreen-overflow/plan.md`, `checks.md` | verified at be5af2a | `checks.md` is unedited in the whole range; `plan.md` is edited at `:13`, `:15`, `:17` and `:27`. C5 covers `:13`; the other three are read under "Scope" |
| conversation | no - not available to the Verifier | see "Could not verify" |

## Checks

Verified at be5af2a. One invocation for the five named tests: `uv run pytest <5 node ids> -v -p no:cacheprovider` -> `collected 6 items`, `6 passed in 7.91s`, exit 0, each named as `PASSED`, the two cases of C11 as `[absolute]` and `[quirks-absolute]`. The same six show as `PASSED` again in the whole suite. The `grep` and `git diff` proofs were run in Git Bash from the repo root, as written.

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | `own-scroller` at 400x300: no Finding, and the crop of `#wide` is 480px wide | `...::test_a_body_that_clips_its_own_overflow_yields_no_finding PASSED` | `tests/test_offscreen_overflow.py:174` - `assert await small(client, "own-scroller") == []`; `:176` - `assert await crop_width(client, "own-scroller", "#wide") == 480`. The code under it changed in `4305aac`; measured, the Capture of this page holds `scroll_width` 400 and pixels 480 wide. Carried from 450cfd7: against the module of `b987904` the test fails at `:174` | PASS |
| C2 | `body-under-html`: the one Finding is still on `body` | `...::test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named PASSED` | `tests/test_offscreen_overflow.py:167` - `assert [finding["selector"] for finding in findings] == ["body"]`. Passes against the modules of `450cfd7` and `b987904` too: a guard | PASS |
| C3 | `quirks` at 400x300: one Finding on `#wide`, `measured == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}` | `...::test_a_page_in_quirks_mode_is_measured_like_any_other PASSED` | `tests/test_offscreen_overflow.py:183` - `assert finding["selector"] == "#wide"`; `:184-188` - `assert finding["evidence"]["measured"] == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`; the single Finding by the unpacking at `:182`. On this page `html` and `body` both report 600, so it passes whichever of the two is read: a guard | PASS |
| C4 | the Check takes no width from the pixels | `grep -c "pixels.width" src/squint_mcp/checks/offscreen_overflow.py` prints `0` | `src/squint_mcp/checks/offscreen_overflow.py:70` - `page_width = capture.scroll_width`. `grep -n "pixels"` on the file now hits nothing at all (the comment round 1 found at `:74` went with `4305aac`), so no other spelling reads them | PASS |
| C5 | the `Flow` of the plan says the width is the scroll width of the element that scrolls the viewport, and no longer that the Check reads it from the pixels | first grep prints `1` (`1` or more asked), second prints `0` | `.specs/features/offscreen-overflow/plan.md:13`, the one hit, inside `## Flow` (`:11` to `:18`) - "The width of the page is the scroll width of the element that scrolls the viewport, which the Capture reads in the page with a one-line script" and, same line, "so the width is no longer read from `pixels`. Nor from `html` alone: in quirks mode it is `body` that scrolls the viewport." The sentence matches the code: `src/squint_mcp/js/scroll_width.js:5`, `src/squint_mcp/capture.py:136` | PASS |
| C11 | `#out`, out of the flow and ending at 600px, at 400x300: the one Finding, `measured == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`, with a doctype (`absolute`) and without one (`quirks-absolute`) | `...::test_an_element_out_of_the_flow_is_named_with_or_without_a_doctype[absolute] PASSED`, `...[quirks-absolute] PASSED` - 2 cases, as the proof says | `tests/test_offscreen_overflow.py:191` - `@pytest.mark.parametrize("name", ["absolute", "quirks-absolute"])`; `:197` - `(finding,) = await small(client, name)`, the one Finding; `:198` - `assert finding["selector"] == "#out"`; `:199-203` - `assert finding["evidence"]["measured"] == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`. Expected values are literals at the assertion. Test and both fixtures are new in the range (`4305aac`); `#out` is `position: absolute; left: 500px; width: 100px` at `:13-20` of each fixture, the second of which has no doctype line. Against the module of `450cfd7` the `quirks-absolute` case fails at `:197` (`not enough values to unpack (expected 1, got 0)`); measured, `body` reports 400 on `absolute` and `html` 400 on `quirks-absolute`, so the two cases together rule out reading either element alone | PASS |
| C6 | the `ponytail` note of `check` says a line ending in an inline child names that child | the grep prints `1` | `src/squint_mcp/checks/offscreen_overflow.py:81-83` - "A line that ends in an inline child names that child, whose text it is, and not the block that keeps the line from wrapping.", inside the comment that opens with `ponytail:` at `:79`, in `check` (`:69`). Carried from 450cfd7: measured on the repro of F2, the Finding is on `#tail` | PASS |
| C7 | `tests/helpers.py` holds the decode and `tests/test_offscreen_overflow.py` uses it instead of its own | the greps print `1` and `0`; `...::test_a_page_as_wide_as_its_viewport_yields_no_finding PASSED` | `tests/helpers.py:30-32` - `def decode(image: ImageContent) -> Image.Image:` / `return Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")` (file untouched since 450cfd7, re-read); `tests/test_offscreen_overflow.py:6` imports `decode`, `:41` - `return decode(image).width`, reached by the named test at `:148` - `assert await crop_width(client, "clean", "#fixed", DESKTOP) == 116`. "The one decode" holds for these two files only: see round 1 gap 3 | PASS |
| C8 | the Handoff names slice 8 as the next step and no longer says the commits are local or the PR is to be opened | the greps print `1` and `0` | `.specs/STATE.md:43` - "**Next step**: the next roadmap slice, 8 (`overlap`, `tlc-spec-driven`)."; `:46` - "**Branch**: `feat/offscreen-overflow`, from `origin/main` at `9923762`, in pull request #17."; matches `docs/ROADMAP.md:110` (`8`, `overlap`, `tlc-spec-driven`, `pendente`) | PASS |
| C9 | the task record holds the review of PR #17 and no longer lists the push and the PR as pending | the greps print `1` and `0` | `docs/tasks/2026-10-09-offscreen-overflow.md:11` - "**Review:** PR [#17](https://github.com/sh4wty1/squint-mcp/pull/17). O `the-judge` ... deu COMMENT na rodada 1, com um should-fix e três nits."; `:13` - "**Pendências:** o F3 do review foi atendido em parte, por decisão do mantenedor em 2026-10-10 ...", with no push or pull request in it | PASS |
| C10 | type check, lint, format and the whole suite green; the test files of `9923762` still lose exactly four lines | see Gate; the `git diff ... \| grep -c "^-[^-]"` proof prints `4` | the four removed lines are the four old `Valid checks: low-contrast-real, text-clipped.` assertions of `tests/test_detect_visual_bugs.py`, printed and read. The nine paths of the proof are every file `git ls-tree 9923762 tests/` lists outside `fixtures`. The scoped diff touches none of the nine (`tests/test_offscreen_overflow.py` is not among them) | PASS |

## Measurements

Verified at be5af2a, against Chromium 153.0.8010.12 at 400x300. `scrolls` is `scrollX` after `scrollTo(100000, 0)`; `Capture` is `capture.scroll_width`; the last three columns are what `check()` of each commit returns on the same Capture.

| Page | Mode | `scrollingElement` | `html` / `body` scroll width | scrolls | pixels | Capture | be5af2a | 450cfd7 | b987904 |
|---|---|---|---|---|---|---|---|---|---|
| fixture `absolute` | CSS1Compat | `html` | 600 / 400 | 200 | 600 | 600 | `#out`, 600 | `#out`, 600 | `#out`, 600 |
| fixture `quirks-absolute` | BackCompat | `body` | 400 / 600 | 200 | 600 | 600 | `#out`, 600 | nothing | `#out`, 600 |
| fixture `quirks` | BackCompat | `body` | 600 / 600 | 200 | 600 | 600 | `#wide`, 600 | `#wide`, 600 | `#wide`, 600 |
| fixture `own-scroller` | CSS1Compat | `html` | 400 / 480 | 0 | 480 | 400 | nothing | nothing | `#wide`, 480 |
| fixture `body-under-html` | CSS1Compat | `html` | 600 / 600 | 200 | 600 | 600 | `body`, 600 | `body`, 600 | `body`, 600 |
| F1 repro, doctype, child of 600px | CSS1Compat | `html` | 400 / 600 | 0 | 600 | 400 | nothing | nothing | `#wide`, 600 |
| F1 repro, no doctype | BackCompat | null | 400 / 600 | 0 | 600 | 400 | nothing | nothing | `#wide`, 600 |
| no doctype, F1 styles, `#out` out of the flow (the page of `Out of scope`) | BackCompat | null | 400 / 400 | 200 | 400 | 400 | nothing | nothing | nothing |
| the same with a doctype | CSS1Compat | `html` | 600 / 400 | 200 | 600 | 600 | `#out`, 600 | `#out`, 600 | `#out`, 600 |
| the same, no doctype, `body` positioned | BackCompat | null | 400 / 600 | 0 | 600 | 400 | nothing | nothing | `#out`, 600 |
| `body-under-html` with no doctype | BackCompat | null | 600 / 600 | 200 | 600 | 600 | `body`, 600 | `body`, 600 | `body`, 600 |
| no doctype, default margins, child of 600px | BackCompat | `body` | 608 / 608 | 208 | 608 | 608 | `#wide`, 608 | `#wide`, 608 | `#wide`, 608 |
| no doctype, tall page, `#out` out of the flow | BackCompat | `body` | 400 / 600 | 200 | 600 | 600 | `#out`, 600 | nothing | `#out`, 600 |
| no doctype, `body { overflow-x: hidden }`, child of 600px | BackCompat | `body` | 600 / 600 | 200 (by script; hidden) | 600 | 600 | nothing | nothing | nothing |
| no doctype, `html { overflow-x: hidden }`, `#out` | BackCompat | `body` | 400 / 600 | 200 (by script; hidden) | 600 | 600 | nothing | nothing | nothing |
| fixtures `hidden-html`, `clip-html`, `hidden-body`, `clip-body` | CSS1Compat | `html` | 480 / 480 | 80 (by script) | 480 | 480 | nothing | nothing | nothing |
| fixture `rtl` | CSS1Compat | `html` | 600 / 600 | 0 | 600 | 600 | nothing | nothing | nothing |
| fixture `pseudo` | CSS1Compat | `html` | 600 / 600 | 200 | 600 | 600 | nothing | nothing | nothing |

Two more pages were measured and add nothing: the fixture `one` (400 everywhere, nothing) and a page with no doctype, `direction: rtl` and `#out` (400 / 400, does not scroll, nothing).

What the table settles: every number the checklist's paragraph "After round 1" states (scrolls by 200, `html` 400, `body` 600 and the scrolling element, the two swapped with a doctype); the comments of the two new fixtures; the comment of `scroll_width.js:3-4` (no scrolling element, `html` read); the `Out of scope` row on the quirks page (no scrolling element, neither width nor the pixels hold the 600, and the module of `b987904` returned nothing there too); and that on the four pages that hide their overflow the Capture still holds 480, so it is still the `overflow-x` rule that keeps them silent and the tests of the slice's C11 still test it.

## Scope

Verified at be5af2a for 450cfd7..be5af2a; the paragraph on b987904..450cfd7 is carried from 450cfd7.

`git diff --name-status 450cfd7..be5af2a`: `M .checks/pr17-review-fixes.md`, `A .checks/pr17-review-fixes.verified.md`, `M .specs/STATE.md`, `M .specs/features/offscreen-overflow/plan.md`, `M docs/tasks/2026-10-09-offscreen-overflow.md`, `M src/squint_mcp/capture.py`, `M src/squint_mcp/checks/offscreen_overflow.py`, `A src/squint_mcp/js/scroll_width.js`, `M src/squint_mcp/models.py`, `A` two fixtures, `M tests/test_offscreen_overflow.py`.

Against `Landing` as edited in `ff25190`: every path of the diff is one it names, bar the two files under `.checks/`. Four new fixtures in the whole range (`own-scroller`, `quirks`, `absolute`, `quirks-absolute`): counted. "No stored shape, tool, field or error changes ... The new field of the Capture is internal: no tool returns it": holds by reading - `Capture(` is built in one place (`src/squint_mcp/capture.py:148`), `detect_visual_bugs` returns `CaptureSummary(viewport, stabilized)` (`tools/detect_visual_bugs.py:129`) and `inspect_element` builds its result field by field (`tools/inspect_element.py:73-82`); `tests/test_inspect_element.py::test_structured_content_has_exactly_the_documented_keys` is `PASSED` in the suite. The new page script raises on no page tried, a document with no `html` included (it returned 600 on an XML and on an SVG document).

Against `Out of scope` as edited in `ff25190`: the diff stays inside it. The three older copies of the decode are untouched (`tests/test_inspect_element.py:82`, `tests/test_detect_visual_bugs.py:212`, `:298`, all still there); F2 is not fixed; `checks.md` and `verification.md` of the slice, `CHANGELOG.md`, `README.md`, `tests/helpers.py` and `tests/conftest.py` are not in the diff; nothing is pushed (`ahead 9` of `origin/feat/offscreen-overflow`, PR #17 at `b987904`). The new row, the quirks page whose `body` is its own scroll container, is true as measured (table above).

What the diff holds that no check names, each read and found to say what the code does:

- `plan.md:15` (the script `js/scroll_width.js`, "one page script per file, as the others": `src/squint_mcp/js/` holds four), `:17` ("compares the width the page scrolls"), `:27` (`Impact`: "the Capture gains `scroll_width`", which is `src/squint_mcp/models.py:81`). C5 reads `:13` only.
- `.specs/STATE.md:41`: "F1, F2 and F4, and F3 in part".
- `docs/tasks/2026-10-09-offscreen-overflow.md:7` and `:13`.
- `src/squint_mcp/checks/offscreen_overflow.py:73-76`: the two early returns of round 1 are now one condition, read after the width. Same results on every page of the table.

Carried from 450cfd7, on b987904..450cfd7: `_finding` taking the width as a parameter (`:41`), `_styles` replaced by `_first` (`:10-14`), `_scrolls_right` reading `computed[...]` in place of `.get(..., default)` (`:21-29`), the same behaviour since every element of a Capture holds `overflow-x` and `direction` (`src/squint_mcp/config.py:46`, `:64`). No existing fixture, `conftest.py` or older `test_*.py` is touched.

## The slice's `checks.md` (C1 to C21)

Verified at be5af2a. No claim of it was made false by the diff. Its tests show as `PASSED` in the whole suite: the 25 of `tests/test_offscreen_overflow.py` (21 of the slice, the two of round 1, the two cases of C11), the four of C16 and the one of C18. The C18 proof prints `4`; the C16 grep prints `4`; the three C19 greps print `1`; the C20 greps print `1` and `0`. Its line 10 ("each of them is wider than that in the full-page `pixels`") still holds: no fixture of the slice changed, and C11 to C13 still assert the crop widths. `Impact` of the plan now lists the new field of the Capture, and `Surface` (`plan.md:36`, "no tool, parameter or field is added") is about the tools and stays true.

## Swept rows resolving to existing

Verified at be5af2a.

| Row | Cited constraint | Holds |
|---|---|---|
| failure modes: C1 - a width the page cannot scroll to yields nothing | `src/squint_mcp/checks/offscreen_overflow.py:70-72` - `page_width = capture.scroll_width` / `if page_width <= capture.viewport.width: return []` | yes; asserted at `tests/test_offscreen_overflow.py:174` |
| failure modes: a document with no `html` yields nothing instead of an error | `src/squint_mcp/checks/offscreen_overflow.py:75-76` - `if html is None or not _scrolls_right(html, _first(capture, "body")): return []` | the line is there; no proof, as the row says. Tried again from scratch with an XML document styled by CSS and with an SVG file: `capture()` did not return in 60s on either. Stepped by hand, every stage runs (three elements collected, none of them `html`; `scroll_width.js` returns 600) until `page.screenshot(full_page=True)`, which times out. That is code this diff does not touch, and round 1 saw the same step end in `Target crashed`. So the arm cannot be reached through a Capture today; see note 5 |

## Test policy rows

Skipped by profile; the checklist carries no `Test policy` section.

## Faults injected

Skipped by profile. The one experiment of that kind, verified at be5af2a: the five named tests against the module of `450cfd7` - `1 failed, 5 passed`; `test_an_element_out_of_the_flow_is_named_with_or_without_a_doctype[quirks-absolute]` fails at `tests/test_offscreen_overflow.py:197`, the other five cases pass. Carried from 450cfd7: against the module of `b987904`, the test of C1 fails and those of C2, C3 and C7 pass. No fault was injected into the code of `4305aac` itself.

## Round 1 gaps, as they stand

Verified at be5af2a.

| Round 1 gap | Status | Evidence |
|---|---|---|
| 1. In quirks mode the fix missed a page it used to report | closed for that page; a narrower limit is left, declared | `src/squint_mcp/js/scroll_width.js:5` reads `document.scrollingElement`; on `quirks-absolute` the Capture holds 600 and `check()` names `#out`, where the module of `450cfd7` returns nothing; asserted at `tests/test_offscreen_overflow.py:197-203`. Left: a quirks page whose `body` is its own scroll container and whose overflow is out of the flow scrolls by 200 and gets nothing. It is in `Out of scope`, in the task record (`:13`) and in the script's comment, and the module of `b987904` did not report it either (its pixels are 400 wide) |
| 2. C2 and C3 do not tell the fix from the code it replaced | changed | C2 and C3 are still guards. C11 is the test that tells: its `quirks-absolute` case fails against `450cfd7`, and its `absolute` case is the one a `body`-only reading would fail (`body` reports 400 there). The arm for no scrolling element is still told by nothing: gap 1 below |
| 3. F3 is half done, and two records say more than that | the records are closed, the code is left by decision | `.specs/STATE.md:41` now reads "F3 in part (the three older copies of the crop decode stay, by the user's decision of 2026-10-10)" and the task record `:13` calls them a follow-up. `grep -rn b64decode tests` still finds four copies (`tests/helpers.py:32`, `tests/test_inspect_element.py:82`, `tests/test_detect_visual_bugs.py:212`, `:298`) where the review asked for one |
| 4. The Handoff is silent on the local commits | left | `.specs/STATE.md:43-46` is unchanged; the branch is now `ahead 9` and PR #17 still shows `b987904`. Whoever starts from the Handoff has no line saying a push is due |
| 5. The task record opens its `Como` with the old mechanism | closed, with a residue | `docs/tasks/2026-10-09-offscreen-overflow.md:7` now names the element that scrolls the viewport and 21 fixtures (counted: 21), and says the build read the pixels. Residue: its list of review commits ends at `2655b2a` and leaves out `4305aac` |
| 6. C4 to C9 are proven by text search | left | fits what they claim. C5 was rewritten and is still two greps over the whole file; its one hit is inside `Flow`. A second search for `pixels` in the Check module now hits nothing |

Precision gaps of round 1:

- **C7**: left. True of the two files its greps read, false of `tests/`.
- **C3**: narrowed. The member round 1 named now has C11. Of "quirks" as a set two kinds are still without proof: the declared limit, and the pages with no scrolling element (gap 1).
- **C1**: left. Re-measured: on the 600px repro `check()` returns nothing at `be5af2a` and the module of `b987904` names `#wide`, so 480 and 600 agree.
- **C9**: left. Settled by reading `:13`.
- **C10**: as predicted. `uv run ruff format --check` reports 96 files: 24 Python and 72 Markdown files are tracked.

## Gaps and notes (ranked)

New in round 2, verified at be5af2a. None fails a check.

1. **The arm of the page script for a page with no scrolling element runs on no fixture** (`src/squint_mcp/js/scroll_width.js:5`, `?? document.documentElement`). `scrollingElement` is null only in quirks mode with a `body` that is its own scroll container (by the CSSOM View text, and on the four scratch pages where it was null); the suite has two pages with no doctype (`quirks`, `quirks-absolute`) and on both it is `body`. Measured, the arm is right on the three scratch pages that reach it and are not the declared limit: the F1 repro with no doctype (400, the page does not scroll, nothing), `body-under-html` with no doctype (600, scrolls by 200, `body`) and the positioned `body` (400, does not scroll, nothing). A fallback to `document.body` would read 600 on the first and the third, which is the false positive of F1 again, and every test would still pass. By reading, not by a run: no mutant was built.
2. **The known limit is not in the plan it limits, nor on the field** (`.specs/features/offscreen-overflow/plan.md:58`, `:95-105`; `src/squint_mcp/models.py:82`). Criterion 1 of the plan is unconditional and its `Out of scope` table has no row for the quirks page that scrolls and gets nothing; the docstring of `Capture.scroll_width` says "How wide the page scrolls" with no exception. The limit is written in the checklist (`:18`), the task record (`:13`) and the script (`scroll_width.js:3-4`), so it is recorded, only not where the criteria are read. `Landing` promises the `Flow` and `Impact` of the plan and no more, so this is not a miss against the checklist.
3. **The task record's list of commits leaves out the second fix** (`docs/tasks/2026-10-09-offscreen-overflow.md:7`): "correções do review em `dc43088`, `3d0899c` e `2655b2a`", while the paragraph at `:11` describes what `4305aac` did.
4. **Six edited lines of records have no check** (`plan.md:15`, `:17`, `:27`; `.specs/STATE.md:41`; the task record `:7`, `:13`). Each was read against the code and is accurate; the next edit of them would pass every proof whatever it said.
5. **Outside the range: a document with no `html` never becomes a Capture** (`src/squint_mcp/capture.py:137`, the full-page screenshot). An XML document and an SVG file both stall there, after the new script has answered. Not investigated; no line of this diff is on that path. It is why `offscreen_overflow.py:75` (`html is None`) has no proof and cannot get one from a fixture.

### Precision gaps

- **C11**: none on the values; the claim, the fixtures and the assertion agree to the pixel. Its title case "with a doctype" passes under every implementation the branch has had, so only one of its two cases is evidence about this fix; the other is the guard against the opposite mistake.
- **C5**: the claim is about the `Flow` section and the proofs grep the whole file. Settled by reading: the hit is `:13`.

### `Out of scope`

Verified at be5af2a for the two rows edited in `ff25190`; the rest carried from 450cfd7.

- The three older copies of the decode: now recorded as a follow-up by the user's decision. The conflict stays mechanical: converting them makes the C18 proof of the slice print 7 or more.
- The quirks page whose `body` is its own scroll container, with overflow out of the flow: agreed as a limit. Measured: no scrolling element, `html` 400, `body` 400, pixels 400, the page scrolls by 200. No fact the Capture reads holds the 600, and the first build did not report the page either. The row's "no width the browser reports" is true of the scroll widths and the screenshot; `scrollX` after a scroll does show it, which would mean scrolling the page inside the Capture.
- The fix of F2, the precision gaps of `verification.md`, `checks.md` unedited, `git push` waiting: carried from 450cfd7 and confirmed against the scoped diff.

Could not verify: the conversation the checklist cites (the user's two decisions of 2026-10-10, local commits only) - the repo shows the outcome matches, not that it was said; CI on the nine commits, which are not on the remote.

## Gate

Verified at be5af2a. `git status --porcelain` was empty before the first command and empty after the last command that preceded this report; this file is the one path it lists now. The suite ran once, alone.

- `uv run pyright` - 0 errors, 0 warnings, 0 informations, exit 0
- `uv run ruff check` - All checks passed!, exit 0
- `uv run ruff format --check` - 96 files already formatted, exit 0
- `uv run pytest -v -p no:cacheprovider` - 237 passed, 0 failed, 0 skipped, 372.20s (235 at `450cfd7`, plus the two cases of C11). Per file: `test_detect_visual_bugs` 44, `test_inspect_element` 55, `test_low_contrast_real` 64, `test_offscreen_overflow` 25, `test_ping` 12, `test_selectors` 18, `test_text_clipped` 17, `test_vision` 2
- `git diff 9923762..HEAD -- <the nine test files> | grep -c "^-[^-]"` - 4
