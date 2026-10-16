# font-fallback Validation

**Date**: 2026-10-16
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-67, as it is at `d02f632`)
**Diff range**: `f5ec283..d02f632` (12 commits, branch `fix/font-name-backslash`, local only, base `main`). `4015689` is a lessons commit outside the feature; `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4; `135f9a8` is the third pass (FAIL); `e598bb8` and `8dc0ead` are FNT-64 and F5; `9ce2d25` is the fourth pass (PASS with a residual); `a2535ca` and `38c74f6` are FNT-65 and F6; `875eae4` is the fifth pass (FAIL); `2eb1780` adds FNT-66, FNT-67 and plans F7; `d02f632` is F7's code (it was `3332609` before its message was reworded; `git diff 3332609 d02f632` is empty). Across the range `src/` changes in one file, `src/squint_mcp/js/font_widths.js` (14 lines in, 8 out): `J:50` in F4, and `J:11-12`, `J:30`, `J:36`, `J:40-45`, `J:48` and `J:53-54` in F7
**Verifier**: independent sub-agent (author ≠ verifier), sixth verification pass. Not the Verifier of an earlier pass, and not the author of the code, of the tests or of the spec edits

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL - 67 of 67 criteria held on the outcome the spec gives, no spec-precision gap; the gate green (Full and Build on Windows, the module in the Playwright image); all 24 mutants that passes 3 to 5 name die, FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM among them, and so does the revert of each of F7's two code changes; 11 of this pass's 18 mutants live, 6 of them equivalent on every input Chromium 153 can produce and 5 not (G1, G2), all on the lines F7 wrote

F7 does what the fifth pass and the maintainer asked. Whitespace in a family name is now pinned on both sides of the matching, and the two faults F7 measured are fixed: a name that Chromium serializes unquoted with a leading U+00A0, and a name it serializes with a hexadecimal escape. The new decoder is correct on everything Chromium 153 writes: every code point from 0 to 0x10FFFF, swept through the computed `font-family` and back, decodes to the name, with no throw, on Windows and on Linux.

The pass fails on the pins, not on the code. FNT-67 holds the decoder with one escape, `\9`, a single digit that reads the same in base 10 and in base 16 and has no letter case, and is followed by a letter. **HEX-ONE-DIGIT**, **HEX-DECIMAL** and **HEX-UPPER-ONLY** read a two-digit escape wrong (`\1f`, `\7f`, or `\a` for a line feed), and **HEX-ALL-WS** eats a real space that follows an escape; each passes the 58 tests (G1). HEX-DECIMAL throws on `\a`, so on a page with such a family the whole call fails. FNT-66 holds U+00A0 only at the start of a name, and **TRIM-END-UNICODE** drops it at the end of an unquoted name and passes (G2). All five are on lines F7 wrote, so under the maintainer's reading they count against the pass. The fix loop has passed its three iterations: this goes to the maintainer.

Abbreviations: `F` = `tests/test_font_fallback.py`, `D` = `tests/test_detect_visual_bugs.py`, `C` = `src/squint_mcp/checks/font_fallback.py`, `J` = `src/squint_mcp/js/font_widths.js`, `N` = `tests/fixtures/font-fallback-names.html`.

---

## Passes

| Pass | On | Outcome | Where it is kept |
| ---- | -- | ------- | ---------------- |
| 1 | `0b9ae25..ab1dbab` | FAIL. 53 of 53 criteria matched, the gate green, the 11 mutants a task names dead; 10 mutants of its own alive (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr) and 4 argued equivalent | `git show 895bd56:.specs/features/font-fallback/validation.md` |
| Fix round 1 | `ab1dbab..6cd7076` | F1 to F3: FNT-55 to FNT-62, two fixtures and two cases more; no change to `src/` | `tasks.md`, "Fixes of the first validation pass" |
| 2 | `0b9ae25..6cd7076` | PASS. 61 of 61 criteria, 33 of 45 mutants killed, 12 alive (4 equivalent, 8 residual); found I-1, which became issue #20 | `git show 79a929a:.specs/features/font-fallback/validation.md` (with the row of FNT-46 that T12 added; `5caa610` holds it as the Verifier wrote it) |
| Fix round 2 | `f5ec283..c7a4729` | `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4: the case `#slash` in `N`, its test, and the name of a Face taken as `document.fonts` gives it | `tasks.md`, "Fix of issue #20", F4 |
| 3 | `f5ec283..c7a4729` | FAIL. 63 of 63 criteria; 8 mutants (the revert among them), 7 killed; FACE-UNQUOTE-ONLY alive on the changed line | `git show 135f9a8:.specs/features/font-fallback/validation.md` |
| Fix round 3 | `135f9a8..8dc0ead` | `e598bb8` adds FNT-64 and plans F5; `8dc0ead` is F5: the case `#quoted` in `N` and its test; no change to `src/` | `tasks.md`, "Fix of issue #20", F5 |
| 4 | `f5ec283..8dc0ead` | PASS. 64 of 64 criteria; 16 mutants, 15 killed; FACE-UNQUOTE-SINGLE-ONLY alive as a residual, which the maintainer chose to close | `git show 9ce2d25:.specs/features/font-fallback/validation.md` |
| Fix round 4 | `9ce2d25..38c74f6` | `a2535ca` adds FNT-65 and plans F6; `38c74f6` is F6: the case `#single` in `N`, its test, and the top comment of `N` rewritten; no change to `src/` | `tasks.md`, "Fix of issue #20", F6 |
| 5 | `f5ec283..38c74f6` | FAIL. 65 of 65 criteria; 24 mutants, 21 killed; FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM alive (G1 there). Third fix iteration: escalated to the maintainer | `git show 875eae4:.specs/features/font-fallback/validation.md` |
| Fix round 5 | `875eae4..d02f632` | The maintainer asked for a measurement across character classes and accepted FNT-66 and FNT-67 (`2eb1780`). `d02f632` is F7: the cases `#spaced-name`, `#nbsp-name` and `#tab-name` in `N`, two tests, and two changes to `J` (only CSS whitespace trimmed in `namesOf`; hexadecimal escapes decoded in `bare`), with a `ponytail:` on final sigma, design rows and a CHANGELOG line | `tasks.md`, "Fix of issue #20", F7 |
| 6 | `f5ec283..d02f632` | FAIL: this report. 67 of 67 criteria; 46 mutants, 35 killed; the 24 of passes 3 to 5 and the two reverts of F7 dead; 11 of this pass's alive, 6 equivalent and 5 not (G1, G2). Past the three iterations: for the maintainer | This file |

### What the round changed, from git

- **`src/`**: `git diff --stat f5ec283..d02f632 -- src` is `font_widths.js | 22 ++++++++++++++--------`. F4 (`c7a4729`) made `J:50` `family: face.family,`. F7 (`d02f632`) added `trimCssWhitespace` (`J:10-12`) and calls it at `J:30` and `J:36` where `name.trim()` was; replaced the decoder of `bare` (`J:41-45`) and took off its `ponytail:` on hexadecimal escapes; added the comment `J:48`; and replaced the comment above `failed` with a `ponytail:` on final sigma (`J:53-54`). `C` is not in the range.
- **`tests/`**: `N` adds `#slash`, `#quoted`, `#single` (F4 to F6) and `#spaced-name`, `#nbsp-name`, `#tab-name` (F7: `N:73-86`, `N:130-140`, `N:151-153`, and the comment `N:22-28`). `F` adds five tests in the range (`F:560-602`), two of them F7's (`F:587-593`, `F:596-602`). Since `38c74f6` the only hunk of `F` is the insertion at `F:584`: citations up to `F:584` do not move, those after it moved 18 down.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff; 58 tests in the module against 53, 503 collected against 498 (the CI run 38752135720 on `f5ec283`).
- **`.specs/` and docs**: `spec.md` (FNT-63 to FNT-67, the paragraph `spec.md:69`, five traceability rows, "67" twice), `design.md:110-112` and `:220-221`, `tasks.md` (F4 to F7), `validation.md` (passes 3 to 5), `LESSONS.md`, `lessons.json`, `CHANGELOG.md:24`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T12, F1 to F6 | ✅ Done | As passes 2 to 5 found them; their tests pass here unchanged |
| F7 | ✅ Done | Each "Done when" checked. The Faces and computed `font-family` of the three cases were read here on Windows and in the Playwright image and are as `N:22-28` says them. `namesOf` trims only space, tab, LF, CR and FF (`J:11-12`) and does not call `trim`. `bare` decodes 1 to 6 hexadecimal digits with `String.fromCodePoint`, one optional CSS whitespace consumed, and every other escaped character without its backslash (`J:41-45`). The revert of each change fails its test: F7-REVERT-TRIM on `F:590`, F7-REVERT-BARE on `F:600`. FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM fail `F:590`. FNT-58 to FNT-60 and FNT-63 to FNT-65 pass unchanged. The old `ponytail:` on hexadecimal escapes is gone; `J:53-54` and `design.md:221` carry final sigma; `CHANGELOG.md:24` names the fix. Full and Build green here; 58 and 503. The header in `tasks.md` (`test(...)`) is the old one of `3332609`; the orchestrator fixes it |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome. `findings_on` and `sits_on` find an element through `inspect_element`, by its box; `of_family` (`F:253-257`) unpacks exactly one Finding for a family; `reported` (`F:189-204`) returns the `(selector, family)` of every Finding that names one of `families` or sits on one of `on`, so an assertion that it equals a list of pairs says "exactly these Findings, there, under these names".

**What was checked again in full.** FNT-63 to FNT-67 from scratch, against the page as read on both platforms. FNT-58 to FNT-60, the neighbours in `N`, against the fixture and their sentence. Every cited line of `F` was printed at `d02f632`; those up to `F:584` are unchanged since pass 5 (`git diff 38c74f6 d02f632 -- tests/test_font_fallback.py` has one hunk, an insertion at `F:584`). Every row whose outcome rests on matching a First family to a Face (FNT-01, FNT-02, FNT-05, FNT-06, FNT-07, FNT-15, FNT-16, FNT-18, FNT-29, FNT-58 to FNT-60, FNT-63 to FNT-67) dies under at least one mutant of the matching below. FNT-40 to FNT-46 were read again at their lines. The module passed whole on both platforms, and the suite on Windows.

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
| FNT-59 | One Finding for `#comma`, `family` `Acme, Inc` | `F:543-546` `reported(client, NAMES, families=("Acme, Inc",), on=("#comma",)) == [("#comma", "Acme, Inc")]` | ✅ PASS |
| FNT-60 | One Finding for `#inch`, `family` `Vinyl 12"`; computed `"Vinyl 12\"", Ahem` | `F:552-555` `reported(..., families=('Vinyl 12"',), on=("#inch",)) == [("#inch", 'Vinyl 12"')]`; `F:556-557` `finding["evidence"]["computed"]["font-family"] == '"Vinyl 12\\"", Ahem'` | ✅ PASS |
| FNT-63 | One Finding for `#slash`, `family` `Back\slash` | `F:563-566` `reported(client, NAMES, families=("Back\\slash",), on=("#slash",)) == [("#slash", "Back\\slash")]`; the Python literal is one backslash | ✅ PASS |
| FNT-64 | One Finding for `#quoted`, `family` `"Quoted"`, quotation marks included | `F:572-575` `reported(..., families=('"Quoted"',), on=("#quoted",)) == [("#quoted", '"Quoted"')]` | ✅ PASS |
| FNT-65 | One Finding for `#single`, `family` `'Single'`, apostrophes included | `F:581-584` `reported(..., families=("'Single'",), on=("#single",)) == [("#single", "'Single'")]` | ✅ PASS |
| FNT-66 | One Finding on `#spaced-name` with `family` ` Two  Spaces ` (a space at each edge, two inside) and one on `#nbsp-name` with `family` U+00A0 followed by `NBSP` | `F:588-593` `reported(client, NAMES, families=(" Two  Spaces ", " NBSP"), on=("#spaced-name", "#nbsp-name")) == [("#spaced-name", " Two  Spaces "), ("#nbsp-name", " NBSP")]`. Python's literals are the two names, character for character. A Finding under a trimmed or collapsed name would still sit on its element and fail the equality; no Finding fails it too (FACE-TRIM, FIRST-TRIM, F7-REVERT-TRIM, below) | ✅ PASS |
| FNT-67 | One Finding on `#tab-name` with `family` `Tab`, one U+0009, `Name` | `F:599-602` `reported(client, NAMES, families=("Tab\tName",), on=("#tab-name",)) == [("#tab-name", "Tab\tName")]`. The Python literal holds one tab. It holds the outcome the spec gives, and only for an escape of one decimal digit: see G1 | ✅ PASS |

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
| FNT-58 | One Finding on `#dual-normal`, `family` `Dual`, `elements` 2 | `F:537-539` `(family(finding), elements(finding)) == ("Dual", 2)`, `reported(..., families=("DUAL",), on=("#dual-bold",)) == []` | ✅ PASS |
| FNT-61 | `textWidthPx` of `#turned` equals `round(box.w, 2)` | `F:608-610` `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of `#swift` equals `round(box.w, 2)` | `F:616-618` `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks`, the five Checks run | `F:138-142` the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` with `low-contrast-real` in one call; the others by their own slices (`D:449-452`) | ✅ PASS |
| FNT-34 | `isError: true` and the literal of the valid Checks | `D:340-344`, `D:351-355`, `D:362-366`, `D:374-378` the literal `in text`; `D:329` `result.is_error is True` | ✅ PASS |
| FNT-35 | `[]` with the other four Checks | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | The four `(selector, check)` pairs in order, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list | ✅ PASS |
| FNT-37 | The description names the Check and what it reports | `F:156-159` the sentence `in " ".join(tool.description.split())` | ✅ PASS |
| FNT-38 | Earlier tests pass with no change but the four literals | The Build run here on `d02f632`: 503 passed. The range touches no test of an earlier slice (`git diff --stat f5ec283..d02f632 -- tests` is `F` and `N` only) | ✅ PASS |
| FNT-39 | `isError: false`, one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

Each line read again at `d02f632`.

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, registered by name | `C:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | `grep -rn playwright src/squint_mcp/checks/` finds nothing (exit 1); `C:3` imports `squint_mcp.models` only | ✅ PASS |
| FNT-42 | Faces and widths read from the Capture, measured only on request | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`; `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`; `src/squint_mcp/capture.py:371-372` `faces = None` unless `fonts` | ✅ PASS |
| FNT-43 | Equality, no tolerance; no threshold in `config` | `C:67` `if widths.own == widths.tail:`; `C:3` imports no `config`; `src/squint_mcp/config.py:83` (`font-style`) and `:113` (`TEXT_SHAPING_PROPERTIES`), names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG entry with the six things | `CHANGELOG.md:14`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`) | ✅ PASS |
| FNT-45 | README names `font-fallback`, five Checks | `README.md:46` "`detect_visual_bugs` runs five Checks: ... `font-fallback`" | ✅ PASS |
| FNT-46 | Slice 9 `concluída` in the roadmap, table and section, with the link | `docs/ROADMAP.md:111` (table) and `docs/ROADMAP.md:163` (section, with the link to `.specs/features/font-fallback/`) | ✅ PASS (file evidence) |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-47 | Each Finding of the first viewport has one in the second | `F:166-175` `len(desktop) == 2`, `desktop <= mobile` | ✅ PASS |
| FNT-48 | `Twice` on `#twice-normal`, `elements` 2 | `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2` | ✅ PASS |

**Status**: ✅ 67 of 67 criteria covered, each with the outcome the spec gives. No spec-precision gap.

### How the criteria write the names

Within one story the names are written in two notations. FNT-59 to FNT-65 write the name itself between backquotes: `"Quoted"` there is a name of eight characters whose first and last are quotation marks, and `Back\slash` one backslash. FNT-66 and FNT-67 write a JSON string: `" Two  Spaces "` is a name of thirteen characters with no quotation mark, `" NBSP"` and `"Tab\tName"` hold one U+00A0 and one U+0009. Read alone, the backquoted literal of FNT-66 can be taken the way FNT-64's is, quotation marks and all.

It is not a spec-precision gap, because each criterion fixes its characters in words beside the literal. FNT-64 says "quotation marks included". FNT-66 says "including its edge spaces, doubled internal spaces and leading U+00A0": with quotation marks in the name there would be no edge space. FNT-67 says "with one U+0009 between `Tab` and `Name`". `spec.md:69` also declares "The string values of FNT-66 and FNT-67 are written in JSON notation". Every reading the words allow gives one name per criterion, and the tests assert that name (`F:588-593`, `F:599-602`). The mixed notation is a residual for the maintainer (R2).

### The names, read from the page

Read with a script outside the repository (Playwright, Chromium 153.0.8010.12), at `d02f632`, on Windows and in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`). The two platforms gave the same output to the character (a `diff` of the two logs is empty).

- **`N`, `document.fonts`**, as JSON: `Ahem` `loaded`, then `Dual`, `DUAL`, `Acme, Inc`, `Vinyl 12\"`, `Back\\slash`, `\"Quoted\"`, `'Single'`, `" Two  Spaces "`, `" NBSP"`, `"Tab\tName"`, all `error`, in this order. This is what `N:13-28` says.
- **`N`, computed `font-family`**, as JSON: `#spaced-name` `"\" Two  Spaces \", Ahem"`; `#nbsp-name` `" NBSP, Ahem"`, unquoted; `#tab-name` `"\"Tab\\9 Name\", Ahem"`. `#slash`, `#quoted`, `#single`, `#inch` and `#comma` are as passes 3 to 5 read them.
- **`N`, the tool**: on both platforms `(#dual-normal, Dual, 2)`, `(#comma, Acme, Inc, 1)`, `(#inch, Vinyl 12", 1)`, `(#slash, Back\slash, 1)`, `(#quoted, "Quoted", 1)`, `(#single, 'Single', 1)`, `(#spaced-name, " Two  Spaces ", 1)`, `(#nbsp-name, " NBSP", 1)` and `(#tab-name, "Tab\tName", 1)`, each with `textWidthPx` 200.
- **The probe page** (`p6.html`, outside the repository): sixteen families with a `src` that names no file, each on ten Ahem glyphs, declared in CSS as `"Unit\1f Sep"`, `"Del\7f X"`, `"Line\a Feed"`, `"Tab\9  Space"` (a tab and then a space), `"NBSP\a0"`, `"Ctl\1 beef"`, `"Tab\9 Name"`, `" Two  Spaces "`, `"\a0 NBSP"`, `"Back\\9 x"`, `"Up\1F X"`, `"Nul\0 X"`, `"Emoji\1F600 X"`, `"Lone\d800 X"`, `"Big\110000 X"` and `"Em\2003 Space"`. Every Face keeps its name as CSS parses it; `\0`, `\d800` and `\110000` become U+FFFD. The computed values write a control character as a lowercase escape of one or two digits and one space (`"Unit\\1f Sep"`, `"Up\\1f X"` from `\1F`, `"Line\\a Feed"`, `"Tab\\9  Space"`), and write every other name raw: unquoted when it is one identifier (`NBSP` + U+00A0, `Em` + U+2003 + `Space`, `Nul` + U+FFFD + `X`, the emoji), quoted otherwise. The tool reports all sixteen, under the name of the Face. Same on both platforms.

---

## The new code against CSS Syntax and Chromium 153

**Against CSS Syntax** (Consume an escaped code point, §4.3.7). `bare` (`J:41-45`) takes 1 to 6 hexadecimal digits of either case and consumes one whitespace after them, as the standard does. It departs in three places: a value of 0, a surrogate or above 0x10FFFF gives U+0000, a lone surrogate, or a `RangeError` from `String.fromCodePoint`, where the standard gives U+FFFD; a backslash at the end of the name is kept, where the standard drops it; and a backslash before a newline gives the newline, where inside a string the standard drops both.

**Against what Chromium 153 writes.** None of the three can be reached. Chromium turns `\0`, a surrogate and anything above 0x10FFFF into U+FFFD when it parses, and writes U+FFFD raw. It escapes in a computed `font-family` only `"` and `\`, with a backslash, and U+0001 to U+001F and U+007F, as one or two lowercase hexadecimal digits and one space. It never writes a lone trailing backslash or an escaped newline. The sweep shows it. Every code point from 0 to 0x10FFFF, with 0x110000 and 0xFFFFFF, was written as a CSS hexadecimal escape into `"A" + char + "B"`, then read back from the computed `font-family` and passed through `namesOf` and `bare`, as `J:11-45` has them. Below U+0800, around the surrogates and at the top of the range it was also tried alone, before an `f`, before a space and before a tab. That is 1,130,698 names, with 0 throws and 0 names that differ from the one CSS parses, on Windows and in the Playwright image. **No input Chromium 153 can produce makes `bare` throw or mis-decode.** The throw is a latent edge only. `bare` sees nothing but the computed values of Chromium, and its comment (`J:40`) says so.

`trimCssWhitespace` (`J:11-12`) trims space, tab, LF, CR and FF. Chromium writes no whitespace around a name but the space after each comma. A quoted name keeps its spaces inside the quotes, and an unquoted name can hold U+00A0 or U+2003 but no CSS whitespace. So the helper takes off exactly that one space, as `trim` did, and keeps what `trim` dropped.

---

## The spec, design and fixture edits of the round

| # | Edit | Judgement |
| - | ---- | --------- |
| E1 | `spec.md:69`, the paragraph: FNT-63 to FNT-65 as pass 5 found them; "On 2026-10-16, after the fifth pass found whitespace unpinned ... accepted FNT-66 and FNT-67 ... with F7 correcting the two bugs measured on Chromium 153; the mismatch ... for final sigma stays an accepted limit. The string values of FNT-66 and FNT-67 are written in JSON notation." | Accurate. The two faults are real: F7-REVERT-TRIM loses `#nbsp-name` and F7-REVERT-BARE loses `#tab-name` (below). The final-sigma limit is real: on a probe page whose Face is `ΟΔΟΣ`, `#same` (`"ΟΔΟΣ"`) is reported and `#small` (`"οδοσ"`) is not counted (`elements` 1) |
| E2 | `spec.md:145`, FNT-66 | Accurate on every fact, each read here on both platforms: the two declarations (`N:74-80`), the two `font-family` (`N:130-136`), the Faces, and the outcome. Notation: see "How the criteria write the names" |
| E3 | `spec.md:146`, FNT-67: "a tab, which Chromium serializes as a hexadecimal escape" | Accurate: the computed value is `"Tab\9 Name", Ahem` on both platforms. "The hexadecimal escape is decoded to the character held by the Face name" is what `J:43-44` does |
| E4 | `spec.md:322-323`, `:325`, `:331`: two traceability rows and "67" twice | Accurate: 67 rows, FNT-01 to FNT-67, each with a task |
| E5 | `design.md:110`, `faces`: "as `document.fonts` gives it ... quotation marks, apostrophes, backslashes and whitespace that belong to the name are kept; FNT-63 to FNT-67" | Accurate. It closes R2 of pass 5 for the design |
| E6 | `design.md:111-112`: `family` "without its surrounding quotes and with its escapes decoded"; "Only CSS whitespace ... is trimmed ... 1 to 6 hexadecimal digits become their code point, consuming one optional CSS whitespace, and every other escaped character is kept without its backslash" | Accurate to `J:11-12` and `J:41-45`. "Become their code point" is true of every escape Chromium writes; the three departures from CSS Syntax above are not said, and cannot be reached (R3) |
| E7 | `design.md:220`: the hexadecimal-escape row now "Handled by F7; FNT-67 pins a tab"; the old row's example, a name that starts with a digit, is gone | Accurate. Chromium writes such a name as a quoted string with no escape, so the old example was never right. "FNT-67 pins a tab" is literally true, and the pin is weaker than the row suggests (G1) |
| E8 | `design.md:221`, final sigma, and `J:53-54`, its `ponytail:` | Accurate, as E1 measured. "Chromium matches them" cannot be seen through the width, since the text falls back either way. The limit is that the tool does not count the element |
| E9 | `N:22-28`, the comment on the three Faces: "read on Windows ... These three were not read in the Playwright Linux image" | Accurate when written. This pass read all three in the image and found them the same, so the comment is one platform short of the truth. Cosmetic. It writes the first name `" Two  Spaces "` with the quotation marks that delimit it, a third notation |
| E10 | `J:48` (F7): "`document.fonts` gives the name of a Face with no quotes and no escapes" | Accurate now that `design.md:110` says what is kept. "No quotes" means no quotes put around the name |
| E11 | `CHANGELOG.md:24`, under `### Fixed`: "`font-fallback` preserves Unicode whitespace at the edges of family names and reports names that Chromium serializes with hexadecimal escapes, such as a tab." | True of the code. The Check itself is unreleased (it is under `### Added`, `:14`), so a fix to it under `### Fixed` describes a change no release had. A blank line follows the bullet, inside the list. Cosmetic (R4) |

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work and empty after it (0 bytes both times). Each mutant ran on its own copy of `src/squint_mcp`, copied whole with `__pycache__` left out, under the session's scratch directory outside the repository. The mutation went into the copy only, line endings kept, and the runner stopped before any run unless each `old` occurred exactly once in its file. Each run was `uv run pytest tests/test_font_fallback.py -q -p no:cacheprovider -p squint_guard --tb=line -rf`, from the repository, with `PYTHONPATH` set to the copy's root and the guard's directory and `PYTHONDONTWRITEBYTECODE=1`. The plugin `squint_guard` exits the session at configure, and again at unconfigure, unless `squint_mcp`, `squint_mcp.capture` and `squint_mcp.checks.font_fallback` are files of the copy and `capture._FONT_WIDTHS` equals the copy's `font_widths.js`. All 47 runs printed `GUARD OK <copy>`. The copy without a mutant ran first: 58 passed. Two pytest processes ran at a time, each in its own copy, each on the whole module, with no `-x`. There was no `git stash` and no worktree, and nothing under `src/` or `tests/` was edited. Each copy was deleted after its run; the `copies` directory is empty.

Two instruments, both outside the repository. **"Shown"** means the probe page `p6.html`, called through the in-memory client from a mutated copy (`squint_mcp.__file__` checked to be in the copy), returned something different from the code. **"Swept"** means the code-point sweep above, run with the mutated `J`. It counts the names, out of 1,130,698, that the mutant decodes wrong or throws on.

| # | `file:line` | Mutation | Tests that failed | Result |
| - | ----------- | -------- | ----------------- | ------ |
| REVERT | `J:50` | `family: bare(face.family),` | FNT-63, FNT-64, FNT-65 | ✅ Killed: `F:564` `[] == [('#slash', 'Back\\slash')]`, `F:573`, `F:582` |
| N60-unescape-quotes-only | `J:42-45` | `bare` keeps only `\"` → `"` | FNT-63, FNT-67 | ✅ Killed: `F:564`; `F:600` `[] == [('#tab-name', 'Tab\tName')]` |
| FACE-UNQUOTE-ONLY | `J:50` | Quotes taken off the Face name | FNT-64, FNT-65 | ✅ Killed: `F:573` `[] == [('#quoted', '"Quoted"')]`, `F:582` |
| FACE-UNESCAPE-ONLY | `J:50` | Escapes taken off the Face name | FNT-63, alone | ✅ Killed: `F:564` |
| FACE-LOWER | `J:50` | The Face name in lower case | 37 tests, the first FNT-01 | ✅ Killed: `F:41` `[] == ['#heading']`; `F:80` `'icon set' == 'Icon Set'` |
| CASE-EXACT | `J:58`, `J:107` | No case folding, either side | FNT-15, FNT-06, FNT-29 | ✅ Killed: `F:269` the list of twelve differs; `F:263` finds no Finding on `#lower` |
| FIRST-NOT-BARE | `J:106` | `const family = names[0];` | 30 tests, among them FNT-02, FNT-03 | ✅ Killed: `F:51`; `F:64` `'Found 1 finding...' == 'Found 2 find...'` |
| NAMESOF-DROP-BACKSLASH | `J:21` | `namesOf` drops the backslash of an escape | FNT-63, FNT-67 | ✅ Killed: `F:564`, `F:600` |
| BARE-UNQUOTE-ONLY | `J:42-45` | `bare` keeps every escape | FNT-60, FNT-63, FNT-64, FNT-67 | ✅ Killed: `F:553` `[] == [('#inch', 'Vinyl 12"')]`, `F:564`, `F:573` |
| BARE-STRIP-ALL-QUOTES | `J:42-45` | Every quotation mark and apostrophe at either end, and the old decoder | FNT-60, FNT-64, FNT-65, FNT-67 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| FIRST-ANY-FAILED | `J:106` | The first Failed family of the list is judged | FNT-16, FNT-18 | ✅ Killed: `F:184`; `F:216` `[('#second', 'Second Choice')] == []` |
| NAMESOF-ESCAPE-AFTER-QUOTE | `J:20-25` | Inside a string a backslash no longer escapes | FNT-60, FNT-64 | ✅ Killed: `F:553`, `F:573` |
| PY-LAST-FACE-NAME | `C:50` | Named as its last Face has it | FNT-58, alone | ✅ Killed: `F:538` `('DUAL', 2) == ('Dual', 2)` |
| PY-CASE-EXACT-FIRST | `C:58` | First family not folded in Python | 47 tests, the first FNT-01 | ✅ Killed: `F:41`, `F:64` |
| PY-NAME-FROM-ELEMENT | `C:69` | Named as the element writes it | FNT-15, FNT-06, FNT-29 | ✅ Killed: `F:330` `'missing brand' == 'Missing Brand'` |
| FACE-UNQUOTE-SINGLE-ONLY | `J:50` | Apostrophes taken off the Face name | FNT-65, alone | ✅ Killed: `F:582` `[] == [('#single', "'Single'")]` |
| FACE-UNQUOTE-DOUBLE-ONLY | `J:50` | Quotation marks taken off the Face name | FNT-64, alone | ✅ Killed: `F:573` |
| BARE-UNESCAPE-FIRST-ONLY | `J:42-45` | Only the first escape taken off, old decoder | FNT-64, FNT-67 | ✅ Killed: `F:573`, `F:600` |
| ELEM-CASE-EXACT | `J:107` | `failed.has(family)` | 47 tests, the first FNT-01 | ✅ Killed: `F:41`, `F:64` |
| PY-FIRST-STRIP-QUOTES | `C:58` | `widths.family.strip("\"'")` | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| PY-FACE-STRIP-QUOTES | `C:51` | The same on the Face side | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| FACE-TRIM | `J:50` | `face.family.trim()` | FNT-66, alone | ✅ **Killed** (alive in pass 5): `F:590` `[] == [('#spaced-na..., '\xa0NBSP')]` |
| FACE-COLLAPSE-SPACES | `J:50` | `face.family.replace(/\s+/g, " ")` | FNT-66, FNT-67 | ✅ **Killed** (alive in pass 5): `F:590`; `F:600` |
| FIRST-TRIM | `J:106` | `bare(names[0]).trim()` | FNT-66, alone | ✅ **Killed** (alive in pass 5): `F:590` |
| BARE-STRIP-ALL-QUOTES/new-decoder | `J:42` | As BARE-STRIP-ALL-QUOTES, the new decoder kept | FNT-60, FNT-64, FNT-65 | ✅ Killed: `F:553`, `F:573`, `F:582` |
| BARE-UNESCAPE-FIRST-ONLY/new-decoder | `J:43` | The new decoder without `g` | FNT-64, alone | ✅ Killed: `F:573` |
| F7-REVERT-TRIM | `J:12` | `name.trim()`, F7's first change taken back | FNT-66, alone | ✅ Killed: `F:590` `[('#spaced-na...wo  Spaces ')] == [..., ('#nbsp-name', '\xa0NBSP')]` |
| F7-REVERT-BARE | `J:42-45` | The pre-F7 `bare`, `\X` to `X` only | FNT-67, alone | ✅ Killed: `F:600` `[] == [('#tab-name', 'Tab\tName')]` |
| HEX-NO-WS | `J:43` | No whitespace consumed after the digits | FNT-67, alone | ✅ Killed: `F:600` |
| TRIM-START-UNICODE | `J:12` | Trailing CSS whitespace trimmed, then `trimStart()` | FNT-66, alone | ✅ Killed: `F:590` |
| FACE-TRIM-END | `J:50` | `face.family.trimEnd()` | FNT-66, alone | ✅ Killed: `F:590` `[('#nbsp-name', '\xa0NBSP')] == [...]` |
| FIRST-COLLAPSE-SPACES | `J:106` | `bare(names[0]).replace(/ +/g, " ")` | FNT-66, alone | ✅ Killed: `F:590` |
| FIRST-TRIM-END | `J:106` | `bare(names[0]).trimEnd()` | FNT-66, alone | ✅ Killed: `F:590` |
| PY-FIRST-RSTRIP | `C:58` | `widths.family.rstrip().lower()` | FNT-66, alone | ✅ Killed: `F:590` |
| PY-FACE-LSTRIP | `C:51` | `failed` built from `face.family.lstrip()` | FNT-66, alone | ✅ Killed: `F:590` `[] == [...]` |
| **HEX-ONE-DIGIT** | `J:43` | `[0-9a-f]{1}` for `{1,6}` | none | ❌ **Survived (58 passed).** Swept: 85 wrong, from U+0010 (`\10 ` read as U+0001 and `0 `). Shown: loses `#us` (`Unit` U+001F `Sep`), `#del` (U+007F) and `#upper` |
| **HEX-DECIMAL** | `J:44` | `parseInt(hex, 10)` | none | ❌ **Survived (58 passed).** Swept: 30 throws (`RangeError: Invalid code point NaN` on `\a`, `\b`, `\c`, `\d`, `\e`, `\f`) and 85 wrong. Shown: the call on the probe page returns `isError: true` ("Error executing tool detect_visual_bugs"), and all sixteen Findings are lost |
| **HEX-UPPER-ONLY** | `J:43` | `[0-9A-F]` and no `i` flag | none | ❌ **Survived (58 passed).** Swept: 65 wrong, `\a ` kept as `a `. Shown: loses `#us`, `#del`, `#lf` and `#upper` |
| **HEX-ALL-WS** | `J:43` | `[ \t\n\r\f]*` for `?` | none | ❌ **Survived (58 passed).** Swept: 32 wrong, a real space after a control character eaten. Shown: loses `#tabsp` (`Tab` U+0009 ` Space`) |
| **TRIM-END-UNICODE** | `J:12` | Leading CSS whitespace trimmed, then `trimEnd()` | none | ❌ **Survived (58 passed).** Swept: 1 wrong, a name that is U+00A0 alone. Shown: loses `#nbspend` (`NBSP` U+00A0, written unquoted) |
| HEX-TWO-DIGITS | `J:43` | `{1,2}` | none | Survived, **equivalent**: swept 0 wrong, shown nothing lost. Chromium writes at most two digits |
| HEX-WS-SPACE-ONLY | `J:43` | ` ?` for `[ \t\n\r\f]?` | none | Survived, **equivalent**: swept 0, shown 0. Chromium writes a space after an escape, never another whitespace |
| HEX-LOWER-ONLY | `J:43` | No `i` flag | none | Survived, **equivalent**: swept 0, shown 0. Chromium writes lowercase digits (`\1F` comes back `\1f`) |
| HEX-FROMCHARCODE | `J:44` | `String.fromCharCode` | none | Survived, **equivalent**: swept 0, shown 0. Every escape Chromium writes is at most U+007F |
| TRIM-START-ONLY | `J:12` | Only leading CSS whitespace trimmed | none | Survived, **equivalent**: swept 0, shown 0. Chromium writes no whitespace before a comma or at the end |
| TRIM-SPACE-ONLY | `J:12` | `/^ +| +$/g` | none | Survived, **equivalent**: swept 0, shown 0. The only whitespace around a name is the space after a comma |

The rows as `(file under src/squint_mcp, old, new)`. The 24 of passes 3 to 5 are exactly as `git show 875eae4:.specs/features/font-fallback/validation.md` gives them. Four of them (N60-unescape-quotes-only, BARE-UNQUOTE-ONLY, BARE-STRIP-ALL-QUOTES, BARE-UNESCAPE-FIRST-ONLY) had as `old` the one-line `bare` that F7 replaced. Their `new` line, as given, was put in place of the whole of `bare`'s body, `J:42-45`, so each also takes back the new decoder. The two `/new-decoder` rows apply the same intent and keep the decoder. NAMESOF-ESCAPE-AFTER-QUOTE swaps the first two branches of the loop (`J:20-25`), as pass 5 describes it. The mutants of this pass:

```
BARE_OLD (J:42-45) =
    name.replace(/^(["'])(.*)\1$/s, "$2").replace(
      /\\(?:([0-9a-f]{1,6})[ \t\n\r\f]?|(.))/gis,
      (_, hex, char) => (hex ? String.fromCodePoint(parseInt(hex, 16)) : char),
    );
DECODER (J:43) = /\\(?:([0-9a-f]{1,6})[ \t\n\r\f]?|(.))/gis,
TRIM (J:12)    =     name.replace(/^[ \t\n\r\f]+|[ \t\n\r\f]+$/g, "");

BARE-STRIP-ALL-QUOTES/new-decoder  old: name.replace(/^(["'])(.*)\1$/s, "$2").replace(
                                   new: name.replace(/^["']+|["']+$/g, "").replace(
BARE-UNESCAPE-FIRST-ONLY/new-decoder  DECODER, flags gis -> is
F7-REVERT-TRIM       TRIM -> name.trim();          (F7's NAMESOF-JS-TRIM)
F7-REVERT-BARE       BARE_OLD -> name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");   (F7's BARE-SIMPLE-ESCAPES)
HEX-ONE-DIGIT        DECODER: {1,6} -> {1}
HEX-TWO-DIGITS       DECODER: {1,6} -> {1,2}
HEX-DECIMAL          parseInt(hex, 16) -> parseInt(hex, 10)
HEX-NO-WS            DECODER: [ \t\n\r\f]? removed
HEX-ALL-WS           DECODER: [ \t\n\r\f]? -> [ \t\n\r\f]*
HEX-WS-SPACE-ONLY    DECODER: [ \t\n\r\f]? -> " ?"
HEX-LOWER-ONLY       DECODER: flags gis -> gs
HEX-UPPER-ONLY       DECODER: [0-9a-f] -> [0-9A-F], flags gis -> gs
HEX-FROMCHARCODE     String.fromCodePoint(parseInt(hex, 16)) -> String.fromCharCode(parseInt(hex, 16))
TRIM-END-UNICODE     TRIM -> name.replace(/^[ \t\n\r\f]+/g, "").trimEnd();
TRIM-START-UNICODE   TRIM -> name.replace(/[ \t\n\r\f]+$/g, "").trimStart();
TRIM-START-ONLY      TRIM -> name.replace(/^[ \t\n\r\f]+/g, "");
TRIM-SPACE-ONLY      TRIM -> name.replace(/^ +| +$/g, "");
FACE-TRIM-END        family: face.family, -> family: face.family.trimEnd(),
FIRST-COLLAPSE-SPACES  const family = bare(names[0]); -> const family = bare(names[0]).replace(/ +/g, " ");
FIRST-TRIM-END       const family = bare(names[0]); -> const family = bare(names[0]).trimEnd();
PY-FIRST-RSTRIP      family = widths.family.lower() -> family = widths.family.rstrip().lower()
PY-FACE-LSTRIP       failed = {face.family.lower() ...} -> failed = {face.family.lstrip().lower() ...}
```

**Why the five fail the pass.** The Assumption "When the discrimination sensor is satisfied" (`spec.md:96`) and the fourth Success Criterion (`spec.md:334`) ask that the mutants of "the code the last fix round changed" die. The maintainer reads F4 to F7 as one round, and counts against the pass a mutant alive anywhere in that code or in the matching of a First family to a Face. All five live on lines F7 wrote (`J:12`, `J:43`, `J:44`), and none is equivalent: each loses a Finding the code gives on a name Chromium 153 writes, and HEX-DECIMAL fails the whole call. FNT-67 says "the hexadecimal escape is decoded to the character held by the Face name", and FNT-66 says "whitespace that is part of a family name is preserved". Each mutant breaks that rule for a name the criterion does not hold.

**The six equivalents.** Each departs from CSS Syntax only on input Chromium 153 never writes. The sweep shows it over every code point, on both platforms, and the probe shows it through the tool. They stop being equivalent if a later Chromium writes escapes of more digits, in upper case or followed by another whitespace. That is not a gap of this round.

**Sensor depth**: the 24 mutants of passes 3 to 5, exactly as they give them; 2 of them carried onto the new decoder; the revert of each of F7's two code changes; and 18 of this pass on how a name is compared. They cover the count of hexadecimal digits (HEX-ONE-DIGIT, HEX-TWO-DIGITS), their base and case (HEX-DECIMAL, HEX-LOWER-ONLY, HEX-UPPER-ONLY, HEX-FROMCHARCODE), the whitespace consumed after them (HEX-NO-WS, HEX-ALL-WS, HEX-WS-SPACE-ONLY), which whitespace is trimmed and where (TRIM-END-UNICODE, TRIM-START-UNICODE, TRIM-START-ONLY, TRIM-SPACE-ONLY), and the Face side against the element side in JavaScript and in Python (FACE-TRIM-END, FIRST-COLLAPSE-SPACES, FIRST-TRIM-END, PY-FIRST-RSTRIP, PY-FACE-LSTRIP).
**Count**: 46 injected; 35 killed; 11 alive: 6 equivalent, 5 not (HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY, HEX-ALL-WS: G1; TRIM-END-UNICODE: G2).

---

## Gate Check

Run here on `d02f632` (tree identical to `3332609`) with a clean tree.

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py`, then `uv run pytest --collect-only -q`; Build, the same with `uv run pytest`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 121 files already formatted
- **The module of the slice**: 58 passed, 0 failed, 0 skipped, in 171.91s
- **Collected**: 503
- **Build**: run here in the background with a log and awaited: the three static checks as above, then 503 passed in 1330.20s (22:10), exit 0
- **Linux**: the Linux command of the gate table (`tasks.md:36`), run here in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a...0da1f0`) from `d02f632`, with the name reads and the sweep before it: 58 passed in 174.79s
- **Test count before the round**: 53 in the module, 498 in the suite (the CI run 38752135720 on `f5ec283`). **After**: 58 and 503. **Delta**: +5, the tests of FNT-63 to FNT-67
- **Skipped**: none. **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened; the diff of `tests/` changes no existing assertion
- **CI**: the branch is not on the remote, so no CI run of it exists

---

## Evidence for the boxes of spec.md

For the maintainer's closing step. No box is ticked here.

| Box | Evidence now | Where |
| --- | ------------ | ----- |
| Goal 1 (`spec.md:13`): every family of the bug fixture reported once, nothing on the clean fixture | Yes | FNT-02 (`F:51-59`) and FNT-16 (`F:182-186`), green in the Full and Build of this pass on Windows and in the Playwright image |
| Goal 2 (`spec.md:14`): a Finding names the family and counts the elements | Yes | FNT-27 (`F:108-134`), the literal with `family` and `elements`; green here |
| Goal 3 (`spec.md:15`): every outcome the same on Windows and on Linux | Yes, for `d02f632`'s module | 58 passed on Windows and 58 passed in the Playwright image, this pass. The Faces and computed names of `N` and of the probe read the same on both. The CI's Linux has not run `d02f632`, because the branch is not on the remote |
| Goal 4 (`spec.md:16`): slice 9 marked done in the roadmap once verification passes | The mark exists; the verification of this round does not pass | `docs/ROADMAP.md:111` and `:163`, set by `79a929a` after the PASS of pass 2. This pass is a FAIL, and whether the mark stands is the maintainer's call |
| Success Criterion 1 (`spec.md:331`): all 67 requirements verified, FNT-40 to FNT-46 from file evidence | Yes | "Spec-Anchored Acceptance Criteria" of this report: 67 of 67 |
| Success Criterion 2 (`spec.md:332`): typecheck, lint, format check and the whole suite pass | Yes | The Build run here on `d02f632`: pyright, ruff check, ruff format, 503 passed. On the CI: 38752135720 on `f5ec283` (success), not on `d02f632` |
| Success Criterion 3 (`spec.md:333`): the first run of the suite on the CI's Linux passes the tests of this slice with no assertion changed for it | Yes for the 53 tests before this round; not yet for the five of FNT-63 to FNT-67 | CI run 38447799140 on `61c4378`, 2026-10-13, success. The tests of FNT-63 to FNT-67 have had no CI run. They pass in the Playwright image here |
| Success Criterion 4 (`spec.md:334`): no mutant a report or a task names alive, nor any of the code the last fix round changed | No | All 24 named by passes 3 to 5 die, and the five F7 names in `tasks.md`. HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY and HEX-ALL-WS live on `J:43-44` (G1), and TRIM-END-UNICODE on `J:12` (G2), all on lines F7 wrote |

---

## Gaps

- **G1. The hexadecimal decoder is pinned by one escape that every misreading reads the same.** FNT-67's `\9` is one digit, the same in base 10 and in base 16, with no letter case, and it is followed by a letter. HEX-ONE-DIGIT, HEX-DECIMAL and HEX-UPPER-ONLY (`J:43-44`) misread a two-digit escape or an escape with a letter digit, and HEX-ALL-WS eats a real space after an escape. Each passes the 58 tests and loses a Finding the code gives, on a name Chromium writes. HEX-DECIMAL throws, and the whole call fails. Severity: minor. A family name with a control character in it is rare, and the fault is a missing Finding, or with HEX-DECIMAL a failed call.
- **G2. U+00A0 at the end of an unquoted name is held by no case.** FNT-66 has it only at the start. TRIM-END-UNICODE (`J:12`) trims Unicode whitespace at the end of a name, passes, and loses `NBSP` + U+00A0, which Chromium writes unquoted. Severity: minor.

## Fix Plans

### Fix 1 (for the maintainer: past the three fix iterations)

- **Root cause**: as in passes 3 to 5, each new case pins the simplest member of its class. A decoder needs an escape whose value changes under each misreading, and a trim needs the character at both ends.
- **Fix task, if the maintainer wants one**: two cases more in `N`, of the shape of F7, each with a `src` that names no file and ten glyphs, and no change to `src/`:
  - `#ctl-name`, of `font-family: "Unit\1f  Sep", Ahem`. Its name is `Unit`, U+001F, a space and `Sep`, and Chromium writes it `"Unit\1f  Sep"`. The test is `reported(client, NAMES, families=("Unit\x1f Sep",), on=("#ctl-name",)) == [("#ctl-name", "Unit\x1f Sep")]`. By the sweep it should be red under each of HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY and HEX-ALL-WS: `1f` is two digits, has a letter and differs in base 10, and the real space follows the consumed one.
  - `#nbsp-end`, of `font-family: "NBSP\a0", Ahem`. Its name is `NBSP` and U+00A0, which Chromium writes unquoted. The test is `reported(client, NAMES, families=("NBSP ",), on=("#nbsp-end",)) == [("#nbsp-end", "NBSP ")]`. It should be red under TRIM-END-UNICODE.

  Both names were read here on both platforms on the probe page (`#us`, `#tabsp`, `#nbspend`), and the code reports them. A criterion FNT-68 would carry them. The new tests should be seen red under each mutant on a scratch copy before the cases are committed. Neither combination was run as a test here.
- **The other way**: accept G1 and G2 as residuals, or open them as an issue. The code is right on every input Chromium 153 writes, as the sweep shows. What is missing is a pin.
- **Priority**: Minor.

---

## Residuals (not gaps of this round)

- **R1. Slice 10 changed the Capture after the second pass** (`capture.py`, `collect_elements.js`). As passes 3 to 5 found: it does not reach the font path, the 58 tests and the Build hold it, and it was not verified mutant by mutant.
- **R2. Three notations for a family name** in one story: raw between backquotes (FNT-59 to FNT-65), JSON (FNT-66, FNT-67, declared once at `spec.md:69`), and CSS with its delimiting quotes in `N:23`. Each criterion fixes its characters in words, so no outcome is unclear. Writing every expected name in one notation, or saying it in each criterion, would spare the next reader the comparison.
- **R3. `bare` departs from CSS Syntax on input Chromium does not write**: U+0000, surrogates and values above 0x10FFFF (a `RangeError` for the last), a trailing backslash, an escaped newline. Unreachable by the sweep; `design.md:112` does not say it.
- **R4. Cosmetic wording**: `N:22-28` says the three Faces of F7 were "not read in the Playwright Linux image", and this pass read them there and found them the same. `CHANGELOG.md:24` is a `### Fixed` entry for a Check that is itself unreleased, followed by a blank line inside the list. The header of F7 in `tasks.md` is the old one of `3332609`, which is the orchestrator's to fix.
- **R5. The Linux gate is not recorded under T10** for this round. It was run here (58 passed). `tasks.md:36` asks for it before a push when `src/` or `tests/` changed.
- **The residuals of the second report** (R1 to R9 there) stand as it lists them; its R7 is issue #28. Its I-1 (issue #20) is fixed for the backslash, the quotation mark, the apostrophe, whitespace and hexadecimal escapes.
- **Not verified here**: a CI run of `d02f632`.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-65 | Implemented (verified by pass 5) | ✅ Verified again at `d02f632` |
| FNT-66, FNT-67 | Implemented | ✅ Verified |

The criteria all hold; the FAIL is the sensor's (G1, G2), on inputs no criterion names. The spec is not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready (two minor gaps, for the maintainer)

**Spec-anchored check**: 67 of 67 criteria matched the spec outcome; 0 spec-precision gaps
**Sensor**: 35 of 46 killed. All 24 of passes 3 to 5 are dead, FACE-TRIM, FACE-COLLAPSE-SPACES and FIRST-TRIM among them, and so are both F7 reverts. 11 of this pass's live: 6 equivalent on every input Chromium 153 writes, and 5 not (HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY, HEX-ALL-WS: G1; TRIM-END-UNICODE: G2)
**Gate**: Full green on Windows (58 passed, 503 collected); Build green on Windows (503 passed); the module green in the Playwright image (58 passed)

**What works**: the fix of issue #20, now for whitespace and hexadecimal escapes too, the same on Windows and on Linux. The decoder is right on all 1,130,698 serialized names of the sweep, with no throw. Every mutant on quotation marks, apostrophes, backslashes, case and whitespace at the start of a name dies, on the Face side and the element side, in `J` and in `C`.

**Issues found**: G1, the decoder pinned by an escape every misreading reads the same. G2, U+00A0 at the end of an unquoted name pinned by no case.

**Next steps**: past the three fix iterations, so the maintainer chooses. Either Fix 1 as F8 (two cases, two tests, no `src/`), or G1 and G2 as residuals or an issue. After that: write the Linux run under T10, push the branch so the CI runs the five new tests on `ubuntu-latest`, and close issue #20 with the pull request.
