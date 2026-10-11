# overlap Validation

**Date**: 2026-10-11
**Spec**: `.specs/features/overlap/spec.md` (OVL-01 to OVL-91)
**Diff range**: `eb9778b..a11b13e` (24 commits, branch `feat/overlap`, base `8aa017c`); the second fix pass is `0a25cca..a11b13e`
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 3, the last before the loop goes to the maintainer

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

The second fix pass did what it was asked. The eleven survivors of the second pass are all killed, each by the test written for it; the six earlier mutants whose fixtures grew are still killed; the twelve new criteria are faithful statements of rules the Terms and the Assumptions already held; every one of the 90 criteria due now has an assertion on the outcome the spec defines; the gate is green; and `git diff 0a25cca..HEAD -- src` is empty.

The verdict is FAIL for three reasons, in the order a maintainer should weigh them.

1. **The code and the spec disagree on three kinds of page that no fixture holds.** Text under a `filter` that changes colours is never reported: the design accepts that and neither the spec nor the CHANGELOG says it. Text made transparent with a colour that Chromium does not compute to `rgb()` is reported, against the rule OVL-38 states: the first defect of `src/` against a criterion's rule in three passes. And the Out of Scope row the fix pass added for pseudo-elements does not cover two cases the code misses for the same reason.
2. **The sensor, pointed again at what no earlier pass tried, left survivors again.** Of 17 new mutants 5 were killed and 12 survived: 1 is equivalent, and 11 give, on a probe page called through the MCP boundary, a result the Terms exclude. N14, which the second pass could not call a gap, is one now that the spec defines its outcome. The spec's third success criterion asks for none.
3. **The pattern has not changed in three passes.** 11 gaps of 49 mutants, then 11 of 21, now 12 of 18. Each fix pass closed exactly the mutants it was shown and stopped there: the scroll at capture is pinned down the page and not across it, the tag over a text in one order of the document and not the other, the open `dialog` on the silent side and not the other. A fourth round of the same would find a fourth batch.

**How much of the code's behaviour is held by tests.** Over the three passes 87 different mutants were written against the 950 lines this feature adds under `src/`. 4 are equivalent. Of the 83 that a page can tell from the real code, 71 were killed when last run (26 of them in this pass, at `a11b13e`) and 12 are not killed. What is held: both thresholds and the truncation, the five roles and how the attribute is read, the open `dialog`, the popover, `fixed` and `sticky`, a Silent layer around the text, the veil on both sides of a half, Text ink on both sides of a half, own text against a child's, Other elements against ancestors and descendants, the Raised layer in all the forms the spec names, the Coverer by size and by document order, shadow trees, the sample by column, by row and at both sides of the cap, a page scrolled down when captured, four texts in one place, and that the other three Checks read the same page as before. What is not held is the list of gaps below: none of them is a wrong result today.

**How serious the gaps are for a user of the tool.** Today, on a real page, a user meets only the first group: a covered text inside a grey-scaled or inverted section is silently missed (likely on some sites, and then for every text in that section), and a text made transparent through a `color-mix()` and partly covered gets a false Finding (uncommon). Everything the sensor found is correct in the code as it is. The risk there is the next change: a refactor of `hidden_ink` could double every share on every real font, or one of the page script could drop every Finding right of the viewport, and all 325 tests would stay green.

OVL-67 (the roadmap) is a closing step that follows a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `O` = `tests/test_overlap.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Earlier passes

The two earlier reports are in git in full, at `aef0799` and `0a25cca`. This pass used them as a map of what had been tried and re-derived the rest.

**First pass (`aef0799`): FAIL.** 68 of 68 criteria matched and the gate was green. Of 49 mutants 36 were killed and 13 survived: 2 equivalent (A7, A8) and 11 gaps. Four commits closed the gaps with ten criteria (OVL-70 to OVL-79); none touched `src/`.

| Gap of the first pass | Mutant | Closed by | Criterion |
| --------------------- | ------ | --------- | --------- |
| The `role` attribute compared as written | J4 | `7c32a5b` | OVL-70 |
| A list of roles taken for a Silent layer | J5 | `bb64438` | OVL-71 |
| An ancestor of the text counted as an Other element | J6b | `7c32a5b` | OVL-72 |
| A descendant of the text counted as an Other element | J6c | `7c32a5b` | OVL-73 |
| An element the scroll moved not passed over | J8 | `1e5d5ef` | OVL-77 |
| A text the step passes over whole not tested | J10 | `f5f190b` | OVL-78 |
| Text ink from any ink | C2 | `7c32a5b` | OVL-74 |
| Text ink from ink of 200 | C2b | `bb64438` | OVL-75 |
| Every measured text in one group | C5 | `bb64438` | OVL-76 |
| A measured text read on the first channel | C11 | `bb64438` | OVL-76 |
| Every hidden pixel hit tested (no cap) | C8 | `f5f190b` | OVL-79 |

**Second pass (`0a25cca`): FAIL.** 78 of 78 criteria matched, the gate was green and the eleven survivors of the first pass were all killed. Of 21 new mutants 8 were killed and 13 survived: 11 gaps, 1 equivalent (N7) and 1 where the spec defined no outcome (N14). Two spec-precision gaps. Four commits closed them with twelve criteria (OVL-80 to OVL-91), two new fixtures and two edits of the spec text; none touched `src/`.

| Gap of the second pass | Mutant | Closed by | Criterion |
| ---------------------- | ------ | --------- | --------- |
| A measured text read in the round of another | N2 | `c6dd9f1` | OVL-80 |
| A third channel without ink | N3 | `c6dd9f1` | OVL-80 |
| A text cut out at the column of another | N1b | `c6dd9f1` | OVL-81 |
| The region of a text without its box | N9 | `c6dd9f1` | OVL-82 |
| The glyphs of a child counted as ink of its parent | N28 | `c6dd9f1` | OVL-83 |
| Glyphs transparent at any alpha under 1 | N10 | `c6dd9f1` | OVL-87 |
| The alpha read from `color` | N22 | `c6dd9f1`, `93357ec` | OVL-89, OVL-88 |
| A hidden Silent layer painted with the text | N11 | `c6dd9f1` | OVL-90 (and OVL-91, `93357ec`, for the Goal) |
| Only the columns of the sample | N5 | `d1eadfb` | OVL-84 |
| A page under the cap sampled too | N13 | `d1eadfb` | OVL-85 |
| The scroll at capture read as 0 | N8 | `a11b13e` | OVL-86 |
| Which Hidden ink counts towards the cap (spec-precision gap 1) | N14 | `c6dd9f1` | a sentence in the Term "Coverer"; no criterion |
| A limit the design accepts and the spec does not list (spec-precision gap 2) | - | `c6dd9f1` | a row in Out of Scope |
---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T13 | ✅ Done | `89385b0` to `cb8d81b`, as in the earlier passes |
| F1 to F4: the fixes of the first pass | ✅ Done | `7c32a5b`, `bb64438`, `1e5d5ef`, `f5f190b` |
| F5: texts stacked in one place, where a text sits, the colour of its glyphs | ✅ Done | `c6dd9f1`, with the two edits of the spec text |
| F6: a transparent fill and closed menus | ✅ Done | `93357ec` |
| F7: the rows of the sample and a page under the cap | ✅ Done | `d1eadfb` |
| F8: a page that is scrolled when it is captured | ✅ Done | `a11b13e` |

Every box of `tasks.md` is ticked (128 `- [x]`, no open box). None is blocked or partial. `git diff 0a25cca..HEAD -- src` is empty: the second fix pass, like the first, changed tests, fixtures and the spec only.

---

## Spec-Anchored Acceptance Criteria

Every line number below was located again in this pass, in `tests/test_overlap.py` at `a11b13e` (863 lines, 88 tests). Each fixture a criterion names was read against it: positions, sizes, roles, `z-index` values and document order in `overlap-bug.html`, `overlap-clean.html`, `overlap-bounds.html`, `overlap-order.html`, `overlap-many.html`, `overlap-scrolled.html`, `overlap-scrolled-on-load.html`, `overlap-sampled.html` and `overlap-exact.html` are the ones the criteria state, and the pixel counts in their comments add up (55,180 in the bounds fixture, 26,610 in the sampled one, 1000 in the exact one).

### P1: Report text that another element covers

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-01 one Finding per covered element | exactly one Finding each | `tests/test_overlap.py:58-63` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements, `finding["check"] == "overlap"`, `len(findings) == 4`; `O:407-446` pins the sorted list of the 34 selectors of the bounds fixture, so a second Finding on one element fails | ✅ PASS as asserted; pages no fixture holds fall short of it ("Gaps in `src/` and in the spec text", 2 and 3) |
| OVL-02 the four Findings of the bug fixture, in order | `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)`, `(#collision, minor, 20, #stray)` | `O:69-76` - `covered(findings) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-03 summary line | first block, `Found 4 findings in 1 viewport: 2 major, 2 minor.` | `O:82-83` - `texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."`; that the first block is the text block is held by `tests/test_detect_visual_bugs.py:263` | ✅ PASS |
| OVL-04 same call, same content | equal structured content | `O:87` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| OVL-05 text under the text of another element | one Finding, `hiddenPercent` 20 | `O:93-94` - `finding_on` unpacks exactly one; `["hiddenPercent"] == 20` | ✅ PASS |
| OVL-06 the text on top | no Finding for `#stray` | `O:98-99` - `await findings_on(client, BUG, "#stray", findings) == []` | ✅ PASS |
| OVL-07, OVL-08, OVL-09 `#left`, `#top`, `#bottom`, exactly 10% | one Finding each, 10 | `O:449-454` - parametrized over the three, `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-10 `#three-lines`, middle box | one Finding, 10 | `O:458-459` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-11 `#split`, second text node | one Finding, 10 | `O:463-464` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-12 `#veil-55` | one Finding, 100, `major` | `O:468-470` - `["hiddenPercent"] == 100`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-13 text and cover in one shadow tree | 50, `coveredBy` `[data-testid="shadow-cover"]` | `O:476-480` - `finding["evidence"]["measured"] == {"hiddenPercent": 50, "coveredBy": SHADOW_COVER}` | ✅ PASS |
| OVL-14 `#narrow`, one viewport only | one Finding at 390 × 844, none at 1440 × 900 | `O:105-110` - `... DESKTOP) == []`, `(finding,) = ... MOBILE)`, `finding["viewport"] == MOBILE` | ✅ PASS |
| OVL-15 `#in-dialog` | one Finding, `major` | `O:486` - `(await bounds(client, "#in-dialog"))["severity"] == "major"` | ✅ PASS |
| OVL-16 `#in-fixed` | one Finding, `major` | `O:492` - `(await bounds(client, "#in-fixed"))["severity"] == "major"` | ✅ PASS |
| OVL-17 `low-contrast-bounds.html` | exactly one Finding, `#covered`, 100, `major` | `O:741-745` - `(finding,) = ...["findings"]`, `finding["selector"] == "#covered"`, `["hiddenPercent"] == 100`, `["severity"] == "major"` | ✅ PASS |
| OVL-18 `low-contrast-reach.html` | exactly one Finding, `#veiled-most`, 100 | `O:751-754` - `(finding,) = ...`, `finding["selector"] == "#veiled-most"`, `["hiddenPercent"] == 100` | ✅ PASS |
| OVL-71 a list of several roles | one Finding, 50, `#role-list`, `major` | `O:605-610` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#role-list"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-75 `#opacity-60` | one Finding, 50 | `O:617-618` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-76 two measured texts over each other | `#under-label` 50 by `#label`; `#label` 50 by `#label-cover` | `O:627-636` - both `["measured"] == {...}` dicts, the values of the spec | ✅ PASS |
| OVL-78 `#speck`, all its Hidden ink off the sample | one Finding, 10, `minor`, `#speck-cover` | `O:818-823` - `["measured"] == {"hiddenPercent": 10, "coveredBy": "#speck-cover"}`, `finding["severity"] == "minor"` | ✅ PASS. Its wording changed in this fix pass (25,010 to 26,610 pixels on the page, which gained the row of OVL-84); its outcome did not |
| OVL-80 four texts stacked in one place | four Findings, all `major`: `#stack-0`, `#stack-1`, `#stack-2` at 80 by `#stack-3`; `#stack-3` at 25 by `#stack-cover` | `O:645-656` - `covered(stack) == [("#stack-0", "major", 80, "#stack-3"), ("#stack-1", "major", 80, "#stack-3"), ("#stack-2", "major", 80, "#stack-3"), ("#stack-3", "major", 25, "#stack-cover")]` | ✅ PASS |
| OVL-81 `#shifted`, a column of its own | one Finding, 10, `minor` | `O:664` - `share_and_severity(await bounds(client, "#shifted")) == (10, "minor")` | ✅ PASS |
| OVL-82 the box of a tag whose glyphs stand beside the text | `#under-tag` 50 by `#tag`; `#tag` 50 by `#tag-cover` | `O:673-682` - both `["measured"] == {...}` dicts, the values of the spec | ✅ PASS |
| OVL-83 `#around`, own text around a child with text | one Finding, 10, `minor` | `O:690` - `share_and_severity(await bounds(client, "#around")) == (10, "minor")`; that the `b` gets none is held by the pinned list, `O:411-446` | ✅ PASS |
| OVL-87 `#translucent`, glyphs of alpha 0.5 | one Finding, 50 | `O:698-699` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-89 `#filled`, transparent `color`, opaque fill | one Finding, 50 | `O:707-708` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-90 a Silent layer that is not painted | one Finding, 50, `#plain-cover`, `major` | `O:717-722` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#plain-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-86 a page scrolled when it is captured | exactly one Finding, `#far`, 50, `major`, `#far-cover` | `O:809-810` - `covered(findings) == [("#far", "major", 50, "#far-cover")]` | ✅ PASS |

### P1: Stay silent on overlaps that are meant

`clean(client, selector)` (`O:208-214`) returns the share of the element's box painted in the colour of the covers, read through `inspect_element`, and the Findings on that box. The first value proves the fixture really paints the cover over the text; the second is the criterion.

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-19 the clean fixture, all Checks | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `O:200-205` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| OVL-20 `#stretched` | no Finding | `O:222` - `await clean(client, "#stretched") == (0, [])` | ✅ PASS |
| OVL-21 `#under-faded` | no Finding | `O:227` - `== (0, [])` | ✅ PASS |
| OVL-22 `#veil-45` | no Finding | `O:234-235` - `painted(...)["#737373"] == 0.6`, `await clean(client, "#veil-45") == (0, [])` | ✅ PASS |
| OVL-23 the five roles | no Finding for each | `O:238-245` - parametrized over `menu`, `listbox`, `tooltip`, `dialog`, `alertdialog`: `await clean(client, f"#under-{role}") == (0.5, [])` | ✅ PASS |
| OVL-24 `dialog[open]` | no Finding | `O:252` - `== (0.5, [])` | ✅ PASS |
| OVL-25 open popover, `position: absolute` | no Finding | `O:258` - `== (0.5, [])` | ✅ PASS |
| OVL-26 `position: fixed` | no Finding | `O:263` - `== (0.5, [])` | ✅ PASS |
| OVL-27 `position: sticky` | no Finding | `O:268` - `== (0.5, [])` | ✅ PASS |
| OVL-28 descendant of a `menu` | no Finding | `O:276` - `== (0.5, [])` | ✅ PASS |
| OVL-29 static child of a fixed element | no Finding | `O:284` - `== (0.5, [])` | ✅ PASS |
| OVL-30 shadow tree of a `menu` host | no Finding | `O:500-503` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []` | ✅ PASS |
| OVL-31 `#nick`, 9.5% along the width | no Finding | `O:291` - `== (0.095, [])` | ✅ PASS |
| OVL-32 `#skim`, 5% along the height | no Finding | `O:299` - `== (0.2, [])` | ✅ PASS |
| OVL-33 `#parent-text`, under its own child | no Finding | `O:304` - `== (0.5, [])` | ✅ PASS |
| OVL-34 `#under-ghost`, `pointer-events: none` | no Finding | `O:312` - `== (0.5, [])` | ✅ PASS |
| OVL-35 `#caption` over `#picture` | no Finding for either | `O:321-324` - `painted(...)["#000000"] == 0.24`, both `findings_on(...) == []` | ✅ PASS |
| OVL-36 `#badge` on `#inbox` | no Finding | `O:332` - `== (0.0533, [])` | ✅ PASS |
| OVL-37 `visibility: hidden` | no Finding | `O:337` - `== (0.5, [])` | ✅ PASS |
| OVL-38 `color: transparent` | no Finding | `O:345` - `== (0.5, [])` | ✅ PASS on its fixture; ❌ the rule it states does not hold for a colour of alpha 0 that Chromium does not compute to `rgb()` ("Gaps in `src/` and in the spec text", 1) |
| OVL-39 `opacity: 0` | no Finding | `O:350` - `== (0.5, [])` | ✅ PASS |
| OVL-70 a role with spaces and a capital | no Finding | `O:358` - `await clean(client, "#under-spaced-role") == (0.5, [])` | ✅ PASS |
| OVL-72 under what an ancestor paints | no Finding | `O:366` - `await clean(client, "#under-own-row") == (0.5, [])` | ✅ PASS |
| OVL-73 hit testing gives a descendant | no Finding | `O:375` - `await clean(client, "#own-link-text") == (0.5, [])` | ✅ PASS |
| OVL-74 `#opacity-40` | no Finding | `O:382` - `await clean(client, "#opacity-40") == (0.5, [])` | ✅ PASS |
| OVL-88 opaque `color`, transparent fill | no Finding | `O:390` - `await clean(client, "#transparent-fill") == (0.5, [])` | ✅ PASS |
| OVL-91 closed menus | no Finding, and nothing painted over the text | `O:393-399` - parametrized over `#under-removed-menu` and `#under-hidden-menu`: `await clean(client, selector) == (0, [])`, the `0` being the share of the box in the colour of the covers | ✅ PASS |

### P1: Severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-40 25% is `major`, 24.5% is `minor` | `#quarter` `major`, `#almost-quarter` `minor` | `O:509-513` - `quarter[...]["hiddenPercent"] == 25`, `quarter["severity"] == "major"`, `almost["severity"] == "minor"` | ✅ PASS |
| OVL-41 `#layered-half` | `minor` | `O:530` - `share_and_severity(...) == (50, "minor")` | ✅ PASS |
| OVL-42 `#layered-corner` | `info` | `O:536` - `== (10, "info")` | ✅ PASS |
| OVL-43 `#layer-ancestor` | `minor` | `O:542-544` - `["coveredBy"] == "#layer-cover"`, `== (50, "minor")` | ✅ PASS |
| OVL-44 `#shared-layer` | `major` | `O:550` - `== (50, "major")` | ✅ PASS |
| OVL-45 `#z-zero` | `major` | `O:554` - `== (50, "major")` | ✅ PASS |
| OVL-46 `#z-static` | `major` | `O:560-562` - `["coveredBy"] == "#z-static-next"`, `== (50, "major")` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-47 the Finding of `#half` | the literal of the spec | `O:116-133` - `findings[0] == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| OVL-48 message at 10% | `10% of the text is covered by another element` | `O:137-139` - `["hiddenPercent"] == 10`, `finding["message"] == "10% of the text is covered by another element"` | ✅ PASS |
| OVL-49 truncation | 24 for 24.5% | `O:518-520` - `["hiddenPercent"] == 24`, `finding["message"] == "24% of the text is covered by another element"` | ✅ PASS |
| OVL-50 `#mixed` | 20, `#mixed-card`, `minor` | `O:569-574` - `["measured"] == {"hiddenPercent": 20, "coveredBy": "#mixed-card"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-51 `#two-covers` | 60, `#large-cover` | `O:581-585` - `["measured"] == {"hiddenPercent": 60, "coveredBy": "#large-cover"}` | ✅ PASS |
| OVL-52 `#tie` | 40, `#tie-first` | `O:593-597` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#tie-first"}` | ✅ PASS |
| OVL-53 both selectors work in `inspect_element` | `isError: false`, same `box` for `selector` | `O:728-735` - for the 4 Findings of the bug fixture and the 34 of the bounds fixture (`len(findings) == count`): `inspected["box"] == finding["box"]`, and `inspect` (`O:186`, `result.is_error is False`) on `coveredBy` | ✅ PASS |
| OVL-77 an element the scroll brings over a text | exactly one Finding, `#far`, 50, `#far-cover` | `O:796-801` - `(finding,) = ...["findings"]`, `finding["selector"] == "#far"`, `["measured"] == {"hiddenPercent": 50, "coveredBy": "#far-cover"}` | ✅ PASS |
| OVL-79 the Coverer of a sample | the fifteen tuples in order, `#striped` covered by `#solid-cover` | `O:831-840` - `covered(findings) == [("#striped", "major", 25, "#solid-cover"), ("#row-striped", "major", 40, "#row-solid-cover"), *fillers 0 to 11, ("#speck", "minor", 10, "#speck-cover")]` | ✅ PASS. Its list gained the tuple of OVL-84 in this fix pass and lost none: the outcome is tighter, not looser |
| OVL-84 the rows of a sample | `#row-striped`: 40, `major`, `#row-solid-cover` | `O:849-854` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#row-solid-cover"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-85 a page under the cap | exactly one Finding, `#striped`, 25, `major`, `#stripes` | `O:862-863` - `covered(findings) == [("#striped", "major", 25, "#stripes")]` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-54 four Checks by default | `overlap` runs with the other three | `O:143-149` - the four `(selector, "overlap")` pairs on a call without `checks`; `O:769-776` - `low-contrast-real` and `overlap` in one default call; the default run of the other two is held by their own modules, which pass | ✅ PASS |
| OVL-55 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `tests/test_detect_visual_bugs.py:340-344` - the literal `in text`; the same literal at `D:351-355`, `D:362-366` (`zzz`) and `D:374-378` | ✅ PASS |
| OVL-56 the other three Checks on the bug fixture | `[]` | `O:153-154` - `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| OVL-57 order across Checks | `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)` | `O:769-776` - `{severity} == {"minor"}`, the four pairs in order | ✅ PASS |
| OVL-58 the description names `overlap` | names it and says what it reports | `O:157-163` - `` "`overlap` (text another element is painted over" in " ".join(tool.description.split()) `` | ✅ PASS |
| OVL-59 earlier tests unchanged | pass, only the four literals differ | by reading: `git diff --name-status 8aa017c..HEAD -- tests` lists nine new fixtures, the new `tests/test_overlap.py` and `tests/test_detect_visual_bugs.py`, whose diff since `eb9778b` is the four `Valid checks:` literals (now at `D:342`, `D:353`, `D:364`, `D:376`) and nothing else; `helpers.py`, `conftest.py` and every earlier fixture and test module are untouched; the gate passes | ✅ PASS |
| OVL-60 a hundred covered texts | `isError: false`, 100 Findings | `O:780-788` - `result.is_error is False`, `len(findings) == 100`, and the 100 tuples `(#text-n, major, 50, #cover-n)` | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| Criterion | Evidence | Result |
| --------- | -------- | ------ |
| OVL-61 one module, one function, registered | `src/squint_mcp/checks/overlap.py:85` - `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:23` - `"overlap": overlap.check` | ✅ PASS |
| OVL-62 no `playwright` in the Checks or in `vision.py` | `grep -rn playwright src/squint_mcp/checks src/squint_mcp/vision.py src/squint_mcp/covered.py` finds nothing (exit 1) | ✅ PASS |
| OVL-63 thresholds and roles in `config`, each cited | `src/squint_mcp/config.py:129` `OVERLAP_MIN_HIDDEN_PERCENT = 10` ("Squint default", with the reason, `:126-128`); `:133` `OVERLAP_MAJOR_HIDDEN_PERCENT = 25` ("Squint default", `:131-132`); `:138` `SILENT_LAYER_ROLES` ("WAI-ARIA 1.2", `:135-137`) | ✅ PASS |
| OVL-64 no literal of them in the Check | `src/squint_mcp/checks/overlap.py:46` and `:59` read both thresholds from `config`; no role name appears in the file. The numbers left are the `* 100` of a percentage (`:46`, `:59`, `:66`) and `== 0` for alpha and ink (`:31`, `:40`) | ✅ PASS |
| OVL-65 CHANGELOG | `CHANGELOG.md:12`, under `## [Unreleased]` (`:7`): the Check, 10% and 25%, one level lower under a raised layer, and what is not reported: declared layers, `fixed` and `sticky`, covers that paint nothing | ✅ PASS |
| OVL-66 README | `README.md:45` - "`detect_visual_bugs` runs four Checks: ... and `overlap` (...)" | ✅ PASS |
| OVL-67 roadmap `concluída` | Pending by design: a closing step after a PASS. `docs/ROADMAP.md:110` says `pendente`, which is right today | ⏳ Pending the verdict |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-68 two viewports | each Finding of the first has one in the second | `O:169-179` - `len(desktop) == 4`, `desktop <= mobile` over `(selector, check)` | ✅ PASS |
| OVL-69 `text-clipped-clean.html` | `[]` | `O:762-763` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |

**Status**: 90 of 90 criteria due now have an assertion on the outcome the spec defines, and every one passes; OVL-67 waits for the verdict. ❌ One rule a criterion states does not hold on a page no fixture has (OVL-38, below). ⚠️ 3 spec-precision gaps flagged. ❌ Gaps present in the sensor (below).

### The twelve new criteria, read critically

Each was checked for two things: that it states a rule the Terms or the Assumptions already held, and that its fixture makes the outcome depend on that rule alone. The geometry of each was worked out again from the fixture.

| Criterion | The rule it states | Its fixture | Verdict |
| --------- | ------------------ | ----------- | ------- |
| OVL-80 | Terms, "Text ink" and "Hidden ink": each text is measured with nothing outside it painted, however many texts share the place | `#stack-0` at 40px to 240px and three more, each 40px further right and painted over the one before. Of `#stack-0`, 80px to 240px are hidden: 160 of 200 columns, 80%; `#stack-1` is on top of 40 of them, `#stack-2` of 40 and `#stack-3` of 80. `#stack-3` loses its last 50px to the cover: 25% | Faithful. The fourth text is the first of any fixture in a second round, and the third the first on the third channel |
| OVL-81 | The same: a share does not depend on where on the page the text starts | `#shifted` from 300px to 500px, its cover over 480px to 500px: 10% | Faithful. It shares a screenshot with texts that start at 40px, which is what makes the column matter |
| OVL-82 | Terms, "Text ink": "when nothing outside the element is painted over it" | `#tag`, a box from 140px to 280px with its glyphs at 240px to 280px, over the last 100px of `#under-tag`; `#tag-cover` over the second glyph | Faithful, for a tag that stands after the text in the document. The other order has no outcome: mutant V7 |
| OVL-83 | Terms, "Own text" | `#around`: 5 glyphs, a `b` of 10, 5 glyphs; the cover over its last 20px is 400 of the 4000 pixels that are its own, and would be 400 of 8000 with the child's | Faithful |
| OVL-87 | Assumptions, "Text hidden on purpose": a glyph colour "with alpha 0" | `color: rgba(0, 0, 0, 0.5)`, half covered | Faithful |
| OVL-88, OVL-89 | The same row: the colour that paints the glyphs is the fill colour | `color` opaque with a transparent fill, and the reverse | Faithful; both sides |
| OVL-90 | Terms, "Hidden ink": "if ... only its Silent layers were painted": one that is not painted hides nothing | `#closed-menu`, `role="menu"` and `visibility: hidden`, over the half `#plain-cover` hides | Faithful. It is the test that kills N11 |
| OVL-91 | Goals: the clean fixture holds "closed and open menus" | A menu of `display: none` and one of `visibility: hidden`, each placed over half of a text | Faithful, and weak: nothing is painted and hit testing never gives a hidden element, so it is hard to break. N11, the mutant it was written next to, passes it (`1 failed, 2 passed`: the two cases of this criterion), and so does every survivor of this pass. It holds the Goal, not a rule; OVL-90 holds the rule |
| OVL-84 | Terms, "Coverer": "every nth pixel of every nth row" | `#row-stripes` on the odd rows of the page over 120px: 10 rows of 120 columns, 1200 pixels, none tested; `#row-solid-cover`, 400 | Faithful |
| OVL-85 | Terms, "Coverer": "When a Capture has more than 20,000 pixels" | The row of `#striped` alone: 1000 pixels, all tested, 600 under `#stripes` | Faithful. The cap is pinned from both sides, at 1000 and at 26,610 pixels; how n grows past 2 is not (mutant V16) |
| OVL-86 | OVL-01 on a page that is not at its top when it is captured | A script of the page scrolls 900px while it loads | Faithful, for a scroll down. A scroll sideways has no outcome: mutant V17 |

### The two edits of existing spec text

**The sentence added to "Coverer"** ("The Hidden ink to test is that of the elements whose Hidden share is at least 10%, those that get no Finding included; an element under that share is not hit tested and its Hidden ink does not count") says what the code does: `src/squint_mcp/capture.py:212` hit tests a text when `hidden * 100 >= OVERLAP_MIN_HIDDEN_PERCENT * ink`, whatever the Check later makes of it, and `:219` sums the Hidden ink of those texts alone. It closes spec-precision gap 1 of the second pass. It has no criterion: mutant N14, which the second pass could not call a gap, now is one (sensor section).

**The row added to Out of Scope** (a pseudo-element of another measured text) does not describe exactly the case the code misses. Probes `q4-pseudo`, `q4b-pseudo-covered` and `q4c-pseudo-nick` (this pass's own pages for what the second report called `p2c` and `p2b`) give what the row says: the text is reported while the element that paints the pseudo-element is seen, missed once at least 10% of that element's own text is unseen, and reported again with 2.5% unseen. Two more probes give a miss the row does not cover:

- `q4d-pseudo-inner`: the pseudo-element is painted by a child, without own text, of an element whose own text is half covered. The row asks that the element that paints it "has own text". The text under it gets no Finding.
- `q4f-pseudo-gap`: the element that paints the pseudo-element has all of its own text seen, and a glyph of a third text shows in the gap between two of its glyphs. The row says "with less than 10% of that own text unseen, the text is reported". It is not: the tool returns no Finding at all.

Both follow from how the code decides: the text is missed whenever the element around the pseudo-element is measured in the same screenshot, and phase 1 keeps an element for measuring when at least 10% of its ink is unseen or when glyphs of another text stand inside its own-text boxes (`src/squint_mcp/covered.py:216-227`), with what is inside it painted too (`src/squint_mcp/js/covered_text.js:227`). The row is spec-precision gap 1 below.

### Gaps in `src/` and in the spec text

Found by probing unmutated code through the MCP boundary on pages of this pass (the sensor section says how the probes were run).

1. ❌ **A glyph colour of alpha 0 that Chromium does not compute to `rgb()` is reported (OVL-38; Assumptions, "Text hidden on purpose").** On probe `q15-alpha0` a text of `color: oklch(0 0 0 / 0)`, half covered, gets `(#oklch, major, 50, #oklch-cover)`; the same text with `color: rgb(0 0 0 / 0%)` gets none. `src/squint_mcp/checks/overlap.py:25-31` reads the alpha from `rgba(r, g, b, a)` alone, and `inspect_element` shows Chromium computes the first colour to `oklch(0 0 0 / 0)`. Probe `q20-color-mix` gives the same false Finding for `color-mix(in oklab, rgb(0 0 0) 0%, transparent)` (computed `oklab(0 0 0 / 0)`), for `color-mix(in srgb, rgb(0 0 0) 0%, transparent)` (computed `color(srgb 0 0 0 / 0)`) and for `color(display-p3 0 0 0 / 0)`. The criterion's condition is "painted with a colour of alpha 0", and its fixture is `color: transparent`. This is the first place in three passes where the code, unmutated, falls short of a rule a criterion states. It is a false Finding on text nobody is meant to see, and needs both conditions: text made transparent through a colour function other than `rgb()` (a `color-mix()` is how an opacity modifier of a utility framework is commonly written), and another element over a tenth of it.
2. ⚠️ **Spec-precision gap 1: the Out of Scope row for a pseudo-element** (above). By the Terms the text of `q4d-pseudo-inner` and of `q4f-pseudo-gap` has a Hidden share of 50% and a Coverer, so OVL-01 asks for a Finding, and no row of Out of Scope takes it back. One wider sentence closes it: the text is not reported when the element that shows the pseudo-element, the one that paints it or an element around that one, is itself measured.
3. ⚠️ **Spec-precision gap 2: a limit the design accepts and the spec does not list, again.** `.specs/features/overlap/design.md:263`: "An ancestor with `mix-blend-mode` or a `filter` ... The channels do not hold what the highlights painted: no Text ink, no Finding ... Known limit". On probe `q21-filter` a text half under a cover, in a row of `filter: grayscale(1)` or of `filter: invert(1)`, gets no Finding; the same row without the filter gets `(#plain, major, 50, #plain-cover)`. A filter on the text itself does the same (`q22-gradient`, `#own-filter`); one that keeps the colours, `drop-shadow`, does not (`#shadow` is reported). By the Terms such a text has Text ink, a Hidden share of 50% and a Coverer, so OVL-01 asks for a Finding. Out of Scope has no row for it and the CHANGELOG does not name it among what the Check does not report. The second pass flagged the same thing for the pseudo-element limit of `design.md:259`, and the fix pass listed that one limit and not this one. Of the gaps of this section it is the one a real page is most likely to meet: a filter that changes colours on a section, or `filter: invert(1)` on the root as a dark mode, leaves the Check silent on everything inside. It needs the maintainer's word: a row in Out of Scope and a line in the CHANGELOG, or a change to how ink is told apart.
4. ⚠️ **Spec-precision gap 3: where an `info` Finding stands.** `info` is first used by this slice (Assumptions, "Severity under a Raised layer"), the story of the severity criteria asks for "the likely intended ones last", and no criterion has an `info` Finding in an asserted order or in a summary line. Unmutated, probe `q13-info` gives the `minor` Finding before the `info` one, though it stands after it in the document, and `Found 2 findings in 1 viewport: 1 minor, 1 info.`: right. Mutant V13 shows nothing holds it.

Observations, not gaps:

- On probe `q15-child-and-nick` a text with its first 80px under its own child and its last 20px under an Other element is reported at 16%, not 10%: the share is of the 2400 pixels the element shows when it is painted alone, child included. That is what the Terms say ("when nothing outside the element is painted over it"); a reader who expects a share of all ten glyphs will be surprised.
- A heading painted with a gradient (`background-clip: text` and `-webkit-text-fill-color: transparent`) is never reported: probe `q22-gradient`, `#gradient`, half covered, gets no Finding. That is the rule as the Assumptions have it (a glyph colour of alpha 0 is "hidden on purpose"), and its reason, "not text a reader was meant to see", does not fit this text. For the maintainer to know, not a gap against the spec.
- Unmutated code gives the outcome of the Terms on every other probe of this pass: a Coverer that is not the raised one of two (`q1-raised`), a shadow host that paints the cover itself (`q2-host`), a text right of the viewport (`q3-wide`), a page scrolled sideways on load (`q18-scrolled-sideways`), a tag before its text in the document (`q7-tagfirst`), an open `details` (`q10-details`), a text half clipped away (`q17-clipped`) or half off the page (`q19-off-page`), a font with anti-aliased edges covered whole (`q6-font`: 100%), 49,000 hidden pixels (`q16-step`), and the sentence added to "Coverer" (`q14-totest`).
- `tests/test_overlap.py:83` reads the first text block, not the first block. `tests/test_detect_visual_bugs.py:263` holds that the two are the same.
- That `inspect_element` does not return `z-index` (Assumptions, "`evidence.computed`") is held by a test of slice 2: `tests/test_inspect_element.py:167-169`, `set(content["computed"]) == COMPUTED_PROPERTIES`.
- Not observable through the tool boundary, and not counted, as in the earlier passes: that covered text is measured only on request (time, not result), `_settle_layout` (Windows and the generic `monospace` font only), and where the page is left scrolled after hit testing (N7).
- The whole suite takes 756s here. `.specs/features/overlap/spike/` and its `extend-exclude` line in `pyproject.toml` are still there, as the closing step of `tasks.md` expects.

---

## Discrimination Sensor

Run in temporary git worktrees of `a11b13e` under the session's temp directory, outside the repository, each with its own `uv sync`. One mutant at a time per worktree, applied by a script that requires the replaced text to occur exactly once, restores the worktree with `git checkout -- .` and checks it clean after each. Each mutation was written by this Verifier from the description in the earlier report, not copied from an earlier script. A mutant expected to die was run against the test of its rule; "Test" is the test that failed, with what it reported. Every failure counted as a kill is an assertion on a value, read from the output; none is a timeout. A mutant with no test of its own was run against all of `tests/test_overlap.py` (88 tests) and, when that passed, against the four other modules that can reach the mutated code (`tests/test_detect_visual_bugs.py`, `test_low_contrast_real.py`, `test_text_clipped.py`, `test_offscreen_overflow.py`: 150 tests) before it was called a survivor.

### The eleven survivors of the second pass

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| N1b | `src/squint_mcp/covered.py:116` | a text is cut out of the screenshot of its group at the left of that screenshot (the column offset dropped) | ✅ Killed - `test_a_text_that_starts_at_a_column_of_its_own_is_measured_there`: no Finding on `#shifted` |
| N2 | `src/squint_mcp/capture.py:205` | a measured text is read on the page as the first round has it, whatever its own round | ✅ Killed - `test_four_texts_stacked_in_one_place_are_each_measured`: `#stack-3` at 100%, not 25% |
| N3 | `src/squint_mcp/js/covered_text.js:143` | the third highlight colour is black | ✅ Killed - the same test: no Finding on `#stack-1` or `#stack-2` |
| N5 | `src/squint_mcp/js/covered_text.js:253` | every row is hit tested: only the columns are sampled | ✅ Killed - `test_the_rows_of_the_page_are_sampled_as_its_columns_are`: `#row-stripes`, not `#row-solid-cover` |
| N8 | `src/squint_mcp/js/covered_text.js:16` | the scroll down the page when the Capture is taken is read as 0 | ✅ Killed - `test_a_page_that_is_scrolled_when_it_is_captured_is_measured`: no Finding |
| N9 | `src/squint_mcp/js/covered_text.js:101-106` | the region of a text is its own text only, without its box and what is inside it | ✅ Killed - `test_a_text_under_the_box_of_a_tag_whose_glyphs_stand_beside_it_is_measured`: no Finding on `#under-tag` |
| N10 | `src/squint_mcp/checks/overlap.py:31` | glyphs count as transparent at any alpha under 1 | ✅ Killed - `test_covered_text_painted_half_transparent_is_reported`: no Finding on `#translucent` |
| N11 | `src/squint_mcp/js/covered_text.js:152` | an element of `visibility: hidden` is shown with the others when a text is painted alone or with its Silent layers | ✅ Killed - `test_a_silent_layer_that_is_not_painted_hides_nothing`: no Finding on `#under-closed-menu`. Both cases of `test_text_under_a_closed_menu_is_not_reported` pass under it |
| N13 | `src/squint_mcp/covered.py:303` | the step is never under 2 | ✅ Killed - `test_every_hidden_pixel_of_a_page_under_the_cap_is_hit_tested`: `#solid-cover`, not `#stripes` |
| N22 | `src/squint_mcp/checks/overlap.py:30` | the alpha is read from `color`, not from `-webkit-text-fill-color` | ✅ Killed - `test_covered_text_of_an_opaque_colour_and_a_transparent_fill_is_not_reported` (a Finding on `#transparent-fill`, 50%, `major`) and `test_covered_text_of_a_transparent_colour_and_an_opaque_fill_is_reported` (no Finding on `#filled`) |
| N28 | `src/squint_mcp/covered.py:212` | phase 1 counts as ink of a text every glyph of its channel inside its bounds | ✅ Killed - `test_the_text_of_a_child_is_not_ink_of_the_element_around_it`: no Finding on `#around` |

**11/11 killed**, each by the test written for it.

### The mutants of earlier passes whose fixtures grew

| # | File:line | Mutation | Fixture that grew | Outcome |
| - | --------- | -------- | ----------------- | ------- |
| J10 | `src/squint_mcp/js/covered_text.js:259-262` | a text the step passes over whole is not tested | sampled | ✅ Still killed - `test_a_text_the_hit_test_step_passes_over_whole_still_names_its_cover`: no Finding on `#speck` |
| C8 | `src/squint_mcp/covered.py:303` | every hidden pixel is hit tested (no cap) | sampled | ✅ Still killed - `test_the_cover_named_is_the_one_over_most_of_the_pixels_hit_tested` (`#stripes`, not `#solid-cover`) and `test_the_rows_of_the_page_are_sampled_as_its_columns_are` (`#row-stripes`) |
| N6 | `src/squint_mcp/js/covered_text.js:254` | the columns of the sample are counted from the start of each run | sampled | ✅ Still killed - `test_the_cover_named_is_the_one_over_most_of_the_pixels_hit_tested`: `#stripes` |
| C5 | `src/squint_mcp/covered.py:242` | every measured text in one group | bounds | ✅ Still killed - `test_two_covered_texts_painted_over_each_other_are_each_measured`: `#under-label` at 28%, not 50% |
| C11 | `src/squint_mcp/capture.py:205` | a measured text is read on the first channel, whatever its own | bounds | ✅ Still killed - the same test: `#label` at 100%, not 50% |
| J8 | `src/squint_mcp/js/covered_text.js:171` | an element the scroll moved is not passed over | scrolled (unchanged; a second scrolled fixture was added) | ✅ Still killed - `test_an_element_the_scroll_brings_over_a_text_is_not_what_covers_it`: `#fixed-bar`, not `#far-cover` |

**6/6 still killed.** The bounds fixture went from 35,380 to 55,180 pixels of Hidden ink and stays at a step of 2; `#tie` and `#two-covers` keep their Coverer.

Four more mutants of the earlier passes whose kill rests on the two rows of the bounds fixture that a sample could tip, `#tie` and `#two-covers`, were run again too, since that fixture grew twice: A5 (on a tie, the last cover in the document), A11 (the first cover, whatever it hides), J17 (the covers not put in document order) and N18 (only the first run of each row sent to hit testing). All four are still killed, by `test_of_two_covers_that_hide_as_much_the_first_in_the_document_is_named` (`#tie-second`) or `test_the_cover_over_most_of_the_hidden_ink_is_the_one_named` (`#small-cover`). The other kills of the earlier passes were not run again.

Unmutated, a scratch worktree passes `tests/test_overlap.py`: 88 passed.

### A7, A8, N7 and N14, judged again

All four were applied again; all four pass `tests/test_overlap.py` and the four other modules.

| # | File:line | Mutation | Judgement of this pass |
| - | --------- | -------- | ---------------------- |
| A7 | `src/squint_mcp/checks/overlap.py:40` | the `ink == 0` guard dropped | ⚠️ Equivalent. `covered.hidden_ink` cuts Hidden ink out of Text ink (`src/squint_mcp/covered.py:269-274`), so no ink means none hidden; the Capture hit tests a text only `if hidden` (`src/squint_mcp/capture.py:212`), `covers` stays empty and `overlap.py:50` returns |
| A8 | `src/squint_mcp/checks/overlap.py:46` | the reporting threshold dropped from the Check | ⚠️ Equivalent. The Capture fills `covers` only at or over the same threshold, with the same expression and the same constant (`capture.py:212`); under it `overlap.py:50` returns |
| N7 | `src/squint_mcp/js/covered_text.js:293` | the scroll is not restored after hit testing | ⚠️ Equivalent. `hit` is called once, as the last thing `_measure_covered_text` does (`capture.py:220`); `capture` then reads nothing more of the page and closes its context (`capture.py:303-305`), and each viewport gets a new context and a new page (`capture.py:253-260`). Nothing reads where the page is left |
| N14 | `src/squint_mcp/capture.py:212` | every text with Hidden ink is hit tested, also under the reporting threshold | ❌ A gap now. The sentence added to "Coverer" says such a text "is not hit tested and its Hidden ink does not count". On probe `q14-totest` (19,000 pixels of Hidden ink in texts at or over a tenth, 1520 in four texts under it) the unmutated code names `#stripes`, as that sentence has it, and the mutant `#solid-cover`. The spec now defines the outcome and no test holds it |

### New mutations of this pass

None of these was tried in an earlier pass. They were chosen as the changes a careless edit would most plausibly make and as the rules of the Terms and the Assumptions that, by reading, had no criterion.

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| V1 | `src/squint_mcp/checks/overlap.py:63` | the severity is lowered when any cover is in a Raised layer, not when the Coverer is | ❌ Survived - `O` and the four other modules pass |
| V14 | `src/squint_mcp/checks/overlap.py:77` | `evidence.computed` is always `{"position": "static", "z-index": "auto"}` | ❌ Survived - `O` and the four other modules pass |
| V2 | `src/squint_mcp/js/covered_text.js:173` | a shadow host is not named when its tree gives nothing at the point (`?? i` dropped) | ⚠️ Survived - equivalent (below) |
| V3 | `src/squint_mcp/js/covered_text.js:282` | hit testing never scrolls the page sideways | ❌ Survived - `O` and the four other modules pass |
| V17 | `src/squint_mcp/js/covered_text.js:15` | the scroll across the page when the Capture is taken is read as 0 | ❌ Survived - `O` and the four other modules pass |
| V4 | `src/squint_mcp/js/covered_text.js:221` | the pseudo-elements of the texts stay painted in the glyphs-only screenshot of phase 1 | ❌ Survived - `O` and the four other modules pass |
| V5 | `src/squint_mcp/js/covered_text.js:218` | the background of the texts stays painted in that screenshot | ✅ Killed - `test_only_the_covered_texts_of_the_bounds_fixture_are_reported`: `#under-tag` missing |
| V10 | `src/squint_mcp/js/covered_text.js:55` | any element with an `open` attribute is a Silent layer, not a `dialog` only | ❌ Survived - `O` and the four other modules pass |
| V11 | `src/squint_mcp/js/covered_text.js:303` | only the ancestors of a cover can raise it, not the cover itself | ✅ Killed - `test_half_hidden_by_a_positioned_cover_with_a_z_index_is_minor`: `(50, "major")`, not `(50, "minor")` |
| V15 | `src/squint_mcp/js/covered_text.js:230` | a text is painted alone without what is inside it | ❌ Survived - `O` and the four other modules pass |
| V6 | `src/squint_mcp/covered.py:272` | Hidden ink is not cut to Text ink: every unseen pixel counts, also one with under half of its ink | ❌ Survived - `O` and the four other modules pass |
| V7 | `src/squint_mcp/covered.py:246` | two texts share a screenshot unless the later one's region touches the earlier one's text: the other direction is dropped | ❌ Survived - `O` and the four other modules pass |
| V16 | `src/squint_mcp/covered.py:303` | the step grows with the pixels, not with their square root | ❌ Survived - `O` and the four other modules pass |
| V8 | `src/squint_mcp/capture.py:219` | the step is taken from the text with the most Hidden ink, not from the sum | ✅ Killed - `test_the_cover_named_is_the_one_over_most_of_the_pixels_hit_tested`: `#stripes`, not `#solid-cover` |
| V9 | `src/squint_mcp/capture.py:198` | hit testing asks the page as phase 2 left it, not as it is painted | ✅ Killed - `test_each_covered_text_yields_one_finding`: no Finding |
| V12 | `src/squint_mcp/capture.py:296-302` | covered text is measured before the three layers of the other Checks are taken | ✅ Killed - `test_the_summary_counts_the_findings_of_the_bug_fixture`: 6 Findings, not 4 |
| V13 | `src/squint_mcp/tools/detect_visual_bugs.py:116` | an `info` Finding is ordered as a `minor` one | ❌ Survived - `O` and the four other modules pass. The line is of slice 3; `info` is first produced by this slice |

**Sensor depth**: expanded (42 mutants this pass: the 11 survivors of the second pass, 10 mutants of earlier passes run again, A7, A8, N7 and N14 judged again, and 17 new ones: 2 in the Check, 8 in the page script, 3 in the arithmetic, 3 in the Capture's wiring, 1 in the tool)
**Sensor outcome**: second-pass survivors 11/11 killed; mutants of regrown fixtures 6/6 still killed; new mutants 5/17 killed, 12 survived: 11 gaps and 1 equivalent (V2); N14, judged again, is a gap now: 12 gaps - ❌

### The survivors, decided by probes through the MCP boundary

Twenty-six probe pages were written for this pass, outside the repository and the worktrees, and called with the in-memory MCP client, as `tests/helpers.py` does, with `checks` equal to `["overlap"]` at 1440 × 900, unmutated and under each survivor. They use Ahem at 20px on rows 50px apart, as the fixtures do, unless the row says otherwise.

| Probe | The page | Unmutated | Mutant | Under the mutant |
| ----- | -------- | --------- | ------ | ---------------- |
| `q6-font` | Two lines of Arial at 16px: one wholly under a cover, one under a cover from 80px into it on | `(#full, major, 100, #full-cover)`, `(#part, major, 54, #part-cover)` | V6 | `#full` at 192%, `#part` at 108% |
| `q15-child-and-nick` | `#t`: its first 80px under its own child, its last 10px under `#nick`. `#u`: the same child, its last 20px under `#u-cover` | `(#u, minor, 16, #u-cover)` only | V15 | `(#t, major, 45, #nick)`, `(#u, major, 50, #u-cover)` |
| `q3-wide` | A page 3000px wide; a text 2000px from its left, half covered | `(#t, major, 50, #cover)` | V3 | no Finding |
| `q18-scrolled-sideways` | The same page, with a script that scrolls it 1500px sideways while it loads | `(#t, major, 50, #cover)` | V17 | no Finding |
| `q7-tagfirst` | The row of `#under-tag` of the bounds fixture with the tag first in the document | `(#tag, major, 50, #tag-cover)`, `(#under, major, 50, #tag)` | V7 | no Finding on `#under` |
| `q10-details` | A text half under a positioned `details` element with the `open` attribute | `(#t, major, 50, #details)` | V10 | no Finding |
| `q1-raised` | A text with `#small`, of `z-index: 1`, over its first 20px and `#large`, with no `z-index`, over its last 80px | `(#t, major, 50, #large)` | V1 | `minor` |
| `q13-info` | `#a`, with a cover of `z-index: 1` over its last 20px, then `#b`, with a plain cover over its last 20px | `(#b, minor, 10, #b-cover)`, `(#a, info, 10, #a-cover)`; `Found 2 findings in 1 viewport: 1 minor, 1 info.` | V13 | `#a` before `#b` |
| `q4-pseudo` | A text half under the `::after` of `#owner`, which has two glyphs of its own beside the text, all seen, and paints the pseudo-element outside its box | `(#below, major, 50, #owner)` | V4 | no Finding |
| `q14-own-styles` | A covered text of `position: relative` and `z-index: 1` | `evidence.computed` is `{"position": "relative", "z-index": "1"}` | V14 | `{"position": "static", "z-index": "auto"}` by construction |
| `q14-totest` | `#striped` with its stripes and its solid cover, nine texts half covered, and four texts with 100px under a menu and 19px under a card | `(#striped, major, 25, #stripes)` | N14 | `coveredBy` `#solid-cover` |
| `q16-step` | `#striped` with twenty-four texts half covered: 49,000 pixels of Hidden ink, a step of 2 | `(#striped, major, 25, #solid-cover)` | V16 | `coveredBy` `#stripes`, at a step of 3 |
| `q2-host` | A text half under a shadow host that paints the cover itself; its tree holds one `slot` | `(#t, major, 50, #host)` | V2 | the same |

**V2 is equivalent.** In Chromium `ShadowRoot.elementsFromPoint` answers with the elements of the document at the point as well as those of its own tree: asked directly on `q2-host`, the document and the shadow root of `#host` both answer `#host`, `#t`, the row, `body`, `html`. So the search inside a host always comes back to the host itself, which is not of that root and is returned (`covered_text.js:172-175`), and `?? i` has nothing to catch. The server launches no other browser.

**The gaps.** V1, V3, V4, V6, V7, V10, V13, V14, V15, V16, V17 and N14 each change what the tool returns on a page, and each page is a fixture a test through the MCP boundary can hold. Three have a wide reach: V6 overstates the share of every text in a real font (192% for 100% on the probe), V15 overstates the share of a text with a child painted over part of it as soon as another element touches that text, and V3 loses every Finding right of the viewport. V7, V10, V1 and V4 need a page built a certain way; V13 is the order of a result; V14, V16 and N14 change a detail of a Finding on a rare page. V13 mutates a line of an earlier slice, the sort of the tool: it is counted because this slice is the first to return an `info` Finding and its story asks for those last. The Fix Plans rank them.

**What the probes say of the code.** Unmutated, it gives on every probe of this table the outcome the Terms define. The survivors are behaviours the code has and no test holds, not defects. The three places where the code or the spec text itself falls short are in "Gaps in `src/` and in the spec text" above.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, apart from this report and the lessons store written afterwards. `HEAD` is `a11b13e` on `feat/overlap` both times, and `git worktree list` shows the main tree alone, as before. Nine worktrees were used: four for the batches of mutants and five added as the queue grew, for probes and for single mutants. A probe was never run in a worktree with a mutant applied by another run: the probe script refuses a worktree that is not clean. All nine were removed: `git worktree remove --force` dropped them from git and stopped on the long paths of their virtual environments, so the directories were then deleted by path and `git worktree prune` was run. `git stash` was not used. Two runner processes were stopped by the Verifier once only repeats of finished mutants (V10 and V13, already run to the end in other worktrees) were left in their queues; their worktrees were restored with `git checkout -- .` and checked clean, no result of an interrupted run is used, and no process of the sensor is left running.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ neither fix pass changes a file under `src/`; `inspect_element` and `ping` are untouched by the feature |
| No scope creep | ✅ the two changes that reach every Capture are the ones the spec puts in scope (AD-006, issue #18) |
| Matches patterns | ✅ one module per Check, thresholds in `config` with their source, the browser only in `capture.py`, tests through the tool |
| Spec-anchored outcome check (asserted values match spec) | ✅ for the 90 criteria due now |
| Per-layer Coverage Expectation met | ⚠️ every criterion has its assertion; the behaviours listed as gaps in the sensor section have none |
| Every test maps to a spec requirement - no unclaimed tests | ✅ the thirteen new tests map to OVL-80 to OVL-91 (OVL-91 has two cases) |
| Documented guidelines followed: `CONTRIBUTING.md` and `docs/SPEC.md`, Testing Decisions (one seam, real Chromium) | ✅ |

---

## Edge Cases

- [x] OVL-68: the Findings of 1440 × 900 are also those of 390 × 844 (`tests/test_overlap.py:169-179`)
- [x] OVL-69: an element behind the clipped part of a text does not cover it (`tests/test_overlap.py:762-763`)

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`, each command run with its own exit status recorded
- **Gate outcome**: pyright exit 0 (0 errors, 0 warnings); ruff check exit 0; ruff format --check exit 0 (104 files); pytest exit 0 - 325 passed, 0 failed, 0 skipped, in 756.14s
- **Test count before feature**: 237
- **Test count after the first pass**: 302
- **Test count after the second pass**: 312
- **Test count now**: 325
- **Delta**: +88 over the feature, all in `tests/test_overlap.py`; +13 in the second fix pass
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed or weakened. `git diff 0a25cca..HEAD -- tests/test_overlap.py` removes one line, the count of the bounds fixture, which goes from 23 to 34 with the eleven new Findings; the pinned list of selectors grows by the same eleven and the list of OVL-79 by one tuple. The fixtures that existed lose no case (`git diff 0a25cca..HEAD -- tests/fixtures` removes comment lines only). `tests/test_detect_visual_bugs.py` is untouched since `aef0799`, and the only assertions of the earlier slices that changed since `eb9778b` are the four `Valid checks:` literals OVL-55 supersedes

---

## Fix Plans

Ranked by how likely a real page is to meet the gap. Fixes 1, 4 and 12 need a decision of the maintainer and may change `src/` or the spec; the others are a fixture case, a criterion and a test each, with the code as it is. The probe pages named are described in the sensor section; each fix can start from its probe.

### Fix 1: Text under a filter that changes colours gets no Finding, and the spec does not say so

- **Root cause**: ink is told apart by the colour a highlight paints (`src/squint_mcp/js/covered_text.js:143`, `src/squint_mcp/covered.py:190-196`). A `filter` on the text or on an ancestor changes that colour, so the text has no ink in any layer. `design.md:263` accepts it; Out of Scope and the CHANGELOG do not list it.
- **Fix task**: the maintainer decides. Either a row in Out of Scope ("Known limit of this Check") and a line in the CHANGELOG, with a case in the clean fixture that holds the silence (a covered text in a row of `filter: grayscale(1)`); or a change to the Capture (the filters of the page switched off while ink is measured) and a case in the bounds fixture that holds the Finding.
- **Done when**: the spec and the code say the same of probe `q21-filter`, and a test holds it.
- **How likely**: likely. A grey-scaled section, a dimmed card, `filter: invert(1)` on the root as a dark mode. Every covered text inside is missed, silently.
- **Priority**: Major

### Fix 2: Hidden ink is not held inside Text ink on a font with anti-aliased edges (V6)

- **Root cause**: every fixture of the Check is in Ahem at whole pixels, where each pixel of a glyph has all of its ink or none. The pixels of a real glyph that have under half of their ink are not Text ink, and nothing shows that they are kept out of Hidden ink too.
- **Fix task**: a case with a text in a system font (`font-family: sans-serif`, 16px) wholly under an opaque cover; a criterion for one Finding with `hiddenPercent` equal to 100, which holds on any platform since every pixel of its Text ink is unseen.
- **Done when**: the test fails with the ink mask dropped at `covered.py:272` (192 on Windows with Arial).
- **How likely**: every page that is not a fixture. The code is right today; a change to `hidden_ink` could double every share and no test would fail.
- **Priority**: Major

### Fix 3: A text is measured with what is inside it (V15)

- **Root cause**: the one fixture with a child over its parent's text (`#parent-text`) has no Other element over that text, so the Finding is withheld by hit testing whether the child was painted with the text or not.
- **Fix task**: two cases from probe `q15-child-and-nick`. A text with a child over its first 80px and an Other element over its last 10px: no Finding. The same with the Other element over its last 20px: one Finding, `minor`, with `hiddenPercent` equal to 16 (400 of the 2400 pixels the element shows alone), covered by the Other element.
- **Done when**: both tests fail with `members.add(i)` for `add(i)` at `covered_text.js:230` (45%, `major`, and 50%, `major`).
- **How likely**: likely. A button or a tab with a badge or an icon positioned inside it is everywhere; the gap opens once anything else touches its text.
- **Priority**: Major

### Fix 4: A glyph colour of alpha 0 outside `rgb()` is reported (OVL-38)

- **Root cause**: `src/squint_mcp/checks/overlap.py:25-31` matches `rgb()` and `rgba()` only. Chromium computes `oklch()`, `oklab()`, `lab()`, `lch()`, `color()` and every `color-mix()` to another notation.
- **Fix task**: read the alpha of every notation Chromium computes a colour to (the newer ones write it after a slash, and it is 1 when there is none), with cases in the clean fixture for `color: oklch(0 0 0 / 0)` and `color: color-mix(in srgb, rgb(0 0 0) 0%, transparent)`, half covered: no Finding. Or, with the maintainer's word, a row in Out of Scope.
- **Done when**: probes `q15-alpha0` and `q20-color-mix` return no Finding and a test holds it.
- **How likely**: uncommon. It takes text made transparent through such a colour and a cover over a tenth of it. The harm is a false Finding.
- **Priority**: Minor

### Fix 5: Hit testing sideways (V3, V17)

- **Root cause**: both scrolled fixtures scroll down. No covered text of any fixture is right of the viewport, and no page is scrolled sideways when it is captured.
- **Fix task**: a page 3000px wide with a text 2000px from its left, half covered (`q3-wide`): one Finding, 50%, with its Coverer. The same page with a script that scrolls it 1500px sideways while it loads (`q18-scrolled-sideways`): the same Finding.
- **Done when**: the first test fails with `left: 0` at `covered_text.js:282`, the second with `startX` read as 0 at `covered_text.js:15`.
- **How likely**: now and then. A page wider than its viewport is what `offscreen-overflow` exists for, and what sticks out is often over something. A page scrolled sideways on load is rare.
- **Priority**: Major (every Finding right of the viewport is lost)

### Fix 6: A cover with text of its own that stands before the text in the document (V7)

- **Root cause**: OVL-82 has the tag after the text it covers. `groups` keeps two texts apart by two tests, one for each order, and the fixture needs only the first.
- **Fix task**: the row of `#under-tag` again with the tag first in the document (`q7-tagfirst`); a criterion for two Findings at 50%.
- **Done when**: the test fails with `or _crosses(other.region, text.bounds)` dropped at `covered.py:246` (no Finding on the text under the tag).
- **How likely**: now and then. A positioned label or badge written before the text it lands on is common; it must also have a tenth of its own text unseen.
- **Priority**: Minor

### Fix 7: An `open` attribute on an element that is not a `dialog` (V10)

- **Root cause**: OVL-24 holds the side that is silent. Nothing with `open` that is not a `dialog` covers a text in any fixture.
- **Fix task**: a text half under a positioned `details` element with `open` (`q10-details`): one Finding, 50%, `major`, covered by it.
- **Done when**: the test fails with the test of `localName` dropped at `covered_text.js:55`.
- **How likely**: now and then. A dropdown built on `details` and left open covers what is under it.
- **Priority**: Minor

### Fix 8: Two covers of which only the smaller is in a Raised layer (V1)

- **Root cause**: in every fixture with two covers over one text neither is raised. Assumptions, "Several elements cover one text": the Raised-layer rule reads the Coverer.
- **Fix task**: a text with a cover of `z-index: 1` over its first 20px and a plain one over its last 80px (`q1-raised`): one Finding, 50%, `major`, covered by the plain one.
- **Done when**: the test fails with `any(cover.raised for cover in covered.covers)` at `overlap.py:63` (`minor`).
- **How likely**: rare.
- **Priority**: Minor

### Fix 9: Where an `info` Finding stands (V13, spec-precision gap 3)

- **Root cause**: `info` is first used here and no criterion has one in an asserted order or in a summary line.
- **Fix task**: a criterion and a small fixture (`q13-info`): a text with a raised cover over its last 20px, then a text with a plain cover over its last 20px. `findings` in the order `minor`, `info`, and the first block equal to `Found 2 findings in 1 viewport: 1 minor, 1 info.`
- **Done when**: the test fails with `info` sorted as `minor` at `tools/detect_visual_bugs.py:116`.
- **How likely**: any page with a raised cover over under a quarter of a text. The code is right today and is of an earlier slice.
- **Priority**: Minor

### Fix 10: The pseudo-elements of a text in the glyphs-only screenshot (V4)

- **Root cause**: the Out of Scope row promises a Finding for a text under the pseudo-element of an element whose own text is seen. No fixture has a pseudo-element painted by an element with own text.
- **Fix task**: a text half under the `::after` of an element with two glyphs of its own beside it, all seen (`q4-pseudo`): one Finding, 50%, covered by that element.
- **Done when**: the test fails with the rule for `::before` and `::after` removed at `covered_text.js:221`.
- **How likely**: rare.
- **Priority**: Minor

### Fix 11: What the criteria leave of the sample and of the evidence (N14, V16, V14)

- **Root cause**: the sentence added to "Coverer" has no criterion; the two totals of the fixtures, 1000 and 26,610 pixels, give the same step under `n × n` and under `n`; `evidence.computed` is asserted on one element whose `position` and `z-index` are the defaults.
- **Fix task**: three cases. A page with 19,000 pixels of Hidden ink in texts at or over a tenth and 1520 in texts under it (`q14-totest`): the Coverer of `#striped` is `#stripes`. A page with 49,000 pixels (`q16-step`): the Coverer of `#striped` is `#solid-cover`. A covered text of `position: relative` and `z-index: 1`: `evidence.computed` equal to `{"position": "relative", "z-index": "1"}`.
- **Done when**: the tests fail with the bound dropped at `capture.py:212`, with the square root dropped at `covered.py:303`, and with the two values written as constants at `overlap.py:77`.
- **How likely**: rare. The first two change only which of two covers is named on a page within a few hundred pixels of a step of the sample.
- **Priority**: Minor

### Fix 12: The row of Out of Scope for a pseudo-element (spec-precision gap 1)

- **Root cause**: the row gives the condition of the probes that showed the limit, not the one the code decides on.
- **Fix task**: reword it: the text is not reported when the element that shows the pseudo-element (the one that paints it, or an element around that one) is itself measured, which is when at least 10% of its own text is unseen or glyphs of another text stand in its lines. Or give a text that shows a positioned pseudo-element a screenshot of its own, as the `ponytail:` comment of `covered.py:235-238` says.
- **Done when**: the row and probes `q4b-pseudo-covered`, `q4d-pseudo-inner` and `q4f-pseudo-gap` agree.
- **How likely**: rare.
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| OVL-01 | Implemented | ⚠️ Verified as asserted; Fix 1 and Fix 12 settle the pages where it is not met |
| OVL-02 to OVL-23, OVL-25 to OVL-32, OVL-34 to OVL-37, OVL-39 to OVL-46, OVL-48 to OVL-66, OVL-68 to OVL-81, OVL-83 to OVL-91 | Implemented | ✅ Verified |
| OVL-24 | Implemented | ⚠️ Verified as written; Fix 7 pins the other side |
| OVL-33 | Implemented | ⚠️ Verified as written; Fix 3 pins a child's cover next to another element's |
| OVL-38 | Implemented | ❌ Needs Fix (Fix 4): holds for `rgb()` and `rgba()` only |
| OVL-47 | Implemented | ⚠️ Verified as written; Fix 11 pins `evidence.computed` off its defaults |
| OVL-82 | Implemented | ⚠️ Verified as written; Fix 6 pins the other order of the document |
| OVL-67 | Pending | Pending the verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 90/90 criteria due now match the spec outcome on their fixtures; OVL-67 pending the verdict; 1 rule not met off its fixture (OVL-38); 3 spec-precision gaps
**Sensor**: second-pass survivors 11/11 killed; regrown fixtures 6/6 still killed; 17 new mutants, 5 killed, 12 survived: 11 gaps, 1 equivalent; N14 a gap now
**Gate**: 325 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: everything the earlier passes found working, and now four texts in one place, a text at a column of its own, a tag's box beside its glyphs, own text around a child's, the alpha and the property of the glyph colour, a Silent layer that is not painted, the rows of the sample, a page under the cap and a page scrolled down when it is captured. On the twenty-six probes of this pass the unmutated code gives the outcome of the Terms everywhere but in the three places below: among them a collision of two lines of a real font (`q23-real-collision`: 38% and 23%), a text half clipped away, a text half off the page, a text right of the viewport, and a real font covered whole at exactly 100%.

**What could have failed and did not**: the 21 earlier mutants run again (all killed), the reading of the twelve new criteria against their fixtures (all faithful), the two reworded criteria (neither looser), the test integrity check (nothing removed or weakened), and A7, A8 and N7 (still equivalent, for reasons re-derived from the code).

**Issues found**:

1. Text under a colour-changing `filter` gets no Finding; the design accepts it, the spec and the CHANGELOG do not say it (Fix 1, a decision).
2. A glyph colour of alpha 0 outside `rgb()` is reported, against the rule of OVL-38 (Fix 4, code or a decision).
3. Ten behaviours without a test (twelve surviving mutants), all correct in the code today (Fix 2, 3 and 5 to 11): Hidden ink inside Text ink on a real font, a text measured with what is inside it, hit testing sideways, a cover with text before its text in the document, `open` on an element that is not a `dialog`, a raised cover that is not the Coverer, the place of an `info` Finding, pseudo-elements in the glyphs-only screenshot, `evidence.computed` off its defaults, and two rules of the sample's size.
4. The Out of Scope row for a pseudo-element is narrower than what the code misses (Fix 12, wording).

**Next steps**: this was the last re-verification of the loop, so the decision is the maintainer's. Fix 1 and Fix 4 are the two that a user can meet today and need the maintainer's word either way. The rest can go one of two ways: route Fix 2, 3 and 5 to 11 to an implementer for one more round, asking this time for a fixture per side, per axis and per order of each rule rather than per mutant shown; or accept the feature with the residual this report lists and keep the list with it. OVL-67 stays pending until a PASS.
