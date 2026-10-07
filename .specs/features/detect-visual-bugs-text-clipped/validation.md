# detect_visual_bugs + text-clipped Validation

**Date**: 2026-10-07
**Spec**: `.specs/features/detect-visual-bugs-text-clipped/spec.md`
**Diff range**: `389230a..c6e124c` (10 commits, branch `feat/detect-visual-bugs-text-clipped`)
**Verifier**: independent sub-agent (author ≠ verifier)

**Verdict**: ❌ FAIL

Every requirement is implemented and every assertion targets the outcome the spec defines; the gate is green. The verdict is FAIL because the discrimination sensor left 9 of 40 mutants alive: the tests do not protect those behaviours. No defect was found in the source. The fixes are tests and fixtures, plus two spec clarifications.

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
| T6 | ✅ Done | `e850693`; corrects the `h1` rule of `text-clipped-bug.html` (see Author's recorded facts) |
| T7 | ✅ Done | `d4e0a46` |
| T8 | ✅ Done | `08afc15` |
| T9 | ✅ Done | `c6e124c` |

`tasks.md` has 55 checked boxes and none open. `179bc3f` only reformats a code block of `design.md`.

---

## Spec-Anchored Acceptance Criteria

Verified by running: the whole suite passes (see Gate Check). The match between each assertion and the spec outcome was verified by reading.

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
| DVB-10 | `isError: false`, `findings == []`, no image, text `No findings in 1 viewport.` | `C:71-75` - `is_error is False`, `findings == []`, `images(result) == []`, `texts(result) == ["No findings in 1 viewport."]` | ✅ PASS |
| DVB-11 | first block is text `Found 2 findings in 1 viewport: 1 major, 1 minor.` | `D:115-117` - `first = result.content[0]`, `first.text == "Found 2 findings in 1 viewport: 1 major, 1 minor."` | ✅ PASS |
| DVB-12 | two equal calls return equal structured content | `D:123` - `detect(BUG) == detect(BUG)` | ✅ PASS |

### P1: Read a Finding

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-13 | the eleven Finding keys; evidence keys `computed`, `measured`, `cropIndex` | `D:130-143` - `set(finding) == {...11 keys}`, `set(finding["evidence"]) == {"computed", "measured", "cropIndex"}` | ✅ PASS |
| DVB-14 | the literal Finding of the `h1` | `S:74-96` - `findings[0] == {...}`; compared field by field with the spec literal, identical | ✅ PASS |
| DVB-15 | severity, then viewport order, then document order; the `h1` before `#badge` | `D:150-153` - severities `== ["major", "minor"]`, `h1` is `findings[0]`, `#badge` is `findings[1]`; viewport order at `D:181-191` | ✅ PASS on the named fixture. ⚠️ The document-order tie-breaker has no direct assertion (mutants J09, J10 survive; C15 dies only through a `TypeError` in the crop test) |
| DVB-16 | `#long`: 39 `X` then `…` | `D:161` - `finding["text"] == "X" * 39 + "…"` | ✅ PASS on the named fixture. ⚠️ No text of exactly 40 characters (mutant J01 survives) |
| DVB-17 | `#spaced`: `XXXXX XXXXX` | `D:167` - `finding["text"] == "XXXXX XXXXX"` | ✅ PASS |
| DVB-18 | every selector of both fixtures resolves in `inspect_element` to the same `box` | `S:102-114` - counts `2` and `12`, `result.is_error is False`, `result.structured_content["box"] == finding["box"]` | ✅ PASS |

### P1: Detect clipped text

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-19 | exactly one Finding for the element | `C:16-18` - `(finding,) = findings_on(BUG, "h1")`, `check == "text-clipped"`, `overflow-x == "hidden"` | ✅ PASS |
| DVB-20 | one Finding for `#clip`, `overflow-x` equal to `clip` | `C:23-24` - `(finding,) = ...`, `computed["overflow-x"] == "clip"` | ✅ PASS |
| DVB-21 | `#over-8`: `major`, `overflowPx` 8 | `C:30-31` - `severity == "major"`, `overflowPx == 8` | ✅ PASS |
| DVB-22 | `#over-7`, `#over-2`: `minor`, 7 and 2 | `C:36-39` - `severity == "minor"`, `overflowPx == overflow_px` | ✅ PASS |
| DVB-23 | no Finding for `#over-1`; fixture yields exactly 5 | `C:44-45` - `findings_on(..., "#over-1") == []`, `len(findings) == 5` | ✅ PASS |
| DVB-24 to DVB-33 | no Finding for `#fits`, `#wraps`, `#visible`, `#scrolls`, `#ellipsis`, `#sr-only`, `#invisible`, `#blank-tail`, `#ancestor` and its child, `#rtl` | `C:79-92` - `reported(client, near_misses) == []`; and `C:73` - `findings == []` for the whole fixture | ✅ PASS |
| DVB-69 | no Finding for `#scaled`, `#stretched`, `#turned`, `#in-scaled` | `C:98-99` - `reported(client, resized) == []`; and `C:73` | ✅ PASS on the named fixtures. ⚠️ Spec-precision gap: none of the four differs in width only (mutant C11 survives) |
| DVB-70 | `#moved`: `box` `{70, 410, 150, 30}`, `overflowPx` 50 | `C:52-54` - `(finding,) = ...`, `finding["box"] == {"x": 70, "y": 410, "w": 150, "h": 30}`, `overflowPx == 50` | ✅ PASS |

### P1: Stable selectors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-34 | `[data-testid="save"]` | `S:24` - `== '[data-testid="save"]'` | ✅ PASS |
| DVB-35 | `#first-row` | `S:28` - `== "#first-row"` | ✅ PASS |
| DVB-36 | `button[aria-label="Close dialog"]` | `S:34` - `== 'button[aria-label="Close dialog"]'` | ✅ PASS |
| DVB-37 | `[role="tab"][aria-label="Settings"]` | `S:40` - `== '[role="tab"][aria-label="Settings"]'` | ✅ PASS (the id has five digits; the three-digit bound is not pinned, mutant J03) |
| DVB-38 | `body > main > p:nth-of-type(2)` | `S:44` - `== "body > main > p:nth-of-type(2)"` | ✅ PASS |
| DVB-39 | each its CSS path, the two differ | `S:52-53` - `== "body > main > button:nth-of-type(2)"`, `== "body > main > button:nth-of-type(3)"` | ✅ PASS |
| DVB-40 | `body > main > h2` | `S:57` - `== "body > main > h2"` | ✅ PASS |
| DVB-41 | `[data-testid="card"] > h3` | `S:63` - `== '[data-testid="card"] > h3'` | ✅ PASS |
| DVB-42 | `[data-testid="say \"hi\""]` | `S:67` - `== '[data-testid="say \\"hi\\""]'` | ✅ PASS |

### P1: Bounded crops

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-43 | one text block, then exactly min(N, 5) `image/png` blocks | `D:206-210` - for N = 2 and N = 7: `isinstance(result.content[0], TextContent)`, `result.content[1:] == images(result)`, mime types `== ["image/png"] * crops`; N = 0 at `C:74` | ✅ PASS |
| DVB-44 | `cropIndex` `0, 1, 2, 3, 4, null, null`; last is the `minor` of `#small` | `D:215-225` - list `== [0, 1, 2, 3, 4, None, None]`, `findings[6]["severity"] == "minor"`, `findings_on(MANY, "#small") == [findings[6]]` | ✅ PASS |
| DVB-45 | each image 182×62, text colour of its own element at (20, 31) | `D:244-245` - `crop.size == (182, 62)`, `crop.getpixel((20, 31)) == text_color` for `#m1` to `#m5` | ✅ PASS on `many.html`. ⚠️ Only one viewport: a crop cut from another viewport's pixels is not detected (mutant T03 survives) |

### P1: Several viewports

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-46 | two captures in order; 3 Findings in the given order; `#half` `overflowPx` 5; the text block | `D:176-193` - `captures == [DESKTOP, MOBILE entries]`, `(viewport, severity)` list, `on == [[findings[0]], [findings[1]], [findings[2]]]`, `overflowPx == 5`, `texts(result) == ["Found 3 findings in 2 viewports: 2 major, 1 minor."]` | ✅ PASS |
| DVB-47 | `isError: false`, `captures[0].stabilized` false | `D:199-200` - `detect(...)` (asserts `is_error is False`, `tests/helpers.py:34`), `stabilized is False` | ✅ PASS |
| DVB-48 | repeated viewport captured once; same findings | `D:251-253` - `twice["captures"] == [{MOBILE, True}]`, `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]` | ✅ PASS |
| DVB-49 | repeated check name: same findings | `D:259-260` - `len(once["findings"]) == 2`, `twice["findings"] == once["findings"]` | ✅ PASS |

### P1: Clear errors

| ID | Spec-defined outcome | `file:line` + assertion | Result |
| -- | -------------------- | ----------------------- | ------ |
| DVB-50 | `isError: true`, `Unknown check "nope". Valid checks: text-clipped.` | `D:266,272` - `result.is_error is True`, `'Unknown check "nope". Valid checks: text-clipped.' in text` | ✅ PASS |
| DVB-51 | the unknown-Check error, not the Chromium one | `D:280-281` - same text `in text`, `"Could not launch Chromium" not in text` | ✅ PASS |
| DVB-52 | error names `checks` | `D:285` - `"checks" in error_text(...)` | ✅ PASS |
| DVB-53 | error names `viewports` | `D:289` - `"viewports" in error_text(...)` | ✅ PASS |
| DVB-54 | error names the offending field | `D:293-296` - `field in text` for `width` and `height` at 0 | ✅ PASS |
| DVB-55 | error names `url` | `D:300` - `"url" in error_text(client, {})` | ✅ PASS |
| DVB-56 | `Unsupported URL scheme "ftp"; use http://, https:// or file://.` | `D:305` - that text `in text` | ✅ PASS |
| DVB-57 | `Could not load ` + URL | `D:310` - `f"Could not load {url}" in error_text(...)` | ✅ PASS |
| DVB-58 | `Could not launch Chromium` and `playwright install chromium` | `D:317-318` - both `in text` | ✅ PASS |
| DVB-59 | `Timed out after Ns` within 1s of the timeout; next call answered | `D:335-337` - `"Timed out after 4s" in text`, `4 <= elapsed < 5`, `len(detect(BUG)["findings"]) == 2` | ✅ PASS |

The real error texts were read by calling the tool (read-only): each validation error names only its own field (`url`, `checks`, `viewports`, `viewports.0.width`, `viewports.0.height`), so the substring assertions of DVB-52 to DVB-55 discriminate.

### P2: Check contract, configuration and documents (file evidence, by reading)

| ID | Spec-defined outcome | Evidence | Result |
| -- | -------------------- | -------- | ------ |
| DVB-60 | own module under a Checks package; Capture in, Findings out | `src/squint_mcp/checks/text_clipped.py:118` - `def check(capture: Capture) -> list[Finding]` | ✅ PASS |
| DVB-61 | only the Capture module imports `playwright` | grep of `src/`: the only imports are `src/squint_mcp/capture.py:12-14` | ✅ PASS |
| DVB-62 | one registry | `src/squint_mcp/checks/__init__.py:14` - `CHECKS: dict[str, Check] = {"text-clipped": text_clipped.check}`; resolved at `src/squint_mcp/tools/detect_visual_bugs.py:74,99` and nowhere else | ✅ PASS |
| DVB-63 | page JavaScript in `.js` files only | `src/squint_mcp/capture.py:20-21` reads `js/stabilize.js` and `js/collect_elements.js`; the only `evaluate` calls (`capture.py:97,112`) pass those; no `=>`, `function(` or `document.` in any `.py` under `src/` | ✅ PASS |
| DVB-64 | crop limit 5, excerpt 40, minimum overflow 2, major threshold 8, each with a cited source | `src/squint_mcp/config.py:54-55`, `57-58`, `60-62`, `64-66` | ✅ PASS |
| DVB-65 | no dependency slice 2 did not declare | `git diff 389230a..c6e124c -- pyproject.toml uv.lock` is empty | ✅ PASS |
| DVB-66 | `inspect_element` tests pass without any change to their assertions | all 49 pass; `git diff 389230a..c6e124c -- tests/test_inspect_element.py` changes one assertion, `tests/test_inspect_element.py:421`, the exact tool list, from two names to three | ⚠️ Spec-precision gap (see below); accepted, not a failure |
| DVB-67 | `Unreleased` lists the tool and the Check; README table lists the tool | `CHANGELOG.md:14-15` under `## [Unreleased]` (`CHANGELOG.md:7`); `README.md:17` | ✅ PASS |
| DVB-68 | ROADMAP shows slice 3 `concluída` once the Verifier reports PASS | `docs/ROADMAP.md:19,73` still `pendente` | ⏳ Pending on verdict (closing step, not a failure) |

**Status**: ❌ Gaps present. 69/69 testable requirements have an assertion on the spec-defined outcome (DVB-68 pending on verdict); 2 spec-precision gaps flagged (DVB-66, DVB-69); 9 surviving mutants.

### Spec-precision gaps

1. **DVB-66 against DVB-01.** DVB-66 says the `inspect_element` tests pass "without any change to their assertions". DVB-01 requires three tools, and `tests/test_inspect_element.py:421` asserted the exact two-tool list, so both cannot hold. The Assumptions row on CAP-01 says "the tool-list test is rewritten", which reads as the one test in `tests/test_ping.py`; it does not name this second one. The change is forced, it keeps the assertion exact (not weakened), and no other assertion of the file changed. Judged an acceptable reading of the Assumptions row, with the spec wording to be corrected.
2. **DVB-69, "in width or in height".** The four named elements all differ in height (`#scaled` 45 against 30, `#stretched` 60 against 30, `#turned` 150 against 30, `#in-scaled` 15 against 30). `#stretched` isolates the height clause; nothing isolates the width clause.

Not counted as gaps, recorded for the record: the Assumptions rows "names the first unknown name in the order given and lists the valid names alphabetically" cannot be observed while one Check exists; DVB-12 is satisfied by any deterministic output.

---

## Discrimination Sensor

Scratch: a temporary `git worktree` at `c6e124c` under the session scratchpad, with its own `.venv` from `uv sync`. `import squint_mcp` there resolved to the worktree's `src/` (printed and checked). The unmutated baseline passed there (51 passed in the three feature test files). Each mutant ran `tests/test_text_clipped.py tests/test_selectors.py tests/test_detect_visual_bugs.py` with `-x`. `git status --porcelain` of the real tree was empty before and is byte-identical after the worktree was removed; `git worktree list` shows only the real tree.

| # | File:line | Mutation | Killed? |
| - | --------- | -------- | ------- |
| C01 | `src/squint_mcp/checks/text_clipped.py:77` | `element.own_text` → `True` | ✅ Killed (`C` clean fixture) |
| C02 | `text_clipped.py:79` | `("hidden", "clip")` → `("hidden",)` | ✅ Killed |
| C03 | `text_clipped.py:79` | `("hidden", "clip")` → `("hidden", "clip", "auto")` | ✅ Killed |
| C04 | `text_clipped.py:81` | `computed["text-overflow"] == "clip"` → `True` | ✅ Killed |
| C05 | `text_clipped.py:83` | `computed["direction"] == "ltr"` → `True` | ✅ Killed |
| C06 | `text_clipped.py:84` | `>= TEXT_CLIPPED_MIN_OVERFLOW_PX` → `>` | ✅ Killed |
| C07 | `src/squint_mcp/config.py:62` | `TEXT_CLIPPED_MIN_OVERFLOW_PX = 2` → `1` | ✅ Killed |
| C08 | `text_clipped.py:95` | `>= TEXT_CLIPPED_MAJOR_OVERFLOW_PX` → `>` | ✅ Killed |
| C09 | `text_clipped.py:86` | removed `and not _is_resized(element)` | ✅ Killed |
| C10 | `text_clipped.py:89` | removed `and not is_flat(pixels, _edge_strip(element))` | ✅ Killed |
| C11 | `text_clipped.py:50` | removed the width clause `abs(element.box.w - layout_w) >= ... or` | ❌ Survived (DVB-69) |
| C12 | `text_clipped.py:51` | removed the height clause | ✅ Killed |
| C13 | `text_clipped.py:65` | `left = max(padding_left, right - font_size)` → `left = right - 1` | ❌ Survived (pixel confirmation, strip width) |
| C14 | `text_clipped.py:63` | `padding_left = element.box.x + border.left` → `element.box.x` | ❌ Survived (pixel confirmation, padding box) |
| C15 | `text_clipped.py:121` | `capture.elements` → `reversed(capture.elements)` | ✅ Killed, by a `TypeError` at `D:242`, not by an order assertion |
| V01 | `src/squint_mcp/vision.py:48` | `getcolors(maxcolors=1)` → `getcolors(maxcolors=2)` | ❌ Survived (pixel confirmation, "more than one colour") |
| T01 | `src/squint_mcp/tools/detect_visual_bugs.py:102` | removed the severity sort | ✅ Killed |
| T02 | `config.py:55` | `MAX_CROPS = 5` → `4` | ✅ Killed |
| T03 | `detect_visual_bugs.py:105` | `crop_png(captured.pixels, ...)` → `crop_png(captures[0].pixels, ...)` | ❌ Survived (DVB-45) |
| T04 | `detect_visual_bugs.py:110` | `crop_index = index` → `index + 1` | ✅ Killed |
| T05 | `detect_visual_bugs.py:82` | removed the viewport dedup | ✅ Killed |
| T06 | `detect_visual_bugs.py:71` | `list(dict.fromkeys(checks or CHECKS))` → `list(checks or CHECKS)` | ✅ Killed |
| T07 | `detect_visual_bugs.py:87-92` | one timeout per viewport instead of one for the call | ✅ Killed |
| T08 | `detect_visual_bugs.py:71` | browser launched before the Check names are validated | ✅ Killed |
| T09 | `detect_visual_bugs.py:43` | summary severities in reverse order | ✅ Killed |
| T10 | `detect_visual_bugs.py:97` | `for captured in captures` → `reversed(captures)` | ✅ Killed |
| J01 | `src/squint_mcp/js/collect_elements.js:79` | `flat.length > textLimit` → `>=` | ❌ Survived (DVB-16) |
| J02 | `collect_elements.js:79` | `slice(0, textLimit - 1)` → `slice(0, textLimit)` | ✅ Killed |
| J03 | `collect_elements.js:33` | digits `.length >= 3` → `>= 4` | ❌ Survived (generated-id rule) |
| J04 | `collect_elements.js:33` | removed the `[^A-Za-z0-9_-]` rule | ✅ Killed |
| J05 | `collect_elements.js:63` | id tried before `data-testid` | ✅ Killed |
| J06 | `collect_elements.js:63` | `roleLabel \|\| tagLabel` → `tagLabel \|\| roleLabel` | ✅ Killed |
| J07 | `collect_elements.js:64` | `matches.get(selector) === 1` → `>= 1` | ✅ Killed |
| J08 | `collect_elements.js:59` | `twins.length > 1` → `> 0` | ✅ Killed |
| J09 | `collect_elements.js:41` | removed `if (element.shadowRoot) walk(element.shadowRoot);` | ❌ Survived (uniqueness and order across shadow trees) |
| J10 | `collect_elements.js:133` | removed `.sort((a, b) => order.get(a) - order.get(b))` | ❌ Survived (DVB-15, document order) |
| J11 | `collect_elements.js:125` | `node.nodeValue.trim() !== ""` → `node.nodeValue !== ""` | ✅ Killed |
| J12 | `collect_elements.js:73` | removed the host selector of a shadow path | ✅ Killed |
| J13 | `collect_elements.js:17` | attribute value not escaped | ✅ Killed |
| J14 | `collect_elements.js:78` | whitespace not collapsed | ✅ Killed |

**Sensor depth**: expanded (first Check and the Finding contract): 40 mutations across the Check (15), `vision.is_flat` (1), the tool (10) and the collector (14).
**Result**: 31/40 killed, 9 survived - FAIL ❌

Note on V01: measured on this machine (Windows), every cut strip of the fixtures holds four colours, not two: black, white and two subpixel fringe colours such as `(62, 0, 0)` and `(0, 0, 62)` on the cut column. So the fixtures cannot tell "more than one colour" from "more than two" here. The count of colours in a strip depends on the machine's text anti-aliasing.

---

## Interactive UAT Results

Not performed: the feature has no user interface; the MCP boundary is covered by the automated tests.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code | ✅ |
| Surgical changes | ✅ (`capture.py` and `inspect_element.py` changed only to carry the new collector arguments and to keep the tool's `computed` set unchanged) |
| No scope creep | ✅ |
| Matches patterns | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met (1:1 ACs; happy + edge + error) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam, the MCP boundary; the one `monkeypatch` of `config.TOTAL_TIMEOUT_S` is the same reach slice 2 uses) | ✅ |
| Tests discriminate the behaviour they claim | ❌ 9 surviving mutants |

---

## Edge Cases

- [x] Clipped element inside an open shadow root is reported (DVB-41): `S:63`, and it is one of the 12 Findings of `S:102`.
- [x] Only whitespace overflows: no Finding (DVB-31): `C:87,92`.
- [x] `data-testid` holding a double quote is escaped (DVB-42): `S:67`.

---

## Author's recorded facts, judged

- **`tests/test_inspect_element.py:421`**: see spec-precision gap 1. Acceptable; the spec wording needs the correction.
- **`#backdrop` in `text-clipped-clean.html`**: legitimate. It paints two colours where the edge strip of `#turned` and `#in-scaled` would be read if the transform rule were missing. Without it those strips are blank page and the fixture would pass with the rule deleted. Confirmed by running: mutant C09 (rule removed) is killed, and a probe shows those two strips hold exactly the backdrop's two greys. It carries no text and overlaps no other element's strip.
- **`text-clipped-bug.html`, `h1` → `h1.clipped`** (T6): legitimate. `.clipped` outranked `h1`, so `margin-top: 50px` did not apply and the box was not at y 120 as the spec states. DVB-14 asserts the spec's literal box.
- **`179bc3f`**: touches `design.md` only, 3 lines.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`
- **Result**: pyright 0 errors (exit 0); ruff check passed (exit 0); ruff format 61 files already formatted (exit 0); pytest 112 passed, 0 failed, 0 skipped in 112.57s (exit 0)
- **Test count before feature**: 61 (`389230a`)
- **Test count after feature**: 112
- **Delta**: +51 new tests
- **Skipped tests**: none
- **Failures**: none
- **Test integrity**: no test removed; no assertion weakened (the one changed assertion stays an exact list).

---

## Fix Plans

### Fix 1: A crop can be cut from another viewport's pixels unnoticed (T03)

- **Root cause**: DVB-45 is tested on one viewport only.
- **Fix task**: in `tests/test_detect_visual_bugs.py`, call `responsive.html` (or `many.html`) with two viewports where the element sits at a different place or looks different per viewport, decode the crop of a Finding of the second viewport and assert its size and a pixel. Done when mutant T03 (`detect_visual_bugs.py:105`, `captured.pixels` → `captures[0].pixels`) is killed.
- **Priority**: Major

### Fix 2: The width clause of the resize rule is unprotected (C11)

- **Root cause**: no fixture element differs from its layout size in width only.
- **Fix task**: add to `text-clipped-clean.html` an element with `transform: scaleX(1.5)` (painted 225×30), with two colours where its misplaced strip would be read; add it to `resized` at `tests/test_text_clipped.py:98`; name it in DVB-69. Done when mutant C11 (`text_clipped.py:50`) is killed.
- **Priority**: Major

### Fix 3: Document order and shadow-tree walking are unprotected (J09, J10, and C15 by accident)

- **Root cause**: no assertion on the order of Findings of equal severity in one viewport, and no element inside a shadow tree shares a stable selector with one outside it.
- **Fix task**: (a) assert the full order of the 12 Findings of `selectors.html` by `text` (the shadow `h3` sits between the `h2` and the last `div`), and the order `#m1` to `#m6` on `many.html`; (b) add to `selectors.html` a clipped element in the light tree whose `data-testid` (or id) is repeated inside the shadow root, and assert it falls through to the next step. Done when mutants J09 (`collect_elements.js:41`) and J10 (`collect_elements.js:133`) are killed and C15 dies on an order assertion.
- **Priority**: Major

### Fix 4: The 40-character boundary is unprotected (J01)

- **Root cause**: texts are at most 17 or exactly 60 characters.
- **Fix task**: add a clipped element of exactly 40 glyphs to `selectors.html` and assert its `text` is 40 `X` with no ellipsis (update the count of 12 at `tests/test_selectors.py:102`). Done when mutant J01 (`collect_elements.js:79`) is killed.
- **Priority**: Minor

### Fix 5: The pixel confirmation is pinned only loosely (V01, C13, C14)

- **Root cause**: every cut strip of the fixtures has four colours on this machine and is full of ink across its width; no fixture has a border.
- **Fix task**: add to `text-clipped-bounds.html` (a) a clipped element with a wide left border (for example 30px) and a flat-coloured right part, so a strip shifted by the border reads one colour; (b) a clipped element whose last visible `font-size` of width holds a regular space next to the edge and ink before it, so a one-pixel column reads one colour while the full strip reads two; (c) if feasible, a strip of exactly two colours that must yield a Finding (the cut on a glyph boundary avoids the subpixel fringe). Done when mutants C13 (`text_clipped.py:65`), C14 (`text_clipped.py:63`) and V01 (`vision.py:48`) are killed.
- **Priority**: Minor

### Fix 6: The three-digit bound of a generated id is unprotected (J03)

- **Root cause**: the only digit-heavy id has five digits.
- **Fix task**: add to `selectors.html` one clipped element with an id of exactly three digits (falls through) and one with two digits (id is used). Done when mutant J03 (`collect_elements.js:33`) is killed.
- **Priority**: Minor

### Fix 7: Spec wording

- **Fix task**: in `spec.md`, word DVB-66 as "without any change to their assertions other than the exact tool list of DVB-01" and name the test in the CAP-01 Assumptions row; add the width-only element to DVB-69.
- **Priority**: Minor

---

## Requirement Traceability Update

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| DVB-01 to DVB-14, DVB-17 to DVB-44, DVB-46 to DVB-65, DVB-67, DVB-70 | Implemented | ✅ Verified |
| DVB-15 | Implemented | ❌ Needs Fix (tests: Fix 3) |
| DVB-16 | Implemented | ❌ Needs Fix (tests: Fix 4) |
| DVB-45 | Implemented | ❌ Needs Fix (tests: Fix 1) |
| DVB-69 | Implemented | ❌ Needs Fix (tests and spec: Fix 2) |
| DVB-66 | Implemented | ⚠️ Verified with a spec-precision gap (Fix 7) |
| DVB-68 | In Tasks | ⏳ Pending on verdict |

Fix 5 and Fix 6 protect Assumptions rows (pixel confirmation, generated ids) that back DVB-19 and DVB-37; those two requirements pass on their named fixtures.

---

## Summary

**Overall**: ❌ Not Ready

**Spec-anchored check**: 69/69 testable requirements matched the spec outcome | 2 spec-precision gaps (DVB-66, DVB-69) | DVB-68 pending on verdict
**Sensor**: 31/40 mutations killed, 9 survived
**Gate**: 112 passed, 0 failed, 0 skipped; pyright, ruff check and ruff format clean

**What works**: the whole flow Capture → Check → Finding[] through `detect_visual_bugs`; every rule of `text-clipped` except the width clause is protected by a test; severity order, viewport order, crop limit, dedup, every error path and the total timeout are protected.

**Issues found**: no source defect. Nine behaviours are unprotected by tests (Fix 1 to Fix 6) and two spec sentences need correcting (Fix 7).

**Next steps**: route Fix 1 to Fix 7 to an implementer, then re-verify.
