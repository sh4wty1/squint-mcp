# low-contrast-real Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/low-contrast-real/design.md`
**Status**: Done; fixes of the first validation pass below

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec - confirm before Execute. Guidelines found: `docs/SPEC.md` (Testing Decisions: one seam, no assertion on Capture internals), `tests/test_text_clipped.py` (style floor).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (handlers, and the Check and vision code they drive) | integration, through the in-memory MCP client only, real Chromium | 1:1 to spec ACs; every listed edge case | `tests/test_*.py` | `uv run pytest` |
| Capture internals (collector, page scripts, layers, models), config, documents | none | build gate only; the existing suite is the regression check | - | build gate |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | While iterating on one test module | `uv run pytest tests/test_low_contrast_real.py` |
| Full | After tasks with tests through the MCP boundary | `uv run pytest` |
| Build | After every task | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |

---

## Execution Plan

Phases are ordered and run sequentially. Seven tasks: one batch, executed inline.

Baseline: 135 tests pass on this branch (2026-10-08).

### Phase 1: Capture

```
T1 → T2 → T3
```

### Phase 2: Check

```
T4 → T5 → T6
```

### Phase 3: Documents

```
T7
```

After the Verifier reports PASS: update `docs/ROADMAP.md` (LCR-46) and the Handoff of `.specs/STATE.md`. It is a closing step, not a task, because it is conditional on the verdict.

---

## Task Breakdown

### Phase 1: Capture

### T1: Add the contrast thresholds to config

- [x] Done

**What**: `CONTRAST_MIN_RATIO`, `CONTRAST_MIN_RATIO_LARGE`, `LARGE_TEXT_MIN_PX`, `LARGE_BOLD_TEXT_MIN_PX`, `BOLD_MIN_WEIGHT`, `LOW_CONTRAST_MAJOR_BELOW_RATIO`, `LOW_CONTRAST_WORST_PART_PERCENT` and `TEXT_INK_MIN`, with the values of the design and the source of each in a comment.
**Where**: `src/squint_mcp/config.py`
**Depends on**: None
**Reuses**: the comment style of the existing thresholds
**Requirement**: LCR-42

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The eight names exist with the values of the design's config table
- [x] Each has a comment starting with `# Source:` that cites WCAG 2.2 SC 1.4.3, CSS, or "Squint default" with the reason
- [x] Gate check passes: Build
- [x] Test count: 135 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(config): add the contrast thresholds of WCAG SC 1.4.3`

---

### T2: Collect the own-text boxes and the opacity of each element

- [x] Done

**What**: The collector emits `ownTextBoxes` (every client rect of the text nodes that are direct children, page coordinates, zero-area rects left out) and `opacity` (the element's computed opacity times that of every ancestor, a shadow root continuing at its host, memoized); `Element` gains `own_text_boxes` and `opacity`.
**Where**: `src/squint_mcp/js/collect_elements.js` (with the two fields in the models module)
**Depends on**: T1
**Reuses**: the `Range` loop that computes `ownTextRight`
**Requirement**: LCR-01, LCR-18, LCR-19 (enabling)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] `ownTextRight` is computed as before
- [x] The header comment of the collector names the two new facts
- [x] No output of `inspect_element` or `detect_visual_bugs` changes
- [x] Gate check passes: Build
- [x] Test count: 135 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): collect the own-text boxes and the opacity of each element`

---

### T3: Capture the background and ink layers

- [x] Done

**What**: `fill_text.js` forces `-webkit-text-fill-color` in the document and every open shadow root; `capture()` takes three more screenshots (fill `transparent`, black, white) after the existing one; `Capture` gains `background` and `ink` (AD-004).
**Where**: `src/squint_mcp/capture.py` (with the new page script and the two fields in the models module)
**Depends on**: T2
**Reuses**: the root walk of `stabilize.js`; the screenshot decoding at `capture.py:128`
**Requirement**: LCR-01 (enabling), LCR-41

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The collector still runs before any fill, so `computed` holds the page's own styles
- [x] `pixels` is still the first screenshot, taken before any fill
- [x] `playwright` is imported only in `capture.py`
- [x] Gate check passes: Build
- [x] Test count: 135 tests pass

**Tests**: none
**Gate**: build

**Commit**: `feat(capture): capture the page without text and the ink of its text`

---

### Phase 2: Check

### T4: Add the low-contrast-real Check

- [x] Done

**What**: `vision.text_backgrounds`; the Check module with design rules 1 (own text only), 3, 4, 5, 6, 7 and 8 and its Finding; its entry in `CHECKS`; `Evidence.measured` accepting strings; the tool docstring naming both Checks; the literal of the unknown-Check message in the four assertions of slice 3.
**Where**: `src/squint_mcp/checks/low_contrast_real.py` (with the sampling function in the vision module, the registry, the `measured` type in the models module, the docstring of the detect tool, fixtures and tests under `tests/`)
**Depends on**: T3
**Reuses**: the shape of `text_clipped.py`; `_region`; `tests/helpers.py`
**Requirement**: LCR-01, LCR-02, LCR-03, LCR-04, LCR-05, LCR-06, LCR-11, LCR-12, LCR-13, LCR-23, LCR-24, LCR-25, LCR-26, LCR-30, LCR-32, LCR-33, LCR-34, LCR-35, LCR-36, LCR-40, LCR-43, LCR-49, LCR-50, LCR-52

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Fixtures exist: `low-contrast-bug.html` (`#flat` at `40,20 200x30`, `#alpha`, `[data-testid="hero"]`, `#almost-large`, in that document order) and `low-contrast-clean.html` (`#flat`, `#gradient`, `#large`, `#large-bold`)
- [x] `tests/test_low_contrast_real.py` holds one test per requirement above that is observable through the tool, asserting the literal values of the spec (the whole Finding of LCR-30; `1.6` and `#cccccc` for the hero; `#808080` and `3.94` for `#alpha`; the summary line of LCR-03)
- [x] The alpha-0 guard of rule 3 is in from this task: `#two-colours` of `text-clipped-strip.html`, whose `color` is `transparent`, would otherwise get a Finding and break a test of slice 3 (LCR-50); LCR-17 gets its own test in T5
- [x] The four `Valid checks:` assertions of `tests/test_detect_visual_bugs.py` carry the literal of LCR-35 and no other existing assertion changes
- [x] The Check module holds no threshold literal and does not import `playwright`
- [x] Gate check passes: Build
- [x] Test count: at least 150 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): add the low-contrast-real check`

---

### T5: Keep the Check silent on hidden text and pin its bounds

- [x] Done

**What**: Design rule 2 (opacity), with the fixture that holds every boundary of the spec: the 10% share on each edge, the hiding rules, the text sizes and the severity floor.
**Where**: `src/squint_mcp/checks/low_contrast_real.py` (with the bounds fixture and its tests under `tests/`)
**Depends on**: T4
**Reuses**: `findings_on` of `tests/helpers.py`
**Requirement**: LCR-07, LCR-08, LCR-09, LCR-10, LCR-14, LCR-15, LCR-16, LCR-17, LCR-18, LCR-19, LCR-20, LCR-21, LCR-22, LCR-27, LCR-28, LCR-29, LCR-31, LCR-47, LCR-51

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] `low-contrast-bounds.html` holds `#right`, `#bottom`, `#left`, `#top`, `#same`, `#nested`, `#hidden`, `#transparent`, `#faded`, `#faded-child`, `#clipped-away`, `#covered`, `#clipped-part`, `#small-bold`, `#semibold`, `#large-low`, `#below-floor` and one element with own text and no box for LCR-51
- [x] One test per requirement above, each locating its element with `findings_on` and asserting the outcome of the spec (one Finding with the named values, or none)
- [x] One test asserts the exact set of elements of the fixture that get a Finding, so a Finding on any other element fails
- [x] LCR-33 is extended to the Findings of this fixture
- [x] Gate check passes: Build
- [x] Test count: at least 169 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): keep low-contrast-real silent on hidden and faded text`

---

### T6: Order Findings by document position across Checks

- [x] Done

**What**: The sort key of `detect_visual_bugs` becomes (severity, viewport, position of the element in the Capture, Check name); the comment and the docstring say so (issue #8).
**Where**: `src/squint_mcp/tools/detect_visual_bugs.py` (with the order fixture and its tests under `tests/`)
**Depends on**: T5
**Reuses**: the crop allocation already in the tool
**Requirement**: LCR-37, LCR-38, LCR-39, LCR-48

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] `checks-order.html` holds `#a` to `#e` as in LCR-37, every Finding `minor`
- [x] Tests assert the six `(selector, check)` pairs in order, the equality of LCR-39, five images and `cropIndex` 0 to 4 then `null`
- [x] The test of LCR-37 fails on the sort key of before this task (run once against it and recorded in the commit body)
- [x] Gate check passes: Build
- [x] Test count: at least 172 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `fix(detect): keep document order across checks of the same severity`

---

### Phase 3: Documents

### T7: Document the Check

- [x] Done

**What**: `CHANGELOG.md` lists the Check, the string values of `evidence.measured` and the order of Findings across Checks under the unreleased version; `README.md` names `low-contrast-real` as a Check that `detect_visual_bugs` runs.
**Where**: `CHANGELOG.md` (with the Checks sentence of the README)
**Depends on**: T6
**Reuses**: the wording of the slice 3 entries
**Requirement**: LCR-44, LCR-45

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The three CHANGELOG entries exist under the unreleased version
- [x] The README no longer says `low-contrast-real` is next
- [x] Gate check passes: Build
- [x] Test count: same as after T6

**Tests**: none
**Gate**: build

**Commit**: `docs: document the low-contrast-real check`

---

## Fixes of the first validation pass

The Verifier's first pass failed on six surviving mutants (`validation.md`). No source defect: each fix adds the criterion the spec lacked and the test that kills the mutant. Fixture: `low-contrast-reach.html`.

- [x] **Fix 1** (S3, LCR-53): the order of Findings of one severity across two viewports. `test_findings_of_one_severity_come_viewport_by_viewport`.
- [x] **Fix 2** (C3b, V3, LCR-51; LCR-54, LCR-55, LCR-60): a parent is not judged on its child's text; every line of a wrapped text is judged; text off the page; LCR-51 reworded to the one case it pins.
- [x] **Fix 3** (G8, G8b, C2; LCR-56 to LCR-59): text under a translucent layer on each side of half the ink, with the limit on its ratio recorded under Out of Scope; opacity across a shadow root.

## Fix of the second validation pass

The six survivors of pass 1 are killed. Two new mutants survived against LCR-55: only the last box sampled, and only the first text node collected.

- [x] **Fix 4** (V5, C4; LCR-61, LCR-62): `#three-lines`, with the band behind the middle line, and `#split`, two text nodes with the band behind the second.

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3

Phase 1:  T1 ------→ T2 ------→ T3
Phase 2:  T4 ------→ T5 ------→ T6
Phase 3:  T7
```

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: contrast thresholds | 1 file | ✅ Granular |
| T2: own-text boxes and opacity | 1 collector change and its 2 model fields | ✅ Granular |
| T3: background and ink layers | 1 function, 1 new script, 2 model fields | ✅ Cohesive |
| T4: the Check | 1 Check with its sampling function, registry entry, fixtures and tests | ⚠️ Cohesive: nothing in it is observable, so testable, before the Check is registered |
| T5: silence rules and bounds | 3 guards in 1 function, 1 fixture | ✅ Granular |
| T6: order across Checks | 1 sort key, 1 fixture | ✅ Granular |
| T7: documents | 2 documents | ✅ Granular |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | None | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | Phase 1 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 | ✅ Match |
| T6 | T5 | T5 → T6 | ✅ Match |
| T7 | T6 | Phase 2 → T7 | ✅ Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Config | none | none | ✅ OK |
| T2 | Capture internals | none | none | ✅ OK |
| T3 | Capture internals | none | none | ✅ OK |
| T4 | MCP tools (Check, vision) | integration | integration | ✅ OK |
| T5 | MCP tools (Check) | integration | integration | ✅ OK |
| T6 | MCP tools (handler) | integration | integration | ✅ OK |
| T7 | Documents | none | none | ✅ OK |
