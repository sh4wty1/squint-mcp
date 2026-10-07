# detect_visual_bugs + text-clipped Validation

**Date**: 2026-10-07
**Spec**: `.specs/features/detect-visual-bugs-text-clipped/spec.md`
**Diff range**: `389230a..9500a19` (18 commits, branch `feat/detect-visual-bugs-text-clipped`)
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 3 of 3 (the last before escalating to the maintainer)

**Verdict**: ✅ PASS (pass 3 itself was ❌ FAIL; its four survivors are killed in "Re-run of the survivors of pass 3", below. The PASS rests on that re-run, not on a fourth pass of the Verifier named above; the four kills were reproduced independently in `.checks/pr7-f3-status-lines.verified.md`)

What follows, down to the re-run section, is pass 3 as written at `9500a19`. Every requirement is implemented and every assertion targets the outcome the spec defines; the gate is green. Fix 8 to Fix 15 of pass 2 all meet their "done when": the 9 mutants that survived pass 2 are now killed. No defect was found in the source in any of the three passes. The verdict is FAIL because of the rule of `validate.md` as written ("Surviving mutants are fix tasks - do not mark the feature done if the sensor found weak tests"): of 8 new mutants tried for the first time in this pass, 4 survived. Three of them break a rule the spec states with a defined outcome; the fourth breaks a rule the spec states without naming its reach (a spec-precision gap). The fixes are tests, fixtures and one line of spec wording.

This was the third fix→re-verify iteration, so the gaps go to the maintainer, not back into the loop. What the maintainer has to weigh is in "For the maintainer" at the end.

**The branch moved while this report was being written.** Everything here (gate, sensor, line numbers) describes `9500a19`. After the sensor finished and before this report was saved, two commits landed on the branch from another session: `5ea9085` (a checklist for the review of PR #7) and `7910fe3` (`fix(checks): skip text-clipped on hidden text over a non-flat backdrop`), which changes `src/squint_mcp/checks/text_clipped.py`, `tests/test_text_clipped.py`, `tests/fixtures/text-clipped-clean.html` and the fixture list of `spec.md`. They are outside the verified range: this pass did not run the gate or the sensor on them. Two consequences:

- `7910fe3` fixes a source defect that was present at `9500a19` and that none of the three passes reported: a `visibility: hidden` element whose parent paints more than one colour behind the edge strip got a Finding, against DVB-30. By reading, that is right: at `9500a19` `_is_clipped` reads no `visibility`, and only the flat page behind `#invisible` kept DVB-30 green. Pass 2 saw the same mechanism on `#two-colours` and filed it as an observation, not as a gap. So "no source defect was found" below means found by the Verifier, not that there was none.
- From `7910fe3` on, the lines of `tests/test_text_clipped.py` after `C:93` are 5 further down and those of `text_clipped.py` after line 83 are 2 further down than cited here.

**History**

| Pass | Range | Verdict | Sensor in that pass | Closed by |
| ---- | ----- | ------- | ------------------- | --------- |
| 1 | `389230a..c6e124c` (report in `2973d07`) | FAIL | 40 mutants, 9 survived; 2 spec-precision gaps | `148a6fa`, `bcaee50` (tests, fixtures), `f8939eb` (spec wording) |
| 2 | `389230a..f8939eb` (report in `a260a11`) | FAIL | 10 re-runs all killed; 11 new, 9 survived | `349b31e`, `fefd0d5` (tests, fixtures), `9500a19` (spec fixture list) |
| 3 | `389230a..9500a19` (this report) | FAIL | 11 re-runs all killed; 8 new, 4 survived | `6ffb1c7`, `ea482ef` (tests, fixtures), `6e952a2` (spec fixture list); re-run below |

No file under `src/` changed after `c6e124c` (`git diff c6e124c..9500a19 -- src` is empty, verified by running).

Abbreviations: `D` = `tests/test_detect_visual_bugs.py`, `C` = `tests/test_text_clipped.py`, `S` = `tests/test_selectors.py`.

---

## Re-run of the survivors of pass 3

**Date**: 2026-10-07, at `883b661`. **Result**: all four killed.

Option (a) of "For the maintainer" was taken: Fix 16 to Fix 19 were applied by `6ffb1c7` (Fix 16, Fix 19) and `ea482ef` (Fix 17, Fix 18), with the fixture list of `spec.md` updated in `6e952a2`, and the four survivors were run again, alone. Each mutation was applied by itself to a scratch worktree of `883b661`, the named test was run against the mutated `src/`, and the worktree was restored. Unmutated, the four tests pass.

| # | Mutation at `883b661` | Test | Result |
| - | --------------------- | ---- | ------ |
| M1 | `detect_visual_bugs.py:73`: `for name in names` → `for name in reversed(names)` | `D` `test_the_first_unknown_check_in_the_order_given_is_the_one_named` | ✅ Killed: the message names `nope`, not `zzz` |
| M4 | `text_clipped.py:57`: `_padding_right` returns `... + element.client_width - element.box_model.padding.right` | `C` `test_the_strip_ends_at_the_padding_edge_not_at_the_content_edge` | ✅ Killed: `#padded` gets a Finding |
| M5 | `config.py:70`: `TRANSFORM_MIN_SIZE_DIFF_PX = 1` → `2` | `C` `test_an_element_painted_at_another_size_than_laid_out_is_not_reported` | ✅ Killed: `#nudged` is reported |
| M6 | `collect_elements.js:20`: `.replace(/[\\"]/g, "\\$&")` → `.replace(/"/g, "\\$&")` | `S` `test_a_backslash_in_an_attribute_value_is_escaped` | ✅ Killed: the selector is `[data-testid="a\b"]` |

Two things differ from pass 3 and are stated so the result is not read for more than it is:

- **Who ran it.** Not the Verifier of passes 1 to 3: the session that resolved F3 of the review of PR #7, which wrote none of Fix 16 to Fix 19. The checklist is `.checks/pr7-f3-status-lines.md`; its independent verification is `.checks/pr7-f3-status-lines.verified.md`.
- **The source moved after `9500a19`.** `7910fe3`, `1827675`, `8c144c8`, `2929cbd` and `bc80575` changed `src/` to answer the review of PR #7. They are outside the range of the three passes and were verified apart, in `.checks/pr7-review-fixes.verified.md` (PASS, 9 of 9 checks). Because of `bc80575` the expression M4 mutates now lives in `_padding_right`, which feeds the strip and the own-text comparison of DVB-71; because of `8c144c8` the one M6 mutates is in `quoted`. No sensor was run on the new source beyond these four mutants.

**Gate at `883b661`**: 135 passed, 0 failed, 0 skipped; pyright, ruff check and ruff format clean.

With the PASS, DVB-68 is due: `docs/ROADMAP.md` shows slice 3 as `concluída` in the table and in its section.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 | ✅ Done | `dd81c5a` |
| T2 | ✅ Done | `d76f66b` |
| T3 | ✅ Done | `0d24fc3` |
| T4 | ✅ Done | `137c98c` |
| T5 | ✅ Done | `e5a6d01` |
| T6 | ✅ Done | `e850693` |
| T7 | ✅ Done | `d4e0a46` |
| T8 | ✅ Done | `08afc15` |
| T9 | ✅ Done | `c6e124c` |
| Fix 1 to Fix 7 (pass 1) | ✅ Done | `148a6fa`, `bcaee50`, `f8939eb`; judged in pass 2 |
| Fix 8 to Fix 15 (pass 2) | ✅ Done | `349b31e`, `fefd0d5`, `9500a19` (see Fixes of pass 2, judged) |
| Fix 16 to Fix 19 (pass 3) | ✅ Done | `6ffb1c7`, `ea482ef`, `6e952a2`; judged in the re-run |

`tasks.md` has 55 checked boxes and none open.

---

## Spec-Anchored Acceptance Criteria

Verified by running: the whole suite passes (see Gate Check). The match between each assertion and the spec outcome was verified by reading. Line numbers are those of `9500a19`.

### P1: Run Checks on a page

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-01 | exactly `ping`, `inspect_element`, `detect_visual_bugs` | `tests/test_ping.py:36` - `sorted(tool.name ...) == ["detect_visual_bugs", "inspect_element", "ping"]`; also `tests/test_inspect_element.py:421` | ✅ PASS |
| DVB-02 | `readOnlyHint: true`, `openWorldHint: true` | `D:43-44` - `annotations.read_only_hint is True`, `annotations.open_world_hint is True` | ✅ PASS |
| DVB-03 | properties exactly `url`, `viewports`, `checks`; `url` string, required; the others array-or-null | `D:52` - `set(properties) == {"url", "viewports", "checks"}`; `D:53-54` - `properties["url"]["type"] == "string"`, `schema["required"] == ["url"]`; `D:64` - option types `== {"array", "null"}`; `D:69-71` - viewport object with `{"width", "height"}`, check item `"string"` | ✅ PASS |
| DVB-04 | `isError: false`, keys exactly `findings`, `captures` | `D:76,78` - `result.is_error is False`, `set(result.structured_content) == {"findings", "captures"}` | ✅ PASS |
| DVB-05 | each capture has exactly `viewport`, `stabilized` | `D:85` - `set(captured) == {"viewport", "stabilized"}` (two captures, `D:83`) | ✅ PASS |
| DVB-06 | `[{"viewport": {"width": 1440, "height": 900}, "stabilized": true}]` | `D:90` - `content["captures"] == [{...1440, 900..., "stabilized": True}]` | ✅ PASS |
| DVB-07 | `null` equals omitting | `D:97-98` - `detect(viewports=None) == omitted`, `detect(checks=None) == omitted` | ✅ PASS |
| DVB-08 | exactly 2 Findings, each `text-clipped` | `D:103` - `[f["check"] ...] == ["text-clipped"] * 2` | ✅ PASS |
| DVB-09 | `["text-clipped"]` equals omitting | `D:110` - `detect(checks=["text-clipped"]) == omitted` | ✅ PASS |
| DVB-10 | `isError: false`, `findings == []`, no image, text `No findings in 1 viewport.` | `C:72-76` - `is_error is False`, `findings == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| DVB-11 | first block is text `Found 2 findings in 1 viewport: 1 major, 1 minor.` | `D:115-117` - `first = result.content[0]`, `first.text == "Found 2 findings in 1 viewport: 1 major, 1 minor."`; the singular of the Assumptions row `D:122` - `texts(result) == ["Found 1 finding in 1 viewport: 1 major."]` | ✅ PASS (closed in pass 3: N5 is killed) |
| DVB-12 | two equal calls return equal structured content | `D:128` - `detect(BUG) == detect(BUG)` | ✅ PASS |

### P1: Read a Finding

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-13 | the eleven Finding keys; evidence keys `computed`, `measured`, `cropIndex` | `D:135-148` - `set(finding) == {...11 keys}`, `set(finding["evidence"]) == {"computed", "measured", "cropIndex"}` | ✅ PASS |
| DVB-14 | the literal Finding of the `h1` | `S:100-122` - `findings[0] == {...}`; compared field by field with the spec literal, identical | ✅ PASS |
| DVB-15 | severity, then viewport order, then document order; the `h1` before `#badge` | `D:155-158` - severities `== ["major", "minor"]`, `h1` is `findings[0]`, `#badge` is `findings[1]`; document order `D:181-199` - all severities `== {"major"}`, the full list of 19 `text` values of `selectors.html`, and the selectors of `many.html` `== ["#m1", ..., "#m6", "#small"]`; viewport order `D:235-239` | ✅ PASS |
| DVB-16 | `#long`: 39 `X` then `…` | `D:166` - `finding["text"] == "X" * 39 + "…"`; the boundary `D:171-174` - the texts of length 40 `== ["X" * 39 + "…", "X" * 40]` | ✅ PASS |
| DVB-17 | `#spaced`: `XXXXX XXXXX` | `D:221` - `finding["text"] == "XXXXX XXXXX"` | ✅ PASS |
| DVB-18 | every selector of both fixtures resolves in `inspect_element` to the same `box` | `S:128-140` - counts `2` and `19`, `result.is_error is False`, `result.structured_content["box"] == finding["box"]`; the fixtures now hold a path with `:nth-of-type` above its last segment (`S:55-56`) and an id that needs escaping (`S:60`) | ✅ PASS (closed in pass 3: N11 and N8 are killed). ⚠️ No attribute value holds a backslash (mutant M6, spec-precision gap) |

### P1: Detect clipped text

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-19 | exactly one Finding for the element | `C:17-19` - `(finding,) = findings_on(BUG, "h1")`, `check == "text-clipped"`, `overflow-x == "hidden"`; pixel confirmation: `C:106` - `findings_on(STRIP, "#bordered") == []`, `C:111-112` - one Finding on `#right-border`, `overflowPx == 50`, `C:120` - `findings_on(STRIP, "#narrow") == []`, `C:127-128` - one Finding on `#gap-at-edge`, `overflowPx == 70`, `C:133-134` - one Finding on `#two-colours`, `overflowPx == 50` | ✅ PASS (closed in pass 3: N1, N2 and N4 are killed). ⚠️ No fixture element has padding, so the padding box is not told from the content box (mutant M4) |
| DVB-20 | one Finding for `#clip`, `overflow-x` equal to `clip` | `C:24-25` - `(finding,) = ...`, `computed["overflow-x"] == "clip"` | ✅ PASS |
| DVB-21 | `#over-8`: `major`, `overflowPx` 8 | `C:31-32` - `severity == "major"`, `overflowPx == 8` | ✅ PASS |
| DVB-22 | `#over-7`, `#over-2`: `minor`, 7 and 2 | `C:38-40` - `(finding,) = ...`, `severity == "minor"`, `overflowPx == overflow_px` | ✅ PASS |
| DVB-23 | no Finding for `#over-1`; fixture yields exactly 5 | `C:45-46` - `findings_on(..., "#over-1") == []`, `len(findings) == 5` | ✅ PASS |
| DVB-24 to DVB-33 | no Finding for `#fits`, `#wraps`, `#visible`, `#scrolls`, `#ellipsis`, `#sr-only`, `#invisible`, `#blank-tail`, `#ancestor` and its child, `#rtl` | `C:80-93` - `reported(client, near_misses) == []`; and `C:74` - `findings == []` for the whole fixture | ✅ PASS |
| DVB-69 | no Finding for `#scaled`, `#stretched`, `#widened`, `#turned`, `#in-scaled` | `C:99-100` - `resized = ("#scaled", "#stretched", "#widened", "#turned", "#in-scaled")`, `reported(client, resized) == []`; and `C:74` | ✅ PASS on the five named elements. ⚠️ Each differs from its layout size by 15px or more, so "by 1px or more" is not pinned (mutant M5) |
| DVB-70 | `#moved`: `box` `{70, 410, 150, 30}`, `overflowPx` 50 | `C:53-55` - `(finding,) = ...`, `finding["box"] == {"x": 70, "y": 410, "w": 150, "h": 30}`, `overflowPx == 50` | ✅ PASS |

### P1: Stable selectors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-34 | `[data-testid="save"]` | `S:24` - `== '[data-testid="save"]'` | ✅ PASS |
| DVB-35 | `#first-row` | `S:28` - `== "#first-row"` | ✅ PASS |
| DVB-36 | `button[aria-label="Close dialog"]` | `S:34` - `== 'button[aria-label="Close dialog"]'` | ✅ PASS |
| DVB-37 | `[role="tab"][aria-label="Settings"]` | `S:40` - `== '[role="tab"][aria-label="Settings"]'`; the digit bound `S:46-47` - `== 'div[aria-label="Step"]'` for `css-1a2b3c`, `== "#col-12"` for `col-12` | ✅ PASS (closed in pass 3: N7 is killed; J03 re-run and still killed) |
| DVB-38 | `body > main > p:nth-of-type(2)` | `S:70` - `== "body > main > p:nth-of-type(2)"` | ✅ PASS |
| DVB-39 | each its CSS path, the two differ | `S:78-79` - `== "body > main > button:nth-of-type(2)"`, `== "body > main > button:nth-of-type(3)"`; sibling containers `S:55-56` - `== "body > main > section:nth-of-type(1) > p"`, `== "body > main > section:nth-of-type(2) > p"` | ✅ PASS |
| DVB-40 | `body > main > h2` | `S:83` - `== "body > main > h2"` | ✅ PASS |
| DVB-41 | `[data-testid="card"] > h3` | `S:89` - `== '[data-testid="card"] > h3'`; uniqueness across shadow trees `S:66` - `== "#outside"` | ✅ PASS |
| DVB-42 | `[data-testid="say \"hi\""]` | `S:93` - `== '[data-testid="say \\"hi\\""]'`; id escaping (Assumptions: selector quoting) `S:60` - `== "#\\32 col"` | ✅ PASS |

### P1: Bounded crops

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-43 | one text block, then exactly min(N, 5) `image/png` blocks | `D:260-264` - for N = 2 and N = 7: `isinstance(result.content[0], TextContent)`, `result.content[1:] == images(result)`, mime types `== ["image/png"] * crops`; N = 0 at `C:75` | ✅ PASS |
| DVB-44 | `cropIndex` `0, 1, 2, 3, 4, null, null`; last is the `minor` of `#small` | `D:269-279` - list `== [0, 1, 2, 3, 4, None, None]`, `findings[6]["severity"] == "minor"`, `findings_on(MANY, "#small") == [findings[6]]` | ✅ PASS |
| DVB-45 | each image 182×62, text colour of its own element at (20, 31) | `D:298-299` - `crop.size == (182, 62)`, `crop.getpixel((20, 31)) == text_color` for `#m1` to `#m5`; second viewport `D:212-215` - `crop.size == (227, 62)`, `getpixel((208, 31)) == (0, 0, 0)`, `getpixel((213, 31)) == (255, 255, 255)` for `#half` at 390×844 | ✅ PASS |

### P1: Several viewports

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-46 | two captures in order; 3 Findings in the given order; `#half` `overflowPx` 5; the text block | `D:230-247` - `captures == [DESKTOP, MOBILE entries]`, `(viewport, severity)` list, `on == [[findings[0]], [findings[1]], [findings[2]]]`, `overflowPx == 5`, `texts(result) == ["Found 3 findings in 2 viewports: 2 major, 1 minor."]` | ✅ PASS |
| DVB-47 | `isError: false`, `captures[0].stabilized` false | `D:253-254` - `detect(...)` (asserts `is_error is False`, `tests/helpers.py:34`), `stabilized is False` | ✅ PASS |
| DVB-48 | repeated viewport captured once; same findings | `D:305-307` - `twice["captures"] == [{MOBILE, True}]`, `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]`; first occurrence `D:312-315` - `[DESKTOP, MOBILE, DESKTOP]` gives `captures == [DESKTOP, MOBILE entries]` | ✅ PASS (closed in pass 3: N6 is killed) |
| DVB-49 | repeated check name: same findings | `D:321-322` - `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]` | ✅ PASS |

### P1: Clear errors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-50 | `isError: true`, `Unknown check "nope". Valid checks: text-clipped.` | `D:328,334` - `result.is_error is True`, `'Unknown check "nope". Valid checks: text-clipped.' in text`; after a valid name `D:341` - the same text for `["text-clipped", "nope"]` | ✅ PASS (closed in pass 3: N10 is killed). ⚠️ No call holds two unknown names, so "names the first unknown name in the order given" is not pinned (mutant M1) |
| DVB-51 | the unknown-Check error, not the Chromium one | `D:349-350` - same text `in text`, `"Could not launch Chromium" not in text` | ✅ PASS |
| DVB-52 | error names `checks` | `D:354` - `"checks" in error_text(...)` | ✅ PASS |
| DVB-53 | error names `viewports` | `D:358` - `"viewports" in error_text(...)` | ✅ PASS |
| DVB-54 | error names the offending field | `D:362-365` - `field in text` for `width` and `height` at 0 | ✅ PASS |
| DVB-55 | error names `url` | `D:369` - `"url" in error_text(client, {})` | ✅ PASS |
| DVB-56 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `D:374` - that text `in text` | ✅ PASS |
| DVB-57 | `Could not load ` + URL | `D:379` - `f"Could not load {url}" in error_text(...)` | ✅ PASS |
| DVB-58 | `Could not launch Chromium` and `playwright install chromium` | `D:386-387` - both `in text` | ✅ PASS |
| DVB-59 | `Timed out after Ns` within 1s of the timeout; next call answered | `D:404-406` - `"Timed out after 4s" in text`, `4 <= elapsed < 5`, `len(detect(BUG)["findings"]) == 2` | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| ID | Spec-defined outcome | Evidence | Result |
| -- | -------------------- | -------- | ------ |
| DVB-60 | own module under a Checks package; Capture in, Findings out | `src/squint_mcp/checks/text_clipped.py:118` - `def check(capture: Capture) -> list[Finding]` | ✅ PASS |
| DVB-61 | only the Capture module imports `playwright` | grep of `src/`: the only imports are `src/squint_mcp/capture.py:12-14` | ✅ PASS |
| DVB-62 | one registry | `src/squint_mcp/checks/__init__.py:14` - `CHECKS: dict[str, Check] = {"text-clipped": text_clipped.check}`; resolved at `src/squint_mcp/tools/detect_visual_bugs.py:71,74,75,99` and nowhere else | ✅ PASS |
| DVB-63 | page JavaScript in `.js` files only | `src/squint_mcp/capture.py:20-21` reads `js/stabilize.js` and `js/collect_elements.js`; the only `evaluate` calls (`capture.py:97,112`) pass those | ✅ PASS |
| DVB-64 | crop limit 5, excerpt 40, minimum overflow 2, major threshold 8, each with a cited source | `src/squint_mcp/config.py:54-55`, `57-58`, `60-62`, `64-66` | ✅ PASS |
| DVB-65 | no dependency slice 2 did not declare | `git diff 389230a..9500a19 -- pyproject.toml uv.lock` is empty (run) | ✅ PASS |
| DVB-66 | `inspect_element` tests pass without any change to their assertions other than the exact tool list of DVB-01 | all pass; `git diff 389230a..9500a19 -- tests/test_inspect_element.py` changes one assertion, `tests/test_inspect_element.py:421`, the exact tool list, from two names to three (run) | ✅ PASS |
| DVB-67 | `Unreleased` lists the tool and the Check; README table lists the tool | `CHANGELOG.md:14-15` under `## [Unreleased]` (`CHANGELOG.md:7`); `README.md:17` | ✅ PASS |
| DVB-68 | ROADMAP shows slice 3 `concluída` once the Verifier reports PASS | A closing step of the orchestrator, made only after a PASS verdict. It is not a criterion this report fails on; the lines it concerns are `docs/ROADMAP.md:19,73` | ✅ PASS after the re-run: `docs/ROADMAP.md:19,73` |

**Status** (as of pass 3; closed by the re-run): ❌ Gaps present. 69/69 testable requirements have an assertion on the spec-defined outcome (DVB-68 pending on verdict); 1 spec-precision gap flagged (M6); 4 surviving mutants, all found in pass 3.

### Spec-precision gaps

1. **Assumptions: selector quoting, "always double-quoted and escaped"** (open, found in pass 3, mutant M6). The row says attribute values are escaped and that "a quoted value is valid for every string", but the only character the spec names is the double quote (DVB-42 and the Edge Cases list). It does not say that a backslash is escaped too. The source does escape it; no test would notice if it stopped.
2. DVB-66 against DVB-01, and "in width or in height" of DVB-69: found in pass 1, closed in pass 2.

### Observations (not gaps)

- The fixture list of the spec says `text-clipped-strip.html` holds "three elements" and then lists five. The list is right; the count is stale.
- Fix 14 replaced the id `step-123` by `css-1a2b3c` instead of adding an element. Three adjacent digits are now carried only by `item-48213`. J03 (`>= 3` → `>= 4`) was re-run for that reason and is still killed.
- `#two-colours` pins a Finding on text nobody can see. That is the rule as written ("painted in more than one colour") and the spec's fixture list names it; it sits in tension with the rationale of the same row ("Rejects ... hidden text"). Unchanged since pass 2.
- "Lists the valid names alphabetically" (Assumptions: unknown Check) cannot be observed while one Check exists. No mutant was run on it; slice 4 makes it observable.

---

## Fixes of pass 2, judged

Done-when verified by running each mutant in pass 3; anchors and test quality verified by reading `git diff a260a11..9500a19`.

| Fix | Done when | Evidence | Spec anchor | Met? |
| --- | --------- | -------- | ----------- | ---- |
| 8 | N11 killed | `tests/fixtures/selectors.html:92-94`, `S:50-56`. N11 dies on `S:55` | Assumptions: CSS path | ✅ |
| 9 | N8 killed | `selectors.html:96`, `S:59-60`; the loop `S:128-140` proves `#\32 col` resolves. N8 dies on `S:60` | Assumptions: selector quoting; DVB-18 | ✅ |
| 10 | N1 and N2 killed | `tests/fixtures/text-clipped-strip.html:32-39`, `C:109-112`. N1 dies on `C:111`, N2 on `C:106` | Assumptions: pixel confirmation | ✅ (done differently from the task text: the top and bottom borders went onto `#bordered`, and the right border onto a new element that expects a Finding; both kill) |
| 11 | N10 killed | `D:337-341`. N10 dies on `D:341` | DVB-50; Assumptions: unknown Check | ✅ on the done-when. ⚠️ The task text also asked for `["zzz", "nope"]` naming `zzz` and for the call without Chromium; neither was written. The first is mutant M1 of this pass |
| 12 | N5 killed | `D:120-122`. N5 dies on `D:122` | Assumptions: text summary | ✅ |
| 13 | N6 killed | `D:310-315`. N6 dies on `D:312` | Assumptions: duplicate entries; DVB-48 | ✅ |
| 14 | N7 killed | `selectors.html:90`, `S:46`. N7 dies on `S:46` | Assumptions: ids that look generated | ✅ |
| 15 | N4 killed | `text-clipped-strip.html:40-45,60`, `C:115-120`. N4 dies on `C:120` | Assumptions: pixel confirmation | ✅ |

Judgement of the new tests:

- No assertion was deleted or weakened. Two existing assertions changed, both to follow the larger fixture: the `text` list of `D:183-189` (16 to 19 entries) and the count of `S:128` (16 to 19).
- Every new test has a spec anchor (the column above), and the spec's fixture list names every new fixture element. None mirrors the implementation: each asserts a literal that follows from the fixture or from an Assumptions row.
- One new test would still pass under a plausible wrong implementation: `D:337-341` passes when the last unknown name is reported instead of the first (M1).
- `C:111` kills N1 on the unpacking `(finding,) = ...`, which is the test's own "exactly one Finding" assertion.

---

## Discrimination Sensor

**Pass 3 scratch**: a temporary `git worktree` at `9500a19` in `C:\tmp\sq-wt3`, with its own `.venv` from `uv sync`. `import squint_mcp` there printed `C:\tmp\sq-wt3\src\squint_mcp\__init__.py`. The unmutated baseline passed there (66 passed in the three feature test files). Each mutant was applied alone, `git diff --stat` confirmed it, the relevant test file ran, and the file was restored (`git status --porcelain` of the worktree empty before and after each). A mutant that passed its relevant file was then run against the whole suite before being called a survivor. `git status --porcelain` of the real tree was empty before and is byte-identical after; the worktree is removed and `git worktree list` shows only the real tree.

The mutants marked "pass 1" or "pass 2" in the last column were not re-run in pass 3: no file under `src/` changed since, and no assertion or fixture element that killed them was removed or weakened. J03 and C14 were re-run because the pass-2 fixes changed the fixture element that killed them.

| # | File:line | Mutation | Killed? | Last run |
| - | --------- | -------- | ------- | -------- |
| C01 | `src/squint_mcp/checks/text_clipped.py:77` | `element.own_text` → `True` | ✅ Killed | pass 1 |
| C02 | `text_clipped.py:79` | `("hidden", "clip")` → `("hidden",)` | ✅ Killed | pass 1 |
| C03 | `text_clipped.py:79` | `("hidden", "clip")` → `("hidden", "clip", "auto")` | ✅ Killed | pass 1 |
| C04 | `text_clipped.py:81` | `computed["text-overflow"] == "clip"` → `True` | ✅ Killed | pass 1 |
| C05 | `text_clipped.py:83` | `computed["direction"] == "ltr"` → `True` | ✅ Killed | pass 1 |
| C06 | `text_clipped.py:84` | `>= TEXT_CLIPPED_MIN_OVERFLOW_PX` → `>` | ✅ Killed | pass 1 |
| C07 | `src/squint_mcp/config.py:62` | `TEXT_CLIPPED_MIN_OVERFLOW_PX = 2` → `1` | ✅ Killed | pass 1 |
| C08 | `text_clipped.py:95` | `>= TEXT_CLIPPED_MAJOR_OVERFLOW_PX` → `>` | ✅ Killed | pass 1 |
| C09 | `text_clipped.py:86` | removed `and not _is_resized(element)` | ✅ Killed | pass 1 |
| C10 | `text_clipped.py:89` | removed `and not is_flat(pixels, _edge_strip(element))` | ✅ Killed | pass 1 |
| C11 | `text_clipped.py:50` | removed the width clause | ✅ Killed (`C:74`; survived pass 1) | pass 2 |
| C12 | `text_clipped.py:51` | removed the height clause | ✅ Killed | pass 1 |
| C13 | `text_clipped.py:65` | `left = max(padding_left, right - font_size)` → `left = right - 1` | ✅ Killed (survived pass 1) | pass 2 |
| C14 | `text_clipped.py:63` | `padding_left = element.box.x + border.left` → `element.box.x` | ✅ Killed (`C:106`; survived pass 1) | pass 3, re-run |
| C15 | `text_clipped.py:121` | `capture.elements` → `reversed(capture.elements)` | ✅ Killed on order assertions | pass 2 |
| V01 | `src/squint_mcp/vision.py:48` | `getcolors(maxcolors=1)` → `getcolors(maxcolors=2)` | ✅ Killed (survived pass 1) | pass 2 |
| T01 | `src/squint_mcp/tools/detect_visual_bugs.py:102` | removed the severity sort | ✅ Killed | pass 1 |
| T02 | `config.py:55` | `MAX_CROPS = 5` → `4` | ✅ Killed | pass 1 |
| T03 | `detect_visual_bugs.py:105` | `crop_png(captured.pixels, ...)` → `crop_png(captures[0].pixels, ...)` | ✅ Killed (survived pass 1) | pass 2 |
| T04 | `detect_visual_bugs.py:110` | `crop_index = index` → `index + 1` | ✅ Killed | pass 1 |
| T05 | `detect_visual_bugs.py:82` | removed the viewport dedup | ✅ Killed | pass 1 |
| T06 | `detect_visual_bugs.py:71` | `list(dict.fromkeys(checks or CHECKS))` → `list(checks or CHECKS)` | ✅ Killed | pass 1 |
| T07 | `detect_visual_bugs.py:87-92` | one timeout per viewport instead of one for the call | ✅ Killed | pass 1 |
| T08 | `detect_visual_bugs.py:71` | browser launched before the Check names are validated | ✅ Killed | pass 1 |
| T09 | `detect_visual_bugs.py:43` | summary severities in reverse order | ✅ Killed | pass 1 |
| T10 | `detect_visual_bugs.py:97` | `for captured in captures` → `reversed(captures)` | ✅ Killed | pass 1 |
| J01 | `src/squint_mcp/js/collect_elements.js:79` | `flat.length > textLimit` → `>=` | ✅ Killed (survived pass 1) | pass 2 |
| J02 | `collect_elements.js:79` | `slice(0, textLimit - 1)` → `slice(0, textLimit)` | ✅ Killed | pass 1 |
| J03 | `collect_elements.js:33` | digits `.length >= 3` → `>= 4` | ✅ Killed (`S:46`; survived pass 1) | pass 3, re-run |
| J04 | `collect_elements.js:33` | removed the `[^A-Za-z0-9_-]` rule | ✅ Killed | pass 1 |
| J05 | `collect_elements.js:63` | id tried before `data-testid` | ✅ Killed | pass 1 |
| J06 | `collect_elements.js:63` | `roleLabel \|\| tagLabel` → `tagLabel \|\| roleLabel` | ✅ Killed | pass 1 |
| J07 | `collect_elements.js:64` | `matches.get(selector) === 1` → `>= 1` | ✅ Killed | pass 1 |
| J08 | `collect_elements.js:59` | `twins.length > 1` → `> 0` | ✅ Killed | pass 1 |
| J09 | `collect_elements.js:41` | removed `if (element.shadowRoot) walk(element.shadowRoot);` | ✅ Killed (survived pass 1) | pass 2 |
| J10 | `collect_elements.js:133` | removed `.sort((a, b) => order.get(a) - order.get(b))` | ✅ Killed (survived pass 1) | pass 2 |
| J11 | `collect_elements.js:125` | `node.nodeValue.trim() !== ""` → `node.nodeValue !== ""` | ✅ Killed | pass 1 |
| J12 | `collect_elements.js:73` | removed the host selector of a shadow path | ✅ Killed | pass 1 |
| J13 | `collect_elements.js:17` | attribute value not escaped | ✅ Killed | pass 1 |
| J14 | `collect_elements.js:78` | whitespace not collapsed | ✅ Killed | pass 1 |
| N1 | `text_clipped.py:64` | `right = padding_left + element.client_width` → `right = element.box.x + element.box.w` | ✅ Killed (`C:111`; survived pass 2) | pass 3, re-run |
| N2 | `text_clipped.py:68,70` | `y=element.box.y + border.top` → `element.box.y`; `h=element.box.h - border.top - border.bottom` → `element.box.h` | ✅ Killed (`C:106`; survived pass 2) | pass 3, re-run |
| N3 | `text_clipped.py:65` | `right - font_size` → `right - 2 * font_size` | ✅ Killed | pass 2 |
| N4 | `text_clipped.py:65` | `left = max(padding_left, right - font_size)` → `left = right - font_size` | ✅ Killed (`C:120`; survived pass 2) | pass 3, re-run |
| N5 | `detect_visual_bugs.py:46` | `Found {_count(len(findings), 'finding')}` → `Found {len(findings)} findings` | ✅ Killed (`D:122`; survived pass 2) | pass 3, re-run |
| N6 | `detect_visual_bugs.py:82` | viewport dedup keeps the place of the last occurrence instead of the first | ✅ Killed (`D:312`; survived pass 2) | pass 3, re-run |
| N7 | `collect_elements.js:33` | `id.replace(/\D/g, "").length >= 3` → `/\d{3}/.test(id)` | ✅ Killed (`S:46`; survived pass 2) | pass 3, re-run |
| N8 | `collect_elements.js:25` | `` `#${CSS.escape(element.id)}` `` → `` `#${element.id}` `` | ✅ Killed (`S:60`; survived pass 2) | pass 3, re-run |
| N9 | `detect_visual_bugs.py:121` | image blocks emitted in reverse order | ✅ Killed | pass 2 |
| N10 | `detect_visual_bugs.py:73` | `for name in names` → `for name in names[:1]` | ✅ Killed (`D:341`; survived pass 2) | pass 3, re-run |
| N11 | `collect_elements.js:70` | `segments.unshift(segment(node))` → `segments.unshift(node.localName)` | ✅ Killed (`S:55`; survived pass 2) | pass 3, re-run |
| M1 | `detect_visual_bugs.py:73` | `for name in names` → `for name in reversed(names)` (the last unknown name is reported, not the first) | ❌ Survived → Fix 16 | pass 3, new |
| M2 | `detect_visual_bugs.py:44` | removed `if by_severity[severity]` (severities that do not occur are listed with 0) | ✅ Killed (`D:117`) | pass 3, new |
| M3 | `detect_visual_bugs.py:114` | `stabilized=captured.stabilized` → `stabilized=True` | ✅ Killed (`D:254`) | pass 3, new |
| M4 | `text_clipped.py:64` | `right = padding_left + element.client_width` → `... - element.box_model.padding.right` (the strip ends at the content box, not at the padding box) | ❌ Survived → Fix 17 | pass 3, new |
| M5 | `config.py:70` | `TRANSFORM_MIN_SIZE_DIFF_PX = 1` → `2` | ❌ Survived → Fix 18 | pass 3, new |
| M6 | `collect_elements.js:17` | `value.replace(/[\\"]/g, "\\$&")` → `value.replace(/"/g, "\\$&")` (a backslash in an attribute value is not escaped) | ❌ Survived → Fix 19 (spec-precision gap) | pass 3, new |
| M7 | `text_clipped.py:50-51` | `abs(...)` removed from both clauses (an element painted smaller than laid out is not seen as resized) | ✅ Killed (`C:74`) | pass 3, new |
| M8 | `collect_elements.js:78` | `.trim()` removed from the excerpt | ✅ Killed (`S:89`) | pass 3, new |

**Sensor depth**: expanded (first Check and the Finding contract): 59 distinct mutations across the Check (22), `vision.is_flat` (1), the tool (17) and the collector (19).
**Pass 3 runs**: 19 mutants run. 11 re-runs (the 9 survivors of pass 2, plus J03 and C14): 11/11 killed. 8 new: 4 killed, 4 survived.
**Carried over, not re-run in pass 3**: 40 killed (30 last run in pass 1, 10 in pass 2).
**Result**: 55/59 killed, 4 survived - FAIL ❌

### The four survivors

Each was probed in the scratch worktree with a throwaway fixture and test (not kept): against the unmutated source the four probes passed, so the source behaves as the spec says in each case; with the four mutants applied, the four probes failed. Verified by running, except where noted.

| # | What the mutant breaks | Does the spec define the outcome? | Kind |
| - | ---------------------- | --------------------------------- | ---- |
| M1 | `checks=["zzz", "nope"]` reports `nope`; the source reports `zzz` | Yes. Assumptions, unknown Check: "The message names the first unknown name in the order given" | Coverage gap |
| M4 | A box with `padding-right: 30px` whose glyphs end 10px inside its content edge, with only spaces overflowing, gets a Finding; the source gives none | Yes. Assumptions, pixel confirmation: "the strip of the element's padding box within one `font-size` of its right edge"; a strip of one colour "yields no Finding" | Coverage gap |
| M5 | An element under `transform: scaleX(1.01)` (painted 151.5px wide, laid out 150px) gets a Finding; the source gives none | Yes. DVB-69 and Assumptions, element under a `transform`: "differs ... by 1px or more in width or in height yields no Finding" | Coverage gap (a bound) |
| M6 | An element with `data-testid="a\b"` gets the selector `[data-testid="a\b"]`; the source gives `[data-testid="a\\b"]`, which `inspect_element` resolves to the same box. That the unescaped form does not resolve was inferred by reading (CSS reads `\b` as a hex escape), not run | Partly. Assumptions, selector quoting: "always double-quoted and escaped ... A quoted value is valid for every string". The row does not name the backslash; DVB-42 and the Edge Cases name only the double quote | Spec-precision gap |

No survivor is behaviour beyond the spec's ceiling: each is a rule the spec writes down. M6 is the one where the spec's own words stop short of the case.

---

## Interactive UAT Results

Not performed: the feature has no user interface; the MCP boundary is covered by the automated tests.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ |
| No scope creep | ✅ |
| Matches patterns | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met (1:1 ACs; happy + edge + error) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam, the MCP boundary; the one `monkeypatch` of `config.TOTAL_TIMEOUT_S` is the same reach slice 2 uses) | ✅ |
| Tests discriminate the behaviour they claim | ❌ 4 surviving mutants |

---

## Edge Cases

- [x] Clipped element inside an open shadow root is reported (DVB-41): `S:89`, and it is one of the 19 Findings of `S:128`.
- [x] Only whitespace overflows: no Finding (DVB-31): `C:88,93`.
- [x] `data-testid` holding a double quote is escaped (DVB-42): `S:93`.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`
- **Result** (real tree at `9500a19`, run in pass 3): pyright 0 errors, 0 warnings (exit 0); ruff check "All checks passed!" (exit 0); ruff format 62 files already formatted (exit 0); pytest 127 passed, 0 failed, 0 skipped in 143.64s (exit 0)
- **Test count before feature**: 61 (`389230a`)
- **Test count after feature**: 127 (112 at pass 1, 120 at pass 2)
- **Delta**: +66 new tests (+7 since pass 2)
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed; no assertion weakened.

---

## Fix Plans

All four are tests and fixtures, plus spec wording for Fix 19. No source change is expected: the probes of this pass show the source already behaves as the spec says in each case. Every new fixture element must also be named in the fixture list of `spec.md`.

### Fix 16: "Names the first unknown name" is unprotected (M1)

- **Root cause**: every test of the unknown-Check error holds exactly one unknown name. This was half of the task text of Fix 11 and was left out.
- **Fix task**: in `tests/test_detect_visual_bugs.py`, call `checks=["zzz", "nope"]` and assert `'Unknown check "zzz". Valid checks: text-clipped.' in text`. Done when mutant M1 (`detect_visual_bugs.py:73`) is killed.
- **Priority**: Minor

### Fix 17: The padding box is not told from the content box (M4)

- **Root cause**: no clipped fixture element has padding, so the right edge of the padding box and of the content box coincide everywhere.
- **Fix task**: add to `tests/fixtures/text-clipped-strip.html` an element with `padding-right: 30px` holding 7 glyphs and then spaces that overflow (`<div id="padded" class="clipped">XXXXXXX          </div>`); in `tests/test_text_clipped.py` assert no Finding for it. Done when mutant M4 (`text_clipped.py:64`) is killed.
- **Priority**: Major (padding is on most real boxes; reading the strip at the content edge gives a false Finding there, and a Finding has to be trustworthy)

### Fix 18: The 1px bound of the resize rule is unprotected (M5)

- **Root cause**: the five elements of DVB-69 differ from their layout size by 15px to 120px.
- **Fix task**: add to `tests/fixtures/text-clipped-clean.html` an element `#nudged` with class `clipped resized` and `transform: scaleX(1.01)` (painted 151.5px wide), name it in DVB-69 and in the `resized` tuple of `C:99`. Done when mutant M5 (`config.py:70`) is killed.
- **Priority**: Minor

### Fix 19: The reach of "escaped" is not stated, and a backslash is unprotected (M6)

- **Root cause**: the Assumptions row on selector quoting says "escaped" and the spec's only example is the double quote.
- **Fix task**: in `spec.md`, make the row say that a double quote and a backslash are each preceded by a backslash, and name the new element in the fixture list. Add to `tests/fixtures/selectors.html` a clipped element whose only stable attribute is `data-testid="a\b"`, with its own glyph count; assert its selector in `tests/test_selectors.py` and raise the count of `S:128`, whose loop then proves the selector resolves. Done when mutant M6 (`collect_elements.js:17`) is killed.
- **Priority**: Minor (spec-precision gap; the maintainer may instead decide that a backslash in a `data-testid` is beyond what this slice pins, and record that in the row)

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| DVB-01 to DVB-10, DVB-12 to DVB-17, DVB-20 to DVB-36, DVB-38 to DVB-47, DVB-49, DVB-51 to DVB-67, DVB-70 | ✅ Verified (pass 2) | ✅ Verified |
| DVB-11, DVB-37, DVB-48 | ❌ Needs Fix (pass 2) | ✅ Verified |
| DVB-18 | ❌ Needs Fix (pass 2) | ⚠️ Spec-precision gap (Fix 19) |
| DVB-19 | ❌ Needs Fix (pass 2) | ❌ Needs Fix (tests: Fix 17) |
| DVB-50 | ❌ Needs Fix (pass 2) | ❌ Needs Fix (tests: Fix 16) |
| DVB-69 | ✅ Verified (pass 2) | ❌ Needs Fix (tests: Fix 18) |
| DVB-68 | In Tasks | ✅ Verified (re-run) |
| DVB-18, DVB-19, DVB-50, DVB-69 | as above (pass 3) | ✅ Verified (re-run: M6, M4, M1, M5 killed) |

Each "Needs Fix" requirement passes on its named fixture; what is missing is the protection of an Assumptions row that backs it.

---

## Summary

**Overall**: ✅ Ready after the re-run of the four survivors. What follows is the summary of pass 3 as written at `9500a19`.

**Spec-anchored check**: 69/69 testable requirements matched the spec outcome | 1 spec-precision gap flagged | DVB-68 pending on verdict
**Sensor**: 55/59 mutations killed, 4 survived (pass 3 ran 19: 11 re-runs all killed, 8 new with 4 survivors; 40 kills carried over from passes 1 and 2)
**Gate**: 127 passed, 0 failed, 0 skipped; pyright, ruff check and ruff format clean

**What works**: the whole flow Capture → Check → Finding[] through `detect_visual_bugs`. Everything passes 1 and 2 found unprotected is now protected: 18 mutants that once survived are killed.

**Issues found**: no source defect. Four further rules the spec states are unprotected by tests (Fix 16 to Fix 19). The one that matters most is the padding box (Fix 17).

**Next steps**: this was iteration 3 of 3, so the decision goes to the maintainer.

### For the maintainer

- In three passes no defect was found in `src/`. Every gap has been a rule of the spec that no test would notice breaking.
- The pattern is steady: each pass kills everything the previous one found, and about half of the new mutants it tries survive (9 of 40, 9 of 11, 4 of 8). The spec has some forty Assumptions rows, most with several sub-rules, and the survivors come from sub-rules no fixture reaches. A fourth pass would very likely find more of the same kind.
- The options are: (a) apply Fix 16 to Fix 19 (four small tests, three fixture elements, one line of spec) and accept the feature on a re-run of M1, M4, M5 and M6 alone; (b) apply only Fix 17, the one with a real-page consequence, and record the other three as accepted limits in the spec; (c) accept as is. Under the rule of `validate.md` as written, only (a) turns this report into a PASS.
