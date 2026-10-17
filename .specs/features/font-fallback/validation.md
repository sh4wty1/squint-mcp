# font-fallback Validation

**Date**: 2026-10-16
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-67, as it is at `bdbef50`)
**Diff range**: this pass verifies F8, `e5ffa21..bdbef50` (one commit, `bdbef50`), on top of the round `f5ec283..bdbef50` (14 commits, branch `fix/font-name-backslash`, local only, base `main`) that pass 6 verified up to `d02f632`. `e5ffa21` is the sixth pass (FAIL); `bdbef50` is F8: `spec.md` (FNT-66, FNT-67, the paragraph `spec.md:69`), `tasks.md` (F8, and F7's commit header), `N` and `F`. `git diff d02f632 bdbef50 -- src` is empty (0 bytes): `src/` is as pass 6 verified it
**Verifier**: independent sub-agent (author ≠ verifier), seventh verification pass. Not the Verifier of an earlier pass, and not the author of the code, of the tests or of the spec edits
**Scope**: **limited, by the maintainer's decision** (recorded at `spec.md:69`: "closing the round with a Verifier limited to them"). This pass confirms that F8 closes G1 and G2 of the sixth pass and breaks nothing. It ran no broad mutation search; what it saw outside that scope is under "Residuals"

**Verdict**: ✅ PASS

**Result**: ✅ PASS - 67 of 67 criteria hold on the outcome the spec gives, FNT-66 and FNT-67 checked again as rewritten against the page read on Windows and in the Playwright image; the five mutants of G1 and G2 and the revert of each of F7's two code changes die, each on the assertion of its criterion; the Full gate green on Windows and the module green in the Playwright image; the Build is the orchestrator's (503 passed)

F8 adds two cases to `font-fallback-names.html` and one pair to each of the two tests of F7, and changes no code. `#unit-sep` holds U+001F, which Chromium writes as an escape of two hexadecimal digits, one of them a letter, followed by a space of the name's own: every misreading of the decoder that pass 6 found alive reads it wrong. `#nbsp-end` holds U+00A0 at the end of a name that Chromium writes unquoted: a trim of Unicode whitespace at the end loses it. Both were read on the page on both platforms, and both tests now fail under each mutant they target.

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
| Fix round 5 | `875eae4..d02f632` | The maintainer asked for a measurement across character classes and accepted FNT-66 and FNT-67 (`2eb1780`). `d02f632` is F7: the cases `#spaced-name`, `#nbsp-name` and `#tab-name` in `N`, two tests, and two changes to `J` (only CSS whitespace trimmed in `namesOf`; hexadecimal escapes decoded in `bare`) | `tasks.md`, "Fix of issue #20", F7 |
| 6 | `f5ec283..d02f632` | FAIL. 67 of 67 criteria; 46 mutants, 35 killed; the 24 of passes 3 to 5 and the two reverts of F7 dead; 11 of its own alive, 6 equivalent and 5 not (G1: HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY, HEX-ALL-WS; G2: TRIM-END-UNICODE). Past the three iterations: for the maintainer | `git show e5ffa21:.specs/features/font-fallback/validation.md` |
| Fix round 6 | `e5ffa21..bdbef50` | The maintainer chose one case more for each gap, on the same criteria, and a last Verifier limited to them (`spec.md:69`). `bdbef50` is F8: FNT-66 and FNT-67 rewritten, the cases `#nbsp-end` and `#unit-sep` in `N`, one pair more in each of F7's two tests; no change to `src/` | `tasks.md`, "Fix of issue #20", F8 |
| 7 | `e5ffa21..bdbef50`, in the round `f5ec283..bdbef50` | PASS: this report. **Limited in scope by the maintainer's decision**: FNT-66 and FNT-67 checked again, the five mutants of G1 and G2 and the two reverts of F7 run, the gate. 7 mutants, 7 killed | This file |

### What F8 changed, from git

- **`src/`**: nothing. `git diff d02f632 bdbef50 -- src` and `git diff e5ffa21 bdbef50 -- src` are both empty. Across the round, `src/` changes only in `J` (`git diff --stat f5ec283..bdbef50 -- src` is `font_widths.js | 22`), as pass 6 found it.
- **`N`**: two Faces (`N:91-101`: `"NBSP\a0"` and `"Unit\1f  Sep"`, each with a `src` that names no file), two rules (`N:157-163`), two elements (`N:177-178`), and the top comment (`N:28-32`).
- **`F`**: the test of FNT-66 gains `"NBSP "` / `#nbsp-end` (`F:588-594`); the test of FNT-67 gains `"Unit\u001f Sep"` / `#unit-sep` (`F:600-605`). The only lines `git diff e5ffa21 bdbef50 -- tests` removes are the old `families`/`on` tuples and the old one-pair equality of FNT-67; each old pair is still in the new expected list. Citations up to `F:586` do not move; those after `F:605` moved 3 down.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff; 58 tests in the module and 503 collected, as at `d02f632`.
- **`.specs/`**: `spec.md:69` (one sentence on the sixth pass and the maintainer's choice), `spec.md:145-146` (FNT-66, FNT-67); `tasks.md` (F8, and F7's **Commit** line now names `d02f632`).

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T12, F1 to F7 | ✅ Done | As passes 2 to 6 found them; `src/` unchanged since pass 6, and their tests pass here unchanged |
| F8 | ✅ Done | Each "Done when" checked. The Faces and computed `font-family` of both cases, read here on Windows and in the Playwright image, are as `N:28-32` says. Both tests pass on the code as it is (Full, here). HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY and HEX-ALL-WS each fail the test of FNT-67 (`F:602`), TRIM-END-UNICODE that of FNT-66 (`F:590`), in each run the other 57 pass. No other test changed. Full green; 58 and 503. The notes' "not read in the Playwright image" is closed by this pass |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome. `findings_on` and `sits_on` find an element through `inspect_element`, by its box; `of_family` (`F:253-257`) unpacks exactly one Finding for a family; `reported` (`F:189-204`) returns the `(selector, family)` of every Finding that names one of `families` or sits on one of `on`, so an assertion that it equals a list of pairs says "exactly these Findings, there, under these names".

**What was checked again, and what was carried.** FNT-66 and FNT-67 from scratch, against the rewritten criteria and the page as read on both platforms. Every other criterion is carried from pass 6 with this argument: `src/` is byte-identical to `d02f632`; the only test lines F8 touched are the two tests of FNT-66 and FNT-67, whose new expected lists contain the old ones; the module passed whole here on Windows and in the Playwright image, and the suite in the orchestrator's Build. Citations after `F:605` were moved 3 lines down and printed again at `bdbef50`.

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
| FNT-66 | One Finding on each of `#spaced-name`, `#nbsp-name`, `#nbsp-end`, with `family` `" Two  Spaces "`, `" NBSP"` and `"NBSP "` (JSON notation, `spec.md:69`), respectively | `F:588-594` `reported(client, NAMES, families=(" Two  Spaces ", " NBSP", "NBSP "), on=("#spaced-name", "#nbsp-name", "#nbsp-end")) == [("#spaced-name", " Two  Spaces "), ("#nbsp-name", " NBSP"), ("#nbsp-end", "NBSP ")]`. Exactly the three selectors and three names the criterion gives, in its order; a Finding under a trimmed name would still sit on its element and fail the equality (TRIM-END-UNICODE, F7-REVERT-TRIM, below) | ✅ PASS |
| FNT-67 | One Finding on each of `#tab-name` and `#unit-sep`, with `family` `"Tab\tName"` and `"Unit\u001f Sep"`, respectively | `F:600-605` `reported(client, NAMES, families=("Tab\tName", "Unit\u001f Sep"), on=("#tab-name", "#unit-sep")) == [("#tab-name", "Tab\tName"), ("#unit-sep", "Unit\u001f Sep")]`. The Python literals hold one U+0009, and one U+001F followed by one space. Exactly the selectors and names the criterion gives. Every misreading of the decoder pass 6 found alive fails it on `#unit-sep` (below) | ✅ PASS |

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
| FNT-61 | `textWidthPx` of `#turned` equals `round(box.w, 2)` | `F:611-613` `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of `#swift` equals `round(box.w, 2)` | `F:619-621` `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks`, the five Checks run | `F:138-142` the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` with `low-contrast-real` in one call; the others by their own slices (`D:449-452`) | ✅ PASS |
| FNT-34 | `isError: true` and the literal of the valid Checks | `D:340-344`, `D:351-355`, `D:362-366`, `D:374-378` the literal `in text`; `D:329` `result.is_error is True` | ✅ PASS |
| FNT-35 | `[]` with the other four Checks | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | The four `(selector, check)` pairs in order, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list | ✅ PASS |
| FNT-37 | The description names the Check and what it reports | `F:156-159` the sentence `in " ".join(tool.description.split())` | ✅ PASS |
| FNT-38 | Earlier tests pass with no change but the four literals | The orchestrator's Build on `bdbef50`: 503 passed. The round touches no test of an earlier slice (`git diff --stat f5ec283..bdbef50 -- tests` is `F` and `N` only) | ✅ PASS |
| FNT-39 | `isError: false`, one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

Carried from pass 6: none of these files is in `e5ffa21..bdbef50`.

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, registered by name | `C:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | `grep -rn playwright src/squint_mcp/checks/` finds nothing; `C:3` imports `squint_mcp.models` only | ✅ PASS |
| FNT-42 | Faces and widths read from the Capture, measured only on request | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`; `src/squint_mcp/tools/detect_visual_bugs.py:94`; `src/squint_mcp/capture.py:371-372` | ✅ PASS |
| FNT-43 | Equality, no tolerance; no threshold in `config` | `C:67` `if widths.own == widths.tail:`; `C:3` imports no `config`; `src/squint_mcp/config.py:83` and `:113`, names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG entry with the six things | `CHANGELOG.md:14`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`) | ✅ PASS |
| FNT-45 | README names `font-fallback`, five Checks | `README.md:46` | ✅ PASS |
| FNT-46 | Slice 9 `concluída` in the roadmap, table and section, with the link | `docs/ROADMAP.md:111` (table) and `docs/ROADMAP.md:163` (section) | ✅ PASS (file evidence) |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-47 | Each Finding of the first viewport has one in the second | `F:166-175` `len(desktop) == 2`, `desktop <= mobile` | ✅ PASS |
| FNT-48 | `Twice` on `#twice-normal`, `elements` 2 | `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2` | ✅ PASS |

**Status**: ✅ 67 of 67 criteria covered, each with the outcome the spec gives. No spec-precision gap.

### The names, read from the page

Read with a script outside the repository (Playwright, Chromium 153.0.8010.12) at `bdbef50`, on Windows and in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`; Docker Desktop was running). The two logs are identical but for line endings (`diff --strip-trailing-cr` is empty).

- **`document.fonts`**, as JSON, in order: `Ahem` `loaded`; then `Dual`, `DUAL`, `Acme, Inc`, `Vinyl 12\"`, `Back\\slash`, `\"Quoted\"`, `'Single'`, `" Two  Spaces "`, `" NBSP"`, `"Tab\tName"`, **`"NBSP "`**, **`"Unit\u001f Sep"`**, all `error`.
- **Computed `font-family`**, as JSON: `#nbsp-end` `"NBSP , Ahem"`, unquoted; `#unit-sep` `"\"Unit\\1f  Sep\", Ahem"`, that is `"Unit\1f  Sep", Ahem`: an escape of two lowercase digits, the space it consumes, then the name's own space. `#spaced-name`, `#nbsp-name` and `#tab-name` as pass 6 read them.

### The wording of F8

| # | Edit | Judgement |
| - | ---- | --------- |
| E1 | `spec.md:145`, FNT-66: adds `#nbsp-end`, of `font-family: "NBSP\a0", Ahem`; the name `"NBSP "`; "a U+00A0 at either end" | Accurate. CSS parses `\a0"` as U+00A0 with no space consumed, and the Face reads `NBSP` + U+00A0 on both platforms. The three expected names are now all in JSON notation, as `spec.md:69` declares, so the mixed notation pass 6 noted inside FNT-66 is gone |
| E2 | `spec.md:146`, FNT-67: "a control character, which Chromium serializes as a hexadecimal escape followed by one space"; `#unit-sep`, "whose name holds U+001F and then one space of its own"; "every hexadecimal digit of an escape is read in base 16, and the escape consumes the one space after it and no more" | Accurate. Both computed values are an escape and one space (`\9 `, `\1f `), and the U+001F name keeps its own space after the consumed one. The last clause is exactly what G1's four mutants break: base (HEX-DECIMAL), number of digits (HEX-ONE-DIGIT), letter digits (HEX-UPPER-ONLY, which `1f` exercises because Chromium writes it lowercase) and the space consumed (HEX-ALL-WS). "A control character" is true of U+0001 to U+001F and U+007F, which pass 6's probe showed Chromium escapes; U+0000 cannot reach a name (CSS turns it into U+FFFD) |
| E3 | `spec.md:69`, the sentence on the sixth pass | Accurate: the two pins were short as it says, and it records that the maintainer accepted one case for each and limited this Verifier to them |
| E4 | `N:28-32`, the comment: "The sixth validation pass read these three in the Playwright Linux image too, the same. F8, read on Windows ...: after them come `error` Faces named NBSP + U+00A0 and Unit + U+001F + one space + Sep; their computed `font-family` values are `NBSP` + U+00A0 + `, Ahem` (no quotes) and `"Unit\1f  Sep", Ahem`" | Accurate to the character, on Windows and, read by this pass, on Linux too. The comments on the two Faces (`N:91`, `N:96-97`) are accurate |
| E5 | `tasks.md`, F8 and F7's **Commit** line | Accurate; the claims of F8's notes were reproduced here |

---

## Discrimination Sensor

**Scope.** Only what the maintainer asked: the five mutants of G1 and G2 exactly as `git show e5ffa21:.specs/features/font-fallback/validation.md` gives them (its lines 249-253 and 269-286), and the revert of each of F7's two code changes, each run against the whole module. No new mutant was searched for.

**Isolation.** `git status --porcelain` was empty (0 bytes) before any sensor work and empty after it. Each run had its own copy of `src/squint_mcp`, copied whole without `__pycache__` into the session's scratch directory outside the repository; the mutation went into the copy only, line endings (CRLF) kept, and the runner stopped unless each `old` occurred exactly once. Each run was `uv run pytest tests/test_font_fallback.py -q -p no:cacheprovider -p squint_guard --tb=short -rf -s` from the repository, with `PYTHONPATH` set to the copy's root and the guard's directory and `PYTHONDONTWRITEBYTECODE=1`. The plugin `squint_guard` exits at configure, and again at unconfigure, unless `squint_mcp`, `squint_mcp.capture` and `squint_mcp.checks.font_fallback` are files of the copy and `capture._FONT_WIDTHS` equals the copy's `font_widths.js`. All 8 runs printed `GUARD OK <copy>` twice. The unmutated copy ran first: 58 passed. Three runs at a time, no `-x`. No `git stash`, no worktree, nothing under `src/` or `tests/` edited; each copy deleted after its run.

| # | `file:line` | Mutation (as pass 6 gives it) | Tests that failed | Result |
| - | ----------- | ----------------------------- | ----------------- | ------ |
| HEX-ONE-DIGIT | `J:43` | `[0-9a-f]{1,6}` → `[0-9a-f]{1}` | FNT-67, alone (1 failed, 57 passed) | ✅ **Killed** (alive in pass 6): `F:602` `[('#tab-name', 'Tab\tName')] == [('#tab-name'...nit\x1f Sep')]`, right contains `('#unit-sep', 'Unit\x1f Sep')` |
| HEX-DECIMAL | `J:44` | `parseInt(hex, 16)` → `parseInt(hex, 10)` | FNT-67, alone | ✅ **Killed** (alive in pass 6): `F:602`, the same: `#unit-sep` missing |
| HEX-UPPER-ONLY | `J:43` | `[0-9a-f]` → `[0-9A-F]`, flags `gis` → `gs` | FNT-67, alone | ✅ **Killed** (alive in pass 6): `F:602`, the same: `#unit-sep` missing |
| HEX-ALL-WS | `J:43` | `[ \t\n\r\f]?` → `[ \t\n\r\f]*` | FNT-67, alone | ✅ **Killed** (alive in pass 6): `F:602`, the same: `#unit-sep` missing |
| TRIM-END-UNICODE | `J:12` | `name.replace(/^[ \t\n\r\f]+/g, "").trimEnd();` | FNT-66, alone | ✅ **Killed** (alive in pass 6): `F:590` `[('#spaced-na..., '\xa0NBSP')] == [('#spaced-na..., 'NBSP\xa0')]`, right contains `('#nbsp-end', 'NBSP\xa0')` |
| F7-REVERT-TRIM | `J:12` | `name.trim();` (F7's first change taken back) | FNT-66, alone | ✅ Killed: `F:590` `[('#spaced-na...wo  Spaces ')] == [...]`, right contains 2 more items, first `('#nbsp-name', '\xa0NBSP')` |
| F7-REVERT-BARE | `J:42-45` | the pre-F7 `bare`: `name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");` | FNT-67, alone | ✅ Killed: `F:602` `[] == [('#tab-name'...nit\x1f Sep')]`, right contains 2 more items, first `('#tab-name', 'Tab\tName')` |

**What was carried, not re-run.** The 35 mutants pass 6 found killed (the 24 of passes 3 to 5, its own 9, and the two reverts, re-run here) still die by argument: `src/` is the same, and the two tests F8 changed now assert a superset of what they asserted, on elements that did not exist before, so no mutant's output can newly equal them. The 6 equivalents of pass 6 are untouched by F8 and stay equivalent.

**Sensor depth**: limited, by the maintainer's decision: the 5 mutants of G1 and G2 and the 2 reverts of F7.
**Count**: 7 injected; 7 killed; 0 survived. ✅

---

## Gate Check

Run here on `bdbef50` with a clean tree.

- **Full** (`uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py`, the last with `-p no:cacheprovider`): pyright 0 errors, 0 warnings, 0 informations; ruff check All checks passed; ruff format 121 files already formatted; **58 passed** in 204.99s; exit 0
- **Collected**: `uv run pytest --collect-only -q`: 503
- **Build**: not re-run here, by instruction. The orchestrator's run on `bdbef50` on Windows: **503 passed in 22m30s**
- **Linux**: the Linux command of `tasks.md:36` run here in the Playwright image from `bdbef50`, after the name reads: **58 passed** in 201.61s; exit 0
- **Test count before the round**: 53 in the module, 498 in the suite (CI run 38752135720 on `f5ec283`). **After**: 58 and 503. F8 adds no test function; it extends two
- **Skipped**: none. **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened; the two changed tests assert strictly more than before
- **CI**: the branch is not on the remote, so no CI run of it exists

---

## Evidence for the boxes of spec.md

For the maintainer's closing step. No box is ticked here.

| Box | Evidence now | Where |
| --- | ------------ | ----- |
| Goal 1 (`spec.md:13`): every family of the bug fixture reported once, nothing on the clean fixture | Yes | FNT-02 (`F:51-59`) and FNT-16 (`F:182-186`), green in the Full here and in the Playwright image at `bdbef50`, and in the orchestrator's Build |
| Goal 2 (`spec.md:14`): a Finding names the family and counts the elements | Yes | FNT-27 (`F:108-134`), the literal with `family` and `elements`; green here |
| Goal 3 (`spec.md:15`): every outcome the same on Windows and on Linux | Yes, for `bdbef50`'s module | 58 passed on Windows and 58 in the Playwright image, this pass; the Faces and computed names of `N` read identical on both. The CI's Linux has not run the branch |
| Goal 4 (`spec.md:16`): slice 9 marked done in the roadmap once verification passes | The mark exists, and this round's verification now passes | `docs/ROADMAP.md:111` and `:163`, set by `79a929a` after pass 2. Whether to keep it as it is, is the maintainer's to confirm |
| Success Criterion 1 (`spec.md:331`): all 67 requirements verified, FNT-40 to FNT-46 from file evidence | Yes | "Spec-Anchored Acceptance Criteria": 67 of 67; FNT-66 and FNT-67 checked again here, the rest carried as stated there |
| Success Criterion 2 (`spec.md:332`): typecheck, lint, format check and the whole suite pass | Yes | The orchestrator's Build on `bdbef50`: 503 passed in 22m30s; the three static checks run again here, green. On the CI: 38752135720 on `f5ec283`, not on the branch |
| Success Criterion 3 (`spec.md:333`): the first CI Linux run passes the slice's tests with no assertion changed for it | Yes for the 53 tests before the round; not yet for the five of FNT-63 to FNT-67 | CI run 38447799140 on `61c4378` (success). The five tests have had no CI run; they pass in the Playwright image here |
| Success Criterion 4 (`spec.md:334`): no mutant a report or a task names alive, nor any of the code the last fix round changed | Yes, within this pass's scope | The five of G1 and G2 and the two reverts of F7 die here (Sensor); the other named mutants die by the argument there, `src/` unchanged since pass 6. The six equivalents of pass 6 remain equivalent on every input Chromium 153 writes |

---

## Gaps

None.

---

## Residuals (not gaps of this round)

- **R1. Slice 10 changed the Capture after the second pass** (`capture.py`, `collect_elements.js`). As passes 3 to 6 found: it does not reach the font path, the tests and the Build hold it, and it was not verified mutant by mutant.
- **R2. Stale words outside F8's diff**: `design.md:220` still says "FNT-67 pins a tab" (it now pins U+001F too); the traceability rows `spec.md:322-323` name F7 only, not F8; `N:23` still says "the last three Faces", which `N:29` then qualifies with "after them come". Cosmetic.
- **R3. Notation in `tasks.md`'s F8 notes**: `"NBSP "` is labelled JSON notation and holds a raw U+00A0, invisible on the page; the spec writes `"NBSP "`. Cosmetic.
- **R4. `bare` departs from CSS Syntax on input Chromium does not write** (U+0000, surrogates, values above 0x10FFFF, a trailing backslash, an escaped newline), as pass 6 measured; `design.md:112` does not say it. Unchanged.
- **R5. `CHANGELOG.md:24`** is a `### Fixed` entry for a Check that is itself unreleased, followed by a blank line inside the list (pass 6's R4). Unchanged.
- **R6. The Linux gate is not recorded under T10** for this round. It was run here on `bdbef50` (58 passed).
- **Not verified here**: a CI run of the branch; the Build (cited from the orchestrator); any mutant beyond the seven above, by the maintainer's decision on scope.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-65 | Verified again at `d02f632` (pass 6) | ✅ Verified, carried to `bdbef50` (`src/` unchanged, module and suite green) |
| FNT-66, FNT-67 | Verified as written at `d02f632`; pins short (G1, G2) | ✅ Verified as rewritten at `bdbef50` |

The spec is not edited by the Verifier.

---

## Summary

**Overall**: ✅ Ready (pass limited in scope by the maintainer)

**Spec-anchored check**: 67 of 67 criteria matched the spec outcome; 0 spec-precision gaps
**Sensor**: 7 of 7 killed: HEX-ONE-DIGIT, HEX-DECIMAL, HEX-UPPER-ONLY, HEX-ALL-WS on `F:602` (`#unit-sep`); TRIM-END-UNICODE on `F:590` (`#nbsp-end`); F7-REVERT-TRIM on `F:590`; F7-REVERT-BARE on `F:602`
**Gate**: Full green on Windows (58 passed, 503 collected); the module green in the Playwright image (58 passed); Build by the orchestrator (503 passed)

**What works**: F8 closes G1 and G2 with no change to `src/`: each mutant pass 6 found alive now fails the test of its criterion, and only that test. The two new names read the same on Windows and on Linux, and the criteria and fixture comment say them accurately.

**Issues found**: none in scope. Residuals R1 to R6.

**Next steps**: for the maintainer: tick the boxes, record the Linux run under T10, push the branch so the CI runs the five tests of FNT-63 to FNT-67 on `ubuntu-latest`, and close issue #20 with the pull request.
