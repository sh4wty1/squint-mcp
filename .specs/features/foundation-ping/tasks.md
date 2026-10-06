# Foundation + ping Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: skipped. Stack and module layout are decided in `docs/SPEC.md` (Implementation Decisions).
**Status**: In Progress

SDK note: the official MCP Python SDK is at 2.x, where `FastMCP` was renamed `MCPServer` (`mcp.server.mcpserver`) and the in-memory client is `mcp.Client(server)`. Verified by running both against `mcp 2.3.0` before writing these tasks.

---

## Test Coverage Matrix

> Generated from project guidelines and spec. Guidelines found: `docs/SPEC.md` (Testing Decisions). No tests exist yet; this slice sets the pattern.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| MCP tools (server registration + tool handlers) | integration, through the in-memory MCP client only | 1:1 to spec ACs; every listed edge case; error path | `tests/test_*.py` | `uv run pytest` |
| stdio entry point | none | Outside the in-memory seam; checked by a one-off stdio launch at the task gate and again by the Verifier | - | build gate |
| Packaging, config module, CI, documents | none | build gate only | - | build gate |

## Gate Check Commands

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Static | Tasks before the first test exists | `uv run pyright && uv run ruff check && uv run ruff format --check` |
| Quick | Not used: there are no unit tests in this project | `uv run pytest` |
| Full | After tasks with tests through the MCP boundary | `uv run pytest` |
| Build | After phase completion or config/document-only tasks | `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest` |

---

## Execution Plan

Phases are ordered and run sequentially. Eight tasks: one batch, executed inline.

### Phase 1: Server

```
T1 → T2 → T3 → T4
```

### Phase 2: CI and documents

```
T5 → T6 → T7 → T8
```

After the Verifier reports PASS: update `docs/ROADMAP.md` (FND-26). It is a closing step, not a task, because it is conditional on the verdict.

---

## Task Breakdown

### Phase 1: Server

### T1: Scaffold the Python project

- [ ] Done

**What**: `pyproject.toml` with project metadata, `requires-python >= 3.12`, runtime dependencies `mcp` and `pydantic`, dev dependencies `pyright`, `ruff`, `pytest`, pyright strict and ruff configuration; the empty `squint_mcp` package; `.python-version`; `uv.lock`; Python entries in `.gitignore`.
**Where**: `pyproject.toml` (plus the generated lock file and the package marker)
**Depends on**: None
**Reuses**: nothing; first code in the repository
**Requirement**: FND-11, FND-12, FND-13, FND-14, FND-19

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `uv sync` succeeds on Python 3.12
- [ ] `playwright`, `Pillow`, `numpy`, `coloraide` are absent from `pyproject.toml`
- [ ] Gate check passes: Static

**Tests**: none
**Gate**: static

**Commit**: `build: scaffold python project with uv, pyright and ruff`

---

### T2: Add the config module

- [ ] Done

**What**: `config` module that exists and defines no thresholds.
**Where**: `src/squint_mcp/config.py`
**Depends on**: T1
**Reuses**: nothing
**Requirement**: FND-18

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Module is importable and holds only its docstring
- [ ] Gate check passes: Static

**Tests**: none
**Gate**: static

**Commit**: `feat(config): add empty config module`

---

### T3: Add the server and the ping tool

- [ ] Done

**What**: The MCP server named `squint-mcp` with the `ping` tool registered and annotated, and the tests that drive it through the in-memory client.
**Where**: `src/squint_mcp/tools/ping.py` (handler and result model; registration in the server module, tests under `tests/`)
**Depends on**: T2
**Reuses**: package name and version from `squint_mcp`
**Requirement**: FND-01, FND-02, FND-03, FND-04, FND-05, FND-06, FND-07, FND-08, FND-15, FND-16, FND-27

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] One test per AC: FND-01 to FND-08 and FND-27
- [ ] Tests import the server only to hand it to `mcp.Client`
- [ ] Gate check passes: Build
- [ ] Test count: 9 tests pass

**Tests**: integration
**Gate**: build

**Commit**: `feat(ping): add mcp server with ping tool`

---

### T4: Add the stdio entry point

- [ ] Done

**What**: `main()` that runs the server over stdio, exposed as the `squint-mcp` console script.
**Where**: `src/squint_mcp/server.py` (modify; script entry in the project metadata)
**Depends on**: T3
**Reuses**: the server object from T3
**Requirement**: FND-09, FND-10

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `uv run squint-mcp`, launched as a subprocess by an MCP stdio client, answers `initialize` and `ping`
- [ ] Every line the process writes to stdout during that session is a JSON-RPC message
- [ ] Gate check passes: Build
- [ ] Test count: 9 tests pass (no silent deletions)

**Tests**: none
**Gate**: build

**Commit**: `feat(server): add stdio entry point`

---

### Phase 2: CI and documents

### T5: Add the CI workflow

- [ ] Done

**What**: GitHub Actions workflow that runs typecheck, lint, format check and tests on push to `main` and on pull requests.
**Where**: `.github/workflows/ci.yml`
**Depends on**: T4
**Reuses**: the four commands from the Build gate
**Requirement**: FND-17

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Workflow triggers on `push` to `main` and on `pull_request`
- [ ] Each of the four commands is its own step
- [ ] Gate check passes: Build

**Tests**: none
**Gate**: build

**Commit**: `ci: run typecheck, lint, format check and tests`

---

### T6: Write the README

- [ ] Done

**What**: README stating what Squint is, that it is pre-release and not on PyPI, how to run the server from a checkout, and the four quality commands.
**Where**: `README.md`
**Depends on**: T5
**Reuses**: wording from `CONTEXT.md` and `docs/SPEC.md`
**Requirement**: FND-20

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] The four content points of FND-20 are present
- [ ] The run-from-checkout command in the README works when executed
- [ ] Gate check passes: Build

**Tests**: none
**Gate**: build

**Commit**: `docs: add readme`

---

### T7: Add the community documents

- [ ] Done

**What**: LICENSE (MIT), CONTRIBUTING, CHANGELOG and SECURITY.
**Where**: repository root (`LICENSE` and the three markdown documents)
**Depends on**: T6
**Reuses**: commands from the README
**Requirement**: FND-21, FND-22, FND-23, FND-24

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] LICENSE holds the MIT text and `Copyright (c) 2026 Lucas Fassi`
- [ ] CONTRIBUTING gives setup, the four commands, Conventional Commits and the English-only rule
- [ ] CHANGELOG follows Keep a Changelog and lists `ping` under `Unreleased`
- [ ] SECURITY points to GitHub private vulnerability reporting
- [ ] Gate check passes: Build

**Tests**: none
**Gate**: build

**Commit**: `docs: add license, contributing, changelog and security policy`

---

### T8: Add the GitHub templates

- [ ] Done

**What**: Bug report and feature request issue templates and a pull request template.
**Where**: `.github/ISSUE_TEMPLATE/` (two templates) and the pull request template beside it
**Depends on**: T7
**Reuses**: the four commands as the PR checklist
**Requirement**: FND-25

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Both issue templates have valid front matter (`name`, `about`)
- [ ] Gate check passes: Build

**Tests**: none
**Gate**: build

**Commit**: `docs: add issue and pull request templates`

---

## Phase Execution Map

```
Phase 1 → Phase 2

Phase 1:  T1 → T2 → T3 → T4
Phase 2:  T5 → T6 → T7 → T8
```

---

## Task Granularity Check

| Task | Scope | Status |
| ---- | ----- | ------ |
| T1: Scaffold | 1 manifest + generated lock and package marker | ✅ Granular |
| T2: Config module | 1 file | ✅ Granular |
| T3: Server + ping | 1 tool, its registration and its tests | ✅ Cohesive: the tool is not testable without the server |
| T4: stdio entry point | 1 function + 1 metadata line | ✅ Granular |
| T5: CI | 1 file | ✅ Granular |
| T6: README | 1 file | ✅ Granular |
| T7: Community documents | 4 static documents | ⚠️ Cohesive, text only, no behaviour |
| T8: GitHub templates | 3 static templates | ⚠️ Cohesive, text only, no behaviour |

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

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T1: Scaffold | Packaging | none | none | ✅ OK |
| T2: Config module | Config | none | none | ✅ OK |
| T3: Server + ping | MCP tools | integration | integration | ✅ OK |
| T4: stdio entry point | stdio entry point | none | none | ✅ OK |
| T5: CI | CI | none | none | ✅ OK |
| T6: README | Documents | none | none | ✅ OK |
| T7: Community documents | Documents | none | none | ✅ OK |
| T8: GitHub templates | Documents | none | none | ✅ OK |
