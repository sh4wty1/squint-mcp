# overlap Validation

**Date**: 2026-10-11
**Spec**: `.specs/features/overlap/spec.md` (OVL-01 to OVL-79)
**Diff range**: `eb9778b..f5f190b` (19 commits, branch `feat/overlap`, base `8aa017c`); the fix pass is `aef0799..f5f190b`
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 2 (fix→re-verify iteration 1 of 3)

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

The fix pass did what it was asked: the eleven survivors of the first pass are all killed, each by the test written for it, and the ten new criteria are faithful statements of rules the Terms and the Assumptions already held. Every one of the 78 criteria due now has an assertion on the outcome the spec defines, the gate is green, and `git diff aef0799..HEAD -- src` is empty.

The verdict is FAIL because the sensor, pointed this time at what the first pass did not try, left survivors again, and the spec's third success criterion asks for none "in the Check, in what the Capture gains for it and in the rules of Silent and Raised layers". Of 21 new mutants, 8 were killed and 13 survived. One survivor is equivalent and one sits where the spec defines no outcome. The other eleven each give, on a probe page called through the MCP boundary, a result the Terms of the spec exclude, so each can be killed by a test through that boundary. They fall in six groups: more than three texts in one place, the place of a text in a screenshot it shares, the two untested sides of the hit-test sample, a page that is scrolled when it is captured, the colour that paints the glyphs, and a Silent layer that is not painted.

No defect was found in `src/` against a criterion. One probe shows the code short of OVL-01 on a page no fixture holds: a limit the design accepted (`.specs/features/overlap/design.md:259`) and the spec's Out of Scope does not list. It needs a decision, not a test.

OVL-67 (the roadmap) is a closing step that follows a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `O` = `tests/test_overlap.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## First pass

The first pass (the report committed at `aef0799`, in full in git) was FAIL: 68 of 68 criteria matched, the gate was green, and of 49 mutants 36 were killed and 13 survived, 2 of them equivalent (A7, A8) and 11 gaps. Four commits closed the gaps, with ten criteria, and none touched `src/`:

| First-pass gap | Mutant | Closed by | Criterion |
| -------------- | ------ | --------- | --------- |
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

This pass re-ran all eleven from the first report's descriptions: all eleven are killed (table in the sensor section). A7 and A8 were judged again and are equivalent.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T13 | ✅ Done | `89385b0` to `cb8d81b`, as in the first pass |
| F1: the reading of `role`, ancestors, descendants and faint text | ✅ Done | `7c32a5b` |
| F2: a list of roles, the bound of Text ink, two measured texts that cross | ✅ Done | `bb64438` |
| F3: an element the scroll moved | ✅ Done | `1e5d5ef` |
| F4: the sample of a capped Capture and the text its step passes over | ✅ Done | `f5f190b` |

All seventeen tasks are ticked in `tasks.md` (17 `- [x] Done`, no open box). None is blocked or partial.

---

## Spec-Anchored Acceptance Criteria

Every line number below was located again in this pass. Each fixture named by a criterion was read against it: positions, sizes, roles, `z-index` values and document order in `overlap-bug.html`, `overlap-clean.html`, `overlap-bounds.html`, `overlap-order.html`, `overlap-many.html`, `overlap-scrolled.html` and `overlap-sampled.html` are the ones the criteria state.

### P1: Report text that another element covers

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-01 one Finding per covered element | exactly one Finding each | `tests/test_overlap.py:57-61` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements, `finding["check"] == "overlap"`, `len(findings) == 4`; `O:391-416` pins the sorted list of the 23 selectors of the bounds fixture, so a second Finding on one element fails | ✅ PASS as asserted; see the limit under "Spec-precision gaps", 2 |
| OVL-02 the four Findings of the bug fixture, in order | `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)`, `(#collision, minor, 20, #stray)` | `O:67-74` - `covered(findings) == [...]`, the four tuples of the spec | ✅ PASS |
| OVL-03 summary line | first block, `Found 4 findings in 1 viewport: 2 major, 2 minor.` | `O:80-81` - `texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."`; that the first block is the text block is held by `tests/test_detect_visual_bugs.py:263` | ✅ PASS |
| OVL-04 same call, same content | equal structured content | `O:85` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| OVL-05 text under the text of another element | one Finding, `hiddenPercent` 20 | `O:91-92` - `finding_on` unpacks exactly one; `["hiddenPercent"] == 20` | ✅ PASS |
| OVL-06 the text on top | no Finding for `#stray` | `O:96-97` - `await findings_on(client, BUG, "#stray", findings) == []` | ✅ PASS |
| OVL-07 `#left`, exactly 10% | one Finding, 10 | `O:419-424` - parametrized, `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-08 `#top`, exactly 10% | one Finding, 10 | `O:419-424` | ✅ PASS |
| OVL-09 `#bottom`, exactly 10% | one Finding, 10 | `O:419-424` | ✅ PASS |
| OVL-10 `#three-lines`, middle box | one Finding, 10 | `O:428-429` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-11 `#split`, second text node | one Finding, 10 | `O:433-434` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-12 `#veil-55` | one Finding, 100, `major` | `O:438-440` - `["hiddenPercent"] == 100`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-13 text and cover in one shadow tree | 50, `coveredBy` `[data-testid="shadow-cover"]` | `O:446-450` - `finding["evidence"]["measured"] == {"hiddenPercent": 50, "coveredBy": SHADOW_COVER}` | ✅ PASS |
| OVL-14 `#narrow`, one viewport only | one Finding at 390 × 844, none at 1440 × 900 | `O:103-108` - `... DESKTOP) == []`, `(finding,) = ... MOBILE)`, `finding["viewport"] == MOBILE` | ✅ PASS |
| OVL-15 `#in-dialog` | one Finding, `major` | `O:456` - `(await bounds(client, "#in-dialog"))["severity"] == "major"` | ✅ PASS |
| OVL-16 `#in-fixed` | one Finding, `major` | `O:462` - `(await bounds(client, "#in-fixed"))["severity"] == "major"` | ✅ PASS |
| OVL-17 `low-contrast-bounds.html` | exactly one Finding, `#covered`, 100, `major` | `O:625-629` - `(finding,) = ...["findings"]`, `finding["selector"] == "#covered"`, `["hiddenPercent"] == 100`, `["severity"] == "major"` | ✅ PASS |
| OVL-18 `low-contrast-reach.html` | exactly one Finding, `#veiled-most`, 100 | `O:635-638` - `(finding,) = ...`, `finding["selector"] == "#veiled-most"`, `["hiddenPercent"] == 100` | ✅ PASS |
| OVL-71 a list of several roles | one Finding, 50, `#role-list`, `major` | `O:575-580` - `["measured"] == {"hiddenPercent": 50, "coveredBy": "#role-list"}`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-75 `#opacity-60` | one Finding, 50 | `O:587-588` - `["hiddenPercent"] == 50` | ✅ PASS |
| OVL-76 two measured texts over each other | `#under-label` 50 by `#label`; `#label` 50 by `#label-cover` | `O:597-606` - both `["measured"] == {...}` dicts, the values of the spec | ✅ PASS |
| OVL-78 `#speck`, all its Hidden ink off the sample | one Finding, 10, `minor`, `#speck-cover` | `O:693-698` - `["measured"] == {"hiddenPercent": 10, "coveredBy": "#speck-cover"}`, `finding["severity"] == "minor"` | ✅ PASS |

### P1: Stay silent on overlaps that are meant

`clean(client, selector)` (`O:206-212`) returns the share of the element's box painted in the colour of the covers, read through `inspect_element`, and the Findings on that box. The first value proves the fixture really paints the cover over the text; the second is the criterion.

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-19 the clean fixture, all Checks | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `O:198-203` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| OVL-20 `#stretched` | no Finding | `O:220` - `await clean(client, "#stretched") == (0, [])` | ✅ PASS |
| OVL-21 `#under-faded` | no Finding | `O:225` - `== (0, [])` | ✅ PASS |
| OVL-22 `#veil-45` | no Finding | `O:232-233` - `painted(...)["#737373"] == 0.6`, `await clean(client, "#veil-45") == (0, [])` | ✅ PASS |
| OVL-23 the five roles | no Finding for each | `O:236-243` - parametrized over `menu`, `listbox`, `tooltip`, `dialog`, `alertdialog`: `await clean(client, f"#under-{role}") == (0.5, [])` | ✅ PASS |
| OVL-24 `dialog[open]` | no Finding | `O:250` - `== (0.5, [])` | ✅ PASS |
| OVL-25 open popover, `position: absolute` | no Finding | `O:256` - `== (0.5, [])` | ✅ PASS |
| OVL-26 `position: fixed` | no Finding | `O:261` - `== (0.5, [])` | ✅ PASS |
| OVL-27 `position: sticky` | no Finding | `O:266` - `== (0.5, [])` | ✅ PASS |
| OVL-28 descendant of a `menu` | no Finding | `O:274` - `== (0.5, [])` | ✅ PASS |
| OVL-29 static child of a fixed element | no Finding | `O:282` - `== (0.5, [])` | ✅ PASS |
| OVL-30 shadow tree of a `menu` host | no Finding | `O:470-473` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []` | ✅ PASS |
| OVL-31 `#nick`, 9.5% along the width | no Finding | `O:289` - `== (0.095, [])` | ✅ PASS |
| OVL-32 `#skim`, 5% along the height | no Finding | `O:297` - `== (0.2, [])` | ✅ PASS |
| OVL-33 `#parent-text`, under its own child | no Finding | `O:302` - `== (0.5, [])` | ✅ PASS |
| OVL-34 `#under-ghost`, `pointer-events: none` | no Finding | `O:310` - `== (0.5, [])` | ✅ PASS |
| OVL-35 `#caption` over `#picture` | no Finding for either | `O:319-322` - `painted(...)["#000000"] == 0.24`, both `findings_on(...) == []` | ✅ PASS |
| OVL-36 `#badge` on `#inbox` | no Finding | `O:330` - `== (0.0533, [])` | ✅ PASS |
| OVL-37 `visibility: hidden` | no Finding | `O:335` - `== (0.5, [])` | ✅ PASS |
| OVL-38 `color: transparent` | no Finding | `O:343` - `== (0.5, [])` | ✅ PASS; ⚠️ only alpha 0 through `color` has an outcome (Fix 5) |
| OVL-39 `opacity: 0` | no Finding | `O:348` - `== (0.5, [])` | ✅ PASS |
| OVL-70 a role with spaces and a capital | no Finding | `O:356` - `await clean(client, "#under-spaced-role") == (0.5, [])` | ✅ PASS |
| OVL-72 under what an ancestor paints | no Finding | `O:364` - `await clean(client, "#under-own-row") == (0.5, [])` | ✅ PASS |
| OVL-73 hit testing gives a descendant | no Finding | `O:373` - `await clean(client, "#own-link-text") == (0.5, [])` | ✅ PASS |
| OVL-74 `#opacity-40` | no Finding | `O:380` - `await clean(client, "#opacity-40") == (0.5, [])` | ✅ PASS |

### P1: Severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-40 25% is `major`, 24.5% is `minor` | `#quarter` `major`, `#almost-quarter` `minor` | `O:479-483` - `quarter[...]["hiddenPercent"] == 25`, `quarter["severity"] == "major"`, `almost["severity"] == "minor"` | ✅ PASS |
| OVL-41 `#layered-half` | `minor` | `O:500` - `share_and_severity(...) == (50, "minor")` | ✅ PASS |
| OVL-42 `#layered-corner` | `info` | `O:506` - `== (10, "info")` | ✅ PASS |
| OVL-43 `#layer-ancestor` | `minor` | `O:512-514` - `["coveredBy"] == "#layer-cover"`, `== (50, "minor")` | ✅ PASS |
| OVL-44 `#shared-layer` | `major` | `O:520` - `== (50, "major")` | ✅ PASS |
| OVL-45 `#z-zero` | `major` | `O:524` - `== (50, "major")` | ✅ PASS |
| OVL-46 `#z-static` | `major` | `O:530-532` - `["coveredBy"] == "#z-static-next"`, `== (50, "major")` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-47 the Finding of `#half` | the literal of the spec | `O:114-131` - `findings[0] == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| OVL-48 message at 10% | `10% of the text is covered by another element` | `O:135-137` - `["hiddenPercent"] == 10`, `finding["message"] == "10% of the text is covered by another element"` | ✅ PASS |
| OVL-49 truncation | 24 for 24.5% | `O:488-490` - `["hiddenPercent"] == 24`, `finding["message"] == "24% of the text is covered by another element"` | ✅ PASS |
| OVL-50 `#mixed` | 20, `#mixed-card`, `minor` | `O:539-544` - `["measured"] == {"hiddenPercent": 20, "coveredBy": "#mixed-card"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-51 `#two-covers` | 60, `#large-cover` | `O:551-555` - `["measured"] == {"hiddenPercent": 60, "coveredBy": "#large-cover"}` | ✅ PASS |
| OVL-52 `#tie` | 40, `#tie-first` | `O:563-567` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#tie-first"}` | ✅ PASS |
| OVL-53 both selectors work in `inspect_element` | `isError: false`, same `box` for `selector` | `O:612-619` - for the 4 Findings of the bug fixture and the 23 of the bounds fixture (`len(findings) == count`): `inspected["box"] == finding["box"]`, and `inspect` (`O:184`, `result.is_error is False`) on `coveredBy` | ✅ PASS |
| OVL-77 an element the scroll brings over a text | exactly one Finding, `#far`, 50, `#far-cover` | `O:680-685` - `(finding,) = ...["findings"]`, `finding["selector"] == "#far"`, `["measured"] == {"hiddenPercent": 50, "coveredBy": "#far-cover"}` | ✅ PASS |
| OVL-79 the Coverer of a sample | the fourteen tuples in order, `#striped` covered by `#solid-cover` | `O:706-714` - `covered(findings) == [("#striped", "major", 25, "#solid-cover"), *fillers 0 to 11, ("#speck", "minor", 10, "#speck-cover")]` | ✅ PASS; ⚠️ the sample is pinned along the columns and over the cap only (Fix 3) |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-54 four Checks by default | `overlap` runs with the other three | `O:141-147` - the four `(selector, "overlap")` pairs on a call without `checks`; `O:653-660` - `low-contrast-real` and `overlap` in one default call; the default run of the other two is held by their own modules (`tests/test_offscreen_overflow.py:230`, `tests/test_text_clipped.py:16`), which pass | ✅ PASS |
| OVL-55 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `tests/test_detect_visual_bugs.py:340-344` - the literal `in text`; the same literal at `D:351-355`, `D:362-366` (`zzz`) and `D:374-378` | ✅ PASS |
| OVL-56 the other three Checks on the bug fixture | `[]` | `O:151-152` - `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| OVL-57 order across Checks | `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)` | `O:653-660` - `{severity} == {"minor"}`, the four pairs in order | ✅ PASS |
| OVL-58 the description names `overlap` | names it and says what it reports | `O:156-161` - `` "`overlap` (text another element is painted over" in " ".join(tool.description.split()) `` | ✅ PASS |
| OVL-59 earlier tests unchanged | pass, only the four literals differ | by reading: `git diff --name-status 8aa017c..HEAD -- tests` lists seven new fixtures, the new `tests/test_overlap.py` and `tests/test_detect_visual_bugs.py`, whose diff since `eb9778b` is the four `Valid checks:` literals and nothing else; `helpers.py`, `conftest.py` and every earlier fixture and test module are untouched; the gate passes | ✅ PASS |
| OVL-60 a hundred covered texts | `isError: false`, 100 Findings | `O:664-672` - `result.is_error is False`, `len(findings) == 100`, and the 100 tuples `(#text-n, major, 50, #cover-n)` | ✅ PASS |

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
| OVL-68 two viewports | each Finding of the first has one in the second | `O:167-177` - `len(desktop) == 4`, `desktop <= mobile` over `(selector, check)` | ✅ PASS |
| OVL-69 `text-clipped-clean.html` | `[]` | `O:646-647` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |

**Status**: 78 of 78 criteria due now are covered and match the spec-defined outcome; OVL-67 waits for the verdict. ⚠️ 2 spec-precision gaps flagged. ❌ Gaps present in the sensor (below).

### The ten new criteria, read critically

Each was checked for two things: that it states a rule the Terms or the Assumptions already held, and that its fixture makes the outcome depend on that rule alone.

| Criterion | The rule it states | Its fixture | Verdict |
| --------- | ------------------ | ----------- | ------- |
| OVL-70 | Assumptions, "The `role` attribute": compared in lower case and trimmed | `#spaced-role`, `role=" Menu "`, a plain cover with no `z-index`: silent by this rule only. Both the trim and the lower case are needed for it | Faithful |
| OVL-71 | The same row: a list of several roles is not a Silent layer | `#role-list`, `role="menu navigation"`: reported unless one role of a list counts | Faithful |
| OVL-72 | Terms, "Other element"; Out of Scope, "something an ancestor paints" | The `::after` of `#decorated-row`: hit testing gives the row, an ancestor. The row is hidden when the text is painted alone, so the text has Hidden ink and only the rule keeps it silent | Faithful |
| OVL-73 | Assumptions, "Hit testing gives no Other element at the Hidden ink" | `#own-link` stretched above `#linked-cover`: the ink is hidden by an Other element and hit testing gives a descendant | Faithful. The cover is real and goes unreported: that is the rule as the spec has it |
| OVL-74, OVL-75 | Terms, "Text ink": "faded below half by `opacity`" | `opacity` 0.4 and 0.6: ink of 102 and 153 around the bound of 128 | Faithful; both sides |
| OVL-76 | Terms, "Text ink": "when nothing outside the element is painted over it" | `#label` over `#under-label`, both with Hidden ink, their own-text boxes crossing | Faithful. It is also the first fixture with a measured text on the second channel: N4 and N12 below die on it |
| OVL-77 | Terms, "Coverer": "an element the scroll moved ... is passed over" | `#fixed-bar` comes over the Hidden ink of `#far` only once hit testing scrolls 900px | Faithful |
| OVL-78 | Terms, "Coverer": "each element at least once" | `#speck`: 10 hidden pixels, all on column 45; 25,010 hidden pixels on the page, so a step of 2 | Faithful |
| OVL-79 | Terms, "Coverer": "the largest part is then of that sample" | `#stripes` on the odd columns, 600 pixels, none tested; `#solid-cover`, 400 | Faithful for the columns of a page over the cap. The rows and a page under the cap have no outcome: N5 and N13 |

The sentence added to the Term "Coverer" ("counted from the origin of the page ...") says what `covered.hit_step` and `covered_text.js:253-254` do: for 25,010 pixels, 25,010 / 4 ≤ 20,000 and 25,010 / 1 is not, so n is 2.

### Spec-precision gaps

1. **Which Hidden ink is "to test" (Terms, "Coverer").** "When a Capture has more than 20,000 pixels of Hidden ink to test" does not say whose. The code counts the texts at or over the reporting threshold (`src/squint_mcp/capture.py:212`, `:219`). A Capture that also tested the texts under it would name another Coverer on a page built for it (mutant N14, probe `p9b`): both readings fit the sentence. One clause closes it.
2. **A limit the design accepts and the spec does not list.** `.specs/features/overlap/design.md:259`: "A pseudo-element of one text of a group, positioned over another text of the group ... a missed Finding. Accepted". On probe `p2b` a text is 50% under the `::after` of another element with own text; that other element has Hidden ink of its own. By the Terms the first text has 4000 pixels of Text ink, a Hidden share of 50% and a Coverer, so OVL-01 asks for a Finding. The tool returns none for it. With the second element uncovered (`p2c`) the Finding is there: `(#below, major, 50, #owner)`. The spec's Out of Scope has no row for this. Either a row is added, with the maintainer's word, or the code is changed.

Not observable through the tool boundary, and not counted as gaps, as in the first pass: that covered text is measured only on request (a matter of time, not of result), `_settle_layout` (Windows and the generic `monospace` font only), and where the page is left scrolled after hit testing (N7 below).

### Observations (not gaps)

- `O:81` reads the first text block, not the first block. `D:263` (`isinstance(result.content[0], TextContent)`) holds that the two are the same.
- No test of the first pass was removed or weakened. `git diff aef0799..HEAD -- tests/test_overlap.py` removes one line, the count of the bounds fixture, which goes from 19 to 23 with the four new Findings; the pinned list of selectors grows by the same four. `tests/test_detect_visual_bugs.py` is untouched since `aef0799`.
- The Goals of the spec name "closed and open menus" among what the clean fixture holds. It holds no closed menu (`visibility: hidden` or `display: none`). Fix 6 would add one.
- The whole suite takes 658s here. `.specs/features/overlap/spike/` and its `extend-exclude` line are still there, as the closing step of `tasks.md` expects.

---

## Discrimination Sensor

Run in four temporary git worktrees of `f5f190b` under the session's temp directory, outside the repository, each with its own `uv sync`. One mutant at a time per worktree, applied by a script that requires the replaced text to occur exactly once, restores the worktree with `git checkout -- .` and checks it clean after each. A mutant expected to die was run against the tests of its rule; "Test" is the test that failed, with what it reported. A survivor was run against all of `O` (75 tests) and then against the four other modules that can reach the mutated code (`D`, `test_low_contrast_real.py`, `test_text_clipped.py`, `test_offscreen_overflow.py`: 150 tests) before it was called one.

### The eleven survivors of the first pass

Each mutation was written again from the first report's description.

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| J4 | `src/squint_mcp/js/covered_text.js:54` | the `role` attribute compared as written, not trimmed or lowered | ✅ Killed - `test_text_under_a_role_written_with_spaces_and_a_capital_is_not_reported`: a Finding on `#under-spaced-role`, 50%, `major` |
| J5 | `src/squint_mcp/js/covered_text.js:54` | a list of roles is a Silent layer when one of them is | ✅ Killed - `test_text_under_an_element_with_a_list_of_roles_is_reported`: no Finding on `#under-role-list` |
| J6b | `src/squint_mcp/js/covered_text.js:290` | an ancestor of the text counts as an Other element | ✅ Killed - `test_text_under_what_one_of_its_ancestors_paints_is_not_reported`: a Finding on `#under-own-row`, 50%, `major` |
| J6c | `src/squint_mcp/js/covered_text.js:290` | a descendant of the text counts as an Other element | ✅ Killed - `test_text_whose_own_descendant_is_what_hit_testing_gives_is_not_reported`: a Finding on `#own-link-text`, 50% |
| J8 | `src/squint_mcp/js/covered_text.js:171` | an element the scroll moved is not passed over | ✅ Killed - `test_an_element_the_scroll_brings_over_a_text_is_not_what_covers_it`: `coveredBy` `#fixed-bar`, not `#far-cover` |
| J10 | `src/squint_mcp/js/covered_text.js:259` | a text the step passes over whole is not tested | ✅ Killed - `test_a_text_the_hit_test_step_passes_over_whole_still_names_its_cover`: no Finding on `#speck` |
| C2 | `src/squint_mcp/covered.py:23` | Text ink from any ink (`>= 1`) | ✅ Killed - `test_covered_text_faded_to_under_half_of_its_ink_is_not_reported`: a Finding on `#opacity-40`, 50%, `major` |
| C2b | `src/squint_mcp/covered.py:23` | Text ink from ink of 200 | ✅ Killed - `test_covered_text_that_keeps_over_half_of_its_ink_is_reported`: no Finding on `#opacity-60` |
| C5 | `src/squint_mcp/covered.py:242` | every measured text in one group | ✅ Killed - `test_two_covered_texts_painted_over_each_other_are_each_measured`: `#under-label` at 28%, not 50% |
| C11 | `src/squint_mcp/capture.py:205` | a measured text is read on the first channel, whatever its own | ✅ Killed - the same test: `#label` at 100%, not 50% |
| C8 | `src/squint_mcp/covered.py:303` | every hidden pixel is hit tested (no cap) | ✅ Killed - `test_the_cover_named_is_the_one_over_most_of_the_pixels_hit_tested`: `#striped` covered by `#stripes`, not `#solid-cover` |

**11/11 killed.**

### A7 and A8, judged again

Both were applied again and both survive `O` and the four other modules. Both are equivalent, for one reason: the Check repeats a guard the Capture already applies, and the Check has no input but a Capture.

| # | File:line | Mutation | Why no page can tell |
| - | --------- | -------- | -------------------- |
| A7 | `src/squint_mcp/checks/overlap.py:40` | the `ink == 0` guard dropped | Hidden ink is cut out of Text ink (`src/squint_mcp/covered.py:271-274`), so no ink means none hidden; the Capture then never hit tests the text (`src/squint_mcp/capture.py:212`, `if hidden and ...`), `covers` stays empty and `overlap.py:50` returns. The division of `overlap.py:66` is never reached |
| A8 | `src/squint_mcp/checks/overlap.py:46` | the reporting threshold dropped from the Check | The Capture fills `covers` only at or over the same threshold, with the same expression and the same constant (`src/squint_mcp/capture.py:212`); under it `overlap.py:50` returns. N14 below is the other half: with the Capture's bound dropped instead, the Check's bound gives the same Findings |

### New mutations of this pass

None of these was tried in the first pass.

| # | File:line | Mutation | Outcome |
| - | --------- | -------- | ------- |
| N1 | `src/squint_mcp/covered.py:116` | a text is cut out of the screenshot of its group at the top of that screenshot (the row offset dropped) | ✅ Killed - `test_only_the_covered_texts_of_the_bounds_fixture_are_reported`: `#three-lines` missing. The order test of the bug fixture passes under it: its four texts are of one shape |
| N1b | `src/squint_mcp/covered.py:116` | the same along the row (the column offset dropped) | ❌ Survived - `O` and the four other modules pass |
| N2 | `src/squint_mcp/capture.py:205` | a measured text is read on the page as the first round has it, whatever its own round | ❌ Survived - `O` and the four other modules pass |
| N3 | `src/squint_mcp/js/covered_text.js:143` | the third highlight colour is black: a text on the third channel has no ink | ❌ Survived - `O` and the four other modules pass |
| N4 | `src/squint_mcp/covered.py:29` | the green channel is read as painted, not times four | ✅ Killed - `test_two_covered_texts_painted_over_each_other_are_each_measured`: no Finding on `#label` |
| N5 | `src/squint_mcp/js/covered_text.js:253` | every row is hit tested: only the columns are sampled | ❌ Survived - `O` and the four other modules pass |
| N6 | `src/squint_mcp/js/covered_text.js:254` | the columns of the sample are counted from the start of each run, not from the origin of the page | ✅ Killed - `test_the_cover_named_is_the_one_over_most_of_the_pixels_hit_tested`: `#stripes`, not `#solid-cover` |
| N7 | `src/squint_mcp/js/covered_text.js:293` | the scroll is not restored after hit testing | ⚠️ Survived - equivalent (below) |
| N8 | `src/squint_mcp/js/covered_text.js:16` | the scroll of the page when the Capture is taken is read as 0 | ❌ Survived - `O` and the four other modules pass |
| N9 | `src/squint_mcp/js/covered_text.js:101-106` | the region of a text is its own text only, without its box and what is inside it | ❌ Survived - `O` and the four other modules pass |
| N10 | `src/squint_mcp/checks/overlap.py:31` | glyphs count as transparent at any alpha under 1 | ❌ Survived - `O` and the four other modules pass |
| N11 | `src/squint_mcp/js/covered_text.js:152` | an element of `visibility: hidden` is shown with the others when a text is painted alone or with its Silent layers | ❌ Survived - `O` and the four other modules pass |
| N12 | `src/squint_mcp/capture.py:190` | the texts of a group are not marked again on the first channel | ✅ Killed - `test_two_covered_texts_painted_over_each_other_are_each_measured`: no Finding on `#label` |
| N13 | `src/squint_mcp/covered.py:303` | the step is never under 2: a page under the cap is sampled too | ❌ Survived - `O` and the four other modules pass |
| N14 | `src/squint_mcp/capture.py:212` | every text with Hidden ink is hit tested, also under the reporting threshold | ⚠️ Survived - where the spec defines no outcome (spec-precision gap 1) |
| N16 | `src/squint_mcp/capture.py:215` | the runs sent to hit testing start at the top of the page, not of the text | ✅ Killed - `test_the_findings_say_how_much_is_hidden_and_by_what_in_order`: no Finding at all |
| N18 | `src/squint_mcp/covered.py:295` | only the first run of each row is sent to hit testing | ✅ Killed - `test_of_two_covers_that_hide_as_much_the_first_in_the_document_is_named`: `#tie-second`, not `#tie-first` |
| N20 | `src/squint_mcp/js/covered_text.js:60` | only `position: absolute` raises a layer | ✅ Killed - `test_a_cover_inside_a_positioned_element_with_a_z_index_is_one_level_lower`: `(50, "major")`, not `(50, "minor")` |
| N21 | `src/squint_mcp/tools/detect_visual_bugs.py:99` | covered text is asked for the first viewport only | ✅ Killed - `test_a_text_covered_at_one_viewport_only_is_reported_there`: no Finding on `#narrow` at 390 × 844 |
| N22 | `src/squint_mcp/checks/overlap.py:30` | the alpha is read from `color`, not from `-webkit-text-fill-color` | ❌ Survived - `O` and the four other modules pass |
| N28 | `src/squint_mcp/covered.py:212` | phase 1 counts as ink of a text every glyph of its channel inside its bounds, not only those in its own boxes | ❌ Survived - `O` and the four other modules pass |

**Sensor depth**: expanded (34 mutants this pass: the 11 survivors of the first pass, A7 and A8 again, and 21 new ones: 2 in the Check, 8 in the page script, 6 in the arithmetic, 4 in the Capture's wiring, 1 in the tool)
**Sensor outcome**: first-pass survivors 11/11 killed; new mutants 8/21 killed, 13 survived: 11 gaps, 1 equivalent (N7), 1 where the spec defines no outcome (N14) - ❌

### The survivors, decided by probes through the MCP boundary

Fourteen probe pages were written outside the repository and the worktrees and called with the in-memory MCP client, as `tests/helpers.py` does, with `checks` equal to `["overlap"]` at 1440 × 900, unmutated and under each survivor. They use Ahem at 20px on rows 50px apart, as the fixtures do. Unmutated, every probe gives the outcome the Terms define, but `p2b` (spec-precision gap 2).

| Probe | The page | Unmutated (the outcome of the Terms) | Mutant | Under the mutant |
| ----- | -------- | ------------------------------------ | ------ | ---------------- |
| `p1` | Four texts of ten glyphs in one row, each 40px to the right of the one before and painted over it; a cover over the last 50px of the fourth | `(#t0, major, 80, #t3)`, `(#t1, major, 80, #t3)`, `(#t2, major, 80, #t3)`, `(#t3, major, 25, #t3-cover)` | N2 | `#t3` at 100%, not 25% |
| `p1` | The same | The same | N3 | no Finding on `#t1` or `#t2` |
| `p12` | Two rows: a text at 40px half covered, a text at 300px with a cover over its last 20px | `(#left, major, 50, #left-cover)`, `(#right, minor, 10, #right-cover)` | N1b | no Finding on `#right` |
| `p2` | A text half under the grey box of a tag; the two glyphs of the tag stand to the right of that text, the second under a cover | `(#below, major, 50, #tag)`, `(#tag, major, 50, #tag-cover)` | N9 | no Finding on `#below` |
| `p10` | `XXXXX`, a `b` of ten glyphs, `XXXXX` in one element; a cover over its last 20px, 10% of its own text | `(#around, minor, 10, #end-cover)` | N28 | no Finding |
| `p3` | The sampled fixture with its stripes turned: opaque on the odd rows of the page over 120px (1200 pixels, none tested), a solid cover over the last 20px (400), twelve fillers | `(#striped, major, 40, #solid-cover)` | N5 | `coveredBy` `#stripes` |
| `p4` | The row of `#striped` of the sampled fixture alone: 1000 hidden pixels, under the cap, so every one is tested | `(#striped, major, 25, #stripes)` | N13 | `coveredBy` `#solid-cover` |
| `p5` | The scrolled fixture without its fixed bar, with a script that scrolls the page 900px while it loads | `(#far, major, 50, #far-cover)` | N8 | no Finding |
| `p6` | A text of `color: rgba(0, 0, 0, 0.5)`, half covered | `(#translucent, major, 50, #alpha-cover)` | N10 | no Finding |
| `p11` | `#clipped-fill`: `color` black, `-webkit-text-fill-color: transparent`; `#filled`: the reverse; both half covered | `(#filled, major, 50, #cover-b)` only | N22 | `(#clipped-fill, major, 50, #cover-a)` only |
| `p7` | A text half under a plain cover; over the same half an element of `role="menu"` and `visibility: hidden` | `(#under, major, 50, #plain-cover)` | N11 | no Finding |
| `p9b` | `#striped` and nine fillers, 19,000 hidden pixels; four texts each with 100px under a menu and 19px (9.5%) under a card | `(#striped, major, 25, #stripes)` | N14 | `coveredBy` `#solid-cover` |
| `p2b` | A text half under the `::after` of an element with two glyphs of its own, the second under a cover | `(#owner, major, 50, #owner-cover)`; no Finding on `#below`, which the Terms give 50% and the Coverer `#owner` | - | spec-precision gap 2 |
| `p2c` | `p2b` without the cover over the second element | `(#below, major, 50, #owner)` | - | the control of `p2b` |

**N7 is equivalent.** Hit testing is the last thing a Capture does to a page: `_measure_covered_text` returns after it (`src/squint_mcp/capture.py:220-230`), `capture` reads nothing more of the page and closes the browser context (`:300-305`), and each viewport gets a new context and a new page (`:253-260`). Where the page is left scrolled is read by nothing. `p5` and `p1` give the same Findings under it, and so does every test with two viewports.

**N14 is not counted as a gap.** Phase 1 already leaves out the texts under the threshold, so the bound of `capture.py:212` only acts on a text that a Silent layer takes under it, and then only on the size of the sample. A first probe, `p9`, with four plain texts at 9.5%, reads the same under the mutant for that reason; `p9b` puts a menu over each. Which of the two the spec means is spec-precision gap 1.

**The eleven gaps** (N1b, N2, N3, N5, N8, N9, N10, N11, N13, N22, N28) each change what the tool returns on a page, and each page is a fixture a test through the MCP boundary can hold. The widest reach: N8 loses every Finding of a page opened at a place other than its top, as by a URL with a fragment; N11 loses the Finding of a text that lies under a closed menu hidden by `visibility`, which is how most menus are closed; N2 and N3 are the stacked slides the spec's Out of Scope says are reported.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, apart from this report and the lessons store written afterwards. `HEAD` is `f5f190b` on `feat/overlap` both times, and `git worktree list` shows the main tree alone, as before. The four worktrees were removed: `git worktree remove --force` dropped them from git and stopped on the long paths of their virtual environments ("Filename too long"), so the directories were then deleted by path and `git worktree prune` was run. `git stash` was not used. Three runner processes were stopped by the Verifier once only repeats of finished mutants were left in their queues; their worktrees were restored with `git checkout -- .` and checked clean, and no result of an interrupted run is used.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ the fix pass changes no file under `src/`; `inspect_element` and `ping` are untouched by the feature |
| No scope creep | ✅ the two changes that reach every Capture are the ones the spec puts in scope (AD-006, issue #18) |
| Matches patterns | ✅ one module per Check, thresholds in `config` with their source, the browser only in `capture.py`, tests through the tool |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met | ⚠️ every criterion has its assertion; eleven behaviours of the code that the Terms decide have none (the survivors) |
| Every test maps to a spec requirement - no unclaimed tests | ✅ the ten new tests map to OVL-70 to OVL-79 |
| Documented guidelines followed: `CONTRIBUTING.md` and `docs/SPEC.md`, Testing Decisions (one seam, real Chromium) | ✅ |

---

## Edge Cases

- [x] OVL-68: the Findings of 1440 × 900 are also those of 390 × 844 (`tests/test_overlap.py:167-177`)
- [x] OVL-69: an element behind the clipped part of a text does not cover it (`tests/test_overlap.py:646-647`)

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`, each command run with its own exit status recorded
- **Gate outcome**: pyright exit 0 (0 errors, 0 warnings); ruff check exit 0; ruff format --check exit 0 (104 files); pytest exit 0 - 312 passed, 0 failed, 0 skipped, in 657.70s
- **Test count before feature**: 237
- **Test count after the first pass**: 302
- **Test count now**: 312
- **Delta**: +75 over the feature, all in `tests/test_overlap.py`; +10 in the fix pass
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed or weakened. The fix pass changes one existing assertion, the count of the bounds fixture (19 to 23), together with the four selectors added to its pinned list. The only assertions of the earlier slices that changed are the four `Valid checks:` literals OVL-55 supersedes

---

## Fix Plans

Fixes 1 to 6 touch no file under `src/`: each is a fixture case, a test and a criterion. Fix 7 is two decisions about the spec. The probe pages named are described in the sensor section; each fix can start from its probe.

### Fix 1: More than three texts in one place (N2, N3)

- **Root cause**: no fixture has more than two texts whose own-text boxes cross, so no text is ever on the third channel or in a second round.
- **Fix task**: a fixture case of four texts stacked in one row, each shifted 40px, with a cover over the last 50px of the fourth (`p1`); a criterion for four Findings: the first three at 80%, covered by the fourth, and the fourth at 25%, covered by its cover.
- **Done when**: the test fails with `painted[0]` read at `capture.py:205` and with the third colour of `INK` black at `covered_text.js:143`.
- **Priority**: Major (a wrong share, 100 for 25, and lost Findings on stacked slides, which the spec says are reported)

### Fix 2: The place of a text in a screenshot it shares (N1b, N9, N28)

- **Root cause**: every measured text of every fixture starts at column 40, no measured text has a box that reaches another's text while its glyphs do not, and no measured text has own text around a child with text.
- **Fix task**: three cases, a criterion each. A text that starts at another column, in a page with a second covered text (`p12`). A tag whose box covers half of a text while its own glyphs stand beside that text, the tag itself half covered (`p2`): two Findings at 50%. Own text around an inline child of ten glyphs, covered over exactly 10% of the own text (`p10`): one Finding at 10%.
- **Done when**: the tests fail with the column offset dropped at `covered.py:116`, with the region built from the own text alone at `covered_text.js:101-106`, and with the own-text mask dropped at `covered.py:212`.
- **Priority**: Major (missed Findings)

### Fix 3: The two sides of the sample that have no outcome (N5, N13)

- **Root cause**: OVL-79 pins the columns of a page over the cap. The rows, and a page under the cap, read the same either way.
- **Fix task**: on a page over the cap, a text with stripes on the odd rows that hide more than a solid cover does (`p3`): `coveredBy` is the solid cover. On a page under the cap, the row of `#striped` (`p4`): `coveredBy` is `#stripes`, since every pixel is tested.
- **Done when**: the first test fails with the row test removed at `covered_text.js:253`, the second with `hit_step` never under 2 at `covered.py:303`.
- **Priority**: Minor

### Fix 4: A page that is scrolled when it is captured (N8)

- **Root cause**: every fixture is captured at scroll zero, so the scroll the page script adds to each box is always 0.
- **Fix task**: a long page with one covered text below the first viewport and a script that scrolls to it on load (`p5`), or the scrolled fixture opened with a fragment; a criterion for its one Finding, with its Coverer.
- **Done when**: the test fails with `startY` read as 0 at `covered_text.js:16`.
- **Priority**: Major (every Finding of the page is lost)

### Fix 5: The colour that paints the glyphs (N10, N22)

- **Root cause**: the one fixture is `color: transparent`: alpha 0, and `color` and `-webkit-text-fill-color` agree.
- **Fix task**: a covered text of `color: rgba(0, 0, 0, 0.5)`: one Finding at 50% (`p6`). A covered text of `color` black and `-webkit-text-fill-color: transparent`: no Finding; and the reverse: one Finding (`p11`).
- **Done when**: the tests fail with `< 1` at `overlap.py:31` and with `color` read at `overlap.py:30`.
- **Priority**: Minor

### Fix 6: A Silent layer that is not painted (N11)

- **Root cause**: no fixture has an element of `visibility: hidden` among the Silent layers of a covered text, or inside one.
- **Fix task**: a text half under a plain cover, with an element of `role="menu"` and `visibility: hidden` over the same half (`p7`): one Finding at 50%, covered by the plain cover. It is also the closed menu the Goals of the spec name.
- **Done when**: the test fails with the visibility test removed at `covered_text.js:152`.
- **Priority**: Major (a closed menu over a covered text is common)

### Fix 7: Two sentences the spec lacks (N14, `p2b`)

- **Root cause**: the Term "Coverer" does not say which Hidden ink counts towards the 20,000; the design accepts a missed Finding (`design.md:259`) that the spec's Out of Scope does not list.
- **Fix task**: say in the Term that the Hidden ink to test is that of the elements whose Hidden share is at least 10%, which is what the code does. For the pseudo-element limit, the maintainer decides: a row in Out of Scope ("Known limit of this Check"), or a change to `covered.groups` with a fixture from `p2b`.
- **Done when**: both are written in `spec.md`; if the code changes, the test from `p2b` returns the Finding on `#below`.
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| OVL-01 to OVL-37, OVL-39 to OVL-66, OVL-68 to OVL-78 | Implemented | ✅ Verified |
| OVL-38 | Implemented | ⚠️ Verified as written; Fix 5 pins the alpha and the property |
| OVL-79 | Implemented | ⚠️ Verified as written; Fix 3 pins the rows and the page under the cap |
| OVL-67 | Pending | Pending the verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 78/78 criteria due now match the spec outcome; OVL-67 pending the verdict; 2 spec-precision gaps
**Sensor**: first-pass survivors 11/11 killed; 21 new mutants, 8 killed, 13 survived: 11 gaps, 1 equivalent, 1 where the spec defines no outcome
**Gate**: 312 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: everything the first pass found working, and now the reading of `role`, ancestors and descendants at hit testing, the bound of Text ink on both sides, two measured texts that cross, an element the scroll moved, the text the step passes over and the columns of the sample. On every probe of this pass but one the unmutated code gives the outcome of the Terms, four texts stacked in one place included.

**Issues found**: no defect against a criterion. Eleven behaviours without a test: a third channel and a second round (Fix 1), the place, the region and the own-text mask of a text in a shared screenshot (Fix 2), the rows of the sample and a page under the cap (Fix 3), a page scrolled when captured (Fix 4), the alpha and the property of the glyph colour (Fix 5) and a Silent layer that is not painted (Fix 6). Two sentences the spec lacks, one of them a missed Finding the design accepted (Fix 7).

**Next steps**: route Fix 1 to Fix 7 to an implementer, then re-verify (iteration 2 of 3). OVL-67 stays pending until that pass.
