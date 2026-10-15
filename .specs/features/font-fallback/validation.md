# font-fallback Validation

**Date**: 2026-10-15
**Spec**: `.specs/features/font-fallback/spec.md` (FNT-01 to FNT-63, as it is at `c7a4729`)
**Diff range**: `f5ec283..c7a4729` (3 commits, branch `fix/font-name-backslash`, base `main`). `4015689` is a lessons commit outside the feature; `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4. The round changes one line of `src/` (`src/squint_mcp/js/font_widths.js:46`, with a comment above it)
**Verifier**: independent sub-agent (author ≠ verifier), third verification pass. Not the Verifier of the first or second pass, and not the author of the code, of the tests or of the spec edits

**Verdict**: ❌ FAIL

**Result**: ❌ FAIL - one mutant of the code the last fix round changed is alive

The fix does what issue #20 asks and FNT-63 holds it: a Failed family whose name holds a backslash gets its Finding, on Windows and in the Playwright image, and the residual N60-unescape-quotes-only of the second report now dies on the test of FNT-63, as F4 claims. The 63 criteria are each held by an assertion on the value the spec gives, and the gate is green.

The pass fails on one thing, the fourth Success Criterion: "The discrimination sensor leaves alive none of the mutants ... nor any of the code the last fix round changed". The changed line used to take two things off the name of a Face, its quotes and its escapes (`bare`). The fix stops both; FNT-63 pins only the escapes. **FACE-UNQUOTE-ONLY**, the changed line with the quotes still taken off, passes all 54 tests, and it changes what the tool returns: a family whose name starts and ends with a quotation mark (`"Quoted"`, `'Single'`) gets its Finding with the code and loses it with the mutant, as it did before the fix. FNT-63's own sentence says "with no quote and no escape taken off", and the issue lists that case as "not run". One small fix task closes it (Fix 1 below).

Abbreviations: `F` = `tests/test_font_fallback.py`, `D` = `tests/test_detect_visual_bugs.py`, `C` = `src/squint_mcp/checks/font_fallback.py`, `J` = `src/squint_mcp/js/font_widths.js`, `N` = `tests/fixtures/font-fallback-names.html`.

---

## Passes

| Pass | On | Outcome | Where it is kept |
| ---- | -- | ------- | ---------------- |
| 1 | `0b9ae25..ab1dbab` | FAIL. 53 of 53 criteria matched, the gate green, the 11 mutants a task names dead; 10 mutants of its own alive (C16b, C5, C2, S1b, S1a, S2b, S7, S8, CFG-dir, CFG-tr) and 4 argued equivalent | `git show 895bd56:.specs/features/font-fallback/validation.md` |
| Fix round 1 | `ab1dbab..6cd7076` | F1 to F3: FNT-55 to FNT-62, two fixtures and two cases more; no change to `src/` | `tasks.md`, "Fixes of the first validation pass" |
| 2 | `0b9ae25..6cd7076` | PASS. 61 of 61 criteria, 33 of 45 mutants killed, 12 alive (4 equivalent, 8 residual); found I-1, which became issue #20 | `git show 79a929a:.specs/features/font-fallback/validation.md` (with the row of FNT-46 that T12 added; `5caa610` holds it as the Verifier wrote it). No later commit touches the file before this report |
| Fix round 2 | `f5ec283..c7a4729` | `70e20fe` adds FNT-63 and plans F4; `c7a4729` is F4: the case `#slash` in `N`, its test, and `J:46` takes the name of a Face as `document.fonts` gives it | `tasks.md`, "Fix of issue #20" |
| 3 | `f5ec283..c7a4729` | FAIL: this report. 63 of 63 criteria; 8 mutants (the revert among them), 7 killed; FACE-UNQUOTE-ONLY alive on the changed line | This file |

### What the round changed, from git

- **`src/`**: `git diff --stat f5ec283..c7a4729 -- src` is `font_widths.js | 3 ++-`. `J:46` goes from `family: bare(face.family),` to `family: face.family,`, and `J:44` is a new comment. Every line of `J` after `J:43` moves one down; the citations below are at HEAD.
- **`tests/`**: `N` adds 14 lines and removes 1, the last line of the comment of the Faces, rewritten (`git diff --numstat`: `14 1`), `F` adds 9 (`F:560-566`, after the test of FNT-60). No line of an existing test is in the diff: the citations of `F` up to `F:557` do not move, those after it move 9 down.
- **No test weakened, skipped or deleted**: no `skip` and no `xfail` in the diff; 54 tests in the module against 53, 499 collected against 498 (the CI run on `f5ec283`, 38752135720: `498 passed`).
- **`.specs/`**: `spec.md` (FNT-63, one sentence of the Assumptions, the traceability row, "63" in the coverage line and in the first Success Criterion), `design.md:110`, `tasks.md` (F4).
- **Not the round, and still under the Check.** Slice 10 (`extract-tokens`, merged as #22 before `f5ec283`) changed `src/squint_mcp/capture.py` and `src/squint_mcp/js/collect_elements.js` after the second pass. Read here: `detect_visual_bugs` never passes the new `descendants` (only `src/squint_mcp/tools/extract_tokens.py:65` does), and the new colour conversion uses an `OffscreenCanvas` that is not in the document (`src/squint_mcp/js/srgb_colors.js`). Nothing of it reaches the Faces or the widths, and the 54 tests pass on it. The brief's "the code outside the one changed line did not change since the second pass" is true of `J` and `C`, not of the Capture.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 to T12, F1 to F3 | ✅ Done | As the second pass found them; none is in this diff |
| F4 | ✅ Done | Each "Done when" checked: the Faces and the computed `font-family` of `#slash` read here (below); the test fails on the code before the fix on `[] == [('#slash', 'Back\\slash')]` (REVERT, below); N60-unescape-quotes-only fails the test of FNT-63 on the same assertion; the tests of FNT-58 to FNT-60 pass unchanged; Full green; 54 in the module, 499 collected |

---

## Spec-Anchored Acceptance Criteria

Evidence-or-zero: each row names the line and the assertion that hold the outcome. `findings_on` and `sits_on` find an element through `inspect_element`, by its box; `of_family` unpacks exactly one Finding for a family; `reported` (`F:189-204`) returns the `(selector, family)` of every Finding that names one of `families` or sits on one of `on`, so an assertion that it equals one pair says "exactly one Finding, there, under that name".

**What was checked again in full.** FNT-63 from scratch. FNT-58, FNT-59 and FNT-60, the neighbours of `#slash` in the same fixture, against the fixture and their sentence. Every row whose outcome rests on matching a First family to the name of a Face, which is what the changed line feeds: FNT-01, FNT-02, FNT-05, FNT-06, FNT-07, FNT-29; each was read again at HEAD and each dies under at least one mutant of the matching (CASE-EXACT, FACE-LOWER, FIRST-NOT-BARE). The other rows are carried forward from the second pass with their citations moved where the diff moved them (`F` after `F:557`, `J` after `J:43`, and the lines slice 10 moved in `capture.py`, `config.py`, `CHANGELOG.md` and `README.md`, each read again at HEAD); their tests did not change.

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
| FNT-63 | One Finding for `#slash`, with `evidence.measured.family` equal to `Back\slash` | `F:563-566` `await reported(client, NAMES, families=("Back\\slash",), on=("#slash",)) == [("#slash", "Back\\slash")]`. The Python literal `"Back\\slash"` is the string `Back\slash`, one backslash, the name the spec gives. The Findings that name the family or sit on `#slash` are exactly one, on `#slash`, under that name: a Finding under `Backslash` would sit on `#slash` and fail the equality | ✅ PASS |

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
| FNT-61 | `textWidthPx` of `#turned` equals `round(box.w, 2)` | `F:572-574` `family(finding) == "Turned Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |
| FNT-62 | `textWidthPx` of `#swift` equals `round(box.w, 2)` | `F:580-582` `family(finding) == "Swift Brand"`, `width(finding) == round(finding["box"]["w"], 2)` | ✅ PASS |

### P1: With the other Checks

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-33 | Without `checks`, the five Checks run | `F:138-142` the pairs `== [("#heading", "font-fallback"), ("#icon", "font-fallback")]`; `F:493-500` with `low-contrast-real` in one call; the others by their own slices (`D:449-452`) | ✅ PASS |
| FNT-34 | `isError: true` and the literal of the valid Checks | `D:340-344`, `D:351-355`, `D:362-366`, `D:374-378` the literal `in text`; `D:329` `result.is_error is True` | ✅ PASS |
| FNT-35 | `[]` with the other four Checks | `F:146-147` `(await detect(client, BUG, checks=others))["findings"] == []` | ✅ PASS |
| FNT-36 | The four `(selector, check)` pairs in order, all `minor` | `F:494-500` `{severity} == {"minor"}` and the whole list. The note of the second pass (R2: O2 is told apart by `D:449`) stands; `src/squint_mcp/tools/detect_visual_bugs.py:118-127` is not in this diff | ✅ PASS |
| FNT-37 | The description names the Check and what it reports | `F:156-159` the sentence `in " ".join(tool.description.split())` | ✅ PASS |
| FNT-38 | Earlier tests pass with no change but the four literals | The Build on `c7a4729`, the orchestrator's run: 499 passed (log not read here; see "Gate Check"). This diff touches no test of an earlier slice. The CI on `f5ec283` passed 498 | ✅ PASS |
| FNT-39 | `isError: false`, one Finding, `elements` 1000 | `F:505-508` `result.is_error is False`, `(finding,) = ...`, `elements(finding) == 1000` | ✅ PASS |

### P2: Check contract, Capture and documents (file evidence)

| Criterion | Spec-defined outcome | `file:line` | Result |
| --------- | -------------------- | ----------- | ------ |
| FNT-40 | One module under `checks/`, registered by name | `src/squint_mcp/checks/font_fallback.py:43` `def check(capture: Capture) -> list[Finding]`; `src/squint_mcp/checks/__init__.py:25` `"font-fallback": font_fallback.check,` | ✅ PASS |
| FNT-41 | No module under `checks/` imports `playwright` | A search of `src/squint_mcp/checks/` for `playwright` finds nothing; `C:3` imports `squint_mcp.models` only | ✅ PASS |
| FNT-42 | Faces and widths read from the Capture, measured only on request | Reads: `C:44`, `C:49-51`, `C:55`. On request: `src/squint_mcp/checks/__init__.py:34` `FONT_CHECKS`; `src/squint_mcp/tools/detect_visual_bugs.py:94` `fonts = not FONT_CHECKS.isdisjoint(names)`, passed at `:103`; `src/squint_mcp/capture.py:371-375` `faces = None` unless `fonts`; `src/squint_mcp/tools/inspect_element.py:53-55` does not ask | ✅ PASS |
| FNT-43 | Equality, no tolerance; no threshold in `config` | `C:67` `if widths.own == widths.tail:`; `C:3` imports no `config`; `src/squint_mcp/config.py:83` (`font-style`) and `:113-119` (`TEXT_SHAPING_PROPERTIES`), names and no number | ✅ PASS |
| FNT-44 | The CHANGELOG entry with the six things | `CHANGELOG.md:14`, under `## [Unreleased]` (`:7`) and `### Added` (`:9`) | ✅ PASS |
| FNT-45 | README names `font-fallback`, five Checks | `README.md:46` "`detect_visual_bugs` runs five Checks: ... `font-fallback`" | ✅ PASS |
| FNT-46 | Slice 9 `concluída` in the roadmap, table and section, with the link | `docs/ROADMAP.md:111` and `docs/ROADMAP.md:163`, from T12 after the second pass (`79a929a`). Whether it stays so under this FAIL is the maintainer's: the slice was merged as #21 and this is the round of an issue | ✅ PASS (file evidence) |

### Edge cases

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| FNT-47 | Each Finding of the first viewport has one in the second | `F:166-175` `len(desktop) == 2`, `desktop <= mobile` | ✅ PASS |
| FNT-48 | `Twice` on `#twice-normal`, `elements` 2 | `F:337-341` `finding == await sits_on(..., "#twice-normal")`, `elements(finding) == 2` | ✅ PASS |

**Status**: ✅ 63 of 63 criteria covered, each with the outcome the spec gives. No spec-precision gap: FNT-63's outcome is exact. Its closing clause states a rule wider than its case (see "FNT-63 and its clause").

### The state of `#slash`, read from the page

Read with a script outside the repository (Playwright, Chromium 153.0.8010.12, Windows), at HEAD:

- `document.fonts` of `N`: `Ahem` `loaded`, then `Dual`, `DUAL`, `Acme, Inc`, `Vinyl 12"`, `Back\slash`, all `error`, in this order. `Back\slash` has one backslash and no quotes, as the comment of the fixture says (`N:17-19`).
- The computed `font-family` of `#slash` is `"Back\\slash", Ahem` (two backslashes), as `N:42-43` and FNT-63 say. Those of `#dual-normal`, `#comma` and `#inch` are as the second pass read them.
- The tool at HEAD returns `(#dual-normal, Dual, 2)`, `(#comma, Acme, Inc, 1)`, `(#inch, Vinyl 12", 1)`, `(#slash, Back\slash, 1)`, each `textWidthPx` 200. With the fix reverted it returns the first three only.
- **Linux**: the module passes in the Playwright image (54 passed, below). The Finding of `#slash` names its family as the Face has it, so the Face is `error` under `Back\slash` there too; the names were not read there directly.

### FNT-63 and its clause

FNT-63's outcome is one Finding with `family` `Back\slash`, and the test holds it exactly. Its sentence ends with the rule the outcome stands for: "the name of a Face is taken as `document.fonts` gives it, with no quote and no escape taken off". The case pins the escape half. No case pins the quote half: no fixture declares a family whose name itself starts and ends with a quotation mark. That is the surviving mutant below, not a vague outcome, so it is counted under the sensor and not as a spec-precision gap.

---

## The spec and design edits of the round

| # | Edit | Judgement |
| - | ---- | --------- |
| E1 | `spec.md:69`: "On 2026-10-15 the maintainer accepted FNT-63, for issue #20 (I-1 of the second pass) ..." | Accurate. It matches the issue and `tasks.md`, "Fix of issue #20" |
| E2 | `spec.md:142`, FNT-63 | Accurate on every fact it states, each read from the page: the computed value with two backslashes, the declared family with one, the `src` that names no file (`N:44-47`), and the rule of the code (`J:44-46`). It does not contradict FNT-60 (a name a computed value escapes, matched after `bare`) or the Assumption "The name a family is reported under" ("A Face gives the name without quotes (measured)", which it makes sharper). Its last clause promises more than its case holds: Fix 1 |
| E3 | `spec.md:315` and `:317`, `:323`: the row of FNT-63, "63" twice | Accurate: 63 rows, FNT-01 to FNT-63, each with a task |
| E4 | `design.md:110`: `faces` gives `family` "as `document.fonts` gives it, which is without quotes and without escapes; FNT-63, issue #20" | Accurate in the sense the Assumptions use: no CSS quoting and no escapes. Read to the letter it is loose: a name that holds quotation marks keeps them (`"Quoted"` is given as `"Quoted"`, read here). "Exactly as `document.fonts` gives it" would say it without the reading. Cosmetic. `design.md:111` ("`family` is the First family without quotes") was not edited and also leaves out the escapes; cosmetic, not the round's |
| E5 | The comment of `N:13-19` and `N:42-43` | Accurate, each read on Windows, and says it was read on Windows only. The first sentence still says "the other four are `error`", true of the four it names; the new one is named after it |

---

## Discrimination Sensor

**Isolation.** `git status --porcelain` was empty before any sensor work and empty after it. Each copy was `src/squint_mcp` copied whole, bytes as they are (CRLF kept), to the scratch directory outside the repository; the mutation was applied to the copy only, each `old` checked to occur exactly once. Each run was `uv run pytest tests/test_font_fallback.py -q -p no:cacheprovider -p squint_guard --tb=short -rf` from the repository with `PYTHONPATH` on the copy. The plugin `squint_guard` aborted the session unless `squint_mcp`, `squint_mcp.capture` and `squint_mcp.checks.font_fallback` were files of the copy and the script the Capture runs (`capture._FONT_WIDTHS`) was the copy's `font_widths.js`, and printed `GUARD OK` at the end; every run printed it. (The guard caught one misdirected setup during the probes, a path the shell had mangled; that run was discarded and redone.) The unmutated copy passed first: 54 passed. One pytest process at a time, the whole module each time, no `-x`. No `git stash`, no worktree, nothing under `src/` or `tests/` edited. The copies were deleted after the last run.

"Shown" means the tool, called through the in-memory client from the copy on a page outside the repository (`probe.html`: five families declared with a `src` that names no file, `"Quoted"` written `'"Quoted"'`, `'Single'` written `"'Single'"`, `Back\slash`, `Two\\Slashes`, `Case\Slash` asked for as `case\slash`, each on a block of ten Ahem glyphs), returned something else with the mutant than without.

| # | `file:line` | Mutation | Test that failed | Result |
| - | ----------- | -------- | ---------------- | ------ |
| REVERT | `J:46` | `family: bare(face.family),`: the fix taken back | `F:560` (FNT-63), alone | ✅ Killed: `[] == [('#slash', 'Back\\slash')]`. Shown: the probe also loses `#quoted`, `#single`, `#two` and `#case` |
| N60-unescape-quotes-only | `J:41` | Exactly the row of the second report: `.replace(/\\(.)/gs, "$1")` becomes `.replace(/\\"/g, '"')` | `F:560` (FNT-63), alone | ✅ Killed: `[] == [('#slash', 'Back\\slash')]`. FNT-59 and FNT-60 pass. The second report's residual, tied to I-1, is closed |
| FACE-UNESCAPE-ONLY | `J:46` | Half of the revert: `face.family.replace(/\\(.)/gs, "$1")`, escapes taken off the Face name | `F:560` (FNT-63), alone | ✅ Killed: `[] == [('#slash', 'Back\\slash')]` |
| **FACE-UNQUOTE-ONLY** | `J:46` | The other half: `face.family.replace(/^(["'])(.*)\1$/s, "$2")`, the quotes of a Face name taken off | none | ❌ **Survived (54 passed).** Shown: with the code the probe returns `(#quoted, "Quoted", 1, 200)` and `(#single, 'Single', 1, 200)`; with the mutant neither, and the three names with backslashes stay. This is half of I-1 come back, on the line the round changed |
| FACE-LOWER | `J:46` | `face.family.toLowerCase()` | 33 tests, the first `F:37` (FNT-01) | ✅ Killed: `[] == ['#heading']`; FNT-63 on `[('#slash', 'back\\slash')] == [('#slash', 'Back\\slash')]` |
| CASE-EXACT | `J:53`, `J:102` | Case folding taken out of the matching, on both sides | `F:267` (FNT-15), `F:297` (FNT-06), `F:328` (FNT-29) | ✅ Killed: `('#quoted', 'Missing Brand', 1) != ('#lower', 'Missing Brand', 2)`; FNT-06 and FNT-29 find no Finding on `#lower` |
| FIRST-NOT-BARE | `J:101` | `const family = names[0];`: the First family keeps its quotes and escapes | 26 tests, among them FNT-02, FNT-06, FNT-59, FNT-60, FNT-63 | ✅ Killed: `[] == [('#slash', 'Back\\slash')]`, `[] == [('#comma', 'Acme, Inc')]`, and the others |
| NAMESOF-DROP-BACKSLASH | `J:17` | `namesOf` drops the backslash of an escape and keeps the character after it | `F:560` (FNT-63), alone | ✅ Killed: `[] == [('#slash', 'Back\\slash')]`. FNT-60 passes under it (`"Vinyl 12""` still unquotes to `Vinyl 12"`): FNT-63 is the only test that holds the escape reading of a computed value whole |

The rows, exactly, as `(file under src/squint_mcp, old, new)`:

```
REVERT                  js/font_widths.js
         old:     family: face.family,
         new:     family: bare(face.family),

N60-unescape-quotes-only  js/font_widths.js
         old:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");
         new:     name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\"/g, '"');

FACE-UNQUOTE-ONLY       js/font_widths.js                    (alive)
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
```

**Why FACE-UNQUOTE-ONLY fails the pass.** The Assumption "When the discrimination sensor is satisfied" asks that "the mutants that a validation report or a task names die, with those of the code the last fix round changed", and the fourth Success Criterion says the same. The last fix round changed `J:46`, and this mutant is of `J:46`: it is not one found "later" in code no round touched, which the Assumption lets stand as a residual. It is not equivalent: the probe shows a family the code reports and the mutant does not, and the code before the fix did not either. The test of FNT-63 holds the case the criterion names; it cannot hold the other half of the rule its sentence states, because no fixture has a name that starts and ends with a quotation mark.

**The second report's residuals**: N60-unescape-quotes-only is killed (above). The other seven (R7 there, now issue #28) were not run again: out of scope.

**Sensor depth**: the one mutant a report names on this code; the revert; six of this pass on the changed line and on the matching of a First family to a Face (quotes, escapes, case).
**Count**: 8 injected, the revert among them; 7 killed, 1 alive (FACE-UNQUOTE-ONLY), 0 equivalent.

---

## Gate Check

Run here on `c7a4729` with a clean tree, before the sensor.

- **Gate command**: Full, `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py`, then `uv run pytest --collect-only -q`
- **pyright**: 0 errors, 0 warnings, 0 informations
- **ruff check**: All checks passed
- **ruff format --check**: 121 files already formatted
- **The module of the slice**: 54 passed, 0 failed, 0 skipped, in 169.84s
- **Collected**: 499
- **Linux**: run here as the Linux row of the gate table gives it, in `mcr.microsoft.com/playwright/python:v1.63.0-noble` (`sha256:72bd171a9ffc2b4b59532aaa6210e21014d07093120dc25528870c0b840da1f0`; not the id the second pass recorded, the tag was pulled again since), from `c7a4729`: 54 passed in 151.02s
- **Test count before the round**: 53 in the module, 498 in the suite (the CI run on `f5ec283`); **after**: 54 and 499; **delta** +1, the test of FNT-63
- **Skipped**: none. **Failures**: none
- **Test integrity**: no test deleted, skipped or weakened; the diff of `tests/` removes one line, of the comment of `N`
- **The Build** (the whole suite): not run here. It is the orchestrator's run on `c7a4729`, Windows: 499 passed in 21m38s, reported in the brief; its log was not read here. One test was added and none of an earlier slice is in the diff

---

## Evidence for the boxes of spec.md

For the maintainer's closing step. No box is ticked here.

| Box | Evidence now | Where |
| --- | ------------ | ----- |
| Goal 1 (`spec.md:13`): every family of the bug fixture reported once, nothing on the clean fixture | Yes | FNT-02 (`F:51-59`) and FNT-16 (`F:182-186`), green in the Full gate of this pass on Windows and in the Playwright image |
| Goal 2 (`spec.md:14`): a Finding names the family and counts the elements | Yes | FNT-27 (`F:108-134`), the literal with `family` and `elements`; green here |
| Goal 3 (`spec.md:15`): every outcome the same on Windows and on Linux | Yes for `c7a4729`'s module | 54 passed on Windows and 54 passed in the Playwright image, this pass. The CI's Linux has not run `c7a4729` (the branch is not on the remote); it ran the 53 tests before it (38752135720 on `f5ec283`) |
| Goal 4 (`spec.md:16`): slice 9 marked done in the roadmap once verification passes | Yes, from the second pass | `docs/ROADMAP.md:111` and `:163`, `79a929a`, after the PASS of pass 2. This pass is a FAIL of the round of issue #20; whether the line stands is the maintainer's |
| Success Criterion 1 (`spec.md:323`): all 63 requirements verified, FNT-40 to FNT-46 from file evidence | Yes | "Spec-Anchored Acceptance Criteria" of this report: 63 of 63 |
| Success Criterion 2 (`spec.md:324`): typecheck, lint, format check and the whole suite pass | Yes, by the orchestrator's Build | The Build on `c7a4729` (499 passed, 21m38s), reported in the brief and not read here; pyright, ruff check and ruff format run again here, green. On the CI: 38752135720 on `f5ec283` (498 passed), not on `c7a4729` |
| Success Criterion 3 (`spec.md:325`): the first run on the CI's Linux passes the tests of this slice with no assertion changed for it | Yes, for the 53 tests before this round | CI run 38447799140 on `61c4378`, the first run of #21, 2026-10-13: 421 passed on `ubuntu-latest`. `git diff 6cd7076 61c4378 -- src tests` is empty, so it ran the tests the second pass verified. The test of FNT-63 has had no CI run yet |
| Success Criterion 4 (`spec.md:326`): no mutant a report or a task names alive, nor any of the code the last fix round changed | **No** | FACE-UNQUOTE-ONLY, on `J:46`, is alive: "Discrimination Sensor". The mutant the second report names (N60-unescape-quotes-only) and the task names (F4) dies |

---

## Fix Plans

### Fix 1: the quote half of FNT-63 has no case

- **Root cause**: no fixture declares a family whose name itself starts and ends with a quotation mark, so the line that stopped taking the quotes off a Face name is held from one side only. Measured on the page of this pass: the family declared as `'"Quoted"'` is given by `document.fonts` as `"Quoted"` (the quotation marks are part of the name), the computed `font-family` of an element that asks for it is `"\"Quoted\"", Ahem`, `bare` reads its First family as `"Quoted"`, and the tool reports `(#quoted, "Quoted", 1, 200)`. With FACE-UNQUOTE-ONLY, and with the code before the fix, it reports nothing.
- **Fix task** (F5): a case in `tests/fixtures/font-fallback-names.html`, beside `#slash`: an `@font-face` of `font-family: '"Quoted"'` with a `src` that names no file, and an element `#quoted` of `font-family: '"Quoted"', Ahem` and ten glyphs; its test, `reported(client, NAMES, families=('"Quoted"',), on=("#quoted",)) == [("#quoted", '"Quoted"')]`, seen red under FACE-UNQUOTE-ONLY in a scratch copy and green on the code. No change to `src/`. The spec needs the case named, either as a criterion of its own (FNT-64) or in FNT-63's parenthesis: the maintainer's choice. Read the Face's name on Linux too.
- **Done when**: FACE-UNQUOTE-ONLY dies on the new test; REVERT, FACE-UNESCAPE-ONLY and N60-unescape-quotes-only still die; the Full gate passes; 55 in the module.
- **Priority**: Minor. A family name that starts and ends with a quotation mark is rarer than one with a backslash, and the fault would be a missing Finding. It fails this pass only because it is a mutant of the line the round changed.

---

## Residuals (not gaps of this round)

- **R1. Slice 10 changed the Capture after the second pass** (`capture.py`, `collect_elements.js`). Read here and found not to reach the font path; held by the 54 tests and the Build. Not verified mutant by mutant.
- **R2. `design.md:110` and `J:44` say "without quotes"** for a name that can hold quotation marks; and `design.md:111` leaves out the escapes. Cosmetic (E4).
- **R3. The Faces of `N` were not read on Linux** directly; the test of FNT-63 passing in the Playwright image implies the name and the status.
- **The residuals of the second report** (R1 to R9 there) stand as it lists them; its R7 is issue #28. Its I-1 is closed by this round, but for Fix 1.
- **Not verified here**: the Build's log (the orchestrator's); a CI run of `c7a4729`.

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FNT-01 to FNT-62 | Implemented (verified by pass 2) | ✅ Verified again at `c7a4729` |
| FNT-63 | Implemented | ✅ Verified for its case (`#slash`); the quote half of its closing clause has no case (Fix 1) |

The spec is not edited by the Verifier.

---

## Summary

**Overall**: ❌ Not Ready, on one small fix task

**Spec-anchored check**: 63 of 63 criteria matched the spec outcome; 0 spec-precision gaps
**Sensor**: 7 of 8 killed; FACE-UNQUOTE-ONLY alive on `J:46`, the line the round changed, and shown to lose a Finding
**Gate**: Full green on Windows (54 passed, 499 collected) and in the Playwright image (54 passed); the Build of `c7a4729` passed in the orchestrator's run (499)

**What works**: the fix of issue #20, on Windows and on Linux; FNT-63 and its neighbours FNT-58 to FNT-60; the residual N60-unescape-quotes-only of the second pass now dies; every rule of name matching dies under its mutant (case, quotes of the First family, escapes of a computed value).

**Issues found**: one mutant of the changed line alive: the quote half of the rule FNT-63 states has no case (Fix 1).

**Next steps**: F5 (Fix 1), then a fourth pass on its range; a CI run of the branch once it is pushed.
