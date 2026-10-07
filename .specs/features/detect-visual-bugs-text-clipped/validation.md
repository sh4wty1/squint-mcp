# detect_visual_bugs + text-clipped Validation

**Date**: 2026-10-07
**Spec**: `.specs/features/detect-visual-bugs-text-clipped/spec.md`
**Diff range**: `389230a..f8939eb` (14 commits, branch `feat/detect-visual-bugs-text-clipped`)
**Verifier**: independent sub-agent (author ≠ verifier), verification pass 2 of at most 3

**Verdict**: ❌ FAIL

Every requirement is implemented and every assertion targets the outcome the spec defines; the gate is green. Fix 1 to Fix 7 of pass 1 are all met: the 9 mutants that survived pass 1 are now killed, and the 2 spec-precision gaps are closed. The verdict is FAIL because 11 new mutants, tried for the first time in this pass, left 9 alive. Each one breaks a rule the spec states (an Assumptions row) and no test notices. No defect was found in the source. The fixes are tests and fixtures only.

**History**: pass 1 (`389230a..c6e124c`, report in commit `2973d07`) was FAIL: gate green, no source defect, 9 of 40 mutants alive, 2 spec-precision gaps. Commits `148a6fa` and `bcaee50` (tests and fixtures) and `f8939eb` (spec wording) closed all of it. No file under `src/` changed after `c6e124c` (`git diff c6e124c..f8939eb -- src` is empty).

Abbreviations: `D` = `tests/test_detect_visual_bugs.py`, `C` = `tests/test_text_clipped.py`, `S` = `tests/test_selectors.py`.

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
| Fix 1 to Fix 7 of pass 1 | ✅ Done | `148a6fa`, `bcaee50`, `f8939eb` (see Fixes of pass 1, judged) |

`tasks.md` has 55 checked boxes and none open.

---

## Spec-Anchored Acceptance Criteria

Verified by running: the whole suite passes (see Gate Check). The match between each assertion and the spec outcome was verified by reading. Line numbers are those of `f8939eb`.

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
| DVB-11 | first block is text `Found 2 findings in 1 viewport: 1 major, 1 minor.` | `D:115-117` - `first = result.content[0]`, `first.text == "Found 2 findings in 1 viewport: 1 major, 1 minor."` | ✅ PASS (the singular `1 finding` of the Assumptions row has no test: mutant N5) |
| DVB-12 | two equal calls return equal structured content | `D:123` - `detect(BUG) == detect(BUG)` | ✅ PASS |

### P1: Read a Finding

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-13 | the eleven Finding keys; evidence keys `computed`, `measured`, `cropIndex` | `D:130-143` - `set(finding) == {...11 keys}`, `set(finding["evidence"]) == {"computed", "measured", "cropIndex"}` | ✅ PASS |
| DVB-14 | the literal Finding of the `h1` | `S:87-109` - `findings[0] == {...}`; compared field by field with the spec literal, identical | ✅ PASS |
| DVB-15 | severity, then viewport order, then document order; the `h1` before `#badge` | `D:150-153` - severities `== ["major", "minor"]`, `h1` is `findings[0]`, `#badge` is `findings[1]`; document order `D:176-195` - all severities `== {"major"}`, the full list of 16 `text` values of `selectors.html` (the shadow `h3` between the `h2` and the next `div`), and the selectors of `many.html` `== ["#m1", ..., "#m6", "#small"]`; viewport order `D:231-235` | ✅ PASS (closed in pass 2: J09, J10 and C15 are killed) |
| DVB-16 | `#long`: 39 `X` then `…` | `D:161` - `finding["text"] == "X" * 39 + "…"`; the boundary `D:166-169` - the texts of length 40 `== ["X" * 39 + "…", "X" * 40]` | ✅ PASS (closed in pass 2: J01 is killed) |
| DVB-17 | `#spaced`: `XXXXX XXXXX` | `D:217` - `finding["text"] == "XXXXX XXXXX"` | ✅ PASS |
| DVB-18 | every selector of both fixtures resolves in `inspect_element` to the same `box` | `S:115-127` - counts `2` and `16`, `result.is_error is False`, `result.structured_content["box"] == finding["box"]` | ✅ PASS on the named fixtures. ⚠️ No fixture element needs `:nth-of-type` above its own segment, and no id needs CSS escaping (mutants N11, N8) |

### P1: Detect clipped text

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-19 | exactly one Finding for the element | `C:17-19` - `(finding,) = findings_on(BUG, "h1")`, `check == "text-clipped"`, `overflow-x == "hidden"`; pixel confirmation: `C:106` - `findings_on(STRIP, "#bordered") == []`, `C:113-114` - one Finding on `#gap-at-edge`, `overflowPx == 70`, `C:119-120` - one Finding on `#two-colours`, `overflowPx == 50` | ✅ PASS (C13, C14 and V01 are killed). ⚠️ Only the left edge of the padding box is pinned (mutants N1, N2, N4) |
| DVB-20 | one Finding for `#clip`, `overflow-x` equal to `clip` | `C:24-25` - `(finding,) = ...`, `computed["overflow-x"] == "clip"` | ✅ PASS |
| DVB-21 | `#over-8`: `major`, `overflowPx` 8 | `C:31-32` - `severity == "major"`, `overflowPx == 8` | ✅ PASS |
| DVB-22 | `#over-7`, `#over-2`: `minor`, 7 and 2 | `C:37-40` - `severity == "minor"`, `overflowPx == overflow_px` | ✅ PASS |
| DVB-23 | no Finding for `#over-1`; fixture yields exactly 5 | `C:45-46` - `findings_on(..., "#over-1") == []`, `len(findings) == 5` | ✅ PASS |
| DVB-24 to DVB-33 | no Finding for `#fits`, `#wraps`, `#visible`, `#scrolls`, `#ellipsis`, `#sr-only`, `#invisible`, `#blank-tail`, `#ancestor` and its child, `#rtl` | `C:80-93` - `reported(client, near_misses) == []`; and `C:74` - `findings == []` for the whole fixture | ✅ PASS |
| DVB-69 | no Finding for `#scaled`, `#stretched`, `#widened`, `#turned`, `#in-scaled` | `C:99-100` - `resized = ("#scaled", "#stretched", "#widened", "#turned", "#in-scaled")`, `reported(client, resized) == []`; and `C:74` | ✅ PASS (closed in pass 2: `#widened` differs in width only and C11 is killed) |
| DVB-70 | `#moved`: `box` `{70, 410, 150, 30}`, `overflowPx` 50 | `C:53-55` - `(finding,) = ...`, `finding["box"] == {"x": 70, "y": 410, "w": 150, "h": 30}`, `overflowPx == 50` | ✅ PASS |

### P1: Stable selectors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-34 | `[data-testid="save"]` | `S:24` - `== '[data-testid="save"]'` | ✅ PASS |
| DVB-35 | `#first-row` | `S:28` - `== "#first-row"` | ✅ PASS |
| DVB-36 | `button[aria-label="Close dialog"]` | `S:34` - `== 'button[aria-label="Close dialog"]'` | ✅ PASS |
| DVB-37 | `[role="tab"][aria-label="Settings"]` | `S:40` - `== '[role="tab"][aria-label="Settings"]'`; the digit bound `S:46-47` - `== 'div[aria-label="Step"]'` for `step-123`, `== "#col-12"` for `col-12` | ✅ PASS (J03 is killed). ⚠️ Every digit-heavy id has its digits adjacent (mutant N7) |
| DVB-38 | `body > main > p:nth-of-type(2)` | `S:57` - `== "body > main > p:nth-of-type(2)"` | ✅ PASS |
| DVB-39 | each its CSS path, the two differ | `S:65-66` - `== "body > main > button:nth-of-type(2)"`, `== "body > main > button:nth-of-type(3)"` | ✅ PASS |
| DVB-40 | `body > main > h2` | `S:70` - `== "body > main > h2"` | ✅ PASS |
| DVB-41 | `[data-testid="card"] > h3` | `S:76` - `== '[data-testid="card"] > h3'`; uniqueness across shadow trees `S:53` - `== "#outside"` | ✅ PASS (J09 is killed) |
| DVB-42 | `[data-testid="say \"hi\""]` | `S:80` - `== '[data-testid="say \\"hi\\""]'` | ✅ PASS |

### P1: Bounded crops

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-43 | one text block, then exactly min(N, 5) `image/png` blocks | `D:256-260` - for N = 2 and N = 7: `isinstance(result.content[0], TextContent)`, `result.content[1:] == images(result)`, mime types `== ["image/png"] * crops`; N = 0 at `C:75` | ✅ PASS |
| DVB-44 | `cropIndex` `0, 1, 2, 3, 4, null, null`; last is the `minor` of `#small` | `D:265-275` - list `== [0, 1, 2, 3, 4, None, None]`, `findings[6]["severity"] == "minor"`, `findings_on(MANY, "#small") == [findings[6]]` | ✅ PASS |
| DVB-45 | each image 182×62, text colour of its own element at (20, 31) | `D:294-295` - `crop.size == (182, 62)`, `crop.getpixel((20, 31)) == text_color` for `#m1` to `#m5`; second viewport `D:208-211` - `crop.size == (227, 62)`, `getpixel((208, 31)) == (0, 0, 0)`, `getpixel((213, 31)) == (255, 255, 255)` for `#half` at 390×844 | ✅ PASS (closed in pass 2: T03 is killed) |

### P1: Several viewports

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-46 | two captures in order; 3 Findings in the given order; `#half` `overflowPx` 5; the text block | `D:226-243` - `captures == [DESKTOP, MOBILE entries]`, `(viewport, severity)` list, `on == [[findings[0]], [findings[1]], [findings[2]]]`, `overflowPx == 5`, `texts(result) == ["Found 3 findings in 2 viewports: 2 major, 1 minor."]` | ✅ PASS |
| DVB-47 | `isError: false`, `captures[0].stabilized` false | `D:249-250` - `detect(...)` (asserts `is_error is False`, `tests/helpers.py:34`), `stabilized is False` | ✅ PASS |
| DVB-48 | repeated viewport captured once; same findings | `D:301-303` - `twice["captures"] == [{MOBILE, True}]`, `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]` | ✅ PASS. ⚠️ The repeat is adjacent, so "collapsed to their first occurrence" is not told from "to their last" (mutant N6) |
| DVB-49 | repeated check name: same findings | `D:309-310` - `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]` | ✅ PASS |

### P1: Clear errors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-50 | `isError: true`, `Unknown check "nope". Valid checks: text-clipped.` | `D:316,322` - `result.is_error is True`, `'Unknown check "nope". Valid checks: text-clipped.' in text` | ✅ PASS for `["nope"]`. ⚠️ An unknown name after a valid one has no test (mutant N10) |
| DVB-51 | the unknown-Check error, not the Chromium one | `D:330-331` - same text `in text`, `"Could not launch Chromium" not in text` | ✅ PASS |
| DVB-52 | error names `checks` | `D:335` - `"checks" in error_text(...)` | ✅ PASS |
| DVB-53 | error names `viewports` | `D:339` - `"viewports" in error_text(...)` | ✅ PASS |
| DVB-54 | error names the offending field | `D:343-346` - `field in text` for `width` and `height` at 0 | ✅ PASS |
| DVB-55 | error names `url` | `D:350` - `"url" in error_text(client, {})` | ✅ PASS |
| DVB-56 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `D:355` - that text `in text` | ✅ PASS |
| DVB-57 | `Could not load ` + URL | `D:360` - `f"Could not load {url}" in error_text(...)` | ✅ PASS |
| DVB-58 | `Could not launch Chromium` and `playwright install chromium` | `D:367-368` - both `in text` | ✅ PASS |
| DVB-59 | `Timed out after Ns` within 1s of the timeout; next call answered | `D:385-387` - `"Timed out after 4s" in text`, `4 <= elapsed < 5`, `len(detect(BUG)["findings"]) == 2` | ✅ PASS |

### P2: Check contract, configuration and documents (file evidence, by reading)

| ID | Spec-defined outcome | Evidence | Result |
| -- | -------------------- | -------- | ------ |
| DVB-60 | own module under a Checks package; Capture in, Findings out | `src/squint_mcp/checks/text_clipped.py:118` - `def check(capture: Capture) -> list[Finding]` | ✅ PASS |
| DVB-61 | only the Capture module imports `playwright` | grep of `src/`: the only imports are `src/squint_mcp/capture.py:12-14` | ✅ PASS |
| DVB-62 | one registry | `src/squint_mcp/checks/__init__.py:14` - `CHECKS: dict[str, Check] = {"text-clipped": text_clipped.check}`; resolved at `src/squint_mcp/tools/detect_visual_bugs.py:71,74,75,99` and nowhere else | ✅ PASS |
| DVB-63 | page JavaScript in `.js` files only | `src/squint_mcp/capture.py:20-21` reads `js/stabilize.js` and `js/collect_elements.js`; the only `evaluate` calls (`capture.py:97,112`) pass those; no `=>`, `function(` or `document.` in any `.py` under `src/` | ✅ PASS |
| DVB-64 | crop limit 5, excerpt 40, minimum overflow 2, major threshold 8, each with a cited source | `src/squint_mcp/config.py:54-55`, `57-58`, `60-62`, `64-66` | ✅ PASS |
| DVB-65 | no dependency slice 2 did not declare | `git diff 389230a..f8939eb -- pyproject.toml uv.lock` is empty | ✅ PASS |
| DVB-66 | `inspect_element` tests pass without any change to their assertions other than the exact tool list of DVB-01 | all pass; `git diff 389230a..f8939eb -- tests/test_inspect_element.py` changes one assertion, `tests/test_inspect_element.py:421`, the exact tool list, from two names to three | ✅ PASS (the gap of pass 1 is closed by the new wording of DVB-66 and of the CAP-01 Assumptions row, which names both tests) |
| DVB-67 | `Unreleased` lists the tool and the Check; README table lists the tool | `CHANGELOG.md:14-15` under `## [Unreleased]` (`CHANGELOG.md:7`); `README.md:17` | ✅ PASS |
| DVB-68 | ROADMAP shows slice 3 `concluída` once the Verifier reports PASS | Closing step of the orchestrator, made only after a PASS verdict. At `f8939eb`, `docs/ROADMAP.md:19,73` read `pendente`, as expected before that step | ⏳ Pending on verdict (not a failure) |

**Status**: ❌ Gaps present. 69/69 testable requirements have an assertion on the spec-defined outcome (DVB-68 pending on verdict); 0 spec-precision gaps open (the 2 of pass 1 are closed); 9 surviving mutants, all found in pass 2.

### Spec-precision gaps of pass 1, re-judged

1. **DVB-66 against DVB-01**: closed. DVB-66 now excepts the exact tool list of DVB-01, and the CAP-01 Assumptions row names both rewritten assertions (`tests/test_ping.py` and `test_server_answers_ping_while_chromium_cannot_be_launched`). The diff of `tests/test_inspect_element.py` holds that one change.
2. **DVB-69, "in width or in height"**: closed. DVB-69 names `#widened` (`transform: scaleX(1.5)`, height unchanged), the fixture has it and `C:99` lists it. Verified by running: mutant C11 (width clause removed) is killed.

### Observations (not gaps, for the maintainer)

- The fixture list of the spec still describes `selectors.html` as "one clipped element per selector case of DVB-34 to DVB-42". It now holds four more clipped elements (16 Findings). Each new one is anchored to an Assumptions row, so no test is unclaimed; the description is behind.
- `#two-colours` pins a Finding on text nobody can see (transparent text over a two-band background). That is the rule as written ("painted in more than one colour"), and the spec's fixture list names it. It is in tension with the rationale of the same row ("Rejects ... hidden text"): the rule rejects hidden text only over a flat background.
- Pass 1 recorded that "names the first unknown name in the order given" cannot be observed with one Check. It can: two unknown names, or an unknown one after a valid one (see mutant N10). Only "lists the valid names alphabetically" is unobservable today.

---

## Fixes of pass 1, judged

| Fix | Done when | Evidence | Met? |
| --- | --------- | -------- | ---- |
| 1 | T03 killed | `D:198-211`, anchored to DVB-45. Run in pass 2: T03 dies on `test_a_crop_is_cut_from_the_pixels_of_its_own_viewport` | ✅ |
| 2 | C11 killed; `#widened` in fixture, test and DVB-69 | `tests/fixtures/text-clipped-clean.html:82-85,136`, `C:99`, spec DVB-69. Run: C11 dies on `C:74` (a Finding on the clean fixture) | ✅ |
| 3 | J09 and J10 killed; C15 dies on an order assertion | `D:172-195` (Assumptions: Finding order), `S:50-53` (Assumptions: Uniqueness). Run: J10 dies on `D:178`; J09 dies on `S:53`; C15, run without fail-fast, fails 3 tests: `D:166` and `D:178` (both list-equality assertions on order) and the crop test that killed it in pass 1 | ✅ |
| 4 | J01 killed | `D:164-169`, `tests/fixtures/selectors.html:88`, anchored to DVB-16 / Assumptions: `text` excerpt. Run: J01 dies on `D:166` | ✅ |
| 5 | C13, C14 and V01 killed | `tests/fixtures/text-clipped-strip.html`, `C:103-129`, anchored to Assumptions: pixel confirmation; the fixture is named in the spec. Run: C14 dies on `C:106`, C13 on `C:113`, V01 on `C:119` | ✅ |
| 6 | J03 killed | `S:43-47`, `tests/fixtures/selectors.html:90-91`, anchored to Assumptions: ids that look generated. Run: J03 dies on `S:46`. `col-12` also guards the other side (a bound of 2) | ✅ |
| 7 | Spec wording of DVB-66, CAP-01 row, DVB-69 | `git diff 2973d07..f8939eb -- .specs` | ✅ |

Judgement of the new tests (by reading the diff `2973d07..f8939eb`):

- No assertion was deleted or weakened. The only changed assertions are the Finding count of `selectors.html` (12 to 16, `S:115`) and the `resized` tuple (one element added, `C:99`), both stricter or equal.
- Every new test has a spec anchor (listed in the table above). None mirrors the implementation: each asserts a value that follows from the fixture geometry or from an Assumptions row.
- `C:122-129` asserts through `inspect_element` that `#two-colours` paints exactly two colours. It is a guard on the fixture's premise (lesson L-023), not a behaviour of this feature; accepted.
- V01 and C13 die on the unpacking `(finding,) = ...`, which is the test's own "exactly one Finding" assertion, not an accident.
- Three new tests would still pass under a plausible wrong implementation: `S:46-47` passes if only adjacent digits are counted (N7); `C:106` passes if the strip is bounded by the border box on the right, top and bottom (N1, N2); `D:301-303`, unchanged from pass 1, passes if a repeated viewport is collapsed to its last place (N6).

---

## Discrimination Sensor

**Pass 2 scratch**: a temporary `git worktree` at `f8939eb` in `C:\tmp\sq-wt`, with its own `.venv` from `uv sync`. `import squint_mcp` there printed `C:\tmp\sq-wt\src\squint_mcp\__init__.py`. The unmutated baseline passed there (59 passed in the three feature test files). Each mutant was applied alone, `git diff --stat` confirmed it, the relevant test files ran, and the file was restored (`git status --porcelain` of the worktree empty after each). `git status --porcelain` of the real tree was empty before and is byte-identical after; the worktree is removed and `git worktree list` shows only the real tree.

The 30 mutants of pass 1 marked "run in pass 1" were not re-run: no file under `src/` changed since, and no assertion that killed them was removed or weakened. Their line numbers still hold.

| # | File:line | Mutation | Killed? | Run |
| - | --------- | -------- | ------- | --- |
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
| C13 | `text_clipped.py:65` | `left = max(padding_left, right - font_size)` → `left = right - 1` | ✅ Killed (`C:113`; survived pass 1) | pass 2 |
| C14 | `text_clipped.py:63` | `padding_left = element.box.x + border.left` → `element.box.x` | ✅ Killed (`C:106`; survived pass 1) | pass 2 |
| C15 | `text_clipped.py:121` | `capture.elements` → `reversed(capture.elements)` | ✅ Killed on order assertions `D:166`, `D:178` (in pass 1 only by a `TypeError`) | pass 2 |
| V01 | `src/squint_mcp/vision.py:48` | `getcolors(maxcolors=1)` → `getcolors(maxcolors=2)` | ✅ Killed (`C:119`; survived pass 1) | pass 2 |
| T01 | `src/squint_mcp/tools/detect_visual_bugs.py:102` | removed the severity sort | ✅ Killed | pass 1 |
| T02 | `config.py:55` | `MAX_CROPS = 5` → `4` | ✅ Killed | pass 1 |
| T03 | `detect_visual_bugs.py:105` | `crop_png(captured.pixels, ...)` → `crop_png(captures[0].pixels, ...)` | ✅ Killed (`D:211`; survived pass 1) | pass 2 |
| T04 | `detect_visual_bugs.py:110` | `crop_index = index` → `index + 1` | ✅ Killed | pass 1 |
| T05 | `detect_visual_bugs.py:82` | removed the viewport dedup | ✅ Killed | pass 1 |
| T06 | `detect_visual_bugs.py:71` | `list(dict.fromkeys(checks or CHECKS))` → `list(checks or CHECKS)` | ✅ Killed | pass 1 |
| T07 | `detect_visual_bugs.py:87-92` | one timeout per viewport instead of one for the call | ✅ Killed | pass 1 |
| T08 | `detect_visual_bugs.py:71` | browser launched before the Check names are validated | ✅ Killed | pass 1 |
| T09 | `detect_visual_bugs.py:43` | summary severities in reverse order | ✅ Killed | pass 1 |
| T10 | `detect_visual_bugs.py:97` | `for captured in captures` → `reversed(captures)` | ✅ Killed | pass 1 |
| J01 | `src/squint_mcp/js/collect_elements.js:79` | `flat.length > textLimit` → `>=` | ✅ Killed (`D:166`; survived pass 1) | pass 2 |
| J02 | `collect_elements.js:79` | `slice(0, textLimit - 1)` → `slice(0, textLimit)` | ✅ Killed | pass 1 |
| J03 | `collect_elements.js:33` | digits `.length >= 3` → `>= 4` | ✅ Killed (`S:46`; survived pass 1) | pass 2 |
| J04 | `collect_elements.js:33` | removed the `[^A-Za-z0-9_-]` rule | ✅ Killed | pass 1 |
| J05 | `collect_elements.js:63` | id tried before `data-testid` | ✅ Killed | pass 1 |
| J06 | `collect_elements.js:63` | `roleLabel \|\| tagLabel` → `tagLabel \|\| roleLabel` | ✅ Killed | pass 1 |
| J07 | `collect_elements.js:64` | `matches.get(selector) === 1` → `>= 1` | ✅ Killed | pass 1 |
| J08 | `collect_elements.js:59` | `twins.length > 1` → `> 0` | ✅ Killed | pass 1 |
| J09 | `collect_elements.js:41` | removed `if (element.shadowRoot) walk(element.shadowRoot);` | ✅ Killed (`S:53`; survived pass 1) | pass 2 |
| J10 | `collect_elements.js:133` | removed `.sort((a, b) => order.get(a) - order.get(b))` | ✅ Killed (`D:178`; survived pass 1) | pass 2 |
| J11 | `collect_elements.js:125` | `node.nodeValue.trim() !== ""` → `node.nodeValue !== ""` | ✅ Killed | pass 1 |
| J12 | `collect_elements.js:73` | removed the host selector of a shadow path | ✅ Killed | pass 1 |
| J13 | `collect_elements.js:17` | attribute value not escaped | ✅ Killed | pass 1 |
| J14 | `collect_elements.js:78` | whitespace not collapsed | ✅ Killed | pass 1 |
| N1 | `text_clipped.py:64` | `right = padding_left + element.client_width` → `right = element.box.x + element.box.w` (strip ends at the border box) | ❌ Survived (pixel confirmation: right edge of the padding box) | pass 2, new |
| N2 | `text_clipped.py:68,70` | `y=element.box.y + border.top` → `element.box.y`; `h=element.box.h - border.top - border.bottom` → `element.box.h` | ❌ Survived (pixel confirmation: top and bottom edges of the padding box) | pass 2, new |
| N3 | `text_clipped.py:65` | `right - font_size` → `right - 2 * font_size` | ✅ Killed (`C:106`) | pass 2, new |
| N4 | `text_clipped.py:65` | `left = max(padding_left, right - font_size)` → `left = right - font_size` (clamp removed) | ❌ Survived (pixel confirmation: strip stays inside a box narrower than one `font-size`) | pass 2, new |
| N5 | `detect_visual_bugs.py:46` | `Found {_count(len(findings), 'finding')}` → `Found {len(findings)} findings` | ❌ Survived (Assumptions: text summary, `finding` singular for 1) | pass 2, new |
| N6 | `detect_visual_bugs.py:82` | viewport dedup keeps the place of the last occurrence instead of the first | ❌ Survived (Assumptions: duplicate entries, DVB-48) | pass 2, new |
| N7 | `collect_elements.js:33` | `id.replace(/\D/g, "").length >= 3` → `/\d{3}/.test(id)` (adjacent digits only) | ❌ Survived (Assumptions: ids that look generated, `css-1a2b3c`) | pass 2, new |
| N8 | `collect_elements.js:25` | `` `#${CSS.escape(element.id)}` `` → `` `#${element.id}` `` | ❌ Survived (Assumptions: selector quoting; DVB-18) | pass 2, new |
| N9 | `detect_visual_bugs.py:121` | image blocks emitted in reverse order | ✅ Killed (`D:208`) | pass 2, new |
| N10 | `detect_visual_bugs.py:73` | `for name in names` → `for name in names[:1]` (only the first name is validated) | ❌ Survived (DVB-50; Assumptions: unknown Check) | pass 2, new |
| N11 | `collect_elements.js:70` | `segments.unshift(segment(node))` → `segments.unshift(node.localName)` (no `:nth-of-type` above the element's own segment) | ❌ Survived (Assumptions: CSS path; DVB-18, selector unique on the page) | pass 2, new |

**Sensor depth**: expanded (first Check and the Finding contract): 51 distinct mutations across the Check (19), `vision.is_flat` (1), the tool (14) and the collector (17).
**Pass 2 runs**: 21 mutants run. 10 re-runs (the 9 survivors of pass 1 and C15): 10/10 killed. 11 new: 2 killed, 9 survived.
**Carried over from pass 1, not re-run**: 30 killed.
**Result**: 42/51 killed, 9 survived - FAIL ❌

That each survivor changes behaviour was inferred by reading, not by a probe: N1 and N2 differ on any element with a right, top or bottom border; N4 on a box narrower than its `font-size`; N5 on a call with exactly one Finding; N6 on `[A, B, A]`; N7 on an id such as `a1b2c3`; N8 on an id such as `2col` (the selector `#2col` is invalid CSS); N10 on `["text-clipped", "nope"]`; N11 on two sibling containers of the same tag that each hold an attribute-less clipped element (both get the same selector). The unmutated source handles all of these as the spec says, by reading.

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
| Tests discriminate the behaviour they claim | ❌ 9 surviving mutants |

---

## Edge Cases

- [x] Clipped element inside an open shadow root is reported (DVB-41): `S:76`, and it is one of the 16 Findings of `S:115`.
- [x] Only whitespace overflows: no Finding (DVB-31): `C:88,93`.
- [x] `data-testid` holding a double quote is escaped (DVB-42): `S:80`.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`
- **Result** (real tree at `f8939eb`): pyright 0 errors (exit 0); ruff check passed (exit 0); ruff format 62 files already formatted (exit 0); pytest 120 passed, 0 failed, 0 skipped in 137.42s (exit 0)
- **Test count before feature**: 61 (`389230a`)
- **Test count after feature**: 120 (112 at pass 1)
- **Delta**: +59 new tests (+8 since pass 1)
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed; no assertion weakened.

---

## Fix Plans

All are tests and fixtures. No source change is expected: the source already behaves as the spec says in each case. Every new fixture element must also be named in the fixture list of `spec.md`.

### Fix 8: A CSS path can match two elements when an ancestor has a same-tag sibling (N11)

- **Root cause**: every fixture element sits directly under `body > main`, so `:nth-of-type` is only ever needed on the last segment.
- **Fix task**: in `tests/fixtures/selectors.html` add two sibling containers of the same tag under `main` (for example two `section`), each holding one attribute-less clipped element of the same tag with its own glyph count. In `tests/test_selectors.py` assert the two selectors (`body > main > section:nth-of-type(1) > h4` and `...(2) > h4`) and update the count at `S:115`. Done when mutant N11 (`collect_elements.js:70`) is killed.
- **Priority**: Major (Goal: every Finding selector is unique on the page)

### Fix 9: An id that needs CSS escaping is unprotected (N8)

- **Root cause**: every id that reaches the selector is a plain identifier.
- **Fix task**: add to `selectors.html` a clipped element whose only stable attribute is an id that starts with a digit and has fewer than three (for example `2col`); assert its selector is the escaped form (`#\32 col`); the loop at `S:115-127` then proves it resolves. Done when mutant N8 (`collect_elements.js:25`) is killed.
- **Priority**: Major (DVB-18)

### Fix 10: Only the left edge of the padding box is pinned (N1, N2)

- **Root cause**: `#bordered` has a left border only.
- **Fix task**: add to `tests/fixtures/text-clipped-strip.html` an element with a border on the right, top and bottom (or all four sides), glyphs that end before the strip and blank overflow; assert no Finding for it in `tests/test_text_clipped.py`. Done when mutants N1 (`text_clipped.py:64`) and N2 (`text_clipped.py:68,70`) are killed.
- **Priority**: Major (a false Finding on any bordered box; lesson L-022 applied to one edge only)

### Fix 11: An unknown Check after a valid one is unprotected (N10)

- **Root cause**: DVB-50 and DVB-51 are tested with `["nope"]` alone.
- **Fix task**: in `tests/test_detect_visual_bugs.py`, with `client_without_chromium`, call `checks=["text-clipped", "nope"]` and assert the `Unknown check "nope"` text and no Chromium error; call `checks=["zzz", "nope"]` and assert the message names `zzz`. Done when mutant N10 (`detect_visual_bugs.py:73`) is killed.
- **Priority**: Minor

### Fix 12: The singular `1 finding` is unprotected (N5)

- **Fix task**: assert `texts(result) == ["Found 1 finding in 1 viewport: 1 major."]` for `responsive.html` at the default viewport (only `#fixed` is cut there). Done when mutant N5 (`detect_visual_bugs.py:46`) is killed.
- **Priority**: Minor

### Fix 13: "Collapsed to their first occurrence" is unprotected (N6)

- **Fix task**: call `responsive.html` with `viewports=[DESKTOP, MOBILE, DESKTOP]` and assert `captures` is `[DESKTOP, MOBILE]` in that order. Done when mutant N6 (`detect_visual_bugs.py:82`) is killed.
- **Priority**: Minor

### Fix 14: Three digits that are not adjacent are unprotected (N7)

- **Fix task**: add to `selectors.html` a clipped element with an id such as `a1b2c3` and an `aria-label`; assert it falls through to the `aria-label` selector. Done when mutant N7 (`collect_elements.js:33`) is killed.
- **Priority**: Minor

### Fix 15: The strip of a box narrower than one font-size is unprotected (N4)

- **Fix task**: add to `text-clipped-strip.html` a box narrower than 20px whose visible part is blank (leading spaces kept by `white-space: pre`, then a glyph that overflows) with ink of another element right before its left edge; assert no Finding for it. Done when mutant N4 (`text_clipped.py:65`) is killed.
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| DVB-01 to DVB-10, DVB-12 to DVB-14, DVB-17, DVB-20 to DVB-36, DVB-38 to DVB-44, DVB-46, DVB-47, DVB-49, DVB-51 to DVB-65, DVB-67, DVB-70 | Implemented | ✅ Verified |
| DVB-15, DVB-16, DVB-45, DVB-69 | ❌ Needs Fix (pass 1) | ✅ Verified |
| DVB-66 | ⚠️ Spec-precision gap (pass 1) | ✅ Verified |
| DVB-18 | Implemented | ❌ Needs Fix (tests: Fix 8, Fix 9) |
| DVB-19 | Implemented | ❌ Needs Fix (tests: Fix 10, Fix 15) |
| DVB-50 | Implemented | ❌ Needs Fix (tests: Fix 11) |
| DVB-11 | Implemented | ❌ Needs Fix (tests: Fix 12) |
| DVB-48 | Implemented | ❌ Needs Fix (tests: Fix 13) |
| DVB-37 | Implemented | ❌ Needs Fix (tests: Fix 14) |
| DVB-68 | In Tasks | ⏳ Pending on verdict |

Each "Needs Fix" requirement passes on its named fixture; what is missing is the protection of an Assumptions row that backs it.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 69/69 testable requirements matched the spec outcome | 0 spec-precision gaps open | DVB-68 pending on verdict
**Sensor**: 42/51 mutations killed, 9 survived (pass 2 ran 21: 10 re-runs all killed, 11 new with 9 survivors; 30 kills carried over from pass 1)
**Gate**: 120 passed, 0 failed, 0 skipped; pyright, ruff check and ruff format clean

**What works**: the whole flow Capture → Check → Finding[] through `detect_visual_bugs`. Everything pass 1 found unprotected is now protected: the crop's own viewport, the width clause of the resize rule, document order and shadow-tree walking, the 40-character boundary, the left edge and the width of the edge strip, "more than one colour", and the three-digit bound.

**Issues found**: no source defect. Nine further behaviours the spec states are unprotected by tests (Fix 8 to Fix 15). Three matter most: selector uniqueness when an ancestor has a same-tag sibling, id escaping, and the other three edges of the padding box.

**Next steps**: route Fix 8 to Fix 15 to an implementer, then re-verify (pass 3, the last before escalating to the user).
