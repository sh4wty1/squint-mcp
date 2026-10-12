# overlap Validation

**Date**: 2026-10-11
**Spec**: `.specs/features/overlap/spec.md` (OVL-01 to OVL-120)
**Diff range**: `eb9778b..a8feee6` (35 commits, branch `feat/overlap`, base `8aa017c`); the third fix round is `b08856a..a8feee6` (nine commits)
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 4, after the third and last fix round of the loop

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

The third fix round did what it was asked, and more of it than the two before. The two places where the third pass found the code short of the spec are fixed: a covered text under a `filter` that changes colours is reported, and a glyph colour of alpha 0 is read in every notation. The twelve survivors of the third pass are all killed, each by the test written for it. The 29 new criteria are faithful statements of the Terms and the Assumptions. All 119 criteria due now have an assertion on the outcome the spec defines, the gate is green with 359 tests, and on sixteen probe pages of this pass the unmutated code gives the outcome the spec defines everywhere inside the scope of this slice. That last point is new.

The verdict is FAIL on one count: the spec's third success criterion, "the discrimination sensor leaves no surviving mutant".

1. **Nine new mutants survive, five of them in the thirteen lines this round added to the cover script.** Of 27 mutants no pass had tried, 17 were killed and 10 survived. One of the ten (one animation frame instead of two) no test can tell from the code. The other nine each give, on a probe page called through the MCP boundary, a result the spec excludes, and all 272 tests that reach the code pass. The filter fix is held for a `filter` of one function: a list of functions, `blur()`, `drop-shadow()` and a filter declared `!important` have no fixture. The other four are a third dimension of rules the round pinned from two sides.
2. **F17 (AD-007) is sound and should stay, with one thing to settle.** The fault it fixes is real: without the wait 20 of 30 calls on `overlap-low.html` returned no Finding here. But the wait runs a function of the page: a page that never calls an animation frame back now times out, in every tool, where it used to be measured. And the spec row that counts the changes reaching every Capture still says two.

Nothing found in this pass is a wrong result of the code on a page inside the scope of this slice. Two things outside it are for the maintainer to know: a right-to-left page that scrolls sideways is read from the wrong pixels by every tool (older than this slice, and in no row of this spec), and a page whose Content Security Policy refuses inline styles comes back clean from `overlap` and from `low-contrast-real` (the row of Out of Scope said "not verified"; it is verified now).

**How much of the code's behaviour is held by tests.** Over the four passes 118 different mutants were written against the code this feature adds under `src/`. 4 are equivalent and 1 cannot be told apart by any test. Of the 113 others, 104 were killed when last run (33 of them in this pass, at `a8feee6`) and 9 are not. The rate of gaps among new mutants went from 11 of 21 and 12 of 18 in the two passes before to 9 of 27 now.

**How serious the gaps are for a user of the tool.** Today, none: every survivor is a behaviour the code has right and no test holds. The risk is the next change to the thirteen lines of the filter fix or to `subtreeOf`: a slip there would lose every Finding under a filter that mixes kinds of functions, or overstate the share of every text with a nested badge, with all 359 tests green.

**Where this leaves the loop.** It is at its bound of three fix rounds, so the decision is the maintainer's. Each pass wrote fresh mutants and each found some alive: 11, 11, 12, 9. A sensor run at this depth by a reader who has not seen the tests will keep finding a few. The list has stopped being about how the Check measures and is now about the edges of one new regular expression and one tree walk. The Fix Plans give the nine fixture rows that would close it and the two decisions on F17.

OVL-67 (the roadmap) is a closing step that follows a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `O` = `tests/test_overlap.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Earlier passes

The three earlier reports are in git in full, at `aef0799`, `0a25cca` and `26d084f`. This pass used the third as a map of what had been tried and re-derived the rest.

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

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T13 | ✅ Done | `89385b0` to `cb8d81b`, as in the earlier passes |
| F1 to F8: the fixes of the first two passes | ✅ Done | `7c32a5b` to `a11b13e` |
| F9: the ink of text under a filter that changes colours | ✅ Done | `82bbaed`, `src/squint_mcp/js/covered_text.js` |
| F10: the alpha of a glyph colour in every notation | ✅ Done | `c018ab2`, `src/squint_mcp/checks/overlap.py` |
| F11: a font with anti-aliased edges | ✅ Done | `b71e582` |
| F12: what is inside a text, the order of two texts, `open`, a raised cover, the styles of a Finding | ✅ Done | `ecdf0e5` |
| F17: the page paints before a screenshot | ✅ Done | `51ff006`, `src/squint_mcp/capture.py`; not planned, see "F17 and AD-007" |
| F13: a page wider than its viewport | ✅ Done | `3711dee` |
| F14: where an `info` Finding stands | ✅ Done | `e4fed09` |
| F15: which Hidden ink counts and how the step grows | ✅ Done | `70f926d` |
| F16: the limits the design accepts, in the spec | ✅ Done | `a8feee6` |

Every box of `tasks.md` is ticked (182 `- [x]`, no open box). None is blocked or partial. `git status --porcelain` of the real tree was empty when this pass began.

The "Done when" claims of F9 to F17 about mutants were checked, not copied: each mutant named there was written again and run (sensor section), and each claim holds. Three sentences of `tasks.md` do not match what was committed, none of them a claim about behaviour: F9 says the text of OVL-93 has `filter: invert(1)` (the fixture and the spec have `hue-rotate(180deg)`), F13 says the wide page is 2700px high (it is 2000px, as the spec says), and F17 says its test calls the tool three times (it calls it six times, as the spec says). The Handoff of `.specs/STATE.md` still says the third fix round has not started.

---

## Spec-Anchored Acceptance Criteria

Every line number below was located again in this pass, in `tests/test_overlap.py` at `a8feee6` (1247 lines, 108 test functions, 122 tests with their parameters). The twelve new fixtures and the two that grew were read against their criteria: positions, sizes, roles, `z-index` values, document order and the pixel counts in their comments are the ones the criteria state (17,200 pixels in the reach fixture, 65,180 in the bounds one, 19,000 + 1520 and 19,000 + 2000 in the two count fixtures, 49,000 and 81,000 in the two step fixtures, worked out again below).

### P1: Report text that another element covers

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-01 one Finding per covered element | exactly one Finding each | `tests/test_overlap.py:69-74` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements, `finding["check"] == "overlap"`, `len(findings) == 4`; `O:468-512` pins the sorted list of the 39 selectors of the bounds fixture, so a second Finding on one element fails | ✅ PASS |
| OVL-02 the four Findings of the bug fixture, in order | `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)`, `(#collision, minor, 20, #stray)` | `O:80-87` - `covered(findings) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-03 summary line | first block, `Found 4 findings in 1 viewport: 2 major, 2 minor.` | `O:93-94` - `texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."` | ✅ PASS |
| OVL-04 same call, same content | equal structured content | `O:98` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| OVL-05 text under the text of another element | one Finding, `hiddenPercent` 20 | `O:104-105` - `finding_on` unpacks exactly one; `["hiddenPercent"] == 20` | ✅ PASS |
| OVL-06 the text on top | no Finding for `#stray` | `O:109-110` - `await findings_on(client, BUG, "#stray", findings) == []` | ✅ PASS |
| OVL-07, OVL-08, OVL-09 `#left`, `#top`, `#bottom`, exactly 10% | one Finding each, 10 | `O:515-520` - parametrized over the three, `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-10 `#three-lines`, middle box | one Finding, 10 | `O:524-525` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-11 `#split`, second text node | one Finding, 10 | `O:529-530` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-12 `#veil-55` | one Finding, 100, `major` | `O:534-536` - `["hiddenPercent"] == 100`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-13 text and cover in one shadow tree | 50, `coveredBy` `[data-testid="shadow-cover"]` | `O:542-546` - `finding["evidence"]["measured"] == {"hiddenPercent": 50, "coveredBy": SHADOW_COVER}` | ✅ PASS |
| OVL-14 `#narrow`, one viewport only | one Finding at 390 × 844, none at 1440 × 900 | `O:116-121` - `... DESKTOP) == []`, `(finding,) = ... MOBILE)`, `finding["viewport"] == MOBILE` | ✅ PASS |
| OVL-15 `#in-dialog` | one Finding, `major` | `O:552` - `(await bounds(client, "#in-dialog"))["severity"] == "major"` | ✅ PASS |
| OVL-16 `#in-fixed` | one Finding, `major` | `O:558` - `(await bounds(client, "#in-fixed"))["severity"] == "major"` | ✅ PASS |
| OVL-17 `low-contrast-bounds.html` | exactly one Finding, `#covered`, 100, `major` | `O:859-863` - `(finding,) = ...["findings"]`, `finding["selector"] == "#covered"`, `["hiddenPercent"] == 100`, `["severity"] == "major"` | ✅ PASS |
| OVL-18 `low-contrast-reach.html` | exactly one Finding, `#veiled-most`, 100 | `O:869-872` - `(finding,) = ...`, `finding["selector"] == "#veiled-most"`, `["hiddenPercent"] == 100` | ✅ PASS |
| OVL-71 a list of several roles | one Finding, 50, `#role-list`, `major` | `O:671-676` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#role-list"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-75 `#opacity-60` | one Finding, 50 | `O:683-684` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-76 two measured texts over each other | `#under-label` 50 by `#label`; `#label` 50 by `#label-cover` | `O:693-702` - both `["measured"] == {...}` dicts, the values of the spec | ✅ PASS |
| OVL-78 `#speck`, all its Hidden ink off the sample | one Finding, 10, `minor`, `#speck-cover` | `O:994-999` - `["measured"] == {"hiddenPercent": 10, "coveredBy": "#speck-cover"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-80 four texts stacked in one place | four Findings, all `major`: three at 80 by `#stack-3`, `#stack-3` at 25 by `#stack-cover` | `O:711-722` - `covered(stack) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-81 `#shifted`, a column of its own | one Finding, 10, `minor` | `O:730` - `share_and_severity(await bounds(client, "#shifted")) == (10, "minor")` | ✅ PASS |
| OVL-82 the box of a tag whose glyphs stand beside the text | `#under-tag` 50 by `#tag`; `#tag` 50 by `#tag-cover` | `O:739-748` - both `["measured"] == {...}` dicts | ✅ PASS |
| OVL-83 `#around`, own text around a child with text | one Finding, 10, `minor` | `O:756` - `share_and_severity(await bounds(client, "#around")) == (10, "minor")` | ✅ PASS |
| OVL-87 `#translucent`, glyphs of alpha 0.5 | one Finding, 50 | `O:764-765` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-89 `#filled`, transparent `color`, opaque fill | one Finding, 50 | `O:773-774` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-90 a Silent layer that is not painted | one Finding, 50, `#plain-cover`, `major` | `O:783-788` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#plain-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-86 a page scrolled when it is captured | exactly one Finding, `#far`, 50, `major`, `#far-cover` | `O:958-959` - `covered(findings) == [("#far", "major", 50, "#far-cover")]` | ✅ PASS |
| OVL-92 `#in-grey`, in a row of `filter: grayscale(1)` | one Finding, 50, `#in-grey-cover`, `major` | `O:791-804` (case `#in-grey`) - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#in-grey-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-93 `#own-filter`, `filter: hue-rotate(180deg)` of its own | one Finding, 50, `#own-filter-cover`, `major` | `O:791-804` (case `#own-filter`) - the same two assertions | ✅ PASS |
| OVL-94 `#held`, a cover held by a `filter` alone | one Finding, 50, `#held-cover`, `major` | `O:813-818` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#held-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-95 `filter: invert(1)` on the root | exactly one Finding, `#inverted`, 50, `major`, `#inverted-cover` | `O:825-826` - `covered(findings) == [("#inverted", "major", 50, "#inverted-cover")]` | ✅ PASS |
| OVL-100 `#opaque-oklch`, `#translucent-oklch` | one Finding each, 50 | `O:829-840` - parametrized over the two, `["measured"] == {"hiddenPercent": 50, "coveredBy": f"{selector}-cover"}` | ✅ PASS |
| OVL-101 `#font-whole` | one Finding, 100, `major`, `#font-whole-cover` | `O:1102-1107` - `covered(findings) == [("#font-whole", "major", 100, "#font-whole-cover"), ...]`, the first of three tuples | ✅ PASS |
| OVL-102 `#font-lines` | one Finding, 50, `major`, `#font-lines-cover` | `O:1102-1107` - the second tuple, `("#font-lines", "major", 50, "#font-lines-cover")` | ✅ PASS |
| OVL-103 `#font-veil-55` | one Finding, 100, `major`, `#font-veil-55-cover` | `O:1102-1107` - the third tuple, `("#font-veil-55", "major", 100, "#font-veil-55-cover")` | ✅ PASS |
| OVL-106 `#child-first`, `#child-last` | one Finding each, 16, `minor`, its cover | `O:1146-1159` - parametrized over the two, `["measured"] == {"hiddenPercent": 16, "coveredBy": f"{selector}-cover"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-107 a tag before the text it covers | `#under-tag-first` 50 by `#tag-first`; `#tag-first` 50 by `#tag-first-cover` | `O:1168-1177` - both `["measured"] == {...}` dicts | ✅ PASS |
| OVL-108 an open `details` | one Finding, 50, `#open-details`, `major` | `O:1186-1191` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#open-details"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-111 `#under-after`, `#under-before` | one Finding each, 50, `major`, the owner of the pseudo-element | `O:1221-1234` - parametrized over the two, `["measured"] == {"hiddenPercent": 50, "coveredBy": f"#{pseudo}-owner"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-114 a page scrolled sideways when it is captured | exactly one Finding, `#far`, 50, `major`, `#far-cover` | `O:983-986` - `covered(findings) == [("#far", "major", 50, "#far-cover")]` | ✅ PASS |

### P1: Stay silent on overlaps that are meant

`clean(client, selector)` (`O:219-225`) returns the share of the element's box painted in the colour of the covers, read through `inspect_element`, and the Findings on that box. The first value proves the fixture really paints the cover over the text (or, for OVL-91, OVL-96 and OVL-98, that it does not); the second is the criterion.

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-19 the clean fixture, all Checks | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `O:211-216` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| OVL-20 `#stretched` | no Finding | `O:233` - `await clean(client, "#stretched") == (0, [])` | ✅ PASS |
| OVL-21 `#under-faded` | no Finding | `O:238` - `== (0, [])` | ✅ PASS |
| OVL-22 `#veil-45` | no Finding | `O:245-246` - `painted(...)["#737373"] == 0.6`, `await clean(client, "#veil-45") == (0, [])` | ✅ PASS |
| OVL-23 the five roles | no Finding for each | `O:249-256` - parametrized over `menu`, `listbox`, `tooltip`, `dialog`, `alertdialog`: `await clean(client, f"#under-{role}") == (0.5, [])` | ✅ PASS |
| OVL-24 `dialog[open]` | no Finding | `O:263` - `== (0.5, [])` | ✅ PASS |
| OVL-25 open popover, `position: absolute` | no Finding | `O:269` - `== (0.5, [])` | ✅ PASS |
| OVL-26 `position: fixed` | no Finding | `O:274` - `== (0.5, [])` | ✅ PASS |
| OVL-27 `position: sticky` | no Finding | `O:279` - `== (0.5, [])` | ✅ PASS |
| OVL-28 descendant of a `menu` | no Finding | `O:287` - `== (0.5, [])` | ✅ PASS |
| OVL-29 static child of a fixed element | no Finding | `O:295` - `== (0.5, [])` | ✅ PASS |
| OVL-30 shadow tree of a `menu` host | no Finding | `O:566-569` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []` | ✅ PASS |
| OVL-31 `#nick`, 9.5% along the width | no Finding | `O:302` - `== (0.095, [])` | ✅ PASS |
| OVL-32 `#skim`, 5% along the height | no Finding | `O:310` - `== (0.2, [])` | ✅ PASS |
| OVL-33 `#parent-text`, under its own child | no Finding | `O:315` - `== (0.5, [])` | ✅ PASS |
| OVL-34 `#under-ghost`, `pointer-events: none` | no Finding | `O:323` - `== (0.5, [])` | ✅ PASS |
| OVL-35 `#caption` over `#picture` | no Finding for either | `O:332-335` - `painted(...)["#000000"] == 0.24`, both `findings_on(...) == []` | ✅ PASS |
| OVL-36 `#badge` on `#inbox` | no Finding | `O:343` - `== (0.0533, [])` | ✅ PASS |
| OVL-37 `visibility: hidden` | no Finding | `O:348` - `== (0.5, [])` | ✅ PASS |
| OVL-38 `color: transparent` | no Finding | `O:356` - `== (0.5, [])` | ✅ PASS. The rule now holds off its fixture too: 18 notations of an alpha of 0 probed, none reported ("Probes of the unmutated code") |
| OVL-39 `opacity: 0` | no Finding | `O:361` - `== (0.5, [])` | ✅ PASS |
| OVL-70 a role with spaces and a capital | no Finding | `O:369` - `await clean(client, "#under-spaced-role") == (0.5, [])` | ✅ PASS |
| OVL-72 under what an ancestor paints | no Finding | `O:377` - `await clean(client, "#under-own-row") == (0.5, [])` | ✅ PASS |
| OVL-73 hit testing gives a descendant | no Finding | `O:386` - `await clean(client, "#own-link-text") == (0.5, [])` | ✅ PASS |
| OVL-74 `#opacity-40` | no Finding | `O:393` - `await clean(client, "#opacity-40") == (0.5, [])` | ✅ PASS |
| OVL-88 opaque `color`, transparent fill | no Finding | `O:401` - `await clean(client, "#transparent-fill") == (0.5, [])` | ✅ PASS |
| OVL-91 closed menus | no Finding, and nothing painted over the text | `O:404-410` - parametrized over `#under-removed-menu` and `#under-hidden-menu`: `await clean(client, selector) == (0, [])` | ✅ PASS |
| OVL-96 a cover faded out by `filter: opacity(0)` | no Finding | `O:419` - `await clean(client, "#under-filter-faded") == (0, [])` | ✅ PASS |
| OVL-97 a text faded out by `filter: opacity(0)` | no Finding | `O:426` - `await clean(client, "#filter-faded-text") == (0.5, [])` | ✅ PASS |
| OVL-98 a text above the layer a `filter` makes | no Finding | `O:436-438` - `painted(inspected)["#c8c8c8"] == 0.1667` (the cover shows around the glyphs, under them), `await clean(client, "#above-filter-layer") == (0, [])` | ✅ PASS |
| OVL-99 an alpha of 0 outside `rgb()` | no Finding for each of the three | `O:441-450` - parametrized over `#transparent-oklch`, `#transparent-mix`, `#transparent-none`: `await clean(client, selector) == (0.5, [])` | ✅ PASS |
| OVL-104 `#font-veil-45` | no Finding | `O:1117-1118` - `await findings_on(client, FONT, "#font-veil-45", findings) == []`; the list of `O:1103-1107` holds that the page has three Findings and no fourth | ✅ PASS |
| OVL-105 `#child-and-nick` | no Finding | `O:460` - `await clean(client, "#child-and-nick") == (0.45, [])` | ✅ PASS |

### P1: Severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-40 25% is `major`, 24.5% is `minor` | `#quarter` `major`, `#almost-quarter` `minor` | `O:575-579` - `quarter[...]["hiddenPercent"] == 25`, `quarter["severity"] == "major"`, `almost["severity"] == "minor"` | ✅ PASS |
| OVL-41 `#layered-half` | `minor` | `O:596` - `share_and_severity(...) == (50, "minor")` | ✅ PASS |
| OVL-42 `#layered-corner` | `info` | `O:602` - `== (10, "info")` | ✅ PASS |
| OVL-43 `#layer-ancestor` | `minor` | `O:608-610` - `["coveredBy"] == "#layer-cover"`, `== (50, "minor")` | ✅ PASS |
| OVL-44 `#shared-layer` | `major` | `O:616` - `== (50, "major")` | ✅ PASS |
| OVL-45 `#z-zero` | `major` | `O:620` - `== (50, "major")` | ✅ PASS |
| OVL-46 `#z-static` | `major` | `O:626-628` - `["coveredBy"] == "#z-static-next"`, `== (50, "major")` | ✅ PASS |
| OVL-109 only the cover that is not the Coverer is raised | 50, `#plain-large`, `major` | `O:1200-1205` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#plain-large"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-110 only the Coverer is raised | 50, `#raised-large`, `minor` | `O:1213-1218` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#raised-large"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-115 `major`, `minor`, `info` in one call | `(#c, major, 50, #c-cover)`, `(#b, minor, 10, #b-cover)`, `(#a, info, 10, #a-cover)`; `Found 3 findings in 1 viewport: 1 major, 1 minor, 1 info.` | `O:903-912` - `covered(result.structured_content["findings"]) == [...]`, the three tuples; `texts(result)[0] == "Found 3 findings in 1 viewport: 1 major, 1 minor, 1 info."` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-47 the Finding of `#half` | the literal of the spec | `O:127-144` - `findings[0] == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| OVL-48 message at 10% | `10% of the text is covered by another element` | `O:148-150` - `["hiddenPercent"] == 10`, `finding["message"] == "10% of the text is covered by another element"` | ✅ PASS |
| OVL-49 truncation | 24 for 24.5% | `O:584-586` - `["hiddenPercent"] == 24`, `finding["message"] == "24% of the text is covered by another element"` | ✅ PASS |
| OVL-50 `#mixed` | 20, `#mixed-card`, `minor` | `O:635-640` - `["measured"] == {"hiddenPercent": 20, "coveredBy": "#mixed-card"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-51 `#two-covers` | 60, `#large-cover` | `O:647-651` - `["measured"] == {"hiddenPercent": 60, "coveredBy": "#large-cover"}` | ✅ PASS |
| OVL-52 `#tie` | 40, `#tie-first` | `O:659-663` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#tie-first"}` | ✅ PASS |
| OVL-53 both selectors work in `inspect_element` | `isError: false`, same `box` for `selector` | `O:846-853` - for the 4 Findings of the bug fixture and the 39 of the bounds fixture (`len(findings) == count`): `inspected["box"] == finding["box"]`, and `inspect` (`O:197`, `result.is_error is False`) on `coveredBy` | ✅ PASS |
| OVL-77 an element the scroll brings over a text | exactly one Finding, `#far`, 50, `#far-cover` | `O:945-950` - `(finding,) = ...["findings"]`, `finding["selector"] == "#far"`, `["measured"] == {"hiddenPercent": 50, "coveredBy": "#far-cover"}` | ✅ PASS |
| OVL-79 the Coverer of a sample | the fifteen tuples in order, `#striped` covered by `#solid-cover` | `O:1007-1016` - `covered(findings) == [...]` | ✅ PASS |
| OVL-84 the rows of a sample | `#row-striped`: 40, `major`, `#row-solid-cover` | `O:1025-1030` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#row-solid-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-85 a page under the cap | exactly one Finding, `#striped`, 25, `major`, `#stripes` | `O:1038-1039` - `covered(findings) == [("#striped", "major", 25, "#stripes")]` | ✅ PASS |
| OVL-112 `evidence.computed` of a positioned text | `{"position": "relative", "z-index": "1"}` for `#positioned`, `{"position": "relative", "z-index": "auto"}` for `#relative` | `O:1237-1247` - parametrized over the two, `finding["evidence"]["computed"] == {"position": "relative", "z-index": z_index}` | ✅ PASS |
| OVL-113 Hidden ink right of the viewport | `(#near, major, 50, #near-cover)`, `(#right, major, 50, #right-cover)`, `(#edge, major, 50, #edge-cover)`, `(#far, major, 50, #far-cover)` | `O:969-975` - `covered(findings) == [...]`, the four tuples | ✅ PASS |
| OVL-116 Hidden ink under a tenth does not count | `(#striped, major, 25, #stripes)` and nine fillers | `O:1061-1062` - `covered(findings) == striped("#stripes", 9)` | ✅ PASS |
| OVL-117 Hidden ink of a text without a Finding counts | `(#striped, major, 25, #solid-cover)` and nine fillers | `O:1071-1072` - `covered(findings) == striped("#solid-cover", 9)` | ✅ PASS |
| OVL-118 a step of 2 up to 80,000 pixels | `(#striped, major, 25, #solid-cover)` and 24 fillers | `O:1080-1081` - `covered(findings) == striped("#solid-cover", 24)` | ✅ PASS |
| OVL-119 a step of 3 from 80,000 pixels on | `(#striped, major, 25, #stripes)` and 40 fillers | `O:1090-1091` - `covered(findings) == striped("#stripes", 40)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-54 four Checks by default | `overlap` runs with the other three | `O:154-160` - the four `(selector, "overlap")` pairs on a call without `checks`; `O:887-894` - `low-contrast-real` and `overlap` in one default call; the default run of the other two is held by their own modules, which pass | ✅ PASS |
| OVL-55 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `tests/test_detect_visual_bugs.py:340-344` - the literal `in text`; the same list at `D:353`, `D:364` and `D:376` | ✅ PASS |
| OVL-56 the other three Checks on the bug fixture | `[]` | `O:164-165` - `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| OVL-57 order across Checks | `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)` | `O:887-894` - `{severity} == {"minor"}`, the four pairs in order | ✅ PASS |
| OVL-58 the description names `overlap` | names it and says what it reports | `O:169-174` - `` "`overlap` (text another element is painted over" in " ".join(tool.description.split()) `` | ✅ PASS |
| OVL-59 earlier tests unchanged | pass, only the four literals differ | by reading: `git diff --name-status 8aa017c..HEAD -- tests` lists the overlap fixtures, the new `tests/test_overlap.py` and `tests/test_detect_visual_bugs.py`, whose diff is the four `Valid checks:` literals (now at `D:342`, `D:353`, `D:364`, `D:376`) and nothing else; the gate passes | ✅ PASS |
| OVL-60 a hundred covered texts | `isError: false`, 100 Findings | `O:916-924` - `result.is_error is False`, `len(findings) == 100`, and the 100 tuples `(#text-n, major, 50, #cover-n)` | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| Criterion | Evidence | Result |
| --------- | -------- | ------ |
| OVL-61 one module, one function, registered | `src/squint_mcp/checks/overlap.py:88` - `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:23` - `"overlap": overlap.check` | ✅ PASS |
| OVL-62 no `playwright` in the Checks or in `vision.py` | `grep -rn playwright src/squint_mcp/checks src/squint_mcp/vision.py src/squint_mcp/covered.py` finds nothing (exit 1) | ✅ PASS |
| OVL-63 thresholds and roles in `config`, each cited | `src/squint_mcp/config.py:129` `OVERLAP_MIN_HIDDEN_PERCENT = 10` ("Squint default", with the reason, `:126-128`); `:133` `OVERLAP_MAJOR_HIDDEN_PERCENT = 25` ("Squint default", `:131-132`); `:138` `SILENT_LAYER_ROLES` ("WAI-ARIA 1.2", `:135-137`) | ✅ PASS |
| OVL-64 no literal of them in the Check | `src/squint_mcp/checks/overlap.py:49` and `:62` read both thresholds from `config`; no role name appears in the file. The numbers left are the `* 100` of a percentage (`:49`, `:62`, `:69`) and `== 0` for alpha and ink (`:34`, `:43`) | ✅ PASS |
| OVL-65 CHANGELOG | `CHANGELOG.md:12`, under `## [Unreleased]`: the Check, 10% and 25%, one level lower under a raised layer, what is not reported (declared layers, `fixed` and `sticky`, covers that paint nothing) and, new in this round, the known limits of F16 | ✅ PASS |
| OVL-66 README | `README.md:45` - "`detect_visual_bugs` runs four Checks: ... and `overlap` (...)" | ✅ PASS |
| OVL-67 roadmap `concluída` | Pending by design: a closing step after a PASS. `docs/ROADMAP.md:110` says `pendente`, which is right today | ⏳ Pending the verdict |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-68 two viewports | each Finding of the first has one in the second | `O:180-190` - `len(desktop) == 4`, `desktop <= mobile` over `(selector, check)` | ✅ PASS |
| OVL-69 `text-clipped-clean.html` | `[]` | `O:880-881` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |
| OVL-120 a covered text low on a page of layers, six calls in a row | every call: exactly one Finding, `#low`, 50, `major`, `#low-cover` | `O:935-937` - `for _ in range(6): ... assert covered(findings) == [("#low", "major", 50, "#low-cover")]` | ✅ PASS. The criterion is about a timing fault, so its test is a sample of six calls and not a proof: see "F17 and AD-007" |

**Status**: 119 of 119 criteria due now have an assertion on the outcome the spec defines, and every one passes; OVL-67 waits for the verdict. No criterion fails off its fixture inside the scope of this slice: the two rules the third pass found broken (a `filter` that changes colours, an alpha of 0 outside `rgb()`) now hold on every probe page of this pass. ⚠️ 2 spec-precision gaps flagged (below). ❌ Gaps present in the sensor (below).

### The 29 new criteria, read critically

Each was checked for two things: that it states a rule the Terms or the Assumptions hold, and that its fixture makes the outcome depend on that rule. The geometry of each was worked out again from the fixture.

| Criterion | The rule it states | Its fixture | Verdict |
| --------- | ------------------ | ----------- | ------- |
| OVL-92, OVL-93, OVL-95 | Assumptions, "A `filter`": ink is measured with the functions that change colours left out | A row of `grayscale(1)` around the text, `hue-rotate(180deg)` on the text, `invert(1)` on the root; each text half under an opaque cover | Faithful. All three filters are one function. A list of functions, which is what the row of the Assumptions is about, is in no fixture: mutants F6 and F8 |
| OVL-94 | The same row: "an element keeps a `filter` while it is measured, so it goes on holding what is positioned inside it" | `#holder`, `position: static` with `filter: sepia(1)`, is the containing block of `#held-cover` | Faithful. With the filter set to `none` the cover leaves the text (mutant F2: no Finding) |
| OVL-96, OVL-97 | The same row: `opacity()` is applied | A cover and a text of `filter: opacity(0)` | Faithful. `opacity()` is the only one of the three kept functions with a fixture: `blur()` and `drop-shadow()` have none (mutants F4 and F5) |
| OVL-98 | The same row: "being painted as one layer" | `#layered-cover`, `z-index: 5` inside `#filter-layer` (`invert(1)`), under a text of `z-index: 1`. The test first asserts that the cover is painted under the glyphs (1000 of the 6000 pixels of the box in its inverted grey) | Faithful |
| OVL-99, OVL-100 | Assumptions, "Text hidden on purpose": the alpha in every notation | `oklch()` with an alpha of 0, of `none`, of 0.5 and without one; a `color-mix()` that computes to `color(srgb 0 0 0 / 0)` | Faithful, on both sides. The code has one rule for every notation, so there is no branch per notation to leave out |
| OVL-101 to OVL-104 | Terms, "Seen" and "Text ink": the bound is relative to the pixel | The system `sans-serif` font at 16px; every share is of whole glyphs | Faithful, and independent of the platform's pixels: under a veil of 0.55 every pixel of Text ink (128 or more of 255) shows 0.45 of its ink, under one of 0.45 it shows 0.55. Not run on the CI's Linux: the branch was never pushed |
| OVL-105, OVL-106 | Terms, "Text ink": "when nothing outside the element is painted over it" | A child over 80px of the text, at its start and at its end; an Other element over 10px (200 of 2400 pixels, 8.3%) and over 20px (400 of 2400, 16.6%) | Faithful, both sides of the threshold and both ends. The child is a direct child in every case: a deeper descendant is in no fixture (mutant U1) |
| OVL-107 | Terms, "Text ink", with the tag before the text in the document | The row of OVL-82 in the other order | Faithful |
| OVL-108 | Terms, "Silent layer": a `dialog` element with the `open` attribute | A `details` element with `open`, positioned over half of the text | Faithful |
| OVL-109, OVL-110 | Assumptions, "Several elements cover one text": the Raised-layer rule reads the Coverer | A raised cover over 20px and a plain one over 80px, and the reverse | Faithful. In both the Coverer is the second of the two covers in the document: mutant R1 |
| OVL-111 | Out of Scope, the row for a pseudo-element: reported when no element that shows it is measured | `::after` and `::before` of an owner whose two glyphs are all seen | Faithful |
| OVL-112 | Assumptions, "`evidence.computed`" | A covered text of `position: relative` with `z-index: 1` and with none | Faithful |
| OVL-113, OVL-114 | Terms, "Coverer": "with the page scrolled so that the point is in the viewport" | A page 3000px wide and 2000px high: a text right of the viewport, one where the page cannot scroll a whole viewport further (2880px to 2980px, scroll limit 1560px), one right and below, a `fixed` bar that a scroll of 1440px brings over the second; and a page scrolled 1500px sideways while it loads | Faithful. The clamp at the end of the page is held on both axes: sideways by `#edge`, down by `#low` of OVL-120 (mutants S1 and S2) |
| OVL-115 | Assumptions, "Order of Findings"; `info` is first used here | Three texts that stand in the document from `info` to `major` | Faithful |
| OVL-116, OVL-117 | Terms, "Coverer": which Hidden ink counts towards the 20,000 | 19,000 + 1520 pixels (four texts at 9.5%, each with a menu over its first half so that it is measured) and 19,000 + 2000 (a transparent text half covered) | Faithful. 1000 + 9 × 2000 = 19,000; 4 × 380 = 1520 |
| OVL-118, OVL-119 | Terms, "Coverer": n is the smallest whole number for which the pixels divided by n × n are at most 20,000 | 49,000 pixels (n = 2: 12,250) and 81,000 (n = 2 gives 20,250, n = 3 gives 9000) | Faithful. The stripes are on the odd columns 41 to 99: at n = 3 they are found on 45, 51, ..., 99 (10 columns) and the solid cover on 222 to 237 (6). The bound itself, exactly 20,000 pixels, is in no fixture (mutant H1) |
| OVL-120 | Assumptions, "A screenshot that shows a part of the page unpainted" | A page 1850px high with 36 rows that are layers of their own and one covered text at its foot; six calls | Faithful as a sample. See "F17 and AD-007" |

### The Out of Scope rows of this round against the code

| Row | Probe | What the code does | Agrees? |
| --- | ----- | ------------------ | ------- |
| A pseudo-element painted outside the box of its element, when an element that shows it is itself measured | `pp-pseudo`: the owner half covered (`#b-under`); the pseudo-element painted by a child without text of an element that is half covered (`#d-under`); the owner all seen with a glyph of a third text in its line (`#f-under`); the pseudo-element inside the box of its owner, which is half covered (`#g-under`) | No Finding for `#b-under`, `#d-under` and `#f-under`; `(#g-under, major, 50, #g-owner)` | ✅ The reworded row says exactly this: spec-precision gap 1 of the third pass is closed |
| Text on an element with `mix-blend-mode` | `pf-filters`, `#f-blend` (`difference`) and `#f-blend-mult` (`multiply`), each half covered | No Finding under `difference`; `(#f-blend-mult, major, 50, ...)` under `multiply` | ✅ |
| A cover with a `backdrop-filter` that changes colours | `pf-filters`, `#f-backdrop`: a clear cover of `backdrop-filter: invert(1)` over half of a text | `(#f-backdrop, major, 50, #f-backdrop-cover)` | ✅ reported, as the row says |
| A page whose Content Security Policy refuses inline styles ("Not verified") | `pcsp`: a covered text and a grey text of contrast 2.95, styled from a file, under `style-src file:`; the same page without the policy as a control | With the policy: `No findings in 1 viewport.` from all four Checks. Without it: `(overlap, #t, major, 50)` and `(low-contrast-real, #grey, major)` | ✅ the row's guess is right, and it is now verified: such a page comes back clean from `overlap` and from `low-contrast-real`. Outside this slice, as the row says, and worth its follow-up: a strict style policy is common on production sites |
| A page that moves when it is scrolled | not probed | - | - |

### Probes of the unmutated code

Sixteen pages of this pass, outside the repository, called with the in-memory MCP client as `tests/helpers.py` does, `checks` equal to `["overlap"]` at 1440 × 900. Ahem at 20px on rows 50px apart, each text half under an opaque cover unless the row says otherwise.

| Probe | What it holds | Result | By the spec |
| ----- | ------------- | ------ | ----------- |
| `pf-filters` | 22 rows. Lists of functions: `grayscale(1) opacity(0.3)`, `grayscale(1) opacity(0.6)`, `opacity(0.4) grayscale(1)`, `opacity(0.6) grayscale(1) opacity(0.6)`, `saturate(2) blur(20px)`, `drop-shadow(...) grayscale(1)`, `invert(1) hue-rotate(90deg)`. `url(#m)` to an SVG `feColorMatrix`. `blur(20px)` and `brightness(0.5)` alone. A filter on the cover, on a pseudo-element that is the cover, on two nested elements, in a shadow tree. `-webkit-filter`. A filter declared `!important`, in an `@layer` with `!important`, and held by an animation with `forwards`. A cover whose `drop-shadow()` hides 40px of the text beside the 60px its box hides | Reported at 50%: every text that keeps at least half of its ink (16 rows, the cover with the shadow among them). No Finding: the five texts a kept function fades or blurs below half, and the one under `mix-blend-mode: difference` | ✅ every row |
| `pc-colours` | 26 rows. An alpha of 0 as `rgb(0 0 0 / 0)`, `#0000`, `hsl()`, `hwb()`, `lab()`, `lch()`, `oklab()`, `color(display-p3 ...)`, `color(xyz ...)`, `color(srgb ... / 0%)`, `color-mix(in oklab, ...)`, a relative colour, `light-dark()`, `calc()`, `lch(... / none)`, on `-webkit-text-fill-color` alone, through `currentcolor`, and with a `-webkit-text-stroke`. Opaque and translucent: `lab(0 0 0)`, `color(display-p3 0 0 0)`, `lch(0 0 0 / 0.01)`, a `color-mix()` of alpha 0.6, a relative colour of alpha 0.5, `hsl(... / 0.5)`, `oklch(none 0 0)`, a transparent `color` under an opaque fill | No Finding for the 18 of alpha 0; 50% for the 8 others. No call fails | ✅ every row |
| `pp-pseudo` | The four cases of the Out of Scope row (above) | as the row says | ✅ |
| `pw-wide` | A page 3000 × 2000: a text in its last corner, where neither scroll reaches a whole viewport; a text whose Hidden ink crosses the right edge of the first viewport; one that crosses its lower edge | 50% and its own cover for all three | ✅ |
| `pw-both` | A page scrolled 1500px sideways and 900px down while it loads | `(#far, major, 50, #far-cover)` | ✅ |
| `pu-depth` | A text with a badge that is its grandchild and a cover over its last 20px; a text half under a grandchild of an element of `role` `menu` | `(#g, minor, 16, #g-cover)`; no Finding for the second | ✅ |
| `pr-raised` | The rows of OVL-109 and OVL-110 with the larger cover first in the document | `(#u1, major, 50, #plain-large-first)`, `(#u2, minor, 50, #raised-large-first)` | ✅ |
| `ph-cap` | The row of `#striped`, nine fillers and a text a quarter covered: exactly 20,000 pixels of Hidden ink | `(#striped, major, 25, #stripes)`: every pixel tested | ✅ |
| `pb-border` | A text half under the left border, 100px wide, of an element with two glyphs of its own beside it | `(#under-border, major, 50, #bordered)` | ✅ |
| `pz-zoom` | `zoom: 2` on `body`; a row of `transform: scale(1.5)` | 50% and its cover for both | ✅ |
| `pr-raf-shim`, `pr-raf-never` | A page that replaces `requestAnimationFrame` by a timer, and one that replaces it by a function that never calls back | The first: `(#t, major, 50, #t-cover)`. The second: `Timed out after 30s.` | ⚠️ see "F17 and AD-007" |
| `pw-rtl-plain`, `pw-rtl` | A right-to-left page that does not scroll, and one 3000px wide that scrolls to the left, each with a covered text in the first viewport | The first: `(#rtl-plain, major, 50, #rtl-plain-cover)`. The second: no Finding | ⚠️ spec-precision gap 2 |
| `pcsp`, `pcsp-control` | The Content Security Policy row (above) | as the row guesses | ✅ |

On every page inside the scope of this slice the unmutated code gives the outcome the Terms and the Assumptions define. That is new: the third pass found two rules broken off their fixtures.

### Spec-precision gaps

1. ⚠️ **The row of Out of Scope that counts the changes reaching every Capture was not updated for AD-007.** `spec.md:55` still says "Two changes reach every Capture and are in scope: text is rasterized in grayscale, and a Capture settles the layout before it measures". The wait of F17 is a third, and it changes how long `inspect_element` takes and when it fails (below). The Assumptions row for it is marked "Taken by the agent ... the maintainer confirms or reverts it": the only row of the table that is not confirmed.
2. ⚠️ **A right-to-left page that scrolls sideways is in no row of Out of Scope.** On `pw-rtl` a text in the first viewport, half under a cover, gets no Finding, and `inspect_element` reads its box as all white: on such a page the screenshot starts left of where the boxes are counted from, for every tool. The limit is older than this slice and the plan of slice 7 names it (`.specs/features/offscreen-overflow/plan.md:103`, "their boxes then start at a negative x that the pixels do not have"); this spec does not. By the Terms the text has a Hidden share of 50% and a Coverer, so OVL-01 asks for a Finding. A row in Out of Scope closes it; the fix belongs to the Capture and to another slice.

---

## Discrimination Sensor

Run in scratch copies of `src/squint_mcp` at `a8feee6`, one copy per mutant, in the session's temp directory outside the repository. A copy is put first on `PYTHONPATH`, where it shadows the editable install, and pytest runs from the repository root against the real tests and fixtures; before each run the runner imports `squint_mcp` in the same environment and refuses to go on unless it comes from the copy. Each mutation is one text replacement that must match its file exactly once. Each was written by this Verifier, the twelve of the third pass from their descriptions in that report. A mutant with a test of its rule was run against that test; "Killed by" is the test that failed, with what it reported, read from the output. Every kill counted is an assertion on a value (a `ValueError` on unpacking is the tests' own "exactly one Finding"); none is a timeout or a tool error. A mutant with no test of its rule, or one that passed it, was run against all of `tests/test_overlap.py` (122 tests) and then against the four other modules that reach the code (`tests/test_detect_visual_bugs.py`, `test_low_contrast_real.py`, `test_text_clipped.py`, `test_offscreen_overflow.py`: 150 tests) before it was called a survivor. Line numbers are those of `a8feee6`.

### The twelve survivors of the third pass

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| V1 | `src/squint_mcp/checks/overlap.py:66` | the severity is lowered when any cover is in a Raised layer, not when the Coverer is | ✅ Killed - `test_a_raised_cover_that_hides_less_than_another_does_not_lower_the_severity`: `'minor' == 'major'` |
| V14 | `src/squint_mcp/checks/overlap.py:80` | `evidence.computed` is always `{"position": "static", "z-index": "auto"}` | ✅ Killed - both cases of `test_the_finding_carries_the_position_and_the_z_index_of_a_positioned_text` |
| V3 | `src/squint_mcp/js/covered_text.js:295` | hit testing never scrolls the page sideways | ✅ Killed - `test_covered_texts_right_of_the_viewport_name_their_covers`: `#near` alone of the four |
| V17 | `src/squint_mcp/js/covered_text.js:15` | the scroll across the page when the Capture is taken is read as 0 | ✅ Killed - `test_a_page_that_is_scrolled_sideways_when_it_is_captured_is_measured`: `[]` |
| V4 | `src/squint_mcp/js/covered_text.js:234` | the pseudo-elements of the texts stay painted in the glyphs-only screenshot | ✅ Killed - both cases of `test_text_under_a_pseudo_element_of_an_element_with_text_is_reported`: no Finding |
| V10 | `src/squint_mcp/js/covered_text.js:68` | any element with an `open` attribute is a Silent layer | ✅ Killed - `test_text_under_an_open_element_that_is_not_a_dialog_is_reported`: no Finding |
| V15 | `src/squint_mcp/js/covered_text.js:243` | a text is painted alone without what is inside it | ✅ Killed - both cases of `test_the_share_is_of_the_ink_a_text_shows_beside_what_is_inside_it` and `test_text_under_its_own_descendant_and_a_nick_beside_it_is_not_reported` (a Finding on `#child-and-nick`) |
| V6 | `src/squint_mcp/covered.py:272` | Hidden ink is not cut to Text ink | ✅ Killed - `test_covered_text_in_a_font_with_anti_aliased_edges_is_measured_by_its_ink`: `#font-whole` at 188%, not 100% |
| V7 | `src/squint_mcp/covered.py:246` | two texts share a screenshot unless the later one's region touches the earlier one's text | ✅ Killed - `test_a_tag_that_stands_before_the_text_it_covers_is_measured_apart_from_it`: no Finding on `#under-tag-first` |
| V16 | `src/squint_mcp/covered.py:303` | the step grows with the pixels, not with their square root | ✅ Killed - `test_a_page_of_over_twice_the_cap_is_still_tested_at_every_second_pixel` |
| V13 | `src/squint_mcp/tools/detect_visual_bugs.py:116` | an `info` Finding is ordered as a `minor` one | ✅ Killed - `test_an_info_finding_comes_after_the_minor_ones_and_is_counted_apart`: `#a` before `#b` |
| N14 | `src/squint_mcp/capture.py:224` | every text with Hidden ink is hit tested, also under the reporting threshold | ✅ Killed - `test_hidden_ink_of_a_text_under_a_tenth_hidden_does_not_count_to_the_cap` |

**12/12 killed**, each by the test written for it. The kills of the first two passes were not run again, and neither were A7, A8, N7 and V2, which the third pass judged equivalent: `git diff a11b13e..HEAD -- src` touches none of their lines.

### New mutations of this pass

None of these was tried in an earlier pass. They aim at the three changes of this round to `src/` and at the neighbours of the rules the new fixtures pin: the other axis, the other order, the other side, the next value of a threshold.

**The filter change (F9), `src/squint_mcp/js/covered_text.js:50-56`**

| # | Line | Mutation | Outcome |
| - | ---- | -------- | ------- |
| F1 | `:53` | no `filter` is touched (the code before the fix) | ✅ Killed - both cases of `test_covered_text_under_a_filter_that_changes_colours_is_reported` (no Finding) and `test_covered_text_of_a_page_with_a_filter_on_its_root_is_reported` (`[]`) |
| F2 | `:54` | a `filter` with nothing to keep becomes `none`, not `opacity(1)` | ✅ Killed - `test_a_cover_that_the_filter_of_its_block_places_stays_over_its_text` (no Finding) and `test_text_above_the_layer_that_a_filter_makes_is_not_reported` (a Finding) |
| F3 | `:50` | `opacity()` is not kept | ✅ Killed - `test_text_under_a_cover_that_a_filter_fades_out_is_not_reported` and `test_covered_text_that_a_filter_fades_out_is_not_reported` (a Finding each) |
| F4 | `:50` | `blur()` is not kept | ❌ Survived - `O` (122) and the four other modules (150) pass |
| F5 | `:50` | `drop-shadow()` is not kept | ❌ Survived - `O` and the four other modules pass |
| F6 | `:53` | a `filter` that holds a function to keep is left whole, with its functions that change colours | ❌ Survived - `O` and the four other modules pass |
| F7 | `:55` | the new `filter` is set without `!important` | ❌ Survived - `O` and the four other modules pass |
| F8 | `:55` | only the first of the kept functions is set | ❌ Survived - `O` and the four other modules pass |

**The alpha change (F10), `src/squint_mcp/checks/overlap.py:28-34`**

| # | Line | Mutation | Outcome |
| - | ---- | -------- | ------- |
| A1 | `:34` | an alpha of `none` is opaque | ✅ Killed - `test_covered_text_of_an_alpha_of_zero_in_any_notation_is_not_reported[#transparent-none]`: a Finding |
| A2 | `:28` | only an alpha after a slash is read, not the fourth value of `rgba()` | ✅ Killed - `test_covered_text_painted_transparent_is_not_reported` and `test_covered_text_of_an_opaque_colour_and_a_transparent_fill_is_not_reported`: a Finding each |
| A3 | `:28` | only the fourth value of `rgba()` is read (the code before the fix) | ✅ Killed - the three cases of `test_covered_text_of_an_alpha_of_zero_in_any_notation_is_not_reported` |
| A4 | `:34` | glyphs count as transparent at any alpha under 1 | ✅ Killed - `test_covered_text_painted_half_transparent_is_reported` and `test_covered_text_of_an_alpha_above_zero_in_any_notation_is_reported[#translucent-oklch]`: no Finding |

**The wait before a screenshot (F17), `src/squint_mcp/capture.py:37-40` and `:119`**

| # | Line | Mutation | Outcome |
| - | ---- | -------- | ------- |
| P1 | `:119` | no wait (the code before the fix) | ✅ Killed - `test_a_covered_text_low_on_a_page_of_layers_is_reported_on_every_call` failed in 5 runs of 5, each with `[] == [('#low', 'major', 50, '#low-cover')]` |
| P2 | `:39` | one animation frame, not two | ⚠️ Survived - the test of OVL-120 passed in 5 runs of 5, then `O` and the four other modules pass. Not a gap: see "F17 and AD-007" |

**Neighbours of the rules the new fixtures pin**

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| R1 | `src/squint_mcp/checks/overlap.py:66` | the Raised layer is read from the last cover in the document, not from the Coverer | ❌ Survived - both tests of OVL-109 and OVL-110 pass, then `O` and the four other modules |
| S1 | `src/squint_mcp/js/covered_text.js:300` | a point is looked up where the page was asked to scroll sideways, not where it is | ✅ Killed - `test_covered_texts_right_of_the_viewport_name_their_covers`: no Finding on `#edge` |
| S2 | `src/squint_mcp/js/covered_text.js:300` | the same, down the page | ✅ Killed - `test_a_covered_text_low_on_a_page_of_layers_is_reported_on_every_call`: `coveredBy` is the cover of the twentieth row, not `#low-cover` |
| S3 | `src/squint_mcp/js/covered_text.js:177` | an element the scroll moved sideways is not passed over | ✅ Killed - `test_covered_texts_right_of_the_viewport_name_their_covers`: `#fixed-bar` for `#right` |
| S4 | `src/squint_mcp/js/covered_text.js:178` | an element the scroll moved down the page is not passed over | ✅ Killed - `test_an_element_the_scroll_brings_over_a_text_is_not_what_covers_it`: `#fixed-bar`, not `#far-cover` |
| T1a | `src/squint_mcp/js/covered_text.js:234` | only `::before` is hidden in the glyphs-only screenshot | ✅ Killed - `test_text_under_a_pseudo_element_of_an_element_with_text_is_reported[after]` |
| T1b | `src/squint_mcp/js/covered_text.js:234` | only `::after` is hidden there | ✅ Killed - the same test, `[before]` |
| B1 | `src/squint_mcp/js/covered_text.js:232` | the borders of the texts stay painted in that screenshot | ❌ Survived - `O` and the four other modules pass |
| U1 | `src/squint_mcp/js/covered_text.js:37-43` | what is inside an element is its children, not all of its descendants | ❌ Survived - `O` and the four other modules pass |
| G2 | `src/squint_mcp/covered.py:245` | two texts share a screenshot unless the earlier one's region touches the later one's text (V7 the other way) | ✅ Killed - `test_a_text_under_the_box_of_a_tag_whose_glyphs_stand_beside_it_is_measured`: no Finding on `#under-tag` |
| E1 | `src/squint_mcp/covered.py:98` | a pixel is seen from half of the ink of a full pixel on, not from half of its own | ✅ Killed - `test_text_in_such_a_font_mostly_seen_through_a_veil_is_not_reported` (a Finding on `#font-veil-45`) and `test_text_mostly_seen_through_a_veil_is_not_reported` (`#veil-45` at 10%) |
| H1 | `src/squint_mcp/covered.py:303` | a page of exactly 20,000 pixels of Hidden ink is sampled too (`floor(...) + 1` for `ceil(...)`) | ❌ Survived - `O` and the four other modules pass |
| H2 | `src/squint_mcp/covered.py:303` | the step is never above 2 | ✅ Killed - `test_a_page_of_over_four_times_the_cap_is_tested_at_every_third_pixel`: `#solid-cover`, not `#stripes` |

**Mutants the tasks name in a "Done when" that no table above holds**

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| K2 | `src/squint_mcp/checks/overlap.py:34` | every colour that is not written as `rgb()` is transparent | ✅ Killed - both cases of `test_covered_text_of_an_alpha_above_zero_in_any_notation_is_reported`: no Finding |
| K3 | `src/squint_mcp/checks/overlap.py:34` | every colour with a slash in it is transparent | ✅ Killed - the same test, `[#translucent-oklch]`: no Finding |
| K4 | `src/squint_mcp/checks/overlap.py:66` | the Raised layer is read from the first cover in the document | ✅ Killed - the tests of OVL-109 (`'minor' == 'major'`) and OVL-110 (`'major' == 'minor'`) |
| K5 | `src/squint_mcp/capture.py:231` | the Hidden ink of a transparent text is left out of the sum the step is taken from | ✅ Killed - `test_hidden_ink_of_a_text_that_gets_no_finding_counts_to_the_cap`: `#stripes`, not `#solid-cover` |

F1 was also run against the test of OVL-94, as F9 claims: killed, no Finding on `#held`.

**Sensor depth**: expanded (43 mutants this pass: the 12 survivors of the third pass, 27 new ones (8 in the filter change, 4 in the alpha change, 2 in the wait, 13 on the neighbours of the new fixtures) and 4 the tasks name)
**Sensor outcome**: third-pass survivors 12/12 killed; new mutants 17/27 killed, 10 survived: 9 gaps and 1 that no test can tell from the code (P2); mutants the tasks name 4/4 killed - ❌

### The survivors, decided by probes through the MCP boundary

Each survivor was called on a probe page of this pass, with the same client as the unmutated code.

| Mutant | Probe | Unmutated | Under the mutant | By the spec |
| ------ | ----- | --------- | ---------------- | ----------- |
| F4 | `pf-filters`: a text of `filter: blur(20px)` and one of `saturate(2) blur(20px)`, each half covered | no Finding for either | `(#f-blur, major, 50, ...)`, `(#f-blur-list, major, 50, ...)` | Assumptions, "A `filter`": `blur()` is applied; Terms, "Text ink": text faded below half by a `filter` has none |
| F5 | `pf-filters`: a cover whose box hides 60px of a text and whose `drop-shadow()` hides 40px more | `(#f-cover-shadow, major, 50, ...)` | 30% | the same row: `drop-shadow()` is applied; what it hides is not seen |
| F6 | `pf-filters`: `grayscale(1) opacity(0.6)` and `drop-shadow(...) grayscale(1)` on a text | 50% for both | no Finding for either | the same row: "the functions of every `filter` that change colours left out" |
| F7 | `pf-filters`: a row of `filter: grayscale(1) !important`, one whose filter is in an `@layer` with `!important`, one whose filter an animation holds | 50% for all three | no Finding for any | OVL-92's rule, on a page that declares its filter with more weight than an inline style |
| F8 | `pf-filters`: a text of `opacity(0.6) grayscale(1) opacity(0.6)`, which shows 36 parts in 100 of its ink | no Finding | `(#f-two-kept, major, 50, ...)` | the same row: the kept functions stay, "in their order" (`covered_text.js:46-47`); Terms, "Text ink" |
| R1 | `pr-raised`: the rows of OVL-109 and OVL-110 with the larger cover first in the document | `(#u1, major, ...)`, `(#u2, minor, ...)` | `#u1` `minor`, `#u2` `major` | Assumptions, "Several elements cover one text": the Raised-layer rule reads the Coverer |
| B1 | `pb-border`: a text half under the left border of an element with two glyphs of its own beside it | `(#under-border, major, 50, #bordered)` | no Finding | OVL-01; Terms, "Text ink" |
| U1 | `pu-depth`: a text with a badge that is its grandchild and a cover over its last 20px; a text half under a grandchild of a `menu` | `(#g, minor, 16, #g-cover)`; no Finding for the second | `(#g, major, 50, #g-cover)`, `(#m-under, major, 50, #deep-item)` | Terms, "Other element" and "Silent layer": descendants, not children |
| H1 | `ph-cap`: exactly 20,000 pixels of Hidden ink | `(#striped, major, 25, #stripes)` | `coveredBy` `#solid-cover` | Terms, "Coverer": "more than 20,000 pixels"; OVL-85: "no more than 20,000" |

**The gaps.** Nine mutants change what the tool returns on a page a fixture can hold, and no test fails. Five are in the thirteen lines F9 added: the fixtures hold a `filter` of one function that changes colours, `opacity(0)`, and the two things an element with a `filter` goes on doing, and they do not hold a list of functions, `blur()`, `drop-shadow()` or a filter the page declares `!important`. F6 is the one with reach: a list is how a `filter` is commonly written, and under F6 every text inside one that mixes the two kinds is missed. The other four each take a second condition (a text blurred or faded away that is also covered, a shadow that hides ink, an `!important`). R1, U1, H1 and B1 are neighbours of rules the round pinned from two sides and not from a third: the order of the two covers in the document, the depth of what is inside a text or a layer, the bound itself of the cap, and the border next to the background (V5) and the pseudo-elements (V4) of a text.

**P2 is not a gap.** One frame and two frames give the same answer here on every call measured (below). No test through the tool boundary can hold the difference, and the criterion (OVL-120) does not ask for two.

**Is the pattern of the third report still there?** In part. Where that report named a mutant, this round pinned its neighbours too: the child at the start and at the end, `::before` and `::after`, the raised cover as the smaller and as the larger, the scroll down and sideways with the clamp at the end of the page on both axes, steps of 2 and of 3, ink that counts and ink that does not. Nine of the thirteen neighbour mutants of this pass died, and the four that did not each needed one more dimension than the fixtures have. Where the round wrote new code, the pattern is unchanged: the fixtures of F9 are the pages of the third report's probes (a grey-scaled row, an inverted root, a filter on the text) plus three for the design's own claims, and five of the eight mutants of those thirteen lines live. The alpha change is the counter-example: one rule for every notation, four mutants, four kills.

**What the probes say of the code.** Unmutated, it gives on every probe of this table the outcome the spec defines. The survivors are behaviours the code has and no test holds, not defects.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, apart from this report and the lessons store written afterwards. `HEAD` is `a8feee6` on `feat/overlap` both times and `git worktree list` shows the main tree alone: no worktree was added. `git stash` was not used. Every mutant lived in its own copy under the session's temp directory; pytest ran with `-p no:cacheprovider` and without bytecode files. Up to four runs were under way at once: no test failed for a timeout in any of them. No process of the sensor is left running.

---

## F17 and AD-007

F17 was not asked for by the third report. The author found, while running new tests against their mutants, that a screenshot taken right after a change of style sometimes shows a band of the page beyond the viewport unpainted, and made `_screenshot` wait two animation frames first (`src/squint_mcp/capture.py:37-40`, `:119`). The maintainer was away; AD-007 and the Assumptions row say so and leave the decision open. This is what this pass measured.

| Question | Evidence of this pass | Answer |
| -------- | --------------------- | ------ |
| Is the fault real? | `detect_visual_bugs` called 30 times in a row on `overlap-low.html` with the wait taken out (mutant P1): 10 calls return the Finding of `#low`, 20 return `[]`. The test of OVL-120 failed in 5 runs of 5 under P1 | Yes: two calls in three here. It is a fault of the product, not of the tests: a covered text low on a page of layers loses its Finding on some calls |
| Does the wait end it? | The same 30 calls on the code as committed: 30 Findings. The test of OVL-120 passed in the gate and in each of the full runs of `tests/test_overlap.py` the sensor made with up to four browsers at work (nine runs whose mutant is nowhere near the wait: 54 calls, 54 Findings) | Yes, as far as a sample can say |
| Does the test hold the fix? | P1 killed 5 times of 5. At two misses in three, six calls all hit less than once in 700 runs | Yes, as a sample of six: no page brings the fault about on every call, and the criterion says so |
| Are two frames needed? | With one frame (mutant P2): 30 Findings in 30 calls, the test passed 5 times of 5, and all 272 tests pass | Not shown. AD-007 lists what was tried and dropped; one frame is not on the list. The second frame is about half of the cost |
| What does it cost? | The suite took 1041s here (17:21) for 359 tests, against 756s for 325 in the third pass. AD-007 gives an eighth to a fifth more time per Capture | As AD-007 says |
| Can the wait fail? | Probe `pr-raf-never`: a page whose script replaces `window.requestAnimationFrame` by a function that never calls back. With the wait: `Timed out after 30s.` With the wait taken out (P1): `(#t, major, 50, #t-cover)` in 2.3s. A page that replaces it by a timer (`pr-raf-shim`) is measured as before | Yes. `page.evaluate` runs in the page's own world and calls whatever the page has put under that name. AD-007 names the risk ("none is known"); it is now shown. It reaches every tool that takes a Capture, `inspect_element` included |
| Is it in scope? | `spec.md:55` puts in scope "two changes [that] reach every Capture"; this is a third | The row needs the maintainer's word, with the Assumptions row |

**Judgement.** The fix is right and the decision to take it was sound: the fault is real, it is in code every Check has read since slice 4 (the three fills of AD-004 are screenshots taken right after a change of style too), and without it the new tests could not be trusted. It should stay. Two things are open for the maintainer. First, the wait has no bound of its own: a timer raced against the two frames, inside the same `page.evaluate`, would turn the 30s failure into a few milliseconds more on a page that never paints a frame. Second, the row of `spec.md:55`. Whether to wait one frame or two is a matter of margin against a fault no test can pin; this pass could not tell them apart.

Not verified by anyone: the branch was never pushed, so neither the timing of this fault nor the system font of `overlap-font.html` has met the CI's Linux.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

The diff of this round under `src/` is 13 lines in `js/covered_text.js`, 11 in `checks/overlap.py` and 14 in `capture.py`.

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ one loop over the elements with one regular expression; one regular expression for every colour notation in place of the one for `rgb()`; one `evaluate` before a screenshot. No option, no abstraction |
| Surgical changes | ✅ nothing around the three changes was touched; `inspect_element` and `ping` are untouched as files |
| No scope creep | ⚠️ F17 reaches every tool and was not in the fix plans. It is justified by a fault this pass reproduced, and recorded in AD-007, in the Assumptions and in the CHANGELOG; `spec.md:55` was not brought in line |
| Matches patterns | ✅ the page script holds what only the page can know, the Check stays a function of a Capture, the comment on each change says why and cites its decision |
| Spec-anchored outcome check (asserted values match spec) | ✅ for the 119 criteria due now |
| Per-layer Coverage Expectation met | ⚠️ every criterion has its assertion; the nine behaviours listed as gaps in the sensor section have none |
| Every test maps to a spec requirement - no unclaimed tests | ✅ the 34 new tests map to OVL-92 to OVL-120; `test_the_reach_fixture_has_these_findings_in_this_order` is the "one test asserts the whole list" of F12 |
| Documented guidelines followed: `CONTRIBUTING.md` and `docs/SPEC.md`, Testing Decisions (one seam, real Chromium, no unit test of a helper) | ✅ every new test calls a tool through the in-memory client; no helper of `covered.py` or of the page script is called directly |

Observations, not gaps:

- `_is_transparent` (`src/squint_mcp/checks/overlap.py:31-34`) calls `float()` on what follows the slash. On the 26 colours of probe `pc-colours` Chromium writes a number or `none` there and no call fails. A token that is neither would fail the whole call, not one Finding.
- The cover script matches the functions to keep in the text of the computed `filter` (`covered_text.js:50`). A `url()` filter is taken out with the functions that change colours (probe `#f-url`: reported), whatever the SVG filter does. The Assumptions row says "and the like"; it does not name `url()`.
- The rule "a glyph colour of alpha 0 is hidden on purpose" also silences a text painted by its `-webkit-text-stroke` alone (probe `#t-stroke`) and, as the third pass noted, a heading painted with a gradient. That is the rule as the Assumptions have it.
- The highlights repaint glyphs whatever their alpha: a text of `lch(0 0 0 / 0.01)`, which nobody can read, is reported at 50% (probe `#o-lch-low`). Also the rule as written: only an alpha of 0 is "hidden on purpose".
- `tests/test_overlap.py:94` reads the first text block, not the first block. `tests/test_detect_visual_bugs.py` holds that the two are the same.

---

## Edge Cases

- [x] OVL-68: the Findings of 1440 × 900 are also those of 390 × 844 (`tests/test_overlap.py:180-190`)
- [x] OVL-69: an element behind the clipped part of a text does not cover it (`tests/test_overlap.py:880-881`)
- [x] OVL-120: a covered text low on a page of layers is reported on six calls in a row (`tests/test_overlap.py:935-937`)

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`, each command run with its own exit status recorded
- **Gate outcome**: pyright exit 0 (0 errors, 0 warnings, 0 informations); ruff check exit 0 (All checks passed); ruff format --check exit 0 (104 files already formatted); pytest exit 0 - 359 passed, 0 failed, 0 skipped, in 1041.78s
- **Test count before feature**: 237
- **Test count after the first pass**: 302
- **Test count after the second pass**: 312
- **Test count after the third pass**: 325
- **Test count now**: 359
- **Delta**: +122 over the feature, all in `tests/test_overlap.py`; +34 in the third fix round
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed or weakened. `git diff b08856a..HEAD -- tests/test_overlap.py` removes one line, the count of the bounds fixture, which goes from 34 to 39 with the five new Findings; the pinned list of selectors grows by the same five. `git diff b08856a..HEAD -- tests/fixtures` removes three comment lines of the bounds fixture (its pixel count, rewritten) and nothing else; the clean fixture only gains rows, and the whole-page test of OVL-19 passes on it. No other test module changed in this round, and the only assertions of the earlier slices that changed since `eb9778b` are the four `Valid checks:` literals OVL-55 supersedes

---

## Fix Plans

The loop is at its bound, so these go to the maintainer. Fixes 1 to 5 are a fixture row, a criterion and a test each, with the code as it is; each can start from the probe page named in the sensor section. Fixes 6 and 7 are decisions. Ranked by how likely a later change is to walk into the gap.

### Fix 1: The filter rule beyond a filter of one function (F4, F5, F6, F7, F8)

- **Root cause**: the fixtures of F9 hold `grayscale(1)`, `hue-rotate(180deg)`, `sepia(1)`, `invert(1)` and `opacity(0)`, each alone and each from a plain rule. The sentence of the Assumptions is about lists ("the functions of every `filter` that change colours left out ... and those that keep them ... applied"), and the code has an order, three kept functions and a priority that nothing reads.
- **Fix task**: five rows. In the bounds fixture: a text of `filter: grayscale(1) opacity(0.6)`, half covered, reported at 50% (F6); a row of `filter: grayscale(1) !important`, its text half covered, reported at 50% (F7); a cover whose box hides 60px and whose `drop-shadow()` hides 40px more, reported at 50% (F5). In the clean fixture: a text of `filter: blur(20px)`, half covered, no Finding (F4); a text of `filter: opacity(0.6) grayscale(1) opacity(0.6)`, half covered, no Finding (F8).
- **Done when**: each test fails under its mutant: `blur` or `drop-shadow` taken out of the expression at `covered_text.js:50`, a filter with a kept function skipped at `:53`, `"important"` dropped or `kept[0]` set at `:55`.
- **How likely**: a list of filter functions is how a filter is commonly written. The code is right today on all 22 rows of probe `pf-filters`.
- **Priority**: Major for F6, Minor for the others

### Fix 2: What is inside a text or a layer, deeper than a child (U1)

- **Root cause**: in every fixture the element inside a text (a badge, a link) and the element inside a Silent layer that covers a text are direct children.
- **Fix task**: two rows from probe `pu-depth`. A text with a badge that is its grandchild over its first 80px and a cover over its last 20px: one Finding, 16%, `minor`. A text half under a grandchild of an element of `role` `menu`: no Finding.
- **Done when**: both tests fail with `subtreeOf` returning the element and its children only (`covered_text.js:37-43`): 50% `major`, and a Finding.
- **How likely**: a badge wrapped in a span, a menu item two levels down: common markup.
- **Priority**: Minor

### Fix 3: The Raised layer read from the Coverer when it is first in the document (R1)

- **Root cause**: in both rows of OVL-109 and OVL-110 the Coverer is the second of the two covers in the document.
- **Fix task**: the two rows again with the larger cover first (probe `pr-raised`): `major` with the plain one as Coverer, `minor` with the raised one.
- **Done when**: the tests fail with `covered.covers[-1].raised` at `overlap.py:66`.
- **How likely**: rare.
- **Priority**: Minor

### Fix 4: A text under the border of an element with text (B1)

- **Root cause**: V5 (the background) and V4 (the pseudo-elements) have fixtures; the border the same rule resets has none.
- **Fix task**: a text half under the left border, 100px wide, of an element with two glyphs of its own beside it, all seen (probe `pb-border`): one Finding, 50%, covered by that element.
- **Done when**: the test fails with `border-color: transparent` taken out of the rule at `covered_text.js:232`.
- **How likely**: now and then: a bordered label or tab over a neighbour.
- **Priority**: Minor

### Fix 5: The cap itself (H1)

- **Root cause**: the fixtures hold 19,000 and 21,000 pixels; "more than 20,000" and "no more than 20,000" meet at a value nothing has.
- **Fix task**: a page of exactly 20,000 pixels of Hidden ink built on the row of `#striped` (probe `ph-cap`): its Coverer is `#stripes`.
- **Done when**: the test fails with `math.floor(...) + 1` for `math.ceil(...)` at `covered.py:303`.
- **How likely**: rare, and it changes only which of two covers is named.
- **Priority**: Minor

### Fix 6: AD-007, the wait before a screenshot (a decision)

- **Root cause**: the wait is `requestAnimationFrame` of the page's own world, with no bound, and the spec counts two changes that reach every Capture where there are three.
- **Fix task**: the maintainer confirms AD-007 or reverts `51ff006`. If it stays: race the two frames against a timer inside the same `evaluate`, so that a page that never calls a frame back is still measured; bring `spec.md:55` in line; decide whether one frame is enough.
- **Done when**: probe `pr-raf-never` returns its Finding, and a test holds it (a fixture whose script replaces `requestAnimationFrame` by a function that never calls back).
- **How likely**: rare. When it happens every tool fails on that page.
- **Priority**: Minor

### Fix 7: A right-to-left page that scrolls sideways (spec-precision gap 2, a decision)

- **Root cause**: on such a page the screenshot and the boxes do not start at the same place; `inspect_element` reads the wrong pixels there too. Older than this slice.
- **Fix task**: a row in Out of Scope ("Known limit of the Capture"), and an issue for the Capture.
- **Done when**: the spec and probe `pw-rtl` say the same.
- **How likely**: rare.
- **Priority**: Minor

### Outside this slice: a Content Security Policy that refuses inline styles

Not a fix of this feature; the row of Out of Scope asks for a follow-up and this pass gives it its evidence. Probe `pcsp`: under `style-src file:` the page returns `No findings in 1 viewport.`; without the policy the same page returns one `overlap` and one `low-contrast-real` Finding, both `major`. The styles a Capture injects are refused, no text has ink, and the result reads as a clean page. `design.md` already names the remedy to try (`bypass_csp` on the browser context).

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| OVL-01 to OVL-66, OVL-68 to OVL-91 | Implemented | ✅ Verified |
| OVL-38 | ❌ Needs Fix in the third pass | ✅ Verified: the rule holds for every notation probed |
| OVL-92, OVL-93, OVL-95 to OVL-97 | Implemented | ⚠️ Verified as written; Fix 1 pins the rule beyond a filter of one function |
| OVL-94, OVL-98 to OVL-104, OVL-107, OVL-108, OVL-111 to OVL-119 | Implemented | ✅ Verified |
| OVL-105, OVL-106 | Implemented | ⚠️ Verified as written; Fix 2 pins a descendant deeper than a child |
| OVL-109, OVL-110 | Implemented | ⚠️ Verified as written; Fix 3 pins the other order of the two covers |
| OVL-120 | Implemented | ✅ Verified as a sample of six calls; Fix 6 is the decision on AD-007 |
| OVL-67 | Pending | Pending the verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready by the spec's own third success criterion; the first two are met

**Spec-anchored check**: 119/119 criteria due now match the spec outcome; OVL-67 pending the verdict; no rule broken off its fixture inside the scope of the slice; 2 spec-precision gaps
**Sensor**: third-pass survivors 12/12 killed; 27 new mutants, 17 killed, 10 survived: 9 gaps and 1 no test can tell; the 4 further mutants the tasks name, 4 killed
**Gate**: 359 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: everything the earlier passes found working, and now a covered text under a filter that changes colours (on the text, around it, on the root, in a list, in a shadow tree, declared `!important`), a glyph colour of alpha 0 in eighteen ways of writing it, a font with anti-aliased edges, a text with a child over part of it, a cover with text before its text, an open `details`, a raised cover that is or is not the Coverer, pseudo-elements, a page wider than its viewport up to its last corner, a page scrolled on both axes when it is captured, the place of an `info` Finding, and the size of the sample at 19,000, 20,000, 21,000, 49,000 and 81,000 pixels.

**What could have failed and did not**: the twelve survivors of the third pass (all killed by an assertion on a value), every mutant the tasks name in a "Done when" (all killed), the reading of the 29 new criteria against their fixtures (all faithful), the Out of Scope rows of this round against the code (all agree), the test integrity check (nothing removed or weakened), and sixteen probe pages against the unmutated code.

**Issues found**:

1. Five behaviours of the filter fix without a test: a list of functions, `blur()`, `drop-shadow()`, the order of the kept functions, `!important` (Fix 1).
2. Four neighbours of the new fixtures without a test: a descendant deeper than a child, the Coverer first in the document, a border, the cap itself (Fix 2 to 5).
3. The wait of AD-007 has no bound and fails every tool on a page that never calls an animation frame back; `spec.md:55` counts two changes where there are three (Fix 6, a decision).
4. A right-to-left page that scrolls sideways is in no row of Out of Scope (Fix 7, wording).

**Next steps**: the loop is at its bound of three rounds, so this goes to the maintainer, with three things to decide. (1) AD-007: confirm it, and whether to bound the wait. (2) The nine gaps: accept the feature with the residual this report lists, or have Fix 1 to 5 done, about nine fixture rows and no change to `src/`. (3) The stopping rule: four passes of fresh mutants found 11, 11, 12 and 9 alive; "no surviving mutant" against a sensor that writes new ones each time may not be a bar a round can meet, and the maintainer may want to say which mutants count. OVL-67 stays pending until a PASS.
