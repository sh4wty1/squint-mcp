# Capture + inspect_element Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/capture-inspect-element/design.md`
**Status**: In Progress

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec. Guidelines found: `docs/SPEC.md` (Testing Decisions), `tests/test_ping.py` (style floor).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (handlers, and the capture and vision code they drive) | integration, through the in-memory MCP client only, real Chromium | 1:1 to spec ACs; every listed edge case; every error path | `tests/test_*.py` | `uv run pytest` |
| Config, packaging, CI, documents | none | build gate only | - | build gate |

## Gate Check Commands

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | Not used: there are no unit tests in this project | `uv run pytest` |
| Full | After tasks with tests through the MCP boundary | `uv run pytest` |
| Build | After every task | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |

---

## Execution Plan

Phases are ordered and run sequentially. Eight tasks: one batch, executed inline.

### Phase 1: Capture and tool

```
T1 → T2 → T3 → T4 → T5 → T6
```

### Phase 2: CI and documents

```
T7 → T8
```

After the Verifier reports PASS: update `docs/ROADMAP.md` (CAP-47). It is a closing step, not a task, because it is conditional on the verdict.

---

## Task Breakdown

### Phase 1: Capture and tool

### T1: Add the playwright and Pillow dependencies

- [x] Done

**What**: `playwright` and `Pillow` as runtime dependencies, lock file updated.
**Where**: `pyproject.toml` (plus the generated lock file)
**Depends on**: None
**Reuses**: existing dependency list
**Requirement**: CAP-41

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] `playwright` and `pillow` are in `[project].dependencies`; `numpy` and `coloraide` are not
- [x] Gate check passes: Build
- [x] Test count: 12 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `build: add playwright and pillow dependencies`

---

### T2: Add the capture and vision defaults to config

- [x] Done

**What**: Default viewport, total timeout, network-idle timeout, crop margin, crop size limit, sampled-colour count and the computed-property list, each with its source cited.
**Where**: `src/squint_mcp/config.py`
**Depends on**: T1
**Reuses**: the module left empty by slice 1
**Requirement**: CAP-40

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The seven values of CAP-40 are defined, each with a source comment
- [x] Gate check passes: Build
- [x] Test count: 12 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `feat(config): add capture and vision defaults`

---

### T3: Add Capture production and the inspect_element tool

- [x] Done

**What**: The `BrowserSession` held by the server lifespan, `capture()` with stabilization, the two page scripts, and `inspect_element` returning `viewport`, `stabilized`, `box`, `boxModel` and `computed`; the fixtures and tests that drive it.
**Where**: `src/squint_mcp/capture.py` (with its page scripts under `js/`, the tool module, the registration in the server module, fixtures and tests under `tests/`)
**Depends on**: T2
**Reuses**: `tools/ping.py` module shape; `tests/conftest.py` client fixture; `tests/test_ping.py` helpers style
**Requirement**: CAP-01, CAP-02, CAP-03, CAP-05, CAP-06, CAP-07, CAP-08, CAP-16, CAP-17, CAP-18, CAP-19, CAP-21, CAP-22, CAP-23, CAP-24, CAP-25, CAP-26, CAP-28, CAP-29, CAP-36, CAP-37, CAP-42, CAP-43

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] One test per testable AC listed above; CAP-24, CAP-28, CAP-29, CAP-42 and CAP-43 hold by file evidence
- [x] `tests/test_ping.py::test_ping_is_the_only_tool` is replaced by a test asserting the exact two-tool list (CAP-01)
- [x] `playwright` is imported only by `capture.py`; page JavaScript lives only in `.js` files
- [x] Gate check passes: Build
- [x] Test count: 29 tests pass (12 existing, one of them rewritten, plus 17)

**Tests**: integration
**Gate**: build

**Commit**: `feat(inspect): add capture production and inspect_element tool`

---

### T4: Add the crop and the sampled colours

- [x] Done

**What**: `vision.crop` and `vision.sample_colors`, and their use by `inspect_element`: the PNG image block and `sampledColors`.
**Where**: `src/squint_mcp/vision.py` (and its use in the tool module, tests under `tests/`)
**Depends on**: T3
**Reuses**: `Capture.pixels` and `Element.box` from T3
**Requirement**: CAP-04, CAP-09, CAP-10, CAP-11, CAP-12, CAP-13, CAP-14, CAP-15, CAP-20

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] One test per AC listed above
- [x] Gate check passes: Build
- [x] Test count: 38 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(vision): add crop and sampled colours to inspect_element`

---

### T5: Add the clear errors

- [x] Done

**What**: The messages for zero matches, several matches, invalid selector, no rendered box, unsupported scheme, failed navigation and Chromium that cannot be launched.
**Where**: `src/squint_mcp/tools/inspect_element.py` (the selector-count checks; the scheme, navigation, selector-syntax and launch errors in the capture module; tests under `tests/`)
**Depends on**: T4
**Reuses**: `ToolError` from the SDK
**Requirement**: CAP-27, CAP-30, CAP-31, CAP-32, CAP-33, CAP-34, CAP-38, CAP-39

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] One test per AC listed above, each asserting `isError` and the spec's message
- [x] Gate check passes: Build
- [x] Test count: 46 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(inspect): return clear errors for bad selectors, urls and missing chromium`

---

### T6: Bound every call by the total timeout

- [ ] Done

**What**: `asyncio.timeout(config.TOTAL_TIMEOUT_S)` around the handler body and the `Timed out after Ns.` error.
**Where**: `src/squint_mcp/tools/inspect_element.py` (modify; test under `tests/`)
**Depends on**: T5
**Reuses**: the local test server from T3, with a path that never answers
**Requirement**: CAP-35

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] A test lowers the timeout to 1s, calls a URL that never answers, asserts `isError` and `Timed out after 1s`, then gets a successful result from the next call on the same client
- [ ] Gate check passes: Build
- [ ] Test count: 47 tests pass (no silent deletions)

**Tests**: integration
**Gate**: build

**Commit**: `feat(inspect): bound each call by the total timeout`

---

### Phase 2: CI and documents

### T7: Install Chromium in CI

- [ ] Done

**What**: A CI step that installs Chromium and its system dependencies before the tests.
**Where**: `.github/workflows/ci.yml`
**Depends on**: T6
**Reuses**: the existing job
**Requirement**: CAP-44

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `uv run playwright install --with-deps chromium` runs after `uv sync` and before `Tests`
- [ ] Gate check passes: Build
- [ ] Test count: 47 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `ci: install chromium before the tests`

---

### T8: Document inspect_element and the Chromium setup step

- [ ] Done

**What**: CHANGELOG entry for `inspect_element`; the Chromium install command in CONTRIBUTING and in the README's development section.
**Where**: `CHANGELOG.md` (plus one setup line each in the contributing guide and the readme)
**Depends on**: T7
**Reuses**: the command from T7
**Requirement**: CAP-45, CAP-46

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `Unreleased` lists `inspect_element`
- [ ] CONTRIBUTING and README give `uv run playwright install chromium`
- [ ] Gate check passes: Build
- [ ] Test count: 47 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `docs: add inspect_element to the changelog and the chromium setup step`

---

## Phase Execution Map

```
Phase 1 → Phase 2

Phase 1:  T1 → T2 → T3 → T4 → T5 → T6
Phase 2:  T7 → T8
```

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Dependencies | 1 manifest + generated lock | ✅ Granular |
| T2: Config defaults | 1 file | ✅ Granular |
| T3: Capture + tool | 1 capture module, its 2 page scripts, 1 tool and its tests | ⚠️ Cohesive: tests only cross the MCP boundary, so the Capture is not testable without the tool, nor the tool without the Capture |
| T4: Crop + sampled colours | 1 module and its use in the tool | ✅ Granular |
| T5: Clear errors | 7 error messages on one tool | ✅ Cohesive: one behaviour (failing clearly) |
| T6: Total timeout | 1 wrapper + 1 message | ✅ Granular |
| T7: CI | 1 step in 1 file | ✅ Granular |
| T8: Documents | 3 text edits | ⚠️ Cohesive, text only, no behaviour |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T1 | None | none | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | T3 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 | ✅ Match |
| T6 | T5 | T5 → T6 | ✅ Match |
| T7 | T6 (previous phase) | phase order | ✅ Match |
| T8 | T7 | T7 → T8 | ✅ Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: Dependencies | Packaging | none | none | ✅ OK |
| T2: Config defaults | Config | none | none | ✅ OK |
| T3: Capture + tool | MCP tools | integration | integration | ✅ OK |
| T4: Crop + sampled colours | MCP tools | integration | integration | ✅ OK |
| T5: Clear errors | MCP tools | integration | integration | ✅ OK |
| T6: Total timeout | MCP tools | integration | integration | ✅ OK |
| T7: CI | CI | none | none | ✅ OK |
| T8: Documents | Documents | none | none | ✅ OK |
