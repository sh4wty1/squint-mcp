# low-contrast-real Validation

**Date**: 2026-10-08
**Spec**: `.specs/features/low-contrast-real/spec.md`
**Diff range**: `9d7afb9..508657e` (13 commits, branch `feat/low-contrast-real`); pass 1 covered `9d7afb9..f97904b`
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 2 (fix→re-verify iteration 1 of 3)

**Verdict**: ❌ FAIL

The verdict is that of the second pass, described in the section right below. The six survivors of pass 1 are all killed and the nine criteria checked in pass 2 match the spec. It is still FAIL because two of the new mutants of pass 2 survive against LCR-55 (V5 in the sampling code, C4 in the collector). No defect was found in the source in either pass.

**History**

| Pass | Range | Verdict | Sensor in that pass | Closed by |
| ---- | ----- | ------- | ------------------- | --------- |
| 1 | `9d7afb9..f97904b` | FAIL | 46 mutants, 7 survived (6 gaps, 1 equivalent in scope) | `42201eb`, `508657e` (tests, fixture, spec wording) |
| 2 | `9d7afb9..508657e` | FAIL | 6 re-runs all killed; 6 new, 4 survived (2 gaps, 2 inside the bracket the spec sets) | open |

Abbreviations: `L` = `tests/test_low_contrast_real.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Second pass

**Date**: 2026-10-08, at `508657e`. **Result**: ❌ FAIL, two new gaps, both on LCR-55.

### What changed since pass 1

`git diff f97904b..508657e -- src` is empty. `git diff f97904b..508657e -- tests` only adds: the fixture `tests/fixtures/low-contrast-reach.html`, nine tests at the end of `L` (`L:344-400`) and one at the end of `D` (`D:473-488`). No test or assertion of pass 1 was touched, so the 51 criteria verified there stand. The spec gained LCR-53 to LCR-60, narrowed LCR-51 to `display: none`, and names the translucent layer in Terms, Out of Scope and Assumptions.

### Spec-anchored check of the new and reworded criteria

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-51 `display: none` (`#no-box`) | no Finding | `L:302-303` - `"#no-box" not in [finding["selector"] ...]`, `len(findings) == 8` | ✅ PASS; the wording now names the one case the test pins |
| LCR-53 one severity, viewport by viewport | the eight `(viewport width, selector)` pairs, in order | `D:479-488` - `[(f["viewport"]["width"], f["selector"]) for f in findings] == [(1440, hero), (390, hero), (1440, "#flat"), (1440, "#alpha"), (1440, "#almost-large"), (390, "#flat"), (390, "#alpha"), (390, "#almost-large")]`, equal to the spec's list | ✅ PASS |
| LCR-54 `#parent` and `#badge` | no Finding for either | `L:362-363` - `await reach(client, "#parent") == []`, `await reach(client, "#badge") == []` | ✅ PASS |
| LCR-55 `#two-lines` | one Finding, ratio 1.6; "the text pixels of all" the boxes | `L:367-369` - `(finding,) = await reach(client, "#two-lines")`, `["contrastRatio"] == 1.6`, `["sampledBackground"] == "#cccccc"` | ✅ PASS for the fixture named; ⚠️ "all of them" is pinned for a later box of one text node only (V5, C4) |
| LCR-56 `#veiled-most`, layer of 0.7 | no Finding | `L:375` - `await reach(client, "#veiled-most") == []` | ✅ PASS |
| LCR-57 `#veiled-little`, layer of 0.3 | one Finding, `textColor` `#777777`, ratio 4.47 | `L:381-383` - `(finding,) = ...`, `["textColor"] == "#777777"`, `["contrastRatio"] == 4.47` | ✅ PASS |
| LCR-58 `#in-plain`, shadow tree | one Finding, ratio 4.47 | `L:387-388` - `(finding,) = await reach(client, "#in-plain")`, `["contrastRatio"] == 4.47` | ✅ PASS |
| LCR-59 `#in-faded`, faded shadow host | no Finding | `L:394` - `await reach(client, "#in-faded") == []` | ✅ PASS |
| LCR-60 `#off-page` | no Finding | `L:399-400` - `"#off-page" not in [finding["selector"] ...]`, `len(findings) == 3`; `L:354-358` pins the three selectors of the fixture | ✅ PASS |

The line of LCR-51 moved from `L:301-302` to `L:302-303` (one constant was added at `L:23`); every `L` line cited in the tables of pass 1 from `L:24` on is now one further down.

**Status**: 9 of 9 match the spec outcome. With pass 1: 59 of 59 criteria due now; LCR-46 still waits for the verdict, by design. One spec-precision gap (LCR-55).

### Sensor of pass 2

Run in a temporary git worktree of `508657e` outside the repository, as in pass 1.

| # | File:line | Mutation | Result |
| - | --------- | -------- | ------ |
| S3 | `tools/detect_visual_bugs.py:110` | viewport index dropped from the sort key | ✅ Killed - `D` `test_findings_of_one_severity_come_viewport_by_viewport` |
| C3b | `js/collect_elements.js:132` | `ownTextBoxes` also gets the boxes of everything inside the element | ✅ Killed - `L` `test_only_three_texts_of_the_reach_fixture_are_reported` (`#parent` is reported) |
| V3 | `vision.py:64` | `boxes[:1]` | ✅ Killed - same test (`#two-lines` is missing) |
| G8 | `config.py:98` | `TEXT_INK_MIN` 128 → 1 | ✅ Killed - same test (`#veiled-most` is reported) |
| G8b | `config.py:98` | `TEXT_INK_MIN` 128 → 200 | ✅ Killed - same test (`#veiled-little` is missing) |
| C2 | `collect_elements.js:95` | opacity stops at a shadow root | ✅ Killed - same test (`#in-faded` is reported) |
| S7 (new) | `detect_visual_bugs.py:110` | viewport index negated | ✅ Killed - `D` `test_several_viewports_are_captured_and_reported_in_the_order_given` |
| C5 (new) | `collect_elements.js:141` | the `x` of an own-text box clamped to 0, so text left of the page is read at the page's edge | ✅ Killed - `L` `test_only_three_texts_of_the_reach_fixture_are_reported` (`#off-page` is reported) |
| V5 (new) | `vision.py:64` | `boxes[-1:]`: only the last box is sampled | ❌ Survived - the whole suite passes (188 passed) |
| C4 (new) | `collect_elements.js:139` | only the first text node of an element gets boxes | ❌ Survived - the whole suite passes (188 passed) |
| T1 (new) | `config.py:98` | `TEXT_INK_MIN` 128 → 100 | ⚠️ Survived on `L` and `D` - inside the bracket the spec sets, not a gap |
| T2 (new) | `config.py:98` | `TEXT_INK_MIN` 128 → 160 | ⚠️ Survived on `L` and `D` - inside the bracket the spec sets, not a gap |

The test named for C3b, V3, G8, G8b, C2 and C5 is the first that fails with `-x`; it pins the exact list of selectors of the fixture and runs before the test written for each criterion.

**Result**: 8/12 killed. 2 gaps (V5, C4), 2 survivors inside the specified bracket (T1, T2). F1 stays as classified in pass 1: equivalent inside the spec's scope.

**The two gaps, shown not to be equivalent.** On a probe fixture in the scratch worktree, the unmutated code reports `#three-lines` (three lines of ten glyphs, light band behind the middle one) and `#split` (`XXXXX<b></b>XXXXX`, light band behind the second half), both at 1.6. Under V5, `#three-lines` is gone. Under C4, `#split` is gone. Under V3 both are gone, so the two probe elements also keep V3 dead.

- **V5** is what a `counts` reset inside the loop would do. `#two-lines` has its band behind the last line, so sampling the last box alone gives the same Finding.
- **C4**: `#two-lines` and `#parent` each have one text node. Own text that a child splits in two (`Text <b>x</b> more text`) has no fixture, although the Terms define own text as "the text nodes", in the plural.

**T1 and T2.** LCR-56 and LCR-57 pin the threshold from both sides with layers of 0.7 and 0.3, which give ink of 76 and 178; any value from 77 to 178 passes. The Term says "at least half". A layer of exactly half gives ink of 127 or 128 depending on rounding, so the exact bound cannot be a stable fixture; the bracket is the spec's own choice and both criteria hold. If the maintainer wants it tighter, layers of 0.55 and 0.45 (ink of about 115 and 140) narrow it without touching the rounding. Not counted as a gap.

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor of pass 2 and is empty after it, apart from this report and the lessons store written afterwards; `HEAD` is `508657e` both times. The worktree was removed and `git worktree list` shows the main tree alone. `git stash` was not used.

### Gate of pass 2

`uv run pyright` exit 0 (0 errors, 0 warnings); `uv run ruff check` exit 0; `uv run ruff format --check` exit 0; `uv run pytest` exit 0 - 188 passed, 0 failed, 0 skipped, in 281.87s. 179 before the fixes, +9 (8 in `L`, 1 in `D`); nothing removed.

### Fix plan of pass 2

#### Fix 7: "all of them" of LCR-55 is pinned for one box order and one text node (V5, C4)

- **Root cause**: the one fixture of LCR-55 has a single text node whose low-contrast part is its last box.
- **Fix task**: in `low-contrast-reach.html`, either turn `#two-lines` into three lines with the light band behind the middle one, or add such an element; add an element whose own text is split by an empty child, white on black, with the light band behind the second half (`XXXXX<b></b>XXXXX`, band from 100px to 200px). State both in LCR-55 or in a new criterion, each with one Finding at 1.6, and adjust the list of `L:354-358` and the count of `L:400`.
- **Done when**: the tests fail with `boxes[-1:]` and with `boxes[:1]` at `vision.py:64`, and with the boxes of the first text node alone at `collect_elements.js:139`.
- **Priority**: Major (text split by an inline child is in most paragraphs)

### Summary of pass 2

**Overall**: ❌ Not Ready

**Spec-anchored check**: 59/59 criteria due now match the spec outcome; LCR-46 pending the verdict; 1 spec-precision gap (LCR-55)
**Sensor**: the 6 survivors of pass 1 killed; 6 new mutants, 2 killed, 2 gaps (V5, C4), 2 inside the specified bracket (T1, T2)
**Gate**: 188 passed, 0 failed; pyright, ruff check and ruff format clean

**Next steps**: route Fix 7 to an implementer, then re-verify (iteration 2 of 3).

---

## First pass (as written at `f97904b`)

**Verdict of pass 1**: FAIL

Every requirement is implemented, every assertion targets the outcome the spec defines and the gate is green. No defect was found in the source. The verdict is FAIL because the discrimination sensor left survivors, and the spec's own third success criterion asks for none "in the Check, the sampling code and the ordering of Findings": of 46 mutants, 39 were killed and 7 survived. One survivor changes nothing inside the scope of the spec (F1). The other six break a behaviour the code has on purpose and no test protects: one in the ordering of Findings (S3), four in the sampling code and the collector (C3b, V3, G8, G8b) and one in the opacity rule across a shadow root (C2). Each of the six was shown to change the tool's output on a probe fixture, so none is an equivalent mutant. The fixes are tests, fixtures and a few lines of spec wording.

Abbreviations: `L` = `tests/test_low_contrast_real.py`, `D` = `tests/test_detect_visual_bugs.py`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1: contrast thresholds | ✅ Done | `f4ce3a2` |
| T2: own-text boxes and opacity | ✅ Done | `51801ee` |
| T3: background and ink layers | ✅ Done | `c337b58` |
| T4: the Check | ✅ Done | `18750b4` |
| T5: silence rules and bounds | ✅ Done | `641edac` |
| T6: order across Checks | ✅ Done | `8031ccb`, `a2bdf27` |
| T7: documents | ✅ Done | `f97904b` |

All seven tasks are ticked in `tasks.md`. Its header still says `**Status**: In Progress` (line 12).

---

## Spec-Anchored Acceptance Criteria

### P1: Detect text with low real contrast

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-01 one Finding per failing element | exactly one Finding each | `L:37` - `(finding,) = await findings_on(client, BUG, selector, findings)` for the four elements; `L:39` - `len(findings) == 4`; `L:224` - the exact list of eight selectors of the bounds fixture | ✅ PASS |
| LCR-02 the hero over its gradient | `findings[0]` on the hero, `major`, 1.6, `#cccccc`, `background-color` `rgb(0, 0, 0)` | `L:46-50` - `first["selector"] == HERO`, `first["severity"] == "major"`, `["contrastRatio"] == 1.6`, `["sampledBackground"] == "#cccccc"`, `["computed"]["background-color"] == "rgb(0, 0, 0)"` | ✅ PASS |
| LCR-03 summary line | `Found 4 findings in 1 viewport: 1 major, 3 minor.` | `L:65` - `texts(result)[0] == "Found 4 findings in 1 viewport: 1 major, 3 minor."` | ✅ PASS |
| LCR-04 same call, same content | equal structured content | `L:69` - `await detect(client, BUG) == await detect(client, BUG)` | ✅ PASS |
| LCR-05 `#flat` | one Finding, `minor` | `L:75` - `(await finding_on(client, BUG, "#flat"))["severity"] == "minor"` | ✅ PASS |
| LCR-06 `#alpha` | `textColor` `#808080`, ratio 3.94 | `L:82-83` - `measured["textColor"] == "#808080"`, `measured["contrastRatio"] == 3.94` | ✅ PASS |
| LCR-07 `#right`, exactly 10% | one Finding | `L:237-238` - `(finding,) = await bounds(client, "#right")`, ratio `== 1.6` | ✅ PASS |
| LCR-08 `#bottom`, exactly 10% | one Finding | `L:242-243` - `(finding,) = await bounds(client, "#bottom")`, ratio `== 1.6` | ✅ PASS |
| LCR-09 `#same` | one Finding, `major`, ratio 1 | `L:259-261` - `finding["severity"] == "major"`, `["contrastRatio"] == 1` | ✅ PASS |
| LCR-10 `#nested` | one Finding, on the child | `L:265-266` - `await bounds(client, "#nested") == []`, `len(await bounds(client, "#nested-child")) == 1` | ✅ PASS as written; ⚠️ the fixture does not pin the reach (gap 2) |

### P1: Stay silent when the text can be read

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-11 clean fixture | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `L:161-165` - `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| LCR-12 `#flat` at 4.54 | no Finding | `L:175` - `await reported(client, "#flat") == []` | ✅ PASS |
| LCR-13 `#gradient` | no Finding | `L:179` - `await reported(client, "#gradient") == []` | ✅ PASS |
| LCR-14 `#left`, under 10% | no Finding | `L:249` - `await bounds(client, "#left") == []` | ✅ PASS |
| LCR-15 `#top`, under 10% | no Finding | `L:255` - `await bounds(client, "#top") == []` | ✅ PASS |
| LCR-16 `#hidden` | no Finding | `L:270` - `await bounds(client, "#hidden") == []` | ✅ PASS |
| LCR-17 `#transparent` | no Finding | `L:274` - `await bounds(client, "#transparent") == []` | ✅ PASS |
| LCR-18 `#faded` | no Finding | `L:278` - `await bounds(client, "#faded") == []` | ✅ PASS |
| LCR-19 `#faded-child` | no Finding | `L:282` - `await bounds(client, "#faded-child") == []` | ✅ PASS |
| LCR-20 `#clipped-away` | no Finding | `L:286` - `await bounds(client, "#clipped-away") == []` | ✅ PASS |
| LCR-21 `#covered` | no Finding | `L:290` - `await bounds(client, "#covered") == []` | ✅ PASS; ⚠️ only an opaque cover has an outcome (gap 4) |
| LCR-22 `#clipped-part` | no Finding | `L:296` - `await bounds(client, "#clipped-part") == []` | ✅ PASS |
| LCR-23 the Check alone on `text-clipped-bug.html` | `[]` | `L:192` - `(await detect(client, url, checks=ONLY))["findings"] == []` | ✅ PASS |

### P1: Thresholds by text size and severity

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-24 `#large`, 24px | no Finding | `L:183` - `await reported(client, "#large") == []` | ✅ PASS |
| LCR-25 `#almost-large`, 23px | `requiredRatio` 4.5, `minor` | `L:129-130` - `["requiredRatio"] == 4.5`, `finding["severity"] == "minor"` | ✅ PASS |
| LCR-26 `#large-bold`, 18.66px 700 | no Finding | `L:187` - `await reported(client, "#large-bold") == []` | ✅ PASS |
| LCR-27 `#small-bold`, 18px 700 | one Finding, `requiredRatio` 4.5 | `L:306-307` - `(finding,) = ...`, `["requiredRatio"] == 4.5` | ✅ PASS |
| LCR-28 `#semibold`, 20px 600 | one Finding, `requiredRatio` 4.5 | `L:311-312` - `(finding,) = ...`, `["requiredRatio"] == 4.5` | ✅ PASS |
| LCR-29 `#large-low` | `requiredRatio` 3, `major` | `L:316-318` - `["requiredRatio"] == 3`, `finding["severity"] == "major"` | ✅ PASS |
| LCR-47 the `major` floor | 2.99 is `major`, 3.03 is `minor` | `L:335-340` - `below[...]["contrastRatio"] == 2.99`, `below["severity"] == "major"`, `above[...]["contrastRatio"] == 3.03`, `above["severity"] == "minor"` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-30 the Finding of `#flat` | the literal of the spec | `L:89-122` - `await finding_on(client, BUG, "#flat") == {...}`, the whole object, compared key by key with the spec: equal | ✅ PASS |
| LCR-31 the 3:1 wording | message literal; suggestion ends `to reach 3:1` | `L:325-329` - `finding["message"] == "Text contrast 2.84:1 against the painted background #ffffff is below the 3:1 minimum"`, `finding["suggestion"].endswith("to reach 3:1")` | ✅ PASS |
| LCR-32 colours of the worst part | Background and Text colour at the worst-part pixel | `L:57-58` - `measured["textColor"] == "#ffffff"`, `measured["sampledBackground"] == "#cccccc"` on the hero, whose `background-color` and 80% of whose text are black | ✅ PASS |
| LCR-33 selector works in `inspect_element` | `isError: false`, same `box` | `L:144-146` - `result.is_error is False`, `result.structured_content["box"] == finding["box"]`, for the 4 Findings of the bug fixture and the 8 of the bounds fixture (`L:136` pins both counts) | ✅ PASS |

### P1: Two Checks in one call

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-34 both Checks by default | both run | `L:198-199` - `{finding["check"] ...} == {"low-contrast-real"}` and `== {"text-clipped"}` on one fixture of each; `D:442` - both Checks in one call without `checks` | ✅ PASS |
| LCR-35 unknown Check | `Unknown check "nope". Valid checks: low-contrast-real, text-clipped.` | `D:340-342` - `'Unknown check "nope". Valid checks: low-contrast-real, text-clipped.' in text`; the same literal at `D:350`, `D:358` (`zzz`) and `D:367` | ✅ PASS |
| LCR-36 `text-clipped` alone on the bug fixture | `[]` | `L:203` - `(await detect(client, BUG, checks=["text-clipped"]))["findings"] == []` | ✅ PASS |
| LCR-37 document order across Checks | the six pairs, in order | `D:441-442` - `{severity} == {"minor"}`, `[(f["selector"], f["check"]) for f in findings] == IN_DOCUMENT_ORDER` (`D:429-436`, equal to the spec's list) | ✅ PASS; ⚠️ the viewport's place in the order has no criterion (gap 1) |
| LCR-38 same element, Check name order | `low-contrast-real` before `text-clipped` | `D:450-453` - `[finding["check"] for finding in on_c] == ["low-contrast-real", "text-clipped"]` | ✅ PASS |
| LCR-39 order of `checks` changes nothing | equal structured content | `D:457-459` - `named == await detect(client, ORDER)`, `len(named["findings"]) == 6` | ✅ PASS |
| LCR-48 crops across Checks | five images, `cropIndex` 0 to 4 then `null` | `D:468-470` - pairs `== IN_DOCUMENT_ORDER`, `len(images(result)) == 5`, `[f["evidence"]["cropIndex"] ...] == [0, 1, 2, 3, 4, None]` | ✅ PASS |
| LCR-49 the description names both Checks | both names | `L:210-211` - `` "`text-clipped`" in tool.description ``, `` "`low-contrast-real`" in tool.description `` | ✅ PASS |
| LCR-50 slice 3's tests unchanged | pass, only the literal of LCR-35 differs | by reading: `git diff 9d7afb9..f97904b -- tests` changes four `Valid checks:` literals in `D` (`D:341`, `350`, `358`, `367`) and appends four tests; `test_text_clipped.py`, `test_selectors.py`, `test_inspect_element.py`, `helpers.py` and `conftest.py` are untouched; the gate passes | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| Criterion | Evidence | Result |
| --------- | -------- | ------ |
| LCR-40 one module, one function, registered | `src/squint_mcp/checks/low_contrast_real.py:152` - `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:14-17` - `"low-contrast-real": low_contrast_real.check` | ✅ PASS |
| LCR-41 no `playwright` in the Checks or in `vision.py` | `grep -rn playwright src/squint_mcp/checks src/squint_mcp/vision.py` finds nothing (exit 1) | ✅ PASS |
| LCR-42 thresholds in `config`, each cited | `src/squint_mcp/config.py:72-94`: `CONTRAST_MIN_RATIO` (73), `CONTRAST_MIN_RATIO_LARGE` (76), `LARGE_TEXT_MIN_PX` (79), `LARGE_BOLD_TEXT_MIN_PX` (82) cite WCAG 2.2 SC 1.4.3 or its "large scale" definition; `BOLD_MIN_WEIGHT` (85) cites CSS Fonts; `LOW_CONTRAST_MAJOR_BELOW_RATIO` (89) and `LOW_CONTRAST_WORST_PART_PERCENT` (94) say "Squint default" with the reason | ✅ PASS |
| LCR-43 no threshold literal in the Check | `low_contrast_real.py:98`, `105-109`, `122` read every threshold from `config`. The literals left are the WCAG luminance formula (37, 40, 46), `opacity < 1` (73), `alpha == 0` (81) and the `* 100` of a percentage (98); none is one of the seven thresholds | ✅ PASS |
| LCR-44 CHANGELOG | `CHANGELOG.md:16` (the Check), `:17` (string values of `evidence.measured`), `:21` (order across Checks), all under `## [Unreleased]` (`:7`) | ✅ PASS |
| LCR-45 README | `README.md:19` - "`detect_visual_bugs` runs two Checks: `text-clipped` ... and `low-contrast-real` ..." | ✅ PASS |
| LCR-46 roadmap `concluída` | Pending the verdict. `docs/ROADMAP.md:20` and `:86` say `pendente`, which is right while the verdict is FAIL; the orchestrator marks them after a PASS | ⏳ Pending the verdict |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| LCR-51 own text, no text pixels | no Finding | `L:301-302` - `"#no-box" not in [finding["selector"] ...]`, `len(findings) == 8` | ✅ PASS for `display: none`; ⚠️ Spec-precision gap (gap 6) |
| LCR-52 two viewports | the same `(selector, check)` in both | `L:155-156` - `len(per_viewport[0]) == 4`, `per_viewport[0] == per_viewport[1]` | ✅ PASS |

**Status**: 51 of 51 criteria due now are covered and match the spec-defined outcome; LCR-46 waits for the verdict. ⚠️ Five spec-precision gaps flagged.

### Spec-precision gaps

1. **The viewport's place in the order of Findings (LCR-37, Assumptions "Order of Findings").** The rule "severity, then the order the viewports were requested, then document order, then Check name" is stated only in the Assumptions table. LCR-37 to LCR-39 fix "the same severity and viewport", so no criterion has an outcome that depends on the viewport component. Mutant S3 lives there.
2. **The reach of "own text" (LCR-10, Assumptions "Reach").** "Each element with own text is judged on its own text pixels with its own `color`". `#nested` has a black parent and a grey child, both on white: a parent judged on its child's pixels too still passes, because black on white is 21:1 everywhere. Mutant C3b lives there.
3. **Own text in more than one box.** The Terms say "text nodes", in the plural, and the collector returns one box per line and per text node. Every fixture has one box per element. Mutant V3 lives there.
4. **How much ink makes a text pixel (Terms "Text pixels", LCR-21).** "Not covered by something painted above it" has an outcome only for an opaque cover. `TEXT_INK_MIN = 128` decides it for a translucent one and for anti-aliased edges, and no criterion names an outcome on either side of it. Mutants G8 and G8b live there. On the probe, grey text under a white layer of 30% is reported at 4.47:1, its computed colour against the layer-free background, while what is painted is lighter than that: such a Finding carries a wrong ratio, and the Out of Scope table does not list it among the known limits.
5. **Shadow trees.** The spec does not say whether the Check reaches text inside an open shadow root, nor whether a faded shadow host silences it. The design does (`design.md:29`, `:101`) and the code does both, with no test. Mutant C2 lives there.
6. **LCR-51 names three instances and pins one.** "Zero-size box, off the page, `display: none`": the test has `display: none` only. A zero-size box with a visible overflow still paints its text, so it has text pixels and is not an instance of the criterion as worded.

### Observations (not gaps)

- LCR-03's parenthesis gives the order `hero`, `#flat`, `#alpha`, `#almost-large`. The tests pin the hero at 0 (`L:46`) and `#flat` at 1 (`cropIndex`, `L:115`); the order of the last two is pinned by the general rule on `checks-order.html` (`D:442`), not on this fixture.
- `L:136` and `L:302` pin the count of the bounds fixture at 8 and `L:224` pins the eight selectors, so a Finding on any element not named by a criterion fails.
- `-webkit-text-fill-color` is inherited, shadow roots included. The style `fill_text.js` adds to each shadow root therefore matters only when a shadow tree sets that property itself, which the spec puts out of scope (see F1).

---

## Discrimination Sensor

Run in a temporary git worktree of `f97904b` outside the repository, one mutant at a time, the worktree restored with `git checkout -- .` after each. Unmutated, the worktree passes `L` and `tests/test_selectors.py` (58 passed). "Test" is the first test that fails with `-x`. A survivor was run against every test module that can reach the mutated code before it was called a survivor.

| # | File:line | Mutation | Result |
| - | --------- | -------- | ------ |
| A1 | `checks/low_contrast_real.py:160` | `ratio < required` → `ratio < required + 0.05` | ✅ Killed - `L` `test_a_page_with_adequate_contrast_has_no_findings` |
| A2 | `low_contrast_real.py:160` | `ratio < required` → `ratio < required - 0.04` | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| A3 | `low_contrast_real.py:98` | `reached * 100 >= percent * total` → `>` | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` (count of the bounds fixture) |
| A4 | `low_contrast_real.py:73` | opacity guard dropped (`opacity < 0`) | ✅ Killed - same test |
| A5 | `low_contrast_real.py:81` | alpha-0 guard dropped (`alpha < 0`) | ✅ Killed - same test |
| A6 | `low_contrast_real.py:52` | `_over` ignores alpha | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| A7 | `low_contrast_real.py:52` | `_over` truncates instead of rounding (127.5 → 127) | ✅ Killed - `L` `test_a_translucent_colour_is_judged_as_seen_over_its_background` |
| A8 | `low_contrast_real.py:121` | `math.floor(ratio * 100) / 100` → `round(ratio, 2)` | ✅ Killed - `L` `test_text_over_a_gradient_is_judged_on_the_painted_band` |
| A9 | `low_contrast_real.py:122` | `major = ratio < MAJOR_BELOW` → `ratio < required` | ✅ Killed - same test |
| A10 | `low_contrast_real.py:106` | `font_size >= LARGE_TEXT_MIN_PX` → `>` | ✅ Killed - `L` `test_a_page_with_adequate_contrast_has_no_findings` |
| A11 | `low_contrast_real.py:105` | `>= BOLD_MIN_WEIGHT` → `>` | ✅ Killed - same test |
| A12 | `low_contrast_real.py:107` | `font_size >= LARGE_BOLD_TEXT_MIN_PX` → `>` | ✅ Killed - same test |
| A13 | `low_contrast_real.py:107` | `bold and` dropped from the large-bold clause | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| A14 | `low_contrast_real.py:87-91` | parts sorted from the most readable down | ✅ Killed - same test |
| A15 | `low_contrast_real.py:99` | returns the Background of the best part | ✅ Killed - `L` `test_text_over_a_gradient_is_judged_on_the_painted_band` |
| A16 | `low_contrast_real.py:99` | returns the uncomposited text colour | ✅ Killed - `L` `test_a_translucent_colour_is_judged_as_seen_over_its_background` |
| A18 | `low_contrast_real.py:97` | `reached += count` → `+= total` (any stray pixel decides) | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| A19 | `low_contrast_real.py:83` | reads `capture.pixels` instead of `capture.background` | ✅ Killed - `L` `test_text_over_a_gradient_is_judged_on_the_painted_band` |
| G1 | `config.py:94` | `LOW_CONTRAST_WORST_PART_PERCENT` 10 → 9 | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| G1b | `config.py:94` | 10 → 11 | ✅ Killed - same test |
| G2 | `config.py:89` | `LOW_CONTRAST_MAJOR_BELOW_RATIO` 3.0 → 3.04 | ✅ Killed - `L` `test_the_summary_counts_the_findings_of_the_bug_fixture` |
| G2b | `config.py:89` | 3.0 → 2.98 | ✅ Killed - `L` `test_a_ratio_under_3_is_major_and_one_from_3_up_is_minor`, the only test that does |
| G3 | `config.py:82` | `LARGE_BOLD_TEXT_MIN_PX` 18.66 → 18.0 | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| G4 | `config.py:85` | `BOLD_MIN_WEIGHT` 700 → 600 | ✅ Killed - same test |
| G5 | `config.py:79` | `LARGE_TEXT_MIN_PX` 24.0 → 23.0 | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| G6 | `config.py:76` | `CONTRAST_MIN_RATIO_LARGE` 3.0 → 2.8 | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| G6b | `config.py:76` | 3.0 → 3.04 | ✅ Killed - `L` `test_a_page_with_adequate_contrast_has_no_findings` |
| G8 | `config.py:98` | `TEXT_INK_MIN` 128 → 1 | ❌ Survived - `L`, `D`, `test_text_clipped.py`, `test_selectors.py` all pass |
| G8b | `config.py:98` | `TEXT_INK_MIN` 128 → 200 | ❌ Survived - same four modules pass |
| V1 | `vision.py:79` | `if alpha:` → `if not alpha:` (counts the pixels that are not text) | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| V2 | `vision.py:73` | ink mask dropped (`putalpha(255)`) | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| V3 | `vision.py:64` | `for box in boxes` → `boxes[:1]` | ❌ Survived - `L`, `D`, `test_text_clipped.py`, `test_selectors.py` all pass |
| V4 | `vision.py:80` | `+= count` → `= 1` (every colour weighs the same) | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| S1 | `tools/detect_visual_bugs.py:111` | document position dropped from the sort key | ✅ Killed - `D` `test_findings_of_two_checks_come_in_document_order` |
| S2 | `detect_visual_bugs.py:112` | Check name dropped from the sort key | ✅ Killed - same test |
| S3 | `detect_visual_bugs.py:110` | viewport index dropped from the sort key | ❌ Survived - `L`, `D`, `test_text_clipped.py`, `test_selectors.py` all pass |
| S4 | `detect_visual_bugs.py:111` | document position negated | ✅ Killed - `L` `test_the_finding_carries_the_ratio_the_threshold_and_both_colours` |
| S5 | `detect_visual_bugs.py:109` | severity dropped from the sort key | ✅ Killed - `L` `test_text_over_a_gradient_is_judged_on_the_painted_band` |
| S6 | `detect_visual_bugs.py:111-112` | position and Check name swapped | ✅ Killed - `D` `test_findings_of_two_checks_come_in_document_order` |
| C1 | `js/collect_elements.js:97` | opacity ignores the ancestors | ✅ Killed - `L` `test_a_finding_selector_works_in_inspect_element` |
| C2 | `collect_elements.js:95` | opacity stops at a shadow root (`?? element.getRootNode().host` dropped) | ❌ Survived - `L`, `D`, `test_text_clipped.py`, `test_selectors.py` all pass |
| C3b | `collect_elements.js:132` | `ownTextBoxes` also gets the boxes of everything inside the element | ❌ Survived - the whole suite passes (179 passed) |
| F1 | `js/fill_text.js:11` | shadow roots not walked | ❌ Survived - `L`, `D`, `test_text_clipped.py`, `test_selectors.py` all pass; equivalent inside the spec's scope |
| P1 | `capture.py:136` | `background` is `pixels` | ✅ Killed - `L` `test_text_over_a_gradient_is_judged_on_the_painted_band` |
| P2 | `capture.py:149` | `ink` is all zero | ✅ Killed - `L` `test_each_text_below_its_ratio_yields_one_finding` |
| P3 | `capture.py:146` | `pixels` is the white-filled screenshot | ✅ Killed - `tests/test_text_clipped.py` `test_text_cut_by_a_hidden_overflow_yields_one_finding` |

A first form of C3 (element nodes let into the own-text loop) also moved `ownTextRight`, which belongs to slice 3. It was replaced by C3b, which touches `ownTextBoxes` alone, and is not counted.

**Sensor depth**: expanded (46 mutants over the Check, the sampling, the sort key, the collector, the fill script, the Capture and the thresholds)
**Result**: 39/46 killed - FAIL ❌

### The survivors, shown not to be equivalent

Each survivor was run, in the scratch worktree, on a probe fixture and on `low-contrast-bug.html` at two viewports. Unmutated, the probe gives three Findings (`#two-lines` 1.6, `#thin-veil` 4.47, `#host > p` 4.47) and the two-viewport order is hero 1440, hero 390, then the three `minor` of 1440, then the three of 390.

| Mutant | What the probe shows under it |
| ------ | ----------------------------- |
| S3 | The `minor` Findings interleave: `#flat` 1440, `#flat` 390, `#alpha` 1440, `#alpha` 390, ... The viewport order of the spec is lost |
| C3b | A new Finding on `#badge-parent` at 1:1: black text whose child is a white-on-black badge is judged on the badge's pixels |
| V3 | The Finding of `#two-lines` is gone: text on two lines whose second line is over the light band is judged on its first line only |
| G8 | A new Finding on `#veiled`: grey text under a white layer of 70% (ink 76) counts as text |
| G8b | The Finding of `#thin-veil` is gone: grey text under a white layer of 30% (ink 178) no longer counts as text |
| C2 | A new Finding on `#faded-host > p`: text in the shadow tree of a host with `opacity: 0.6` is judged |
| F1 | No change. The fill reaches the shadow tree by inheritance from the host; only a shadow tree that sets `-webkit-text-fill-color` itself would differ, and the spec puts that property out of scope. Not a gap |

**Isolation**: `git status --porcelain` of the real tree was empty before the sensor and is empty after it, and `HEAD` is `f97904b` both times. The worktree was removed and `git worktree list` shows the main tree alone. `git stash` was not used.

---

## Interactive UAT Results

Not performed: the feature has no user interface. Its surface is the MCP tool, which the tests drive.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ `inspect_element` and `ping` are untouched; the Capture gains two layers and the collector two facts, both asked for by the Check (AD-004) |
| No scope creep | ✅ |
| Matches patterns | ✅ one module per Check, thresholds in `config` with their source, tests through the tool |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met | ⚠️ every AC has its assertion; six behaviours of the code have none (the survivors) |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md`, Testing Decisions (one seam, real Chromium) | ✅ |

---

## Edge Cases

- [x] LCR-51, `display: none`: no Finding (`L:301-302`)
- [ ] LCR-51, zero-size box and off the page: no fixture (gap 6)
- [x] LCR-52: the same Findings at 1440 and at 390 (`L:155-156`)

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`, each command run with its own exit status recorded
- **Result**: pyright exit 0 (0 errors, 0 warnings); ruff check exit 0; ruff format --check exit 0; pytest exit 0 - 179 passed, 0 failed, 0 skipped, in 275.80s
- **Test count before feature**: 135
- **Test count after feature**: 179
- **Delta**: +44 (40 in `L`, 4 in `D`)
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed; the only assertions changed are the four `Valid checks:` literals LCR-35 supersedes

---

## Fix Plans

### Fix 1: The viewport component of the sort key is unprotected (S3)

- **Root cause**: no call with two viewports has two Findings of one severity at different places in the document. `D:236` has one element per severity and viewport, and `L:149-156` compares sets.
- **Fix task**: add to `spec.md` a criterion for the order on `low-contrast-bug.html` with viewports 1440 and 390: `(viewport width, selector)` equal to hero 1440, hero 390, `#flat` 1440, `#alpha` 1440, `#almost-large` 1440, `#flat` 390, `#alpha` 390, `#almost-large` 390. Add the test asserting that list in full.
- **Done when**: the test passes and fails with `index,` removed from `detect_visual_bugs.py:110`.
- **Priority**: Major

### Fix 2: The reach of own text is unprotected (C3b)

- **Root cause**: in `#nested` the parent's colour passes on the child's pixels as well.
- **Fix task**: add to `low-contrast-bounds.html` a black-on-white parent with own text and a child whose text is `rgb(255, 255, 255)` on its own `rgb(0, 0, 0)` background; a criterion and a test that neither gets a Finding; the count of `L:136`, `L:224` and `L:302` stays 8.
- **Done when**: the test fails when `ownTextBoxes` also holds the boxes of the element's descendants.
- **Priority**: Major (a badge inside a paragraph is common, and the false Finding would be 1:1, `major`)

### Fix 3: Only the first own-text box is protected (V3)

- **Root cause**: every fixture has one text box per element.
- **Fix task**: add an element whose own text wraps into two lines (20 Ahem glyphs with a space in a 200px box), white on black, with the light band behind the second line only; a criterion and a test for one Finding at 1.6.
- **Done when**: the test fails with `boxes[:1]` at `vision.py:64`.
- **Priority**: Major

### Fix 4: `TEXT_INK_MIN` has no outcome on either side (G8, G8b)

- **Root cause**: Ahem gives ink of 243 or more inside a glyph and 22 or less outside (`design.md:202`), so any threshold between passes, and 1 passes too.
- **Fix task**: decide in the spec what text under a translucent layer is. Either two criteria (grey text under a white layer of 70% gets no Finding; under one of 30% it gets one), with fixtures, or a line in Out of Scope that names translucent covers as a known limit and one criterion for the 70% case, which is the false Finding the threshold prevents.
- **Done when**: the tests fail with `TEXT_INK_MIN` at 1 and, if the 30% case is specified, at 200.
- **Priority**: Major for the 128 → 1 side (false Findings), Minor for the other

### Fix 5: Opacity across a shadow root is unprotected (C2)

- **Root cause**: no fixture has low-contrast text in a shadow tree.
- **Fix task**: add to the spec whether the Check reaches open shadow trees; if it does, a fixture with grey text in the shadow tree of a plain host (one Finding) and of a host with `opacity: 0.6` (none).
- **Done when**: the second test fails with `?? element.getRootNode().host` removed from `collect_elements.js:95`.
- **Priority**: Minor

### Fix 6: LCR-51 pins one of its three instances

- **Fix task**: add an element moved off the page (`position: absolute; left: -9999px`) to the bounds fixture and to the test of `L:299`; reword "zero-size box" as "a zero-size box that clips its text", or drop it, since `#clipped-away` already is one.
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| LCR-01 to LCR-09, LCR-11 to LCR-20, LCR-22 to LCR-36, LCR-38 to LCR-45, LCR-47 to LCR-50, LCR-52 | Implemented | ✅ Verified |
| LCR-10 | Implemented | ⚠️ Verified as written; Fix 2 pins its reach |
| LCR-21 | Implemented | ⚠️ Verified as written; Fix 4 |
| LCR-37 | Implemented | ⚠️ Verified as written; Fix 1 adds the viewport |
| LCR-51 | Implemented | ⚠️ Verified for `display: none`; Fix 6 |
| LCR-46 | Pending | Pending the verdict |

`spec.md` was not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 51/51 criteria due now match the spec outcome; LCR-46 pending the verdict; 5 spec-precision gaps plus the reach of LCR-51
**Sensor**: 39/46 mutants killed; 7 survived, 6 of them gaps, 1 equivalent inside the spec's scope
**Gate**: 179 passed, 0 failed; pyright, ruff check and ruff format clean

**What works**: the Check, its thresholds on both sides of every WCAG bound, the 10% rule on all four edges, the compositing of a translucent colour, the truncation of the ratio, the silence rules, the Finding literal, the order across Checks within a viewport and the crops.

**Issues found**: no source defect. Six behaviours without a test: the viewport's place in the order (Fix 1), the reach of own text (Fix 2), own text in several boxes (Fix 3), the ink threshold (Fix 4), opacity across a shadow root (Fix 5), two instances of LCR-51 (Fix 6).

**Next steps**: route Fix 1 to Fix 6 to an implementer, then re-verify (iteration 1 of 3). LCR-46 stays pending until that pass.
