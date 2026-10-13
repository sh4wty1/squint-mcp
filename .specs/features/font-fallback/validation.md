# font-fallback Validation

**Date**: 2026-10-13
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-54)
**Diff range**: `0b9ae25..ab1dbab` (21 commits, branch `feat/font-fallback`, base `main`). `src/` and `tests/` last changed in `ba860c9`; `82fa6cc` changed `CHANGELOG.md` and `README.md`; the commits after it touch `.specs/` only (`git diff --stat 82fa6cc..ab1dbab -- src tests` is empty)
**Verifier**: independent sub-agent (author ≠ verifier), first verification pass

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL

The 53 criteria in scope are all held by an assertion on the value the spec gives, the gate is green, and every mutant that a task names dies: 11 of 11, the one of FNT-14 on 7 runs of 7. The feature fails on the sensor alone. Of the 39 mutants written for this pass on the Check, the page script, the config, the Capture and the tool, 10 pass every test of the module and are not equivalent: nine were shown, on a page no fixture holds, to change what the tool returns; the tenth (`text-rendering`) was not shown to, and is not proved equivalent either. Three of them are on rules the spec states in its Terms and Assumptions:

1. **The equality of the two Line widths is held from one side only.** `own >= tail` in place of `own == tail` passes all 45 tests. Every fixture element that renders in a loaded Face of a Failed family is narrower there than in its Tail (the loaded Faces are Ahem at 20px a glyph, the Tails are `Wide` at 30px). An element in a loaded Face that is wider than its Tail is counted by the mutant and the Finding moves to it.
2. **"Judged element" is held for `visibility: hidden` only.** `== "hidden"` in place of `!= "visible"` passes all 45 tests; text of `visibility: collapse` is then judged and counted.
3. **The name of the first Face is held by no test.** With the name of the last Face of a family kept in place of the first, all 45 tests pass; no fixture has a family whose Faces write its name in two ways.

The other seven are on rules that only the design states, or that neither states: a family name that holds a comma, a name Chromium writes with a backslash, own text that is only whitespace and still paints a box, and two of the five names of `TEXT_SHAPING_PROPERTIES` (`direction`, `text-rendering`). They are listed under "Discrimination Sensor" and "Fix Plans"; the maintainer decides which become criteria and which become rows of Out of Scope.

No wrong Finding and no missing one was found on any fixture. The code does what the 53 criteria say; what is missing is tests for rules the code implements beyond them.

FNT-46 (the roadmap) is the closing step T12, which runs after a PASS. It is pending by design and is not counted as a gap.

Abbreviations: `F` = `tests/test_font_fallback.py`, `D` = `tests/test_detect_visual_bugs.py`, `C` = `src/squint_mcp/checks/font_fallback.py`, `J` = `src/squint_mcp/js/font_widths.js`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 | ✅ Done | The four literals of FNT-34 are the only lines of an earlier test module in the diff (`D:342`, `D:353`, `D:364`, `D:376`) |
| T2 | ✅ Done | `C:3` imports `models` only; `C:67` compares with `==`; the three `ponytail:` marks are at `J:37`, `J:74`, `J:102` |
| T3 | ✅ Done | `INSPECT_COMPUTED_PROPERTIES` is not in the diff; `font-style` is at `src/squint_mcp/config.py:80` |
| T4 | ✅ Done | The mutant it names dies (T4-a) |
| T5 | ✅ Done | Both mutants it names die (T5-a, T5-b); each half of T5-b alone passes, as the task says |
| T6 | ✅ Done | The six mutants it names die (T6-a to T6-f) |
| T7 | ✅ Done | The mutant it names dies (T7-a) |
| T8 | ✅ Done | The mutant it names dies on Windows, 7 runs of 7 (T8-a) |
| T9 | ✅ Done | See "FNT-36" below |
| T10 | ✅ Done | The Linux run is the author's record in `tasks.md` (45 passed in the Playwright image, on `c1aeef3`). Not re-run here |
| T11 | ✅ Done | `CHANGELOG.md:13`, `README.md:45` |
| T12 | ⏳ Pending | Runs after a PASS. Not a gap |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome, and the asserted value was compared with the one the spec gives. `findings_on` and `sits_on` find an element through `inspect_element`, by its box, not by the selector the Finding carries; `of_family` unpacks exactly one Finding for a family, so "one Finding for the family" is held wherever it is used.

The statuses of the Faces that the fixtures' comments state are not shown by the tool. They were read here with a script outside the repository (Playwright, the Chromium arguments of `config`): every one is as the spec says (`Second Choice`, `Hidden Brand`, `Pseudo Brand`, `Preloaded` are `error`; `Unused`, `After Generic`, `Never Shown`, `Blank`, `Upper Only` are `unloaded`; `Narrow Only` is `unloaded` at 1440 and `error` at 390).

### P1: Report a font that did not load

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-01 | Exactly one Finding for the family, on the first element that falls back | `F:39` `[f["selector"] for f in findings if family(f) == "Brand"] == ["#heading"]`; `F:40-42` one Finding on `#heading`, `[]` on `#lead` and `#note` | ✅ PASS |
| FNT-02 | `(#heading, minor, Brand, 3)`, `(#icon, minor, Icon Set, 1)`, in this order | `F:49-57` the whole list `== [("#heading", "minor", "Brand", 3), ("#icon", "minor", "Icon Set", 1)]` | ✅ PASS |
| FNT-03 | Without `checks`, the first content block is the text `Found 2 findings in 1 viewport: 2 minor.` | `F:62` `texts(result)[0] == "Found 2 findings in 1 viewport: 2 minor."`. That the first text block is the first content block is held for the tool by `D:263` | ✅ PASS |
| FNT-04 | Two calls with the same arguments return equal structured content | `F:68-69` `first["findings"]` is not empty and `first == second` | ✅ PASS |
| FNT-05 | One Finding for `#scripted` with `family` `Scripted` | `F:290-292` `family(finding) == "Scripted"`, `of_family(..., "Scripted") == finding` | ✅ PASS |
| FNT-06 | One Finding for `Missing Brand`, on `#lower`, `elements` 2 | `F:296-298` `finding == await sits_on(client, BOUNDS, "#lower")`, `elements(finding) == 2` | ✅ PASS |
| FNT-07 | One Finding for `#icon`, whose only family failed | `F:76-78` one Finding on `#icon`, `check == "font-fallback"`, `family(finding) == "Icon Set"` | ✅ PASS |
| FNT-08 | One Finding for `#half-bold`, `family` `Half`, `elements` 1 | `F:304-306` `(family(finding), elements(finding)) == ("Half", 1)`, `of_family(..., "Half") == finding` | ✅ PASS |
| FNT-09 | One Finding for `#mixed-lower`, `family` `Mixed`, `elements` 1 | `F:312-314` `(family(finding), elements(finding)) == ("Mixed", 1)` | ✅ PASS |
| FNT-10 | One Finding for `Shadow Brand`, `selector` `[data-testid="shadow-text"]`, `elements` 2 | `F:321-323` `finding["selector"] == '[data-testid="shadow-text"]'`, `elements(finding) == 2` | ✅ PASS |
| FNT-11 | One Finding for `Parent Brand`, on `#own-parent`, `elements` 1, `textWidthPx` 100 | `F:357-359` `finding == await sits_on(..., "#own-parent")`, `(elements(finding), width(finding)) == (1, 100)`, nothing on `#bare-parent` | ✅ PASS |
| FNT-12 | One Finding for `Child Brand`, on `#fallen-child`, `elements` 1 | `F:366-368` `finding == await sits_on(..., "#fallen-child")`, `elements(finding) == 1`, nothing on `#clean-parent` | ✅ PASS |
| FNT-13 | `#narrow`: one Finding at 390 × 844 with `family` `Narrow Only`, none at 1440 × 900 | `F:85-89` the `(viewport, family)` of the Findings on `#narrow` or of `Narrow Only` `== [(MOBILE, "Narrow Only")]` | ✅ PASS |
| FNT-14 | Exactly one Finding, on `#code`, `family` `Brand`, `elements` 1, `textWidthPx` equal to `box.w` rounded to two places | `F:481-485` `(finding,) = findings`, `finding["selector"] == "#code"`, `(family(finding), elements(finding)) == ("Brand", 1)`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-15 | The twelve `(selector, family, elements)` in order, all `minor` | `F:267-283` the whole list of twelve, the same as the spec's; `F:284` `[...] == ["minor"] * 12` | ✅ PASS |
| FNT-50 | One Finding for `Slant`, on `#slant-italic`, `elements` 1, `computed` equal to `{"font-family": "Slant, Wide", "font-weight": "400", "font-style": "italic"}` | `F:461-469` `finding == await sits_on(..., "#slant-italic")`, `elements(finding) == 1`, `finding["evidence"]["computed"] == {...}` (the spec's literal), nothing on `#slant-normal` | ✅ PASS |

### P1: Stay silent when the text is in the font it asks for

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-16 | `isError: false`, `findings` `[]`, no image block, one text block `No findings in 1 viewport.` | `F:180-184` `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| FNT-17 | No Finding for `#undeclared` | `F:206-207` `reported(..., families=("Squint No Such Font",), on=("#undeclared",)) == []` | ✅ PASS |
| FNT-18 | No Finding for `Second Choice` | `F:213-214` `reported(..., families=("Second Choice",), on=("#second",)) == []` | ✅ PASS |
| FNT-19 | No Finding for `Preloaded` | `F:220` `reported(client, CLEAN, families=("Preloaded",)) == []` | ✅ PASS |
| FNT-20 | No Finding on `#half-normal`, and it is not counted | `F:372-373` `reported(..., on=("#half-normal",)) == []`, `elements(await of_family(..., "Half")) == 1` | ✅ PASS |
| FNT-21 | No Finding on `#wrapped`, and it is not counted | `F:379-380` `reported(..., on=("#wrapped",)) == []`, `elements(...) == 1` | ✅ PASS |
| FNT-22 | No Finding on `#mixed-both`, and it is not counted | `F:386-387` `reported(..., on=("#mixed-both",)) == []`, `elements(await of_family(..., "Mixed")) == 1` | ✅ PASS |
| FNT-23 | No Finding for `Hidden Brand` | `F:226-227` `reported(..., families=("Hidden Brand",), on=("#hidden",)) == []` | ✅ PASS |
| FNT-24 | No Finding for `Pseudo Brand` | `F:233-234` `reported(..., families=("Pseudo Brand",), on=("#pseudo",)) == []` | ✅ PASS |
| FNT-25 | No Finding for `Unused`, `After Generic`, `Never Shown`, `Blank` | `F:242-244` `reported(..., families=("Unused", "After Generic", "Never Shown", "Blank"), on=("#after-generic",)) == []` | ✅ PASS |
| FNT-26 | The Finding of `Veiled Brand` sits on `#seen`, `elements` 1 | `F:393-396` `finding == await sits_on(..., "#seen")`, `elements(finding) == 1`, nothing on `#veiled` | ✅ PASS |
| FNT-49 | No Finding on `#upper-mixed`, and it is not counted | `F:451-455` the Finding of `Mixed` has `selector` `#lower-mixed` and `elements` 1; `reported(..., on=("#upper-mixed",)) == []` | ✅ PASS |
| FNT-52 | The Finding of `Unshown Brand` sits on `#shown`, `elements` 1 | `F:401-404` `finding["selector"] == "#shown"`, `finding == await sits_on(..., "#shown")`, `elements(finding) == 1` | ✅ PASS |
| FNT-53 | No Finding for `Upper Only` | `F:345-348` `reported(..., families=("Upper Only",), on=("#out-of-range",)) == []` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-27 | The Finding of `#heading` equals the literal of the spec | `F:106-132` `finding == {...}`: every field of the literal compared with the spec's, one by one, and equal (message, `text`, `box` 40/20/200/30, the three computed styles, `family` `Brand`, `elements` 3, `textWidthPx` 200, `cropIndex` 0, suggestion, source) | ✅ PASS |
| FNT-28 | `The font "Icon Set" did not load: the text of 1 element is rendered in a fallback font` | `F:95-98` `finding["message"] == (...)`, the same string | ✅ PASS |
| FNT-29 | `family` `Missing Brand`; computed `font-family` `"missing brand", Ahem` | `F:328-329` `family(finding) == "Missing Brand"`, `finding["evidence"]["computed"]["font-family"] == '"missing brand", Ahem'` | ✅ PASS |
| FNT-30 | `textWidthPx` 280, `box.w` 100 | `F:409-410` `width(finding) == 280`, `finding["box"]["w"] == 100` | ✅ PASS |
| FNT-31 | `computed` equal to `{"font-family": "Half, Wide", "font-weight": "700", "font-style": "normal"}`; `textWidthPx` 300 | `F:415-420` `finding["evidence"]["computed"] == {...}` (the spec's literal), `width(finding) == 300` | ✅ PASS |
| FNT-32 | Every `selector` of the bug and bounds fixtures works in `inspect_element`, with the Finding's `box` | `F:426-438` 5 Findings of the bug fixture at two viewports and 12 of the bounds; for each `result.is_error is False` and `result.structured_content["box"] == finding["box"]` | ✅ PASS |
| FNT-51 | `textWidthPx` 226 | `F:475-476` `width(finding) == 226` | ✅ PASS |
| FNT-54 | `textWidthPx` 140, `elements` 1 | `F:444-445` `(width(finding), elements(finding)) == (140, 1)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks` the server runs the five Checks | `F:136-140` without `checks`, the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:491-498` shows it running beside `low-contrast-real` in one call. That the other Checks run by default is held by their own slices (`tests/test_overlap.py:159`; `D:449-452`, two Checks in one call without `checks`) | ✅ PASS |
| FNT-34 | `isError: true`, text containing `Unknown check "nope". Valid checks: font-fallback, low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `D:340-344` (and `D:351-355`, `D:362-366`, `D:374-378`) the literal `in text`; `D:329` `result.is_error is True`. Run here: 4 passed | ✅ PASS |
| FNT-35 | With the other four Checks named, `findings` is `[]` on the bug fixture | `F:144-145` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | `(#a, font-fallback)`, `(#b, font-fallback)`, `(#b, low-contrast-real)`, `(#c, low-contrast-real)`, all `minor` | `F:492-498` `{severity} == {"minor"}` and the whole list of four pairs, the same as the spec's. See "FNT-36" below | ✅ PASS |
| FNT-37 | The description names `font-fallback`, a font the page declares that did not load, one Finding per family | `F:154-157` `` "`font-fallback` (a font the page declares that did not load, one Finding per family)" in " ".join(tool.description.split()) `` | ✅ PASS |
| FNT-38 | The tests of earlier slices pass with no change but the four literals | `git diff 0b9ae25..ab1dbab -- tests`: nine files, eight added, one modified; the only removed lines are the eight of the four literals at `D:342`, `D:353`, `D:364`, `D:376`; no `skip` or `xfail` added. That every earlier test passes is the Build of `82fa6cc` (413 tests), the author's record: by the maintainer's decision the whole suite was not run again, and `src/` and `tests/` have not changed since | ✅ PASS |
| FNT-39 | `isError: false`, exactly one Finding, `elements` 1000 | `F:503-506` `result.is_error is False`, `(finding,) = ...["findings"]`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, a function from a Capture to Findings, registered by name | `src/squint_mcp/checks/font_fallback.py:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | A search of `src/squint_mcp/checks/` for `playwright` finds nothing; the only import of the new module is `src/squint_mcp/checks/font_fallback.py:3` (`squint_mcp.models`) | ✅ PASS |
| FNT-42 | The Check reads Faces and Line widths from the Capture; the Capture measures them only when a Check that reads them is called | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`, `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`, passed at `:103`; `src/squint_mcp/capture.py:339-343` `faces = None` unless `fonts`; `src/squint_mcp/tools/inspect_element.py:53` does not ask | ✅ PASS |
| FNT-43 | Equality, no tolerance; `config` gains no threshold | `C:67` `if widths.own == widths.tail:`; the module does not import `config` (`C:3`); the diff of `src/squint_mcp/config.py` adds `"font-style"` (`:80`) and `TEXT_SHAPING_PROPERTIES` (`:86-92`), five names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG lists the Check under the unreleased version, with the six things the criterion names | `CHANGELOG.md:13`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`): "one Finding per family"; "always `minor`"; "Only the first family ... and only when the page declares it"; not reported: "a family that is only named", "a font that loaded and is not used", "text of pseudo-elements", "text of `visibility: hidden`" | ✅ PASS |
| FNT-45 | The README names `font-fallback` and gives the number of Checks as five | `README.md:45` "`detect_visual_bugs` runs five Checks: ... and `font-fallback` (...)" | ✅ PASS |
| FNT-46 | The roadmap shows slice 9 as `concluída` | Pending T12, which runs after a PASS | ⏳ Pending T12 |

**Status**: ✅ 53 of 53 criteria in scope are covered, each with the outcome the spec gives. No criterion is held by a vague assertion. One spec-precision gap is flagged, on a case no criterion names (SP-1, under "Discrimination Sensor").

### FNT-36: the order of Findings

The author recorded a doubt about whether the test can tell apart the orderings the spec distinguishes. Decided: **covered**.

- The criterion gives a literal outcome on a fixture it describes element by element, and `F:492-498` asserts that outcome whole. The fixture is the one the spec describes.
- Three wrong orders were tried on the key of `src/squint_mcp/tools/detect_visual_bugs.py:120-127`, which is code of slice 4 that this diff does not touch. With no sort at all (O1) the test fails. With the Check name left out of the key (O3) the test fails: on `#b` the registry gives `low-contrast-real` first. With the Check name put before the document order (O2) the test **passes**: `font-fallback` comes first in the alphabet and its two Findings are on the first two elements, so both orders give the same four pairs.
- O2 is killed by `D:449-452` (`test_findings_of_two_checks_come_in_document_order`, slice 4), whose fixture alternates two Checks down the page. The key is one tuple for every Check and names none of them, so an order that is wrong for `font-fallback` is wrong for the Checks that test holds.

So the test alone holds two of the three orders, and the suite holds the third. It is not a gap of this slice: the test asserts what the criterion says, and it could tell O2 apart only on another fixture than the one the criterion fixes. It is not a spec-precision gap either: the outcome is precise. What is true is that the fixture of FNT-36 is weaker than the sentence before it. A Finding of `font-fallback` on an element that comes after one of `low-contrast-real` would make the criterion stand alone; that is a change to the spec, and the maintainer's call (residual R2).

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work. Each run made a fresh copy of `src/squint_mcp` under the scratch directory outside the repository, applied one mutant to the copy only (each `old` checked to occur exactly once, line endings kept), and ran `uv run pytest -x -p no:cacheprovider` from the repository with `PYTHONPATH` on the copy. A pytest plugin in the scratch directory aborted any run in which `squint_mcp` or `squint_mcp.capture` was not imported from the copy; every run below printed its `GUARD OK` line. The unmutated copy passed first: 45 passed in 134.81s. One pytest process at a time. The copy was deleted after the last run and `git status --porcelain` was empty again, before this report was written. No `git stash`, no worktree, nothing under `src/` or `tests/` edited.

A mutant was run against the test that should kill it; one that was expected to live, or that I was unsure of, against the whole module. "Module" below is `tests/test_font_fallback.py`, 45 tests. A survivor was then tried on two pages written for this pass, outside the repository, through the tool and the in-memory client, with and without the mutant: "shown" means the tool returned something else with the mutant than without.

### Mutants that a task names: 11 of 11 killed

| # | Task | Mutation | Test(s) run | Result |
| - | ---- | -------- | ----------- | ------ |
| T4-a | T4 | `J:100` the family judged is the first of the list that has a Face | `F:210` (FNT-18) | ✅ Killed: `[('#second', 'Second Choice')] == []` |
| T5-a | T5 | `J:107` the copies do not carry `font-weight` | `F:301` (FNT-08) | ✅ Killed: no Finding on `#half-bold` |
| T5-b | T5 | `J:51` and `C:51` both take any status but `loaded` for a Face that failed | `F:342` (FNT-53) | ✅ Killed: `[('#out-of-range', 'Upper Only')] == []` |
| T6-a | T6 | `C:67` `if widths.own == widths.tail:` becomes `if True:` | `F:371` (FNT-20), `F:376` (FNT-21), `F:383` (FNT-22), one run each | ✅ Killed by each of the three |
| T6-b | T6 | `J:114-115` the copies hold the whole text content of the element | `F:355` (FNT-11) | ✅ Killed: `(1, 200.0) == (1, 100)` |
| T6-c | T6 | `C:62` the Check does not read `visibility` | `F:390` (FNT-26), `F:223` (FNT-23), one run each | ✅ Killed by both |
| T6-d | T6 | `C:62` the Check does not read `own_text_boxes` | `F:399` (FNT-52) | ✅ Killed: `'#unshown' == '#shown'` |
| T6-e | T6 | `J:114-115` only the first text node is measured | `F:441` (FNT-54) | ✅ Killed: `(60.0, 1) == (140, 1)` |
| T6-f | T6 | `J:84` a copy is left free to wrap | `F:407` (FNT-30) | ✅ Killed: `80.0 == 280` |
| T7-a | T7 | `J:107` the copies do not carry `font-style` | `F:458` (FNT-50) | ✅ Killed: no Finding of `Slant` |
| T8-a | T8 | `src/squint_mcp/capture.py:314` `capture()` does not call `_settle_layout` | `F:479` (FNT-14): 5 runs alone, each in a fresh browser, and 2 runs of the module | ✅ Killed, 7 runs of 7, always `180.03 == 164.95` (the width read after the first full screenshot, the box before it). In the module runs the other 42 tests before it passed |

Each half of T5-b alone passes the module, as T5 says it does (T5-b-js, T5-b-py below): the family is filtered twice by design.

### Mutants written for this pass: 39, of which 25 killed, 4 equivalent, 10 alive

| # | Mutation | Test(s) run | Result |
| - | -------- | ----------- | ------ |
| C2 | `C:50` the name of the last Face of a family is kept, not the first | Module | ❌ Survived. Shown: a family whose Faces are `Dual` and `DUAL` is reported as `DUAL` → Fix 3 |
| C3 | `C:69` the family is named as the element writes it | `F:326` (FNT-29) | ✅ Killed: `'missing brand' == 'Missing Brand'` |
| C4 | `C:58` the first family of an element is not lowered | `F:295` (FNT-06) | ✅ Killed: `1 == 2` |
| C5 | `C:62` `!= "visible"` becomes `== "hidden"` | Module | ❌ Survived. Shown: text of `visibility: collapse` is judged and counted → Fix 2 |
| C8 | `C:13` the Finding sits on the last element that falls back | `F:35` (FNT-01) | ✅ Killed: `['#note'] == ['#heading']` |
| C9 | `C:31` `elements` is always 1 | `F:45` (FNT-02) | ✅ Killed |
| C10 | `C:18` severity `major` | `F:45` (FNT-02) | ✅ Killed |
| C11a | `C:14` the message always says `elements` | `F:92` (FNT-28) | ✅ Killed |
| C11b | `C:14` the message always says `element` | `F:101` (FNT-27) | ✅ Killed |
| C12 | `C:32` `round(width)` in place of `round(width, 2)` | `F:479` (FNT-14) | ✅ Killed: `180 == 180.03` |
| C14 | `C:6` `font-style` left out of the evidence | `F:458` (FNT-50) | ✅ Killed |
| C16a | `C:67` `own <= tail` | `F:371` (FNT-20) | ✅ Killed |
| C16b | `C:67` `own >= tail` | Module | ❌ Survived. Shown: an element in a loaded Face 300px wide, 200px in its Tail, is counted and the Finding sits on it → Fix 1 |
| S1a | `J:16-18` the branch of the backslash taken out of `namesOf` | Module | ❌ Survived. Shown: the family `A", B` loses its Finding → Fix 5 |
| S1b | `J:22-24` a quote no longer opens a string, so a comma inside one splits | Module | ❌ Survived. Shown: the family `Acme, Inc` loses its Finding → Fix 4 |
| S1c | `J:25` the list is not split at commas | `F:35` (FNT-01) | ✅ Killed |
| S2a | `J:41` quotes are not taken off a name | `F:45` (FNT-02) | ✅ Killed |
| S2b | `J:41` escapes are not taken off a name | Module | ❌ Survived. Shown: the family `A", B` loses its Finding → Fix 5 |
| S4a | `J:52` and `J:101` names compared in the case they are written in | `F:295` (FNT-06) | ✅ Killed |
| S6b | `J:85` a copy carries no property of its element | `F:101` (FNT-27) | ✅ Killed |
| S7 | `J:95` text nodes of whitespace are measured too | Module | ❌ Survived. Shown: an element of `white-space: pre` whose own text is five spaces gets the Finding of its family, `elements` 2, `textWidthPx` 0 → SP-1, Fix 6 |
| S8 | `J:97` `if (nodes.length === 0) return;` taken out | Module | ❌ Survived. Shown: the same page, the same result as S7 → SP-1, Fix 6 |
| S10 | `J:101` the script measures every element with own text, whatever its family | Module | ➖ Survived, equivalent (argued below) |
| S11a | `J:104` the Tail of a list of one name is `monospace`, not `initial` | `F:72` (FNT-07) | ✅ Killed |
| S11b | `J:104` the Tail leaves out two names | `F:35` (FNT-01) | ✅ Killed |
| S12a | `J:107` the copies do not carry `font-size` | `F:101` (FNT-27) | ✅ Killed |
| S12b | `J:109` the copies carry none of `shaping` | `F:448` (FNT-49), `F:472` (FNT-51), one run each | ✅ Killed by both (`200.0 == 226`) |
| S14 | `J:124` the widths of the text nodes are not added: the widest is kept | `F:441` (FNT-54) | ✅ Killed: `(80.0, 1) == (140, 1)` |
| S5a | `J:128` the host is left in the page | Module | ➖ Survived, equivalent at the tool boundary (argued below) |
| CFG-tt | `src/squint_mcp/config.py:89` `text-transform` out of `TEXT_SHAPING_PROPERTIES` | `F:448` (FNT-49) | ✅ Killed |
| CFG-ls | `src/squint_mcp/config.py:87` `letter-spacing` out | `F:472` (FNT-51) | ✅ Killed: `206.0 == 226` |
| CFG-ws | `src/squint_mcp/config.py:88` `word-spacing` out | `F:472` (FNT-51) | ✅ Killed: `220.0 == 226` |
| CFG-tr | `src/squint_mcp/config.py:90` `text-rendering` out | Module | ❌ Survived. Not shown: the same result on every page tried → Fix 8 |
| CFG-dir | `src/squint_mcp/config.py:91` `direction` out | Module | ❌ Survived. Shown: `textWidthPx` 298.64 in place of 298.67 on a text of two scripts in an `inline-block` of `direction: rtl`, whose box is 298.67 wide → Fix 7 |
| CFG-fs | `src/squint_mcp/config.py:80` `font-style` not collected | `F:101` (FNT-27) | ✅ Killed, by a tool error and not by a value |
| K1 | `src/squint_mcp/capture.py:265` the widths go to the element before | `F:101` (FNT-27) | ✅ Killed |
| K3 | `src/squint_mcp/tools/detect_visual_bugs.py:94` fonts are measured only when `overlap` is named | `F:45` (FNT-02) | ✅ Killed |
| T5-b-js | `J:51` alone: any status but `loaded` | Module | ➖ Survived, as T5 says; equivalent (argued below) |
| T5-b-py | `C:51` alone: any status but `loaded` | Module | ➖ Survived, as T5 says; equivalent (argued below) |

The 39 rows: 25 killed (C3, C4, C8, C9, C10, C11a, C11b, C12, C14, C16a, S1c, S2a, S4a, S6b, S11a, S11b, S12a, S12b, S14, CFG-tt, CFG-ls, CFG-ws, CFG-fs, K1, K3), 4 equivalent (S10, S5a, T5-b-js, T5-b-py) and 10 alive (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr).

### Mutants of the order of Findings (FNT-36; code of slice 4, outside the diff)

| # | Mutation | Test(s) run | Result |
| - | -------- | ----------- | ------ |
| O1 | `src/squint_mcp/tools/detect_visual_bugs.py:127` no sort | `F:488` (FNT-36) | ✅ Killed |
| O2 | `src/squint_mcp/tools/detect_visual_bugs.py:123-124` the Check name before the document order | `F:488` (FNT-36), then `D:449` | Passes `F:488`; ✅ killed by `D:449` |
| O3 | `src/squint_mcp/tools/detect_visual_bugs.py:124` no Check name in the key | `F:488` (FNT-36) | ✅ Killed |

### The equivalent mutants, argued

- **S10, T5-b-js, T5-b-py: the family is filtered twice.** The script gives widths to an element only when its first family has a Face of `error` (`J:49-53`, `J:101`), and the Check keeps an element only when the family of its widths is in the set it builds itself from the same Faces with the same test (`C:51`, `C:59`). The Faces are read once, before any copy is made (`J:44`), so the two sets are of one list. Widen either filter and the other still decides: the same elements are kept. The mutants differ in how many copies the page lays out, which no response shows. On the first of the two pages written for this pass, the one with twelve cases, each returns what the code returns.
- **S5a: the host left in the page.** After the script only covered text reads the page, from pixels and by hit testing. The host is absolutely positioned at the origin, 0 by 0, with `overflow: hidden`, and it is the containing block of its copies, which are absolutely positioned too: they are clipped to nothing, paint nothing, take no place and are not hit. The context is closed when the call ends (AD-001). In the suite only the fixtures of this slice have a Face that fails (the 43 other fixtures with an `@font-face` rule all load `Ahem.ttf`, and none builds a `FontFace`: searched), so only this module can reach the line, and it was run whole: 45 passed. Equivalent in what the tool returns; the line is hygiene.

### The mutants that are alive, exactly

Each row is `(file under src/squint_mcp, old, new)`.

```
C16b  checks/font_fallback.py
      old:         if widths.own == widths.tail:
      new:         if widths.own >= widths.tail:

C5    checks/font_fallback.py
      old:         if not element.own_text_boxes or element.computed["visibility"] != "visible":
      new:         if not element.own_text_boxes or element.computed["visibility"] == "hidden":

C2    checks/font_fallback.py
      old:         names.setdefault(face.family.lower(), face.family)
      new:         names[face.family.lower()] = face.family

S1b   js/font_widths.js
      old:         quote = char;
                   name += char;
      new:         name += char;

S1a   js/font_widths.js
      old:       if (char === "\\") {
                   name += char + (fontFamily[at + 1] ?? "");
                   at++;
                 } else if (quote !== null) {
      new:       if (quote !== null) {

S2b   js/font_widths.js
      old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
      new:     name.replace(/^(["'])(.*)\1$/s, "$2");

S7    js/font_widths.js
      old:       (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "",
      new:       (node) => node.nodeType === Node.TEXT_NODE,

S8    js/font_widths.js
      old:     if (nodes.length === 0) return;
      new:     (the line removed)

CFG-dir  config.py, in TEXT_SHAPING_PROPERTIES
      old:     "direction",
      new:     (the line removed)

CFG-tr   config.py, in TEXT_SHAPING_PROPERTIES
      old:     "text-rendering",
      new:     (the line removed)
```

What the two pages returned, `(selector, family, elements, textWidthPx)`, without and with each mutant:

| Mutant | The code | The mutant |
| ------ | -------- | ---------- |
| C16b | `(#big-bold, Big, 1, 200)`; `#big-normal` (300px in the loaded Face, 200px in its Tail) not counted | `(#big-normal, Big, 2, 300)` |
| C5 | `(#seen, Gone, 1, 200)`; `#collapsed` (`visibility: collapse`) not judged | `(#collapsed, Gone, 2, 200)` |
| C2 | `(#dual-normal, Dual, 2, 200)` | `(#dual-normal, DUAL, 2, 200)` |
| S1b | `(#comma, "Acme, Inc", 1, 200)` and `(#escaped, 'A", B', 1, 200)` | Neither Finding |
| S1a, S2b | `(#escaped, 'A", B', 1, 200)` | No Finding |
| S7, S8 | `(#after-pre, Spaces, 1, 200)`; `#pre` not counted | `(#pre, Spaces, 2, 0)` |
| CFG-dir | `#rtl-block`: `textWidthPx` 298.67, `box.w` 298.67 | `textWidthPx` 298.64, `box.w` 298.67 |
| CFG-tr | Three texts in a system font at 13px with `geometricPrecision`, `optimizeLegibility`, `optimizeSpeed`, and one at 40px with `optimizeSpeed`: `textWidthPx` equal to `box.w` | The same figures |

### SP-1: a spec-precision gap, found by S7 and S8

Own text that is only whitespace and still paints a box (an element of `white-space: pre` that holds spaces) is, by the letter of the Terms, a Judged element whose two Line widths are equal: it falls back. The code leaves it out (`J:94-97`, as the design says: "a text node ... that is not whitespace") and no criterion says which is right. FNT-25 has `#blank`, whose whitespace collapses and paints nothing, and whose Face stays `unloaded`: it is silent for another reason. Flagged, not passed: the Terms need a word on it, and whichever way it is decided a case has to hold it.

### What was not attacked

- `C:44` (`capture.faces is None`): the tool asks for fonts whenever it calls the Check, so no call reaches it.
- `C:56-57` (`line_widths is None`) and `J:120` (`measured.length > 0`): without them the code fails or does the same with more work; neither is a rule.
- The styles of the host (`J:62-71`) and `all: initial` and `position: absolute` of a copy (`J:82-83`): the host and the copy each reset what the other inherits, so one alone taken out changes nothing; none is a rule of the spec.
- Where fonts are read in `capture()` relative to covered text (`src/squint_mcp/capture.py:340-346`), and the Faces read before the copies are made (`J:44`): no rule of the spec says what would differ.
- FNT-42 and FNT-43 are held from file evidence by the spec's own decision: a Capture that always measures fonts, or a tolerance smaller than the differences of the fixtures, cannot be seen through the tool.

**Sensor depth**: one mutant at least on every rule of the Check that a call can reach and on every branch of the page script, with the mutants of T4 to T8 run again
**Result**: 53 injected (11 named by a task, 39 written for this pass, 3 of the order of Findings). 39 killed: the 11 a task names, 25 of this pass, the 3 of the order (one of them by a test of slice 4). 14 alive: 4 equivalent (S10, S5a, T5-b-js, T5-b-py), 10 not (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr) - FAIL ❌

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ 69 lines of Check, 131 of script, one helper in the Capture. `text-rendering` and `direction` in `TEXT_SHAPING_PROPERTIES` come from the design and have no criterion (Fix 7, Fix 8) |
| Surgical changes | ✅ Outside the new files the diff adds: one registry entry and `FONT_CHECKS`, one keyword and one helper in `capture.py`, two models and two fields, two entries of config, one clause of the tool's docstring and three lines of the tool |
| No scope creep | ✅ No parameter, no new tool behaviour, `inspect_element` untouched (`INSPECT_COMPUTED_PROPERTIES` is not in the diff) |
| Matches patterns | ✅ `_EVIDENCE_PROPERTIES` and `_finding` as in `src/squint_mcp/checks/overlap.py`; `_measure_fonts` beside `_measure_covered_text`; `FONT_CHECKS` beside `COVERED_TEXT_CHECKS`; the tests use `helpers.py` as `tests/test_overlap.py` does |
| No single-use abstractions | ✅ `important`, `copyOf`, `namesOf` and `bare` are each used twice; the test helpers `reported`, `of_family`, `sits_on` are used throughout |
| Spec-anchored outcome check (asserted values match spec) | ✅ 53 of 53 |
| Payload asserted on value, not on presence | ✅ FNT-27 compares the whole Finding; every other test compares a value |
| Per-layer Coverage Expectation met (1:1 to the criteria) | ⚠️ 1:1 to the criteria, yes. Three rules of the Terms and Assumptions have no criterion that holds them from both sides (Fix 1 to Fix 3) |
| Every test maps to a spec requirement - no unclaimed tests | ✅ 45 tests, 45 criteria: FNT-01 to FNT-39 without FNT-34 and FNT-38, and FNT-47 to FNT-54, one test each |
| Documented guidelines followed: `CONTRIBUTING.md`, `docs/SPEC.md` Testing Decisions | ✅ One seam: every test goes through the in-memory MCP client; no test of an internal helper |

---

## Edge Cases

- [x] FNT-47: each Finding of the first viewport has one in the second. `F:164-173` builds the set of `(selector, check, family)` per viewport and asserts `len(desktop) == 2` and `desktop <= mobile`.
- [x] FNT-48: a family whose Faces all failed gets one Finding, on `#twice-normal`, `elements` 2. `F:335-339` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2`, nothing on `#twice-bold`.

---

## Gate Check

Run here, once, on `ab1dbab`, before the sensor.

- **Gate command**: `uv run pyright`, `uv run ruff check`, `uv run ruff format --check`, `uv run pytest tests/test_font_fallback.py`, `uv run pytest --collect-only -q`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 111 files already formatted
- **The module of the slice**: 45 passed, 0 failed, 0 skipped, in 143.73s
- **The four tests of FNT-34** (`tests/test_detect_visual_bugs.py -k unknown_check`): 4 passed
- **Test count before feature**: 368 (at `28360bd`, the author's figure; 413 less the 45 tests the diff adds)
- **Test count after feature**: 413 collected
- **Delta**: +45 new tests
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test of an earlier slice deleted, skipped or weakened. The diff of `tests/` removes eight lines, all of the four literals of FNT-34, and each is replaced by the longer literal.
- **The whole suite**: not run here, by the maintainer's decision. It passed on `82fa6cc` (413 tests, 24 minutes; the author's record in `.specs/STATE.md`), and `src/` and `tests/` have not changed since: confirmed.
- **Linux**: the module passed in the Playwright image for Docker (45 passed, on `c1aeef3`): the author's record under T10, not re-run here.
- **The spec's third Success Criterion** (the first run on the CI's Linux): open. It cannot be seen before a pull request.

---

## Fix Plans

Each says what has to be true after the fix, not how. A new criterion is the maintainer's to accept, as FNT-52 to FNT-54 were; no existing test is to be weakened, skipped or deleted.

### Fix 1: A loaded Face that is wider than the Tail (C16b)

- **Root cause**: in FNT-20, FNT-21, FNT-22, FNT-49 and the `#slant-normal` of FNT-50 the loaded Face is Ahem and the Tail is `Wide`: the element is always narrower in its family than in its Tail, so `>=` reads as `==`.
- **Fix task**: a test fails when an element whose Line width in its `font-family` is greater than in its Tail is counted. Verify: C16b dies, and C16a still does.
- **Priority**: Major. It is the comparison the Check exists for

### Fix 2: `visibility` other than `visible` and `hidden` (C5)

- **Root cause**: FNT-23 and FNT-26 hold `visibility: hidden`; the Term says "is `visible`".
- **Fix task**: a test fails when an element whose computed `visibility` is `collapse` is judged. Verify: C5 dies.
- **Priority**: Minor

### Fix 3: The name of the first Face (C2)

- **Root cause**: no fixture has a family whose Faces write its name in two ways, so "the first of its Faces" (Assumptions, "The name a family is reported under") is the same as any other.
- **Fix task**: a test fails when a family is reported under the name of another of its Faces than the first. Verify: C2 dies.
- **Priority**: Minor

### Fix 4: A family name that holds a comma (S1b)

- **Root cause**: no fixture names a family with a comma inside its quotes; the design asks for "the commas outside strings".
- **Fix task**: a test fails when a quoted family name that holds a comma is split in two. Verify: S1b dies.
- **Priority**: Minor

### Fix 5: A family name Chromium writes with a backslash (S1a, S2b)

- **Root cause**: no fixture names a family that holds a quote or a backslash. The design asks for both lines ("a backslash taking the character after it", "without ... the escapes"); the spec's Terms speak of quotes only.
- **Fix task**: either a test fails when such a name is not matched to its Face, or the spec says such names are not matched, as it already says of a hexadecimal escape, and the code does not claim to. Verify: S1a and S2b die, or have no line left to change.
- **Priority**: Minor

### Fix 6: Own text that is only whitespace and paints a box (S7, S8; SP-1)

- **Root cause**: the Terms do not say whether such an element is judged; the code says no.
- **Fix task**: the spec says which, and a test fails when the other happens. Verify: S7 and S8 die.
- **Priority**: Minor

### Fix 7: `direction` carried by a copy (CFG-dir)

- **Root cause**: no fixture has text whose width on one line depends on `direction`. The difference shown is 0.03px of 298.67.
- **Fix task**: either a test fails when a copy does not carry `direction`, on an outcome that is the same on Windows and on Linux, or the name leaves the list. Read residual R4 first: on an inline element the copy that carries it is the one that is off. Verify: CFG-dir dies, or has no line left to change.
- **Priority**: Minor

### Fix 8: `text-rendering` carried by a copy (CFG-tr)

- **Root cause**: no page was found on which it changes a width in this Chromium.
- **Fix task**: the same as Fix 6, for `text-rendering`. If no page shows a difference, the maintainer accepts it as equivalent or takes the name out. Verify: CFG-tr dies, is argued equivalent, or has no line left to change.
- **Priority**: Cosmetic

---

## Residuals (not gaps of this slice)

- **R1. The comment above `_settle_layout`** (`src/squint_mcp/capture.py:110-114`) says no test holds the call. The test of FNT-14 now does on Windows: 7 runs of 7 fail without it. The comment is the maintainer's to change.
- **R2. The fixture of FNT-36** cannot tell "Check name, then document order" from the order the spec asks for; `D:449` can. See "FNT-36".
- **R3. The spec's text of FNT-49** does not name `#lower-mixed`, which the fixture needs for `Mixed` to be a Failed family at all and which the test reads (`F:452`). `tasks.md` (T7) says why. The spec could say it.
- **R4. `direction` on an inline element.** On the page it has no effect on an inline element without `unicode-bidi`; the copy is a block of its own, where it has. For an inline `span` of `direction: rtl` with text of two scripts the code gives `textWidthPx` 298.67 for a box 298.64 wide. Both copies move together, so no Finding is lost or gained.
- **R5. CFG-fs dies by a tool error**, not by a value: with `font-style` not collected the Check fails on a missing key.
- **Not verified here**: the whole suite and the Linux run (the author's records), the CI's first run (open).

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-39 | Implemented | ✅ Verified |
| FNT-40 to FNT-45 | Implemented | ✅ Verified (file evidence) |
| FNT-46 | Pending | Pending T12 |
| FNT-47 to FNT-54 | Implemented | ✅ Verified |

The spec is not edited by the Verifier. The criteria a fix round adds are verified in the next pass.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 53 of 53 criteria matched the spec outcome; 1 spec-precision gap (SP-1); FNT-46 pending T12
**Sensor**: 39 of 53 mutants killed; 4 equivalent; 10 alive, none of them named by a task
**Gate**: green (pyright, ruff check, ruff format, 45 of 45 in the module, 413 collected)

**What works**: every criterion; every mutant the tasks name; the order of Findings (FNT-36); the Face statuses the fixtures claim; the documents.

**Issues found**: eight fix plans for ten mutants. Fix 1 first (the equality held from one side), then Fix 2 and Fix 3 (rules of the Terms and Assumptions), then Fix 6 (the spec has to say), then Fix 4, Fix 5, Fix 7 and Fix 8 (rules of the design alone).

**Next steps**: the maintainer decides, for each of the eight, between a criterion with a case and a row of Out of Scope; the fix round follows, then the Linux gate and the Build if `src/` or `tests/` change, then a second pass of the Verifier on the mutants this report names.
