# overlap Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/overlap/design.md`
**Status**: Approved by the maintainer on 2026-10-11. T1 to T13 and the fixes of the first validation pass (F1 to F4) are done; the fixes of the second pass (F5 to F8, at the end of this file) are in progress

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec - confirm before Execute. Guidelines found: `CONTRIBUTING.md` and `docs/SPEC.md` (Testing Decisions: one seam, the MCP tool boundary; no unit tests for internal helpers), `tests/test_low_contrast_real.py` (style floor). Lessons applied: L-012 (an outcome for every axis and edge of a geometric rule), L-020 (assert the whole order of a returned list).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (handlers, and the Check, Capture and pixel code they drive) | integration, through the in-memory MCP client only, real Chromium | 1:1 to spec ACs; every listed edge case | `tests/test_*.py` | `uv run pytest` |
| Capture internals (collector, page scripts, covered-text arithmetic, models), config, documents | none | build gate only; the existing suite is the regression check | - | build gate |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | While iterating on one test module | `uv run pytest tests/test_overlap.py` |
| Full | After tasks with tests through the MCP boundary | `uv run pytest` |
| Build | After every task | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |

---

## Execution Plan

Phases are ordered and run sequentially. Thirteen tasks: two batches (phases 1 and 2, then phases 3 and 4), so sub-agents are offered before Execute.

Baseline: 237 tests pass on this branch (2026-10-11), with and without `--disable-lcd-text`. The whole suite takes about seven minutes.

The spike in `.specs/features/overlap/spike/` is the prototype of phases 1 and 2: `overlap.js` of `covered_text.js`, `spike.py` of `covered.py` and of the order inside `capture()`, `cases.py` of the three fixtures.

### Phase 1: Every Capture

```
T1 → T2 → T3 → T4 → T5
```

### Phase 2: Covered text

```
T6 → T7 → T8
```

### Phase 3: Check

```
T9 → T10 → T11 → T12
```

### Phase 4: Documents

```
T13
```

After the Verifier reports PASS: update `docs/ROADMAP.md` (OVL-67), remove `.specs/features/overlap/spike/` and its `extend-exclude` line in `pyproject.toml`, close issue #18 through the pull request, and replace the Handoff of `.specs/STATE.md`. It is a closing step, not a task, because it is conditional on the verdict.

---

## Task Breakdown

### Phase 1: Every Capture

### T1: Launch Chromium with grayscale text

- [x] Done

**What**: `CHROMIUM_ARGS = ("--disable-lcd-text",)` in config, with its source in a comment (AD-006), passed to `chromium.launch` by `BrowserSession`.
**Where**: `src/squint_mcp/capture.py` (with the constant in the config module)
**Depends on**: None
**Reuses**: the launch at `capture.py:44`
**Requirement**: OVL-59 (enabling), AD-006

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Every launch of the session passes the arguments, the relaunch after a crash included
- [x] No existing test changes
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): rasterize text in grayscale`

---

### T2: Settle the layout before a Capture measures anything

- [x] Done

**What**: `_settle_layout(page)`: one screenshot of 16 × 16 pixels with `full_page=True`, discarded, taken after the idle wait and before the selector is counted; retried once on a `PlaywrightError` (issue #18, AD-006).
**Where**: `src/squint_mcp/capture.py`
**Depends on**: T1
**Reuses**: `page.screenshot` as in `_screenshot` (`capture.py:77`)
**Requirement**: issue #18, AD-006

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The collector, `scroll_width` and `pixels` all come after it
- [x] A comment says what it is for and that Linux does not show the fault
- [x] On Windows, `.specs/features/overlap/spike/probe_first_screenshot.py` shows the `code` width unchanged between the collector's layout and the screenshots (checked by hand; no test can hold it on CI)
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `fix(capture): settle the layout before measuring (#18)`

---

### T3: Add the overlap thresholds, the Silent layer roles and the hit-test cap to config

- [x] Done

**What**: `OVERLAP_MIN_HIDDEN_PERCENT`, `OVERLAP_MAJOR_HIDDEN_PERCENT`, `SILENT_LAYER_ROLES` and `HIT_TEST_MAX` with the values of the design and the source of each in a comment; `"z-index"` in `CAPTURE_COMPUTED_PROPERTIES`.
**Where**: `src/squint_mcp/config.py`
**Depends on**: T2
**Reuses**: the comment form of the existing constants
**Requirement**: OVL-63

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Each constant cites "Squint default" with its reason, or WAI-ARIA for the roles
- [x] `INSPECT_COMPUTED_PROPERTIES` is unchanged, so `inspect_element` does not return `z-index`
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(config): add the overlap thresholds and the Silent layer roles`

---

### T4: Add covered text to the Element model

- [x] Done

**What**: `Cover` (`selector`, `pixels`, `raised`), `CoveredText` (`ink`, `hidden`, `covers`) and `Element.covered_text: CoveredText | None = None`, with the docstrings of the design.
**Where**: `src/squint_mcp/models.py`
**Depends on**: T3
**Reuses**: the camelCase alias configuration of `Element`
**Requirement**: OVL-01 (enabling), AD-005

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] An `Element` validated from the collector's output, which has no such key, gets `None`
- [x] The result of `inspect_element` is unchanged
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(models): add covered text to an element`

---

### T5: Keep the collector's element list on the page

- [x] Done

**What**: The collector stores the list it returns, in the order it returns it, as `globalThis.__squintElements`.
**Where**: `src/squint_mcp/js/collect_elements.js`
**Depends on**: T4
**Reuses**: the sorted list at `collect_elements.js:185`
**Requirement**: OVL-13, OVL-53 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The header comment of the script says the list is kept and why
- [x] What the collector returns is unchanged
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): keep the collected elements on the page`

---

### Phase 2: Covered text

### T6: Add the cover page script

- [x] Done

**What**: `covered_text.js`: installs `globalThis.__squintCovered` and returns the texts (`index`, `ancestors`, `region`, `layers`); `mark`, `ink`, `show` and `hit` as in the design, with the Silent layer and Raised layer rules.
**Where**: `src/squint_mcp/js/covered_text.js`
**Depends on**: T5
**Reuses**: `.specs/features/overlap/spike/overlap.js`; the root walk of `fill_text.js`
**Requirement**: OVL-23 to OVL-30, OVL-41 to OVL-46 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] It speaks of elements only by their index in `__squintElements`
- [x] The highlight colours are red and blue at 255 and green at 64, with the reason in a comment
- [x] Only elements that were `visible` before are ever shown
- [x] `hit` restores the scroll position and tests each text at least once
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): add the page script that paints and hit tests covered text`

---

### T7: Add the covered-text arithmetic

- [x] Done

**What**: `covered.py`: `assign_channels`, `ink_layers`, `may_be_covered`, `groups`, `hidden_ink`, `runs` and `hit_step` as in the design, on Pillow only.
**Where**: `src/squint_mcp/covered.py` (with `_bounds` of the vision module made public)
**Depends on**: T6
**Reuses**: `.specs/features/overlap/spike/spike.py`; `vision._bounds`; `config.TEXT_INK_MIN`
**Requirement**: OVL-62, OVL-49 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The module imports neither `playwright` nor `capture`
- [x] "Seen" is in integers: twice the ink that shows is at least the ink alone
- [x] No literal of the thresholds or of the cap: they come from `config`
- [x] The two limits of the design are marked `ponytail:` (a positioned pseudo-element in a group; a text with a very large region)
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(covered): compute the hidden ink of a text from its layers`

---

### T8: Measure covered text in a Capture on request

- [x] Done

**What**: `capture(..., covered_text: bool = False)`: after the fills, install the cover script, take the pairs of phase 1 and of phase 2 (clipped), hit test, and set `Element.covered_text` for every text of phase 2 (AD-005). `_screenshot` gains an optional clip.
**Where**: `src/squint_mcp/capture.py`
**Depends on**: T7
**Reuses**: `_screenshot`; the order of `measure` in `.specs/features/overlap/spike/spike.py`
**Requirement**: OVL-01 (enabling), OVL-60 (enabling), AD-005

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] A Capture taken without the keyword makes the same page calls as before this task
- [x] `pixels`, `background` and `ink` are taken before anything of covered text touches the page
- [x] The `ponytail:` comment at the layers of AD-004 is updated: covered text is on request
- [x] `playwright` is imported only in `capture.py`
- [x] Gate check passes: Build
- [x] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): measure covered text on request`

---

### Phase 3: Check

### T9: Add the overlap Check

- [x] Done

**What**: `checks/overlap.py` with the five rules of the design, its entry in `CHECKS`, `COVERED_TEXT_CHECKS`, the tool asking for covered text and naming the Check in its description, the fixture `overlap-bug.html` and the tests of what it reports.
**Where**: `src/squint_mcp/checks/overlap.py` (with the registry, the tool, `tests/fixtures/overlap-bug.html` and `tests/test_overlap.py`)
**Depends on**: T8
**Reuses**: the shape of `checks/low_contrast_real.py`; `tests/helpers.py`; the cases of `.specs/features/overlap/spike/cases.py`
**Requirement**: OVL-01 to OVL-06, OVL-14, OVL-47, OVL-48, OVL-54 to OVL-56, OVL-58, OVL-61, OVL-64, OVL-68

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test of OVL-02 asserts the whole list of `(selector, severity, hiddenPercent, coveredBy)` in order (L-020)
- [x] The test of OVL-47 compares the Finding of `#half` with the literal of the spec
- [x] The four assertions of `tests/test_detect_visual_bugs.py` that hold the list of valid Checks carry the literal of OVL-55, and nothing else of that file changes
- [x] `overlap.py` holds no literal of a threshold or of a role
- [x] Gate check passes: Build
- [x] Test count: 237 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): add the overlap Check`

---

### T10: Keep the Check silent on overlaps that are meant

- [x] Done

**What**: The fixture `overlap-clean.html` with the cases of OVL-20 to OVL-29 and OVL-31 to OVL-39, and its tests: the page as a whole, and one test per rule that names the element it holds silent.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-clean.html`)
**Depends on**: T9
**Reuses**: the clean cases of `.specs/features/overlap/spike/cases.py`, the placement of its fixed element and of its popover
**Requirement**: OVL-19 to OVL-29, OVL-31 to OVL-39

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Each case fails if its rule is removed: a test per case says which element would be reported, and the fixture's comment gives the share its cover hides
- [x] `#nick` and `#skim` are under the threshold along the width and along the height (L-012)
- [x] No text of the fixture is covered by anything its criterion does not name
- [x] Gate check passes: Build
- [x] Test count: the count after T9 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold the Check silent on overlaps that are meant`

---

### T11: Pin the bounds, the severity and the Coverer

- [x] Done

**What**: The fixture `overlap-bounds.html` with the cases of the edges, the veil, the shadow trees, the shared layers, the severity rules and the several covers, and its tests.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-bounds.html`)
**Depends on**: T10
**Reuses**: the bounds cases of `.specs/features/overlap/spike/cases.py`
**Requirement**: OVL-07 to OVL-13, OVL-15, OVL-16, OVL-30, OVL-40 to OVL-46, OVL-49 to OVL-53

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The threshold of 10% is pinned at the left, the top and the bottom edge, in a middle line and in a second text node (L-012)
- [x] `#tie` and `#two-covers` name their Coverer at the hit-test step the fixture gets: it holds more than 20,000 pixels of Hidden ink
- [x] The test of OVL-53 passes every `selector` and every `coveredBy` of the bug and bounds fixtures to `inspect_element`
- [x] Gate check passes: Build
- [x] Test count: the count after T10 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin the bounds, the severity and the Coverer`

---

### T12: Hold the Check with the other Checks and on a page of many covered texts

- [x] Done

**What**: The fixtures `overlap-order.html` and `overlap-many.html`, and the tests of the order across Checks, of the 100 covered texts and of the three existing fixtures the spec names (`low-contrast-bounds.html`, `low-contrast-reach.html`, `text-clipped-clean.html`).
**Where**: `tests/test_overlap.py` (with the two fixtures)
**Depends on**: T11
**Reuses**: `checks-order.html` as the form of an order fixture; `.specs/features/overlap/spike/many1.html`
**Requirement**: OVL-17, OVL-18, OVL-57, OVL-59, OVL-60, OVL-69

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test of OVL-57 asserts the whole list of `(selector, check)` pairs in order (L-020)
- [x] The test of OVL-60 asserts 100 Findings and no error
- [x] No test of an earlier slice changed but for the four literals of T9 (OVL-59)
- [x] Gate check passes: Build
- [x] Test count: the count after T11 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold the Check with the others and on many covered texts`

---

### Phase 4: Documents

### T13: Document the Check

- [x] Done

**What**: The CHANGELOG entries under the unreleased version (the Check with its two thresholds, the lower severity under a Raised layer and what it does not report; grayscale text; the fix of issue #18) and the README naming four Checks.
**Where**: `CHANGELOG.md` (with the README)
**Depends on**: T12
**Reuses**: the entry of `offscreen-overflow` as the form
**Requirement**: OVL-65, OVL-66

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The CHANGELOG names the Silent layers, `fixed` and `sticky` elements and covers that paint nothing as not reported
- [x] The README gives the number of Checks as four and says what `overlap` reports
- [x] Gate check passes: Build
- [x] Test count: the count after T12; none deleted

**Tests**: none
**Gate**: build

**Commit**: `docs: document the overlap Check`

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3 → Phase 4

Phase 1:  T1 ------→ T2 ------→ T3 ------→ T4 ------→ T5
Phase 2:  T6 ------→ T7 ------→ T8
Phase 3:  T9 ------→ T10 -----→ T11 -----→ T12
Phase 4:  T13
```

Execution is strictly sequential. Batches: phases 1 and 2 (eight tasks, all Capture internals, the build gate after each), then phases 3 and 4 (five tasks).

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Grayscale text | 1 constant, 1 call | ✅ Granular |
| T2: Settle the layout | 1 function, 1 call | ✅ Granular |
| T3: Config | 5 constants, 1 file | ✅ Granular |
| T4: Models | 2 models and 1 field, 1 file | ✅ Granular |
| T5: Collector's list | 1 statement | ✅ Granular |
| T6: Cover script | 1 page script | ✅ Granular |
| T7: Arithmetic | 1 module, 7 cohesive functions | ⚠️ OK: one concept, no browser |
| T8: Capture on request | 1 function extended | ✅ Granular |
| T9: The Check | 1 Check with its wiring, fixture and tests | ⚠️ OK: the Check is observable only once registered and asked for; its tests cannot come later |
| T10: Clean fixture | 1 fixture with its tests | ✅ Granular |
| T11: Bounds fixture | 1 fixture with its tests | ✅ Granular |
| T12: With the others | 2 small fixtures with their tests | ⚠️ OK: both hold the Check among the others |
| T13: Documents | 2 documents | ✅ Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T1 | None | first of phase 1 | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | T3 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 | ✅ Match |
| T6 | T5 | first of phase 2, after phase 1 | ✅ Match |
| T7 | T6 | T6 → T7 | ✅ Match |
| T8 | T7 | T7 → T8 | ✅ Match |
| T9 | T8 | first of phase 3, after phase 2 | ✅ Match |
| T10 | T9 | T9 → T10 | ✅ Match |
| T11 | T10 | T10 → T11 | ✅ Match |
| T12 | T11 | T11 → T12 | ✅ Match |
| T13 | T12 | first of phase 4, after phase 3 | ✅ Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: Grayscale text | Capture internals, config | none | none | ✅ OK |
| T2: Settle the layout | Capture internals | none | none | ✅ OK |
| T3: Config | config | none | none | ✅ OK |
| T4: Models | Capture internals (models) | none | none | ✅ OK |
| T5: Collector's list | Capture internals (page script) | none | none | ✅ OK |
| T6: Cover script | Capture internals (page script) | none | none | ✅ OK |
| T7: Arithmetic | Capture internals (covered-text arithmetic) | none | none | ✅ OK |
| T8: Capture on request | Capture internals | none | none | ✅ OK |
| T9: The Check | MCP tools (the Check and the tool that drives it) | integration | integration | ✅ OK |
| T10: Clean fixture | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T11: Bounds fixture | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T12: With the others | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T13: Documents | documents | none | none | ✅ OK |

Phases 1 and 2 build Capture internals that no client can observe until the Check exists: the source documents forbid a second test seam, so their proof is T9 to T12, which run every criterion through the tool, and the build gate after each of them holds the existing 237 tests.

---

## Requirement Coverage

| Requirements | Task |
| --- | --- |
| OVL-01 to OVL-06, OVL-14, OVL-47, OVL-48, OVL-54 to OVL-56, OVL-58, OVL-61, OVL-64, OVL-68 | T9 |
| OVL-19 to OVL-29, OVL-31 to OVL-39 | T10 |
| OVL-07 to OVL-13, OVL-15, OVL-16, OVL-30, OVL-40 to OVL-46, OVL-49 to OVL-53 | T11 |
| OVL-17, OVL-18, OVL-57, OVL-59, OVL-60, OVL-69 | T12 |
| OVL-62 | T7 (and T9: the Check module) |
| OVL-63 | T3 |
| OVL-65, OVL-66 | T13 |
| OVL-67 | closing step |

69 of 69 mapped.

---

## Fixes of the first validation pass

The Verifier's first pass ([`validation.md`](validation.md), 2026-10-11) found no defect in `src/` and eleven surviving mutants: rules that the Terms and the Assumptions of the spec state, that the code implements and that no criterion held. The four tasks below add the criteria OVL-70 to OVL-79, their fixture cases and their tests through the MCP boundary. None changes `src/`. A new test is done when it fails under the mutant it is for, applied to a scratch copy of `src/` as the report describes it.

```
F1 → F2 → F3 → F4
```

Baseline: 302 tests pass (2026-10-11). The whole suite takes about eleven minutes. The matrix and the gate commands at the top of this file apply.

### F1: Hold the reading of `role`, ancestors, descendants and faint text silent

- [x] Done

**What**: Four cases appended to `overlap-clean.html`, with a test each: a cover of `role` `" Menu "` (OVL-70), a box painted by the `::after` of the row of the text (OVL-72), a link of the text stretched over it above its cover (OVL-73) and a text of `opacity: 0.4` (OVL-74).
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-clean.html`)
**Depends on**: None
**Reuses**: the rows of the fixture and the `clean` helper of the tests
**Requirement**: OVL-70, OVL-72, OVL-73, OVL-74

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The cases come after the existing rows, so nothing already placed moves
- [x] The whole-page test of OVL-19 passes unchanged: no Finding of any of the four Checks
- [x] Each test fails under its mutant: J4 (`#under-spaced-role`), J6b (`#under-own-row`), J6c (`#own-link-text`), C2 (`#opacity-40`)
- [x] Gate check passes: Build
- [x] Test count: 306 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold the reading of role, ancestors, descendants and faint text silent`

---

### F2: Pin a list of roles, the bound of Text ink and two measured texts that cross

- [x] Done

**What**: Three cases appended to `overlap-bounds.html`, with a test each: a cover of `role` `"menu navigation"` (OVL-71), a text of `opacity: 0.6` (OVL-75) and a text under a label whose own glyphs are covered too (OVL-76).
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-bounds.html`)
**Depends on**: F1
**Reuses**: the rows of the fixture and the `bounds` helper of the tests
**Requirement**: OVL-71, OVL-75, OVL-76

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The pinned list of selectors and the count of the fixture grow by the four new Findings, to 23
- [x] `#tie` and `#two-covers` keep their Coverer: the page stays at a hit-test step of 2
- [x] Each test fails under its mutants: J5 (`#under-role-list`), C2b (`#opacity-60`), C5 and C11 (`#under-label` and `#label`)
- [x] Gate check passes: Build
- [x] Test count: 309 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin a list of roles, the bound of Text ink and two measured texts that cross`

---

### F3: Pass over an element the scroll moved at hit testing

- [x] Done

**What**: The fixture `overlap-scrolled.html`, a page of three viewports with one covered text below the first and a fixed element that lies over its Hidden ink once hit testing scrolls, and its test (OVL-77).
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-scrolled.html`)
**Depends on**: F2
**Reuses**: the row and the cover of `overlap-bounds.html`
**Requirement**: OVL-77

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test asserts the whole list of Findings of the page: one, with `coveredBy` the plain cover
- [x] Nothing else on the page is covered
- [x] The test fails under J8
- [x] Gate check passes: Build
- [x] Test count: 310 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pass over an element the scroll moved at hit testing`

---

### F4: Pin the sample of a capped Capture and the text its step passes over

- [x] Done

**What**: The fixture `overlap-sampled.html`, a page of more than 20,000 pixels of Hidden ink with a text the step passes over whole (OVL-78) and a text whose Coverer depends on the sample (OVL-79), and their tests. The sentence of the Terms on the sample says where its count starts.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-sampled.html`)
**Depends on**: F3
**Reuses**: the rows of `overlap-many.html` as the filler
**Requirement**: OVL-78, OVL-79

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test of OVL-79 asserts the whole list of `(selector, severity, hiddenPercent, coveredBy)` of the page in order (L-020)
- [x] The comment of the fixture gives its pixels of Hidden ink and the step they are tested at
- [x] Each test fails under its mutant: J10 (`#speck`), C8 (`#striped`)
- [x] `validate_spec.py --strict` exits 0 on the spec with its ten new criteria
- [x] Gate check passes: Build
- [x] Test count: 312 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin the sample of a capped Capture and the text its step passes over`

---

### Requirement coverage of the fixes

| Requirements | Task |
| --- | --- |
| OVL-70, OVL-72, OVL-73, OVL-74 | F1 |
| OVL-71, OVL-75, OVL-76 | F2 |
| OVL-77 | F3 |
| OVL-78, OVL-79 | F4 |

10 of 10 mapped; with the table above, 79 of 79.

---

## Fixes of the second validation pass

The Verifier's second pass ([`validation.md`](validation.md), 2026-10-11) again found no defect in `src/`. Of its 21 new mutants eleven survive as gaps: rules the code implements and the Terms decide, with no criterion and no test. The four tasks below add the criteria OVL-80 to OVL-91, their fixture cases and their tests through the MCP boundary, and the two sentences the report asks of the spec (Fix 7): which Hidden ink counts towards the 20,000 of the Term "Coverer", and the limit of the design that Out of Scope did not list. None changes `src/`. A new test is done when it fails under the mutant it is for, applied to a scratch copy of `src/` as the report describes it.

```
F5 → F6 → F7 → F8
```

Baseline: 312 tests pass (2026-10-11). The whole suite takes about eleven minutes. The matrix and the gate commands at the top of this file apply.

### F5: Pin texts stacked in one place, where a text sits and the colour of its glyphs

- [x] Done

**What**: Seven cases appended to `overlap-bounds.html`, with a test each: four texts stacked in one row (OVL-80), a text that starts at a column of its own (OVL-81), a text under the box of a tag whose glyphs stand beside it (OVL-82), own text around a child with text (OVL-83), glyphs of a colour of alpha 0.5 (OVL-87), a transparent `color` under an opaque fill (OVL-89) and a hidden menu over what a plain cover hides (OVL-90). With them, the sentence of the Term "Coverer" on which Hidden ink is tested and the Out of Scope row for the pseudo-element limit of the design.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-bounds.html`)
**Depends on**: None
**Reuses**: the rows of the fixture and the `bounds` helper of the tests
**Requirement**: OVL-80, OVL-81, OVL-82, OVL-83, OVL-87, OVL-89, OVL-90

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The pinned list of selectors and the count of the fixture grow by the eleven new Findings, to 34
- [x] The page holds 55,180 pixels of Hidden ink to test, counted in the comment of the fixture: it stays at a hit-test step of 2, and `#tie` and `#two-covers` keep their Coverer
- [x] Each test fails under its mutants: N2 and N3 (`#stack-0` to `#stack-3`), N1b (`#shifted`), N9 (`#under-tag`), N28 (`#around`), N10 (`#translucent`), N22 (`#filled`), N11 (`#under-closed-menu`)
- [x] The Out of Scope row describes the case that probes `p2b` and `p2c` of the report tell apart, and no more
- [x] Gate check passes: Build
- [x] Test count: 319 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin stacked texts, where a text sits and its glyph colour`

---

### F6: Hold a transparent fill and closed menus silent

- [x] Done

**What**: Three cases appended to `overlap-clean.html`, with their tests: a text of a transparent `-webkit-text-fill-color` under an opaque `color` (OVL-88), a text under a menu closed by `display: none` and one under a menu closed by `visibility: hidden` (OVL-91).
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-clean.html`)
**Depends on**: None
**Reuses**: the rows of the fixture and the `clean` helper of the tests
**Requirement**: OVL-88, OVL-91

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The cases come after the existing rows, so nothing already placed moves
- [x] The whole-page test of OVL-19 passes unchanged: no Finding of any of the four Checks
- [x] The test of OVL-88 fails under N22 (`#transparent-fill`)
- [x] The tests of OVL-91 assert through `inspect_element` that nothing is painted over the two texts
- [x] Gate check passes: Build
- [x] Test count: 322 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold a transparent fill and closed menus silent`

---

### F7: Pin the rows of the sample and a page under the cap

- [x] Done

**What**: A text of `overlap-sampled.html` whose Coverer depends on the rows the sample tests (OVL-84), and the fixture `overlap-exact.html`, the row of `#striped` alone on a page under the cap (OVL-85), with their tests.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-sampled.html` and `tests/fixtures/overlap-exact.html`)
**Depends on**: None
**Reuses**: the row of `#striped` of `overlap-sampled.html`
**Requirement**: OVL-84, OVL-85

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The whole-list assertion of the sampled page grows by the new Finding, and `#speck` and `#striped` keep theirs
- [x] The comment of the sampled fixture gives its 26,610 pixels of Hidden ink and the step they are tested at, which stays 2
- [x] Each test fails under its mutant: N5 (`#row-striped`), N13 (`#striped` of `overlap-exact.html`)
- [x] Gate check passes: Build
- [x] Test count: 324 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin the rows of the sample and a page under the cap`

---

### F8: Measure a page that is scrolled when it is captured

- [ ] Done

**What**: The fixture `overlap-scrolled-on-load.html`, a page of three viewports with one covered text below the first and a script that scrolls it 900px while it loads, and its test (OVL-86).
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-scrolled-on-load.html`)
**Depends on**: None
**Reuses**: the row and the cover of `overlap-scrolled.html`
**Requirement**: OVL-86

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The test asserts the whole list of Findings of the page: one, with its severity and with `coveredBy` the plain cover
- [ ] The test fails under N8
- [ ] `validate_spec.py --strict` exits 0 on the spec with its twelve new criteria
- [ ] Gate check passes: Build
- [ ] Test count: 325 tests pass; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): measure a page that is scrolled when it is captured`

---

### Requirement coverage of the second fixes

| Requirements | Task |
| --- | --- |
| OVL-80, OVL-81, OVL-82, OVL-83, OVL-87, OVL-89, OVL-90 | F5 |
| OVL-88, OVL-91 | F6 |
| OVL-84, OVL-85 | F7 |
| OVL-86 | F8 |

12 of 12 mapped; with the tables above, 91 of 91.
