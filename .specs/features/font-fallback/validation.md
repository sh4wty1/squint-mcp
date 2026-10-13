# font-fallback Validation

**Date**: 2026-10-13
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-62, as it is at `6cd7076`)
**Diff range**: `0b9ae25..6cd7076` (26 commits, branch `feat/font-fallback`, base `main`). The fix round is `ab1dbab..6cd7076`: it changes nothing under `src/` (`git diff --stat ab1dbab..6cd7076 -- src` is empty) and only adds lines under `tests/`
**Verifier**: independent sub-agent (author ≠ verifier), second verification pass. Not the Verifier of the first pass, and not the author of the code, of the tests or of the fix round

**Verdict**: ✅ PASS

**Result**: ✅ PASS

The 61 criteria in scope are each held by an assertion on the value the spec gives, the eight new ones (FNT-55 to FNT-62) on a page that is in the state their sentence describes. The gate is green. The sensor is satisfied as the Assumption "When the discrimination sensor is satisfied" defines it: every mutant a task names dies (the eleven of T4 to T8, the one of FNT-14 on 5 runs of 5, and the four that F1 and F3 say still die), every one of the ten mutants the first report left alive dies, each on the test written for it and on the value expected, and the fix round changed no code, so there is no mutant "of the code the last fix round changed" to ask for.

Three things the maintainer has to read, none of which changes the verdict:

1. **One defect of `src/` was found on the way, on a page no fixture holds (I-1).** A Failed family whose name holds a backslash gets no Finding: `src/squint_mcp/js/font_widths.js:45` takes the escapes off the name of a Face, which `document.fonts` gives without any. Never a wrong Finding, one that is missing, of the same kind as the hexadecimal escape the design accepts. It is in code the round did not touch and no criterion names such a family: by the Assumption it is an issue and does not fail the feature. The summary of the first pass in `tasks.md`, "found no defect in `src/`", no longer stands as written; the first report's own sentence, which is about the fixtures, does.
2. **The spec was edited by the round and the maintainer has not read the edits.** Four edits of accepted text and eight criteria. Each is judged under "The spec edits". One of them does change the letter of a Term (whitespace in "Judged element"); it says what the approved design and the code already did. This PASS is of the spec as it is at `6cd7076`.
3. **Eight of the thirteen mutants of this pass, written to attack the eight new tests from another side, pass the 53 tests.** Seven were shown to change what the tool returns on a page no fixture holds; the eighth was not, and cannot be while I-1 stands. Each is in code the round did not change and none shows a new test that does not hold the criterion it claims: by the Assumption they are residuals, listed with their exact rows.

FNT-46 (the roadmap) is the closing step T12, which runs after a PASS: it was pending when the Verifier wrote this report. T12 then ran and added the row of FNT-46 from file evidence, as the task asks; that row, the line of the traceability update and this sentence are the closing step's, and nothing else of the report was changed.

Abbreviations: `F` = `tests/test_font_fallback.py`, `D` = `tests/test_detect_visual_bugs.py`, `C` = `src/squint_mcp/checks/font_fallback.py`, `J` = `src/squint_mcp/js/font_widths.js`.

---

## Passes

| Pass | On | Outcome | Where it is kept |
| ---- | -- | ------- | ---------------- |
| 1 | `0b9ae25..ab1dbab` | FAIL. 53 of 53 criteria matched, the gate green, the 11 mutants a task names dead; 10 mutants of its own alive (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr) and 4 argued equivalent | The commit `895bd56` holds that report whole: `git show 895bd56:.specs/features/font-fallback/validation.md` |
| Fix round 1 | `ab1dbab..6cd7076` | `895bd56` tracks the first report, writes the tasks F1 to F3 and edits the spec; `c8174c5` (F1: FNT-55 to FNT-57, `font-fallback-judged.html`), `81d045f` (F2: FNT-58 to FNT-60, `font-fallback-names.html`), `76640b8` (F3: FNT-61 and FNT-62, two cases more in `font-fallback-shaping.html`), `6cd7076` (the second Linux run, under T10) | `tasks.md`, "Fixes of the first validation pass" |
| 2 | `0b9ae25..6cd7076` | PASS: this report | This file |

### What the round changed, from git

- **`src/`**: nothing. `git diff --stat ab1dbab..6cd7076 -- src` prints nothing.
- **`tests/`**: four files, 275 lines added and none removed (`git diff --numstat ab1dbab..6cd7076 -- tests`: `95 0` and `78 0` for the two new fixtures, `35 0` for `font-fallback-shaping.html`, `67 0` for `tests/test_font_fallback.py`). In the test module two constants are added at `F:27-28` and eight tests after the last one, from `F:511`; no line of an existing test is in the diff. In the shaping fixture the three hunks add two `@font-face` rules after that of `Spaced Brand`, two rules after that of `#spaced` and two elements after the last of the body: the five cases already there come before them in the flow, keep their boxes, and name none of the two new families. The tests of FNT-49 to FNT-51 pass unchanged.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff of `tests/`; 53 tests collected in the module against 45, 421 in the suite against 413; `tests/conftest.py`, `tests/helpers.py` and `pyproject.toml` are not in the diff.
- **`.specs/`**: `spec.md`, `tasks.md` and the first report. `design.md` is not in the diff.

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
| T8 | ✅ Done | The mutant it names dies on Windows, 5 runs of 5 (T8-a) |
| T9 | ✅ Done | See "FNT-36" below |
| T10 | ✅ Done | Two runs recorded by the author (45 passed on `c1aeef3`, 53 passed on `76640b8`). The module was run again here in the same image: see "Gate Check" |
| T11 | ✅ Done | `CHANGELOG.md:13`, `README.md:45` |
| F1 | ✅ Done | C16b, C5, S7 and S8 die on the tests of FNT-55 to FNT-57; C16a still dies |
| F2 | ✅ Done | C2, S1b, S1a and S2b die on the tests of FNT-58 to FNT-60 |
| F3 | ✅ Done | CFG-dir and CFG-tr die on the tests of FNT-61 and FNT-62, on Windows and in the Playwright image; CFG-tt, CFG-ls and CFG-ws still die |
| T12 | ⏳ Pending | Runs after a PASS. Not a gap |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome, and the asserted value was compared with the one the spec gives. `findings_on` and `sits_on` find an element through `inspect_element`, by its box, not by the selector the Finding carries; `of_family` unpacks exactly one Finding for a family, so "one Finding for the family" is held wherever it is used.

**The 53 rows of the first pass are carried forward.** The tests they cite did not change: the round removed no line of `F` and added two at `F:27-28`, above every line the first report cites, so each citation moved two lines down. Every moved citation was read again at HEAD and points at the assertion the row quotes; the lines of `D` and of `src/` did not move. Fourteen rows were checked again in full, the spec's sentence against the fixture and the assertion: FNT-02, FNT-14, FNT-15, FNT-16, FNT-20, FNT-23, FNT-26, FNT-27, FNT-29, FNT-30, FNT-49, FNT-50, FNT-51 and FNT-54. No row was wrong in substance. One was rewritten: FNT-38, whose count of files and whose Build are those of this range.

**The eight new rows (FNT-55 to FNT-62) are written from scratch**, and each has a line under "The state the new fixtures put the page in".

The statuses of the Faces that the fixtures' comments state are not shown by the tool. They were read here with a script outside the repository (Playwright, the Chromium arguments of `config`, Chromium 153.0.8010.12): in `font-fallback-clean.html` `Second Choice`, `Hidden Brand`, `Pseudo Brand` and `Preloaded` are `error` and `Unused`, `After Generic`, `Never Shown` and `Blank` are `unloaded`; in `font-fallback-bounds.html` `Upper Only` is `unloaded`, `Half` is `loaded` (400) and `error` (700) and the others are `error`; those of the two new fixtures and of the shaping fixture are below.

### P1: Report a font that did not load

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-01 | Exactly one Finding for the family, on the first element that falls back | `F:41` `[f["selector"] for f in findings if family(f) == "Brand"] == ["#heading"]`; `F:42-44` one Finding on `#heading`, `[]` on `#lead` and `#note` | ✅ PASS |
| FNT-02 | `(#heading, minor, Brand, 3)`, `(#icon, minor, Icon Set, 1)`, in this order | `F:51-59` the whole list `== [("#heading", "minor", "Brand", 3), ("#icon", "minor", "Icon Set", 1)]` | ✅ PASS |
| FNT-03 | Without `checks`, the first content block is the text `Found 2 findings in 1 viewport: 2 minor.` | `F:64` `texts(result)[0] == "Found 2 findings in 1 viewport: 2 minor."`. That the first text block is the first content block is held for the tool by `D:263` | ✅ PASS |
| FNT-04 | Two calls with the same arguments return equal structured content | `F:70-71` `first["findings"]` is not empty and `first == second` | ✅ PASS |
| FNT-05 | One Finding for `#scripted` with `family` `Scripted` | `F:292-294` `family(finding) == "Scripted"`, `of_family(..., "Scripted") == finding` | ✅ PASS |
| FNT-06 | One Finding for `Missing Brand`, on `#lower`, `elements` 2 | `F:298-300` `finding == await sits_on(client, BOUNDS, "#lower")`, `elements(finding) == 2` | ✅ PASS |
| FNT-07 | One Finding for `#icon`, whose only family failed | `F:78-80` one Finding on `#icon`, `check == "font-fallback"`, `family(finding) == "Icon Set"` | ✅ PASS |
| FNT-08 | One Finding for `#half-bold`, `family` `Half`, `elements` 1 | `F:306-308` `(family(finding), elements(finding)) == ("Half", 1)`, `of_family(..., "Half") == finding` | ✅ PASS |
| FNT-09 | One Finding for `#mixed-lower`, `family` `Mixed`, `elements` 1 | `F:314-316` `(family(finding), elements(finding)) == ("Mixed", 1)` | ✅ PASS |
| FNT-10 | One Finding for `Shadow Brand`, `selector` `[data-testid="shadow-text"]`, `elements` 2 | `F:323-325` `finding["selector"] == '[data-testid="shadow-text"]'`, `elements(finding) == 2` | ✅ PASS |
| FNT-11 | One Finding for `Parent Brand`, on `#own-parent`, `elements` 1, `textWidthPx` 100 | `F:359-361` `finding == await sits_on(..., "#own-parent")`, `(elements(finding), width(finding)) == (1, 100)`, nothing on `#bare-parent` | ✅ PASS |
| FNT-12 | One Finding for `Child Brand`, on `#fallen-child`, `elements` 1 | `F:368-370` `finding == await sits_on(..., "#fallen-child")`, `elements(finding) == 1`, nothing on `#clean-parent` | ✅ PASS |
| FNT-13 | `#narrow`: one Finding at 390 × 844 with `family` `Narrow Only`, none at 1440 × 900 | `F:87-91` the `(viewport, family)` of the Findings on `#narrow` or of `Narrow Only` `== [(MOBILE, "Narrow Only")]` | ✅ PASS |
| FNT-14 | Exactly one Finding, on `#code`, `family` `Brand`, `elements` 1, `textWidthPx` equal to `box.w` rounded to two places | `F:483-487` `(finding,) = findings`, `finding["selector"] == "#code"`, `(family(finding), elements(finding)) == ("Brand", 1)`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-15 | The twelve `(selector, family, elements)` in order, all `minor` | `F:269-285` the whole list of twelve, the same as the spec's; `F:286` `[...] == ["minor"] * 12` | ✅ PASS |
| FNT-50 | One Finding for `Slant`, on `#slant-italic`, `elements` 1, `computed` equal to `{"font-family": "Slant, Wide", "font-weight": "400", "font-style": "italic"}` | `F:463-471` `finding == await sits_on(..., "#slant-italic")`, `elements(finding) == 1`, `finding["evidence"]["computed"] == {...}` (the spec's literal), nothing on `#slant-normal` | ✅ PASS |
| FNT-59 | One Finding for `#comma`, with `family` equal to `Acme, Inc` | `F:543-546` `await reported(client, NAMES, families=("Acme, Inc",), on=("#comma",)) == [("#comma", "Acme, Inc")]`: the Findings that name the family or sit on the element are exactly one, on `#comma`, under the name the spec gives | ✅ PASS |
| FNT-60 | One Finding for `#inch`, with `family` equal to `Vinyl 12"`; computed `font-family` `"Vinyl 12\"", Ahem` | `F:552-555` `await reported(client, NAMES, families=('Vinyl 12"',), on=("#inch",)) == [("#inch", 'Vinyl 12"')]`; `F:556-557` `finding["evidence"]["computed"]["font-family"] == '"Vinyl 12\\"", Ahem'`, which is the spec's string, one backslash before the inner quote | ✅ PASS |

### P1: Stay silent when the text is in the font it asks for

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-16 | `isError: false`, `findings` `[]`, no image block, one text block `No findings in 1 viewport.` | `F:182-186` `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| FNT-17 | No Finding for `#undeclared` | `F:208-209` `reported(..., families=("Squint No Such Font",), on=("#undeclared",)) == []` | ✅ PASS |
| FNT-18 | No Finding for `Second Choice` | `F:215-216` `reported(..., families=("Second Choice",), on=("#second",)) == []` | ✅ PASS |
| FNT-19 | No Finding for `Preloaded` | `F:222` `reported(client, CLEAN, families=("Preloaded",)) == []` | ✅ PASS |
| FNT-20 | No Finding on `#half-normal`, and it is not counted | `F:374-375` `reported(..., on=("#half-normal",)) == []`, `elements(await of_family(..., "Half")) == 1` | ✅ PASS |
| FNT-21 | No Finding on `#wrapped`, and it is not counted | `F:381-382` `reported(..., on=("#wrapped",)) == []`, `elements(...) == 1` | ✅ PASS |
| FNT-22 | No Finding on `#mixed-both`, and it is not counted | `F:388-389` `reported(..., on=("#mixed-both",)) == []`, `elements(await of_family(..., "Mixed")) == 1` | ✅ PASS |
| FNT-23 | No Finding for `Hidden Brand` | `F:228-229` `reported(..., families=("Hidden Brand",), on=("#hidden",)) == []` | ✅ PASS |
| FNT-24 | No Finding for `Pseudo Brand` | `F:235-236` `reported(..., families=("Pseudo Brand",), on=("#pseudo",)) == []` | ✅ PASS |
| FNT-25 | No Finding for `Unused`, `After Generic`, `Never Shown`, `Blank` | `F:244-246` `reported(..., families=("Unused", "After Generic", "Never Shown", "Blank"), on=("#after-generic",)) == []` | ✅ PASS |
| FNT-26 | The Finding of `Veiled Brand` sits on `#seen`, `elements` 1 | `F:395-398` `finding == await sits_on(..., "#seen")`, `elements(finding) == 1`, nothing on `#veiled` | ✅ PASS |
| FNT-49 | No Finding on `#upper-mixed`, and it is not counted | `F:453-457` the Finding of `Mixed` has `selector` `#lower-mixed` and `elements` 1; `reported(..., on=("#upper-mixed",)) == []` | ✅ PASS |
| FNT-52 | The Finding of `Unshown Brand` sits on `#shown`, `elements` 1 | `F:403-406` `finding["selector"] == "#shown"`, `finding == await sits_on(..., "#shown")`, `elements(finding) == 1` | ✅ PASS |
| FNT-53 | No Finding for `Upper Only` | `F:347-350` `reported(..., families=("Upper Only",), on=("#out-of-range",)) == []` | ✅ PASS |
| FNT-55 | No Finding on `#broad-normal`, and it is not counted: the Finding of `Broad` sits on `#broad-bold`, `elements` 1 | `F:514-517` `finding = await of_family(client, JUDGED, "Broad")`, `(finding["selector"], elements(finding)) == ("#broad-bold", 1)`, `finding == await sits_on(client, JUDGED, "#broad-bold")`, `await reported(client, JUDGED, families=(), on=("#broad-normal",)) == []` | ✅ PASS |
| FNT-56 | The Finding of `Folded Brand` sits on `#unfolded`, `elements` 1 | `F:521-524` `(finding["selector"], elements(finding)) == ("#unfolded", 1)` for the one Finding of the family, `finding == await sits_on(client, JUDGED, "#unfolded")`, nothing on `#folded` | ✅ PASS |
| FNT-57 | The Finding of `Space Brand` sits on `#after-spaces`, `elements` 1 | `F:528-531` `(finding["selector"], elements(finding)) == ("#after-spaces", 1)` for the one Finding of the family, `finding == await sits_on(client, JUDGED, "#after-spaces")`, nothing on `#spaces` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-27 | The Finding of `#heading` equals the literal of the spec | `F:108-134` `finding == {...}`: every field of the literal compared with the spec's, one by one, and equal (message, `text`, `box` 40/20/200/30, the three computed styles, `family` `Brand`, `elements` 3, `textWidthPx` 200, `cropIndex` 0, suggestion, source) | ✅ PASS |
| FNT-28 | `The font "Icon Set" did not load: the text of 1 element is rendered in a fallback font` | `F:97-100` `finding["message"] == (...)`, the same string | ✅ PASS |
| FNT-29 | `family` `Missing Brand`; computed `font-family` `"missing brand", Ahem` | `F:330-331` `family(finding) == "Missing Brand"`, `finding["evidence"]["computed"]["font-family"] == '"missing brand", Ahem'` | ✅ PASS |
| FNT-30 | `textWidthPx` 280, `box.w` 100 | `F:411-412` `width(finding) == 280`, `finding["box"]["w"] == 100` | ✅ PASS |
| FNT-31 | `computed` equal to `{"font-family": "Half, Wide", "font-weight": "700", "font-style": "normal"}`; `textWidthPx` 300 | `F:417-422` `finding["evidence"]["computed"] == {...}` (the spec's literal), `width(finding) == 300` | ✅ PASS |
| FNT-32 | Every `selector` of the bug and bounds fixtures works in `inspect_element`, with the Finding's `box` | `F:428-440` 5 Findings of the bug fixture at two viewports and 12 of the bounds; for each `result.is_error is False` and `result.structured_content["box"] == finding["box"]` | ✅ PASS |
| FNT-51 | `textWidthPx` 226 | `F:477-478` `width(finding) == 226` | ✅ PASS |
| FNT-54 | `textWidthPx` 140, `elements` 1 | `F:446-447` `(width(finding), elements(finding)) == (140, 1)` | ✅ PASS |
| FNT-58 | One Finding for the family, on `#dual-normal`, `family` equal to `Dual`, `elements` 2 | `F:537-539` `finding = await sits_on(client, NAMES, "#dual-normal")` (exactly one Finding on the element), `(family(finding), elements(finding)) == ("Dual", 2)`, `await reported(client, NAMES, families=("DUAL",), on=("#dual-bold",)) == []`. The family has two elements: one Finding on the first, none on the second and none under the other name is one Finding for the family | ✅ PASS |
| FNT-61 | `textWidthPx` of the Finding on `#turned` equal to `box.w` rounded to two decimal places | `F:563-565` `finding = await sits_on(client, SHAPING, "#turned")`, `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of the Finding on `#swift` equal to `box.w` rounded to two decimal places | `F:571-573` `finding = await sits_on(client, SHAPING, "#swift")`, `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks` the server runs the five Checks | `F:138-142` without `checks`, the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` shows it running beside `low-contrast-real` in one call. That the other Checks run by default is held by their own slices (`tests/test_overlap.py:159`; `D:449-452`, two Checks in one call without `checks`) | ✅ PASS |
| FNT-34 | `isError: true`, text containing `Unknown check "nope". Valid checks: font-fallback, low-contrast-real, offscreen-overflow, overlap, text-clipped.` | `D:340-344` (and `D:351-355`, `D:362-366`, `D:374-378`) the literal `in text`; `D:329` `result.is_error is True`. Run here: 4 passed | ✅ PASS |
| FNT-35 | With the other four Checks named, `findings` is `[]` on the bug fixture | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | `(#a, font-fallback)`, `(#b, font-fallback)`, `(#b, low-contrast-real)`, `(#c, low-contrast-real)`, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list of four pairs, the same as the spec's. See "FNT-36" below | ✅ PASS |
| FNT-37 | The description names `font-fallback`, a font the page declares that did not load, one Finding per family | `F:156-159` `` "`font-fallback` (a font the page declares that did not load, one Finding per family)" in " ".join(tool.description.split()) `` | ✅ PASS |
| FNT-38 | The tests of earlier slices pass with no change but the four literals | `git diff 0b9ae25..6cd7076 -- tests`: eleven files, ten added (nine fixtures and `F`), one modified (`D`); the only removed lines are the eight of the four literals at `D:342`, `D:353`, `D:364`, `D:376`; no `skip` or `xfail` added. That every earlier test passes is the Build on `6cd7076`, the orchestrator's run of today: `421 passed in 1208.19s`, its log read here. `src/` has not changed since the first pass | ✅ PASS |
| FNT-39 | `isError: false`, exactly one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...["findings"]`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, a function from a Capture to Findings, registered by name | `src/squint_mcp/checks/font_fallback.py:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | A search of `src/squint_mcp/checks/` for `playwright` finds nothing; the only import of the new module is `src/squint_mcp/checks/font_fallback.py:3` (`squint_mcp.models`) | ✅ PASS |
| FNT-42 | The Check reads Faces and Line widths from the Capture; the Capture measures them only when a Check that reads them is called | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`, `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`, passed at `:103`; `src/squint_mcp/capture.py:339-343` `faces = None` unless `fonts`; `src/squint_mcp/tools/inspect_element.py:53` does not ask | ✅ PASS |
| FNT-43 | Equality, no tolerance; `config` gains no threshold | `C:67` `if widths.own == widths.tail:`; the module does not import `config` (`C:3`); the diff of `src/squint_mcp/config.py` adds `"font-style"` (`:80`) and `TEXT_SHAPING_PROPERTIES` (`:86-92`), five names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG lists the Check under the unreleased version, with the six things the criterion names | `CHANGELOG.md:13`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`): "one Finding per family"; "always `minor`"; "Only the first family ... and only when the page declares it"; not reported: "a family that is only named", "a font that loaded and is not used", "text of pseudo-elements", "text of `visibility: hidden`" | ✅ PASS |
| FNT-45 | The README names `font-fallback` and gives the number of Checks as five | `README.md:45` "`detect_visual_bugs` runs five Checks: ... and `font-fallback` (...)" | ✅ PASS |
| FNT-46 | The roadmap shows slice 9 as `concluída`, in the table and in its section, with a link to this feature's directory | `docs/ROADMAP.md:111` "| 9 | `font-fallback` | — | `tlc-spec-driven` | concluída |" and `docs/ROADMAP.md:163` "- **Status:** concluída. Spec, design e relatório de validação em [`.specs/features/font-fallback/`](../.specs/features/font-fallback/)." Added by the closing step T12 after this PASS, from the file, not by the Verifier | ✅ PASS (T12, file evidence) |

**Status**: ✅ 61 of 61 criteria in scope are covered, each with the outcome the spec gives. No criterion is held by a vague assertion and none is a spec-precision gap: SP-1 of the first report (own text that is only whitespace) is closed by the Term as edited and by FNT-57.

The file evidence of FNT-40 to FNT-45 was read again at HEAD: `C:43` is `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` and `:34` are the registry entry and `FONT_CHECKS`; a search of `src/squint_mcp/checks/` for `playwright` finds nothing; `src/squint_mcp/tools/detect_visual_bugs.py:94` and `:103`, `src/squint_mcp/capture.py:339-343` and `src/squint_mcp/tools/inspect_element.py:53` are as the row says; `C:67` is `if widths.own == widths.tail:`; `CHANGELOG.md:13` names the six things FNT-44 asks for; `README.md:45` says "five Checks".

### The state the new fixtures put the page in

Read with a script outside the repository, in Chromium 153.0.8010.12 on Windows, the same build the tests run on. Widths are of the text of the element on one line (a `Range` over its text node).

| Criterion | What the sentence says of the page | What was read |
| --------- | ---------------------------------- | ------------- |
| FNT-55 | `Broad` has a Face that loaded and one that failed; `#broad-normal` is 300px wide in the family and 200px in its Tail | Faces `Broad` 400 `loaded`, `Broad` 700 `error`. `#broad-normal`: 300px on one line, in a box 200px wide; its Tail is `Ahem`, 20px a glyph. `#broad-bold`: 200px |
| FNT-56 | `#folded` has a computed `visibility` that is neither `visible` nor `hidden`; its family failed | `Folded Brand` is `error`. `#folded`: computed `visibility` is `collapse`, its text has one box, 200px wide. `#unfolded`: `visible`, 200px |
| FNT-57 | The Own text of `#spaces` is only whitespace and paints a box | `Space Brand` is `error`. `#spaces`: `white-space: pre`, one text node of five spaces, one box 100px wide. Under S7 and S8 the tool counts it (`('#spaces', 2)`), so the Capture holds a box for it |
| FNT-58 | The first Face is `Dual`, the second `DUAL`, and both failed | `document.fonts` gives `Dual` (400, `error`) and then `DUAL` (700, `error`). `#dual-normal` and `#dual-bold` compute `Dual, Ahem`, 200px each |
| FNT-59 | The page declares `"Acme, Inc"` and it failed | The Face is named `Acme, Inc`, `error`. `#comma` computes `"Acme, Inc", Ahem` |
| FNT-60 | The family is `Vinyl 12"` and the computed `font-family` writes a backslash before the quotation mark | The Face is named `Vinyl 12"`, `error`. `#inch` computes `"Vinyl 12\"", Ahem` |
| FNT-61 | `#turned` is a block of `direction: rtl` in a font of the machine, and the full stop is not kerned with the letter before it | `Turned Brand` is `error`. `#turned`: `inline-block`, `rtl`, in Times New Roman (asked of Chromium for the node), 55.39px wide. The same text on one line is 52.81px from left to right and 55.39px from right to left |
| FNT-62 | `#swift` has `text-rendering: optimizeSpeed`, is on one line, and is in a font that has ligatures | `Swift Brand` is `error`. `#swift`: inline, one box, in Calibri, 17 glyphs for 17 characters, 113.84px wide. The same text is 112.69px with its ligatures and 113.84px with `optimizeSpeed` |

### FNT-36: the order of Findings

The note of the first report stands, and its three mutants were run again here. **Covered.**

- The criterion gives a literal outcome on a fixture it describes element by element, and `F:494-500` asserts that outcome whole.
- On the key of `src/squint_mcp/tools/detect_visual_bugs.py:120-127`, code of slice 4 that this diff does not touch: with no sort at all (O1) the test fails; with the Check name left out of the key (O3) it fails; with the Check name put before the document order (O2) it **passes**, because `font-fallback` comes first in the alphabet and its two Findings are on the first two elements.
- O2 is killed by `D:449-452` (`test_findings_of_two_checks_come_in_document_order`, slice 4). The key is one tuple for every Check and names none of them.

The test asserts what the criterion says; it could tell O2 apart only on another fixture than the one the criterion fixes. Residual R2, the maintainer's call.

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work. Each run made a fresh copy of `src/squint_mcp` under the scratch directory outside the repository, applied one mutant to the copy only (each `old` checked to occur exactly once, line endings kept) and ran `uv run pytest -x -q -p no:cacheprovider` from the repository with `PYTHONPATH` on the parent of the copy. A pytest plugin in the scratch directory aborted any run in which `squint_mcp` was not imported from the copy, and at the end of a run printed `GUARD OK` only when `squint_mcp`, `squint_mcp.capture`, `squint_mcp.config` and `squint_mcp.checks.font_fallback` were all files of the copy; every run below printed it. The unmutated copy passed first: 53 passed in 163.27s. One pytest process at a time. No `git stash`, no worktree, nothing under `src/` or `tests/` edited. The copies were deleted after the last run and `git status --porcelain` was empty again before this report was written.

**The rows.** The mutants of the first pass were read from the first Verifier's file of rows; before the first run every mutant was printed as a diff of the copy against the tree, and the ten that were alive were compared with the section "The mutants that are alive, exactly" of the first report: the same lines.

**How a mutant was run.** Against the whole module (53 tests), with the test expected to kill it moved to the front by the plugin: with `-x` a mutant that dies there dies at once, and one that does not is tried on the other 52. T6-a and T6-c were also run against each other test their task names, alone. T8-a was run 3 times against its test alone, each in a fresh browser, and 2 times against the module in its own order. "Shown" means the tool, called through the in-memory client on a page written for this pass outside the repository, returned something else with the mutant than without.

### Mutants that a task names: 15 of 15 killed

The eleven of T4 to T8, and the four that F1 and F3 say still die.

| # | Task | `file:line` | Mutation | Test that failed | Result |
| - | ---- | ----------- | -------- | ---------------- | ------ |
| T4-a | T4 | `J:100` | The family judged is the first of the list that has a Face | `F:212` (FNT-18) | ✅ Killed: `[('#second', 'Second Choice')] == []` |
| T5-a | T5 | `J:107` | The copies do not carry `font-weight` | `F:303` (FNT-08) | ✅ Killed: no Finding on `#half-bold` |
| T5-b | T5 | `J:51` and `C:51` | Both take any status but `loaded` for a Face that failed | `F:344` (FNT-53) | ✅ Killed: `[('#out-of-range', 'Upper Only')] == []` |
| T6-a | T6 | `C:67` | `if widths.own == widths.tail:` becomes `if True:` | `F:373` (FNT-20) in the module; `F:378` (FNT-21) and `F:385` (FNT-22) alone | ✅ Killed by each of the three: `[('#half-normal', 'Half')] == []`, `3 == 1`, `[('#mixed-both', 'Mixed')] == []` |
| T6-b | T6 | `J:114-115` | The copies hold the whole text content of the element | `F:357` (FNT-11) | ✅ Killed: `(1, 200.0) == (1, 100)` |
| T6-c | T6 | `C:62` | The Check does not read `visibility` | `F:392` (FNT-26) in the module; `F:225` (FNT-23) alone | ✅ Killed by both: no Finding on `#seen`; `[('#hidden', 'Hidden Brand')] == []` |
| T6-d | T6 | `C:62` | The Check does not read `own_text_boxes` | `F:401` (FNT-52) | ✅ Killed: `'#unshown' == '#shown'` |
| T6-e | T6 | `J:114-115` | Only the first text node is measured | `F:443` (FNT-54) | ✅ Killed: `(60.0, 1) == (140, 1)` |
| T6-f | T6 | `J:84` | A copy is left free to wrap | `F:409` (FNT-30) | ✅ Killed: `80.0 == 280` |
| T7-a | T7 | `J:107` | The copies do not carry `font-style` | `F:460` (FNT-50) | ✅ Killed: no Finding of `Slant` |
| T8-a | T8 | `src/squint_mcp/capture.py:313-314` | `capture()` does not call `_settle_layout` | `F:481` (FNT-14): 3 runs alone and 2 runs of the module | ✅ Killed, 5 runs of 5, always `180.03 == 164.95` (the width read after the first full screenshot, the box before it). In the module runs the 42 tests before it passed |
| C16a | F1 | `C:67` | `own <= tail` | `F:373` (FNT-20) | ✅ Killed: `[('#half-normal', 'Half')] == []` |
| CFG-tt | F3 | `src/squint_mcp/config.py:89` | `text-transform` out of `TEXT_SHAPING_PROPERTIES` | `F:450` (FNT-49) | ✅ Killed: `'#upper-mixed' == '#lower-mixed'` |
| CFG-ls | F3 | `src/squint_mcp/config.py:87` | `letter-spacing` out | `F:474` (FNT-51) | ✅ Killed: `206.0 == 226` |
| CFG-ws | F3 | `src/squint_mcp/config.py:88` | `word-spacing` out | `F:474` (FNT-51) | ✅ Killed: `220.0 == 226` |

### The ten the first report left alive: 10 of 10 killed

Each dies on the test written for it, on the value the rule gives.

| # | `file:line` | Mutation | Test that failed | Result |
| - | ----------- | -------- | ---------------- | ------ |
| C16b | `C:67` | `own >= tail` | `F:511` (FNT-55) | ✅ Killed: `('#broad-normal', 2) == ('#broad-bold', 1)` |
| C5 | `C:62` | `!= "visible"` becomes `== "hidden"` | `F:520` (FNT-56) | ✅ Killed: `('#folded', 2) == ('#unfolded', 1)` |
| C2 | `C:50` | The name of the last Face of a family is kept, not the first | `F:534` (FNT-58) | ✅ Killed: `('DUAL', 2) == ('Dual', 2)` |
| S1b | `J:23` | A quote no longer opens a string, so a comma inside one splits | `F:542` (FNT-59) | ✅ Killed: `[] == [('#comma', 'Acme, Inc')]` |
| S1a | `J:16-19` | The branch of the backslash taken out of `namesOf` | `F:549` (FNT-60) | ✅ Killed: `[] == [('#inch', 'Vinyl 12"')]` |
| S2b | `J:41` | Escapes are not taken off a name | `F:549` (FNT-60) | ✅ Killed: `[] == [('#inch', 'Vinyl 12"')]` |
| S7 | `J:95` | Text nodes of whitespace are measured too | `F:527` (FNT-57) | ✅ Killed: `('#spaces', 2) == ('#after-spaces', 1)` |
| S8 | `J:97` | `if (nodes.length === 0) return;` taken out | `F:527` (FNT-57) | ✅ Killed: `('#spaces', 2) == ('#after-spaces', 1)` |
| CFG-dir | `src/squint_mcp/config.py:91` | `direction` out of `TEXT_SHAPING_PROPERTIES` | `F:560` (FNT-61) | ✅ Killed on Windows: `52.81 == 55.39`. ✅ Killed in the Playwright image, run here: `52.81 == 55.39` |
| CFG-tr | `src/squint_mcp/config.py:90` | `text-rendering` out | `F:568` (FNT-62) | ✅ Killed on Windows: `112.69 == 113.84` (Calibri). ✅ Killed in the Playwright image, run here: `110.06 == 117.48` (FreeSerif) |

### The four the first report argued equivalent: accepted

Each was run again against the 53 tests and passes them all. I accept the four arguments, each for what it claims: the same response of the tool, not the same work in the page.

| # | `file:line` | Mutation | Result | Accepted because |
| - | ----------- | -------- | ------ | ---------------- |
| S10 | `J:101` | The script measures every element with own text, whatever its family | ➖ Survived (53 passed) | The Check keeps an element only when the family of its widths is in the set it builds itself from the same Faces (`C:51`, `C:58-60`). A width the script should not have measured is never read. What changes is the work in the page and, for a Tail that names a family the page declares and no text used, one request more: the Faces are read before any copy is made (`J:44`), so no status the Check reads moves |
| T5-b-js | `J:51` | The script alone takes any status but `loaded` | ➖ Survived (53 passed) | The same: the script measures more, the Check's own set (`C:51`) decides |
| T5-b-py | `C:51` | The Check alone takes any status but `loaded` | ➖ Survived (53 passed) | An element of a family with no Face of `error` has no `line_widths` (`J:49-53`, `J:101`) and is skipped at `C:56-57`; the wider set of the Check has nothing to add |
| S5a | `J:128` | The host is left in the page | ➖ Survived (53 passed) | The host is absolutely positioned, 0 by 0, `overflow: hidden` and `visibility: hidden` (`J:61-71`), and it is the containing block of its copies, which are absolutely positioned (`J:83`): they are clipped to nothing, paint nothing and are not hit. Only covered text reads the page after it, and each Capture has a page of its own. Equivalent in what the tool returns; the line is hygiene, and the design asks for it |

### Mutants of this pass, on what the round added: 13, of which 5 killed and 8 alive

At least one for each new test, on the same rule from another side than the mutant the test was written for.

| # | For | `file:line` | Mutation | Result |
| - | --- | ----------- | -------- | ------ |
| N55-ne | FNT-55 | `C:67` | `own != tail` | ✅ Killed by `F:511`: `('#broad-normal', 1) == ('#broad-bold', 1)` |
| N55-wider-by-under-150 | FNT-55 | `C:67` | `0 <= own - tail < 150`: a text up to 150px wider than in its Tail counts | ✅ Killed by `F:511`: `('#broad-normal', 2) == ('#broad-bold', 1)` |
| N55-within-50 | FNT-55 | `C:67` | `abs(own - tail) < 50`: a tolerance of 50px | ❌ Survived (53 passed). Shown: a text 220px wide in a loaded Face and 200px in its Tail is counted and the Finding sits on it. Residual: held from the file, by the spec's decision (FNT-43) |
| N56-collapse-only | FNT-56 | `C:62` | `!= "visible"` becomes `== "collapse"` | ✅ Killed by `F:178` (FNT-16), after `F:520` and 12 others passed: `Hidden Brand` is reported |
| N57-whitespace-beside-text | FNT-57 | `J:94-96` | Every text node of an element is measured when one of them is not whitespace | ❌ Survived (53 passed). Shown: `textWidthPx` 100 in place of 60 for a text followed, after a child, by two no-break spaces. Residual |
| N57-spaces-only | FNT-57 | `J:95` | Only U+0020 is whitespace: `nodeValue.replace(/ /g, "") !== ""` | ❌ Survived (53 passed). Shown: an element of `white-space: pre` that holds a tab, and one that holds three no-break spaces, each get the Finding of their family, `elements` 2. Residual |
| N58-first-failed-face | FNT-58 | `C:50` | The name is that of the first Face of the family that failed | ❌ Survived (53 passed). Shown: a family whose first Face is `Mark` (not failed) and whose second is `MARK` (failed) is reported as `MARK`. Residual |
| N59-tail-after-first-comma | FNT-59 | `J:104` | The Tail is the computed `font-family` after its first comma | ✅ Killed by `F:542`: `[] == [('#comma', 'Acme, Inc')]` |
| N60-unescape-quotes-only | FNT-60 | `J:41` | Only `\"` is unescaped, not every escape | ❌ Survived (53 passed). Not shown: the same rows on the page tried. It can differ only for a name that holds a backslash, which the code as it is never matches (I-1). Residual, tied to I-1 |
| N60-first-escape-only | FNT-60 | `J:41` | Only the first escape of a name is taken off | ❌ Survived (53 passed). Shown: the family `6" by 9"` loses its Finding. Residual |
| N61-always-rtl | FNT-61 | `J:85-86` | Every copy is given `direction: rtl` | ❌ Survived (53 passed). Shown: a block from left to right with the text `PLAY.` gets `textWidthPx` 55.39 for a box 52.81 wide. Residual |
| N62-always-optimize-speed | FNT-62 | `J:85-86` | Every copy is given `text-rendering: optimizeSpeed` | ❌ Survived (53 passed). Shown: `fifth office file` in Calibri with `text-rendering: auto` gets `textWidthPx` 113.84 for a box 112.69 wide. Residual |
| N61-62-width-from-box | FNT-61, FNT-62 | `C:32` | `textWidthPx` is the width of the box of the element | ✅ Killed by `F:357` (FNT-11), after `F:560`, `F:568`, `F:481` and 28 others passed: `(1, 200.0) == (1, 100)` |

A name with both a comma and an escaped quotation mark (`A", B`) is reported by the code as it is (the page of this pass: `(#both, A", B, 1)`); S1b or S1a alone loses it, and both now die. No mutant was found that passes the tests of FNT-59 and FNT-60 and loses only that name: a wrong reading of an escaped quotation mark turns the quote state over and takes the comma after the name with it, which the test of FNT-60 sees.

### Mutants of the order of Findings (FNT-36; code of slice 4, outside the diff)

| # | `file:line` | Mutation | Test(s) run | Result |
| - | ----------- | -------- | ----------- | ------ |
| O1 | `src/squint_mcp/tools/detect_visual_bugs.py:127` | No sort | `F:490` (FNT-36) | ✅ Killed |
| O2 | `src/squint_mcp/tools/detect_visual_bugs.py:123-124` | The Check name before the document order | `F:490` (FNT-36), then `D:449` | Passes `F:490`; ✅ killed by `D:449` |
| O3 | `src/squint_mcp/tools/detect_visual_bugs.py:124` | No Check name in the key | `F:490` (FNT-36) | ✅ Killed |

### The mutants that are alive, exactly

Each row is `(file under src/squint_mcp, old, new)`. The four equivalents first, then the eight residuals of this pass.

```
S10      js/font_widths.js                                  (equivalent)
         old:     if (!failed.has(family.toLowerCase())) return;
         new:     (the line removed)

S5a      js/font_widths.js                                  (equivalent)
         old:     host.remove();
         new:     (the line removed)

T5-b-js  js/font_widths.js                                  (equivalent)
         old:       .filter((face) => face.status === "error")
         new:       .filter((face) => face.status !== "loaded")

T5-b-py  checks/font_fallback.py                            (equivalent)
         old:     failed = {face.family.lower() for face in capture.faces if face.status == "error"}
         new:     failed = {face.family.lower() for face in capture.faces if face.status != "loaded"}

N55-within-50  checks/font_fallback.py                      (residual)
         old:         if widths.own == widths.tail:
         new:         if abs(widths.own - widths.tail) < 50:

N57-whitespace-beside-text  js/font_widths.js               (residual)
         old:     const nodes = [...element.childNodes].filter(
                    (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "",
                  );
         new:     const every = [...element.childNodes].filter(
                    (node) => node.nodeType === Node.TEXT_NODE,
                  );
                  const nodes = every.some((node) => node.nodeValue.trim() !== "")
                    ? every
                    : [];

N57-spaces-only  js/font_widths.js                          (residual)
         old:       (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "",
         new:       (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.replace(/ /g, "") !== "",

N58-first-failed-face  checks/font_fallback.py              (residual)
         old:         names.setdefault(face.family.lower(), face.family)
         new:         if face.status == "error":
                          names.setdefault(face.family.lower(), face.family)

N60-unescape-quotes-only  js/font_widths.js                 (residual, tied to I-1)
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\"/g, '"');

N60-first-escape-only  js/font_widths.js                    (residual)
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/s, "$1");

N61-always-rtl  js/font_widths.js                           (residual)
         old:       ...shaped,
                    ["font-family", fontFamily],
         new:       ...shaped,
                    ["direction", "rtl"],
                    ["font-family", fontFamily],

N62-always-optimize-speed  js/font_widths.js                (residual)
         old:       ...shaped,
                    ["font-family", fontFamily],
         new:       ...shaped,
                    ["text-rendering", "optimizeSpeed"],
                    ["font-family", fontFamily],
```

What the page of this pass returned, `(selector, family, elements, textWidthPx)`, without and with each mutant:

| Mutant | The code | The mutant |
| ------ | -------- | ---------- |
| N55-within-50 | `(#near-bold, Near, 1, 200)`; `#near-normal` (220px in the loaded Face, 200px in its Tail) not counted | `(#near-normal, Near, 2, 220)` |
| N57-whitespace-beside-text | `(#gap, Gap, 1, 60)`: `XXX`, a child, then two no-break spaces | `(#gap, Gap, 1, 100)` |
| N57-spaces-only | `(#after-tab, Tab, 1, 200)` and `(#after-hard, Hard, 1, 200)`; `#tab` (a tab kept by `white-space: pre`) and `#hard` (three no-break spaces) not judged | `(#tab, Tab, 2, 0)` and `(#hard, Hard, 2, 60)` |
| N58-first-failed-face | `(#mark-bold, Mark, 1, 200)` | `(#mark-bold, MARK, 1, 200)` |
| N60-unescape-quotes-only | The ten rows of the page | The same ten rows |
| N60-first-escape-only | `(#two-quotes, 6" by 9", 1, 200)` | No Finding |
| N61-always-rtl | `#ltr-block`: `textWidthPx` 52.81, `box.w` 52.81 | `textWidthPx` 55.39, `box.w` 52.81 |
| N62-always-optimize-speed | `#auto`: `textWidthPx` 112.69, `box.w` 112.69 | `textWidthPx` 113.84, `box.w` 112.69 |

### Why the eight are residuals and not gaps

The Assumption "When the discrimination sensor is satisfied" makes a mutant found alive later, in code the last fix round did not change, a residual or an issue. The round changed no code, so all eight are in such code. One thing would still make a survivor a gap: a new test that does not hold the criterion it claims. None of the eight shows that.

- **N55-within-50.** The test of FNT-55 holds its case: C16b, N55-ne and N55-wider-by-under-150 die on it. A tolerance smaller than the smallest difference of a fixture (50px, in FNT-22) is the rule of FNT-43, which the spec has the Verifier read from the file: `C:67` is `==` and the module imports no value of `config`.
- **N57-whitespace-beside-text.** FNT-57 is about an element whose Own text is only whitespace. The mutant leaves that rule whole (`#spaces` is still not measured, and the test passes for the right reason) and changes another thing: whether a text node of whitespace beside real text is added to the Line width. No criterion speaks of it. It also shows a small thing about the code: a text node of no-break spaces beside real text is left out of `textWidthPx` (R6).
- **N57-spaces-only.** The case of FNT-57 is five spaces, and the test holds it. Whitespace that is not U+0020 and still paints a box (a tab under `white-space: pre`, no-break spaces) is pinned by no case. This is the nearest of the eight to a gap: the sentence of FNT-57 says "only whitespace" and its case is one kind of it. The test asserts the outcome the criterion gives on the fixture the criterion describes, so it is a residual.
- **N58-first-failed-face.** The fixture of FNT-58 is the one its sentence describes: both Faces failed. There the first Face and the first Face that failed are the same one. A family whose first Face did not fail and is written in another case than the one that did is pinned by no case.
- **N60-first-escape-only.** The name of FNT-60 holds one quotation mark, as its sentence says. A name with two is pinned by no case.
- **N60-unescape-quotes-only.** Not shown to change anything, and not proved equivalent: see I-1.
- **N61-always-rtl, N62-always-optimize-speed.** FNT-61 and FNT-62 each hold the property where the element sets it away from its initial value, which is their sentence. No case has an element that leaves it at its initial value and whose width would show a copy that does not: a block from left to right whose text ends in a full stop, a text with ligatures and `text-rendering: auto`.

**Sensor depth**: every mutant a task or the first report names, at HEAD; at least one more for each of the eight new tests; the four equivalents and the three of the order of Findings run again
**Result**: 45 injected (15 named by a task, 10 that the first report left alive, 4 that it argued equivalent, 13 of this pass, 3 of the order of Findings). 33 killed: the 15, the 10, 5 of this pass and the 3 of the order (one of them by a test of slice 4). 12 alive: 4 equivalent, 8 residual, 0 gap. None of the 25 that a task or a report names is alive, and the round changed no code - PASS ✅

---

## I-1: a defect of `src/`, found on the way

Found while building a page for N60-unescape-quotes-only. It is the code as it is at HEAD, with no mutant.

- **What happens.** A Failed family whose name holds a backslash gets no Finding. On the page of this pass, which declares `"Back\\slash"` with a `src` that names no file and holds `#slash` (`font-family: "Back\\slash", Ahem`, ten glyphs), the Face is `error`, the text is in Ahem, 200px wide as in its Tail, and `detect_visual_bugs` returns nothing for it. The same call returns `(#two-quotes, 6" by 9", 1)` and `(#both, A", B, 1)` for its neighbours.
- **Why.** `document.fonts` gives the family of a Face without quotes and without escapes: read here, `Acme, Inc`, `Vinyl 12"`, `Back\slash` (the Assumption "The name a family is reported under" says so: "A Face gives the name without quotes (measured)"). `bare` (`J:40-41`) is written for the names of a computed `font-family`, which Chromium does write with quotes and escapes, and `J:45` applies it to the name of a Face as well. There it takes the backslash for an escape: `Back\slash` becomes `Backslash`. The First family of `#slash`, read from `"Back\\slash", Ahem`, is `Back\slash`. The two do not match (`J:101`), the element gets no widths and the family no Finding. The same line takes the quotes off a Face name that itself starts and ends with a quotation mark; that case was not run.
- **Against the spec.** By the Terms `Back\slash` is a Failed family and `#slash` falls back in it, so the rule of FNT-01 asks for a Finding. No criterion names such a family. The design accepts the same outcome for a neighbouring case, a name Chromium writes with a hexadecimal escape (`J:37-39`: "matches no Face and is never reported"), and says of it "Never a wrong Finding", which holds here too.
- **Why it does not fail the feature.** It is in code of T2 that the fix round did not touch, it was found after the first report, and it is on a page no criterion describes: by the Assumption "When the discrimination sensor is satisfied" what is found later in such code is a residual or an issue. The 61 criteria are held with their outcomes, the gate is green and the named mutants die. Read the other way, with the rule of FNT-01 held to every name a family can have, it is a gap of FNT-01 and the one gap of this pass: that reading is the maintainer's to make.
- **What it asks of the maintainer.** One of: an issue; a criterion with its case and the fix (the name of a Face taken as `document.fonts` gives it), in a round of its own; or a `ponytail:` mark and a row of the design's Risks, as the hexadecimal escape has. Severity: Minor. A family name with a backslash in it is rare, and the fault is a Finding that is missing.
- **What it changes in this report.** The first report's "No wrong Finding and no missing one was found on any fixture" still holds: no fixture has such a name. The summary of it in `tasks.md`, "found no defect in `src/`", does not. And N60-unescape-quotes-only cannot be told from the code until this is decided: the only names on which it could differ are those the code already fails to match.

---

## The spec edits

`git diff ab1dbab..6cd7076 -- .specs/features/font-fallback/spec.md`. The spec itself says of them: "the maintainer has not read them yet". Each edit of accepted text, then the new text.

| # | Edit | Does it only say what was already said? | Does the code do what it says? | Judgement |
| - | ---- | --------------------------------------- | ------------------------------ | --------- |
| E1 | Term "Judged element": "whose Own text paints at least one box" becomes "whose Own text is not only whitespace and paints at least one box" | **No: it changes the letter of an accepted Term.** Before it, own text of kept whitespace that paints a box was, by the Terms, judged and fallen back (SP-1 of the first report). The approved design said the other thing ("each element that has a text node as a direct child that is not whitespace", `design.md`, Font script) and the code has done it since T2. The edit settles a contradiction between the Term and the design on the side of the design: a rule of the spec changes, no behaviour does | Yes: `J:94-97`; FNT-57 holds it, S7 and S8 die. "Whitespace" is what `trim()` takes off: it includes the no-break space (on the page of this pass an element of three no-break spaces paints a box and is not judged) | The maintainer's to accept. I would accept it. It contradicts no other line of the spec. One sentence of `design.md` is now loose: "'Judged element' and the equality are only there" (Tech Decisions, of the Check), while this clause of the Term is held by the script and not by the Check |
| E2 | Assumptions, row "Which elements are judged": the same words added | As E1 | As E1 | With E1 |
| E3 | Out of Scope, row "Text that is not seen for another reason than `visibility`": "Only `visibility: hidden` and text that paints no box are left out" becomes "Only text whose `visibility` is not `visible`, text that paints no box and text that is only whitespace are left out" | Two changes. "`hidden`" to "not `visible`": yes, the Term has said "is `visible`" since it was accepted and the row said less than it; no rule changes. Whitespace: as E1 | Yes: `C:62` is `!= "visible"` (C5 and T6-c die); whitespace as E1 | The first half: accept, it only brings the row to the Term. The second: with E1 |
| E4 | FNT-49: the clause "and `#lower-mixed` after it, the same text without the transform, asks for the Face that failed" | Yes. It describes the fixture as it has been since T7 (`#lower-mixed` is not in the round's diff of the fixture) and what the test already read (`F:454`). No rule and no outcome changes. It closes R3 of the first report | Yes | Accept |
| E5 | New: the criteria FNT-55 to FNT-62, the paragraph of the Assumptions that tells of them, their eight rows of the traceability table, "62" in the coverage line and in the first Success Criterion | New text, not an edit: each criterion pins a rule stated before it. FNT-55: the Term "Falls back". FNT-56: the Term "Judged element". FNT-57: the design, and the Term as E1 leaves it. FNT-58: Assumptions, "The name a family is reported under". FNT-59 and FNT-60: the design ("split at the commas outside strings, a backslash taking the character after it"); the Term "Failed family" speaks of quotes only, so FNT-60 is the first line of the spec that commits the tool to a name written with an escape. FNT-61 and FNT-62: the Term "Line width" ("every style of the element that shapes text") and the design's `TEXT_SHAPING_PROPERTIES` | Yes, each: see the eight rows above | The maintainer's to accept, as FNT-52 to FNT-54 were. I find no contradiction with an accepted line, and one point to read: the row "Fixtures" of the Assumptions says "No fixture names a family that a machine can have installed", and `#swift` (FNT-62) names Calibri and FreeSerif, in its Tail, on purpose. The accepted fixture of FNT-16 already names `"Segoe UI"`, `Roboto` and `"Helvetica Neue"` in `#stack`, so the row has been read since acceptance as being about the families a page declares. FNT-62 fits that reading, and the row "Outcomes on two platforms". By the letter the row is further from true than it was: the maintainer accepts the reading or rewords the row |

Behind the edits, and cosmetic: `tasks.md:399` (the Requirement of T10 still ends at FNT-54) and the list of fixtures of `design.md`, which names seven.

---

## FNT-61 and FNT-62: what depends on the machine

Both assertions are relative to the response itself: `textWidthPx` against the `w` of the box of the same Finding, both read by `getBoundingClientRect` and rounded the same way, as FNT-14 has been since T8.

**Can either fail for another reason than a defect, on a machine that lacks the font? No.**

- **FNT-62 without Calibri and without FreeSerif.** Both lists then end in the default font: the family still changes nothing and the Finding is there. The copy and the element are in the same font with the same `text-rendering`, so the two widths are equal whatever the font. Read here with two names no machine has in place of the two fonts: 117.36px with and without `optimizeSpeed`. The one other way to fail is for `#swift` to wrap in its parent of 200px, since its box would then be narrower than its line: the text is 186.94px in the widest generic family of this machine (`monospace`), 148.77px in `cursive`, 138.11px in Verdana, 117.36px in the default font. A default font would have to be wider than a monospace of 0.59em a character.
- **FNT-61 with a `serif` that has no kerning pair for `Y` and a full stop.** The text is as wide in both directions and the assertion holds.

**What does depend on the machine is whether the mutant dies.** CFG-dir and CFG-tr die on Windows and in the Playwright image, both run here. On a machine with neither Calibri nor FreeSerif the test of FNT-62 passes with `text-rendering` in the list or out of it: there it holds the assertion and not the rule, and nothing says so. The same for FNT-61 on a `serif` without that pair.

**Is "dies on Windows and in the Playwright image" enough for the criterion as the spec writes it? Yes.** The platforms of the spec are those two (Assumptions, "The platforms the spike ran on"). Its row "Outcomes on two platforms" asks, for text in a system font, for exactly this form of assertion. FNT-62 names the two fonts in its own sentence as "a font of Windows and one of the Linux the tests run on". The fourth Success Criterion asks that the named mutants die, and they do on both. The CI's Linux is `ubuntu-latest` after `uv run playwright install --with-deps chromium` (`.github/workflows/ci.yml:16`): the driver bundled with the locked Playwright asks apt for `fonts-freefont-ttf` and `fonts-liberation` on Ubuntu 24.04 (read from the driver's own list), so FreeSerif should be there too; this was not seen on a runner. The loss of discrimination elsewhere is residual R8. The author's note offers a font file of the repository with a ligature, which would make the widths exact: the maintainer's call, not a condition of this PASS.

---

## Code Quality

Over what the round added; the rows of the first report on `src/` stand, since `src/` did not change.

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ Eight tests of three to six lines, two fixtures of six and four elements, two cases more in a third. No helper added: `of_family`, `sits_on`, `reported`, `family`, `elements` and `width` were there |
| Surgical changes | ✅ `src/` untouched. In `tests/` only added lines; the two constants `JUDGED` and `NAMES` sit with the seven others (`F:27-28`) |
| No scope creep | ✅ No parameter, no new tool behaviour, no test outside the module of the slice |
| Matches patterns | ✅ The new fixtures have the form of `font-fallback-bounds.html` (Ahem at 20px on 30px, a block 200px wide 40px from the left, one family per rule, a `src` that starts with `no-such-`, the statuses of the Faces in a comment). The tests of FNT-56 and FNT-57 have the form of that of FNT-26, those of FNT-61 and FNT-62 the form of that of FNT-14. `ruff format --check` passes |
| Every new test goes through the MCP tool boundary | ✅ Each calls `detect_visual_bugs` through the in-memory client (`detect`), and finds its element through `inspect_element` (`findings_on`); none imports from `squint_mcp` |
| Payload asserted on value, not on presence | ✅ Each asserts a selector, a family name, a count, a computed string or the equality of two widths of one Finding |
| Fixtures hold nothing no test reads | ✅ `font-fallback-judged.html`: its six elements are each read by a test of FNT-55 to FNT-57. `font-fallback-names.html`: its four by those of FNT-58 to FNT-60. The two new elements of the shaping fixture by those of FNT-61 and FNT-62 |
| Spec-anchored outcome check (asserted values match spec) | ✅ 61 of 61 |
| Per-layer Coverage Expectation met (1:1 to the criteria) | ✅ One test for each of FNT-55 to FNT-62. The three rules the first report found held from one side only (the equality, `visibility`, the name of the first Face) now have a case on the other side |
| Every test maps to a spec requirement - no unclaimed tests | ✅ 53 tests, 53 criteria: FNT-01 to FNT-39 without FNT-34 and FNT-38, and FNT-47 to FNT-62, one test each |
| Documented guidelines followed: `CONTRIBUTING.md` ("Tests have one seam: the MCP tool boundary"), `docs/SPEC.md` Testing Decisions | ✅ One seam, real Chromium, fixtures with planted problems, external behaviour only |

---

## Edge Cases

- [x] FNT-47: each Finding of the first viewport has one in the second. `F:166-175` builds the set of `(selector, check, family)` per viewport and asserts `len(desktop) == 2` and `desktop <= mobile`.
- [x] FNT-48: a family whose Faces all failed gets one Finding, on `#twice-normal`, `elements` 2. `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2`, nothing on `#twice-bold`.

---

## Gate Check

Run here, once, on `6cd7076` with a clean tree, before the sensor.

- **Gate command**: `uv run pyright`, `uv run ruff check`, `uv run ruff format --check`, `uv run pytest tests/test_font_fallback.py`, `uv run pytest --collect-only -q`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 112 files already formatted
- **The module of the slice**: 53 passed, 0 failed, 0 skipped, in 163.04s
- **The four tests of FNT-34** (`tests/test_detect_visual_bugs.py -k unknown_check`): 4 passed
- **Test count before feature**: 368 (at `28360bd`, the author's figure; 421 less the 53 tests the diff adds)
- **Test count after feature**: 421 collected
- **Delta**: +53 new tests (45 before the fix round, 8 in it)
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened. Over the whole range the diff of `tests/` removes eight lines, all of the four literals of FNT-34, each replaced by the longer literal; over the fix round it removes none.
- **The Build** (pyright, ruff check, ruff format, the whole suite): not run again here. It is the orchestrator's run of today on `6cd7076`, whose log was read whole: `0 errors, 0 warnings, 0 informations`, `All checks passed!`, `112 files already formatted`, `421 passed in 1208.19s (0:20:08)`, `BUILD_EXIT=0`, from 13:14:57 to 13:35:13. The log does not name its commit; `6cd7076` is of 13:14:17 and the name of the log carries it.
- **Linux**: the author's record under T10 is `53 passed in 153.82s` in `mcr.microsoft.com/playwright/python:v1.63.0-noble` on `76640b8` (`6cd7076` changes `tasks.md` only). Run again here, in the image of the same id (`sha256:59fe35832a79d1324e778b737760b2afc11cffcbaeba325012f96cabae832a75`), from `6cd7076` copied in as the Linux command of the gate table does: `53 passed in 155.14s`. CFG-dir and CFG-tr were then applied to the copy inside the container and each died on its test.
- **The spec's third Success Criterion** (the first run on the CI's Linux): open. It cannot be seen before a pull request.

---

## Residuals (not gaps of this slice)

- **I-1. A Failed family whose name holds a backslash gets no Finding** (`J:45`). A defect of `src/`, on a page no fixture holds. See "I-1". The maintainer decides between an issue, a criterion with the fix, and a known limit.
- **R1. The comment above `_settle_layout`** (`src/squint_mcp/capture.py:107-114`) says no test holds the call. The test of FNT-14 does on Windows: 5 runs of 5 fail without it. Known, and the maintainer's to change.
- **R2. The fixture of FNT-36** cannot tell "Check name, then document order" from the order the spec asks for; `D:449` can. See "FNT-36".
- **R3 of the first report is closed**: FNT-49 now names `#lower-mixed` (E4).
- **R4. `direction` on an inline element.** On the page it has no effect on an inline element without `unicode-bidi`; the copy is a block of its own, where it has. Measured here on the text of FNT-61: an inline `span` of `direction: rtl` with the text `PLAY.` gets `textWidthPx` 55.39 for a box 52.81 wide. Both copies move together, so no Finding is lost or gained. FNT-61 is about a block, on purpose.
- **R5. CFG-fs dies by a tool error**, not by a value (first report). Not run again here.
- **R6. A text node of no-break spaces beside real text is left out of `textWidthPx`.** The Term "Line width" adds the widths of the text nodes of the Own text; the script leaves out a node that `trim()` empties (`J:95`), and a no-break space is one. `XXX`, a child, then two no-break spaces: 60 and not 100. Both widths lack it alike.
- **R7. The eight mutants of this pass that are alive** (their rows are under "The mutants that are alive, exactly"). Each names a case a fixture could hold, if the maintainer wants it held: a tolerance below 50px (FNT-43 is read from the file today); whitespace that is not U+0020 and paints a box; whitespace beside real text; a family whose first Face did not fail and is written in another case; a name with two quotation marks, and one with a backslash once I-1 is decided; a block from left to right whose text ends in a full stop; a text with ligatures and `text-rendering: auto`. None is asked for by the Assumption.
- **R8. The tests of FNT-61 and FNT-62 tell a copy that carries the property from one that does not only where the machine has the font**: a `serif` with a kerning pair for `Y` and a full stop, and Calibri or FreeSerif. Elsewhere they pass either way. See "FNT-61 and FNT-62".
- **R9. Text behind the round**: `tasks.md:399`, the list of fixtures and one sentence of the Tech Decisions of `design.md`, the row "Fixtures" of the Assumptions (E5).
- **Not verified here**: the whole suite (the orchestrator's log, read); the CI's first run (open); the fonts of a GitHub runner (the driver's list of packages was read, no runner was); the statuses of the Faces on Linux (the author's comments in the fixtures; the 53 tests pass in the image, which they would not with other statuses for the families they report).

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-39 | Implemented | ✅ Verified |
| FNT-40 to FNT-45 | Implemented | ✅ Verified (file evidence) |
| FNT-46 | Pending | ✅ Implemented by T12 after the PASS (file evidence, `docs/ROADMAP.md:111` and `:163`) |
| FNT-47 to FNT-54 | Implemented | ✅ Verified |
| FNT-55 to FNT-62 | Implemented | ✅ Verified, as the spec words them at `6cd7076`; their text waits for the maintainer's reading (E5) |

The spec is not edited by the Verifier.

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 61 of 61 criteria matched the spec outcome; 0 spec-precision gaps; FNT-46 pending T12
**Sensor**: 33 of 45 mutants killed, every one of the 25 that a task or the first report names among them; 12 alive: 4 equivalent, 8 residual, 0 gap
**Gate**: green (pyright, ruff check, ruff format, 53 of 53 in the module on Windows and in the Playwright image, 421 collected; the Build of `6cd7076` passed with 421 tests in the orchestrator's run)

**What works**: every criterion, the eight new ones on pages that are in the state they describe; every mutant the tasks and the first report name; the order of Findings (FNT-36); the Face statuses the fixtures claim; the documents. The round added tests and changed no code.

**Issues found**: one defect of `src/` outside every fixture (I-1: a family name with a backslash gets no Finding). Eight residual mutants on cases no criterion describes. One spec edit that changes the letter of a Term (E1), and eight criteria, not yet read by the maintainer.

**Next steps**: T12 follows this PASS. The maintainer reads E1 to E5 and decides I-1 (an issue, a criterion with its fix, or a known limit). A fix of I-1 changes `src/`: its round is verified on its own, with the Build and the Linux gate. A criterion or an edit the maintainer turns down is verified again as reworded.
