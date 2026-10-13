# extract-tokens Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/extract-tokens/design.md` (approved by the maintainer on 2026-10-13, AD-009 with it)
**Status**: Approved by the maintainer on 2026-10-13, as written. The three points that waited for the maintainer's word are answered, under "Waiting for the maintainer" at the end of this file.

---

## Test Coverage Matrix

> Generated from codebase, project guidelines and spec - confirm before Execute. Guidelines found: `CONTRIBUTING.md` and `docs/SPEC.md` (Testing Decisions: one seam, the MCP tool boundary; no unit tests for internal helpers), the spec's Assumptions (one test below the seam, for ΔE2000), `tests/test_inspect_element.py` (style floor). Lessons applied: L-020 (the whole order of a list with ties: TOK-01, TOK-52, and the whole lists of T19 and T22), L-021 and L-046 (a threshold with a case at it and a case past it: TOK-45 for 1px, TOK-62 and TOK-63 for the Limit; for ΔE the two sides the spec has, in T20), L-050 (every rule of Terms and the fixture that tells it: "Terms and the fixture that tells each"), L-019 (one fixture per clause: TOK-21, TOK-24, TOK-28, TOK-29, TOK-33, TOK-35, TOK-51), L-065 (a rule that picks one item: TOK-41, TOK-44, TOK-46, TOK-62), L-036 (an element judged on its own content: TOK-15, TOK-25, TOK-37).

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (the handler, and what it drives: `tokens.py`, the parsing and the Lab of `color.py`, the Capture, the page scripts, the models, the config) | integration, through the in-memory MCP client only, real Chromium; written before the code of the task | 1:1 to TOK-01 to TOK-73, TOK-78 and TOK-79 | `tests/test_extract_tokens.py` | `uv run pytest tests/test_extract_tokens.py` |
| The ΔE2000 function | unit: the one test below the seam, which the spec's Assumptions allow | TOK-74: the 34 pairs | `tests/test_color.py` | `uv run pytest tests/test_color.py` |
| The contract of the Capture, before a tool reads it (phase 2) | integration: the tests of the earlier tools, with no assertion changed | TOK-77. No new test: no tool reads the three new facts until phase 3, and the testing decision allows no test that calls `capture(...)` | the nine existing modules | the Capture gate, then the Build |
| Config constants, test data, documents, the roadmap, a run on another platform | none | file evidence (TOK-75, TOK-76); the gate | - | gate only |

TOK-75 and TOK-76 are not observable through the tool boundary: the Verifier reads them from the files of T1 and T29.

## Gate Check Commands

> Generated from codebase - confirm before Execute. `tests/test_inspect_element.py` was run on 2026-10-13 at `486004c`: 55 passed in 2 minutes 2 seconds. The Linux command is that of slice 9 with the modules of this slice; it was not run for this file.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Static | T1 and T2, before the slice has a test module | `uv run pyright && uv run ruff check && uv run ruff format --check` |
| Quick | While iterating on the tests of the slice | `uv run pytest tests/test_color.py tests/test_extract_tokens.py` (the second module exists from T8 on) |
| Full | After every task from T3 on | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest tests/test_color.py tests/test_extract_tokens.py` |
| Capture | T4 to T7, which change what every tool reads | Full, with `tests/test_inspect_element.py` added to the pytest call |
| Build | At the end of every phase, in the background | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |
| Linux | T28, and again before a push if `src/` or `tests/` changed after it | `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/repo:ro" mcr.microsoft.com/playwright/python:v1.63.0-noble bash -c 'mkdir /work && cd /repo && cp -r pyproject.toml uv.lock README.md CHANGELOG.md src tests /work/ && cd /work && pip install -q uv && uv sync --locked -q && uv run pytest tests/test_color.py tests/test_extract_tokens.py'` (Git Bash, from the repository root) |

---

## Execution Plan

Phases are ordered and run sequentially. A session runs one batch of whole phases, seven tasks at most, in its own window: no sub-agent is offered for the tasks. The Verifier is a fresh sub-agent, in a session of its own.

| Session | Runs | Tasks | Closes when |
| --- | --- | --- | --- |
| 1 | Phase 1 and phase 2 | T1 to T7 | the Build of phase 2 passes |
| 2 | Phase 3 | T8 to T13 | the Build of phase 3 passes |
| 3 | Phase 4 | T14 to T19 | the Build of phase 4 passes |
| 4 | Phase 5 | T20 to T23 | the Build of phase 5 passes |
| 5 | Phase 6 | T24 to T29 | the Build of phase 6 passes |
| 6 | The Verifier, its fix rounds if any, and T30 on a PASS | T30 | `validate_state.py extract-tokens` exits 0 |

A session reads `tasks.md` down to the end of its batch and, of the spec and the design, what its tasks name; it does not read the phases that follow. It ends with the Handoff of `.specs/STATE.md` replaced and committed, and with the prompt for the next session handed to the maintainer. Commits stay local: pushing the branch and opening the pull request wait for the maintainer's go-ahead.

Baseline: 421 tests are collected on this branch at `486004c` (2026-10-13, `uv run pytest --collect-only`). The whole suite took 20 to 24 minutes on the Builds of slice 9.

**Tests first, and every test seen failing.** The tests of a task and its fixture are written and run before a line of `src/` is touched, and the run is read. Each test is one of two things:

- **Red**: it fails because the rule it asks for is not built yet. Rules are built in the task whose fixture needs them: T9 to T12 build what `tokens-page.html` forces and leave out on purpose what phases 4 to 6 add.
- **Pin**: it passes at once, because an earlier task built the rule. A pin is seen failing under the mutant its task names: the mutant is applied to a scratch copy of `src/squint_mcp` (run with `PYTHONPATH` set to the copy, never to the tree) and the test fails there. A task lists, under "Rule dropped", what each of its tests must fail without; whether a test turned out red or a pin is written under the task when it is done.

A pin with no rule of ours behind it (a message that `capture(...)` writes, a value Chromium computes) says so in its task and has no mutant.

**Fixtures.** Every element of a fixture is a `div` or a `span`: an `h1`, a `p` or a `button` brings margins, a border and a font from the browser's stylesheet that the criteria do not list. Each fixture but `tokens-default.html` sets `margin: 0` on `html` and `body` and gives every element its styles explicitly. `tokens-used.html` and `tokens-groups.html` grow task by task: a task adds the elements its criteria name, so that a value no rule reads yet cannot fail the whole page.

**The module of the slice.** `tests/test_extract_tokens.py` has its own helper, `extract(client, name, **arguments)`, which calls `extract_tokens` on a fixture, fails on a tool error and returns the structured content; `tests/helpers.py` is not changed (its `call` names `detect_visual_bugs`). From T13 the helper checks TOK-13 and TOK-14 on every result, and from T26 TOK-66.

**The whole suite.** The gate of a task is Full: the static checks and the two modules of the slice. The Build runs once per phase, in the background (it does not fit a foreground call), on the commit of the last task of the phase, and the session waits for it without running pytest in the foreground: a phase is closed only when it passes. A test of an earlier slice that fails there is run again alone before it counts as a regression, and a regression is fixed in a commit of its own, in the same session. The Build of phase 1 is the baseline of the slice on the machine, before the Capture changes. The Build of phase 6 is the gate the spec's Success Criteria name, and the Verifier starts only after it passes.

**Phase 2 has no test of its own.** It changes the Capture for every tool before any tool reads the change. Its gate is the tests of the earlier tools (TOK-77), and each of its tasks ends with a probe: a script in the session's scratchpad that calls `capture(...)` with a `BrowserSession()` on a page written there, whose output is recorded under the task. A probe is evidence for the session, not a test: each fact gets its test through the tool, red before the code that reads it, in T17 (`auto_margins`), T15 (`Capture.srgb`) and T24 (`descendants`); the twelve properties are read from T9, T11 and T12.

### Phase 1: Below the browser

```
T1 → T2 → T3
```

### Phase 2: The contract of the Capture

```
T4 → T5 → T6 → T7
```

### Phase 3: The tool, on `tokens-page.html`

```
T8 → T9 → T10 → T11 → T12 → T13
```

### Phase 4: A value only where it paints

```
T14 → T15 → T16 → T17 → T18 → T19
```

### Phase 5: Values that are nearly equal

```
T20 → T21 → T22 → T23
```

### Phase 6: Scope, the Limit, the contract and the documents

```
T24 → T25 → T26 → T27 → T28 → T29
```

### Phase 7: Closing

```
T30
```

The Verifier is dispatched in the sixth session, after T29 and the Build of phase 6. T30 is the closing step: it runs only on a PASS.

---

## Task Breakdown

### Phase 1: Below the browser

### T1: Name the three thresholds in the config

- [ ] Done

**What**: `TOKENS_NEAR_COLOR_BELOW_DELTA_E = 2.0`, `TOKENS_NEAR_LENGTH_BELOW_PX = 1.0` and `TOKENS_MAX_PER_FAMILY = 20`, each under a comment that gives its source as the Assumptions table of the spec does. The two lists of the Capture are T4.
**Where**: `src/squint_mcp/config.py`
**Depends on**: None
**Reuses**: how the constants of the Checks carry their sources in the same file
**Requirement**: TOK-75

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] The comment of the ΔE threshold names CSS Color Module Level 4, section 20.2 for the formula and section 14.2.1 for "one JND is 2", that the module compares with `E < JND`, and that reading it as "one token" is Squint's
- [ ] The comment of the Length threshold says it is a Squint default with no norm behind it, and why (one image pixel per CSS pixel; whole steps of a scale stay apart)
- [ ] The comment of the Limit says it is a Squint default, not measured on real pages
- [ ] Gate check passes: Static

**Tests**: none
**Gate**: static

**Commit**: `feat(config): name the thresholds of extract_tokens`

---

### T2: Fetch the CIEDE2000 test data

- [ ] Done

**What**: The file of Sharma, Wu and Dalal, fetched raw (with `curl`, not through WebFetch) from `https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt` and kept as fetched. The maintainer asked for the download in the prompt of the Tasks session.
**Where**: `tests/fixtures/ciede2000testdata.txt`
**Depends on**: T1
**Reuses**: the 34 rows of the appendix of the design
**Requirement**: TOK-74 (its data)

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] A script of the scratchpad reads the file and the 34 rows of the appendix of `design.md` and shows them equal, number for number, seven numbers a row. If a row differs, STOP: the appendix was read through WebFetch, one of the two is wrong, and the maintainer decides which
- [ ] The layout of the raw file (separators, any heading line, any column the appendix does not have) is written under this task, for the parser of T3
- [ ] Gate check passes: Static

**Tests**: none
**Gate**: static

**Commit**: `test(color): add the CIEDE2000 test data`

---

### T3: Compute ΔE2000

- [ ] Done

**What**: `delta_e_2000(reference, sample)` on two Lab colours, as the appendix of the design writes it, and the one test of TOK-74. `lab_of`, `parse` and `to_hex` are not written here: T9, T15 and T20 add each when a test of the tool asks for it.
**Where**: `src/squint_mcp/color.py` (with the new test module of the colour difference)
**Depends on**: T2
**Reuses**: the appendix of `design.md`
**Requirement**: TOK-74

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the test fails on the import of `squint_mcp.color`
- [ ] The test reads the file of T2, asserts that it holds 34 pairs, and for each pair that the function, rounded to four decimal places, gives the published value, in both orders of the pair
- [ ] Gate check passes: Full; then Build for phase 1, in the background: the baseline of the slice
- [ ] Test count: 422 collected (421 and the test of TOK-74); none deleted

**Tests**: unit
**Gate**: full, then build for the phase

**Commit**: `feat(color): add the CIEDE2000 colour difference`

---

### Phase 2: The contract of the Capture

### T4: Read the twelve properties tokens are made of

- [ ] Done

**What**: `CAPTURE_COMPUTED_PROPERTIES` gains the four `border-<side>-color`, the four corner radius properties, `box-shadow`, `text-shadow`, `row-gap` and `column-gap`; `CAPTURE_COLOR_PROPERTIES` names the seven of the list whose computed value is one colour.
**Where**: `src/squint_mcp/config.py`
**Depends on**: T3
**Reuses**: the contract of AD-003: the collector reads the list the config gives it
**Requirement**: TOK-77

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Probe: on a scratch page, `Element.computed` of an element holds the twelve names with the texts the design measured (`rgba(0, 0, 0, 0.2) 0px 1px 3px 0px` for the shadow of TOK-08, `8px` for a corner, `normal` for no gap)
- [ ] No response of another tool changes: Checks and `inspect_element` read named properties (design, Integration Points)
- [ ] Gate check passes: Capture

**Tests**: integration
**Gate**: capture

**Commit**: `feat(capture): read the properties tokens are made of`

---

### T5: Tell the sides whose margin is `auto`

- [ ] Done

**What**: The field `autoMargins` of the collector, read with `element.computedStyleMap()`, and `Element.auto_margins` with the comment the design gives it.
**Where**: `src/squint_mcp/js/collect_elements.js` (with the model of an element)
**Depends on**: T4
**Reuses**: `describe` in the collector; the camelCase aliases of the models
**Requirement**: TOK-77; read by TOK-30 in T17

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Probe: a box of 200px with `margin: 0 auto` gives `["right", "left"]` and a margin of 620px laid out on each of those sides; a box with `margin: 10px` gives `[]`; an element of an open shadow tree with `margin-left: auto` gives `["left"]`
- [ ] The sides come in the order `top`, `right`, `bottom`, `left`
- [ ] Gate check passes: Capture

**Tests**: integration
**Gate**: capture

**Commit**: `feat(capture): tell the sides whose margin is auto`

---

### T6: Hold what is under the matches of a selector

- [ ] Done

**What**: The argument `descendants` of the collector and of `capture(..., descendants=False)`: the matches and every element under one of them, in the light tree and in open shadow trees, each once, in document order. The comment of `Capture.elements` says so.
**Where**: `src/squint_mcp/js/collect_elements.js` (with the signature of the Capture and the comment of the model)
**Depends on**: T5
**Reuses**: `order` and `walk` of the collector; `globalThis.__squintElements`, which holds the elements returned
**Requirement**: TOK-77; read by TOK-52 to TOK-55 in T24

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Probe, on a scratch page shaped as `tokens-scope.html`: `.card` with `descendants` gives `#one`, `#one-child`, `#two`, `#inner`, `#host`, `#deep`, each once and in that order; `#deep` gives that element alone; `#gone` gives one element with no box; `.missing` gives none; `.card` without `descendants` gives the three matches, as today
- [ ] Without `descendants`, a Capture holds what it held before this task
- [ ] Gate check passes: Capture

**Tests**: integration
**Gate**: capture

**Commit**: `feat(capture): hold what is under the matches of a selector`

---

### T7: Convert the colours outside `rgb()` in the page

- [ ] Done

**What**: `srgb_colors.js` as the design gives it, `_srgb_colors(page, elements)` called right after the collector, and `Capture.srgb`.
**Where**: `src/squint_mcp/js/srgb_colors.js` (with its call in the Capture and the field of the model)
**Depends on**: T6
**Reuses**: how the Capture loads and evaluates the collector
**Requirement**: TOK-77; read by TOK-39 and TOK-40 in T15

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Probe: a page with `background-color: color(display-p3 1 0 0)` gives `Capture.srgb` that colour as `color(srgb 1.09302 -0.22669 -0.150073)`; `color(srgb 0.2 0.4 0.6)` reads itself; a page whose colours are all `rgb()` gives `{}` and evaluates no script
- [ ] The texts are sent sorted, in one call; a text the browser does not convert is left out
- [ ] `git diff main --stat -- tests/` shows the two files of T2 and T3 and no file of an earlier slice
- [ ] Gate check passes: Capture; then Build for phase 2, in the background: 422 tests, every test of the earlier tools with no assertion changed (TOK-77)

**Tests**: integration
**Gate**: capture, then build for the phase

**Commit**: `feat(capture): convert colours outside rgb() to sRGB in the page`

---

### Phase 3: The tool, on `tokens-page.html`

### T8: Make `extract_tokens` a tool

- [ ] Done

**What**: The handler (one Capture under `asyncio.timeout`, the default viewport, a hand-built `CallToolResult` with one text block and the structured content), the models of "Data Models" in a new `tokens.py` whose `extract` returns `elements` and eight empty Families, the registration with its two annotations, `tokens-page.html` as the spec's table gives it, and the new test module with its `extract` helper. `scope` is in the signature, for the schema, and is not read: the selector is `"*"` until T24.
**Where**: `src/squint_mcp/tools/extract_tokens.py` (with the models, the registration in the server, the fixture and the new test module)
**Depends on**: T7
**Reuses**: the handler of `inspect_element`, line for line up to the Capture; the listing test at line 54 of the tests of `inspect_element`
**Requirement**: TOK-67, TOK-09, TOK-11

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the three tests fail on a tool that is not listed
- [ ] TOK-67: the test asserts `readOnlyHint` true, `openWorldHint` true, an output schema, and an input schema where `url` alone is required, `scope` is an optional string and `viewport` an optional object whose `width` and `height` are at least 1
- [ ] TOK-09: `viewport` `{width: 1440, height: 900}`, `stabilized` true, `scope` null, `elements` 8, and in each of the eight Families a `total` equal to the length of its `tokens`. The Families are empty here: that clause gains its teeth from T9 to T12
- [ ] TOK-11: exactly one content block, a text block
- [ ] `elements` counts Read elements by their box only (the elements of `head` have none); `visibility` and opacity wait for T19
- [ ] The two lists of tool names (`tests/test_ping.py:36`, `tests/test_inspect_element.py:464`) gain `extract_tokens`, and `test_tools_are_exactly_the_three_documented_ones` becomes `..._the_four_documented_ones`: `git diff` of the two files shows those lines and nothing else. This is the exception TOK-77 words
- [ ] Gate check passes: Full, with `tests/test_ping.py` and `tests/test_inspect_element.py` added to the pytest call
- [ ] Test count: recorded here; none deleted

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): add the extract_tokens tool`

---

### T9: Read the colours of a page

- [ ] Done

**What**: The Family `colors`: `color.parse` for `rgb()` and `rgba()`, `color.to_hex`, the Uses of a colour by Role, and Tokens in Rank order. Each Value is its own Group until T20.
**Where**: `src/squint_mcp/tokens.py` (with the parsing and the hex of the colour module)
**Depends on**: T8
**Reuses**: `Element.computed`, `box_model.border`, `own_text` and `own_text_boxes`
**Requirement**: TOK-01

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the test of TOK-01 gets an empty list
- [ ] The test asserts the five `(value, uses, roles.text, roles.background, roles.border)` whole and in order (L-020: two Tokens of 2 Uses and two of 1, each pair in order of its text)
- [ ] Rules this page forces, each seen as a wrong tuple while the code is written: a colour of alpha 0 is no Value (`html` has `rgba(0, 0, 0, 0)`); a border colour counts only where the border has a width (every element has four border colours); a text colour counts only with Painted text (`body`, `#card`); four equal sides are one Use (`#cccccc` has 1)
- [ ] Every Token has one variant, itself
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read the colours of a page`

---

### T10: Read the type scale of a page

- [ ] Done

**What**: The four lists of `typography`, read on elements with Painted text, each in its Family order.
**Where**: `src/squint_mcp/tokens.py`
**Depends on**: T9
**Reuses**: the counting of T9
**Requirement**: TOK-02, TOK-03, TOK-04, TOK-05

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the four tests get empty lists
- [ ] Each test asserts its list whole and in order
- [ ] Rules this page forces: Painted text (`Arial, sans-serif` has 5 Uses, not 8); Family order by `value` (`400` comes before `700`, which has more Uses)
- [ ] A `line-height` that is not a px length is left for T16, which has the fixture
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read the type scale of a page`

---

### T11: Read the spacings of a page

- [ ] Done

**What**: The Family `spacing`, with its three Roles, in Family order.
**Where**: `src/squint_mcp/tokens.py`
**Depends on**: T10
**Reuses**: `Element.box_model`; `computed["row-gap"]`, `computed["column-gap"]`
**Requirement**: TOK-06

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the test of TOK-06 gets an empty list
- [ ] The test asserts the three `(value, uses, roles.margin, roles.padding, roles.gap)` whole and in order
- [ ] Rules this page forces: a length of 0 is no Value; the same Value on several sides of one element in one Role is one Use (`16` has `padding` 2: `#card` and `#button`); the two axes of a gap are one Use; Family order by `value` (`8` before `16`, which has more Uses)
- [ ] The `auto` sides and the `display` of a gap are left for T17, which has the fixtures
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read the spacings of a page`

---

### T12: Read the radii and the shadows of a page

- [ ] Done

**What**: The Families `radii` and `shadows` for what `tokens-page.html` holds: corner radii that are one px length, and a `box-shadow`.
**Where**: `src/squint_mcp/tokens.py`
**Depends on**: T11
**Reuses**: the twelve properties of T4
**Requirement**: TOK-07, TOK-08

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: the two tests get empty lists
- [ ] TOK-07: `(4px, 1)` then `(8px, 1)`: four equal corners are one Use, and a corner of `0px` is no Value
- [ ] TOK-08: `(box, rgba(0, 0, 0, 0.2) 0px 1px 3px 0px, 1)` alone: `none` is no Value
- [ ] `text-shadow` and the radii that are not a Length are left for T18
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read the radii and the shadows of a page`

---

### T13: Pin the summary and the sums of a result

- [ ] Done

**What**: The tests of the summary line and of two equal calls, and the two sums of a Token checked by the `extract` helper on every result of the module from here on.
**Where**: `tests/test_extract_tokens.py`
**Depends on**: T12
**Reuses**: the summary T8 wrote from the eight `total`
**Requirement**: TOK-10, TOK-12, TOK-13, TOK-14

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] TOK-10: the text block equals the line of the criterion, character for character. Rule dropped: two counts of the summary swapped
- [ ] TOK-12: two calls with the same arguments return equal structured content. No mutant kills it inside one process: every order of the result is held by a criterion of its own (TOK-01, TOK-04, TOK-06, TOK-45, TOK-52, TOK-62)
- [ ] TOK-13 and TOK-14: the helper asserts, for every Token of every result, that `uses` is the sum of its `variants` and its `value` that of the first, and for `colors` and `spacing` that `uses` is the sum of its `roles`. On this page every tuple already says so; TOK-13 is seen failing in T20, the first fixture where a Token has two variants
- [ ] Rule dropped for TOK-14: the `uses` of a colour Token counts its `text` Role only
- [ ] Gate check passes: Full; then Build for phase 3, in the background

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `test(tokens): pin the summary and the sums of a result`

---

### Phase 4: A value only where it paints

### T14: Count a colour only where it paints

- [ ] Done

**What**: `tokens-used.html` with `#inherit` and its child, `#fill`, `#clear`, `#clip`, `#veil`, `#edge` and `#sides`, and the seven tests. Any rule T9 did not need is built here.
**Where**: `tests/fixtures/tokens-used.html` (with its tests and what they ask of the token module)
**Depends on**: T13
**Reuses**: the counting of T9
**Requirement**: TOK-15, TOK-16, TOK-17, TOK-18, TOK-19, TOK-20, TOK-21

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] The module has two helpers the criteria word: a list "holds" a value (the `value` of one of its Tokens) and "does not hold" it (the `value` of no Token and of no variant)
- [ ] Rule dropped, test by test. TOK-15: the text Role counts an element with no Own text (`#aa0000` has 2 Uses). TOK-16: the text Role reads `color` (`#111111` is held). TOK-17 and TOK-18: a colour of alpha 0 is a Value (`#00808000`, `#00000000`). TOK-19: the alpha is cut, not rounded half up (`#0000007f`). TOK-20: a border colour counts whatever the width (`#00aa00` is held). TOK-21: one side is read for the four (three of the colours are gone)
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `test(tokens): hold a colour to the elements that paint it`

---

### T15: Read the colours Chromium does not write as `rgb()`

- [ ] Done

**What**: `color.parse` reads `color(srgb r g b)` and `color(srgb r g b / a)`, with `none` as 0; a colour is read through `capture.srgb.get(text, text)`; `#srgb` and `#wide` join the fixture.
**Where**: `src/squint_mcp/color.py` (with the lookup in the token module, and the two elements of the fixture)
**Depends on**: T14
**Reuses**: `Capture.srgb` of T7, which this task holds end to end
**Requirement**: TOK-39, TOK-40

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: both tests fail with `Unsupported colour`, or with the colour missing
- [ ] TOK-39: `#336699` is held. TOK-40: `#ff0000` is held: a channel above 1 clips to 255 and one below 0 to 0
- [ ] The branch that raises `Unsupported colour "<text>".` has no fixture that reaches it: the browser converts every colour it computes (design, Error Handling and Risks). It is one line that raises, and the Verifier does not count it as a gap of the tests
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read colours in the notations Chromium keeps`

---

### T16: Count a type value only on Painted text

- [ ] Done

**What**: `#big` and its child, `#normal` and `#ratio` in the fixture, their three tests, and a `line-height` of `normal` as no Value.
**Where**: `src/squint_mcp/tokens.py` (with the three elements of the fixture and their tests)
**Depends on**: T15
**Reuses**: the lists of T10
**Requirement**: TOK-25, TOK-26, TOK-27

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-26 fails on `normal`
- [ ] TOK-25. Rule dropped: a type value is read on an element with no Own text (`40`, `900`, `50` and `Georgia, serif` are held, each in its list)
- [ ] TOK-26: `13` is held, and the Uses of `lineHeights` add up to one less than those of `sizes`: every other element with Own text of the fixture has a `line-height` in px
- [ ] TOK-27: `30` is held. No rule of ours to drop: 30px is what Chromium computes for `1.5` at 20px, and the test pins that the computed value is what is read
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): leave out a line height that is not a length`

---

### T17: Count a spacing only where it is one

- [ ] Done

**What**: `#margins`, `#paddings`, `#centered`, `#pulled`, `#flex`, `#iflex`, `#grid`, `#igrid` and `#block` in the fixture, their seven tests, the sides of `auto_margins` left out of the margins, and a gap read only on the four displays.
**Where**: `src/squint_mcp/tokens.py` (with the nine elements of the fixture and their tests)
**Depends on**: T16
**Reuses**: `Element.auto_margins` of T5, which this task holds end to end
**Requirement**: TOK-28, TOK-29, TOK-30, TOK-31, TOK-32, TOK-33, TOK-34

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-30 holds `620`; TOK-34 holds `91` if T11 did not read `display`
- [ ] Rule dropped, test by test. TOK-28 and TOK-29: one side is read for the four (three values of each are gone; L-019, a value per side). TOK-31: a Value is a length other than 0, not above 0 (a `value` below 0 is held), and the test also refuses `71`. TOK-32: `row-gap` alone is read (`83` is gone). TOK-33: `inline-flex`, `grid` and `inline-grid` taken out of the displays, one mutant each (`85`, `87`, `89` gone in turn). TOK-34: the `display` is not read
- [ ] `#centered` sits in a `body` 1440px wide, so that 620px is what a missing rule would return
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): leave out auto margins and the gap of a block`

---

### T18: Count a radius and a shadow where they are

- [ ] Done

**What**: `#corners`, `#round`, `#oval`, `#glow` and its child, and `#layers` in the fixture, their four tests, the Family order of radii that are not a Length, and `text-shadow` on Painted text.
**Where**: `src/squint_mcp/tokens.py` (with the six elements of the fixture and their tests)
**Depends on**: T17
**Reuses**: the lists of T12
**Requirement**: TOK-35, TOK-36, TOK-37, TOK-38

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-37 finds no Token of `kind` `text`
- [ ] TOK-35. Rules dropped: one corner is read for the four (three radii gone); a corner of zero is a Value (`0px` is held)
- [ ] TOK-36: `50%` and `10px 20px` come after every Token that is one px length. Rule dropped: the radii are sorted as texts (`10px 20px` comes first)
- [ ] TOK-37: `(text, rgb(0, 0, 0) 1px 1px 2px)` with 1 Use. Rule dropped: `text-shadow` is read on an element with no Own text (2 Uses)
- [ ] TOK-38: one Token of `kind` `box` whose `value` is the two layers. Rule dropped: the text is split at its commas
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): read text shadows and radii that are not a length`

---

### T19: Read only the elements that paint

- [ ] Done

**What**: `#hidden`, `#faded` and its child, `#none`, `#flat-w` and `#flat-h` in the fixture, their three tests, the `visibility` and the opacity of a Read element, and one test of the eight lists of the finished fixture.
**Where**: `src/squint_mcp/tokens.py` (with the six elements of the fixture and their tests)
**Depends on**: T18
**Reuses**: `Element.opacity`, `computed["visibility"]`, `Element.box`
**Requirement**: TOK-22, TOK-23, TOK-24

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-22 holds `#aa00aa`, TOK-23 holds `#00aaaa`
- [ ] TOK-24: none of the three colours is held, and `elements` equals the number of Read elements of the finished fixture, counted by hand in a comment of the test. Rules dropped: the width of a box is not read (`#abcd02` is held and `elements` is one more); the height is not read (`#abcd03`). `#none` fails both and tells neither
- [ ] The eight lists of `tokens-used.html` are asserted whole and in order (L-020): most of its Tokens have 1 Use, so their places are decided by the `value` alone. The expected lists are written from the Terms and the fixture, not from a run
- [ ] Gate check passes: Full; then Build for phase 4, in the background

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `feat(tokens): read only the elements that paint`

---

### Phase 5: Values that are nearly equal

### T20: Fold colours that are Near

- [ ] Done

**What**: `group(values, distance)` as the design gives it, `color.lab_of` as the appendix writes it, the distance of two colours (equal alpha as 8 bits, ΔE2000 below the threshold of T1), and `tokens-groups.html` with the elements of the four criteria.
**Where**: `src/squint_mcp/tokens.py` (with the Lab of the colour module, the new fixture and its tests)
**Depends on**: T19
**Reuses**: `delta_e_2000` of T3; the threshold of T1
**Requirement**: TOK-41, TOK-42, TOK-43, TOK-44

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-41 and TOK-44 find two Tokens where they ask for one
- [ ] TOK-42 and TOK-43 pass before the code, since nothing groups yet; each is seen failing under its mutant once the code is in. TOK-42: a Value is compared with every Value of a Group (`#1a79e8` joins through `#1a78e8`). TOK-43: the alpha is left out of Near (`#1a73e880` joins `#1a73e8`)
- [ ] Rules dropped. TOK-41: the Representative is the first Value of the document (`#1a78e8`); the threshold is 1.8 (two Tokens). TOK-42: the threshold is 2.3 (`#1a79e8` joins). TOK-44: a tie in Uses goes to the first of the document (`#858585`). TOK-13: the `uses` of a Token is that of its Representative
- [ ] L-021: no criterion has a pair at exactly 2. The two sides the spec gives are 1.8620 (Near) and 2.2280 (not): the mutants at 1.8 and at 2.3 are the nearest that tell
- [ ] The other colours of the fixture (its text, the background of `body`) are Near none of the colours of the criteria
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): fold colours closer than one noticeable difference`

---

### T21: Fold font sizes less than 1px apart

- [ ] Done

**What**: The distance of two Lengths (their difference in px, rounded to six decimal places, when it is below the threshold of T1), `sizes` grouped with it, and the nine elements with Own text of the fixture: 15px on 1, 16px on 3, 16.5px on 1, 16.75px on 1, 17px on 2, 17.75px on 1.
**Where**: `src/squint_mcp/tokens.py` (with the elements of the fixture and their tests)
**Depends on**: T20
**Reuses**: `group` of T20
**Requirement**: TOK-45, TOK-46, TOK-47

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-45 finds six Tokens
- [ ] The element with Own text of TOK-41 is one of the nine; all nine have `line-height: 20px` until T22
- [ ] Rules dropped. TOK-45 (L-021, sizes exactly at the threshold): Near is at or below 1px (15, 16 and 17 fold). TOK-46: a Value joins the first Near Group opened, not the nearest (16.75 joins 16); the threshold is 0.7 (17.75 opens a Group). TOK-47: a tie in distance goes to the Group opened last (16.5 joins 17)
- [ ] Each test asserts its `variants` whole and in order
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): fold font sizes less than a pixel apart`

---

### T22: Fold spacings, radii and line heights

- [ ] Done

**What**: `spacing`, `radii` and `lineHeights` grouped with the distance of T21, a radius being a Length only when its text is one px length; the elements of the four criteria; and one test of the eight lists of the finished fixture.
**Where**: `src/squint_mcp/tokens.py` (with the elements of the fixture and their tests)
**Depends on**: T21
**Reuses**: `group` of T20, the distance of T21
**Requirement**: TOK-48, TOK-49, TOK-50, TOK-51

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-48, TOK-49 and TOK-50 find two Tokens where they ask for one, unless T21 grouped every Family of Lengths at once; then each is seen failing with its Family taken out of the grouping
- [ ] TOK-50: one of the nine elements with Own text takes `line-height: 20.5px`; the one Token is `20` and its `variants` end with `(20.5, 1)`
- [ ] TOK-51 (L-019, a case per clause). Rules dropped: a radius is a Length when its text starts with a px length (`10px 20px` and `10.5px 20px` fold); a percentage is read as a number (`30%` and `30.5%` fold)
- [ ] The eight lists of `tokens-groups.html` are asserted whole and in order (L-020), written from the Terms and the fixture, not from a run: among them `#1a73e880` before `#1a79e8`, both of 1 Use
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): fold spacings, radii and line heights`

---

### T23: Hold the two edge cases of the default page

- [ ] Done

**What**: `tokens-default.html`, which leaves the margin of `body` as the browser gives it and holds `#mixed` with `padding: 40px 40.5px`, and its two tests.
**Where**: `tests/fixtures/tokens-default.html` (with its two tests)
**Depends on**: T22
**Reuses**: nothing new in `src/` is expected
**Requirement**: TOK-78, TOK-79

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] TOK-78: the Token `40` has 2 Uses and the variants `(40, 1)` and `(40.5, 1)`, in that order. Rule dropped: an element counts once for a Token (1 Use)
- [ ] TOK-79: `8` is held with 1 Use and `roles.margin` 1. Rule dropped: `html` and `body` are left out of the reading. The fixture is the proof that no reset is assumed
- [ ] Gate check passes: Full; then Build for phase 5, in the background

**Tests**: integration
**Gate**: full, then build for the phase

**Commit**: `test(tokens): hold two near values on one element and the default margin`

---

### Phase 6: Scope, the Limit, the contract and the documents

### T24: Narrow the reading to a scope

- [ ] Done

**What**: The handler reads `scope`: the selector is the `scope` as given when it is not `None`, with `descendants=True`, and the result says which `scope` it read. `tokens-scope.html` as the spec gives it, with its five tests.
**Where**: `src/squint_mcp/tools/extract_tokens.py` (with the new fixture and its tests)
**Depends on**: T23
**Reuses**: `capture(..., descendants=True)` of T6, which this task holds end to end
**Requirement**: TOK-52, TOK-53, TOK-54, TOK-55, TOK-56

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-52, TOK-53, TOK-55 and TOK-56 get the whole page. TOK-54 passes before and after: it is the other side of the rule
- [ ] TOK-52: the four `(value, uses)` whole and in order (L-020: three Tokens of 1 Use, in order of their text), and `scope` equal to `.card`
- [ ] Rules dropped, on a scratch copy. `descendants` is not passed (`#0000ff` and `#00ffff` are gone). The collector adds a match under a match twice (TOK-53: 7 elements, and `#ffff00` has 2 Uses). The collector does not walk the shadow tree under a match (`#00ffff` is gone). TOK-54: the selector without `scope` is `body *` (7 elements)
- [ ] TOK-55: `#deep` alone. No rule of ours to drop: Playwright's `css=` engine reaches into open shadow trees
- [ ] `#host` has no background and holds `#deep`, a block of 100px by 20px, in an open shadow tree, so that the host has a box
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): narrow the reading to a scope`

---

### T25: Fail on a scope that reads nothing, and answer one that paints nothing

- [ ] Done

**What**: A Capture with no element raises `Scope "<scope>" matched no elements.`; the five tests of the errors and of the empty reading.
**Where**: `src/squint_mcp/tools/extract_tokens.py` (with its tests)
**Depends on**: T24
**Reuses**: the selector error of `capture(...)`, which quotes the `scope` as written
**Requirement**: TOK-57, TOK-58, TOK-59, TOK-60, TOK-61

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-57 gets a result with 0 elements
- [ ] TOK-58: the message is `Invalid selector "div[".`, whole. It is `capture(...)`'s message: no rule of the tool to drop
- [ ] TOK-59 and TOK-60: `#gone` succeeds with 0 elements, eight Families of `{total: 0, tokens: []}` and the summary of zeros, character for character. Rule dropped: the call fails when no element is Read
- [ ] TOK-61: an empty `scope` fails, with no structured content and a text that is not a summary. Rule dropped: the selector is `scope or "*"` (the call succeeds on the whole page)
- [ ] Every failure of this task is also asserted an error with no structured content (TOK-72, which T27 owns)
- [ ] TOK-24, sharpened now that a scope exists: with `scope` equal to `#none`, `#flat-w` and `#flat-h` of `tokens-used.html` in turn, `elements` is 0
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): fail on a scope that matches no element`

---

### T26: Bound each Family to its 20 most used Tokens

- [ ] Done

**What**: `total` as the number of Tokens found, the `TOKENS_MAX_PER_FAMILY` first in Rank order kept and put in Family order, the summary counting `total`; `tokens-limit.html` and its five tests.
**Where**: `src/squint_mcp/tokens.py` (with the new fixture and its tests)
**Depends on**: T25
**Reuses**: the Limit of T1; the scope of T24, for TOK-63
**Requirement**: TOK-62, TOK-63, TOK-64, TOK-65, TOK-66

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Red before the code: TOK-62 and TOK-64 get 21 Tokens
- [ ] TOK-62 (one past the Limit): `total` 21, and the values 10 to 190 and then 210, whole and in order. TOK-63 (exactly at it): `total` 20 and the twenty values from 10 to 200
- [ ] Rules dropped. The cut is made in Family order (200 stays and 210 goes). The Limit is 19 (TOK-63 loses a value). The Limit is 21 (TOK-62 keeps 200). The summary counts the Tokens returned (`colors 20`). One budget is shared by the Families (TOK-64 or TOK-62 comes back short)
- [ ] TOK-64: the 20 colours that come first by text, whole and in order. The page has no other colour: `body` has no background and no element has Own text. A script of the scratchpad shows, with `lab_of` and `delta_e_2000`, that the smallest ΔE2000 among the 21 is at or above 2; the number is written here
- [ ] TOK-66: the helper of the module asserts, on every result from here on, that each of the eight Families holds at most 20 Tokens
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `feat(tokens): bound each family to its twenty most used tokens`

---

### T27: Hold the contract the tool shares with the others

- [ ] Done

**What**: `tokens-viewport.html` and the six tests of the viewport, the two URL errors, the timeout, the shape of a failure and a page that never goes idle.
**Where**: `tests/test_extract_tokens.py`
**Depends on**: T26
**Reuses**: the tests at lines 209 and 478 of the tests of `inspect_element`; `local_server`, `/hang` and `polling.html`
**Requirement**: TOK-68, TOK-69, TOK-70, TOK-71, TOK-72, TOK-73

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] TOK-68: at `{width: 375, height: 812}`, `#111111` is held, `#999999` is not, and the result says that viewport. Rule dropped: the viewport is not passed to the Capture
- [ ] TOK-69 and TOK-70: the two messages, the first whole and the second by its start and the url. They are `capture(...)`'s messages: no rule of the tool to drop
- [ ] TOK-71: with `TOTAL_TIMEOUT_S` patched to 1 on `/hang`, as the test of `inspect_element` does, the message is `Timed out after 1s.` and the next call succeeds. Rule dropped: the Capture is taken outside `asyncio.timeout` (the test ends on its own bound)
- [ ] TOK-72: every failing call of the module is an error with no structured content, through one helper
- [ ] TOK-73: on `polling.html` served by `local_server`, `stabilized` is false and the text block ends with `; not stabilized.`. Rule dropped: the summary always says `stabilized.`
- [ ] Gate check passes: Full

**Tests**: integration
**Gate**: full

**Commit**: `test(tokens): hold the viewport, the errors and the timeout of the tool`

---

### T28: Run the tests of the slice on Linux

- [ ] Done

**What**: The two modules of the slice run in the Playwright image for Docker, and the result written under this task. The design's spikes ran on Windows only, and the CI of the pull request is Linux. No criterion of its own: it runs those of T3 to T27 on the other platform.
**Where**: `.specs/features/extract-tokens/tasks.md`
**Depends on**: T27
**Reuses**: the Linux command of slice 9 and the notes of the Handoff on Docker
**Requirement**: none

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] The count of passed tests on Linux equals that of the same two modules on Windows, and both are written here
- [ ] A test that fails on Linux only is a finding for the maintainer before it is a fix: STOP and report it
- [ ] Gate check passes: Linux

**Tests**: none
**Gate**: linux

**Commit**: `docs(specs): record the Linux run of extract-tokens`

---

### T29: Document the tool

- [ ] Done

**What**: The README describes `extract_tokens`: its inputs, the eight Families, what counts as a Use, the two thresholds with their sources, and the Limit. The CHANGELOG lists it under `Unreleased`.
**Where**: `README.md` (with the changelog)
**Depends on**: T28
**Reuses**: how the README describes `inspect_element` and `detect_visual_bugs`
**Requirement**: TOK-76

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] Each of the five things TOK-76 names is in the README, and the sources of the two thresholds are those of the comments of T1
- [ ] Any sentence of the README that says the server has three tools says four
- [ ] Gate check passes: Full; then Build for phase 6, in the background. It is the gate of the spec's Success Criteria, and the Verifier waits for it

**Tests**: none
**Gate**: full, then build for the phase

**Commit**: `docs: describe extract_tokens`

---

### Phase 7: Closing

### T30: Mark slice 10 as done

- [ ] Done

**What**: After the Verifier's PASS: `docs/ROADMAP.md` shows slice 10 as `concluída`, in the table and in its section, with a link to this feature's directory; the Status column of the spec's traceability table and the Handoff of `.specs/STATE.md` say the same.
**Where**: `docs/ROADMAP.md` (with the traceability table of the spec and the Handoff)
**Depends on**: T29
**Reuses**: how slice 9 was closed
**Requirement**: none

**Tools**: MCP NONE; Skill NONE

**Done when**:

- [ ] `validation.md` holds a PASS for the 79 criteria
- [ ] `validate_state.py extract-tokens` exits 0
- [ ] If a fix round changed `src/` or `tests/` after T28, the Linux gate is run again and its result written under T28
- [ ] Nothing is pushed and no pull request is opened: both wait for the maintainer's go-ahead

**Tests**: none
**Gate**: full

**Commit**: `docs(roadmap): mark slice 10 as done`

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Verifier → Phase 7

Phase 1:  T1 ------→ T2 ------→ T3
Phase 2:  T4 ------→ T5 ------→ T6 ------→ T7
Phase 3:  T8 ------→ T9 ------→ T10 -----→ T11 -----→ T12 -----→ T13
Phase 4:  T14 -----→ T15 -----→ T16 -----→ T17 -----→ T18 -----→ T19
Phase 5:  T20 -----→ T21 -----→ T22 -----→ T23
Phase 6:  T24 -----→ T25 -----→ T26 -----→ T27 -----→ T28 -----→ T29
Phase 7:  T30
```

Execution is strictly sequential, one batch per session (Execution Plan). T30 is taken in the session of the Verifier, after its PASS.

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Thresholds | 3 constants in 1 file | ✅ Granular |
| T2: Test data | 1 file, fetched and compared | ✅ Granular |
| T3: ΔE2000 | 1 function, 1 test | ✅ Granular |
| T4: Twelve properties | 2 tuples in 1 file | ✅ Granular |
| T5: `auto` margins | 1 field, from the collector to the model | ⚠️ OK: the model refuses a collector that does not give the field |
| T6: `descendants` | 1 argument, from the Capture to the collector | ⚠️ OK: one argument through two files |
| T7: sRGB | 1 page script, its call, 1 field | ⚠️ OK: the script has no caller without the other two |
| T8: The tool | 1 handler with its models, its registration, 1 fixture, 3 tests | ⚠️ OK: a tool is observable only once all of them exist; tests come first, so none can be a task of its own |
| T9: Colours | 1 Family, 2 functions of the colour module | ⚠️ OK: the Family cannot write a Value without them |
| T10: Type scale | 4 lists of one shape | ✅ Granular |
| T11: Spacings | 1 Family | ✅ Granular |
| T12: Radii and shadows | 2 Families of a few lines each | ⚠️ OK: both read a text as it is |
| T13: Summary and sums | tests of 1 fixture, 1 helper | ✅ Granular |
| T14: Colours that paint | 1 fixture, 7 tests | ✅ Granular |
| T15: Other notations | 1 parser branch, 1 lookup, 2 tests | ✅ Granular |
| T16: Type on Painted text | 1 rule, 3 tests | ✅ Granular |
| T17: Spacing that is one | 2 rules, 7 tests | ⚠️ OK: both decide what a spacing is |
| T18: Radii and shadows that paint | 2 rules, 4 tests | ⚠️ OK: as T12 |
| T19: Read elements | 1 condition, 3 tests, 1 test of the whole fixture | ✅ Granular |
| T20: Fold colours | 1 function, 1 distance, `lab_of`, 1 fixture, 4 tests | ⚠️ OK: a Group of colours needs the three |
| T21: Fold sizes | 1 distance, 3 tests | ✅ Granular |
| T22: Fold the other Lengths | 3 Families through 1 function, 4 tests | ✅ Granular |
| T23: Edge cases | 1 fixture, 2 tests | ✅ Granular |
| T24: Scope | 1 argument read, 1 fixture, 5 tests | ✅ Granular |
| T25: Scope errors | 1 error, 5 tests | ✅ Granular |
| T26: The Limit | 1 rule, 1 fixture, 5 tests | ✅ Granular |
| T27: Contract | 1 fixture, 6 tests | ⚠️ OK: six criteria of the handler the tool shares with the others |
| T28: Linux | 1 run, 1 record | ✅ Granular |
| T29: Documents | 2 documents | ✅ Granular |
| T30: Closing | 1 roadmap row and section, the Handoff | ✅ Granular |

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
| T7 | T6 | T6 → T7 | ✅ Match |
| T8 | T7 | first of phase 3, after phase 2 | ✅ Match |
| T9 | T8 | T8 → T9 | ✅ Match |
| T10 | T9 | T9 → T10 | ✅ Match |
| T11 | T10 | T10 → T11 | ✅ Match |
| T12 | T11 | T11 → T12 | ✅ Match |
| T13 | T12 | T12 → T13 | ✅ Match |
| T14 | T13 | first of phase 4, after phase 3 | ✅ Match |
| T15 | T14 | T14 → T15 | ✅ Match |
| T16 | T15 | T15 → T16 | ✅ Match |
| T17 | T16 | T16 → T17 | ✅ Match |
| T18 | T17 | T17 → T18 | ✅ Match |
| T19 | T18 | T18 → T19 | ✅ Match |
| T20 | T19 | first of phase 5, after phase 4 | ✅ Match |
| T21 | T20 | T20 → T21 | ✅ Match |
| T22 | T21 | T21 → T22 | ✅ Match |
| T23 | T22 | T22 → T23 | ✅ Match |
| T24 | T23 | first of phase 6, after phase 5 | ✅ Match |
| T25 | T24 | T24 → T25 | ✅ Match |
| T26 | T25 | T25 → T26 | ✅ Match |
| T27 | T26 | T26 → T27 | ✅ Match |
| T28 | T27 | T27 → T28 | ✅ Match |
| T29 | T28 | T28 → T29 | ✅ Match |
| T30 | T29 | first of phase 7, after phase 6 | ✅ Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: Thresholds | config constants | none | none | ✅ OK |
| T2: Test data | test data | none | none | ✅ OK |
| T3: ΔE2000 | the ΔE2000 function | unit | unit | ✅ OK |
| T4: Twelve properties | the contract of the Capture | integration (the earlier tools) | integration | ⚠️ OK, see below |
| T5: `auto` margins | the contract of the Capture | integration (the earlier tools) | integration | ⚠️ OK, see below |
| T6: `descendants` | the contract of the Capture | integration (the earlier tools) | integration | ⚠️ OK, see below |
| T7: sRGB | the contract of the Capture | integration (the earlier tools) | integration | ⚠️ OK, see below |
| T8: The tool | MCP tools (handler, models, registration) | integration | integration | ✅ OK |
| T9 to T12 | MCP tools (`tokens.py`, `color.py`) | integration | integration | ✅ OK |
| T13: Summary and sums | MCP tools (tests of the tool) | integration | integration | ✅ OK |
| T14 to T19 | MCP tools (`tokens.py`, `color.py`, their tests) | integration | integration | ✅ OK |
| T20 to T23 | MCP tools (`tokens.py`, `color.py`, their tests) | integration | integration | ✅ OK |
| T24 to T27 | MCP tools (handler, `tokens.py`, their tests) | integration | integration | ✅ OK |
| T28: Linux | a run on another platform | none | none | ✅ OK |
| T29: Documents | documents | none | none | ✅ OK |
| T30: Closing | the roadmap | none | none | ✅ OK |

T4 to T7 add three facts and twelve properties that no test reads in their own task: the project allows no test below the tool boundary, and no tool reads them before phase 3. The order is the maintainer's (the contract of the Capture first, closed by the whole suite for TOK-77). What the tasks do about it: a recorded probe in each, and a test through the tool that is red before the code that reads the fact, in T17, T15 and T24, each naming the task it holds end to end. From T8 on, no task changes `src/` without tests of its own, written first.

---

## Requirement Coverage

| Requirements | Task |
| --- | --- |
| TOK-75 | T1, from file evidence |
| TOK-74 | T3 (its data: T2) |
| TOK-77 | T7, by the Build of phase 2; held again by the Build of every phase. T8 holds its one exception, the two lists of tool names |
| TOK-09, TOK-11, TOK-67 | T8 |
| TOK-01 | T9 |
| TOK-02 to TOK-05 | T10 |
| TOK-06 | T11 |
| TOK-07, TOK-08 | T12 |
| TOK-10, TOK-12, TOK-13, TOK-14 | T13 |
| TOK-15 to TOK-21 | T14 |
| TOK-39, TOK-40 | T15 |
| TOK-25 to TOK-27 | T16 |
| TOK-28 to TOK-34 | T17 |
| TOK-35 to TOK-38 | T18 |
| TOK-22 to TOK-24 | T19 (TOK-24 sharpened in T25) |
| TOK-41 to TOK-44 | T20 |
| TOK-45 to TOK-47 | T21 |
| TOK-48 to TOK-51 | T22 |
| TOK-78, TOK-79 | T23 |
| TOK-52 to TOK-56 | T24 |
| TOK-57 to TOK-61 | T25 |
| TOK-62 to TOK-66 | T26 |
| TOK-68 to TOK-73 | T27 |
| TOK-76 | T29, from file evidence |

79 of 79 mapped. T2, T4, T5, T6, T28 and T30 hold no criterion of their own.

---

## Terms and the fixture that tells each

L-050 asks that every rule of the spec's Terms have a fixture whose outcome changes when the rule is dropped. This is where each rule lands.

| Rule of Terms | Told by | Task |
| --- | --- | --- |
| Scope: the whole page without it; matches and descendants; open shadow trees; each element once | TOK-54; TOK-52; TOK-52 and TOK-55; TOK-53 | T24 |
| Read element: width, height, `visibility`, opacity through the ancestors | TOK-24 (`#flat-w`, `#flat-h`), TOK-22, TOK-23 | T19 |
| Painted text: the element's own text nodes, not its children's | TOK-15, TOK-25, TOK-37 | T14, T16, T18 |
| Colours: alpha above 0; lower-case hex; clipping; alpha rounded half up, eight digits below 255 | TOK-17 and TOK-18; TOK-01; TOK-40; TOK-19 and TOK-43 | T14, T9, T15, T20 |
| Colour Roles: the text fill, the background, a border side that has a width | TOK-16; TOK-01; TOK-20 and TOK-21 | T14, T9 |
| Typography on Painted text; `normal` is no Value; the computed px | TOK-25; TOK-26; TOK-27 | T16 |
| Spacing: above 0; a margin not `auto`; each side; a gap on four displays, on two axes | TOK-31; TOK-30; TOK-28 and TOK-29; TOK-32 to TOK-34 | T17 |
| Radii: each corner; a zero corner is no Value | TOK-35 | T18 |
| Shadows: the whole text, one Token; `text-shadow` on Painted text | TOK-38; TOK-37 | T18 |
| Use: one element, one Value, one Role; equal sides are one Use | TOK-01, TOK-06, TOK-07 | T9, T11, T12 |
| Near, colours: equal alpha, ΔE2000 below 2 | TOK-43; TOK-41, TOK-42, TOK-44 | T20 |
| Near, Lengths: less than 1px apart; nothing else is Near | TOK-45; TOK-51 | T21, T22 |
| ΔE2000 | TOK-74 | T3 |
| Rank order: by Uses, then by Value | TOK-01, TOK-41, TOK-44, TOK-62 | T9, T20, T26 |
| Group: walked in Rank order; the nearest Representative; a tie to the first opened; Representatives only | TOK-41 and TOK-44; TOK-46; TOK-47; TOK-42 | T20, T21 |
| Token: `uses`, `roles`, `variants` in Rank order | TOK-13, TOK-14, TOK-41, TOK-46 | T13, T20, T21 |
| Family order of `colors` and `typography.families`: Rank order | TOK-01; the whole lists of `tokens-used.html` | T9, T19 |
| Family order of `sizes`, `weights`, `spacing`: by `value` | TOK-45; TOK-04; TOK-06 and TOK-62 | T21, T10, T11, T26 |
| Family order of `radii`: the Lengths before the others | TOK-36 | T18 |
| Limit: 20 per Family, the first in Rank order, `total` the full count | TOK-62 to TOK-66 | T26 |

Rules no fixture of the spec tells. No criterion was added and no task covers them: the maintainer left them so on 2026-10-13 (point 1 of "Waiting for the maintainer").

| Rule | Why no fixture tells it | What would |
| --- | --- | --- |
| Family order of `radii`: Lengths by size, and Family order rather than Rank order | The radii that are Lengths are `4px` and `8px`, `41px` to `47px`, and one Group of `4px`: by size, by text and by Uses they come in the same order | Two elements of `border-radius: 10px` and one of `9px` on one page: by rule `9px`, `10px`; by text or by Uses `10px` first |
| Family order of `typography.lineHeights`: by `value` rather than Rank order | No fixture has a line height with more Uses than a smaller one: `tokens-page.html` has 20 (3 Uses), 24 and 40 | Two texts of `line-height: 30px` and one of `22px` |
| Rank order of `shadows`: `box` before `text` | The one page with both (`tokens-used.html`) has a `box` text that also comes first as a text | A `box-shadow` of `0 2px 2px #000000` beside a `text-shadow` of `0 1px 2px #000000`, 1 Use each |
| `lab_of`: the D50 white and the matrices of CSS Color 4 | TOK-74 holds `delta_e_2000` on Lab numbers; through the tool only three sides of the threshold are seen (1.8554 and 1.8620 below 2, 2.2280 above), and a Lab that is a little off keeps them | A second test below the seam: the four ΔE values the criteria quote, to four decimal places, from the hex colours |
| A channel rounded to 8 bits, on a channel that is not whole | Every colour of the fixtures has whole channels; `color(srgb 0.2 0.4 0.6)` is 51, 102 and 153 exactly | The colours of point 3 of the design, which the maintainer left without a criterion |

The four "Points for the maintainer" of the design stay readings with no criterion, by the maintainer's word of 2026-10-13: the Rank order of radii that are Lengths, Painted text and whitespace, the other colour notations, and Lengths 1px apart that are not exact in binary.

---

## Waiting for the maintainer

Nothing waits: the maintainer answered the three points on 2026-10-13. TOK-77 has the proposed text in `spec.md`, with the two lists of tool names as its one exception.

1. **The five rules no fixture tells** (table above). Each can become a criterion, with a row in the traceability table and a line in a task of phase 4, 5 or 6; or stay as it is, and the Verifier is told so. **Answered: they stay as they are, with no new criterion.**
2. **T28, the run on Linux.** Not in the order the maintainer gave for this phase: added because the spikes ran on Windows only and the CI is Linux. It costs about four minutes and can be struck. **Answered: T28 stays.**
