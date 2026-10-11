# overlap Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/overlap/design.md`
**Status**: Approved by the maintainer on 2026-10-11

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

- [ ] Done

**What**: `Cover` (`selector`, `pixels`, `raised`), `CoveredText` (`ink`, `hidden`, `covers`) and `Element.covered_text: CoveredText | None = None`, with the docstrings of the design.
**Where**: `src/squint_mcp/models.py`
**Depends on**: T3
**Reuses**: the camelCase alias configuration of `Element`
**Requirement**: OVL-01 (enabling), AD-005

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] An `Element` validated from the collector's output, which has no such key, gets `None`
- [ ] The result of `inspect_element` is unchanged
- [ ] Gate check passes: Build
- [ ] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(models): add covered text to an element`

---

### T5: Keep the collector's element list on the page

- [ ] Done

**What**: The collector stores the list it returns, in the order it returns it, as `globalThis.__squintElements`.
**Where**: `src/squint_mcp/js/collect_elements.js`
**Depends on**: T4
**Reuses**: the sorted list at `collect_elements.js:185`
**Requirement**: OVL-13, OVL-53 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The header comment of the script says the list is kept and why
- [ ] What the collector returns is unchanged
- [ ] Gate check passes: Build
- [ ] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): keep the collected elements on the page`

---

### Phase 2: Covered text

### T6: Add the cover page script

- [ ] Done

**What**: `covered_text.js`: installs `globalThis.__squintCovered` and returns the texts (`index`, `ancestors`, `region`, `layers`); `mark`, `ink`, `show` and `hit` as in the design, with the Silent layer and Raised layer rules.
**Where**: `src/squint_mcp/js/covered_text.js`
**Depends on**: T5
**Reuses**: `.specs/features/overlap/spike/overlap.js`; the root walk of `fill_text.js`
**Requirement**: OVL-23 to OVL-30, OVL-41 to OVL-46 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] It speaks of elements only by their index in `__squintElements`
- [ ] The highlight colours are red and blue at 255 and green at 64, with the reason in a comment
- [ ] Only elements that were `visible` before are ever shown
- [ ] `hit` restores the scroll position and tests each text at least once
- [ ] Gate check passes: Build
- [ ] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): add the page script that paints and hit tests covered text`

---

### T7: Add the covered-text arithmetic

- [ ] Done

**What**: `covered.py`: `assign_channels`, `ink_layers`, `may_be_covered`, `groups`, `hidden_ink`, `runs` and `hit_step` as in the design, on Pillow only.
**Where**: `src/squint_mcp/covered.py` (with `_bounds` of the vision module made public)
**Depends on**: T6
**Reuses**: `.specs/features/overlap/spike/spike.py`; `vision._bounds`; `config.TEXT_INK_MIN`
**Requirement**: OVL-62, OVL-49 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The module imports neither `playwright` nor `capture`
- [ ] "Seen" is in integers: twice the ink that shows is at least the ink alone
- [ ] No literal of the thresholds or of the cap: they come from `config`
- [ ] The two limits of the design are marked `ponytail:` (a positioned pseudo-element in a group; a text with a very large region)
- [ ] Gate check passes: Build
- [ ] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(covered): compute the hidden ink of a text from its layers`

---

### T8: Measure covered text in a Capture on request

- [ ] Done

**What**: `capture(..., covered_text: bool = False)`: after the fills, install the cover script, take the pairs of phase 1 and of phase 2 (clipped), hit test, and set `Element.covered_text` for every text of phase 2 (AD-005). `_screenshot` gains an optional clip.
**Where**: `src/squint_mcp/capture.py`
**Depends on**: T7
**Reuses**: `_screenshot`; the order of `measure` in `.specs/features/overlap/spike/spike.py`
**Requirement**: OVL-01 (enabling), OVL-60 (enabling), AD-005

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] A Capture taken without the keyword makes the same page calls as before this task
- [ ] `pixels`, `background` and `ink` are taken before anything of covered text touches the page
- [ ] The `ponytail:` comment at the layers of AD-004 is updated: covered text is on request
- [ ] `playwright` is imported only in `capture.py`
- [ ] Gate check passes: Build
- [ ] Test count: 237 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): measure covered text on request`

---

### Phase 3: Check

### T9: Add the overlap Check

- [ ] Done

**What**: `checks/overlap.py` with the five rules of the design, its entry in `CHECKS`, `COVERED_TEXT_CHECKS`, the tool asking for covered text and naming the Check in its description, the fixture `overlap-bug.html` and the tests of what it reports.
**Where**: `src/squint_mcp/checks/overlap.py` (with the registry, the tool, `tests/fixtures/overlap-bug.html` and `tests/test_overlap.py`)
**Depends on**: T8
**Reuses**: the shape of `checks/low_contrast_real.py`; `tests/helpers.py`; the cases of `.specs/features/overlap/spike/cases.py`
**Requirement**: OVL-01 to OVL-06, OVL-14, OVL-47, OVL-48, OVL-54 to OVL-56, OVL-58, OVL-61, OVL-64, OVL-68

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The test of OVL-02 asserts the whole list of `(selector, severity, hiddenPercent, coveredBy)` in order (L-020)
- [ ] The test of OVL-47 compares the Finding of `#half` with the literal of the spec
- [ ] The four assertions of `tests/test_detect_visual_bugs.py` that hold the list of valid Checks carry the literal of OVL-55, and nothing else of that file changes
- [ ] `overlap.py` holds no literal of a threshold or of a role
- [ ] Gate check passes: Build
- [ ] Test count: 237 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): add the overlap Check`

---

### T10: Keep the Check silent on overlaps that are meant

- [ ] Done

**What**: The fixture `overlap-clean.html` with the cases of OVL-20 to OVL-29 and OVL-31 to OVL-39, and its tests: the page as a whole, and one test per rule that names the element it holds silent.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-clean.html`)
**Depends on**: T9
**Reuses**: the clean cases of `.specs/features/overlap/spike/cases.py`, the placement of its fixed element and of its popover
**Requirement**: OVL-19 to OVL-29, OVL-31 to OVL-39

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Each case fails if its rule is removed: a test per case says which element would be reported, and the fixture's comment gives the share its cover hides
- [ ] `#nick` and `#skim` are under the threshold along the width and along the height (L-012)
- [ ] No text of the fixture is covered by anything its criterion does not name
- [ ] Gate check passes: Build
- [ ] Test count: the count after T9 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold the Check silent on overlaps that are meant`

---

### T11: Pin the bounds, the severity and the Coverer

- [ ] Done

**What**: The fixture `overlap-bounds.html` with the cases of the edges, the veil, the shadow trees, the shared layers, the severity rules and the several covers, and its tests.
**Where**: `tests/test_overlap.py` (with `tests/fixtures/overlap-bounds.html`)
**Depends on**: T10
**Reuses**: the bounds cases of `.specs/features/overlap/spike/cases.py`
**Requirement**: OVL-07 to OVL-13, OVL-15, OVL-16, OVL-30, OVL-40 to OVL-46, OVL-49 to OVL-53

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The threshold of 10% is pinned at the left, the top and the bottom edge, in a middle line and in a second text node (L-012)
- [ ] `#tie` and `#two-covers` name their Coverer at the hit-test step the fixture gets: it holds more than 20,000 pixels of Hidden ink
- [ ] The test of OVL-53 passes every `selector` and every `coveredBy` of the bug and bounds fixtures to `inspect_element`
- [ ] Gate check passes: Build
- [ ] Test count: the count after T10 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): pin the bounds, the severity and the Coverer`

---

### T12: Hold the Check with the other Checks and on a page of many covered texts

- [ ] Done

**What**: The fixtures `overlap-order.html` and `overlap-many.html`, and the tests of the order across Checks, of the 100 covered texts and of the three existing fixtures the spec names (`low-contrast-bounds.html`, `low-contrast-reach.html`, `text-clipped-clean.html`).
**Where**: `tests/test_overlap.py` (with the two fixtures)
**Depends on**: T11
**Reuses**: `checks-order.html` as the form of an order fixture; `.specs/features/overlap/spike/many1.html`
**Requirement**: OVL-17, OVL-18, OVL-57, OVL-59, OVL-60, OVL-69

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The test of OVL-57 asserts the whole list of `(selector, check)` pairs in order (L-020)
- [ ] The test of OVL-60 asserts 100 Findings and no error
- [ ] No test of an earlier slice changed but for the four literals of T9 (OVL-59)
- [ ] Gate check passes: Build
- [ ] Test count: the count after T11 plus the tests of this task; none deleted

**Tests**: integration
**Gate**: build

**Commit**: `test(overlap): hold the Check with the others and on many covered texts`

---

### Phase 4: Documents

### T13: Document the Check

- [ ] Done

**What**: The CHANGELOG entries under the unreleased version (the Check with its two thresholds, the lower severity under a Raised layer and what it does not report; grayscale text; the fix of issue #18) and the README naming four Checks.
**Where**: `CHANGELOG.md` (with the README)
**Depends on**: T12
**Reuses**: the entry of `offscreen-overflow` as the form
**Requirement**: OVL-65, OVL-66

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The CHANGELOG names the Silent layers, `fixed` and `sticky` elements and covers that paint nothing as not reported
- [ ] The README gives the number of Checks as four and says what `overlap` reports
- [ ] Gate check passes: Build
- [ ] Test count: the count after T12; none deleted

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
