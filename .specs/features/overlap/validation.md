# overlap Validation

**Date**: 2026-10-12
**Spec**: `.specs/features/overlap/spec.md` (OVL-01 to OVL-132)
**Diff range**: `eb9778b..c14cd2f` (44 commits, branch `feat/overlap`, base `8aa017c`); the fourth fix round is `5bca797..c14cd2f` (seven commits)
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 5, after the fourth fix round and under the stopping rule the maintainer set on 2026-10-12

**Verdict**: ✅ PASS

**Result**: ✅ PASS

The fourth fix round did what the fourth report and the maintainer asked. The nine mutants that report left alive are all killed, each by the test written for it and each by an assertion on a value. The wait before a screenshot has its bound: a page that never calls an animation frame back is measured. The twelve new criteria are faithful statements of the Terms and the Assumptions, their six fixtures are the pages the criteria describe, and every number in them was worked out again. All 131 criteria due now have an assertion on the outcome the spec defines, no test was removed or weakened, and the gate is green with 368 tests.

The sensor of this pass is the one the spec now defines (Assumptions, "When the discrimination sensor is satisfied"): the nine survivors, the mutants the "Done when" lines of F18 to F23 name, and mutants of the seventeen lines the round changed under `src/`. No fresh mutants were written across the feature.

1. **The nine survivors of the fourth pass: 9 of 9 killed.**
2. **The mutants the tasks name: every claim holds as written.** The timer taken out fails the test of OVL-121 with `Timed out after 30s.`; the step computed for one pixel more fails the test of OVL-132; computed for one pixel less it passes, as F23 says it does.
3. **Mutants of the code the round changed: ten written, none alive that a test of an outcome the spec defines could hold.** The three that change what a call returns on a page a fixture can hold die (the timer taken out, the timer started by the first frame only, the bound made 250 seconds). Six give the same Findings as the code on every page tried and differ in time alone, or not even there. The tenth, the wait taken out whole, is the mutant the test of OVL-120 was written for: it dies on some runs and not on others, which is what the criterion is (a sample of six calls of a timing fault).

Three things found on the way are for the maintainer. None is in the list the stopping rule gives, and none is a wrong Finding or a clean result where a Finding is due. They are recorded as residuals with a proposed issue each ("Residuals and proposed issues"), and the first two are worth reading before the pull request.

- **The test of OVL-120 holds the wait less well than the fourth pass measured.** With the wait taken out it failed on 3 of 10 runs on a quiet machine and on 0 of 3 with three browsers at work; the fourth pass had 5 of 5. The fault itself is still there: 7 calls in 30 lose the Finding of `#low` without the wait, none in 30 with it.
- **A page that replaces `setTimeout` as well as `requestAnimationFrame` by functions that never call back still fails every tool with `Timed out after 30s.`** The bound of F18 is a timer of the page's own world, as the frames are. The spec says the wait "has an end of its own"; on such a page it has none. Flagged as a spec-precision gap.
- **A timer of 0ms in place of the two frames gave no miss in 78 calls.** Whether any frame is needed, and not only whether two are, is not shown.

OVL-67 (the roadmap) is a closing step that follows a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `O` = `tests/test_overlap.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Earlier passes

The four earlier reports are in git in full, at `aef0799`, `0a25cca`, `26d084f` and `ad6c911`. This pass used the fourth as an index of what had been tried and re-derived the rest.

**First pass (`aef0799`): FAIL.** 68 of 68 criteria matched and the gate was green. Of 49 mutants 36 were killed and 13 survived: 2 equivalent and 11 gaps. Four commits closed them with ten criteria (OVL-70 to OVL-79); none touched `src/`.

**Second pass (`0a25cca`): FAIL.** 78 of 78 criteria matched, the gate was green and the eleven survivors were all killed. Of 21 new mutants 8 were killed and 13 survived: 11 gaps, 1 equivalent and 1 with no outcome in the spec. Four commits closed them with twelve criteria (OVL-80 to OVL-91); none touched `src/`.

**Third pass (`26d084f`): FAIL.** 90 of 90 criteria matched, the gate was green (325 tests) and the eleven survivors were all killed. Of 17 new mutants 5 were killed and 12 survived (11 gaps, 1 equivalent), and N14 became a gap. For the first time the code fell short of the spec on pages no fixture held: text under a `filter` that changes colours was never reported, and a glyph colour of alpha 0 outside `rgb()` was. Three spec-precision gaps. Its central finding: each round closed the mutants it was shown and not their neighbours. Nine commits answered it, three of them in `src/`.

| Gap of the third pass | Mutant | Closed by | Criterion |
| --------------------- | ------ | --------- | --------- |
| Text under a `filter` that changes colours not reported (code) | - | `82bbaed` | OVL-92 to OVL-98 |
| A glyph colour of alpha 0 outside `rgb()` reported (code) | - | `c018ab2` | OVL-99, OVL-100 |
| Hidden ink not held inside Text ink | V6 | `b71e582` | OVL-101 to OVL-104 |
| A text painted alone without what is inside it | V15 | `ecdf0e5` | OVL-105, OVL-106 |
| A cover with text that stands before its text in the document | V7 | `ecdf0e5` | OVL-107 |
| Any `open` attribute taken for a Silent layer | V10 | `ecdf0e5` | OVL-108 |
| The severity lowered by a raised cover that is not the Coverer | V1 | `ecdf0e5` | OVL-109, OVL-110 |
| Pseudo-elements left in the glyphs-only screenshot | V4 | `ecdf0e5` | OVL-111 |
| `evidence.computed` written as constants | V14 | `ecdf0e5` | OVL-112 |
| No scroll sideways at hit testing | V3 | `3711dee` | OVL-113 |
| The scroll across the page at capture read as 0 | V17 | `3711dee` | OVL-114 |
| An `info` Finding ordered as a `minor` one (spec-precision gap 3) | V13 | `e4fed09` | OVL-115 |
| Hidden ink under the threshold counted towards the cap | N14 | `70f926d` | OVL-116, OVL-117 |
| The step grown with the pixels, not their square root | V16 | `70f926d` | OVL-118, OVL-119 |
| The Out of Scope row for a pseudo-element; limits of the design not listed (spec-precision gaps 1 and 2) | - | `a8feee6` | rows of Out of Scope |
| Not asked for: a screenshot with a part of the page unpainted | - | `51ff006` | OVL-120 (AD-007) |

**Fourth pass (`ad6c911`): FAIL.** 119 of 119 criteria matched, the gate was green (359 tests) and the twelve survivors of the third pass were all killed. For the first time the unmutated code gave the outcome the spec defines on every probe page inside the scope of the slice (sixteen pages). Of 27 new mutants 17 were killed and 10 survived: 9 gaps and 1 that no test can tell from the code (one animation frame for two). Two spec-precision gaps. F17 (AD-007), taken by the agent with the maintainer away, was found sound and unbounded: a page that never calls an animation frame back failed every tool. The loop was at its bound of three rounds, and the maintainer decided on 2026-10-12: AD-007 stays, with a bound; the nine gaps get their fixture rows; a PASS asks from here on that the mutants a report or a task names die, with those of the code the last round changed. Seven commits answered it, one of them in `src/`.

| Gap of the fourth pass | Mutant | Closed by | Criterion |
| ---------------------- | ------ | --------- | --------- |
| The wait before a screenshot has no end of its own (Fix 6) | - | `bd77a0c` | OVL-121 |
| A `filter` that lists functions of both kinds | F6 | `081e6a1` | OVL-122 |
| A `filter` declared `!important` | F7 | `081e6a1` | OVL-123 |
| `drop-shadow()` kept while ink is measured | F5 | `081e6a1` | OVL-124 |
| `blur()` kept while ink is measured | F4 | `081e6a1` | OVL-125 |
| Every kept function of a `filter` applied, not the first | F8 | `081e6a1` | OVL-126 |
| What is inside a text or a layer, deeper than a child | U1 | `9f58aab` | OVL-127, OVL-128 |
| The Raised layer read from a Coverer that stands first in the document | R1 | `a58e816` | OVL-129, OVL-130 |
| The borders of the texts in the glyphs-only screenshot | B1 | `f99e424` | OVL-131 |
| The cap itself, exactly 20,000 pixels | H1 | `788732c` | OVL-132 |
| The row that counts the changes reaching every Capture (spec-precision gap 1) | - | `bd77a0c` | row of Out of Scope |
| A right-to-left page that scrolls sideways (spec-precision gap 2); the stopping rule | - | `c14cd2f` | rows of Out of Scope and of the Assumptions |

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T13 | ✅ Done | `89385b0` to `cb8d81b`, as in the earlier passes |
| F1 to F17: the fixes of the first three passes | ✅ Done | `7c32a5b` to `a8feee6` |
| F18: an end of its own for the wait before a screenshot | ✅ Done | `bd77a0c`, `src/squint_mcp/capture.py:39-43` and `:122`, `src/squint_mcp/config.py:22` |
| F19: the filter rule beyond a filter of one function | ✅ Done | `081e6a1`, tests and `tests/fixtures/overlap-filters.html` only |
| F20: what is inside a text or a layer, deeper than a child | ✅ Done | `9f58aab`, tests and `tests/fixtures/overlap-nested.html` only |
| F21: the Raised layer of a Coverer that stands first | ✅ Done | `a58e816`, tests and `tests/fixtures/overlap-raised.html` only |
| F22: a text under the border of an element with text | ✅ Done | `f99e424`, tests and `tests/fixtures/overlap-border.html` only |
| F23: the cap itself | ✅ Done | `788732c`, tests and `tests/fixtures/overlap-cap.html` only |
| F24: the stopping rule and the limit of right-to-left pages | ✅ Done | `c14cd2f`, `spec.md` and `tasks.md` only |

Every box of `tasks.md` is ticked (214 `- [x]`, no open box). None is blocked or partial. `git status --porcelain` of the real tree was empty when this pass began, at `c14cd2f`.

`git diff --stat a8feee6..HEAD -- src/` lists two files, `capture.py` (11 lines) and `config.py` (6 lines): the page script, the Check and `covered.py` are byte for byte those the fourth pass read, so its line numbers for them hold.

The "Done when" claims of F18 to F24 were checked, not copied (sensor section and "The rows this round wrote in the spec"). Each claim about a mutant holds. Two sentences of the round do not match what this pass measured, neither of them a claim about behaviour: F18 says the call on the page that never calls a frame back "takes about 5s" and AD-007 says such a page costs "about 4s more"; here the call takes 3.8s to 4.2s in all, 2.3s more than the same page with its frames. The Handoff of `.specs/STATE.md` still describes the state before this round (the fourth pass FAIL, 120 criteria, 359 tests).

**The one deviation from the Fix Plans.** Fix 1 of the fourth report put its five rows in the bounds and the clean fixtures; F19 put them in a page of their own, `overlap-filters.html`. Judged sound. What a `blur(20px)` spreads reaches 60px around its text, and in the clean fixture the whole-page test of OVL-19 runs every Check on every row: a blurred text there could draw a Finding from another Check and turn OVL-19 red for a reason that is not the rule under test. The new page keeps the blurred row apart (`margin-top: 80px`, `padding: 60px 0`, `overflow: hidden`). Nothing is lost by it: the five mutants die on the new page, the list of the three Findings is asserted whole and in order (`tests/test_overlap.py:1275-1279`), and the two silent rows are each shown to be painted under their cover before they are shown to have no Finding (`tests/test_overlap.py:1290`).

---

## Spec-Anchored Acceptance Criteria

Every line number below was located again in this pass, in `tests/test_overlap.py` at `c14cd2f` (1356 lines, 116 test functions, 131 tests with their parameters). The file gained 109 lines in this round and lost none, so each assertion of the first 120 criteria is the one the fourth pass read, at a new line; each was read again against the spec at its new line. The six new fixtures were opened and read against their criteria, and each was also read through `inspect_element` ("The twelve new criteria").

### P1: Report text that another element covers

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-01 one Finding per covered element | exactly one Finding each | `tests/test_overlap.py:76-80` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements, `finding["check"] == "overlap"`, `len(findings) == 4`; `O:477-518` pins the sorted list of the 39 selectors of the bounds fixture, so a second Finding on one element fails | ✅ PASS |
| OVL-02 the four Findings of the bug fixture, in order | `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)`, `(#collision, minor, 20, #stray)` | `O:86-93` - `covered(findings) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-03 summary line | first block, `Found 4 findings in 1 viewport: 2 major, 2 minor.` | `O:99-100` - `texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."` | ✅ PASS |
| OVL-04 same call, same content | equal structured content | `O:104` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| OVL-05 text under the text of another element | one Finding, `hiddenPercent` 20 | `O:110-111` - `finding_on` unpacks exactly one; `["hiddenPercent"] == 20` | ✅ PASS |
| OVL-06 the text on top | no Finding for `#stray` | `O:115-116` - `await findings_on(client, BUG, "#stray", findings) == []` | ✅ PASS |
| OVL-07, OVL-08, OVL-09 `#left`, `#top`, `#bottom`, exactly 10% | one Finding each, 10 | `O:521-526` - parametrized over the three, `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-10 `#three-lines`, middle box | one Finding, 10 | `O:530-531` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-11 `#split`, second text node | one Finding, 10 | `O:535-536` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-12 `#veil-55` | one Finding, 100, `major` | `O:540-542` - `["hiddenPercent"] == 100`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-13 text and cover in one shadow tree | 50, `coveredBy` `[data-testid="shadow-cover"]` | `O:548-552` - `finding["evidence"]["measured"] == {"hiddenPercent": 50, "coveredBy": SHADOW_COVER}` | ✅ PASS |
| OVL-14 `#narrow`, one viewport only | one Finding at 390 × 844, none at 1440 × 900 | `O:122-127` - `... DESKTOP) == []`, `(finding,) = ... MOBILE)`, `finding["viewport"] == MOBILE` | ✅ PASS |
| OVL-15 `#in-dialog` | one Finding, `major` | `O:558` - `(await bounds(client, "#in-dialog"))["severity"] == "major"` | ✅ PASS |
| OVL-16 `#in-fixed` | one Finding, `major` | `O:564` - `(await bounds(client, "#in-fixed"))["severity"] == "major"` | ✅ PASS |
| OVL-17 `low-contrast-bounds.html` | exactly one Finding, `#covered`, 100, `major` | `O:865-869` - `(finding,) = ...["findings"]`, `finding["selector"] == "#covered"`, `["hiddenPercent"] == 100`, `["severity"] == "major"` | ✅ PASS |
| OVL-18 `low-contrast-reach.html` | exactly one Finding, `#veiled-most`, 100 | `O:875-878` - `(finding,) = ...`, `finding["selector"] == "#veiled-most"`, `["hiddenPercent"] == 100` | ✅ PASS |
| OVL-71 a list of several roles | one Finding, 50, `#role-list`, `major` | `O:677-682` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#role-list"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-75 `#opacity-60` | one Finding, 50 | `O:689-690` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-76 two measured texts over each other | `#under-label` 50 by `#label`; `#label` 50 by `#label-cover` | `O:699-708` - both `["measured"] == {...}` dicts, the values of the spec | ✅ PASS |
| OVL-78 `#speck`, all its Hidden ink off the sample | one Finding, 10, `minor`, `#speck-cover` | `O:1010-1015` - `["measured"] == {"hiddenPercent": 10, "coveredBy": "#speck-cover"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-80 four texts stacked in one place | four Findings, all `major`: three at 80 by `#stack-3`, `#stack-3` at 25 by `#stack-cover` | `O:717-728` - `covered(stack) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-81 `#shifted`, a column of its own | one Finding, 10, `minor` | `O:736` - `share_and_severity(await bounds(client, "#shifted")) == (10, "minor")` | ✅ PASS |
| OVL-82 the box of a tag whose glyphs stand beside the text | `#under-tag` 50 by `#tag`; `#tag` 50 by `#tag-cover` | `O:745-754` - both `["measured"] == {...}` dicts | ✅ PASS |
| OVL-83 `#around`, own text around a child with text | one Finding, 10, `minor` | `O:762` - `share_and_severity(await bounds(client, "#around")) == (10, "minor")` | ✅ PASS |
| OVL-87 `#translucent`, glyphs of alpha 0.5 | one Finding, 50 | `O:770-771` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-89 `#filled`, transparent `color`, opaque fill | one Finding, 50 | `O:779-780` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-90 a Silent layer that is not painted | one Finding, 50, `#plain-cover`, `major` | `O:789-794` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#plain-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-86 a page scrolled when it is captured | exactly one Finding, `#far`, 50, `major`, `#far-cover` | `O:974-975` - `covered(findings) == [("#far", "major", 50, "#far-cover")]` | ✅ PASS |
| OVL-92 `#in-grey`, in a row of `filter: grayscale(1)` | one Finding, 50, `#in-grey-cover`, `major` | `O:797-810` (case `#in-grey`) - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#in-grey-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-93 `#own-filter`, `filter: hue-rotate(180deg)` of its own | one Finding, 50, `#own-filter-cover`, `major` | `O:797-810` (case `#own-filter`) - the same two assertions | ✅ PASS |
| OVL-94 `#held`, a cover held by a `filter` alone | one Finding, 50, `#held-cover`, `major` | `O:819-824` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#held-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-95 `filter: invert(1)` on the root | exactly one Finding, `#inverted`, 50, `major`, `#inverted-cover` | `O:831-832` - `covered(findings) == [("#inverted", "major", 50, "#inverted-cover")]` | ✅ PASS |
| OVL-100 `#opaque-oklch`, `#translucent-oklch` | one Finding each, 50 | `O:835-846` - parametrized over the two, `["measured"] == {"hiddenPercent": 50, "coveredBy": f"{selector}-cover"}` | ✅ PASS |
| OVL-101 `#font-whole` | one Finding, 100, `major`, `#font-whole-cover` | `O:1118-1123` - `covered(findings) == [("#font-whole", "major", 100, "#font-whole-cover"), ...]`, the first of three tuples | ✅ PASS |
| OVL-102 `#font-lines` | one Finding, 50, `major`, `#font-lines-cover` | `O:1118-1123` - the second tuple, `("#font-lines", "major", 50, "#font-lines-cover")` | ✅ PASS |
| OVL-103 `#font-veil-55` | one Finding, 100, `major`, `#font-veil-55-cover` | `O:1118-1123` - the third tuple, `("#font-veil-55", "major", 100, "#font-veil-55-cover")` | ✅ PASS |
| OVL-106 `#child-first`, `#child-last` | one Finding each, 16, `minor`, its cover | `O:1162-1175` - parametrized over the two, `["measured"] == {"hiddenPercent": 16, "coveredBy": f"{selector}-cover"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-107 a tag before the text it covers | `#under-tag-first` 50 by `#tag-first`; `#tag-first` 50 by `#tag-first-cover` | `O:1184-1193` - both `["measured"] == {...}` dicts | ✅ PASS |
| OVL-108 an open `details` | one Finding, 50, `#open-details`, `major` | `O:1202-1207` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#open-details"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-111 `#under-after`, `#under-before` | one Finding each, 50, `major`, the owner of the pseudo-element | `O:1237-1250` - parametrized over the two, `["measured"] == {"hiddenPercent": 50, "coveredBy": f"#{pseudo}-owner"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-114 a page scrolled sideways when it is captured | exactly one Finding, `#far`, 50, `major`, `#far-cover` | `O:999-1002` - `covered(findings) == [("#far", "major", 50, "#far-cover")]` | ✅ PASS |
| OVL-122 `#listed`, `filter: grayscale(1) opacity(0.6)` | one Finding, 50, `#listed-cover`, `major` | `tests/test_overlap.py:1274-1279` - `covered(findings) == [("#listed", "major", 50, "#listed-cover"), ...]`, the first of the three tuples of the whole page | ✅ PASS |
| OVL-123 `#weighty`, in a row of `filter: grayscale(1) !important` | one Finding, 50, `#weighty-cover`, `major` | `O:1274-1279` - the second tuple, `("#weighty", "major", 50, "#weighty-cover")` | ✅ PASS |
| OVL-124 `#under-shadow`, 60px under a box and 40px under its `drop-shadow()` | one Finding, 50, `#shadow-cover`, `major` | `O:1274-1279` - the third tuple, `("#under-shadow", "major", 50, "#shadow-cover")` | ✅ PASS |
| OVL-127 `#grandchild-first`, a badge that is the child of a child | one Finding, 16, `minor`, `#grandchild-first-cover` | `tests/test_overlap.py:1302-1305` - `covered(findings) == [("#grandchild-first", "minor", 16, "#grandchild-first-cover")]`, the whole page | ✅ PASS |
| OVL-131 `#under-border`, under the left border of `#bordered` | one Finding, 50, `major`, `#bordered` | `tests/test_overlap.py:1342-1343` - `covered(findings) == [("#under-border", "major", 50, "#bordered")]`, the whole page | ✅ PASS |

### P1: Stay silent on overlaps that are meant

`clean(client, selector)` (`O:225-231`) returns the share of the element's box painted in the colour of the covers, read through `inspect_element`, and the Findings on that box. The first value proves the fixture really paints the cover over the text (or, for OVL-91, OVL-96 and OVL-98, that it does not); the second is the criterion. The three new silent criteria are asserted the same way, with the two values apart.

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-19 the clean fixture, all Checks | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `O:217-222` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| OVL-20 `#stretched` | no Finding | `O:239` - `await clean(client, "#stretched") == (0, [])` | ✅ PASS |
| OVL-21 `#under-faded` | no Finding | `O:244` - `== (0, [])` | ✅ PASS |
| OVL-22 `#veil-45` | no Finding | `O:251-252` - `painted(...)["#737373"] == 0.6`, `await clean(client, "#veil-45") == (0, [])` | ✅ PASS |
| OVL-23 the five roles | no Finding for each | `O:255-262` - parametrized over `menu`, `listbox`, `tooltip`, `dialog`, `alertdialog`: `await clean(client, f"#under-{role}") == (0.5, [])` | ✅ PASS |
| OVL-24 `dialog[open]` | no Finding | `O:269` - `== (0.5, [])` | ✅ PASS |
| OVL-25 open popover, `position: absolute` | no Finding | `O:275` - `== (0.5, [])` | ✅ PASS |
| OVL-26 `position: fixed` | no Finding | `O:280` - `== (0.5, [])` | ✅ PASS |
| OVL-27 `position: sticky` | no Finding | `O:285` - `== (0.5, [])` | ✅ PASS |
| OVL-28 descendant of a `menu` | no Finding | `O:293` - `== (0.5, [])` | ✅ PASS |
| OVL-29 static child of a fixed element | no Finding | `O:301` - `== (0.5, [])` | ✅ PASS |
| OVL-30 shadow tree of a `menu` host | no Finding | `O:572-575` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []` | ✅ PASS |
| OVL-31 `#nick`, 9.5% along the width | no Finding | `O:308` - `== (0.095, [])` | ✅ PASS |
| OVL-32 `#skim`, 5% along the height | no Finding | `O:316` - `== (0.2, [])` | ✅ PASS |
| OVL-33 `#parent-text`, under its own child | no Finding | `O:321` - `== (0.5, [])` | ✅ PASS |
| OVL-34 `#under-ghost`, `pointer-events: none` | no Finding | `O:329` - `== (0.5, [])` | ✅ PASS |
| OVL-35 `#caption` over `#picture` | no Finding for either | `O:338-341` - `painted(...)["#000000"] == 0.24`, both `findings_on(...) == []` | ✅ PASS |
| OVL-36 `#badge` on `#inbox` | no Finding | `O:349` - `== (0.0533, [])` | ✅ PASS |
| OVL-37 `visibility: hidden` | no Finding | `O:354` - `== (0.5, [])` | ✅ PASS |
| OVL-38 `color: transparent` | no Finding | `O:362` - `== (0.5, [])` | ✅ PASS |
| OVL-39 `opacity: 0` | no Finding | `O:367` - `== (0.5, [])` | ✅ PASS |
| OVL-70 a role with spaces and a capital | no Finding | `O:375` - `await clean(client, "#under-spaced-role") == (0.5, [])` | ✅ PASS |
| OVL-72 under what an ancestor paints | no Finding | `O:383` - `await clean(client, "#under-own-row") == (0.5, [])` | ✅ PASS |
| OVL-73 hit testing gives a descendant | no Finding | `O:392` - `await clean(client, "#own-link-text") == (0.5, [])` | ✅ PASS |
| OVL-74 `#opacity-40` | no Finding | `O:399` - `await clean(client, "#opacity-40") == (0.5, [])` | ✅ PASS |
| OVL-88 opaque `color`, transparent fill | no Finding | `O:407` - `await clean(client, "#transparent-fill") == (0.5, [])` | ✅ PASS |
| OVL-91 closed menus | no Finding, and nothing painted over the text | `O:410-416` - parametrized over `#under-removed-menu` and `#under-hidden-menu`: `await clean(client, selector) == (0, [])` | ✅ PASS |
| OVL-96 a cover faded out by `filter: opacity(0)` | no Finding | `O:425` - `await clean(client, "#under-filter-faded") == (0, [])` | ✅ PASS |
| OVL-97 a text faded out by `filter: opacity(0)` | no Finding | `O:432` - `await clean(client, "#filter-faded-text") == (0.5, [])` | ✅ PASS |
| OVL-98 a text above the layer a `filter` makes | no Finding | `O:442-444` - `painted(inspected)["#c8c8c8"] == 0.1667`, `await clean(client, "#above-filter-layer") == (0, [])` | ✅ PASS |
| OVL-99 an alpha of 0 outside `rgb()` | no Finding for each of the three | `O:447-456` - parametrized over `#transparent-oklch`, `#transparent-mix`, `#transparent-none`: `await clean(client, selector) == (0.5, [])` | ✅ PASS |
| OVL-104 `#font-veil-45` | no Finding | `O:1133-1134` - `await findings_on(client, FONT, "#font-veil-45", findings) == []`; the list of `O:1119-1123` holds that the page has three Findings and no fourth | ✅ PASS |
| OVL-105 `#child-and-nick` | no Finding | `O:466` - `await clean(client, "#child-and-nick") == (0.45, [])` | ✅ PASS |
| OVL-125 `#blurred`, `filter: blur(20px)`, half under a cover | no Finding | `tests/test_overlap.py:1282-1292` (case `#blurred`) - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []`; the list of `O:1275-1279` holds that the page has three Findings and no fourth | ✅ PASS |
| OVL-126 `#twice-faded`, `filter: opacity(0.6) grayscale(1) opacity(0.6)` | no Finding | `O:1282-1292` (case `#twice-faded`) - the same two assertions | ✅ PASS |
| OVL-128 `#under-deep-item`, under the child of a child of a `menu` | no Finding | `tests/test_overlap.py:1314-1317` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []`; the list of `O:1303-1305` holds that the page has one Finding and no second | ✅ PASS |

### P1: Severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-40 25% is `major`, 24.5% is `minor` | `#quarter` `major`, `#almost-quarter` `minor` | `O:581-585` - `quarter[...]["hiddenPercent"] == 25`, `quarter["severity"] == "major"`, `almost["severity"] == "minor"` | ✅ PASS |
| OVL-41 `#layered-half` | `minor` | `O:602` - `share_and_severity(...) == (50, "minor")` | ✅ PASS |
| OVL-42 `#layered-corner` | `info` | `O:608` - `== (10, "info")` | ✅ PASS |
| OVL-43 `#layer-ancestor` | `minor` | `O:614-616` - `["coveredBy"] == "#layer-cover"`, `== (50, "minor")` | ✅ PASS |
| OVL-44 `#shared-layer` | `major` | `O:622` - `== (50, "major")` | ✅ PASS |
| OVL-45 `#z-zero` | `major` | `O:626` - `== (50, "major")` | ✅ PASS |
| OVL-46 `#z-static` | `major` | `O:632-634` - `["coveredBy"] == "#z-static-next"`, `== (50, "major")` | ✅ PASS |
| OVL-109 only the cover that is not the Coverer is raised | 50, `#plain-large`, `major` | `O:1216-1221` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#plain-large"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-110 only the Coverer is raised | 50, `#raised-large`, `minor` | `O:1229-1234` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#raised-large"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-115 `major`, `minor`, `info` in one call | `(#c, major, 50, #c-cover)`, `(#b, minor, 10, #b-cover)`, `(#a, info, 10, #a-cover)`; `Found 3 findings in 1 viewport: 1 major, 1 minor, 1 info.` | `O:909-918` - `covered(result.structured_content["findings"]) == [...]`, the three tuples; `texts(result)[0] == "Found 3 findings in 1 viewport: 1 major, 1 minor, 1 info."` | ✅ PASS |
| OVL-129 the Coverer first of two covers, only the other raised | 50, `#plain-large-first`, `major` | `tests/test_overlap.py:1328-1332` - `covered(findings) == [("#under-plain-first", "major", 50, "#plain-large-first"), ...]`, the first of the two tuples of the whole page | ✅ PASS |
| OVL-130 the Coverer first of two covers, only the Coverer raised | 50, `#raised-large-first`, `minor` | `O:1328-1332` - the second tuple, `("#under-raised-first", "minor", 50, "#raised-large-first")` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-47 the Finding of `#half` | the literal of the spec | `O:133-150` - `findings[0] == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| OVL-48 message at 10% | `10% of the text is covered by another element` | `O:154-156` - `["hiddenPercent"] == 10`, `finding["message"] == "10% of the text is covered by another element"` | ✅ PASS |
| OVL-49 truncation | 24 for 24.5% | `O:590-592` - `["hiddenPercent"] == 24`, `finding["message"] == "24% of the text is covered by another element"` | ✅ PASS |
| OVL-50 `#mixed` | 20, `#mixed-card`, `minor` | `O:641-646` - `["measured"] == {"hiddenPercent": 20, "coveredBy": "#mixed-card"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-51 `#two-covers` | 60, `#large-cover` | `O:653-657` - `["measured"] == {"hiddenPercent": 60, "coveredBy": "#large-cover"}` | ✅ PASS |
| OVL-52 `#tie` | 40, `#tie-first` | `O:665-669` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#tie-first"}` | ✅ PASS |
| OVL-53 both selectors work in `inspect_element` | `isError: false`, same `box` for `selector` | `O:852-859` - for the 4 Findings of the bug fixture and the 39 of the bounds fixture (`len(findings) == count`): `inspected["box"] == finding["box"]`, and `inspect` (`O:203`, `result.is_error is False`) on `coveredBy` | ✅ PASS |
| OVL-77 an element the scroll brings over a text | exactly one Finding, `#far`, 50, `#far-cover` | `O:961-966` - `(finding,) = ...["findings"]`, `finding["selector"] == "#far"`, `["measured"] == {"hiddenPercent": 50, "coveredBy": "#far-cover"}` | ✅ PASS |
| OVL-79 the Coverer of a sample | the fifteen tuples in order, `#striped` covered by `#solid-cover` | `O:1023-1032` - `covered(findings) == [...]` | ✅ PASS |
| OVL-84 the rows of a sample | `#row-striped`: 40, `major`, `#row-solid-cover` | `O:1041-1046` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#row-solid-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-85 a page under the cap | exactly one Finding, `#striped`, 25, `major`, `#stripes` | `O:1054-1055` - `covered(findings) == [("#striped", "major", 25, "#stripes")]` | ✅ PASS |
| OVL-112 `evidence.computed` of a positioned text | `{"position": "relative", "z-index": "1"}` for `#positioned`, `{"position": "relative", "z-index": "auto"}` for `#relative` | `O:1253-1263` - parametrized over the two, `finding["evidence"]["computed"] == {"position": "relative", "z-index": z_index}` | ✅ PASS |
| OVL-113 Hidden ink right of the viewport | `(#near, major, 50, #near-cover)`, `(#right, major, 50, #right-cover)`, `(#edge, major, 50, #edge-cover)`, `(#far, major, 50, #far-cover)` | `O:985-991` - `covered(findings) == [...]`, the four tuples | ✅ PASS |
| OVL-116 Hidden ink under a tenth does not count | `(#striped, major, 25, #stripes)` and nine fillers | `O:1077-1078` - `covered(findings) == striped("#stripes", 9)` | ✅ PASS |
| OVL-117 Hidden ink of a text without a Finding counts | `(#striped, major, 25, #solid-cover)` and nine fillers | `O:1087-1088` - `covered(findings) == striped("#solid-cover", 9)` | ✅ PASS |
| OVL-118 a step of 2 up to 80,000 pixels | `(#striped, major, 25, #solid-cover)` and 24 fillers | `O:1096-1097` - `covered(findings) == striped("#solid-cover", 24)` | ✅ PASS |
| OVL-119 a step of 3 from 80,000 pixels on | `(#striped, major, 25, #stripes)` and 40 fillers | `O:1106-1107` - `covered(findings) == striped("#stripes", 40)` | ✅ PASS |
| OVL-132 exactly 20,000 pixels: every one hit tested | `(#striped, major, 25, #stripes)`, nine fillers, `(#last, major, 25, #last-cover)` | `tests/test_overlap.py:1352-1356` - `covered(findings) == [*striped("#stripes", 9), ("#last", "major", 25, "#last-cover")]`, the whole page | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-54 four Checks by default | `overlap` runs with the other three | `O:160-166` - the four `(selector, "overlap")` pairs on a call without `checks`; `O:893-900` - `low-contrast-real` and `overlap` in one default call; the default run of the other two is held by their own modules, which pass | ✅ PASS |
| OVL-55 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `tests/test_detect_visual_bugs.py:339-344` - the literal `in text`; the same list at `D:353`, `D:364` and `D:376` | ✅ PASS |
| OVL-56 the other three Checks on the bug fixture | `[]` | `O:170-171` - `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| OVL-57 order across Checks | `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)` | `O:893-900` - `{severity} == {"minor"}`, the four pairs in order | ✅ PASS |
| OVL-58 the description names `overlap` | names it and says what it reports | `O:175-180` - `` "`overlap` (text another element is painted over" in " ".join(tool.description.split()) `` | ✅ PASS |
| OVL-59 earlier tests unchanged | pass, only the four literals differ | by reading: `git diff --name-status 8aa017c..HEAD -- tests` lists the overlap fixtures, the new `tests/test_overlap.py` and `tests/test_detect_visual_bugs.py`, whose diff is the four `Valid checks:` literals (now at `D:342`, `D:353`, `D:364`, `D:376`) and nothing else; the gate passes | ✅ PASS |
| OVL-60 a hundred covered texts | `isError: false`, 100 Findings | `O:922-930` - `result.is_error is False`, `len(findings) == 100`, and the 100 tuples `(#text-n, major, 50, #cover-n)` | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| Criterion | Evidence | Result |
| --------- | -------- | ------ |
| OVL-61 one module, one function, registered | `src/squint_mcp/checks/overlap.py:88` - `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:23` - `"overlap": overlap.check` | ✅ PASS |
| OVL-62 no `playwright` in the Checks or in `vision.py` | `grep -rn playwright src/squint_mcp/checks src/squint_mcp/vision.py src/squint_mcp/covered.py` finds nothing (exit 1) | ✅ PASS |
| OVL-63 thresholds and roles in `config`, each cited | `src/squint_mcp/config.py:135` `OVERLAP_MIN_HIDDEN_PERCENT = 10` ("Squint default", with the reason, `:132-134`); `:139` `OVERLAP_MAJOR_HIDDEN_PERCENT = 25` ("Squint default", `:137-138`); `:144` `SILENT_LAYER_ROLES` ("WAI-ARIA 1.2", `:141-143`). The lines moved by six with the new `PAINT_WAIT_MAX_S` (`:22`), which carries its source too | ✅ PASS |
| OVL-64 no literal of them in the Check | `src/squint_mcp/checks/overlap.py:49` and `:62` read both thresholds from `config`; no role name appears in the file (grep exit 1). The numbers left are the `* 100` of a percentage (`:49`, `:62`, `:69`) and `== 0` for alpha and ink (`:34`, `:43`) | ✅ PASS |
| OVL-65 CHANGELOG | `CHANGELOG.md:12`, under `## [Unreleased]`: the Check, 10% and 25%, one level lower under a raised layer, what is not reported (declared layers, `fixed` and `sticky`, covers that paint nothing) and the known limits | ✅ PASS |
| OVL-66 README | `README.md:45` - "`detect_visual_bugs` runs four Checks: ... and `overlap` (...)" | ✅ PASS |
| OVL-67 roadmap `concluída` | Pending by design: a closing step after a PASS. `docs/ROADMAP.md:110` says `pendente`, which is right until the closing step is taken | ⏳ Due now that the verdict is PASS |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-68 two viewports | each Finding of the first has one in the second | `O:186-196` - `len(desktop) == 4`, `desktop <= mobile` over `(selector, check)` | ✅ PASS |
| OVL-69 `text-clipped-clean.html` | `[]` | `O:886-887` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |
| OVL-120 a covered text low on a page of layers, six calls in a row | every call: exactly one Finding, `#low`, 50, `major`, `#low-cover` | `O:941-943` - `for _ in range(6): ... assert covered(findings) == [("#low", "major", 50, "#low-cover")]` | ✅ PASS. The criterion is a sample of a timing fault and its test is that sample: see "The wait before a screenshot" for how well it holds the wait today |
| OVL-121 a page that never calls an animation frame back | exactly one Finding, `#still`, 50, `major`, `#still-cover` | `tests/test_overlap.py:952-953` - `covered(findings) == [("#still", "major", 50, "#still-cover")]`, the whole page; `detect` (`tests/helpers.py:42`) fails first on a tool error | ✅ PASS for the page the criterion names. ⚠️ The sentence after its colon is wider than the code: spec-precision gap 1 |

**Status**: ✅ 131 of 131 criteria due now have an assertion on the outcome the spec defines, and every one passes; OVL-67 is the closing step. ⚠️ 1 spec-precision gap flagged (below).

### The twelve new criteria, read critically

Each was checked for three things: that it states a rule the Terms or the Assumptions hold, that its fixture is the page it describes, and that the outcome depends on the rule. The geometry of each was worked out from the HTML, and each element was then read through `inspect_element` on the unmutated code (the share of its box in each colour).

| Criterion | The rule it states | Its fixture, as read | Verdict |
| --------- | ------------------ | -------------------- | ------- |
| OVL-121 | Assumptions, "A screenshot that shows a part of the page unpainted": the wait has an end | `overlap-no-frames.html:10` - `window.requestAnimationFrame = () => 0;` in the head, before any style. One row: text from 40px to 240px, `#still-cover` from 140px to 240px. `inspect_element`: the cover is half of the box | Faithful. The page replaces the one function the criterion names. `setTimeout`, which the bound is made of, is the page's too: gap 1 |
| OVL-122 | Assumptions, "A `filter`": the functions that change colours left out, those that keep them applied | `#listed`, `filter: grayscale(1) opacity(0.6)` on the text. `inspect_element`: its glyphs show as `#666666`, 60 parts in 100 of black | Faithful. 0.6 is above half, so the text has Text ink only if `grayscale()` is left out and has it faded only if `opacity()` is applied |
| OVL-123 | The same row, on a page that declares its filter with more weight than an inline style | `#weighty-row`, `filter: grayscale(1) !important`, around the text and its cover. `inspect_element`: the cover shows as `#2b2b2b`, the grey of its red | Faithful. An inline style without `!important` loses to this rule |
| OVL-124 | The same row: `drop-shadow()` is applied | `#shadow-cover`, box from 180px to 240px (60px), `filter: drop-shadow(-40px 0 0 rgb(200, 0, 0))`: the shadow is the box moved 40px left, 140px to 200px, of which 140px to 180px shows beside the box. 100px together. `inspect_element`: `#c80000` over 0.5 of the box of the text | Faithful. Without the shadow 60px are hidden, 30%; hit testing gives the cover at its box only, which is enough for `coveredBy` |
| OVL-125 | Terms, "Text ink": faded below half by a `filter` | `#blurred`, `filter: blur(20px)`. A block of ink 20px high under a blur of 20px keeps at its middle row about 38 parts in 100 (the share of a normal curve within half a deviation of its centre), less everywhere else. Its row stands 80px under the others with 60px of padding and `overflow: hidden` | Faithful. No pixel reaches half |
| OVL-126 | Assumptions, "A `filter`": every function that keeps colours is applied | `#twice-faded`, `filter: opacity(0.6) grayscale(1) opacity(0.6)`: 0.6 × 0.6 = 0.36. `inspect_element`: its glyphs show as `#a3a3a3`, 36 parts in 100 of black | Faithful. With the first function alone it keeps 60 and is text |
| OVL-127 | Terms, "Other element" and "Text ink": descendants, not children | `#grandchild-first` (`position: relative`) holds `<span><span id="grandchild-badge">`: the badge is the child of a child, 80px wide from the left of the text. `#grandchild-first-cover` from 220px to 240px. 120px × 20 rows = 2400 pixels shown, 400 hidden: 16.6%. `inspect_element`: the grey of the badge is 0.4 of the box | Faithful. The span between the two is in the list of elements, so the badge is not a child there either (mutant U1 dies) |
| OVL-128 | Terms, "Silent layer": "together with its descendants" | `<div role="menu"><div><div id="deep-item">`: two elements down, over 140px to 240px. `inspect_element`: the cover is half of the box | Faithful |
| OVL-129, OVL-130 | Assumptions, "Several elements cover one text": the Raised-layer rule reads the Coverer | Two rows; in each the cover over the last 80px stands first in the document and the one over the first 20px last. `z-index: 1` on `#raised-small-last` and on `#raised-large-first` (both `position: absolute`). 20px + 80px = 50% | Faithful. With OVL-109 and OVL-110 the Coverer is now pinned as the first and as the last of the covers, raised and plain |
| OVL-131 | Terms, "Text ink", with an Other element that has own text and hides by its border | `#bordered`: `position: absolute`, `left: 140px`, `border-left: 100px solid rgb(200, 0, 0)`, content 40px wide with `XX`, no background. The border is 140px to 240px, the glyphs 240px to 280px. `inspect_element`: its box is 140px to 280px | Faithful. The two glyphs are beside the text and all seen, so the element is measured in one screenshot with the text |
| OVL-132 | Terms, "Coverer": "more than 20,000 pixels" | `#striped` 600 + 400, nine fillers of 2000, `#last-cover` from 190px to 240px over 20 rows = 1000: 20,000. The fillers are appended by a script that stands between the first row and the last, so the document order is the one the criterion lists | Faithful. The count is pinned from both sides by the code: the test passes at the cap and fails with the step computed for one pixel more |

### The rows this round wrote in the spec, against the code

| Row | Probe or evidence of this pass | What the code does | Agrees? |
| --- | ------------------------------ | ------------------ | ------- |
| Out of Scope, a right-to-left page that scrolls sideways (`spec.md:49`) | Three pages of this pass, a text half under a cover in the first viewport: `ltr-wide` (3000px wide), `rtl-wide` (the same with `dir="rtl"`), `rtl-plain` (right-to-left, no sideways scroll) | `ltr-wide`: `(#t, major, 50, #t-cover)`. `rtl-wide`: `No findings in 1 viewport.`, and `inspect_element` on the text returns its box (x 1200) painted `#ffffff` over all of it. `rtl-plain`: `(#t, major, 50, #t-cover)`, and `inspect_element` shows the cover over half of the box | ✅ Every clause of the row: no Finding, `inspect_element` reads the wrong pixels, a right-to-left page that does not scroll sideways is measured as any other. The "Done when" of F24 holds |
| Out of Scope, a Content Security Policy that refuses inline styles (`spec.md:48`) | `csp`: a text half under a cover and a text of `rgb(150, 150, 150)` on white, styled from a file, under `style-src file:`; `csp-control`: the same page without the policy. All four Checks | With the policy: `No findings in 1 viewport.`, while `inspect_element` shows the page styled as without it (the cover over half of the text, the grey glyphs). Without it: `(overlap, #t, major, 50, #t-cover)` and `(low-contrast-real, #grey, major)` | ✅ As the row says, for both Checks it names |
| Out of Scope, "Three changes reach every Capture" (`spec.md:56`) | By reading `git diff eb9778b..HEAD -- src/squint_mcp/capture.py` | `src/squint_mcp/capture.py:63-65` launches Chromium with `config.CHROMIUM_ARGS` (`--disable-lcd-text`); `:290` settles the layout in every `capture()`; `:122` waits before every screenshot. `inspect_element` and `detect_visual_bugs` both go through `capture()`. Nothing else in the diff runs without `covered_text` | ✅ Three, and those three |
| Assumptions, the bounded wait (`spec.md:97`), and AD-007 | An instrumented copy of `capture.py` timed every wait | **250ms is what the code does**: `config.py:22` × 1000 at `capture.py:122`; on `overlap-no-frames.html` the ten waits of a call took 254ms to 268ms. **"About 30ms" for two frames is right**: 192 waits on four fixtures (bug, low, bounds, filters) took a median of 24ms to 29ms per page and 50ms at most. "About eight times" is 250 / 28 | ✅ for the bound and for the cost of the frames. ⚠️ "has an end of its own": gap 1. AD-007's "about 4s more on a page of one covered text" is 2.3s more here (3.9s in all against 1.6s): the 4s is the whole call |
| CHANGELOG, Fixed (`CHANGELOG.md:22`) | By reading, against the code and the probes | "lets the page paint two frames before each screenshot, and waits for them 250ms at most: a page that never calls an animation frame back is captured all the same" | ✅ for the page it describes |
| Assumptions, "When the discrimination sensor is satisfied" (`spec.md:100`), and the third Success Criterion (`spec.md:480`) | By reading | The two say the same, and the row gives the history that led to it (11, 11, 12 and 9 alive) | ✅ This pass was run by it |

`validate_spec.py --strict` exits 0 on the spec (0 errors, 0 warnings), as F24 claims.

### Spec-precision gaps

1. ⚠️ **"The wait has an end of its own" is true of the page OVL-121 names and not of every page.** The bound is `setTimeout` called in the page's own world (`src/squint_mcp/capture.py:39-43`), where the frames are asked too. Probe `dead-timers`: the page of OVL-121 with `window.setTimeout = () => 0;` beside the same line for `requestAnimationFrame`. `detect_visual_bugs` and `inspect_element` both return `Timed out after 30s.` With the wait taken out the same page returns `(#t, major, 50, #t-cover)` in 3.2s, and with `setTimeout` alone replaced it is measured (the frames end the wait). So the sentence of `spec.md:97`, the colon clause of OVL-121 (`spec.md:331`) and the comment at `capture.py:36-38` promise more than a timer of the page can give. A library that fakes the clock of a page can replace both functions together, which is how a real page would get there. Not a wrong Finding: the tool says it failed. See residual 2.

The two gaps of the fourth pass are closed: the row that counts the changes says three, and the right-to-left page has its row.

---

"""
## Discrimination Sensor

Run in scratch copies of `src/squint_mcp` at `c14cd2f`, one copy per mutant, in the session's temp directory outside the repository. A copy is put first on `PYTHONPATH`, where it shadows the editable install, and pytest runs from the repository root against the real tests and fixtures; before each run the runner imports `squint_mcp` in the same environment and stops unless it comes from the copy. Each mutation is one text replacement that must match its file exactly once, written by this Verifier from the descriptions in the fourth report and in `tasks.md`. "Killed by" is the test that failed, with what it reported, read from the output. A control copy with no change of behaviour passed all 131 tests of `tests/test_overlap.py`.

The list is the one the stopping rule gives, and no other: (a) the nine survivors of the fourth pass, (b) mutants of the diff of `bd77a0c` under `src/`, (c) the mutants the "Done when" lines of F18 to F23 name where they are not in (a). 21 mutants in all.

### (a) The nine survivors of the fourth pass

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| F4 | `src/squint_mcp/js/covered_text.js:50` | `blur()` is not kept while ink is measured | ✅ Killed - `test_covered_text_that_its_filter_leaves_without_ink_is_not_reported[#blurred]` (a Finding, 50%) and `test_covered_text_under_a_filter_of_several_functions_is_measured` (a fourth tuple, `('#blurred', 'major', 50, '#blurred-cover')`) |
| F5 | `src/squint_mcp/js/covered_text.js:50` | `drop-shadow()` is not kept | ✅ Killed - `test_covered_text_under_a_filter_of_several_functions_is_measured`: `('#under-shadow', 'major', 30, '#shadow-cover')` for 50 |
| F6 | `src/squint_mcp/js/covered_text.js:54` | a `filter` that holds a function to keep is left as the page wrote it | ✅ Killed - the same test: no Finding for `#listed` |
| F7 | `src/squint_mcp/js/covered_text.js:55` | the new `filter` is set without `!important` | ✅ Killed - the same test: no Finding for `#weighty` |
| F8 | `src/squint_mcp/js/covered_text.js:55` | only the first of the kept functions is set (`kept[0]`) | ✅ Killed - `test_covered_text_that_its_filter_leaves_without_ink_is_not_reported[#twice-faded]` (a Finding, 50%) and the list test (a fourth tuple) |
| U1 | `src/squint_mcp/js/covered_text.js:37-43` | what is inside an element is its children, not all of its descendants | ✅ Killed - `test_a_badge_two_elements_down_inside_a_text_is_part_of_it` (`('#grandchild-first', 'major', 50, ...)` for `minor`, 16, and a Finding on `#under-deep-item`) and `test_text_under_an_element_two_elements_down_inside_a_menu_is_not_reported` (a Finding, covered by `#deep-item`) |
| R1 | `src/squint_mcp/checks/overlap.py:66` | the Raised layer is read from the last cover in the document (`covered.covers[-1].raised`) | ✅ Killed - `test_the_severity_reads_the_coverer_when_it_stands_first_of_two_covers`: `#under-raised-first` comes out `major` and `#under-plain-first` `minor` |
| B1 | `src/squint_mcp/js/covered_text.js:232` | the borders of the texts stay painted in the glyphs-only screenshot | ✅ Killed - `test_text_under_the_border_of_an_element_with_text_is_reported`: `[] == [('#under-border', 'major', 50, '#bordered')]` |
| H1 | `src/squint_mcp/covered.py:303` | a page of exactly 20,000 pixels is sampled too (`math.floor(...) + 1` for `math.ceil(...)`) | ✅ Killed - `test_a_page_of_exactly_the_cap_is_hit_tested_at_every_hidden_pixel`: `('#striped', 'major', 25, '#solid-cover')` for `#stripes` |

**9/9 killed**, each by an assertion on a value, on the first run. None is a timeout or a tool error. The two tests of F19 kill their five mutants between them exactly as its "Done when" says: the list test under F5, F6 and F7, the silent test for `#blurred` under F4 and for `#twice-faded` under F8.

### (c) Mutants the "Done when" lines name that are not in (a)

| # | Task | File:line | Mutation | The task says | Outcome |
| - | ---- | --------- | -------- | ------------- | ------- |
| W1 | F18 | `src/squint_mcp/capture.py:42` | the timer taken out of the wait | the test of OVL-121 fails with `Timed out after 30s.` | ✅ Killed - `test_a_page_that_never_calls_an_animation_frame_back_is_measured`: `Error executing tool detect_visual_bugs: Timed out after 30s.` (the mutant's fault is the timeout itself, so this kill is a tool error by design) |
| H1+ | F23 | `src/squint_mcp/covered.py:303` | the step computed for one pixel more (`pixels + 1`) | the test of OVL-132 fails | ✅ Killed - `#solid-cover` for `#stripes` |
| H1- | F23 | `src/squint_mcp/covered.py:303` | the step computed for one pixel less (`pixels - 1`) | the test of OVL-132 passes: "the page holds 20,000 pixels and not one more or less" | ✅ As the task says: it passes. Read as what the task uses it for, a measure of the fixture. As a mutant of its own it is residual 5 |

F18 also claims "the call takes about 5s": 3.8s to 4.2s here. F19 claims the page holds 6000 pixels of Hidden ink to test: three texts of 2000. F20, F21 and F22 name U1, R1 and B1, which are in (a).

### (b) Mutants of the code this round changed

The diff of `bd77a0c` under `src/` is the expression `_PAINTED` (`src/squint_mcp/capture.py:39-43`), its call (`:122`) and `PAINT_WAIT_MAX_S` (`src/squint_mcp/config.py:22`). Each mutant was run against the tests of OVL-120 and OVL-121. For each: can a test tell it from the code?

| # | File:line | Mutation | Outcome | Can a test tell it from the code? |
| - | --------- | -------- | ------- | --------------------------------- |
| W1 | `capture.py:42` | the timer taken out | ✅ Killed (above) | Yes: OVL-121 |
| W6 | `capture.py:41-42` | the timer started by the first frame, not beside it | ✅ Killed - the test of OVL-121: `Timed out after 30s.` | Yes: OVL-121 |
| W3 | `capture.py:122` | the bound made useless: 250 seconds for 250ms (`* 1000 * 1000`) | ✅ Killed - the test of OVL-121: `Timed out after 30s.` | Yes: OVL-121 |
| W2 | `capture.py:41` | the frames taken out: the timer alone, 250ms before every screenshot | Survived - both tests pass; the test of OVL-120 takes 44s for 21s | Not by an outcome the spec defines. Every Finding is the same; a call takes about 2s to 7s longer (10 to 32 screenshots). Only a test of wall-clock time could hold it |
| W8 | `capture.py:41` | one frame, not two (P2 of the fourth pass, on the line this round rewrote) | Survived - both tests pass | No, as the fourth pass found: no call measured differs |
| W9 | `config.py:22` | the bound ten times as long, 2.5s | Survived - both tests pass; the test of OVL-121 takes 26s | Not by an outcome. The test of OVL-121 fails only from about 3s on (ten screenshots against the 30s of a call). The value is held by its comment in `config.py`, not by a test |
| W10 | `config.py:22` | the bound four times as long, 1s | Survived - both tests pass; the test of OVL-121 takes 11s | The same |
| W4 | `capture.py:122` | the bound not passed: `most` is undefined, a timer of 0ms that ends the wait before any frame | Survived - both tests pass in 8 runs of 8 (5 on a quiet machine, 3 with three browsers at work) | Not on any page known. Called 30 more times on `overlap-low.html`: 30 Findings. 78 calls, no miss. The wait then lasts 3.5ms (median of 36) for 27ms |
| W5 | `capture.py:122` | the bound passed in seconds: a timer of 0.25ms | Survived - the same 8 runs of 8, and 30 Findings in 30 calls | The same |
| W7 | `capture.py:122` | no wait at all (P1 of the fourth pass, on the line this round rewrote) | Killed on 3 runs of 13 - the test of OVL-120: `[] == [('#low', 'major', 50, '#low-cover')]`. 3 of 10 on a quiet machine, 0 of 3 with three browsers at work | Yes, by sample: this is the mutant the test of OVL-120 is for, and the criterion is six calls of a fault of timing. See the next section |

**Sensor depth**: the list of the stopping rule, 21 mutants: 9 named by the fourth report, 2 more named by a task, 10 of the code the round changed (W1 is in both of the last two groups and is counted once, with the round's)
**Sensor outcome**: (a) 9/9 killed; (c) 3/3 as their tasks say; (b) 3 killed by a test that fails on every run, 1 killed by the sample that is its test (3 runs of 13), 6 that no test of an outcome the spec defines can tell from the code. No mutant of the list is alive that such a test could hold - ✅

**Judgement on the six and the one.** The stopping rule fails the feature on a mutant "that survives and that a test through the MCP boundary could hold". W2, W9 and W10 return the Findings of the code on every page and differ in seconds: the spec has no criterion on the time of a call, and a test of wall-clock time is not one this suite has or should grow for a constant. W4, W5 and W8 return the Findings of the code on the one page built to show the fault, in every call made. W7 is told apart by the test the spec defines for it, on some runs: no page shows this fault on every call (F17 and the fourth pass say so, and this pass confirms it), so no test can hold it on every run, and how many calls the sample should be is the spec's to say (OVL-120 says six). None of the seven is a behaviour a fixture row can pin. They are recorded as residuals 1, 3 and 4.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, apart from this report and the lessons store written afterwards. `HEAD` is `c14cd2f` on `feat/overlap` both times and `git worktree list` shows the main tree alone. `git stash` was not used. Every mutant lived in its own copy under the session's temp directory; pytest ran with `-p no:cacheprovider` and without bytecode files. While the gate ran, one mutant at a time ran beside it; afterwards up to three browsers were at work, and the measurements of time and of the fault were taken with one.

---

## The wait before a screenshot (AD-007, F17 and F18)

The fourth pass asked for a bound and the maintainer had it added. This is what this pass measured of the wait as it now is. Probes ran through the in-memory MCP client, as `tests/helpers.py` does.

| Question | Evidence of this pass | Answer |
| -------- | --------------------- | ------ |
| Is a page that never calls a frame back measured? | The gate, and probe `no-frames` (a twin of the fixture): `(#t, major, 50, #t-cover)` in 3.8s to 4.2s; `inspect_element` answers too | Yes. OVL-121 holds |
| Is the bound 250ms? | Ten waits of one call on `overlap-no-frames.html`: 254ms to 268ms each | Yes |
| What do the two frames take? | 192 waits on four fixtures: median 24ms to 29ms per page, 50ms at most. A call makes 10 waits on the bug fixture, 12 on `overlap-low.html`, 32 on the bounds fixture | About 30ms, as the spec and AD-007 say: 0.3s to 0.9s of a call |
| Is the fault still there without the wait? | `detect_visual_bugs` called 30 times in a row on `overlap-low.html` with the wait taken out (W7), one browser at work: 23 calls return the Finding of `#low`, 7 return `[]` | Yes: about one call in four here today. The fourth pass had two in three, AD-007 six in ten |
| Does the wait end it? | The same 30 calls on the code as committed: 30 Findings. With every run of the test of OVL-120 in which the wait was the code's (the gate, the control, and W1, W3, W6, W9 and W10, which leave it whole on that page): 72 calls, 72 Findings | Yes, as far as a sample can say |
| Does the test hold the wait? | W7 against the test of OVL-120: failed on 3 of 10 runs on a quiet machine and on 0 of 3 with three browsers at work. The fourth pass: 5 of 5. F17's "Done when": "fails in most runs" | Less than was measured before. At one miss in four, six calls all hit about once in five runs; the runs of this pass hit more often than that, and under load the fault did not show at all in 18 calls. A removed wait would turn the suite red on some runs and leave it green on most |
| Are the frames what ends the fault? | W4 and W5 end the wait after a timer of 0ms, before any frame: 78 calls each, no miss, at 3.5ms per wait. W8, one frame: no miss | Not shown. Something as small as one turn of the page's task queue gave the same result as two frames on every call made. AD-007 lists what was tried and dropped; this is not on the list |
| Does the bound hold on every page? | Probe `dead-timers`: `setTimeout` and `requestAnimationFrame` both replaced by functions that never call back. `Timed out after 30s.` from both tools; measured in 3.2s with the wait taken out | No: spec-precision gap 1 |

**Judgement.** F18 does what Fix 6 of the fourth report and the maintainer asked: the probe of that report returns its Finding and a test holds it. The code is right on every call this pass made of it. What the tests hold of the wait is thinner than the records say: that some wait is there, on a share of runs; nothing of the two frames; the bound on a page that leaves `setTimeout` alone. That is the nature of a fix for a fault of timing, and the stopping rule does not count it against the feature. It is the first thing to look at if this code is touched again, and the reason residuals 1 to 3 propose an issue each.

Not verified by anyone: the branch was never pushed, so neither the timing of this fault nor the system font of `overlap-font.html` has met the CI's Linux.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

The diff of this round under `src/` is 11 lines in `capture.py` and 6 in `config.py`.

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ one more statement in the page expression, one argument at its call, one constant. No option, no abstraction |
| Surgical changes | ✅ nothing around the wait was touched; the page script, the Check and `covered.py` are unchanged since the fourth pass |
| No scope creep | ✅ the change is Fix 6 of the fourth report, as the maintainer decided it; the row of Out of Scope now counts it |
| Matches patterns | ✅ the constant is in `config` with its source and its measurement (`src/squint_mcp/config.py:18-22`), as every other; the comment on the expression says why the timer is there |
| Spec-anchored outcome check (asserted values match spec) | ✅ for the 131 criteria due now |
| Per-layer Coverage Expectation met | ✅ every criterion has its assertion; each of the nine behaviours the fourth pass listed as gaps has one now |
| Every test maps to a spec requirement - no unclaimed tests | ✅ the nine new tests map to OVL-121 to OVL-132 |
| Documented guidelines followed: `CONTRIBUTING.md` and `docs/SPEC.md`, Testing Decisions (one seam, real Chromium, no unit test of a helper) | ✅ every new test calls a tool through the in-memory client |

Observations, not gaps:

- The timer of `_PAINTED` is never cleared: when the frames win, it fires later and calls a function that does nothing by then. Harmless; at most one pending timer per screenshot.
- `src/squint_mcp/capture.py:36-38` says "the timer ends the wait then". It does when the page has left `setTimeout` alone (gap 1).
- The observations of the fourth report on `_is_transparent`, on a `url()` filter, on a text painted by its stroke alone and on a text of a very low alpha stand as written there: none of that code changed.

---

## Edge Cases

- [x] OVL-68: the Findings of 1440 × 900 are also those of 390 × 844 (`tests/test_overlap.py:186-196`)
- [x] OVL-69: an element behind the clipped part of a text does not cover it (`tests/test_overlap.py:886-887`)
- [x] OVL-120: a covered text low on a page of layers is reported on six calls in a row (`tests/test_overlap.py:941-943`)
- [x] OVL-121: a page that never calls an animation frame back is measured (`tests/test_overlap.py:952-953`)

---

## Gate Check

- **Gate command**: `uv run pyright`, `uv run ruff check`, `uv run ruff format --check`, `uv run pytest`, each run by this Verifier with its own exit status recorded. pytest ran in the background with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`, so that the run wrote nothing in the tree
- **Gate outcome**: pyright exit 0 (0 errors, 0 warnings, 0 informations); ruff check exit 0 (All checks passed); ruff format --check exit 0 (104 files already formatted); pytest exit 0 - 368 passed, 0 failed, 0 skipped, in 1353.09s (with one mutant at a time running beside it)
- **Test count before feature**: 237
- **Test count after the fourth pass**: 359
- **Test count now**: 368
- **Delta**: +131 over the feature, all in `tests/test_overlap.py`; +9 in the fourth fix round
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed or weakened. `git diff a8feee6..HEAD -- tests/` adds 598 lines in seven files and removes none: six new fixtures and 109 lines of `tests/test_overlap.py` (six constants and nine tests). No fixture of an earlier pass or slice changed, and the only assertions of the earlier slices that changed since `eb9778b` are the four `Valid checks:` literals OVL-55 supersedes

---

## Residuals and proposed issues

No fix task of this feature. By the stopping rule what is found outside its list "is a residual or an issue and does not fail the feature". Ranked by how much a later change could walk into each.

### 1. The test of OVL-120 holds the wait on a minority of runs (W7)

- **What**: with the wait taken out the test failed on 3 of 10 runs on a quiet machine and on 0 of 3 under load, where the fourth pass measured 5 of 5 and F17 says "in most runs". The fault it stands for is real: 7 calls in 30 lose their Finding without the wait.
- **Why it is not a gap of this pass**: no page shows the fault on every call, so no test fails on every run; the criterion is a sample of six by its own words.
- **Proposed issue**: decide what the test is for. As a tripwire it works as it is. To hold the wait on most runs it needs more calls (at one miss in four, twelve calls fail about 96 runs in 100, at 3.5s a call), and it will still pass on a loaded machine. Record in AD-007 the rate measured today beside "six calls in ten".

### 2. The bound of the wait is a timer of the page's own world (spec-precision gap 1)

- **What**: a page that replaces `setTimeout` and `requestAnimationFrame` both by functions that never call back fails `detect_visual_bugs` and `inspect_element` with `Timed out after 30s.`; before F17 it was measured. A library that fakes the clock of a page can replace the two together.
- **Proposed issue**: bound the wait from the server's side, where no function of the page is asked (a timeout around the `evaluate` at `src/squint_mcp/capture.py:122`), with a fixture that replaces both functions. Until then, word `spec.md:97`, the colon clause of OVL-121 and the comment at `capture.py:36-38` for what the timer gives, or add a row to Out of Scope.
- **How likely**: rare on a production page; a page under test with a faked clock is the likely case. When it happens every tool fails on that page, with a clear error.

### 3. Whether the frames are needed (W4, W5, W8)

- **What**: a wait that ends on a timer of 0ms, before any frame, gave 78 Findings in 78 calls on the page built to show the fault, at 3.5ms a wait for 27ms. One frame did as well, as the fourth pass found.
- **Proposed issue**: measure it where it counts (the CI's Linux, and the clean fixture under the mutants F17 names) before changing anything. If it holds, a Capture gets back most of the "eighth to a fifth more time" AD-007 records. If a page is found that needs the frames, it is the fixture the two frames lack.

### 4. The value of the bound and the frames show only in time (W2, W9, W10)

- **What**: the bound at 1s or at 2.5s, and the wait as a timer alone, pass every test; a call gets seconds slower. The test of OVL-121 fails from a bound of about 3s on.
- **Proposed issue**: none needed. A note for a reviewer: `PAINT_WAIT_MAX_S` is held by its comment, not by a test.

### 5. One pixel past the cap (H1-)

- **What**: the step computed for one pixel less passes every test of the cap, the count and the steps (16 tests run), as F23 says of the cap fixture. The smallest page a fixture samples has 21,000 pixels of Hidden ink, so "20,001 pixels are sampled" is held by nothing.
- **Proposed issue**: a row of one more hidden pixel on the cap page (a cover one pixel wide over a text of `font-size: 10px`, as `#speck` has), if the bound is ever touched. It changes only which of two covers is named. The playbook already has this lesson (L-021, a case exactly at a threshold and one past it).

### 6. Records that are out of date

- AD-007 says a page that never calls a frame back costs "about 4s more"; it is 2.3s more, 3.9s in all. F18 says the call "takes about 5s".
- The Handoff of `.specs/STATE.md` describes the state before this round.

### 7. Outside this slice, carried from the fourth report

- A Content Security Policy that refuses inline styles: a page comes back clean from `overlap` and `low-contrast-real` (probed again: `spec.md:48` is right). `STATE.md` says it has no issue yet.
- A right-to-left page that scrolls sideways: every tool reads the wrong pixels (probed again: `spec.md:49` is right). No issue yet.
- The branch has never run on the CI's Linux.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| OVL-01 to OVL-66, OVL-68 to OVL-119 | Implemented | ✅ Verified |
| OVL-92, OVL-93, OVL-95 to OVL-97 | ⚠️ Verified as written in the fourth pass | ✅ Verified: OVL-122 to OVL-126 pin the rule beyond a filter of one function |
| OVL-105, OVL-106 | ⚠️ Verified as written in the fourth pass | ✅ Verified: OVL-127 and OVL-128 pin a descendant deeper than a child |
| OVL-109, OVL-110 | ⚠️ Verified as written in the fourth pass | ✅ Verified: OVL-129 and OVL-130 pin the other order of the two covers |
| OVL-120 | Implemented | ✅ Verified as a sample of six calls; residual 1 |
| OVL-121 | Implemented | ✅ Verified for the page it names; ⚠️ spec-precision gap 1 on its last clause |
| OVL-122 to OVL-132 | Implemented | ✅ Verified |
| OVL-67 | Pending | Due: the closing step of `tasks.md` follows this verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ✅ Ready, with seven residuals for the maintainer to read, the first two before the pull request

**Spec-anchored check**: 131/131 criteria due now match the spec outcome; OVL-67 is the closing step; 1 spec-precision gap
**Sensor**: the nine survivors of the fourth pass 9/9 killed; the mutants the tasks name 3/3 as the tasks say; of ten mutants of the round's code 3 killed on every run, 1 killed by its sample on 3 runs of 13, 6 that no test of an outcome the spec defines can tell from the code
**Gate**: 368 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: everything the earlier passes found working, and now, each with a fixture and a test that dies with its rule: a filter that lists functions of both kinds, a filter declared `!important`, a cover that hides by its `drop-shadow()`, a text blurred or twice faded below half, a badge or a menu item two elements down, the Coverer first or last of two covers with either of them raised, a text under a border, a page of exactly 20,000 hidden pixels, and a page that never calls an animation frame back.

**What could have failed and did not**: the nine survivors of the fourth pass (all killed, by values, on the first run), every claim of a "Done when" about a mutant, the reading of the twelve new criteria against their fixtures and against `inspect_element`, the rows this round wrote in the spec against six probe pages, the measurement of the bound and of the two frames, the test integrity check, and 72 calls on the page of the timing fault with the wait whole.

**Issues found**: none that fails the feature under the stopping rule. For the maintainer:

1. The test of OVL-120 fails without the wait on about a third of quiet runs and on none under load (residual 1).
2. The bound of the wait does not hold on a page that replaces `setTimeout` too (residual 2, spec-precision gap 1).
3. A timer of 0ms did as well as the two frames in 78 calls (residual 3).

**Lessons**: two candidates recorded through `lessons.py`, one per grounded signal: L-080 (spec-precision gap 1, the bound of a wait built from a function of the page) and L-081 (W7, the size of a test that samples a timing fault).

**Next steps**: the closing step of `tasks.md` (OVL-67: the roadmap, the spike and its `extend-exclude` removed, issue #18 through the pull request), which needs the maintainer's go-ahead for the push. Issues for residuals 1 to 3 and for the two limits of section 7. The Handoff of `.specs/STATE.md` brought up to date.
