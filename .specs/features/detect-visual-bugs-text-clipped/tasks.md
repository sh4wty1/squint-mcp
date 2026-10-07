# detect_visual_bugs + text-clipped Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/detect-visual-bugs-text-clipped/design.md`
**Status**: Approved

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec - confirm before Execute. Guidelines found: `docs/SPEC.md` (Testing Decisions), `tests/test_inspect_element.py` (style floor).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (handlers, and the capture, Check and vision code they drive) | integration, through the in-memory MCP client only, real Chromium | 1:1 to spec ACs; every listed edge case; every error path | `tests/test_*.py` | `uv run pytest` |
| Config, models, documents | none | build gate only | - | build gate |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | Not used: there are no unit tests in this project | `uv run pytest` |
| Full | After tasks with tests through the MCP boundary | `uv run pytest` |
| Build | After every task | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |

---

## Execution Plan

Phases are ordered and run sequentially. Nine tasks: two batches (Phases 1 and 2, then Phase 3), so sub-agents are offered at Execute.

Baseline: 61 tests pass on this branch with the fix of issue #5 merged in (`docs/adr/0003-box-model-content-is-layout-size.md` exists).

### Phase 1: Flow and Check

```
T1 → T2 → T3 → T4
```

### Phase 2: Tool behaviour

```
T5 → T6 → T7 → T8
```

### Phase 3: Documents

```
T9
```

After the Verifier reports PASS: update `docs/ROADMAP.md` (DVB-68). It is a closing step, not a task, because it is conditional on the verdict. DVB-65 (no new dependency) has no task: no task touches `pyproject.toml`, and the Verifier checks it.

---

## Task Breakdown

### Phase 1: Flow and Check

### T1: Add the Check and Finding defaults to config

- [x] Done

**What**: `MAX_CROPS = 5`, `TEXT_EXCERPT_MAX_CHARS = 40`, `TEXT_CLIPPED_MIN_OVERFLOW_PX = 2`, `TEXT_CLIPPED_MAJOR_OVERFLOW_PX = 8`, `TRANSFORM_MIN_SIZE_DIFF_PX = 1` and `CAPTURE_COMPUTED_PROPERTIES` (the 20 inspect properties plus `direction`), each with its source in a comment.
**Where**: `src/squint_mcp/config.py`
**Depends on**: None
**Reuses**: the existing constants and comment style
**Requirement**: DVB-64

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The six values exist, each under a `# Source:` comment
- [x] Gate check passes: Build
- [x] Test count: 61 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `feat(config): add check, finding and crop defaults`

---

### T2: Add the Capture → Check → Finding flow behind detect_visual_bugs

- [x] Done

**What**: The whole flow for one or more viewports, without crops: the collector emits `text` (collapsed, cut to 40 with `…`), `ownText`, `scrollWidth`, `clientWidth` and a CSS-path `selector`, in document order; `Element`, `Finding` and `Evidence` models; the Check registry; `text-clipped` with design rules 1 to 5 and the two severities; the tool with its schema, `null` handling, viewport loop, Finding order, summary line and result; registration in the server. `inspect_element` filters `computed` to its 20 properties.
**Where**: `src/squint_mcp/tools/detect_visual_bugs.py` (with the collector script, the models, the Checks package, the registration in the server module, the `computed` filter in the inspect tool, fixtures and tests under `tests/`)
**Depends on**: T1
**Reuses**: `capture()` with selector `*`; the `tools/inspect_element.py` shape (AD-002); `tests/conftest.py` fixtures
**Requirement**: DVB-01, DVB-02, DVB-03, DVB-04, DVB-05, DVB-06, DVB-07, DVB-08, DVB-09, DVB-11, DVB-12, DVB-13, DVB-15, DVB-16, DVB-17, DVB-19, DVB-20, DVB-21, DVB-22, DVB-23, DVB-46, DVB-47, DVB-60, DVB-61, DVB-62, DVB-63, DVB-66, DVB-70

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Fixtures exist: `Ahem.ttf`, `text-clipped-bug.html`, `text-clipped-bounds.html` (with `#moved`), `responsive.html`, and `selectors.html` holding `#long` and `#spaced`
- [x] One test per requirement above that is observable through the tool, asserting the literal values of the spec (`overflowPx` 8, 7 and 2; exactly 5 Findings on the bounds fixture; `#moved` at `{"x": 70, "y": 410, "w": 150, "h": 30}`; the two summary lines)
- [x] The exact-tool-list test in `tests/test_ping.py` asserts the three names; no assertion in `tests/test_inspect_element.py` changes
- [x] `evidence.cropIndex` is `null` on every Finding and the response carries no image block (crops arrive in T5)
- [x] Gate check passes: Build
- [x] Test count: at least 80 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(detect): add detect_visual_bugs with the text-clipped check`

---

### T3: Confirm the cut in the pixels

- [x] Done

**What**: `vision.is_flat` and design rule 7: no Finding when the edge strip of the padding box is painted in one colour.
**Where**: `src/squint_mcp/vision.py` (and its use in the Check module, fixture and tests under `tests/`)
**Depends on**: T2
**Reuses**: `_region`; `PIL.Image.getcolors(maxcolors=1)`
**Requirement**: DVB-10, DVB-24, DVB-25, DVB-26, DVB-27, DVB-28, DVB-29, DVB-30, DVB-31, DVB-32, DVB-33

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] `text-clipped-clean.html` holds the ten near-misses of DVB-24 to DVB-33, one element each
- [x] The clean fixture returns `findings` equal to `[]`, no image block and the text `No findings in 1 viewport.`
- [x] A test names each near-miss, so that one of them being reported says which
- [x] Gate check passes: Build
- [x] Test count: at least 82 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): confirm clipped text in the pixels`

---

### T4: Stay silent on an element painted at another size than its layout

- [ ] Done

**What**: Design rule 6: no Finding when `box` differs from the layout border box rebuilt from `box_model` by `TRANSFORM_MIN_SIZE_DIFF_PX` or more in width or in height. Runs before the pixel rule.
**Where**: `src/squint_mcp/checks/text_clipped.py` (modify; fixture and test under `tests/`)
**Depends on**: T3
**Reuses**: `Element.box_model` as the layout size (ADR-0003)
**Requirement**: DVB-69

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `text-clipped-clean.html` gains `#scaled`, `#stretched`, `#turned` and `#in-scaled`, last in the document, absolutely positioned, `transform-origin: 0 0`, 200px apart
- [ ] The clean fixture still returns no Finding, and the test fails for each of the four when rule 6 is removed
- [ ] `#moved` is still reported (DVB-70 stays green)
- [ ] A comment in the Check names the limit: a mirror or a half turn keeps both sizes and is read as no transform
- [ ] Gate check passes: Build
- [ ] Test count: at least 83 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(checks): skip text-clipped on elements under a resizing transform`

---

### Phase 2: Tool behaviour

### T5: Attach at most five crops, by severity

- [ ] Done

**What**: After sorting, the first `MAX_CROPS` Findings get `cropIndex` and a `crop_png` image block; the rest keep `null`.
**Where**: `src/squint_mcp/tools/detect_visual_bugs.py` (modify; fixture and tests under `tests/`)
**Depends on**: T4
**Reuses**: `vision.crop_png`, unchanged
**Requirement**: DVB-43, DVB-44, DVB-45

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `many.html` exists: `#small` first, then `#m1` to `#m6`, each in its own text colour
- [ ] `cropIndex` values on `many.html` are `0, 1, 2, 3, 4, null, null`; the response is one text block then five `image/png` blocks
- [ ] Each image is 182×62 px and shows its own Finding's text colour at offset (20, 31)
- [ ] The T2 assertion "no image block" on the bug fixture is replaced by the count of DVB-43
- [ ] Gate check passes: Build
- [ ] Test count: at least 86 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(detect): attach up to five crops by severity`

---

### T6: Prefer stable attributes in the selector

- [ ] Done

**What**: The collector's selector steps before the CSS path: unique `data-testid`, unique non-generated `id`, `aria-label` with tag or explicit `role`; attribute escaping; a shadow tree's path starting at its host's selector.
**Where**: `src/squint_mcp/js/collect_elements.js` (modify; fixture and tests under `tests/`)
**Depends on**: T5
**Reuses**: the document walk and CSS path added in T2
**Requirement**: DVB-14, DVB-18, DVB-34, DVB-35, DVB-36, DVB-37, DVB-38, DVB-39, DVB-40, DVB-41, DVB-42

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `selectors.html` holds one clipped element per case of DVB-34 to DVB-42
- [ ] One test per case asserts the literal selector of the spec, the Finding matched to its element by `text`
- [ ] `findings[0]` of `text-clipped-bug.html` equals the full literal of DVB-14
- [ ] Every Finding selector of `text-clipped-bug.html` and `selectors.html`, passed to `inspect_element`, returns the Finding's `box` (DVB-18)
- [ ] A comment in the collector names the known limit: a slotted child and a shadow child of the same tag under one host
- [ ] Gate check passes: Build
- [ ] Test count: at least 97 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(capture): generate stable selectors for findings`

---

### T7: Collapse repeated viewports and Check names

- [ ] Done

**What**: Equal viewports and repeated Check names are reduced to their first occurrence before any Capture.
**Where**: `src/squint_mcp/tools/detect_visual_bugs.py` (modify; tests under `tests/`)
**Depends on**: T6
**Reuses**: `dict.fromkeys` for order-keeping deduplication
**Requirement**: DVB-48, DVB-49

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] A call with the same viewport twice returns one `captures` entry and the `findings` of the single-viewport call
- [ ] A call with `["text-clipped", "text-clipped"]` returns the `findings` of the call with one name
- [ ] Gate check passes: Build
- [ ] Test count: at least 99 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(detect): collapse repeated viewports and check names`

---

### T8: Fail clearly

- [ ] Done

**What**: The unknown-Check error raised before any browser work; `min_length=1` on `viewports` and `checks`; the total timeout over all viewports with its message.
**Where**: `src/squint_mcp/tools/detect_visual_bugs.py` (modify; tests under `tests/`)
**Depends on**: T7
**Reuses**: the scheme, navigation and launch errors of `capture()`; the `asyncio.timeout` block and the timeout test of `inspect_element`; `client_without_chromium` and `/hang` from `tests/conftest.py`
**Requirement**: DVB-50, DVB-51, DVB-52, DVB-53, DVB-54, DVB-55, DVB-56, DVB-57, DVB-58, DVB-59

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] One test per requirement asserts `isError: true` and the message text of the spec
- [ ] DVB-51 runs on `client_without_chromium` and gets the unknown-Check message
- [ ] The timeout test patches `config.TOTAL_TIMEOUT_S` with a float, asserts the elapsed time on both sides and then makes a second call that succeeds
- [ ] Gate check passes: Build
- [ ] Test count: at least 109 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(detect): return clear errors and bound the call by the total timeout`

---

### Phase 3: Documents

### T9: Document detect_visual_bugs and text-clipped

- [ ] Done

**What**: The tool and the Check under `Unreleased` in the changelog; `detect_visual_bugs` in the tool table of the readme.
**Where**: `CHANGELOG.md` (plus one row in the tool table of the readme)
**Depends on**: T8
**Reuses**: the existing `inspect_element` entries
**Requirement**: DVB-67

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `Unreleased` lists `detect_visual_bugs` and `text-clipped`
- [ ] The readme's tool table has a `detect_visual_bugs` row
- [ ] Gate check passes: Build
- [ ] Test count: same as after T8 (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `docs: add detect_visual_bugs and text-clipped to the changelog and readme`

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3

Phase 1:  T1 → T2 → T3 → T4
Phase 2:  T5 → T6 → T7 → T8
Phase 3:  T9
```

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Config defaults | 1 file | ✅ Granular |
| T2: Flow behind the tool | 1 tool, the collector fields, the models, 1 Check, the registry and their tests | ⚠️ Cohesive: tests only cross the MCP boundary, so no part is testable before the tool returns a Finding. Crops, pixel rule, transform rule, selector preference, deduplication and errors are each split out |
| T3: Pixel confirmation | 1 function and its use in the Check | ✅ Granular |
| T4: Transform rule | 1 rule in 1 file | ✅ Granular |
| T5: Crops | 1 step in the tool | ✅ Granular |
| T6: Selector preference | 3 steps of 1 function in the collector | ✅ Cohesive: one behaviour (which selector is chosen) |
| T7: Deduplication | 2 lines in the tool | ✅ Granular |
| T8: Errors and timeout | 10 failure paths on one tool | ✅ Cohesive: one behaviour (failing clearly); seven of them reuse existing code |
| T9: Documents | 2 text edits | ⚠️ Cohesive, text only, no behaviour |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T1 | None | none | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | T3 → T4 | ✅ Match |
| T5 | T4 (previous phase) | phase order | ✅ Match |
| T6 | T5 | T5 → T6 | ✅ Match |
| T7 | T6 | T6 → T7 | ✅ Match |
| T8 | T7 | T7 → T8 | ✅ Match |
| T9 | T8 (previous phase) | phase order | ✅ Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: Config defaults | Config | none | none | ✅ OK |
| T2: Flow behind the tool | MCP tools | integration | integration | ✅ OK |
| T3: Pixel confirmation | MCP tools | integration | integration | ✅ OK |
| T4: Transform rule | MCP tools | integration | integration | ✅ OK |
| T5: Crops | MCP tools | integration | integration | ✅ OK |
| T6: Selector preference | MCP tools | integration | integration | ✅ OK |
| T7: Deduplication | MCP tools | integration | integration | ✅ OK |
| T8: Errors and timeout | MCP tools | integration | integration | ✅ OK |
| T9: Documents | Documents | none | none | ✅ OK |

## Requirement Coverage

| Task | Requirements |
| ---- | ------------ |
| T1 | DVB-64 |
| T2 | DVB-01 to DVB-09, DVB-11 to DVB-13, DVB-15 to DVB-17, DVB-19 to DVB-23, DVB-46, DVB-47, DVB-60 to DVB-63, DVB-66, DVB-70 |
| T3 | DVB-10, DVB-24 to DVB-33 |
| T4 | DVB-69 |
| T5 | DVB-43 to DVB-45 |
| T6 | DVB-14, DVB-18, DVB-34 to DVB-42 |
| T7 | DVB-48, DVB-49 |
| T8 | DVB-50 to DVB-59 |
| T9 | DVB-67 |
| Verifier, from file evidence | DVB-65 |
| Closing step | DVB-68 |

70 of 70 requirements mapped.
