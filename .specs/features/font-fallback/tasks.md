# font-fallback Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/font-fallback/design.md`
**Status**: Written on 2026-10-12. The maintainer read it the same day, accepted FNT-52 to FNT-54 and had it committed, then asked for one phase per session. Execute: phase 1 (T1 to T3) is done and its Build passed on `9953077`, phase 2 (T4 to T6) is done and its Build passed on `357206d`, and phase 3 (T7 to T9) is done and its Build passed on `ba860c9`, all the same day; phase 4 (T10 and T11) is done and its Build passed on `82fa6cc` on 2026-10-13. The Verifier's first pass returned FAIL on its sensor the same day: its fix round, F1 to F3, is at the end of this file

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec - confirm before Execute. Guidelines found: `CONTRIBUTING.md` and `docs/SPEC.md` (Testing Decisions: one seam, the MCP tool boundary; no unit tests for internal helpers), `tests/test_overlap.py` (style floor). Lessons applied: L-020 (assert the whole order of a returned list: FNT-02, FNT-15, FNT-36), L-036 (a rule on an element's own content, with a child that would change the outcome: FNT-11), L-046 (a limit on a fixture that reads differently on each side of it: FNT-20 to FNT-22), L-019 (a fixture for each clause of a condition: FNT-52 for the half of "Judged element" that FNT-26 does not hold).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (handlers, and the Check, Capture, page script, models and config they drive) | integration, through the in-memory MCP client only, real Chromium; written before the code of the task | 1:1 to the criteria FNT-01 to FNT-39 and FNT-47 to FNT-62; every listed edge case | `tests/test_font_fallback.py` | `uv run pytest tests/test_font_fallback.py` |
| Documents, the roadmap, a run on another platform | none | file evidence (FNT-44 to FNT-46); the gate | - | gate only |

FNT-40 to FNT-43 are not observable through the tool boundary: the Verifier reads them from the files of the task that the Requirement Coverage table names.

## Gate Check Commands

> Generated from codebase - confirm before Execute. The Linux command was run on 2026-10-12 against two existing modules (`tests/test_ping.py` and `tests/test_offscreen_overflow.py`: 37 passed, one minute in all).

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | While iterating on the tests of the slice | `uv run pytest tests/test_font_fallback.py` |
| Full | After every task | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_font_fallback.py` |
| Build | At the end of every phase, in the background | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |
| Linux | T10, and again before a push if `src/` or `tests/` changed after it | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/repo:ro" mcr.microsoft.com/playwright/python:v1.63.0-noble bash -c 'mkdir /work && cd /repo && cp -r pyproject.toml uv.lock README.md CHANGELOG.md src tests /work/ && cd /work && pip install -q uv && uv sync --locked -q && uv run pytest tests/test_font_fallback.py'` (Git Bash, from the repository root; the image is on this machine) |

---

## Execution Plan

Phases are ordered and run sequentially, one phase per session: the maintainer asked for it on 2026-10-12, so that a session closes one piece of work and stays under about 30% of its context. A session holds three tasks at most and runs them in its own window: no sub-agent is offered for the tasks. The Verifier is still a fresh sub-agent, in a session of its own.

| Session | Runs | Closes when |
| --- | --- | --- |
| 1 | Phase 1: T1 to T3 | the Build of phase 1 passes |
| 2 | Phase 2: T4 to T6 | the Build of phase 2 passes |
| 3 | Phase 3: T7 to T9 | the Build of phase 3 passes |
| 4 | Phase 4: T10 and T11 | the Build of phase 4 passes |
| 5 | The Verifier, its fix rounds if any, and T12 on a PASS | `validate_state.py` exits 0 |

A session reads `tasks.md` down to the end of its phase and, of the spec and the design, what its tasks name; it does not read the phases that follow. It ends with the Handoff of `.specs/STATE.md` replaced and committed, and with the prompt for the next session handed to the maintainer: the phase, the hash of the last commit and what weighs in that phase. Pushing the branch and opening the pull request are a session after the fifth, on the maintainer's go-ahead.

Baseline: 368 tests are collected on this branch at `28360bd` (2026-10-12, `uv run pytest --collect-only`). The whole suite takes 18 to 23 minutes.

**Tests first, in every task.** The tests of a task and its fixture are written and run before a line of `src/` is touched, and the run is read: each test is either red for the reason the task gives, or a pin.

- **Red**: the test fails because the rule it asks for is not built yet. The task lists them under "Red before the code". Rules are built in the task whose fixture needs them, so T2 leaves out on purpose what T3, T4, T5 and T7 add.
- **Pin**: the test passes at once, because an earlier task built the rule. A pin a task names a mutant for is proved by it: the mutant is applied to a scratch copy of `src/squint_mcp` (run with `PYTHONPATH` set to the copy, never to the tree) and the test fails there.

**The whole suite.** The gate of a task is Full: the static checks and the test module of the slice. The Build gate runs once per phase, in the background (it does not fit a foreground call), on the commit of the last task of the phase, and the session waits for it: a phase is closed, and its session over, only when it passes. A test of an earlier slice that fails there is run again alone before it counts as a regression, and a regression is fixed in a commit of its own, in the same session. The Build of phase 4 is the gate the spec's Success Criteria name, and the Verifier starts only after it passes.

**The page script.** The spike's scripts were not kept. `font_widths.js` is written from the section "Font script" of `design.md`, which gives its interface, the names of a `font-family`, a copy, the shaping properties and the host.

### Phase 1: The Check, end to end

```
T1 → T2 → T3
```

### Phase 2: What it leaves alone, and its bounds

```
T4 → T5 → T6
```

### Phase 3: Shaping, layout and the other Checks

```
T7 → T8 → T9
```

### Phase 4: The other platform and the documents

```
T10 → T11
```

### Phase 5: Closing

```
T12
```

The Verifier is dispatched in the fifth session, after T11 and the Build of phase 4. T12 is the closing step, written as a task so that FNT-46 has one: it runs only on a PASS, and the Verifier's report already holds the other criteria by then (53 when this was written, 61 with those of the fix round).

---

## Task Breakdown

### Phase 1: The Check, end to end

### T1: Make `font-fallback` a Check name

- [x] Done

**What**: A module `checks/font_fallback.py` whose `check` returns no Finding yet, its entry in `CHECKS`, and the docstring of `detect_visual_bugs` naming the Check: a font the page declares that did not load, one Finding per family. Before them: the literal of FNT-34 in the four assertions of `tests/test_detect_visual_bugs.py` (lines 342, 353, 364 and 376), and a new `tests/test_font_fallback.py` with the test of the description.
**Where**: `src/squint_mcp/checks/font_fallback.py` (with the registry, the tool's docstring, the four literals and the new test module)
**Depends on**: None
**Reuses**: `CHECKS` at `checks/__init__.py:19`; the description test of `tests/test_overlap.py:174`
**Requirement**: FNT-34, FNT-37, FNT-38 (the four literals), FNT-40

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: the four tests that hold the list of valid Checks and the test of the description fail
- [x] `git diff` of `tests/test_detect_visual_bugs.py` shows those four lines and nothing else (two lines each: the literal passes 88 columns, and the formatter joins `in text` to its second line)
- [x] The test of FNT-37 asserts that the description names `font-fallback`, says it reports a font the page declares that did not load, and says one Finding per family
- [x] Gate check passes: Full, with `tests/test_detect_visual_bugs.py` added to the pytest call
- [x] Test count: 369 collected (368 plus the test of the description); none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(checks): register the font-fallback Check`

---

### T2: Report a family that did not load

- [x] Done

**What**: The fixture `font-fallback-bug.html` and its tests, then what makes them pass. `models.py`: `Face`, `LineWidths`, `Element.line_widths` and `Capture.faces` as in the design. `js/font_widths.js`: the Faces, read before any copy is made; for each element with a text node that is not whitespace as a direct child and whose First family has a Face of `error`, two copies of each such node (its `font-family`, its Tail, or `initial` for a list of one name) carrying every `font-` longhand of the element; one host, one layout, the host removed in the same call. `capture.py`: the keyword `fonts` and `_measure_fonts`, after the three fills and before covered text. `checks/__init__.py`: `FONT_CHECKS`; the tool asks for fonts when a Check of it is among the names. `checks/font_fallback.py`: rules 1, 2 and 4 of the design, and of rule 3 the Failed family and `own == tail`. Left to later tasks, each with the test that asks for it: `font-style` in the evidence (T3), "Judged element" (T4), names in another case (T5), the `shaping` argument (T7).
**Where**: `src/squint_mcp/checks/font_fallback.py` (with the models, the page script, the Capture, the registry, the tool, the bug fixture and the test module)
**Depends on**: T1
**Reuses**: `_measure_covered_text` (`capture.py:168`) as the form of `_measure_fonts`; `globalThis.__squintElements` (`collect_elements.js:189`); `COVERED_TEXT_CHECKS` and how the tool reads it (`detect_visual_bugs.py:91`); the shape of `checks/offscreen_overflow.py`; `tests/helpers.py`; `checks-order.html` as the form of a fixture in Ahem
**Requirement**: FNT-01 to FNT-04, FNT-07, FNT-13, FNT-28, FNT-33, FNT-35, FNT-47; from file evidence FNT-41, FNT-42, FNT-43

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: every test of the task fails but that of FNT-35, which holds before and after. The tests of FNT-04 and FNT-47 assert that the result has Findings, so that neither holds on an empty one
- [x] The test of FNT-02 asserts the whole list of `(selector, severity, family, elements)` in order (L-020); the test of FNT-01 that `#lead` and `#note` get no Finding of their own
- [x] The test of FNT-13 reads both viewports in one call: `#narrow` has one Finding at 390 × 844 and none at 1440 × 900
- [x] The host and every copy are styled through the style object, each declaration `!important` after `all: initial`; no style of the page is changed
- [x] A Capture taken without `fonts` makes the same page calls as before this task
- [x] `checks/font_fallback.py` imports neither `playwright` nor `config`, and compares the two widths with `==`
- [x] The three limits the design accepts are marked `ponytail:` in the script (a Tail that asks for a font no text had used; a name with a hexadecimal escape; what a copy does not carry)
- [x] Gate check passes: Full
- [x] Test count: 369 plus the tests of this task (ten at least, one per criterion); none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(checks): report a font the page declares that did not load`

---

### T3: Say in the evidence which Face the element asked for

- [x] Done

**What**: The test of FNT-27, then `"font-style"` in `CAPTURE_COMPUTED_PROPERTIES` (its comment says what the property is for) and in the styles the Finding carries: `font-family`, `font-weight` and `font-style`.
**Where**: `src/squint_mcp/config.py` (with the evidence of the Check and the test)
**Depends on**: T2
**Reuses**: how `z-index` joined the tuple in slice 8 (`config.py:74`)
**Requirement**: FNT-27

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: the test fails on `evidence.computed`, which has no `font-style`
- [x] The test compares the Finding of `#heading` with the whole literal of the spec
- [x] `INSPECT_COMPUTED_PROPERTIES` is unchanged, so `inspect_element` does not return `font-style`
- [x] Gate check passes: Full; then Build for phase 1, in the background
- [x] Test count: the count after T2 plus one; none deleted

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `feat(checks): carry font-style in the evidence of font-fallback`

---

### Phase 2: What it leaves alone, and its bounds

### T4: Leave out text that is hidden or paints no box

- [x] Done

**What**: The fixture `font-fallback-clean.html` with the cases of FNT-16 to FNT-19 and FNT-23 to FNT-25, and its tests; then "Judged element" in rule 3 of the Check: `own_text_boxes` is not empty and `computed["visibility"]` is `visible`.
**Where**: `src/squint_mcp/checks/font_fallback.py` (with the clean fixture and its tests)
**Depends on**: T3
**Reuses**: `Element.own_text_boxes` (`models.py:81`); the form of `test_a_page_of_overlaps_that_are_meant_has_no_findings` (`tests/test_overlap.py:214`)
**Requirement**: FNT-16 to FNT-19, FNT-23 to FNT-25

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: the tests of FNT-16 and FNT-23 fail on a Finding of `Hidden Brand` on `#hidden`
- [x] The test of FNT-16 calls the tool without `checks`: the page is clean for the other four Checks too, and the response has no image block and the one text block `No findings in 1 viewport.`
- [x] One test per criterion names the element or the family it holds silent
- [x] The test of FNT-18 fails on a scratch copy in which the family judged is the first of the list that has a Face
- [x] The comment of the fixture gives the status of its eight Faces, four `error` and four `unloaded`, as read from the page in Chromium when the fixture was written: the tool does not show a status
- [x] The half "paints at least one box" is written here with the other, from the Term of the spec; its test is FNT-52, a pin of T6, whose case is in the bounds fixture
- [x] Gate check passes: Full
- [x] Test count: the count after T3 plus the tests of this task (seven at least); none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(checks): judge only text that is on the page and seen`

---

### T5: Match a family whatever the case of its name

- [x] Done

**What**: The fixture `font-fallback-bounds.html`, whole: every case the spec places in it (FNT-05, FNT-06, FNT-08 to FNT-12, FNT-20 to FNT-22, FNT-26, FNT-29 to FNT-31, FNT-48, FNT-52 to FNT-54). The tests of which family is reported, for which Face and under which name; then family names compared in lower case, in the script and in the Check, and reported as the first Face of the family has them.
**Where**: `src/squint_mcp/checks/font_fallback.py` (with the page script, the bounds fixture and its tests)
**Depends on**: T4
**Reuses**: the open shadow tree and `[data-testid="shadow-text"]` of `overlap-bounds.html`
**Requirement**: FNT-05, FNT-06, FNT-08 to FNT-10, FNT-15, FNT-29, FNT-48, FNT-53

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: the tests of FNT-06, FNT-15 and FNT-29 fail for want of the Finding of `Missing Brand` on `#lower`
- [x] The test of FNT-15 asserts the whole list of `(selector, family, elements)` in order, and `minor` on every Finding (L-020)
- [x] The test of FNT-08 fails on a scratch copy in which the copies do not carry `font-weight`
- [x] The test of FNT-53 fails on a scratch copy in which the script and the Check both take a Face of any status but `loaded` for one that failed. Changed in one of the two alone the test still passes: the family is compared twice by design
- [x] The test of FNT-29 asserts `family` equal to `Missing Brand` and the `font-family` of `evidence.computed` as computed, `"missing brand", Ahem`
- [x] No family of the fixture has the name of a font a machine can have installed, and each rule has a family of its own
- [x] Gate check passes: Full
- [x] Test count: the count after T4 plus the tests of this task (nine at least); none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(checks): match a font family whatever the case of its name`

---

### T6: Pin own text, the one line and the evidence

- [x] Done

**What**: The tests of the cases of `font-fallback-bounds.html` that T5 did not read: what an element is judged on, the widths of one line, the element a Finding sits on and what it carries, and every `selector` passed to `inspect_element`. No change to `src/`: every test is a pin.
**Where**: `tests/test_font_fallback.py`
**Depends on**: T5
**Reuses**: `findings_on` of `tests/helpers.py`; the test of OVL-53 as the form of FNT-32
**Requirement**: FNT-11, FNT-12, FNT-20 to FNT-22, FNT-26, FNT-30 to FNT-32, FNT-52, FNT-54

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The tests of FNT-20, FNT-21 and FNT-22 fail on a scratch copy in which the Check counts an element without comparing its two widths (L-046)
- [x] The test of FNT-11 fails on a scratch copy in which the script copies the whole text content of an element in place of its own text nodes (L-036)
- [x] The test of FNT-26 fails on a scratch copy in which the Check does not read `visibility`
- [x] The test of FNT-52 fails on a scratch copy in which the Check does not read `own_text_boxes` (L-019)
- [x] The test of FNT-54 fails on a scratch copy in which the script measures only the first text node of an element
- [x] The test of FNT-30 fails on a scratch copy in which a copy is left free to wrap, and asserts both `textWidthPx` equal to 280 and a `box` 100 wide
- [x] The test of FNT-32 passes every `selector` of the Findings of the bug fixture, at both viewports, and of the bounds fixture to `inspect_element` and compares the `box`
- [x] Gate check passes: Full; then Build for phase 2, in the background
- [x] Test count: the count after T5 plus the tests of this task (eleven at least); none deleted

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `test(font-fallback): pin own text, the one line and the evidence`

---

### Phase 3: Shaping, layout and the other Checks

### T7: Measure a text with the styles that shape it

- [x] Done

**What**: The fixture `font-fallback-shaping.html` with the cases of FNT-49 to FNT-51, and its tests; then `TEXT_SHAPING_PROPERTIES` in config with the value and the source of the design, passed to the script as `shaping` and set on each copy with the computed value of the element.
**Where**: `src/squint_mcp/js/font_widths.js` (with the config, the call in the Capture, the shaping fixture and its tests)
**Depends on**: T6
**Reuses**: how `capture.py` passes `CAPTURE_COMPUTED_PROPERTIES` to the collector
**Requirement**: FNT-49 to FNT-51; from file evidence FNT-43 (config gains a list of names and no threshold)

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Red before the code: the test of FNT-49 fails on a Finding of `Mixed` on `#upper-mixed`, and that of FNT-51 on a `textWidthPx` of 200 (the fixture holds `#lower-mixed` after `#upper-mixed`, the same text without the transform: alone, `#upper-mixed` asks for the capitals only, the Face of the small letters stays `unloaded` and `Mixed` is not a Failed family; the Finding of `Mixed` sits on `#lower-mixed` and counts one element)
- [x] The test of FNT-50 is a pin: it fails on a scratch copy in which the copies do not carry `font-style`
- [x] The script holds no list of property names of its own: the `font-` longhands come from the computed style and the rest from `shaping`
- [x] Gate check passes: Full
- [x] Test count: the count after T6 plus the tests of this task (three at least); none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(capture): measure a text with the styles that shape it`

---

### T8: Hold the two widths to the layout of the boxes

- [x] Done

**What**: The fixture `font-fallback-monospace.html` as FNT-14 words it (the family is `Brand` and the page 3900px high; the row of the design's spike calls the family `Mono Brand`, and the spec is the one followed) and its test. No change to `src/`: the test is a pin of the order inside `capture()`.
**Where**: `tests/test_font_fallback.py` (with the monospace fixture)
**Depends on**: T7
**Reuses**: nothing
**Requirement**: FNT-14

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test asserts exactly one Finding, on `#code`, with `family` equal to `Brand`, `elements` equal to 1 and `textWidthPx` equal to the `w` of its `box` rounded to two decimal places; it compares no width with a figure
- [x] On Windows the test fails on a scratch copy in which `capture()` does not call `_settle_layout`
- [x] Gate check passes: Full
- [x] Test count: the count after T7 plus one; none deleted

**Tests**: integration
**Gate**: full

**Commit**: `test(font-fallback): hold the two widths to the layout of the boxes`

---

### T9: Hold the Check with the other Checks and on a page of a thousand texts

- [x] Done

**What**: The fixtures `font-fallback-order.html` and `font-fallback-many.html`, and the tests of the order of Findings across Checks and of the 1,000 elements. No change to `src/`.
**Where**: `tests/test_font_fallback.py` (with the two fixtures)
**Depends on**: T8
**Reuses**: `checks-order.html` and `overlap-many.html` as the forms of the two fixtures
**Requirement**: FNT-36, FNT-39

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The test of FNT-36 asserts the whole list of `(selector, check)` pairs in order (L-020), and every Finding is `minor`
- [x] The test of FNT-39 asserts `isError: false`, exactly one Finding and `elements` equal to 1000
- [x] Gate check passes: Full; then Build for phase 3, in the background
- [x] Test count: the count after T8 plus two; none deleted

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `test(font-fallback): hold the Check with the others and on a thousand texts`

---

### Phase 4: The other platform and the documents

### T10: Run the tests of the slice on Linux

- [x] Done

**What**: `tests/test_font_fallback.py` run in the Playwright image for Docker with the Linux command of the gate table, and the result written under this task: the date, the id of the image and the count of tests passed.
**Where**: `.specs/features/font-fallback/tasks.md`
**Depends on**: T9
**Reuses**: the image `mcr.microsoft.com/playwright/python:v1.63.0-noble`, the same Chromium 153 as Windows
**Requirement**: the third Goal of the spec and its third Success Criterion: FNT-01 to FNT-39 and FNT-47 to FNT-54 have the same outcome on Windows and on Linux

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Every test of the module passes in the image, and their count is the count collected on Windows
- [x] A test that fails there is fixed in the code or in the fixture, in a commit of its own, never by an assertion that depends on the platform; the module then passes again on both
- [x] The result is written here
- [x] Gate check passes: Linux

**Result** (2026-10-13): `45 passed in 160.04s (0:02:40)` in `mcr.microsoft.com/playwright/python:v1.63.0-noble`, image id `sha256:59fe35832a79d1324e778b737760b2afc11cffcbaeba325012f96cabae832a75` (`docker image inspect`; created 2026-09-15), on `c1aeef3` with a clean tree: Python 3.12.3, pytest 9.1.1, Docker engine 28.0.4. The count is the 45 collected on Windows. No test failed there: nothing was fixed and no assertion was changed.

**Second run** (2026-10-13, after the first fix round): `53 passed in 153.82s (0:02:33)` in the same image, id `sha256:59fe35832a79d1324e778b737760b2afc11cffcbaeba325012f96cabae832a75`, on `76640b8` with a clean tree: Python 3.12.3, pytest 9.1.1, Docker engine 28.0.4. The count is the 53 collected on Windows: the 45 of the first run and the eight of F1 to F3. No test failed there: nothing was fixed and no assertion was changed.

**Tests**: none
**Gate**: linux

**Commit**: `docs(specs): record the Linux run of the font-fallback tests`

---

### T11: Document the Check

- [x] Done

**What**: The CHANGELOG entry under the unreleased version (one Finding per family, always `minor`, only the first family of `font-family` and only when the page declares it, and what is not reported: a family that is only named, a font that loaded and is not used, text of pseudo-elements, text of `visibility: hidden`), and the README naming five Checks.
**Where**: `CHANGELOG.md` (with the README)
**Depends on**: T10
**Reuses**: the entry of `overlap` as the form; the sentence of `README.md:45`
**Requirement**: FNT-44, FNT-45

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The CHANGELOG entry says each of the things FNT-44 lists
- [x] The README gives the number of Checks as five and says what `font-fallback` reports
- [x] Gate check passes: Full; then Build for phase 4, in the background. It is the gate of the spec's Success Criteria, and the Verifier waits for it
- [x] Test count: the count after T9; none deleted

**Tests**: none
**Gate**: full, then build for the phase

**Commit**: `docs: document the font-fallback Check`

---

### Phase 5: Closing

### T12: Mark slice 9 as done

- [ ] Done

**What**: After the Verifier's PASS: `docs/ROADMAP.md` shows slice 9 as `concluída`, in the table and in its section, with a link to this feature's directory; the Status column of the spec's traceability table and the Handoff of `.specs/STATE.md` say the same.
**Where**: `docs/ROADMAP.md` (with the traceability table of the spec and the Handoff)
**Depends on**: T11
**Reuses**: how slice 8 was closed
**Requirement**: FNT-46

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `validation.md` holds a PASS for the other 61 criteria (53, and the eight of the fix round), and FNT-46 is added to it from file evidence once this task is done
- [ ] `validate_state.py font-fallback` exits 0
- [ ] If a fix round changed `src/` or `tests/` after T10, the Linux gate is run again and its result written under T10
- [ ] Nothing is pushed and no pull request is opened: both wait for the maintainer's go-ahead

**Tests**: none
**Gate**: full

**Commit**: `docs(roadmap): mark slice 9 as done`

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Verifier → Phase 5

Phase 1:  T1 ------→ T2 ------→ T3
Phase 2:  T4 ------→ T5 ------→ T6
Phase 3:  T7 ------→ T8 ------→ T9
Phase 4:  T10 -----→ T11
Phase 5:  T12
```

Execution is strictly sequential, one phase per session (Execution Plan). T12 is taken in the session of the Verifier, after its PASS.

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: The name | 1 registry entry, 1 docstring clause, 4 literals, 1 test | ✅ Granular |
| T2: Report a family | 1 Check with what the Capture reads for it, 1 fixture and its tests | ⚠️ OK: a Finding is observable only once the models, the script, the Capture and the Check all exist; tests come first, so none of them can be a task of its own |
| T3: `font-style` | 1 property in 2 tuples, 1 test | ✅ Granular |
| T4: Judged element | 1 condition, 1 fixture and its tests | ✅ Granular |
| T5: Names in another case | 1 rule, 1 fixture and the tests of its families | ✅ Granular |
| T6: Own text and the line | tests of 1 fixture | ✅ Granular |
| T7: Shaping | 1 list of names through 3 files, 1 fixture and its tests | ⚠️ OK: one argument from config to the copies |
| T8: Monospace | 1 fixture, 1 test | ✅ Granular |
| T9: With the others | 2 small fixtures with their tests | ⚠️ OK: both hold the Check among the others |
| T10: Linux | 1 run, 1 record | ✅ Granular |
| T11: Documents | 2 documents | ✅ Granular |
| T12: Closing | 1 roadmap row and section, the Handoff | ✅ Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T1 | None | first of phase 1 | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 | ✅ Match |
| T4 | T3 | first of phase 2, after phase 1 | ✅ Match |
| T5 | T4 | T4 → T5 | ✅ Match |
| T6 | T5 | T5 → T6 | ✅ Match |
| T7 | T6 | first of phase 3, after phase 2 | ✅ Match |
| T8 | T7 | T7 → T8 | ✅ Match |
| T9 | T8 | T8 → T9 | ✅ Match |
| T10 | T9 | first of phase 4, after phase 3 | ✅ Match |
| T11 | T10 | T10 → T11 | ✅ Match |
| T12 | T11 | first of phase 5, after phase 4 | ✅ Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: The name | MCP tools (registry, tool description) | integration | integration | ✅ OK |
| T2: Report a family | MCP tools (Check, Capture, page script, models) | integration | integration | ✅ OK |
| T3: `font-style` | MCP tools (config, Check) | integration | integration | ✅ OK |
| T4: Judged element | MCP tools (Check) | integration | integration | ✅ OK |
| T5: Names in another case | MCP tools (Check, page script) | integration | integration | ✅ OK |
| T6: Own text and the line | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T7: Shaping | MCP tools (page script, config, Capture) | integration | integration | ✅ OK |
| T8: Monospace | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T9: With the others | MCP tools (tests of the Check) | integration | integration | ✅ OK |
| T10: Linux | a run on another platform | none | none | ✅ OK |
| T11: Documents | documents | none | none | ✅ OK |
| T12: Closing | the roadmap | none | none | ✅ OK |

No task changes `src/` without tests of its own, written first.

---

## Requirement Coverage

| Requirements | Task |
| --- | --- |
| FNT-34, FNT-37, FNT-38, FNT-40 | T1 (FNT-38: the four literals; that no other test of an earlier slice changes is held by the Build of every phase) |
| FNT-01 to FNT-04, FNT-07, FNT-13, FNT-28, FNT-33, FNT-35, FNT-47 | T2 |
| FNT-41, FNT-42, FNT-43 | T2, from file evidence (FNT-43 is read again after T7, which adds to config) |
| FNT-27 | T3 |
| FNT-16 to FNT-19, FNT-23 to FNT-25 | T4 |
| FNT-05, FNT-06, FNT-08 to FNT-10, FNT-15, FNT-29, FNT-48, FNT-53 | T5 |
| FNT-11, FNT-12, FNT-20 to FNT-22, FNT-26, FNT-30 to FNT-32, FNT-52, FNT-54 | T6 |
| FNT-49 to FNT-51 | T7 |
| FNT-14 | T8 |
| FNT-36, FNT-39 | T9 |
| FNT-44, FNT-45 | T11, from file evidence |
| FNT-46 | T12, from file evidence |

54 of 54 mapped. T10 holds no criterion of its own: it runs those of T1 to T9 on Linux.

---

## Criteria added with the tasks

Three rules that the Terms of the spec state and the design builds were held by none of the 51 criteria the Tasks phase started from: a mutant of each passed every test. The maintainer accepted a criterion for each on 2026-10-12, each on one case more of `font-fallback-bounds.html`; the premises were measured the same day on Windows and on Linux ([`context.md`](context.md)).

| Criterion | Rule | Case | Task |
| --- | --- | --- | --- |
| FNT-52 | "Paints at least one box" (Judged element) | `#unshown`, of `display: none`, before `#shown` in `Unshown Brand` | T6 |
| FNT-53 | Only `error` makes a Failed family | `#out-of-range`, whose text is outside the `unicode-range` of the one Face of `Upper Only`, which stays `unloaded` | T5 |
| FNT-54 | The widths of several text nodes are added | `#split`, with a text node on each side of a child | T6 |

FNT-15 gained the rows of `#shown` and `#split`.

---

## Fixes of the first validation pass

The Verifier's first pass ([`validation.md`](validation.md), 2026-10-13) covered 53 of 53 criteria, found no defect in `src/` and killed the eleven mutants the tasks name. It failed the feature on its sensor: ten mutants of its own pass the 45 tests, on rules that the Terms, the Assumptions or the design state, that the code implements and that no criterion held. The three tasks below add the criteria FNT-55 to FNT-62, their fixture cases and their tests through the MCP boundary. None changes `src/`. A new test is done when it fails under the mutant it is for, applied to a scratch copy of `src/squint_mcp` as the report gives the row, and passes on the copy without it.

```
F1 → F2 → F3
```

Baseline: 413 tests are collected and the 45 of the module pass on `ab1dbab` (2026-10-13). The matrix and the gate commands at the top of this file apply; the gate of a fix task is Full. The Build runs once, on the commit of F3, and the Linux gate with it: its result is written under T10 as a second run.

**Not yet read by the maintainer.** The eight criteria, the word on whitespace in the Term "Judged element" (and in the row "Which elements are judged" of the Assumptions and the row of Out of Scope on text that is not seen, which said the same thing in other words) and the clause of FNT-49 that names `#lower-mixed` (residual R3 of the report) were written from the report under the orchestrator's defaults. Each pins what the accepted spec and design already say, and none changes a behaviour. They wait for the maintainer's reading, as FNT-52 to FNT-54 did.

| Fix of the report | Mutant | The rule, and where it was stated | Criterion | Case | Task |
| --- | --- | --- | --- | --- | --- |
| Fix 1 | C16b | The two Line widths are equal (Term "Falls back", FNT-43) | FNT-55 | `#broad-normal`, in a loaded Face that is wider than its Tail, before `#broad-bold` in `Broad` | F1 |
| Fix 2 | C5 | The computed `visibility` is `visible` (Term "Judged element") | FNT-56 | `#folded`, of `visibility: collapse`, before `#unfolded` in `Folded Brand` | F1 |
| Fix 6 (SP-1) | S7, S8 | A text node that is whitespace is not measured ([`design.md`](design.md), "Font script"); the Term now says it | FNT-57 | `#spaces`, five spaces that `white-space: pre` keeps, before `#after-spaces` in `Space Brand` | F1 |
| Fix 3 | C2 | A family is reported under the name of the first of its Faces (Assumptions, "The name a family is reported under") | FNT-58 | `Dual` and then `DUAL`, the two Faces of one family | F2 |
| Fix 4 | S1b | A `font-family` is split "at the commas outside strings" (design, "Font script") | FNT-59 | `#comma`, in `"Acme, Inc"` | F2 |
| Fix 5 | S1a, S2b | "A backslash taking the character after it"; a name is compared "without the quotes and the escapes" (design, "Font script") | FNT-60 | `#inch`, in the family `Vinyl 12"` | F2 |
| Fix 7 | CFG-dir | `direction` is one of `TEXT_SHAPING_PROPERTIES` (design, Config) | FNT-61 | `#turned`, a block of `direction: rtl` in the font of `serif` | F3 |
| Fix 8 | CFG-tr | `text-rendering` is one of them (design, Config) | FNT-62 | `#swift`, of `text-rendering: optimizeSpeed`, in Calibri or FreeSerif | F3 |

**Fix 7 and Fix 8 were measured before a criterion was written** (2026-10-13, Chromium 153.0.8010.12 on Windows 11 and in the Playwright image for Docker; the scripts were not kept). The report had found 0.03px for `direction` and nothing for `text-rendering`.

- **`direction`.** In a block that runs from right to left, a mark at the end of a text of Latin letters takes the direction of the block and is shaped apart from the letter before it, so the two are not kerned. In the font of `serif` at 20px, `Y.` is 16.88px wide from left to right and 19.45px from right to left; `PLAY.` is 52.81px and 55.39px. The figures are the same on both platforms (Times New Roman on Windows, Liberation Serif in the image). With `direction` out of the list the tool returns a `textWidthPx` of 52.81 for `#turned`, whose box is 55.39 wide, on both. The case is a block of its own (`inline-block`) on purpose: on an inline element `direction` has no effect on the page without `unicode-bidi`, and the copy, which is a block of its own, is then the one that is off (residual R4 of the report: no Finding is lost or gained by it). FNT-61 says nothing of that case.
- **`text-rendering`.** Of its four values only `optimizeSpeed` changed a width, and only in a font with ligatures: it turns them off and leaves kerning on. No generic family gives such a font on either platform (seven generic families, sixteen sizes from 6px to 72px, eight texts: no width differs). By name the fonts that do are Calibri, Candara, Constantia, Corbel, Gabriola, Palatino Linotype, Segoe Script and Sitka Text on Windows, and FreeSerif, FreeSans and Loma in the image. `fifth office file` at 20px is 112.69px wide in Calibri and 113.84px without its ligatures; in FreeSerif, 110.06px and 117.48px. With `text-rendering` out of the list the tool returns 112.69 for a box 113.84 wide on Windows, and 110.06 for 117.48 on Linux. So the Tail of `#swift` names two fonts of the machine, `Calibri, FreeSerif`. What the test asserts holds whatever font the machine has; the mutant dies only where one of the two is installed. The maintainer may prefer a font file of the repository that has a ligature, which would make the widths exact, or to take the name out of the list.

### F1: Hold what falls back from the other side

- [x] Done

**What**: The fixture `font-fallback-judged.html` with three cases, and a test each: an element in a loaded Face of a Failed family that is wider than its Tail (FNT-55), an element of `visibility: collapse` before the first that falls back (FNT-56) and an element whose Own text is five spaces that `white-space: pre` keeps (FNT-57). No change to `src/`: every test is a pin.
**Where**: `tests/test_font_fallback.py` (with `tests/fixtures/font-fallback-judged.html`)
**Depends on**: None
**Reuses**: the form of `font-fallback-bounds.html`; `of_family`, `sits_on` and `reported` of the test module
**Requirement**: FNT-55, FNT-56, FNT-57

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The fixture is new: no fixture and no assertion of T1 to T9 changes
- [x] The comment of the fixture gives the status of its Faces, as read from the page in Chromium on Windows and in the Playwright image
- [x] Each test fails under its mutant on a scratch copy and passes on the copy without it: C16b (FNT-55), C5 (FNT-56), S7 and S8 (FNT-57)
- [x] C16a, the other side of the equality, still dies (FNT-20)
- [x] Gate check passes: Full
- [x] Test count: 48 in the module, 416 collected; none deleted

**Tests**: integration
**Gate**: full

**Commit**: `test(font-fallback): hold what falls back from the other side`

---

### F2: Pin the names a family is read and reported under

- [x] Done

**What**: The fixture `font-fallback-names.html` with three cases, and a test each: a family whose two Faces write its name in two cases (FNT-58), a family whose name holds a comma (FNT-59) and one whose name holds a quotation mark, which a computed `font-family` writes with a backslash (FNT-60). No change to `src/`: every test is a pin. The hexadecimal escape stays the limit the design accepts.
**Where**: `tests/test_font_fallback.py` (with `tests/fixtures/font-fallback-names.html`)
**Depends on**: F1
**Reuses**: the form of `font-fallback-bounds.html`; `sits_on` and `reported` of the test module
**Requirement**: FNT-58, FNT-59, FNT-60

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The fixture is new: no fixture and no assertion of T1 to T9 changes
- [x] The comment of the fixture gives the name each Face has in `document.fonts` and the computed `font-family` of `#inch`, as read from the page on both platforms
- [x] Each test fails under its mutants on a scratch copy and passes on the copy without them: C2 (FNT-58), S1b (FNT-59), S1a and S2b (FNT-60)
- [x] The case of FNT-59 holds no backslash and that of FNT-60 no comma: S1b leaves the test of FNT-60 passing, S1a and S2b that of FNT-59
- [x] Gate check passes: Full
- [x] Test count: 51 in the module, 419 collected; none deleted

**Tests**: integration
**Gate**: full

**Commit**: `test(font-fallback): pin the names a family is read and reported under`

---

### F3: Pin the direction and the text-rendering a copy takes

- [x] Done

**What**: Two cases after the last of `font-fallback-shaping.html`, and a test each: a block of `direction: rtl` whose text ends in a full stop (FNT-61) and a text of `text-rendering: optimizeSpeed` in a font with ligatures (FNT-62). Both are in fonts of the machine, so each test compares `textWidthPx` with the width of the box of the same Finding, as FNT-14 does, and with no figure. No change to `src/`: both tests are pins.
**Where**: `tests/test_font_fallback.py` (with `tests/fixtures/font-fallback-shaping.html`)
**Depends on**: F2
**Reuses**: the form of the test of FNT-14
**Requirement**: FNT-61, FNT-62

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The two cases come after `#spaced`: nothing already placed moves, and the tests of FNT-49 to FNT-51 pass unchanged
- [x] Each test fails under its mutant on a scratch copy, on Windows and in the Playwright image, and passes on the copy without it: CFG-dir (FNT-61), CFG-tr (FNT-62)
- [x] CFG-tt, CFG-ls and CFG-ws, the other three names of the list, still die (FNT-49, FNT-51)
- [x] Gate check passes: Full
- [x] Test count: 53 in the module, 421 collected; none deleted

**Tests**: integration
**Gate**: full

**Commit**: `test(font-fallback): pin the direction and the text-rendering of a copy`

---

### Requirement coverage of the fixes

| Requirements | Task |
| --- | --- |
| FNT-55, FNT-56, FNT-57 | F1 |
| FNT-58, FNT-59, FNT-60 | F2 |
| FNT-61, FNT-62 | F3 |

8 of 8 mapped; with the table of "Requirement Coverage", 62 of 62.

### The mutants of the report, run again

Each of the ten was applied alone to a fresh copy of `src/squint_mcp` outside the repository, as the report gives the row, and the whole module was run against the copy with `-x` (2026-10-13, Windows, on `76640b8` with a clean tree; a plugin checked that `squint_mcp` came from the copy). The copy without a mutant passed first: 53 passed in 161.60s. `src/` is as it was on `ab1dbab`.

| Mutant | Result | The test that fails | Its assertion |
| --- | --- | --- | --- |
| C16b | Killed | FNT-55 | `('#broad-normal', 2) == ('#broad-bold', 1)` |
| C5 | Killed | FNT-56 | `('#folded', 2) == ('#unfolded', 1)` |
| C2 | Killed | FNT-58 | `('DUAL', 2) == ('Dual', 2)` |
| S1b | Killed | FNT-59 | `[] == [('#comma', 'Acme, Inc')]` |
| S1a | Killed | FNT-60 | `[] == [('#inch', 'Vinyl 12"')]` |
| S2b | Killed | FNT-60 | `[] == [('#inch', 'Vinyl 12"')]` |
| S7 | Killed | FNT-57 | `('#spaces', 2) == ('#after-spaces', 1)` |
| S8 | Killed | FNT-57 | `('#spaces', 2) == ('#after-spaces', 1)` |
| CFG-dir | Killed | FNT-61 | `52.81 == 55.39` |
| CFG-tr | Killed | FNT-62 | `112.69 == 113.84` |

Ten of ten killed, none alive. CFG-dir and CFG-tr were also run in the Playwright image, each against its test: both die there, on `52.81 == 55.39` and on `110.06 == 117.48`. A run with `-x` stops at its first failure: in each, every test of the module before the one named passed, the 45 of T1 to T9 among them, as in the report.
