# Foundation + ping Specification

Slice 1 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0001, ADR-0002. Decisions made there are final and are not restated as open here.

Scope size: Large by breadth (package, server, tool, tests, CI, project docs), low ambiguity. Design is skipped: the stack and module layout are already decided in `docs/SPEC.md`.

## Problem Statement

The repository holds only documents. There is no package, no server, no test pattern and no quality gate, so slices 2 to 5 have nothing to build on and an agent implementing them gets no feedback. This slice delivers the smallest end-to-end Squint: an MCP server that starts over stdio and answers `ping`, with typecheck, lint, format and tests running locally and in CI.

## Goals

- [ ] An MCP client can launch Squint over stdio, list its tools and call `ping`.
- [ ] `ping` is tested through the MCP tool boundary with an in-memory client, setting the test pattern for every later slice.
- [ ] Typecheck, lint, format check and tests each run with one command, locally and in CI.
- [ ] The project documents a contributor needs are in place, in English.
- [ ] Slice 1 is marked done in `docs/ROADMAP.md` once verification passes.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Playwright, Chromium, any browser code | Slice 2 |
| Capture, stabilization, collectors, vision | Slice 2 |
| `inspect_element`, `detect_visual_bugs` | Slices 2 and 3 |
| Finding model, any Check, selector generation | Slices 3 and 4 |
| Thresholds or defaults in `config` | No slice-1 behaviour needs one; the module exists empty |
| URL validation, 30s total tool timeout | Slice 2 (first tool that can hang) |
| CI installing Chromium | Slice 2 |
| `Pillow`, `numpy`, `coloraide` dependencies | Arrive with the slice that uses them |
| PyPI release, two-step install instructions in the README | Slice 5 |
| Tests outside the MCP tool boundary (unit tests of helpers, subprocess tests) | `docs/SPEC.md` Testing Decisions: one seam, in-memory client |
| HTTP transport, user config file | Out of scope for v0.1 |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| How the stdio launch and the clean-stdout rule are verified, given tests are in-memory only | Not covered by pytest. The Verifier launches the `squint-mcp` entry point once as a subprocess, sends `initialize`, and checks that stdout carries only JSON-RPC lines | The in-memory client bypasses stdio, so it cannot observe either behaviour; the source docs forbid a second test seam | n |
| "Official MCP Python SDK (FastMCP)" against the current SDK | `mcp` 2.x, where `FastMCP` is renamed `MCPServer`; no pin to `mcp<2` | Same high-level API under its current name; a new project should not start on the superseded major | n |
| Server name | `squint-mcp`, reported both as MCP `serverInfo.name` and as `ping`'s `name` | Matches the PyPI package and the `uvx` command | n |
| Version reported by `ping` | The installed package version, read from package metadata; `pyproject.toml` starts at `0.1.0` | One source of truth; nothing is published before slice 5 | n |
| `ping` output field names | `name`, `version`, `message` | Direct reading of "server name, version, echoed message" | n |
| `message` omitted | `message` is `null` in the output | Keeps the output shape constant | n |
| `message` length limit | None | Local stdio server echoing to its own caller; no resource to protect | n |
| `ping` annotations | `readOnlyHint: true`, `openWorldHint: false` | `ping` changes nothing and reaches nothing outside the process | n |
| `ping` text summary | One text block containing the server name and the version | SPEC requires "structured content plus a text summary" and fixes no wording | n |
| Package layout and entry point | `src/squint_mcp/`, console script `squint-mcp` | Required for `uvx squint-mcp` in slice 5 | n |
| One-command quality gates | `uv run pyright`, `uv run ruff check`, `uv run ruff format --check`, `uv run pytest` | Tools named in ADR-0001; no task runner needed | n |
| CI platform and matrix | GitHub Actions, `ubuntu-latest`, Python 3.12, on push to `main` and on pull requests | Repository is on GitHub; one job is enough until a platform bug shows up | n |
| Licence copyright line | `Copyright (c) 2026 Lucas Fassi` | Git author of the repository | n |
| Security reporting channel | GitHub private vulnerability reporting, no email address published | Avoids publishing a personal address; needs the feature enabled in repository settings (human step) | n |
| Issue templates | Two: bug report, feature request | The minimum that covers "report on and contribute" | n |
| CHANGELOG format | Keep a Changelog, with an `Unreleased` section | SPEC requires recording Checks and threshold changes; this is the conventional shape | n |
| README install section | States the project is pre-release and not on PyPI yet; documents running from a checkout | The `uvx` two-step install is slice 5 and would be false today | n |
| Roadmap status wording | `concluída`, in the table and in the slice 1 section | The roadmap is written in Portuguese | n |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:** input validation is covered by FND-08; observability by FND-10. Failure states, idempotency, auth, concurrency, data lifecycle, external-dependency failure and state transitions are N/A because `ping` is a pure function of its input with no I/O, no state and no external call.

---

## User Stories

### P1: Connect and ping ⭐ MVP

**User Story**: As a coding agent, I want a `ping` tool that returns the server name and version and echoes an optional message, so that I can verify the connection before spending a browser launch.

**Why P1**: It is the first proof that the server, the tool registration and the test seam work.

**Acceptance Criteria**:

1. WHEN an MCP client initializes a session THEN the server SHALL report `serverInfo.name` equal to `squint-mcp`. <!-- FND-01 -->
2. WHEN an MCP client lists tools THEN the server SHALL return exactly one tool, named `ping`. <!-- FND-02 -->
3. The `ping` tool SHALL declare the annotations `readOnlyHint: true` and `openWorldHint: false`. <!-- FND-03 -->
4. The `ping` tool SHALL declare an input schema whose only property is `message`, of type string and not required. <!-- FND-04 -->
5. WHEN `ping` is called with `message` set to `"hello"` THEN the server SHALL return structured content equal to `{"name": "squint-mcp", "version": V, "message": "hello"}`, V being the installed `squint-mcp` package version. <!-- FND-05 -->
6. WHEN `ping` is called with no arguments THEN the server SHALL return structured content equal to `{"name": "squint-mcp", "version": V, "message": null}`. <!-- FND-06 -->
7. WHEN `ping` succeeds THEN the server SHALL return `isError: false` and a text content block containing both `squint-mcp` and V. <!-- FND-07 -->
8. IF `ping` is called with a `message` that is not a string (for example `123`) THEN the server SHALL return `isError: true` with a text content block that names `message`. <!-- FND-08 -->
9. WHEN the `squint-mcp` console entry point is run THEN the server SHALL serve MCP over stdio. <!-- FND-09 -->
10. The server SHALL write logs to stderr only, leaving stdout to MCP protocol messages. <!-- FND-10 -->

**Independent Test**: Connect an in-memory MCP client to the server, list tools, call `ping` with and without `message`, and compare the structured content.

---

### P1: Quality tooling, locally and in CI

**User Story**: As the maintainer, I want strict typing, lint, format and tests to run locally and in CI with one command each, so that an AI agent implementing a ticket gets fast feedback and corrects itself.

**Why P1**: Every later slice is implemented by an agent that depends on these gates.

**Acceptance Criteria**:

1. The project SHALL declare `requires-python >= 3.12` and be installable with `uv sync`. <!-- FND-11 -->
2. WHEN `uv run pyright` is run THEN the project SHALL type-check in strict mode with zero errors. <!-- FND-12 -->
3. WHEN `uv run ruff check` is run THEN the project SHALL exit with code 0. <!-- FND-13 -->
4. WHEN `uv run ruff format --check` is run THEN the project SHALL exit with code 0. <!-- FND-14 -->
5. WHEN `uv run pytest` is run THEN the project SHALL exit with code 0. <!-- FND-15 -->
6. The test suite SHALL exercise the server only through an in-memory MCP client. <!-- FND-16 -->
7. WHEN a commit is pushed to `main` or a pull request is opened or updated THEN CI SHALL run typecheck, lint, format check and tests, and fail if any of them exits non-zero. <!-- FND-17 -->
8. The package SHALL contain a `config` module that defines no thresholds. <!-- FND-18 -->
9. The project SHALL NOT declare `playwright`, `Pillow`, `numpy` or `coloraide` as dependencies. <!-- FND-19 -->

**Independent Test**: On a clean checkout, run `uv sync` and the four commands; all exit 0. Open a pull request and see the CI job pass.

---

### P2: Project documents

**User Story**: As a contributor, I want README, LICENSE (MIT), CONTRIBUTING, CHANGELOG, SECURITY and GitHub issue/PR templates in place, so that I know how to use, report on and contribute to the project.

**Why P2**: Required by the slice, but nothing else in the slice depends on it.

**Acceptance Criteria**:

1. The repository SHALL contain a `README.md` that states what Squint is, that it is pre-release and not yet on PyPI, how to run the server from a checkout, and the four quality commands. <!-- FND-20 -->
2. The repository SHALL contain a `LICENSE` file with the MIT licence text and the line `Copyright (c) 2026 Lucas Fassi`. <!-- FND-21 -->
3. The repository SHALL contain a `CONTRIBUTING.md` that gives the setup command, the four quality commands, the Conventional Commits rule and the English-only rule for public text. <!-- FND-22 -->
4. The repository SHALL contain a `CHANGELOG.md` in Keep a Changelog format whose `Unreleased` section lists the `ping` tool. <!-- FND-23 -->
5. The repository SHALL contain a `SECURITY.md` that directs reporters to GitHub private vulnerability reporting. <!-- FND-24 -->
6. The repository SHALL contain a bug report and a feature request template under `.github/ISSUE_TEMPLATE/` and a pull request template under `.github/`. <!-- FND-25 -->
7. WHEN the Verifier reports PASS for this feature THEN `docs/ROADMAP.md` SHALL show slice 1 as `concluída` in both the table and the slice 1 section. <!-- FND-26 -->

**Independent Test**: Open each file on GitHub and confirm it renders and contains the listed content; the "New issue" page offers both templates.

---

## Edge Cases

- WHEN `ping` is called with `message` set to the empty string THEN the server SHALL echo `""`, not `null`. <!-- FND-27 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| FND-01 | P1: Connect and ping | T3 | Implementing |
| FND-02 | P1: Connect and ping | T3 | Implementing |
| FND-03 | P1: Connect and ping | T3 | Implementing |
| FND-04 | P1: Connect and ping | T3 | Implementing |
| FND-05 | P1: Connect and ping | T3 | Implementing |
| FND-06 | P1: Connect and ping | T3 | Implementing |
| FND-07 | P1: Connect and ping | T3 | Implementing |
| FND-08 | P1: Connect and ping | T3 | Implementing |
| FND-09 | P1: Connect and ping | T4 | Implementing |
| FND-10 | P1: Connect and ping | T4 | Implementing |
| FND-11 | P1: Quality tooling | T1 | Implementing |
| FND-12 | P1: Quality tooling | T1 | Implementing |
| FND-13 | P1: Quality tooling | T1 | Implementing |
| FND-14 | P1: Quality tooling | T1 | Implementing |
| FND-15 | P1: Quality tooling | T3 | Implementing |
| FND-16 | P1: Quality tooling | T3 | Implementing |
| FND-17 | P1: Quality tooling | - | Pending |
| FND-18 | P1: Quality tooling | T2 | Implementing |
| FND-19 | P1: Quality tooling | T1 | Implementing |
| FND-20 | P2: Project documents | - | Pending |
| FND-21 | P2: Project documents | - | Pending |
| FND-22 | P2: Project documents | - | Pending |
| FND-23 | P2: Project documents | - | Pending |
| FND-24 | P2: Project documents | - | Pending |
| FND-25 | P2: Project documents | - | Pending |
| FND-26 | P2: Project documents | - | Pending |
| FND-27 | P1: Connect and ping | T3 | Implementing |

**Coverage:** 27 total, 19 implemented, 8 pending.

**Verification method:** FND-01 to FND-08 and FND-27 by pytest through the in-memory MCP client. FND-09 and FND-10 by the Verifier's one-off stdio launch. FND-11 to FND-15 by running the commands. FND-16 to FND-26 by file evidence; FND-17 additionally by a green CI run once the branch is pushed, which needs an explicit go-ahead.

---

## Success Criteria

- [ ] `uv sync` followed by the four quality commands exits 0 on a clean checkout.
- [ ] An MCP client configured with the `squint-mcp` entry point lists `ping` and gets its name, version and echo back.
- [ ] CI is green on the pull request for this slice.
- [ ] Slice 1 reads `concluída` in `docs/ROADMAP.md`.
