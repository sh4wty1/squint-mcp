# font-fallback Validation

**Date**: 2026-10-15
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-65, as it is at `38c74f6`)
**Diff range**: `f5ec283..38c74f6` (8 commits, branch `fix/font-name-backslash`, base `main`). `4015689` is a lessons commit outside the feature; `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4; `135f9a8` is the third pass (FAIL); `e598bb8` adds FNT-64 and plans F5; `8dc0ead` is F5; `9ce2d25` is the fourth pass (PASS with residual R1); `a2535ca` adds FNT-65 and plans F6; `38c74f6` is F6. Across the range `src/` changes in one line (`src/squint_mcp/js/font_widths.js:46`, with a comment above it), all of it in F4; F5 and F6 change no `src/`
**Verifier**: independent sub-agent (author ≠ verifier), fifth verification pass. Not the Verifier of an earlier pass, and not the author of the code, of the tests or of the spec edits

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL - 65 of 65 criteria held on the outcome the spec gives; the gate green on Windows and in the Playwright image; all 16 mutants that passes 3 and 4 name die, FACE-UNQUOTE-SINGLE-ONLY among them; 3 of this pass's own 8 mutants live, all on whitespace in the matching of a First family to a Face (G1)

F6 does what the fourth pass asked. The case `#single` holds a family whose name starts and ends with an apostrophe, and its test kills FACE-UNQUOTE-SINGLE-ONLY on `F:582` `[] == [('#single', "'Single'")]`. The Faces and the computed `font-family` of `#single` were read here on Windows and in the Playwright image, and they are the same on both.

The pass fails on whitespace. **FACE-TRIM** and **FACE-COLLAPSE-SPACES**, on `J:46`, the line the round changed, and **FIRST-TRIM**, on `J:101`, the element side of the matching, each pass the 56 tests. None is equivalent. Chromium keeps the whitespace of a family name in the Face and in the computed `font-family`, on both platforms. The code reports a family declared as `" Pad "` or `"Two  Spaces"`, and each mutant loses one of the two. The maintainer reads F4 to F6 as one round, and under that reading a mutant alive in the code the round changed or in the matching of a First family to a Face counts against the pass. This is the third fix iteration of the loop, so it goes to the maintainer and not to another fix round.

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
| 4 | `f5ec283..8dc0ead` | PASS. 64 of 64 criteria; 16 mutants, 15 killed; FACE-UNQUOTE-SINGLE-ONLY alive as a residual (R1), which the maintainer chose to close | `git show 9ce2d25:.specs/features/font-fallback/validation.md` |
| Fix round 4 | `9ce2d25..38c74f6` | `a2535ca` adds FNT-65 and plans F6; `38c74f6` is F6: the case `#single` in `N`, its test, and the top comment of `N` rewritten; no change to `src/` | `tasks.md`, "Fix of issue #20", F6 |
| 5 | `f5ec283..38c74f6` | FAIL: this report. 65 of 65 criteria; 24 mutants, 21 killed; the 16 of passes 3 and 4 all dead; FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM, of this pass, alive (G1). Third fix iteration: escalated to the maintainer | This file |

### What the round changed, from git

- **`src/`**: `git diff --stat f5ec283..38c74f6 -- src` is `font_widths.js | 3 ++-`, all of it in `c7a4729`: `J:46` goes from `family: bare(face.family),` to `family: face.family,`, and `J:44` is a new comment. `git diff c7a4729..38c74f6 -- src` is empty.
- **`tests/`**: `N` adds `#slash` (F4), `#quoted` (F5) and `#single` (F6), each with an `@font-face` whose `src` names no file and a comment (`N:44-65`, `N:97-107`, `N:115-117`); F6 rewrote the top comment (`N:13-21`). `F` adds three tests (`F:560-566`, `F:569-575`, `F:578-584`) after the test of FNT-60. No line of an existing test is in the diff: the citations of `F` up to `F:557` do not move since `f5ec283`, and those after `F:584` moved 27 down.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff; 56 tests in the module against 53, 501 collected against 498 (the CI run 38752135720 on `f5ec283`, success).
- **`.specs/`**: `spec.md` (FNT-63 to FNT-65, the paragraph at `spec.md:69`, three traceability rows `:317-319`, "65" at `:321` and `:327`), `design.md:110`, `tasks.md` (F4 to F6), `validation.md` (passes 3 and 4), `LESSONS.md` and `lessons.json`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T12, F1 to F3 | ✅ Done | As the second pass found them; none is in this diff |
| F4 | ✅ Done | Its test fails on the code before the fix, on `F:564` `[] == [('#slash', 'Back\\slash')]` (REVERT, below), and N60-unescape-quotes-only fails it on the same assertion |
| F5 | ✅ Done | Its test fails under FACE-UNQUOTE-ONLY on `F:573` `[] == [('#quoted', '"Quoted"')]` |
| F6 | ✅ Done | Each "Done when" checked: the computed `font-family` of `#single` (`"'Single'", Ahem`) and its Face (`'Single'`, apostrophes included, `error`, last of the eight) read from the page here on Windows and in the Playwright image, as `N:58-61` says them; the test passes on the code and fails under FACE-UNQUOTE-SINGLE-ONLY on `F:582` `[] == [('#single', "'Single'")]`; the tests of FNT-58 to FNT-60, FNT-63 and FNT-64 pass; Full green; 56 in the module, 501 collected |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome. `findings_on` and `sits_on` find an element through `inspect_element`, by its box; `of_family` (`F:253-257`) unpacks exactly one Finding for a family; `reported` (`F:189-204`) returns the `(selector, family)` of every Finding that names one of `families` or sits on one of `on`, so an assertion that it equals one pair says "exactly one Finding, there, under that name".

**What was checked again in full.** FNT-63 to FNT-65 from scratch, against the page as read on both platforms. FNT-58 to FNT-60, the neighbours in `N`, against the fixture and their sentence. Every cited line of `F` was printed at `38c74f6` and read against its row. Every row whose outcome rests on matching a First family to the name of a Face (FNT-01, FNT-02, FNT-05, FNT-06, FNT-07, FNT-15, FNT-16, FNT-18, FNT-29) dies under at least one mutant of the matching below. FNT-40 to FNT-46 were read again at their lines. The module passed whole on both platforms.

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
| FNT-63 | One Finding for `#slash`, with `evidence.measured.family` equal to `Back\slash` | `F:563-566` `await reported(client, NAMES, families=("Back\\slash",), on=("#slash",)) == [("#slash", "Back\\slash")]`. The Python literal is `Back\slash`, one backslash, the name the spec gives | ✅ PASS |
| FNT-64 | One Finding for `#quoted`, with `evidence.measured.family` equal to `"Quoted"`, quotation marks included | `F:572-575` `await reported(client, NAMES, families=('"Quoted"',), on=("#quoted",)) == [("#quoted", '"Quoted"')]`. A Finding under `Quoted` would sit on `#quoted` and fail the equality | ✅ PASS |
| FNT-65 | One Finding for `#single`, with `evidence.measured.family` equal to `'Single'`, apostrophes included | `F:581-584` `await reported(client, NAMES, families=("'Single'",), on=("#single",)) == [("#single", "'Single'")]`. The Python literal `"'Single'"` is the name with its two apostrophes. A Finding under `Single` would sit on `#single` and fail the equality; no Finding at all fails it too (FACE-UNQUOTE-SINGLE-ONLY, below) | ✅ PASS |

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
| FNT-61 | `textWidthPx` of `#turned` equals `round(box.w, 2)` | `F:590-592` `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of `#swift` equals `round(box.w, 2)` | `F:598-600` `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks`, the five Checks run | `F:138-142` the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` with `low-contrast-real` in one call; the others by their own slices (`D:449-452`) | ✅ PASS |
| FNT-34 | `isError: true` and the literal of the valid Checks | `D:340-344`, `D:351-355`, `D:362-366`, `D:374-378` the literal `in text`; `D:329` `result.is_error is True` | ✅ PASS |
| FNT-35 | `[]` with the other four Checks | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | The four `(selector, check)` pairs in order, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list | ✅ PASS |
| FNT-37 | The description names the Check and what it reports | `F:156-159` the sentence `in " ".join(tool.description.split())` | ✅ PASS |
| FNT-38 | Earlier tests pass with no change but the four literals | The Build on `38c74f6`, the orchestrator's run: 501 passed in 20m02s (log not read here). This diff touches no test of an earlier slice. The CI on `f5ec283` (38752135720) succeeded | ✅ PASS |
| FNT-39 | `isError: false`, one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

Each line read again at `38c74f6`.

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, registered by name | `C:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | `grep -rn playwright src/squint_mcp/checks/` finds nothing (exit 1); `C:3` imports `squint_mcp.models` only | ✅ PASS |
| FNT-42 | Faces and widths read from the Capture, measured only on request | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`; `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`, passed at `:103`; `src/squint_mcp/capture.py:371-375` `faces = None` unless `fonts`; `src/squint_mcp/tools/inspect_element.py:53-55` does not ask | ✅ PASS |
| FNT-43 | Equality, no tolerance; no threshold in `config` | `C:67` `if widths.own == widths.tail:`; `C:3` imports no `config`; `src/squint_mcp/config.py:83` (`font-style`) and `:113-119` (`TEXT_SHAPING_PROPERTIES`), names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG entry with the six things | `CHANGELOG.md:14`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`) | ✅ PASS |
| FNT-45 | README names `font-fallback`, five Checks | `README.md:46` "`detect_visual_bugs` runs five Checks: ... `font-fallback`" | ✅ PASS |
| FNT-46 | Slice 9 `concluída` in the roadmap, table and section, with the link | `docs/ROADMAP.md:111` (table) and `docs/ROADMAP.md:163` (section, with the link to `.specs/features/font-fallback/`) | ✅ PASS (file evidence) |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-47 | Each Finding of the first viewport has one in the second | `F:166-175` `len(desktop) == 2`, `desktop <= mobile` | ✅ PASS |
| FNT-48 | `Twice` on `#twice-normal`, `elements` 2 | `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2` | ✅ PASS |

**Status**: ✅ 65 of 65 criteria covered, each with the outcome the spec gives. No spec-precision gap: the outcomes of FNT-63 to FNT-65 are exact strings.

### The names, read from the page

Read with a script outside the repository (Playwright, Chromium 153.0.8010.12), at `38c74f6`, on Windows and in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`). The two platforms gave the same output to the character.

- **`N`, `document.fonts`**: `Ahem` `loaded`, then `Dual`, `DUAL`, `Acme, Inc`, `Vinyl 12"`, `Back\slash`, `"Quoted"`, `'Single'`, all `error`, in this order. `'Single'` keeps its two apostrophes. This is what `N:13-21` and `N:58-61` say.
- **`N`, computed `font-family`**: `#single` is `"'Single'", Ahem`, as `N:58-61` and FNT-65 say. `#dual-normal`, `#comma`, `#inch`, `#slash` and `#quoted` are as passes 3 and 4 read them.
- **`N`, the tool**: at `38c74f6`, on both platforms, it returns `(#dual-normal, Dual, 2)`, `(#comma, Acme, Inc, 1)`, `(#inch, Vinyl 12", 1)`, `(#slash, Back\slash, 1)`, `(#quoted, "Quoted", 1)` and `(#single, 'Single', 1)`, each with `textWidthPx` 200.
- **The probe page** (`p5.html`, outside the repository): seven families declared with a `src` that names no file, each on a block of ten Ahem glyphs: `" Pad "`, `"Two  Spaces"`, `"'Single'"`, `'"Quoted"'`, `"Back\\slash"`, `'"MiXed"'` (asked for as `'"mixed"'`) and `"Esc\\\"q"`. The Faces keep every character: ` Pad ` with its two edge spaces, `Two  Spaces` with its double space. The computed values keep them too: `" Pad ", Ahem` and `"Two  Spaces", Ahem`. With the code the tool reports all seven, under the name of the Face: `(#pad, " Pad ", 1, 200)`, `(#two, "Two  Spaces", 1, 200)`, `(#single, 'Single', ...)`, `(#quoted, "Quoted", ...)`, `(#slash, Back\slash, ...)`, `(#mixed, "MiXed", ...)` and `(#escq, Esc\"q, ...)`.

---

## The spec, design and fixture edits of the round

| # | Edit | Judgement |
| - | ---- | --------- |
| E1 | `spec.md:69`: FNT-63 for issue #20; FNT-64 after the third pass; "The fourth pass found the same of apostrophes ... the maintainer accepted FNT-65 for them" | Accurate. It matches the fourth report, `tasks.md` F6 and `a2535ca` |
| E2 | `spec.md:142-143`, FNT-63 and FNT-64 | Accurate, as passes 3 and 4 found them; every fact read again here on both platforms |
| E3 | `spec.md:144`, FNT-65 | Accurate on every fact it states, each read here on both platforms: the declaration `"'Single'"` (`N:62-65`), the `font-family` of `#single` (`N:105-107`), the Face `'Single'` with its apostrophes, a `src` that names no file, and the outcome. "The apostrophes a name holds are not taken off it" is what `J:46` does |
| E4 | `spec.md:317-319`, `:321`, `:327`: three traceability rows and "65" twice | Accurate: 65 rows, FNT-01 to FNT-65, each with a task |
| E5 | `design.md:110`: `faces` gives `family` "as `document.fonts` gives it ... so a quotation mark, an apostrophe or a backslash that is part of the name is kept; FNT-63 to FNT-65, issue #20" | Accurate as far as it goes. It names three characters, and the rule is wider: whitespace at the edges or doubled is kept too, and nothing holds that (G1). `design.md:111` ("`family` is the First family without quotes") still leaves out the escapes: cosmetic (R2) |
| E6 | `N:13-21`, the top comment rewritten by F6: the first four Faces "read ... on Windows and on Linux when this fixture was written"; `Back\slash`, `"Quoted"` and `'Single'` "added later ... Read on Windows, and the first two on Linux as well by the fourth validation pass" | Accurate. Pass 4 read `Back\slash` and `"Quoted"` in the Playwright image (its "The names of `N`"), and F6 read `'Single'` on Windows only (`tasks.md` F6 Notes). This pass read `'Single'` in the Playwright image too, and found the same Face, so the comment is now short of the truth by one platform. Cosmetic |
| E7 | `N:50-53` and `N:58-61`: each says "Read on Windows" for its Face and computed value | Accurate when written; this pass read both on Linux as well. Cosmetic |
| E8 | `J:44` (F4): "`document.fonts` gives the name of a Face with no quotes and no escapes" | Loose: a name can hold quotation marks, apostrophes and edge whitespace, and all are kept. Cosmetic (R2) |

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work and empty after it (0 bytes both times). Each mutant ran on its own copy of `src/squint_mcp`, copied whole with `__pycache__` left out, under the session's scratch directory outside the repository. The mutation went into the copy only, line endings kept, and the runner stopped unless each `old` occurred exactly once. Each run was `uv run pytest tests/test_font_fallback.py -q -p no:cacheprovider -p squint_guard --tb=short -rf`, from the repository, with `PYTHONPATH` set to the copy's parent and the guard's directory and `PYTHONDONTWRITEBYTECODE=1`. The plugin `squint_guard` exits the session at configure, and again at unconfigure, unless `squint_mcp`, `squint_mcp.capture` and `squint_mcp.checks.font_fallback` are files of the copy and `capture._FONT_WIDTHS` equals the copy's `font_widths.js`. It then prints `GUARD OK <copy>`, and all 25 runs printed it. The copy without a mutant ran first: 56 passed. Two pytest processes ran at a time, each in its own copy, each on the whole module, with no `-x`. There was no `git stash` and no worktree, and nothing under `src/` or `tests/` was edited. Each copy was deleted after its run; the `copies` directory is empty.

"Shown" means the probe page above, called through the in-memory client from the same copy, returned something different with the mutant than without it.

| # | `file:line` | Mutation | Tests that failed | Result |
| - | ----------- | -------- | ----------------- | ------ |
| REVERT | `J:46` | `family: bare(face.family),`: the fix taken back | FNT-63, FNT-64, FNT-65 | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]`, `F:573` `[] == [('#quoted', '"Quoted"')]`, `F:582` `[] == [('#single', "'Single'")]` |
| N60-unescape-quotes-only | `J:41` | `.replace(/\\(.)/gs, "$1")` becomes `.replace(/\\"/g, '"')` | FNT-63, alone | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]` |
| FACE-UNQUOTE-ONLY | `J:46` | `face.family.replace(/^(["'])(.*)\1$/s, "$2")` | FNT-64, FNT-65 | ✅ Killed: `F:573`, `F:582` |
| FACE-UNESCAPE-ONLY | `J:46` | `face.family.replace(/\\(.)/gs, "$1")` | FNT-63, alone | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]` |
| FACE-LOWER | `J:46` | `face.family.toLowerCase()` | 35 tests, the first FNT-01 | ✅ Killed: `F:41` `[] == ['#heading']`; `F:80` `'icon set' == 'Icon Set'` |
| CASE-EXACT | `J:53`, `J:102` | Case folding taken out of the matching, on both sides | FNT-15, FNT-06, FNT-29 | ✅ Killed: `F:269` the list of twelve differs; `F:263` (in `sits_on` from `F:299`, `F:329`) finds no Finding on `#lower` |
| FIRST-NOT-BARE | `J:101` | `const family = names[0];` | 28 tests, among them FNT-02, FNT-03, FNT-07, FNT-13 | ✅ Killed: `F:51` `[('#heading', ..., 'Brand', 3)] == [..., ('#icon', ..., 'Icon Set', 1)]`, `F:64` `'Found 1 finding...'` |
| NAMESOF-DROP-BACKSLASH | `J:17` | `namesOf` drops the backslash of an escape | FNT-63, alone | ✅ Killed: `F:564` |
| BARE-UNQUOTE-ONLY | `J:41` | `bare` keeps the escapes | FNT-60, FNT-63, FNT-64 | ✅ Killed: `F:553` `[] == [('#inch', 'Vinyl 12"')]`, `F:564`, `F:573` |
| BARE-STRIP-ALL-QUOTES | `J:41` | `bare` strips every quotation mark and apostrophe at either end | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| FIRST-ANY-FAILED | `J:101` | The judged family is the first Failed family of the list | FNT-16, FNT-18 | ✅ Killed: `F:216` `[('#second', 'Second Choice')] == []`; `F:184` the clean page gets a Finding |
| NAMESOF-ESCAPE-AFTER-QUOTE | `J:16-22` | Inside a string a backslash no longer escapes | FNT-60, FNT-64 | ✅ Killed: `F:553`, `F:573` |
| PY-LAST-FACE-NAME | `C:50` | The family named as its last Face has it | FNT-58, alone | ✅ Killed: `F:538` `('DUAL', 2) == ('Dual', 2)` |
| PY-CASE-EXACT-FIRST | `C:58` | The First family not folded on the Python side | 45 tests, the first FNT-01 | ✅ Killed: `F:41` `[] == ['#heading']`, `F:64` `'No findings in 1 viewport.'` |
| PY-NAME-FROM-ELEMENT | `C:69` | The Finding named as the element writes the family | FNT-15, FNT-06, FNT-29 | ✅ Killed: `F:330` `'missing brand' == 'Missing Brand'`; `F:269`; `F:256` |
| FACE-UNQUOTE-SINGLE-ONLY | `J:46` | `face.family.replace(/^'(.*)'$/s, "$1")` | FNT-65, alone | ✅ **Killed** (alive in pass 4): `F:582` `[] == [('#single', "'Single'")]` |
| FACE-UNQUOTE-DOUBLE-ONLY | `J:46` | Of this pass: `face.family.replace(/^"(.*)"$/s, "$1")`, the other half of FACE-UNQUOTE-ONLY | FNT-64, alone | ✅ Killed: `F:573` `[] == [('#quoted', '"Quoted"')]` |
| BARE-UNESCAPE-FIRST-ONLY | `J:41` | Of this pass, escapes on the element side: `bare` takes off only the first escape (`/\\(.)/s`, no `g`) | FNT-64, alone | ✅ Killed: `F:573` `[] == [('#quoted', '"Quoted"')]` |
| ELEM-CASE-EXACT | `J:102` | Of this pass, case on the element side only: `failed.has(family)` | 45 tests, the first FNT-01 | ✅ Killed: `F:41` `[] == ['#heading']`, `F:64` `'No findings in 1 viewport.'` |
| PY-FIRST-STRIP-QUOTES | `C:58` | Of this pass, quotes and apostrophes on the element side in Python: `widths.family.strip("\"'").lower()` | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| PY-FACE-STRIP-QUOTES | `C:51` | Of this pass, the same on the Face side: `failed` built from `face.family.strip("\"'").lower()` | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| **FACE-TRIM** | `J:46` | Of this pass, whitespace on the Face side: `face.family.trim()` | none | ❌ **Survived (56 passed).** Shown: the probe loses `(#pad, " Pad ", 1, 200)` and keeps the other six. Not equivalent |
| **FACE-COLLAPSE-SPACES** | `J:46` | Of this pass, whitespace on the Face side: `face.family.replace(/\s+/g, " ")` | none | ❌ **Survived (56 passed).** Shown: the probe loses `(#two, "Two  Spaces", 1, 200)` and keeps the other six. Not equivalent |
| **FIRST-TRIM** | `J:101` | Of this pass, whitespace on the element side: `bare(names[0]).trim()` | none | ❌ **Survived (56 passed).** Shown: the probe loses `(#pad, " Pad ", 1, 200)` and keeps the other six. Not equivalent |

The rows, exactly, as `(file under src/squint_mcp, old, new)`. The first sixteen are those of passes 3 and 4, unchanged:

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

FACE-UNQUOTE-SINGLE-ONLY  js/font_widths.js
         old:     family: face.family,
         new:     family: face.family.replace(/^'(.*)'$/s, "$1"),

FACE-UNQUOTE-DOUBLE-ONLY  js/font_widths.js
         old:     family: face.family,
         new:     family: face.family.replace(/^"(.*)"$/s, "$1"),

BARE-UNESCAPE-FIRST-ONLY  js/font_widths.js
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/s, "$1");

ELEM-CASE-EXACT         js/font_widths.js
         old:     if (!failed.has(family.toLowerCase())) return;
         new:     if (!failed.has(family)) return;

PY-FIRST-STRIP-QUOTES   checks/font_fallback.py
         old:         family = widths.family.lower()
         new:         family = widths.family.strip("\"'").lower()

PY-FACE-STRIP-QUOTES    checks/font_fallback.py
         old:     failed = {face.family.lower() for face in capture.faces if face.status == "error"}
         new:     failed = {face.family.strip("\"'").lower() for face in capture.faces if face.status == "error"}

FACE-TRIM               js/font_widths.js                 (alive, G1)
         old:     family: face.family,
         new:     family: face.family.trim(),

FACE-COLLAPSE-SPACES    js/font_widths.js                 (alive, G1)
         old:     family: face.family,
         new:     family: face.family.replace(/\s+/g, " "),

FIRST-TRIM              js/font_widths.js                 (alive, G1)
         old:     const family = bare(names[0]);
         new:     const family = bare(names[0]).trim();
```

**Why the three fail the pass.** The Assumption "When the discrimination sensor is satisfied" (`spec.md:96`) and the fourth Success Criterion (`spec.md:330`) ask that the mutants of "the code the last fix round changed" die. The maintainer reads F4 to F6 as one round, and counts against the pass a mutant alive anywhere in that code or in the matching of a First family to a Face. FACE-TRIM and FACE-COLLAPSE-SPACES are of `J:46`, the one line of `src/` the round changed. FIRST-TRIM is of `J:101`, the element side of the same matching. The spec asks for the behaviour each of them breaks. The Term "Failed family" (`spec.md:24`) compares names "without their quotes and whatever their case" and lets nothing else go, and issue #20 expects a Failed family "reported under the name its Face has, whatever characters the name holds". Chromium keeps the whitespace (above), so none of the three is equivalent. They are of the same kind as FACE-UNQUOTE-ONLY and FACE-UNQUOTE-SINGLE-ONLY: one normalization of a name that the code does not do, and that no fixture name would show.

**Mutants considered and not run, argued equivalent.** On the element side, `bare` taking off only double quotes (`/^(")(.*)\1$/s`): Chromium writes every string of a computed `font-family` with double quotes (all the computed values read here), and an unquoted name cannot start with an apostrophe. Taking off only the escapes of `"` and `\` (`/\\(["\\])/g`): Chromium escapes only those two in a string, and writes a control character or a leading digit as a hexadecimal escape, which the design leaves as a known limit (`J:37-39`).

**Sensor depth**: the 16 mutants that passes 3 and 4 name, exactly as they give them (the revert among them), and 8 of this pass on how a name is compared: quotation marks (FACE-UNQUOTE-DOUBLE-ONLY), quotes and apostrophes in Python on both sides (PY-FIRST-STRIP-QUOTES, PY-FACE-STRIP-QUOTES), escapes on the element side (BARE-UNESCAPE-FIRST-ONLY), case on the element side alone (ELEM-CASE-EXACT), and whitespace on both sides (FACE-TRIM, FACE-COLLAPSE-SPACES, FIRST-TRIM).
**Count**: 24 injected; 21 killed; 3 alive (FACE-TRIM, FACE-COLLAPSE-SPACES, FIRST-TRIM: G1); 0 equivalent among those run.

---

## Gate Check

Run here on `38c74f6` with a clean tree, before the sensor.

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py`, then `uv run pytest --collect-only -q`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 121 files already formatted
- **The module of the slice**: 56 passed, 0 failed, 0 skipped, in 154.64s
- **Collected**: 501
- **Linux**: the Linux command of the gate table (`tasks.md:36`), run here in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`) from `38c74f6`, with the name probes before it: 56 passed in 155.69s
- **Test count before the round**: 53 in the module, 498 in the suite (the CI run 38752135720 on `f5ec283`). **After**: 56 and 501. **Delta**: +3, the tests of FNT-63, FNT-64 and FNT-65
- **Skipped**: none. **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened; the diff of `tests/` changes no existing assertion
- **The Build** (the whole suite): not run here. The orchestrator ran it on `38c74f6`, Windows: 501 passed in 20m02s, reported in the brief; its log was not read here. Since `8dc0ead` the diff is one test and one fixture case, and no test of an earlier slice is in the range
- **CI**: the branch is not on the remote (`git ls-remote --heads origin fix/font-name-backslash` is empty), so no CI run of it exists

---

## Evidence for the boxes of spec.md

For the maintainer's closing step. No box is ticked here.

| Box | Evidence now | Where |
| --- | ------------ | ----- |
| Goal 1 (`spec.md:13`): every family of the bug fixture reported once, nothing on the clean fixture | Yes | FNT-02 (`F:51-59`) and FNT-16 (`F:182-186`), green in the Full gate of this pass on Windows and in the Playwright image |
| Goal 2 (`spec.md:14`): a Finding names the family and counts the elements | Yes | FNT-27 (`F:108-134`), the literal with `family` and `elements`; green here |
| Goal 3 (`spec.md:15`): every outcome the same on Windows and on Linux | Yes, for `38c74f6`'s module | 56 passed on Windows and 56 passed in the Playwright image, this pass. The Faces and computed names of `N` and of the probe read the same on both. The CI's Linux has not run `38c74f6`, because the branch is not on the remote |
| Goal 4 (`spec.md:16`): slice 9 marked done in the roadmap once verification passes | The mark exists; the verification of this round does not pass | `docs/ROADMAP.md:111` and `:163`, set by `79a929a` after the PASS of pass 2. This pass is a FAIL, and whether the mark stands is the maintainer's call |
| Success Criterion 1 (`spec.md:327`): all 65 requirements verified, FNT-40 to FNT-46 from file evidence | Yes | "Spec-Anchored Acceptance Criteria" of this report: 65 of 65 |
| Success Criterion 2 (`spec.md:328`): typecheck, lint, format check and the whole suite pass | Yes, by the orchestrator's Build | The Build on `38c74f6` (501 passed, 20m02s), reported in the brief and not read here. pyright, ruff check, ruff format and the module were run again here, all green. On the CI: 38752135720 on `f5ec283` (success), not on `38c74f6` |
| Success Criterion 3 (`spec.md:329`): the first run of the suite on the CI's Linux passes the tests of this slice with no assertion changed for it | Yes for the 53 tests before this round; not yet for the three of FNT-63 to FNT-65 | CI run 38447799140 on `61c4378`, 2026-10-13, success. The tests of FNT-63 to FNT-65 have had no CI run. They pass in the Playwright image here |
| Success Criterion 4 (`spec.md:330`): no mutant a report or a task names alive, nor any of the code the last fix round changed | No | All 16 named by passes 3 and 4 die. FACE-TRIM and FACE-COLLAPSE-SPACES live on `J:46`, the line the round changed, and FIRST-TRIM lives on `J:101` (G1) |

---

## Gaps

- **G1. Whitespace in a family name is held by no case.** FACE-TRIM, FACE-COLLAPSE-SPACES (`J:46`) and FIRST-TRIM (`J:101`) pass the 56 tests. A family declared as `" Pad "` or `"Two  Spaces"` is reported by the code under that name, on both platforms, and each mutant loses one of them. Severity: minor. A name with whitespace at its edges or doubled inside is rare, and the fault would be a missing Finding.

## Fix Plans

### Fix 1 (for the maintainer: this is the third fix iteration)

- **Root cause**: each fixture name of `N` pins one character class. A normalization the code does not do, applied to a class no name holds, goes unseen. The last three passes each found one more class: quotation marks, apostrophes, whitespace.
- **Fix task, if the maintainer wants one**: one case more in `N`, of the shape of F5 and F6. A family declared as `" Two  Spaces "`, with a space at each edge and two inside, and a `src` that names no file; `#spaced-name` of `font-family: " Two  Spaces ", Ahem` on ten glyphs; and the test `reported(client, NAMES, families=(" Two  Spaces ",), on=("#spaced-name",)) == [("#spaced-name", " Two  Spaces ")]`. It should be seen red under each of FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM, and it needs no change to `src/`. A criterion FNT-66 would carry it. The name was read here on both platforms in the probe, as two cases: Chromium keeps the edge spaces and the double space, in the Face and in the computed value.
- **The other way**: accept G1 as a residual, or open it as an issue. The spec's Assumption ties that choice to the maintainer's reading of "the last fix round".
- **Priority**: Minor.

---

## Residuals (not gaps of this round)

- **R1. Slice 10 changed the Capture after the second pass** (`capture.py`, `collect_elements.js`). As passes 3 and 4 found: it does not reach the font path, the 56 tests and the Build hold it, and it was not verified mutant by mutant.
- **R2. Cosmetic wording**: `J:44` says a Face name has "no quotes", and a name can hold quotation marks, apostrophes and edge whitespace, all of which are kept. `design.md:111` says the First family is "without quotes" and leaves out the escapes. `N:20-21`, `N:51` and `N:59` say "Read on Windows" for `'Single'` and `"Quoted"`; this pass read both on Linux as well.
- **R3. The Linux gate is not recorded under T10** for this round. It was run here (56 passed). `tasks.md:36` asks for it before a push when `src/` or `tests/` changed, and recording it there is the orchestrator's job.
- **The residuals of the second report** (R1 to R9 there) stand as it lists them; its R7 is issue #28. Its I-1 (issue #20) is fixed for the backslash, the quotation mark and the apostrophe.
- **Not verified here**: the Build's log, which is the orchestrator's; a CI run of `38c74f6`.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-64 | Implemented (verified by pass 4) | ✅ Verified again at `38c74f6` |
| FNT-65 | Implemented | ✅ Verified |

The criteria all hold; the FAIL is the sensor's (G1), on a rule no criterion states for whitespace. The spec is not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready (one minor gap, for the maintainer)

**Spec-anchored check**: 65 of 65 criteria matched the spec outcome; 0 spec-precision gaps
**Sensor**: 21 of 24 killed; the 16 of passes 3 and 4 all dead, FACE-UNQUOTE-SINGLE-ONLY among them; FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM alive (G1)
**Gate**: Full green on Windows (56 passed, 501 collected) and in the Playwright image (56 passed); the orchestrator's Build of `38c74f6` passed (501)

**What works**: the fix of issue #20 on Windows and on Linux, with the Faces read the same on both; FNT-63 to FNT-65 and their neighbours FNT-58 to FNT-60; every mutant on quotation marks, apostrophes, escapes and case dies, on the Face side and the element side, in `J` and in `C`.

**Issues found**: G1. Whitespace in a family name is kept by the code and pinned by no case.

**Next steps**: the fix loop has run three times, so the maintainer chooses: Fix 1 as F7 (one case, one test, no `src/`), or G1 as a residual or an issue. After that: write the Linux run under T10, push the branch so the CI runs the three new tests on `ubuntu-latest`, and close issue #20 with the pull request.
