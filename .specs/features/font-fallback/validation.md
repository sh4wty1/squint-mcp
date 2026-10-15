# font-fallback Validation

**Date**: 2026-10-15
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-64, as it is at `8dc0ead`)
**Diff range**: `f5ec283..8dc0ead` (6 commits, branch `fix/font-name-backslash`, base `main`). `4015689` is a lessons commit outside the feature; `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4; `135f9a8` is the third pass (FAIL); `e598bb8` adds FNT-64 and plans F5; `8dc0ead` is F5. Across the range `src/` changes in one line (`src/squint_mcp/js/font_widths.js:46`, with a comment above it), all of it in F4; F5 changes no `src/`
**Verifier**: independent sub-agent (author ≠ verifier), fourth verification pass. Not the Verifier of an earlier pass, and not the author of the code, of the tests or of the spec edits

**Verdict**: ✅ PASS

**Result**: ✅ PASS - 64 of 64 criteria held on the outcome the spec gives; the gate green on Windows and in the Playwright image; every mutant a report or a task names dies, FACE-UNQUOTE-ONLY among them; one mutant of this pass's own is alive, a residual under the Assumption "When the discrimination sensor is satisfied" (R1)

F5 does what the third pass asked. The case `#quoted` holds a family whose name starts and ends with a quotation mark, and its test kills FACE-UNQUOTE-ONLY, the mutant that failed the third pass, on `[] == [('#quoted', '"Quoted"')]`. Issue #20 is fixed on both platforms: the Faces of `N` were read here on Windows and, for the first time, in the Playwright image, and they are the same, `Back\slash` and `"Quoted"` included.

One mutant of this pass's own lives. **FACE-UNQUOTE-SINGLE-ONLY** takes the apostrophes off a Face name that starts and ends with one, and passes the 55 tests. It is not equivalent: a family declared as `"'Single'"` gets its Finding with the code and loses it with the mutant. It counts as a residual, not a gap. The last fix round, F5, changed no code, so this mutant is not of "the code the last fix round changed". It is "one found alive later", which the Assumption keeps out of the verdict. Read the other way, with F4 and F5 as one round, it would fail the pass as FACE-UNQUOTE-ONLY failed the third. The maintainer decides (R1).

Abbreviations: `F` = `tests/test_font_fallback.py`, `D` = `tests/test_detect_visual_bugs.py`, `C` = `src/squint_mcp/checks/font_fallback.py`, `J` = `src/squint_mcp/js/font_widths.js`, `N` = `tests/fixtures/font-fallback-names.html`.

---

## Passes

| Pass | On | Outcome | Where it is kept |
| ---- | -- | ------- | ---------------- |
| 1 | `0b9ae25..ab1dbab` | FAIL. 53 of 53 criteria matched, the gate green, the 11 mutants a task names dead; 10 mutants of its own alive (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr) and 4 argued equivalent | `git show 895bd56:.specs/features/font-fallback/validation.md` |
| Fix round 1 | `ab1dbab..6cd7076` | F1 to F3: FNT-55 to FNT-62, two fixtures and two cases more; no change to `src/` | `tasks.md`, "Fixes of the first validation pass" |
| 2 | `0b9ae25..6cd7076` | PASS. 61 of 61 criteria, 33 of 45 mutants killed, 12 alive (4 equivalent, 8 residual); found I-1, which became issue #20 | `git show 79a929a:.specs/features/font-fallback/validation.md` (with the row of FNT-46 that T12 added; `5caa610` holds it as the Verifier wrote it) |
| Fix round 2 | `f5ec283..c7a4729` | `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4: the case `#slash` in `N`, its test, and `J:46` takes the name of a Face as `document.fonts` gives it | `tasks.md`, "Fix of issue #20", F4 |
| 3 | `f5ec283..c7a4729` | FAIL. 63 of 63 criteria; 8 mutants (the revert among them), 7 killed; FACE-UNQUOTE-ONLY alive on the changed line | `git show 135f9a8:.specs/features/font-fallback/validation.md` |
| Fix round 3 | `135f9a8..8dc0ead` | `e598bb8` adds FNT-64 and plans F5; `8dc0ead` is F5: the case `#quoted` in `N` and its test; no change to `src/` | `tasks.md`, "Fix of issue #20", F5 |
| 4 | `f5ec283..8dc0ead` | PASS: this report. 64 of 64 criteria; 16 mutants (the revert and the 7 others of the third report among them), 15 killed; FACE-UNQUOTE-SINGLE-ONLY, of this pass, alive as a residual (R1) | This file |

### What the round changed, from git

- **`src/`**: `git diff --stat f5ec283..8dc0ead -- src` is `font_widths.js | 3 ++-`, all of it in `c7a4729`: `J:46` goes from `family: bare(face.family),` to `family: face.family,` and `J:44` is a new comment. `git diff c7a4729..8dc0ead -- src` is empty. The citations of `J` and `C` of the third pass hold unchanged.
- **`tests/`**: `N` adds the cases `#slash` (F4) and `#quoted` (F5), with a comment on each (`N:42-55`, `N:87-93`, `N:101-102`) and two sentences on `Back\slash` in the comment of the Faces (`N:17-19`). `F` adds two tests (`F:560-566`, F4; `F:569-575`, F5) after the test of FNT-60. No line of an existing test is in the diff: the citations of `F` up to `F:557` do not move since `f5ec283`, and those after `F:575` moved 18 down.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff; 55 tests in the module against 53, 500 collected against 498 (the CI run on `f5ec283`, 38752135720: `498 passed`).
- **`.specs/`**: `spec.md` (FNT-63 and FNT-64, one sentence of the Assumptions, two traceability rows, "64" in the coverage line and in the first Success Criterion), `design.md:110`, `tasks.md` (F4, F5), `validation.md` (the third pass), `LESSONS.md` and `lessons.json` (`4015689` and L-096 of the third pass).

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T12, F1 to F3 | ✅ Done | As the second pass found them; none is in this diff |
| F4 | ✅ Done | As the third pass found it. Its test still fails on the code before the fix, on `F:564` `[] == [('#slash', 'Back\\slash')]` (REVERT, below), and N60-unescape-quotes-only still fails it on the same assertion |
| F5 | ✅ Done | Each "Done when" checked: the computed `font-family` of `#quoted` (`"\"Quoted\"", Ahem`) and its Face (`"Quoted"`, marks included, `error`, last) read from the page here and as `N:48-51` says them; the test passes on the code and fails under FACE-UNQUOTE-ONLY on `F:573` `[] == [('#quoted', '"Quoted"')]`; the tests of FNT-58 to FNT-60 and FNT-63 pass unchanged; Full green; 55 in the module, 500 collected |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome. `findings_on` and `sits_on` find an element through `inspect_element`, by its box; `of_family` (`F:253-257`) unpacks exactly one Finding for a family; `reported` (`F:189-204`) returns the `(selector, family)` of every Finding that names one of `families` or sits on one of `on`, so an assertion that it equals one pair says "exactly one Finding, there, under that name".

**What was checked again in full.** FNT-63 and FNT-64 from scratch, against the page as read on both platforms. FNT-58, FNT-59 and FNT-60, the neighbours of `#slash` and `#quoted` in `N`, against the fixture and their sentence: green, and each named by a kill below. Every row whose outcome rests on matching a First family to the name of a Face: FNT-01, FNT-02, FNT-05, FNT-06, FNT-07, FNT-15, FNT-16, FNT-18, FNT-29; each was read again at HEAD and each dies under at least one mutant of the matching below (FACE-LOWER, CASE-EXACT, FIRST-NOT-BARE, FIRST-ANY-FAILED, PY-CASE-EXACT-FIRST, PY-NAME-FROM-ELEMENT). FNT-40 to FNT-46 were read again at their lines at HEAD. The other rows are carried forward from the third pass: their tests and the code they hold did not change in `c7a4729..8dc0ead`, and the module passes on both platforms here.

### P1: Report a font that did not load

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-01 | Exactly one Finding for the family, on the first element that falls back | `F:41` `[f["selector"] for f in findings if family(f) == "Brand"] == ["#heading"]`; `F:42-44` one Finding on `#heading`, `[]` on `#lead` and `#note` | ✅ PASS |
| FNT-02 | `(#heading, minor, Brand, 3)`, `(#icon, minor, Icon Set, 1)`, in this order | `F:51-59` the whole list `== [("#heading", "minor", "Brand", 3), ("#icon", "minor", "Icon Set", 1)]` | ✅ PASS |
| FNT-03 | First content block `Found 2 findings in 1 viewport: 2 minor.` | `F:64` `texts(result)[0] == "Found 2 findings in 1 viewport: 2 minor."`; first text block is first content block: `D:263` | ✅ PASS |
| FNT-04 | Equal structured content on two calls | `F:70-71` `first["findings"]` not empty, `first == second` | ✅ PASS |
| FNT-05 | One Finding for `#scripted`, `family` `Scripted` | `F:292-294` `family(finding) == "Scripted"`, `of_family(..., "Scripted") == finding` | ✅ PASS |
| FNT-06 | One Finding for `Missing Brand`, on `#lower`, `elements` 2 | `F:298-300` `finding == await sits_on(client, BOUNDS, "#lower")`, `elements(finding) == 2` | ✅ PASS |
| FNT-07 | One Finding for `#icon` | `F:78-80` one Finding on `#icon`, `check == "font-fallback"`, `family(finding) == "Icon Set"` | ✅ PASS |
| FNT-08 | `#half-bold`, `Half`, `elements` 1 | `F:306-308` `(family(finding), elements(finding)) == ("Half", 1)` | ✅ PASS |
| FNT-09 | `#mixed-lower`, `Mixed`, `elements` 1 | `F:314-316` `(family(finding), elements(finding)) == ("Mixed", 1)` | ✅ PASS |
| FNT-10 | `Shadow Brand`, selector `[data-testid="shadow-text"]`, `elements` 2 | `F:322-325` `finding["selector"] == '[data-testid="shadow-text"]'`, `elements(finding) == 2` | ✅ PASS |
| FNT-11 | `Parent Brand` on `#own-parent`, `elements` 1, `textWidthPx` 100 | `F:359-361` `finding == await sits_on(..., "#own-parent")`, `(elements(finding), width(finding)) == (1, 100)` | ✅ PASS |
| FNT-12 | `Child Brand` on `#fallen-child`, `elements` 1 | `F:368-370` `finding == await sits_on(..., "#fallen-child")`, `elements(finding) == 1` | ✅ PASS |
| FNT-13 | `#narrow`: one Finding at 390 × 844, `Narrow Only`; none at 1440 × 900 | `F:87-91` the `(viewport, family)` list `== [(MOBILE, "Narrow Only")]` | ✅ PASS |
| FNT-14 | One Finding on `#code`, `Brand`, `elements` 1, `textWidthPx == round(box.w, 2)` | `F:483-487` `(finding,) = findings`, `finding["selector"] == "#code"`, `("Brand", 1)`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-15 | The twelve `(selector, family, elements)` in order, all `minor` | `F:269-285` the whole list of twelve; `F:286` `== ["minor"] * 12` | ✅ PASS |
| FNT-50 | `Slant` on `#slant-italic`, `elements` 1, the `computed` literal | `F:463-471` `finding == await sits_on(..., "#slant-italic")`, `elements(finding) == 1`, `finding["evidence"]["computed"] == {...}` | ✅ PASS |
| FNT-59 | One Finding for `#comma`, `family` `Acme, Inc` | `F:543-546` `await reported(client, NAMES, families=("Acme, Inc",), on=("#comma",)) == [("#comma", "Acme, Inc")]` | ✅ PASS |
| FNT-60 | One Finding for `#inch`, `family` `Vinyl 12"`; computed `"Vinyl 12\"", Ahem` | `F:552-555` `reported(..., families=('Vinyl 12"',), on=("#inch",)) == [("#inch", 'Vinyl 12"')]`; `F:556-557` `finding["evidence"]["computed"]["font-family"] == '"Vinyl 12\\"", Ahem'` | ✅ PASS |
| FNT-63 | One Finding for `#slash`, with `evidence.measured.family` equal to `Back\slash` | `F:563-566` `await reported(client, NAMES, families=("Back\\slash",), on=("#slash",)) == [("#slash", "Back\\slash")]`. The Python literal `"Back\\slash"` is the string `Back\slash`, one backslash, the name the spec gives. A Finding under `Backslash` would sit on `#slash` and fail the equality | ✅ PASS |
| FNT-64 | One Finding for `#quoted`, with `evidence.measured.family` equal to `"Quoted"`, quotation marks included | `F:572-575` `await reported(client, NAMES, families=('"Quoted"',), on=("#quoted",)) == [("#quoted", '"Quoted"')]`. The Python literal `'"Quoted"'` is the name with its two marks. A Finding under `Quoted` would sit on `#quoted` and fail the equality; no Finding at all fails it too (FACE-UNQUOTE-ONLY, below) | ✅ PASS |

### P1: Stay silent when the text is in the font it asks for

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-16 | `isError: false`, `[]`, no image, `No findings in 1 viewport.` | `F:182-186` `result.is_error is False`, `["findings"] == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| FNT-17 | No Finding for `#undeclared` | `F:208-209` `reported(..., families=("Squint No Such Font",), on=("#undeclared",)) == []` | ✅ PASS |
| FNT-18 | No Finding for `Second Choice` | `F:215-216` `reported(..., families=("Second Choice",), on=("#second",)) == []` | ✅ PASS |
| FNT-19 | No Finding for `Preloaded` | `F:222` `reported(client, CLEAN, families=("Preloaded",)) == []` | ✅ PASS |
| FNT-20 | Nothing on `#half-normal`, not counted | `F:374-375` `reported(..., on=("#half-normal",)) == []`, `elements(await of_family(..., "Half")) == 1` | ✅ PASS |
| FNT-21 | Nothing on `#wrapped`, not counted | `F:381-382` `reported(..., on=("#wrapped",)) == []`, `elements(...) == 1` | ✅ PASS |
| FNT-22 | Nothing on `#mixed-both`, not counted | `F:388-389` `reported(..., on=("#mixed-both",)) == []`, `elements(...) == 1` | ✅ PASS |
| FNT-23 | No Finding for `Hidden Brand` | `F:228-229` `reported(..., families=("Hidden Brand",), on=("#hidden",)) == []` | ✅ PASS |
| FNT-24 | No Finding for `Pseudo Brand` | `F:235-236` `reported(..., families=("Pseudo Brand",), on=("#pseudo",)) == []` | ✅ PASS |
| FNT-25 | No Finding for `Unused`, `After Generic`, `Never Shown`, `Blank` | `F:244-246` `reported(..., families=(...four...), on=("#after-generic",)) == []` | ✅ PASS |
| FNT-26 | `Veiled Brand` on `#seen`, `elements` 1 | `F:395-398` `finding == await sits_on(..., "#seen")`, `elements(finding) == 1`, nothing on `#veiled` | ✅ PASS |
| FNT-49 | Nothing on `#upper-mixed`, not counted | `F:453-457` the Finding of `Mixed` is `#lower-mixed`, `elements` 1; `reported(..., on=("#upper-mixed",)) == []` | ✅ PASS |
| FNT-52 | `Unshown Brand` on `#shown`, `elements` 1 | `F:403-406` `finding["selector"] == "#shown"`, `finding == await sits_on(..., "#shown")`, `elements(finding) == 1` | ✅ PASS |
| FNT-53 | No Finding for `Upper Only` | `F:347-350` `reported(..., families=("Upper Only",), on=("#out-of-range",)) == []` | ✅ PASS |
| FNT-55 | Nothing on `#broad-normal`; `Broad` on `#broad-bold`, `elements` 1 | `F:514-517` `(finding["selector"], elements(finding)) == ("#broad-bold", 1)`, `finding == await sits_on(..., "#broad-bold")`, `reported(..., on=("#broad-normal",)) == []` | ✅ PASS |
| FNT-56 | `Folded Brand` on `#unfolded`, `elements` 1 | `F:521-524` `("#unfolded", 1)`, `finding == await sits_on(..., "#unfolded")`, nothing on `#folded` | ✅ PASS |
| FNT-57 | `Space Brand` on `#after-spaces`, `elements` 1 | `F:528-531` `("#after-spaces", 1)`, `finding == await sits_on(..., "#after-spaces")`, nothing on `#spaces` | ✅ PASS |

### P1: Read the Finding

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-27 | The Finding of `#heading` equals the spec's literal | `F:108-134` `finding == {...}`, every field equal to the spec's | ✅ PASS |
| FNT-28 | `The font "Icon Set" did not load: the text of 1 element is rendered in a fallback font` | `F:97-100` `finding["message"] == (...)` | ✅ PASS |
| FNT-29 | `family` `Missing Brand`; computed `"missing brand", Ahem` | `F:330-331` `family(finding) == "Missing Brand"`, `computed["font-family"] == '"missing brand", Ahem'` | ✅ PASS |
| FNT-30 | `textWidthPx` 280, `box.w` 100 | `F:411-412` `width(finding) == 280`, `finding["box"]["w"] == 100` | ✅ PASS |
| FNT-31 | `computed` literal of `#half-bold`; `textWidthPx` 300 | `F:417-422` `computed == {...}`, `width(finding) == 300` | ✅ PASS |
| FNT-32 | Every selector works in `inspect_element` with the Finding's `box` | `F:428-440` `result.is_error is False`, `structured_content["box"] == finding["box"]` for each | ✅ PASS |
| FNT-51 | `textWidthPx` 226 | `F:477-478` `width(finding) == 226` | ✅ PASS |
| FNT-54 | `textWidthPx` 140, `elements` 1 | `F:446-447` `(width(finding), elements(finding)) == (140, 1)` | ✅ PASS |
| FNT-58 | One Finding on `#dual-normal`, `family` `Dual`, `elements` 2 | `F:537-539` `finding = await sits_on(client, NAMES, "#dual-normal")`, `(family(finding), elements(finding)) == ("Dual", 2)`, `reported(..., families=("DUAL",), on=("#dual-bold",)) == []` | ✅ PASS |
| FNT-61 | `textWidthPx` of `#turned` equals `round(box.w, 2)` | `F:581-583` `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of `#swift` equals `round(box.w, 2)` | `F:589-591` `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks`, the five Checks run | `F:138-142` the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` with `low-contrast-real` in one call; the others by their own slices (`D:449-452`) | ✅ PASS |
| FNT-34 | `isError: true` and the literal of the valid Checks | `D:340-344`, `D:351-355`, `D:362-366`, `D:374-378` the literal `in text`; `D:329` `result.is_error is True` | ✅ PASS |
| FNT-35 | `[]` with the other four Checks | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | The four `(selector, check)` pairs in order, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list | ✅ PASS |
| FNT-37 | The description names the Check and what it reports | `F:156-159` the sentence `in " ".join(tool.description.split())` | ✅ PASS |
| FNT-38 | Earlier tests pass with no change but the four literals | The Build on `8dc0ead`, the orchestrator's run: 500 passed in 20m37s (log not read here; see "Gate Check"). This diff touches no test of an earlier slice. The CI on `f5ec283` passed 498 | ✅ PASS |
| FNT-39 | `isError: false`, one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

Each line read again at HEAD.

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, registered by name | `C:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | `grep -rn playwright src/squint_mcp/checks/` finds nothing (exit 1); `C:3` imports `squint_mcp.models` only | ✅ PASS |
| FNT-42 | Faces and widths read from the Capture, measured only on request | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`; `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`, passed at `:103`; `src/squint_mcp/capture.py:371-375` `faces = None` unless `fonts`; `src/squint_mcp/tools/inspect_element.py:53-55` does not ask | ✅ PASS |
| FNT-43 | Equality, no tolerance; no threshold in `config` | `C:67` `if widths.own == widths.tail:`; `C:3` imports no `config`; `src/squint_mcp/config.py:83` (`font-style`) and `:113-119` (`TEXT_SHAPING_PROPERTIES`), names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG entry with the six things | `CHANGELOG.md:14`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`) | ✅ PASS |
| FNT-45 | README names `font-fallback`, five Checks | `README.md:46` "`detect_visual_bugs` runs five Checks: ... `font-fallback`" | ✅ PASS |
| FNT-46 | Slice 9 `concluída` in the roadmap, table and section, with the link | `docs/ROADMAP.md:111` (table) and `docs/ROADMAP.md:163` (section, with the link to `.specs/features/font-fallback/`), from T12 after the second pass (`79a929a`) | ✅ PASS (file evidence) |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-47 | Each Finding of the first viewport has one in the second | `F:166-175` `len(desktop) == 2`, `desktop <= mobile` | ✅ PASS |
| FNT-48 | `Twice` on `#twice-normal`, `elements` 2 | `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2` | ✅ PASS |

**Status**: ✅ 64 of 64 criteria covered, each with the outcome the spec gives. No spec-precision gap: the outcomes of FNT-63 and FNT-64 are exact strings.

### The names of `N`, read from the page

Read with a script outside the repository (Playwright, Chromium 153.0.8010.12), at HEAD, on Windows and in `mcr.microsoft.com/playwright/python:v1.63.0-noble`. The two platforms gave the same output to the character:

- `document.fonts`: `Ahem` `loaded`, then `Dual`, `DUAL`, `Acme, Inc`, `Vinyl 12"`, `Back\slash`, `"Quoted"`, all `error`, in this order. `Back\slash` has one backslash; `"Quoted"` keeps its two marks. This is what `N:13-19` and `N:48-51` say.
- The computed `font-family`: `#slash` `"Back\\slash", Ahem`, `#quoted` `"\"Quoted\"", Ahem`, as `N:42-43`, `N:48-51`, FNT-63 and FNT-64 say. `#dual-normal`, `#comma` and `#inch` as the earlier passes read them.
- The tool at HEAD returns on `N`, on both platforms, `(#dual-normal, Dual, 2)`, `(#comma, Acme, Inc, 1)`, `(#inch, Vinyl 12", 1)`, `(#slash, Back\slash, 1)`, `(#quoted, "Quoted", 1)`, each `textWidthPx` 200.
- This closes R3 of the third pass. The comment at `N:17-19` still says `Back\slash` was "read on Windows only", which was true when it was written.

---

## The spec, design and fixture edits of the round

| # | Edit | Judgement |
| - | ---- | --------- |
| E1 | `spec.md:69`: FNT-63 for issue #20, then "The third pass found the other half of the rule held by no case ... the maintainer accepted FNT-64 the same day" | Accurate. It matches the third report, `tasks.md` F5 and `e598bb8` |
| E2 | `spec.md:142`, FNT-63 | Accurate, as the third pass found it; every fact read again here on both platforms |
| E3 | `spec.md:143`, FNT-64 | Accurate on every fact it states, each read from the page on both platforms: the declaration `'"Quoted"'` (`N:52-55`), the `font-family` of `#quoted` (`N:91-93`), the Face named `"Quoted"` with its marks, a `src` that names no file, and the outcome. "The quotation marks a name holds are not taken off it" is what `J:46` does. It sits well with FNT-60, where the quotation marks of a computed value are CSS quoting and `bare` takes them off: at `#quoted` the outer pair is quoting and the inner pair is the name. One cosmetic note: FNT-06 and FNT-15 name a `#quoted` of `font-fallback-bounds.html`, and FNT-64 names a `#quoted` of `N`. Each criterion names its page, so neither is ambiguous |
| E4 | `spec.md:316-317`, `:319`, `:325`: two traceability rows, "64" three times | Accurate: 64 rows, FNT-01 to FNT-64, each with a task (F4, F5) |
| E5 | `design.md:110`: `faces` gives `family` "as `document.fonts` gives it: the name itself, with no quotes put around it and no escapes, so a quotation mark or a backslash that is part of the name is kept; FNT-63, FNT-64, issue #20" | Accurate, and it settles the looseness the third pass noted (its E4, R2) for this line. `design.md:111` ("`family` is the First family without quotes") still leaves out the escapes: cosmetic, not the round's (R3) |
| E6 | The comments of `N:13-19`, `N:42-43`, `N:48-51` | Accurate, each read here. The sentence at `N:16` ("the other four are `error`") is true of the four it names, and the two added later are named after it. "Read on Windows only" is now out of date, because this pass read them on Linux and they are the same. It is cosmetic |
| E7 | `J:44` (F4): "`document.fonts` gives the name of a Face with no quotes and no escapes" | Loose in the same way `design.md:110` was before this round: a name can hold quotation marks, and they are kept. Cosmetic (R3) |

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work and empty after it (the runner printed `porcelain after: '' SAME`). Each mutant ran on a copy of `src/squint_mcp`, copied whole (CRLF kept, `__pycache__` left out) to the session's scratch directory outside the repository. The mutation went into the copy only, and the runner stopped unless each `old` occurred exactly once. Each run was `uv run pytest tests/test_font_fallback.py -q -p no:cacheprovider -p squint_guard --tb=line -rf`, from the repository, with `PYTHONPATH` set to the copy and to the guard's directory. The plugin `squint_guard` aborts the session, at configure and again at unconfigure, unless `squint_mcp`, `squint_mcp.capture` and `squint_mcp.checks.font_fallback` are files of the copy and `capture._FONT_WIDTHS` is the copy's `font_widths.js` read whole. It writes a mark and prints `GUARD OK`, and every one of the 17 runs did. The copy without a mutant ran first: 55 passed. Runs were one pytest process at a time, the whole module each time, no `-x`. There was no `git stash`, no worktree, and nothing under `src/` or `tests/` was edited. Each copy was deleted after its run.

"Shown" means the tool, called through the in-memory client on a page outside the repository (`probe.html`: `"'Single'"`, `'"Quoted"'` and `'"Half'` declared with a `src` that names no file, each on a block of ten Ahem glyphs), returned something different with the mutant than without it. With the code, the probe returns `(#single, 'Single', 1, 200)`, `(#quoted, "Quoted", 1, 200)` and `(#half, "Half, 1, 200)`.

| # | `file:line` | Mutation | Test that failed | Result |
| - | ----------- | -------- | ---------------- | ------ |
| REVERT | `J:46` | `family: bare(face.family),`: the fix taken back | `F:560` (FNT-63), `F:569` (FNT-64) | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]`, `F:573` `[] == [('#quoted', '"Quoted"')]` |
| N60-unescape-quotes-only | `J:41` | `.replace(/\\(.)/gs, "$1")` becomes `.replace(/\\"/g, '"')` | `F:560` (FNT-63), alone | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]` |
| FACE-UNQUOTE-ONLY | `J:46` | `face.family.replace(/^(["'])(.*)\1$/s, "$2")`: the quotes of a Face name taken off | `F:569` (FNT-64), alone | ✅ **Killed** (alive in the third pass): `F:573` `[] == [('#quoted', '"Quoted"')]` |
| FACE-UNESCAPE-ONLY | `J:46` | `face.family.replace(/\\(.)/gs, "$1")`: the escapes of a Face name taken off | `F:560` (FNT-63), alone | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]` |
| FACE-LOWER | `J:46` | `face.family.toLowerCase()` | 34 tests, the first `F:37` (FNT-01) | ✅ Killed: `F:41` `[] == ['#heading']`; `F:80` `'icon set' == 'Icon Set'` |
| CASE-EXACT | `J:53`, `J:102` | Case folding taken out of the matching, on both sides | `F:267` (FNT-15), `F:297` (FNT-06), `F:328` (FNT-29) | ✅ Killed: `F:269` the list of twelve differs; `F:263` finds no Finding on `#lower` |
| FIRST-NOT-BARE | `J:101` | `const family = names[0];` | 27 tests, among them FNT-02, FNT-03, FNT-07, FNT-13 | ✅ Killed: `F:51` `[('#heading', ..., 'Brand', 3)] == [..., ('#icon', ..., 'Icon Set', 1)]`, `F:64` `'Found 1 finding...'` |
| NAMESOF-DROP-BACKSLASH | `J:17` | `namesOf` drops the backslash of an escape | `F:560` (FNT-63), alone | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]` |
| BARE-UNQUOTE-ONLY | `J:41` | `bare` keeps the escapes: `name.replace(/^(["'])(.*)\1$/s, "$2");` | FNT-60, FNT-63, FNT-64 | ✅ Killed: `F:553` `[] == [('#inch', 'Vinyl 12"')]`, `F:564`, `F:573` |
| BARE-STRIP-ALL-QUOTES | `J:41` | `bare` strips every quotation mark at either end: `name.replace(/^["']+\|["']+$/g, "")` before the unescape | FNT-60, FNT-64 | ✅ Killed: `F:553` `[] == [('#inch', 'Vinyl 12"')]`, `F:573` `[] == [('#quoted', '"Quoted"')]` |
| FIRST-ANY-FAILED | `J:101` | The judged family is the first Failed family of the list, not the First family: `bare(names.find((n) => failed.has(bare(n).toLowerCase())) ?? names[0])` | FNT-16, FNT-18 | ✅ Killed: `F:216` `[('#second', 'Second Choice')] == []`; `F:184` the clean page gets a Finding |
| NAMESOF-ESCAPE-AFTER-QUOTE | `J:16-22` | Inside a string, a backslash no longer escapes: the quote branch is tested before the backslash branch | FNT-60, FNT-64 | ✅ Killed: `F:553` `[] == [('#inch', 'Vinyl 12"')]`, `F:573` `[] == [('#quoted', '"Quoted"')]` |
| PY-LAST-FACE-NAME | `C:50` | `names[face.family.lower()] = face.family`: the family named as its last Face has it | `F:534` (FNT-58), alone | ✅ Killed: `F:538` `('DUAL', 2) == ('Dual', 2)` |
| PY-CASE-EXACT-FIRST | `C:58` | `family = widths.family`: the First family not folded on the Python side | 44 tests, the first `F:37` (FNT-01) | ✅ Killed: `F:41` `[] == ['#heading']`, `F:64` `'No findings in 1 viewport.'` |
| PY-NAME-FROM-ELEMENT | `C:69` | The Finding named as the element writes the family, not as its Face has it | FNT-15, FNT-06, FNT-29 | ✅ Killed: `F:330` `'missing brand' == 'Missing Brand'`; `F:269`; `F:256` |
| **FACE-UNQUOTE-SINGLE-ONLY** | `J:46` | `face.family.replace(/^'(.*)'$/s, "$1")`: only the apostrophes of a Face name taken off. A second-order mutant: the single-quote half of FACE-UNQUOTE-ONLY | none | ⚠️ **Survived (55 passed): residual R1.** Shown: with the mutant the probe loses `(#single, 'Single', 1, 200)` and keeps `#quoted` and `#half`. Not equivalent |

The rows, exactly, as `(file under src/squint_mcp, old, new)`. The first eight are the third report's, unchanged:

```
REVERT                  js/font_widths.js
         old:     family: face.family,
         new:     family: bare(face.family),

N60-unescape-quotes-only  js/font_widths.js
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\"/g, '"');

FACE-UNQUOTE-ONLY       js/font_widths.js
         old:     family: face.family,
         new:     family: face.family.replace(/^(["'])(.*)\1$/s, "$2"),

FACE-UNESCAPE-ONLY      js/font_widths.js
         old:     family: face.family,
         new:     family: face.family.replace(/\\(.)/gs, "$1"),

FACE-LOWER              js/font_widths.js
         old:     family: face.family,
         new:     family: face.family.toLowerCase(),

CASE-EXACT              js/font_widths.js
         old:       .map((face) => face.family.toLowerCase()),
         new:       .map((face) => face.family),
         old:     if (!failed.has(family.toLowerCase())) return;
         new:     if (!failed.has(family)) return;

FIRST-NOT-BARE          js/font_widths.js
         old:     const family = bare(names[0]);
         new:     const family = names[0];

NAMESOF-DROP-BACKSLASH  js/font_widths.js
         old:         name += char + (fontFamily[at + 1] ?? "");
         new:         name += fontFamily[at + 1] ?? "";

BARE-UNQUOTE-ONLY       js/font_widths.js
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2");

BARE-STRIP-ALL-QUOTES   js/font_widths.js
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^["']+|["']+$/g, "").replace(/\\(.)/gs, "$1");

FIRST-ANY-FAILED        js/font_widths.js
         old:     const family = bare(names[0]);
         new:     const family = bare(names.find((n) => failed.has(bare(n).toLowerCase())) ?? names[0]);

NAMESOF-ESCAPE-AFTER-QUOTE  js/font_widths.js   (the two first branches of the loop swapped)
         old:       if (char === "\\") { ...escape... } else if (quote !== null) { ...string... } else if
         new:       if (quote !== null) { ...string... } else if (char === "\\") { ...escape... } else if

PY-LAST-FACE-NAME       checks/font_fallback.py
         old:         names.setdefault(face.family.lower(), face.family)
         new:         names[face.family.lower()] = face.family

PY-CASE-EXACT-FIRST     checks/font_fallback.py
         old:         family = widths.family.lower()
         new:         family = widths.family

PY-NAME-FROM-ELEMENT    checks/font_fallback.py
         old:     return [_finding(capture, names[family], found) for family, found in fallen.items()]
         new:     return [_finding(capture, found[0][0].line_widths.family, found) for family, found in fallen.items()]

FACE-UNQUOTE-SINGLE-ONLY  js/font_widths.js                 (alive, R1)
         old:     family: face.family,
         new:     family: face.family.replace(/^'(.*)'$/s, "$1"),
```

**Why FACE-UNQUOTE-SINGLE-ONLY does not fail the pass.** The Assumption "When the discrimination sensor is satisfied" (`spec.md:96`) and the fourth Success Criterion ask for two things. The first is that the mutants a report or a task names die: all eight do, FACE-UNQUOTE-ONLY among them. The second is that the mutants "of the code the last fix round changed" die. The last fix round is F5 (`8dc0ead`, "Fix round 3" above), and `git diff c7a4729..8dc0ead -- src` is empty. FACE-UNQUOTE-SINGLE-ONLY is of `J:46`, which F4 changed and the third pass sensed. It was found alive later, in this pass, and the Assumption makes such a mutant "a residual or an issue". Two more points weigh the same way. The mutant is second-order: it does not change the code the round left, it brings back one quarter of the `bare` the round took off. And the third report saw `'Single'` lost under FACE-UNQUOTE-ONLY, then asked only for `"Quoted"` (its Fix 1), which F5 delivered as asked. **The other reading**, with F4 and F5 as one round of issue #20 as the brief's diff range draws it, makes `J:46` code of the last round and fails this pass as FACE-UNQUOTE-ONLY failed the third. This report takes the first reading, which is the one the house numbering of the table "Passes" gives. The maintainer may take the other one (R1).

**Sensor depth**: the eight mutants the third report names, exactly as it gives them (the revert among them); eight of this pass's own on the matching of a First family to a Face, five in `J` and three in `C`.
**Count**: 16 injected; 15 killed; 1 alive (FACE-UNQUOTE-SINGLE-ONLY, residual R1); 0 equivalent.

---

## Gate Check

Run here on `8dc0ead` with a clean tree, before the sensor.

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py`, then `uv run pytest --collect-only -q`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 121 files already formatted
- **The module of the slice**: 55 passed, 0 failed, 0 skipped, in 169.73s
- **Collected**: 500
- **Linux**: run here with the Linux command of the gate table (`tasks.md:36`) in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`, the id the third pass recorded), from `8dc0ead`, with the name probe before it: 55 passed in 156.46s
- **Test count before the round**: 53 in the module, 498 in the suite (the CI run on `f5ec283`). **After**: 55 and 500. **Delta**: +2, the tests of FNT-63 and FNT-64
- **Skipped**: none. **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened; the diff of `tests/` removes one line, of the comment of `N`
- **The Build** (the whole suite): not run here. It is the orchestrator's run on `8dc0ead`, Windows: 500 passed in 20m37s, reported in the brief; its log was not read here. The diff since `c7a4729` is one test and one fixture case; no test of an earlier slice is in the range
- **CI**: the branch is not on the remote (`git ls-remote --heads origin fix/font-name-backslash` is empty), so no CI run of it exists

---

## Evidence for the boxes of spec.md

For the maintainer's closing step. No box is ticked here.

| Box | Evidence now | Where |
| --- | ------------ | ----- |
| Goal 1 (`spec.md:13`): every family of the bug fixture reported once, nothing on the clean fixture | Yes | FNT-02 (`F:51-59`) and FNT-16 (`F:182-186`), green in the Full gate of this pass on Windows and in the Playwright image |
| Goal 2 (`spec.md:14`): a Finding names the family and counts the elements | Yes | FNT-27 (`F:108-134`), the literal with `family` and `elements`; green here |
| Goal 3 (`spec.md:15`): every outcome the same on Windows and on Linux | Yes, for `8dc0ead`'s module | 55 passed on Windows and 55 passed in the Playwright image, this pass; the Faces and the computed names of `N` read identical on both. The CI's Linux has not run `8dc0ead` (the branch is not on the remote) |
| Goal 4 (`spec.md:16`): slice 9 marked done in the roadmap once verification passes | Yes | `docs/ROADMAP.md:111` and `:163`, `79a929a`, after the PASS of pass 2; this pass is a PASS too, so the line stands |
| Success Criterion 1 (`spec.md:325`): all 64 requirements verified, FNT-40 to FNT-46 from file evidence | Yes | "Spec-Anchored Acceptance Criteria" of this report: 64 of 64 |
| Success Criterion 2 (`spec.md:326`): typecheck, lint, format check and the whole suite pass | Yes, by the orchestrator's Build | The Build on `8dc0ead` (500 passed, 20m37s), reported in the brief and not read here; pyright, ruff check, ruff format and the module run again here, green. On the CI: 38752135720 on `f5ec283` (498 passed), not on `8dc0ead` |
| Success Criterion 3 (`spec.md:327`): the first run of the suite on the CI's Linux passes the tests of this slice with no assertion changed for it | Yes, for the 53 tests before this round; not yet for the two of FNT-63 and FNT-64 | CI run 38447799140 on `61c4378`, the first run of #21, 2026-10-13: 421 passed on `ubuntu-latest`. The tests of FNT-63 and FNT-64 have had no CI run. They pass in the Playwright image here |
| Success Criterion 4 (`spec.md:328`): no mutant a report or a task names alive, nor any of the code the last fix round changed | Yes, under the reading of R1 | "Discrimination Sensor": the eight mutants of the third report and the one F5 names (FACE-UNQUOTE-ONLY) die; F5 changed no code. FACE-UNQUOTE-SINGLE-ONLY lives on `J:46`, code of F4. Under the reading that F4 and F5 are one round, the answer is No |

---

## Residuals (not gaps of this round)

- **R1. FACE-UNQUOTE-SINGLE-ONLY lives** on `J:46`. A family whose name starts and ends with an apostrophe (declared as `"'Single'"`) is reported by the code under `'Single'`. The mutant, and the code before F4, lose it. The fix, if the maintainer wants it, is the shape of F5: a case `#single` in `N` beside `#quoted`, of `font-family: "'Single'", Ahem` with a Face declared as `"'Single'"` whose `src` names no file, and the test `reported(client, NAMES, families=("'Single'",), on=("#single",)) == [("#single", "'Single'")]`, which should be seen red under this mutant. No change to `src/`. Severity: minor. A name wrapped in apostrophes is rarer still than one wrapped in quotation marks, and the fault would be a missing Finding. If the maintainer reads F4 and F5 as one round (the other reading above), this residual becomes a fix task and the pass a FAIL.
- **R2. Slice 10 changed the Capture after the second pass** (`capture.py`, `collect_elements.js`). As the third pass found: it does not reach the font path; held by the 55 tests and the Build; not verified mutant by mutant.
- **R3. Cosmetic wording**: `J:44` says a Face name has "no quotes", and a name can hold quotation marks, which are kept. `design.md:111` says the First family is "without quotes" and leaves out the escapes. `N:17-19` says `Back\slash` was "read on Windows only", which is now out of date.
- **R4. The Linux gate is not recorded under T10** for this round. It is run here (55 passed). `tasks.md:36` asks for it before a push when `src/` or `tests/` changed; writing it there is the orchestrator's job.
- **The residuals of the second report** (R1 to R9 there) stand as it lists them; its R7 is issue #28. Its I-1 (issue #20) is closed by this round.
- **Not verified here**: the Build's log (the orchestrator's); a CI run of `8dc0ead`.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-62 | Implemented (verified by passes 2 and 3) | ✅ Verified again at `8dc0ead` |
| FNT-63 | Implemented (verified for its case by pass 3) | ✅ Verified |
| FNT-64 | Implemented | ✅ Verified |

The spec is not edited by the Verifier.

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 64 of 64 criteria matched the spec outcome; 0 spec-precision gaps
**Sensor**: 15 of 16 killed; the eight of the third report all dead, FACE-UNQUOTE-ONLY among them; FACE-UNQUOTE-SINGLE-ONLY (this pass's own, second-order) alive as residual R1
**Gate**: Full green on Windows (55 passed, 500 collected) and in the Playwright image (55 passed); the Build of `8dc0ead` passed in the orchestrator's run (500)

**What works**: the fix of issue #20 on Windows and on Linux, with the names of the Faces read the same on both; FNT-63 and FNT-64 and their neighbours FNT-58 to FNT-60; each half of what `J:46` stopped doing (taking off quotes, taking off escapes) dies under its own test; every rule of name matching dies under its mutant, in `J` and in `C`.

**Issues found**: none that fail the pass. R1 is the maintainer's call: one more case, or accept the residual.

**Next steps**: the maintainer's choice on R1; the Linux run written under T10; push the branch and let the CI run the two new tests on `ubuntu-latest`; close issue #20 with the pull request.
