# overlap Validation

**Date**: 2026-10-11
**Spec**: `.specs/features/overlap/spec.md`
**Diff range**: `eb9778b..cb8d81b` (14 commits, branch `feat/overlap`, base `8aa017c`)
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 1

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

Every one of the 68 criteria due now has an assertion on the outcome the spec defines, the gate is green, and no defect was found in the source: on ten probe cases built for this pass the unmutated code gives the outcome the Terms and the Assumptions define. The verdict is FAIL because the discrimination sensor left survivors, and the spec's third success criterion asks for none "in the Check, in what the Capture gains for it and in the rules of Silent and Raised layers". Of 49 mutants, 36 were killed and 13 survived. Two survivors are equivalent (a guard of the Check that the Capture already enforces). The other eleven each break a rule the Terms or the Assumptions table state, each was shown on a probe page to change what the tool returns, and each can be killed by a test through the MCP boundary. The fixes are fixtures, tests and a few criteria; no change to `src/` is asked for.

OVL-67 (the roadmap) is a closing step that follows a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `O` = `tests/test_overlap.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1: grayscale text | ✅ Done | `89385b0` |
| T2: settle the layout | ✅ Done | `a0c360e` |
| T3: thresholds, roles and hit-test cap in config | ✅ Done | `672699b` |
| T4: covered text on the Element model | ✅ Done | `434392c` |
| T5: keep the collector's list on the page | ✅ Done | `0713e8b` |
| T6: the cover page script | ✅ Done | `e9eb389` |
| T7: the covered-text arithmetic | ✅ Done | `60b50b5` |
| T8: measure covered text on request | ✅ Done | `c4b6407` |
| T9: the Check | ✅ Done | `e42c61b` |
| T10: silence on overlaps that are meant | ✅ Done | `cb74c82` |
| T11: bounds, severity and Coverer | ✅ Done | `806d09d` |
| T12: with the other Checks, many texts | ✅ Done | `b7f774a` |
| T13: documents | ✅ Done | `cb8d81b` |

All thirteen tasks are ticked in `tasks.md`. None is blocked or partial.

---

## Spec-Anchored Acceptance Criteria

Each fixture named by a criterion was read against it: the positions, sizes, roles, `z-index` values and document order in `overlap-bug.html`, `overlap-clean.html`, `overlap-bounds.html`, `overlap-order.html` and `overlap-many.html` are the ones the criteria state.

### P1: Report text that another element covers

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-01 one Finding per covered element | exactly one Finding each | `tests/test_overlap.py:55-59` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements, `finding["check"] == "overlap"`, `len(findings) == 4`; `O:357-378` pins the sorted list of the 19 selectors of the bounds fixture, so a second Finding on one element fails | ✅ PASS |
| OVL-02 the four Findings of the bug fixture, in order | `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)`, `(#collision, minor, 20, #stray)` | `O:67-72` - `covered(findings) == [...]`, the four tuples, equal to the spec's list | ✅ PASS |
| OVL-03 summary line | first block, `Found 4 findings in 1 viewport: 2 major, 2 minor.` | `O:79` - `texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."`; that the first block is the text block is held by `tests/test_detect_visual_bugs.py:263` | ✅ PASS |
| OVL-04 same call, same content | equal structured content | `O:83` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| OVL-05 text under the text of another element | one Finding, `hiddenPercent` 20 | `O:89-90` - `finding_on` unpacks exactly one; `["hiddenPercent"] == 20` | ✅ PASS |
| OVL-06 the text on top | no Finding for `#stray` | `O:94-95` - `await findings_on(client, BUG, "#stray", findings) == []` | ✅ PASS |
| OVL-07 `#left`, exactly 10% | one Finding, 10 | `O:381-386` - parametrized, `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-08 `#top`, exactly 10% | one Finding, 10 | `O:381-386` | ✅ PASS |
| OVL-09 `#bottom`, exactly 10% | one Finding, 10 | `O:381-386` | ✅ PASS |
| OVL-10 `#three-lines`, middle box | one Finding, 10 | `O:390-391` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-11 `#split`, second text node | one Finding, 10 | `O:395-396` - `["hiddenPercent"] == 10` | ✅ PASS |
| OVL-12 `#veil-55` | one Finding, 100, `major` | `O:400-402` - `["hiddenPercent"] == 100`, `finding["severity"] == "major"` | ✅ PASS |
| OVL-13 text and cover in one shadow tree | 50, `coveredBy` `[data-testid="shadow-cover"]` | `O:408-412` - `finding["evidence"]["measured"] == {"hiddenPercent": 50, "coveredBy": SHADOW_COVER}` | ✅ PASS |
| OVL-14 `#narrow`, one viewport only | one Finding at 390 × 844, none at 1440 × 900 | `O:101-106` - `... DESKTOP) == []`, `(finding,) = ... MOBILE)`, `finding["viewport"] == MOBILE` | ✅ PASS |
| OVL-15 `#in-dialog` | one Finding, `major` | `O:418` - `(await bounds(client, "#in-dialog"))["severity"] == "major"` | ✅ PASS |
| OVL-16 `#in-fixed` | one Finding, `major` | `O:424` - `(await bounds(client, "#in-fixed"))["severity"] == "major"` | ✅ PASS |
| OVL-17 `low-contrast-bounds.html` | exactly one Finding, `#covered`, 100, `major` | `O:548-552` - `(finding,) = ...["findings"]`, `finding["selector"] == "#covered"`, `["hiddenPercent"] == 100`, `["severity"] == "major"` | ✅ PASS |
| OVL-18 `low-contrast-reach.html` | exactly one Finding, `#veiled-most`, 100 | `O:558-561` - `(finding,) = ...`, `finding["selector"] == "#veiled-most"`, `["hiddenPercent"] == 100` | ✅ PASS |

### P1: Stay silent on overlaps that are meant

`clean(client, selector)` (`O:204-210`) returns the share of the element's box painted in the colour of the covers, read through `inspect_element`, and the Findings on that box. The first value proves the fixture really paints the cover over the text; the second is the criterion.

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-19 the clean fixture, all Checks | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `O:196-201` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| OVL-20 `#stretched` | no Finding | `O:218` - `await clean(client, "#stretched") == (0, [])` | ✅ PASS |
| OVL-21 `#under-faded` | no Finding | `O:223` - `== (0, [])` | ✅ PASS |
| OVL-22 `#veil-45` | no Finding | `O:230-231` - `painted(...)["#737373"] == 0.6`, `await clean(client, "#veil-45") == (0, [])` | ✅ PASS |
| OVL-23 the five roles | no Finding for each | `O:234-241` - parametrized over `menu`, `listbox`, `tooltip`, `dialog`, `alertdialog`: `await clean(client, f"#under-{role}") == (0.5, [])` | ✅ PASS; ⚠️ the reading of the attribute has no outcome (gap 1) |
| OVL-24 `dialog[open]` | no Finding | `O:248` - `== (0.5, [])` | ✅ PASS |
| OVL-25 open popover, `position: absolute` | no Finding | `O:254` - `== (0.5, [])` | ✅ PASS |
| OVL-26 `position: fixed` | no Finding | `O:259` - `== (0.5, [])` | ✅ PASS |
| OVL-27 `position: sticky` | no Finding | `O:264` - `== (0.5, [])` | ✅ PASS |
| OVL-28 descendant of a `menu` | no Finding | `O:272` - `== (0.5, [])` | ✅ PASS |
| OVL-29 static child of a fixed element | no Finding | `O:280` - `== (0.5, [])` | ✅ PASS |
| OVL-30 shadow tree of a `menu` host | no Finding | `O:432-435` - `painted(inspected)[COVER] == 0.5`, `[f for f in findings if f["box"] == inspected["box"]] == []` | ✅ PASS |
| OVL-31 `#nick`, 9.5% along the width | no Finding | `O:287` - `== (0.095, [])` | ✅ PASS |
| OVL-32 `#skim`, 5% along the height | no Finding | `O:295` - `== (0.2, [])` | ✅ PASS |
| OVL-33 `#parent-text`, under its own child | no Finding | `O:300` - `== (0.5, [])` | ✅ PASS; ⚠️ decided by Text ink, not by the Other-element rule (gap 2) |
| OVL-34 `#under-ghost`, `pointer-events: none` | no Finding | `O:308` - `== (0.5, [])` | ✅ PASS |
| OVL-35 `#caption` over `#picture` | no Finding for either | `O:317-320` - `painted(...)["#000000"] == 0.24`, both `findings_on(...) == []` | ✅ PASS |
| OVL-36 `#badge` on `#inbox` | no Finding | `O:328` - `== (0.0533, [])` | ✅ PASS |
| OVL-37 `visibility: hidden` | no Finding | `O:333` - `== (0.5, [])` | ✅ PASS |
| OVL-38 `color: transparent` | no Finding | `O:341` - `== (0.5, [])` | ✅ PASS |
| OVL-39 `opacity: 0` | no Finding | `O:346` - `== (0.5, [])` | ✅ PASS; ⚠️ only `opacity: 0` has an outcome (gap 4) |

### P1: Severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-40 25% is `major`, 24.5% is `minor` | `#quarter` `major`, `#almost-quarter` `minor` | `O:441-445` - `quarter[...]["hiddenPercent"] == 25`, `quarter["severity"] == "major"`, `almost["severity"] == "minor"` | ✅ PASS |
| OVL-41 `#layered-half` | `minor` | `O:462` - `share_and_severity(...) == (50, "minor")` | ✅ PASS |
| OVL-42 `#layered-corner` | `info` | `O:468` - `== (10, "info")` | ✅ PASS |
| OVL-43 `#layer-ancestor` | `minor` | `O:474-476` - `["coveredBy"] == "#layer-cover"`, `== (50, "minor")` | ✅ PASS |
| OVL-44 `#shared-layer` | `major` | `O:482` - `== (50, "major")` | ✅ PASS |
| OVL-45 `#z-zero` | `major` | `O:486` - `== (50, "major")` | ✅ PASS |
| OVL-46 `#z-static` | `major` | `O:492-494` - `["coveredBy"] == "#z-static-next"`, `== (50, "major")` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-47 the Finding of `#half` | the literal of the spec | `O:112-129` - `findings[0] == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| OVL-48 message at 10% | `10% of the text is covered by another element` | `O:133-135` - `["hiddenPercent"] == 10`, `finding["message"] == "10% of the text is covered by another element"` | ✅ PASS |
| OVL-49 truncation | 24 for 24.5% | `O:450-452` - `["hiddenPercent"] == 24`, `finding["message"] == "24% of the text is covered by another element"` | ✅ PASS |
| OVL-50 `#mixed` | 20, `#mixed-card`, `minor` | `O:501-506` - `["measured"] == {"hiddenPercent": 20, "coveredBy": "#mixed-card"}`, `finding["severity"] == "minor"` | ✅ PASS |
| OVL-51 `#two-covers` | 60, `#large-cover` | `O:513-517` - `["measured"] == {"hiddenPercent": 60, "coveredBy": "#large-cover"}` | ✅ PASS |
| OVL-52 `#tie` | 40, `#tie-first` | `O:525-529` - `["measured"] == {"hiddenPercent": 40, "coveredBy": "#tie-first"}` | ✅ PASS |
| OVL-53 both selectors work in `inspect_element` | `isError: false`, same `box` for `selector` | `O:535-542` - for the 4 Findings of the bug fixture and the 19 of the bounds fixture (`len(findings) == count`): `inspected["box"] == finding["box"]`, and `inspect` (`O:182`, `result.is_error is False`) on `coveredBy` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-54 four Checks by default | `overlap` runs with the other three | `O:139-145` - the four `(selector, "overlap")` pairs on a call without `checks`; `O:576-583` - `low-contrast-real` and `overlap` in one default call; the default run of the other two is held by their own modules, which pass | ✅ PASS |
| OVL-55 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `tests/test_detect_visual_bugs.py:340-344` - the literal `in text`; the same literal at `D:351-355`, `D:362-366` (`zzz`) and `D:374-378` | ✅ PASS |
| OVL-56 the other three Checks on the bug fixture | `[]` | `O:149-150` - `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| OVL-57 order across Checks | `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)` | `O:576-583` - `{severity} == {"minor"}`, the four pairs in order | ✅ PASS |
| OVL-58 the description names `overlap` | names it and says what it reports | `O:154-159` - `` "`overlap` (text another element is painted over" in " ".join(tool.description.split()) `` | ✅ PASS |
| OVL-59 earlier tests unchanged | pass, only the four literals differ | by reading: `git diff --name-status 8aa017c..cb8d81b -- tests` lists five new fixtures, the new `tests/test_overlap.py` and `tests/test_detect_visual_bugs.py`, whose diff is the four `Valid checks:` literals and nothing else; `helpers.py`, `conftest.py` and every earlier fixture are untouched; the gate passes | ✅ PASS |
| OVL-60 a hundred covered texts | `isError: false`, 100 Findings | `O:587-595` - `result.is_error is False`, `len(findings) == 100`, and the 100 tuples `(#text-n, major, 50, #cover-n)` | ✅ PASS; ⚠️ the fixture reads the same with and without the hit-test cap (gap 3) |

### P2: Check contract, configuration and documents (file evidence, by reading)

| Criterion | Evidence | Result |
| --------- | -------- | ------ |
| OVL-61 one module, one function, registered | `src/squint_mcp/checks/overlap.py:85` - `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:23` - `"overlap": overlap.check` | ✅ PASS |
| OVL-62 no `playwright` in the Checks or in `vision.py` | `grep -rn playwright src/squint_mcp/checks src/squint_mcp/vision.py src/squint_mcp/covered.py` finds nothing (exit 1) | ✅ PASS |
| OVL-63 thresholds and roles in `config`, each cited | `src/squint_mcp/config.py:129` `OVERLAP_MIN_HIDDEN_PERCENT = 10` ("Squint default", with the reason, `:126-128`); `:133` `OVERLAP_MAJOR_HIDDEN_PERCENT = 25` ("Squint default", `:131-132`); `:138` `SILENT_LAYER_ROLES` ("WAI-ARIA 1.2", `:135-137`) | ✅ PASS |
| OVL-64 no literal of them in the Check | `src/squint_mcp/checks/overlap.py:46` and `:59` read both thresholds from `config`; the roles do not appear. The literals left are the `* 100` of a percentage (`:46`, `:59`, `:66`) and `== 0` for alpha and ink (`:31`, `:40`) | ✅ PASS |
| OVL-65 CHANGELOG | `CHANGELOG.md:12`, under `## [Unreleased]` (`:7`): the Check, 10% and 25%, one level lower under a raised layer, and what is not reported: declared layers, `fixed` and `sticky`, covers that paint nothing | ✅ PASS |
| OVL-66 README | `README.md:45` - "`detect_visual_bugs` runs four Checks: ... and `overlap` (...)" | ✅ PASS |
| OVL-67 roadmap `concluída` | Pending by design: a closing step after a PASS. `docs/ROADMAP.md:110` says `pendente`, which is right today | ⏳ Pending the verdict |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| OVL-68 two viewports | each Finding of the first has one in the second | `O:165-175` - `len(desktop) == 4`, `desktop <= mobile` over `(selector, check)` | ✅ PASS |
| OVL-69 `text-clipped-clean.html` | `[]` | `O:569-570` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |

**Status**: 68 of 68 criteria due now are covered and match the spec-defined outcome; OVL-67 waits for the verdict. ⚠️ Five spec-precision gaps flagged, all on rules stated in the Terms or the Assumptions table and held by no criterion.

### Spec-precision gaps

1. **How the `role` attribute is read (Assumptions, "The `role` attribute").** "Compared whole, in lower case and trimmed; a list of several roles is not a Silent layer." Every fixture writes its role alone, in lower case, with no space. OVL-23 has no outcome that depends on any of the three clauses. Mutants J4 and J5 live there.
2. **Which elements are Other elements at hit testing (Terms, "Other element"; Out of Scope, "Text covered by one of its own descendants, or by something an ancestor paints").** OVL-34 holds that the text itself is not one. Nothing holds that an ancestor is not one: no fixture has an ancestor that paints over the text. OVL-33 reads as the criterion for descendants, but `#parent-text` is silent because its child is part of what the text is painted alone with, so it has no Hidden ink and hit testing is never asked. Mutants J6b and J6c live there.
3. **The three clauses of the Coverer that only show on a long or heavy page (Terms, "Coverer").** "An element the scroll moved from where the Capture has it is passed over", "each element at least once" and "the largest part is then of that sample" have no criterion. The bounds fixture scrolls and is sampled, but its fixed element is never over a tested pixel after the scroll, no text of it is passed over whole by the step, and no Coverer of it depends on the sample. `overlap-many.html` (OVL-60) returns the same 100 Findings with the cap removed, in 15.5s instead of 4.4s on this machine: the 30s clock does not hold the cap either. Mutants J8, J10 and C8 live there.
4. **How much ink makes Text ink (Terms, "Text ink").** "Covers by at least half" and "faded below half by `opacity`" are pinned at the two ends only: Ahem gives ink of 255 or 0, and the one faded fixture is `opacity: 0` (OVL-39). Mutants C2 and C2b live there. "Seen" does not share this gap: OVL-12 and OVL-22 bracket its half between 45% and 55% (C1, C1b).
5. **Two measured texts that cross.** The Terms measure Text ink "when nothing outside the element is painted over it". In every fixture where the boxes of two texts cross, only one of the two is measured (`#collision` and `#z-static`; `#stray` and `#z-static-next` have nothing hidden). So nothing depends on the rule that keeps two measured texts out of one screenshot, nor on a measured text being read on its own channel. Mutants C5 and C11 live there.

Not observable through the tool boundary, and not counted as gaps:

- **Covered text is measured only on request.** W1 and W1b kill the wiring that fails to ask when `overlap` runs. Asking when no Check reads it changes only how long a call takes: `_measure_covered_text` runs after `pixels`, `background` and `ink` are taken (`src/squint_mcp/capture.py:300-302`) and writes only `covered_text`. The CHANGELOG sentence "a call whose `checks` leaves it out does not pay for it" is true of the code and has no test.
- **`_settle_layout` (issue #18, AD-006).** The fault shows on Windows only and on a page that uses the generic `monospace` font; no fixture does. The code, the design and `tasks.md` (T2) say no test holds it. Not sensed.
- **Two guards of the Check repeat what the Capture enforces** (A7, A8 below).

### Observations (not gaps)

- `O:79` reads the first text block, not the first block. `D:263` (`isinstance(result.content[0], TextContent)`) holds that the two are the same.
- The silent cases of the clean fixture are also held together by OVL-19 (`O:199`), with all four Checks running.
- `O:357-378` pins the 19 selectors of the bounds fixture and `O:535-537` both counts, so a Finding on any element no criterion names fails.
- The whole suite now takes 621s here; `tasks.md` gives about seven minutes for the 237 tests before the slice.
- `.specs/features/overlap/spike/` and its `extend-exclude` line are still there, as the closing step of `tasks.md` expects.

---

## Discrimination Sensor

Run in temporary git worktrees of `cb8d81b` under the session's temp directory, outside the repository, each with its own `uv sync`. One mutant at a time, the worktree restored with `git checkout -- .` and checked clean after each. Unmutated, a worktree passes `O` (65 passed in 199s). A mutant expected to die was run against the tests of its rule; "Test" is the test that failed, with what it reported. A survivor was run against all of `O` and then against the four other modules that can reach the mutated code (`D`, `test_low_contrast_real.py`, `test_text_clipped.py`, `test_offscreen_overflow.py`: 150 tests) before it was called a survivor. The four modules left (`test_inspect_element.py`, `test_selectors.py`, `test_ping.py`, `test_vision.py`) never ask a Capture for covered text.

### The Check (`src/squint_mcp/checks/overlap.py`)

| # | Line | Mutation | Result |
| - | ---- | -------- | ------ |
| A1 | `:46` | reporting threshold `<` → `<=` (exactly 10% is dropped) | ✅ Killed - `test_the_findings_say_how_much_is_hidden_and_by_what_in_order`, the three edges of `test_a_tenth_of_the_text_hidden_at_one_of_its_edges_is_enough` and `test_the_message_states_the_hidden_share` |
| A2 | `:59` | `major` threshold `>=` → `>` | ✅ Killed - the order test and `test_a_quarter_hidden_is_major_and_just_under_it_is_minor` |
| A3 | `:66` | the percent rounded up instead of truncated | ✅ Killed - `test_the_hidden_share_is_truncated_to_whole_percents` (`25 == 24`) |
| A4 | `:64` | a raised cover never gives `info` | ✅ Killed - `test_a_tenth_hidden_by_a_positioned_cover_with_a_z_index_is_info` |
| A10 | `:63` | a raised cover lowers `major` only | ✅ Killed - same test |
| A5 | `:53` | on a tie, the last cover in the document | ✅ Killed - `test_of_two_covers_that_hide_as_much_the_first_in_the_document_is_named` |
| A11 | `:53` | the first cover in the document, whatever it hides | ✅ Killed - `test_the_cover_over_most_of_the_hidden_ink_is_the_one_named` |
| A6 | `:43` | the transparent-glyph guard dropped | ✅ Killed - `test_covered_text_painted_transparent_is_not_reported` and the clean page |
| A9 | `:50` | the no-cover guard dropped | ✅ Killed - `test_text_under_a_cover_hit_testing_passes_through_is_not_reported` (the call fails) and the clean page |
| A7 | `:40` | the `ink == 0` guard dropped | ⚠️ Survived on `O` - equivalent: no ink means no Hidden ink, so the Capture never hit tests the text (`capture.py:212`) and `:50` returns |
| A8 | `:46` | the reporting threshold dropped from the Check | ⚠️ Survived on `O` - equivalent: under the threshold the Capture leaves `covers` empty (`capture.py:212`) and `:50` returns. W2 shows the other half: with the Capture's bound moved, the tests fail |

### Silent layers, Raised layers, Other elements and hit testing (`src/squint_mcp/js/covered_text.js`)

| # | Line | Mutation | Result |
| - | ---- | -------- | ------ |
| J1 | `:56` | an open popover is no Silent layer | ✅ Killed - `test_text_under_an_open_popover_is_not_reported` |
| J2 | `:58` | `sticky` is no Silent layer | ✅ Killed - `test_text_under_a_sticky_element_is_not_reported` |
| J2b | `:57` | `fixed` is no Silent layer | ✅ Killed - `test_text_under_a_fixed_element_is_not_reported` |
| J2c | `:55` | `dialog[open]` is no Silent layer | ✅ Killed - `test_text_under_an_open_dialog_element_is_not_reported` |
| J3 | `:109` | a Silent layer that holds the text is still one for it | ✅ Killed - both `test_text_covered_by_its_neighbour_inside_one_...` tests |
| J16 | `:231` | a Silent layer is painted without what is inside it | ✅ Killed - the menu item, the static child of a fixed element and the shadow tree of a menu |
| J19 | `:20` | ancestors stop at a shadow root | ✅ Killed - `test_text_under_an_element_in_the_shadow_tree_of_a_menu_is_not_reported` |
| J4 | `:54` | the `role` attribute compared as written, not trimmed or lowered | ❌ Survived - `O` and the four other modules pass |
| J5 | `:54` | a list of roles is a Silent layer when one of them is | ❌ Survived - `O` and the four other modules pass |
| J6a | `:290` | the Other-element rule dropped | ✅ Killed - `test_text_under_a_cover_hit_testing_passes_through_is_not_reported` (`coveredBy` is the text itself) |
| J6b | `:290` | an ancestor of the text counts as an Other element | ❌ Survived - `O` and the four other modules pass |
| J6c | `:290` | a descendant of the text counts as an Other element | ❌ Survived - `O` and the four other modules pass |
| J7 | `:173` | hit testing stops at a shadow host | ✅ Killed - `test_text_covered_inside_its_shadow_tree_names_the_cover_of_that_tree` |
| J8 | `:171` | an element the scroll moved is not passed over | ❌ Survived - `O` and the four other modules pass |
| J9 | `:279` | the page is not scrolled for hit testing | ✅ Killed - the list of the bounds fixture and `test_a_page_of_a_hundred_covered_texts_is_checked` |
| J10 | `:259` | a text the step passes over whole is not tested | ❌ Survived - `O` and the four other modules pass |
| J17 | `:297` | the covers are not put in document order | ✅ Killed - the tie test (`#tie-second`) |
| J12 | `:304` | a raised ancestor of both counts | ✅ Killed - `test_a_z_index_on_an_ancestor_of_both_does_not_lower_the_severity` |
| J13 | `:60` | a `z-index` counts without `position` | ✅ Killed - `test_a_z_index_on_a_static_cover_does_not_lower_the_severity` |
| J14 | `:60` | `z-index` `> 0` → `>= 0` | ✅ Killed - `test_a_z_index_of_zero_does_not_lower_the_severity` |
| J15 | `:303` | the ancestors of the cover are not looked at | ✅ Killed - `test_a_cover_inside_a_positioned_element_with_a_z_index_is_one_level_lower` |

### "Seen", Text ink, the phase-1 bound and the grouping (`src/squint_mcp/covered.py`)

| # | Line | Mutation | Result |
| - | ---- | -------- | ------ |
| C1 | `:24` | seen from a third of the ink | ✅ Killed - `test_text_mostly_hidden_by_a_veil_is_hidden_whole` |
| C1b | `:24` | seen only with all of the ink | ✅ Killed - `test_text_mostly_seen_through_a_veil_is_not_reported` and the veil of the earlier fixture |
| C2 | `:23` | Text ink from any ink (`>= 1`) | ❌ Survived - `O` and the four other modules pass |
| C2b | `:23` | Text ink from ink of 200 | ❌ Survived - `O` and the four other modules pass |
| C3 | `:225` | phase 1 ignores the glyphs of another text | ✅ Killed - the order test and `test_text_under_the_text_of_another_element_is_reported` |
| C4 | `:227` | phase-1 bound `>=` → `>` | ✅ Killed - the order test and the three edges |
| C5 | `:242` | every measured text in one group | ❌ Survived - `O` and the four other modules pass |
| C8 | `:303` | every hidden pixel is hit tested (no cap) | ❌ Survived - `O` and the four other modules pass |
| C10 | `:186` | every text on one channel of one round | ✅ Killed - the order test, the collision test and `test_a_z_index_on_a_static_cover_does_not_lower_the_severity` |

### The on-request wiring (`tools/detect_visual_bugs.py`, `capture.py`, `config.py`)

| # | File:line | Mutation | Result |
| - | --------- | -------- | ------ |
| W1 | `src/squint_mcp/tools/detect_visual_bugs.py:91` | covered text asked only when `checks` is given | ✅ Killed - `test_the_summary_counts_the_findings_of_the_bug_fixture`, `test_overlap_runs_when_no_check_is_named` and the order across Checks |
| W1b | `src/squint_mcp/tools/detect_visual_bugs.py:91` | covered text asked only when `overlap` runs alone | ✅ Killed - the same three |
| W2 | `src/squint_mcp/capture.py:212` | the hit-test bound `>=` → `>` | ✅ Killed - the order test and the three edges |
| W3 | `src/squint_mcp/capture.py:207` | the Silent layers are never painted | ✅ Killed - the five roles and `#mixed` |
| W4 | `src/squint_mcp/capture.py:228` | a cover is never raised | ✅ Killed - the three tests of a lower severity |
| W5 | `src/squint_mcp/capture.py:194` | texts with different Silent layers painted with them together | ✅ Killed - both `test_text_covered_by_its_neighbour_inside_one_...` tests |
| C11 | `src/squint_mcp/capture.py:205` | a measured text is read on the first channel, whatever its own | ❌ Survived - `O` and the four other modules pass |
| W8 | `src/squint_mcp/config.py:16` | `--disable-lcd-text` dropped | ✅ Killed here, on Windows - `test_text_mostly_hidden_by_a_veil_is_hidden_whole` (`95 == 100`, the value AD-006 records) |

**Sensor depth**: expanded (49 mutants: 11 in the Check, 21 in the page script, 9 in the arithmetic, 8 in the wiring)
**Sensor outcome**: 36/49 killed, 13 survived: 11 gaps, 2 equivalent - ❌

### The eleven gaps, shown not to be equivalent

Four probe pages were written outside the worktrees and called through the in-memory MCP client, with `checks` equal to `["overlap"]`, unmutated and under each survivor. Unmutated, every probe case gives the outcome the spec states.

| Probe case | Unmutated (the spec's outcome) | Mutant | Under the mutant |
| ---------- | ------------------------------ | ------ | ---------------- |
| Text half under an element of `role=" Menu "` | no Finding | J4 | a Finding, 50%, `major` |
| Text half under an element of `role="menu navigation"` | a Finding, 50%, `major` | J5 | no Finding |
| Text half under the `::after` of its own row | no Finding | J6b | a Finding, 50%, `coveredBy` the row |
| Text half under a cover, with a link of its own stretched over it above the cover | no Finding | J6c | a Finding, 50%, `coveredBy` the link |
| Text 1000px down a page of 2700px, half under a plain cover; a `fixed` element 100px down the viewport, so over that half once hit testing scrolls to 900px | `coveredBy` the plain cover | J8 | `coveredBy` the fixed element |
| One glyph of 10px with a cover one column wide on an odd column (10%), on a page of 24,000 hidden pixels | a Finding, 10%, `minor` | J10 | no Finding |
| Text of `opacity: 0.4`, half covered | no Finding | C2 | a Finding, 50% |
| Text of `opacity: 0.6`, half covered | a Finding, 50% | C2b | no Finding |
| `#below` half under a label with a background; the label's own two glyphs half under a second cover | `#below` 50%, `#label` 50% | C5 | `#below` 28% |
| The same | `#label` 50% | C11 | `#label` 100% |
| Text with 600 hidden pixels on odd columns under one cover and 400 under another, on a page of 24,000 hidden pixels | `coveredBy` the cover of the 400, the largest part of the sample | C8 | `coveredBy` the cover of the 600 |

J8 is the one with the widest reach: a fixed header on any page longer than its viewport is over other text once hit testing scrolls, and without the rule it is named as what covers that text.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, apart from this report and the lessons store written afterwards. `HEAD` is `cb8d81b` on `feat/overlap` both times. The three worktrees were removed (`git worktree remove --force` dropped them from git and stopped on the long paths of their virtual environments, so the directories were then deleted by path), `git worktree prune` was run, and `git worktree list` shows the main tree alone, as before. `git stash` was not used. One run was interrupted by the Verifier while a mutant was applied in a scratch worktree; that worktree was restored, the run was discarded and the mutant was run again in a clean one.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ `inspect_element` and `ping` are untouched; `vision._bounds` is made public for the one new caller |
| No scope creep | ✅ the two changes that reach every Capture are the ones the spec puts in scope (AD-006, issue #18) |
| Matches patterns | ✅ one module per Check, thresholds in `config` with their source, the browser only in `capture.py`, tests through the tool |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met | ⚠️ every criterion has its assertion; eleven behaviours the Terms and the Assumptions define have none (the survivors) |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `CONTRIBUTING.md` and `docs/SPEC.md`, Testing Decisions (one seam, real Chromium) | ✅ |

---

## Edge Cases

- [x] OVL-68: the Findings of 1440 × 900 are also those of 390 × 844 (`tests/test_overlap.py:165-175`)
- [x] OVL-69: an element behind the clipped part of a text does not cover it (`tests/test_overlap.py:569-570`)

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`, each command run with its own exit status recorded
- **Gate outcome**: pyright exit 0 (0 errors, 0 warnings); ruff check exit 0; ruff format --check exit 0 (103 files); pytest exit 0 - 302 passed, 0 failed, 0 skipped, in 621.62s
- **Test count before feature**: 237
- **Test count after feature**: 302
- **Delta**: +65, all in `tests/test_overlap.py`
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed; the only assertions changed are the four `Valid checks:` literals OVL-55 supersedes

---

## Fix Plans

No fix touches `src/`. Each is a fixture, a test and, where the spec has no criterion, a criterion. Fixes 1 to 3 belong in the clean and bounds fixtures; fixes 4, 5 and 8 need a page of their own, because they need a long page or more than 20,000 hidden pixels with nothing else on it.

### Fix 1: The reading of the `role` attribute is unprotected (J4, J5)

- **Root cause**: every role of the fixtures is written alone, in lower case, with no space.
- **Fix task**: add to `overlap-clean.html` a text half under an element of `role=" Menu "` (no Finding) and to `overlap-bounds.html` a text half under an element of `role="menu navigation"` (one Finding, 50%, `major`); a criterion for each; the list of `tests/test_overlap.py:357-378` and the count of `:535` grow by one.
- **Done when**: the first test fails with `.trim().toLowerCase()` removed at `covered_text.js:54` and the second with the attribute split into tokens.
- **Priority**: Minor

### Fix 2: An ancestor is not held out of the Other elements (J6b)

- **Root cause**: no fixture has an ancestor of a text that paints over it.
- **Fix task**: add to `overlap-clean.html` a row whose `::after` is an opaque box over the last 100px of its text; a criterion that the text gets no Finding, with the painted share (0.5) asserted as for the other clean cases.
- **Done when**: the test fails with the ancestors left out of the check at `covered_text.js:290`.
- **Priority**: Major (decorations painted by a parent are common, and the false Finding would be `major` and name the parent)

### Fix 3: A descendant is held out of the Other elements by Text ink only (J6c)

- **Root cause**: in `#parent-text` the child is part of what the text is painted alone with, so hit testing is never asked.
- **Fix task**: add a text with a link of its own stretched over it (`::after`, `inset: 0`, `z-index: 2`) and a cover of `z-index: 1` over half of it; a criterion that it gets no Finding. Or state in the spec that such a text is reported and name the Coverer.
- **Done when**: the test fails with `ancestorsOf(found).includes(...)` removed at `covered_text.js:290`.
- **Priority**: Minor

### Fix 4: An element the scroll moved is not passed over (J8)

- **Root cause**: after the one scroll of the bounds fixture, its fixed element is not over a tested pixel.
- **Fix task**: a fixture longer than two viewports with a text below the first viewport, half under a plain cover, and a `fixed` element placed so that it lies over that half once the page is scrolled a viewport (text 1000px down, fixed element 100px down the viewport, for 1440 × 900); a criterion that `coveredBy` is the plain cover.
- **Done when**: the test fails with `moved(element, i)` removed at `covered_text.js:171`.
- **Priority**: Major (a fixed header on a long page)

### Fix 5: A text the step passes over whole (J10)

- **Root cause**: with a step of 2 every text of the bounds fixture has a hidden pixel on an even column of an even row.
- **Fix task**: a fixture with more than 20,000 hidden pixels and one text of one glyph of 10px under a cover one column wide on an odd column; a criterion for one Finding at 10% that names the cover.
- **Done when**: the test fails with the fallback at `covered_text.js:259` removed.
- **Priority**: Minor

### Fix 6: The ink that makes Text ink has no outcome on either side (C2, C2b)

- **Root cause**: Ahem gives ink of 255 or 0, and the one faded text is `opacity: 0`.
- **Fix task**: add to `overlap-clean.html` a text of `opacity: 0.4`, half covered (no Finding: it has no Text ink), and to `overlap-bounds.html` one of `opacity: 0.6`, half covered (one Finding, 50%); a criterion for each. They give ink of 102 and 153 and bracket the bound as OVL-12 and OVL-22 bracket "seen".
- **Done when**: the first test fails with `_IS_TEXT` at 1 and the second with it at 200 (`covered.py:23`).
- **Priority**: Major for the `>= 1` side (false Findings on faint text), Minor for the other

### Fix 7: Two measured texts that cross (C5, C11)

- **Root cause**: where the boxes of two texts cross, only one of them is ever measured.
- **Fix task**: add to `overlap-bounds.html` a text with a label over its first 100px, the label having a background and two glyphs of its own, and a cover over the second of them: a criterion for two Findings, both at 50%, the text covered by the label and the label by the cover.
- **Done when**: the test fails with every candidate in one group (`covered.py:242`) and with the first channel read for every text (`capture.py:205`).
- **Priority**: Major (a wrong `hiddenPercent`, 28 for 50 and 100 for 50 on the probe)

### Fix 8: The hit-test cap changes no result (C8)

- **Root cause**: `overlap-many.html` returns the same Findings with every pixel tested, and well inside the 30s clock.
- **Fix task**: on the page of Fix 5, a text with 600 hidden pixels on odd columns under one cover (a `repeating-linear-gradient` of 1px stripes) and 400 under a second, opaque one; a criterion that `coveredBy` is the second, "the largest part of that sample". If the maintainer would rather not pin the sample, say in the Terms that which element a sampled Capture names is not specified, and this stops being a gap.
- **Done when**: the test fails with `hit_step` returning 1 (`covered.py:303`).
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| OVL-01 to OVL-22, OVL-24 to OVL-32, OVL-34 to OVL-38, OVL-40 to OVL-59, OVL-61 to OVL-66, OVL-68, OVL-69 | Implemented | ✅ Verified |
| OVL-23 | Implemented | ⚠️ Verified as written; Fix 1 pins how the attribute is read |
| OVL-33 | Implemented | ⚠️ Verified as written; Fix 2 and Fix 3 pin the Other-element rule |
| OVL-39 | Implemented | ⚠️ Verified as written; Fix 6 pins the bound of Text ink |
| OVL-60 | Implemented | ⚠️ Verified as written; Fix 4, Fix 5 and Fix 8 pin the three clauses of the Coverer |
| OVL-67 | Pending | Pending the verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 68/68 criteria due now match the spec outcome; OVL-67 pending the verdict; 5 spec-precision gaps
**Sensor**: 36/49 mutants killed; 13 survived, 11 of them gaps, 2 equivalent
**Gate**: 302 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: the Check and both of its thresholds on each side, the truncation of the share, the two levels of a lower severity, the choice of the Coverer and its tie, every kind of Silent layer with its descendants and across a shadow root, the Silent layer that holds the text, the four clauses of a Raised layer, "seen" on both sides of half, text over text, the scroll of hit testing, the descent into shadow trees, the Finding literal, the order across Checks and the wiring that asks for covered text.

**Issues found**: no source defect. Eleven behaviours without a test: the reading of `role` (Fix 1), ancestors and descendants as Other elements (Fix 2, Fix 3), an element moved by the scroll (Fix 4), a text the step passes over (Fix 5), the bound of Text ink (Fix 6), two measured texts that cross (Fix 7) and the sample of a capped Capture (Fix 8).

**Next steps**: route Fix 1 to Fix 8 to an implementer, then re-verify (iteration 1 of 3). OVL-67 stays pending until that pass.
