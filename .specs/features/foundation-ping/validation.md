# Foundation + ping Validation

## Validation: foundation-ping - PASS ✅

**Date**: 2026-10-06
**Spec**: `.specs/features/foundation-ping/spec.md`
**Diff range**: `main..HEAD` on `feat/foundation-ping` (13 commits, `9bd137e`..`ca91012`)
**Verifier**: independent sub-agent (author ≠ verifier), re-verification iteration 3 of 3

Every acceptance criterion and edge case that can be judged today is matched by the implementation and by an assertion on the spec-defined value. The four previous survivors (M19, M27, N31, N32) are all killed. Of 37 mutants injected, 34 are killed by pytest; the 3 that pass pytest are not gaps: two change nothing the spec constrains (S01, S02) and one is outside the pytest seam by design and is caught by the stdio launch (S03).

Two items remain open and are not failures: FND-17's live CI run (needs a push that is not authorized yet) and FND-26's roadmap update (a closing step after this verdict).

How each claim was checked is stated per row: **ran** (executed, output read) or **read** (file evidence only). All line numbers were re-read from the files at `ca91012`.

---

## Task Completion

| Task | Status | Notes |
| ---- | ------ | ----- |
| T1 Scaffold | ✅ Done | commit `feab63e` |
| T2 Config module | ✅ Done | commit `a133768` |
| T3 Server + ping | ✅ Done | commit `fa055dd`; tests tightened in `06ae714` and `ca91012` |
| T4 stdio entry point | ✅ Done | commit `df897e9` |
| T5 CI workflow | ✅ Done | commit `82765cc` |
| T6 README | ✅ Done | commit `5822c95` |
| T7 Community documents | ✅ Done | commit `5735970` |
| T8 GitHub templates | ✅ Done | commit `f2fb631` |

`tasks.md` has 34 ticked boxes and 0 unticked (ran grep). Commits `26cad87` and `a37b094` touch only `AGENTS.md` and `REQUIREMENTS.md`, outside this feature's criteria.

---

## Spec-Anchored Acceptance Criteria

### P1: Connect and ping

| ID | Criterion | Spec-defined outcome | `file:line` + assertion / evidence | How | Verdict |
| -- | --------- | -------------------- | ---------------------------------- | --- | ------- |
| FND-01 | initialize reports server name | `serverInfo.name == "squint-mcp"` | `tests/test_ping.py:26` - `assert client.server_info.name == NAME` (`NAME = "squint-mcp"`, `tests/test_ping.py:11`). Impl `src/squint_mcp/server.py:9`. On the wire: `"serverInfo":{"name":"squint-mcp","version":"0.1.0"}`. | ran | ✅ PASS |
| FND-02 | tools/list returns exactly one tool, `ping` | names are exactly `["ping"]` | `tests/test_ping.py:31` - `assert [tool.name for tool in tools] == ["ping"]` | ran | ✅ PASS |
| FND-03 | annotations | `readOnlyHint: true`, `openWorldHint: false` | `tests/test_ping.py:37` - `assert annotations.read_only_hint is True`; `tests/test_ping.py:38` - `assert annotations.open_world_hint is False`. Impl `src/squint_mcp/server.py:13`. | ran | ✅ PASS |
| FND-04 | input schema: only property `message`, string, not required | properties == {message}; string the only non-null type (`spec.md:51`); not in `required` | `tests/test_ping.py:43` - `assert list(schema["properties"]) == ["message"]`; `tests/test_ping.py:46` - `assert accepted - {None, "null"} == {"string"}`; `tests/test_ping.py:47` - `assert "message" not in schema.get("required", [])`. Schema on the wire: `{"anyOf":[{"type":"string"},{"type":"null"}],"default":null,"title":"Message"}`, no `required`. | ran | ✅ PASS |
| FND-05 | `ping` with `"hello"` | `{"name":"squint-mcp","version":V,"message":"hello"}` | `tests/test_ping.py:52` - `assert result.structured_content == {"name": NAME, "version": VERSION, "message": "hello"}`; `VERSION = version(NAME)` (`tests/test_ping.py:12`), read from package metadata independently of the implementation. | ran | ✅ PASS |
| FND-06 | `ping` with no arguments | same shape, `message: null` | `tests/test_ping.py:61` - `assert result.structured_content == {"name": NAME, "version": VERSION, "message": None}` | ran | ✅ PASS |
| FND-07 | success shape | `isError: false`; a text block containing both `squint-mcp` and V | `tests/test_ping.py:70` - `assert result.is_error is False`; `tests/test_ping.py:71` - `assert any(NAME in text and VERSION in text for text in texts(result))` | ran | ✅ PASS |
| FND-08 | non-string `message` (`123`) | `isError: true`; a text block that names `message` | `tests/test_ping.py:76` - `assert result.is_error is True`; `tests/test_ping.py:77` - `assert any("message" in text for text in texts(result))`. On the wire: `Error executing tool ping: 1 validation error for pingArguments\nmessage\n  Input should be a valid string ...` | ran | ✅ PASS |
| FND-09 | console entry point serves MCP over stdio | `squint-mcp` answers MCP over stdin/stdout | `pyproject.toml:14` (`squint-mcp = "squint_mcp.server:main"`), `src/squint_mcp/server.py:19` (`server.run()`). One-off launch of `uv run --directory C:/Fassi/squint-mcp squint-mcp`: `initialize`, `notifications/initialized`, `tools/list`, `tools/call ping {"message":"hello"}` each answered with the matching `id`; every response awaited before stdin was closed; exit 0. | ran | ✅ PASS |
| FND-10 | logs on stderr only | every non-empty stdout line is a JSON-RPC message | Same launch plus two calls that make the server log (`message: 123`, unknown tool `nope`). stdout: 5 non-empty lines, 5 JSON-RPC 2.0 objects, 0 others. stderr: `Tool 'ping' rejected arguments: ['message']` and `Tool 'nope' failed: 'Unknown tool: nope'`. The probe discriminates: against scratch mutant S03 it reported `non_jsonrpc=1` (`BAD pinged`). | ran | ✅ PASS |

### P1: Quality tooling

| ID | Criterion | Evidence | How | Verdict |
| -- | --------- | -------- | --- | ------- |
| FND-11 | `requires-python >= 3.12`, installable with `uv sync` | `pyproject.toml:7`; `uv sync --locked` succeeded in a fresh copy of the tracked files with no `.venv`, followed by 11 passed there | ran | ✅ PASS |
| FND-12 | pyright strict, zero errors | `pyproject.toml:25` (`typeCheckingMode = "strict"`), `pyproject.toml:24` (`include = ["src", "tests"]`); `uv run pyright` → `0 errors, 0 warnings, 0 informations`, exit 0 | ran | ✅ PASS |
| FND-13 | `uv run ruff check` exit 0 | `All checks passed!`, exit 0 | ran | ✅ PASS |
| FND-14 | `uv run ruff format --check` exit 0 | `29 files already formatted`, exit 0 | ran | ✅ PASS |
| FND-15 | `uv run pytest` exit 0 | `11 passed`, exit 0 | ran | ✅ PASS |
| FND-16 | tests only through an in-memory MCP client | `tests/conftest.py:13` - `async with Client(server) as connected` is the only use of the server object; `tests/conftest.py:8` is the only `squint_mcp` import under `tests/`; `tests/test_ping.py:3-7` imports nothing from the package and no `subprocess` | read | ✅ PASS |
| FND-17 | CI runs the four gates on push to `main` and on PRs, fails on non-zero | `.github/workflows/ci.yml:4-6` (`push: branches: [main]`, `pull_request`); four separate `run:` steps at `.github/workflows/ci.yml:16`, `:18`, `:20`, `:22`, none with `continue-on-error`; `uv sync --locked` at `:14`; Python from `.python-version:1` | read | ✅ file verified; **live green run pending push** (not authorized, not a failure) |
| FND-18 | `config` module with no thresholds | `src/squint_mcp/config.py:1-4` is a docstring only | read | ✅ PASS |
| FND-19 | no `playwright`, `Pillow`, `numpy`, `coloraide` | `pyproject.toml:8-11` declares only `mcp` and `pydantic`; dev group `pyproject.toml:37-41` only `pyright`, `pytest`, `ruff`; none of the four is a package in `uv.lock` (grep, no match) | read + ran grep | ✅ PASS |

### P2: Project documents

| ID | Criterion | Evidence (read) | Verdict |
| -- | --------- | --------------- | ------- |
| FND-20 | README: what Squint is, pre-release / not on PyPI, run from checkout, four commands | `README.md:3`, `README.md:9`, `README.md:23-28`, `README.md:49-54`. The `uv run --directory ... squint-mcp` form at `README.md:37` is the one the stdio launch used. | ✅ PASS |
| FND-21 | LICENSE: MIT text + copyright line | `LICENSE:1` (`MIT License`), `LICENSE:3` (`Copyright (c) 2026 Lucas Fassi`), `LICENSE:5-21` | ✅ PASS |
| FND-22 | CONTRIBUTING: setup, four commands, Conventional Commits, English-only | `CONTRIBUTING.md:8`, `CONTRIBUTING.md:16-19`, `CONTRIBUTING.md:28`, `CONTRIBUTING.md:32` | ✅ PASS |
| FND-23 | CHANGELOG: Keep a Changelog, `Unreleased` lists `ping` | `CHANGELOG.md:5`, `CHANGELOG.md:7`, `CHANGELOG.md:12` | ✅ PASS |
| FND-24 | SECURITY: GitHub private vulnerability reporting | `SECURITY.md:11`; no email address in the file | ✅ PASS |
| FND-25 | bug + feature issue templates, PR template | `.github/ISSUE_TEMPLATE/bug_report.md:1-5`, `.github/ISSUE_TEMPLATE/feature_request.md:1-5`, `.github/pull_request_template.md:1-12` | ✅ PASS |
| FND-26 | ROADMAP shows slice 1 as `concluída` | `docs/ROADMAP.md:9` and `docs/ROADMAP.md:31` still read `pendente`. Closing step done by the orchestrator after this verdict. | ⏳ Deferred to post-PASS (not a failure) |

### Edge cases

| ID | Criterion | Spec-defined outcome | `file:line` + assertion | How | Verdict |
| -- | --------- | -------------------- | ----------------------- | --- | ------- |
| FND-27 | empty string | `message: ""`, not `null` | `tests/test_ping.py:82` - `assert result.structured_content == {"name": NAME, "version": VERSION, "message": ""}` | ran | ✅ PASS |
| FND-28 | `"  a longer message, padded with spaces  "` echoed character for character | `message` equals the input exactly | `tests/test_ping.py:90` holds the spec string verbatim (40 characters, two spaces each side); `tests/test_ping.py:92` - `assert result.structured_content == {"name": NAME, "version": VERSION, "message": message}` | ran | ✅ PASS |
| FND-29 | explicit `null` equals omission | same structured content as FND-06 | `tests/test_ping.py:100` sends `{"message": None}`; `tests/test_ping.py:101` - `assert result.structured_content == {"name": NAME, "version": VERSION, "message": None}`, the same literal as `tests/test_ping.py:61` | ran | ✅ PASS |

**Status**: ✅ 28 of 29 criteria matched the spec outcome with evidence; FND-26 deferred by design; FND-17 live run pending push. No spec-precision gaps.

---

## Discrimination Sensor

Scratch: a plain copy of the tracked files at `C:\tmp\sq-v3` (no `.git`), own `.venv` via `uv sync --locked`, baseline `11 passed` there. Each mutant was applied to the scratch copy by a script that refuses to run on the real tree, `uv run pytest -q` run in the scratch, and the file restored. No `git stash`, no worktree. Line numbers refer to the unmutated files.

| # | File:line | Mutation | Killed? | Killing test(s) |
| - | --------- | -------- | ------- | --------------- |
| N31 | `src/squint_mcp/tools/ping.py:19` | echo whitespace-stripped (previous survivor) | ✅ Killed | `test_ping_echoes_the_message_unchanged` |
| N32 | `src/squint_mcp/tools/ping.py:19` | echo truncated to 5 characters (previous survivor) | ✅ Killed | same |
| M19 | `src/squint_mcp/tools/ping.py:14` | type `str \| list[str] \| None` (previous survivor) | ✅ Killed | `test_ping_takes_only_an_optional_string_message` |
| M27 | `src/squint_mcp/tools/ping.py:14,19` | `str \| int \| None`, ints rejected by hand with `ToolError` (previous survivor) | ✅ Killed | same |
| F01 | `src/squint_mcp/tools/ping.py:19` | echo `rstrip()` only | ✅ Killed | `test_ping_echoes_the_message_unchanged` |
| F02 | `src/squint_mcp/tools/ping.py:19` | echo `lstrip()` only | ✅ Killed | same |
| F03 | `src/squint_mcp/tools/ping.py:19` | echo capped at 39 characters (off by one) | ✅ Killed | same |
| F04 | `src/squint_mcp/tools/ping.py:19` | whitespace normalised (`" ".join(message.split())`) | ✅ Killed | same |
| F05 | `src/squint_mcp/tools/ping.py:19` | comma removed from the echo | ✅ Killed | same |
| F06 | `src/squint_mcp/tools/ping.py:19` | echo upper-cased | ✅ Killed | both echo tests |
| F07 | `src/squint_mcp/tools/ping.py:19` | echo reversed | ✅ Killed | both echo tests |
| F08 | `src/squint_mcp/tools/ping.py:14,19` | explicit `null` rejected, omission still gives `null` (string sentinel default) | ✅ Killed | `test_ping_with_null_message_matches_omitting_it` |
| F09 | `src/squint_mcp/tools/ping.py:19` | empty string collapsed to `null` | ✅ Killed | `test_ping_echoes_an_empty_message_as_empty` |
| F10 | `src/squint_mcp/tools/ping.py:19` | `null` collapsed to empty string | ✅ Killed | null and omission tests |
| F11 | `src/squint_mcp/tools/ping.py:19` | message never echoed | ✅ Killed | three echo tests |
| F12 | `src/squint_mcp/tools/ping.py:19` | result `name` wrong | ✅ Killed | 6 tests |
| F13 | `src/squint_mcp/tools/ping.py:19` | result `version` wrong | ✅ Killed | 6 tests |
| F14 | `src/squint_mcp/tools/ping.py:11` | extra field `ok` in structured content | ✅ Killed | 5 tests |
| F15 | `src/squint_mcp/server.py:9` | server name `squint` | ✅ Killed | `test_server_reports_its_name` |
| F16 | `src/squint_mcp/server.py:13` | `read_only_hint=False` | ✅ Killed | `test_ping_is_read_only_and_closed_world` |
| F17 | `src/squint_mcp/server.py:13` | `open_world_hint=True` | ✅ Killed | same |
| F18 | `src/squint_mcp/server.py:13` | `open_world_hint` omitted | ✅ Killed | same |
| F19 | `src/squint_mcp/server.py:14` | second tool registered (`echo`) | ✅ Killed | `test_ping_is_the_only_tool` |
| F20 | `src/squint_mcp/server.py:12` | tool renamed `pong` | ✅ Killed | 10 tests |
| F21 | `src/squint_mcp/tools/ping.py:14` | `message` required | ✅ Killed | schema, omission, summary tests |
| F22 | `src/squint_mcp/tools/ping.py:14` | extra input parameter `loud` | ✅ Killed | schema test (`tests/test_ping.py:43`) |
| F23 | `src/squint_mcp/tools/ping.py:14` | `str \| float \| None` | ✅ Killed | schema test, non-string test |
| F24 | `src/squint_mcp/tools/ping.py:14` | schema unchanged, non-strings coerced with `str()` | ✅ Killed | `test_ping_rejects_a_non_string_message` (`tests/test_ping.py:76`) |
| F25 | `src/squint_mcp/tools/ping.py:14,19` | schema unchanged, non-string rejected with text `bad input` | ✅ Killed | same test (`tests/test_ping.py:77`) |
| F26 | `src/squint_mcp/tools/ping.py:19` | text summary replaced by `pong`, structured content intact | ✅ Killed | `test_ping_success_carries_a_text_summary` |
| F27 | `src/squint_mcp/tools/ping.py:19` | text summary has the name, not the version | ✅ Killed | same |
| F28 | `src/squint_mcp/tools/ping.py:19` | text summary has the version, not the name | ✅ Killed | same |
| F29 | `src/squint_mcp/tools/ping.py:19` | success returned with `is_error=True` | ✅ Killed | same (`tests/test_ping.py:70`) |
| F30 | `src/squint_mcp/__init__.py:6` + `pyproject.toml:3` | `__version__` hard-coded `"0.1.0"`, package bumped to `0.2.0` | ✅ Killed | 6 tests: the tests pin the version source |
| S01 | `src/squint_mcp/tools/ping.py:19` | echo lower-cased | ➖ Survived, out of spec | none: 11 passed |
| S02 | `src/squint_mcp/tools/ping.py:19` | echo capped at 1000 characters | ➖ Survived, out of spec | none: 11 passed |
| S03 | `src/squint_mcp/tools/ping.py:19` | `print()` to stdout inside `ping` | ➖ Survived pytest by design; caught by the stdio launch | stdio probe: `non_jsonrpc=1` |

### Why the three survivors are not gaps

- **S01 (lower-casing)** returns the spec-defined value for every input the spec defines: `"hello"`, `""` and the FND-28 string are all lower-case already. No AC, edge case or Assumptions row is violated. An example-based suite always admits some transformation that is the identity on its examples; failing on this would never terminate. A cheap optional hardening exists (see Summary).
- **S02 (cap at 1000)** contradicts the Assumptions row "`message` length limit: None" (`spec.md:52`) in principle, but no finite test can kill every cap: whatever length is tested, a larger cap survives. The cap that the listed edge case can observe (F03, 39 characters; N32, 5 characters) is killed. Treated as an unkillable class, not a test-strength gap.
- **S03 (stdout print)** is outside the pytest seam on purpose: the spec assigns FND-10 to the Verifier's stdio launch (`spec.md:45`, `spec.md:182`), and that launch does catch it.

A first version of F04 (`" ".join(message.split(" "))`) passed all tests because it is the identity function, an error in the mutant, not in the suite; it was replaced by the version in the table.

**Sensor depth**: expanded (37 behaviour-level mutations; the lightweight tier requires 1-3)
**Sensor outcome**: 37 injected, 34 killed by pytest, 3 survived pytest and none of them is a gap (2 out of spec, 1 outside the pytest seam and caught by the stdio launch) - PASS ✅

**Isolation check**: real-tree `git status --porcelain` before the sensor and after deleting the scratch are identical (`diff` empty): `?? .specs/LESSONS.md`, `?? .specs/features/foundation-ping/validation.md`, `?? .specs/lessons.json`. HEAD is `ca91012` before and after, `git diff --stat HEAD` is empty, `git worktree list` shows only the main tree, and `C:\tmp\sq-v3` is deleted.

---

## Code Quality

| Principle | Status |
| --------- | ------ |
| Minimum code (5 source files, 48 lines; no speculative abstraction) | ✅ |
| Surgical changes (diff touches only files the tasks name, plus two unrelated docs commits) | ✅ |
| No scope creep (no browser code, no thresholds, no extra dependencies) | ✅ |
| Matches patterns (first code in the repository; sets them) | ✅ |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met (11 tests for FND-01..08 and FND-27..29: happy, edge and error paths) | ✅ |
| Every test maps to a spec requirement - no unclaimed tests | ✅ |
| Documented guidelines followed: `docs/SPEC.md` Testing Decisions (one seam, in-memory client) | ✅ |

---

## Edge Cases

- [x] FND-27 empty string echoed as `""`, not `null`: `tests/test_ping.py:82`, mutant F09 killed.
- [x] FND-28 padded, longer message echoed character for character: `tests/test_ping.py:92`, mutants N31, N32, F01-F05 killed.
- [x] FND-29 explicit `null` equals omission: `tests/test_ping.py:101`, mutants F08, F10 killed.

---

## Gate Check

- **Gate command**: `uv run pyright && uv run ruff check && uv run ruff format --check && uv run pytest`
- **Outcome**: pyright exit 0 (0 errors, 0 warnings); ruff check exit 0; ruff format --check exit 0 (29 files); pytest exit 0 with 11 passed, 0 failed, 0 skipped
- **Also on a clean copy** (tracked files only, `uv sync --locked`): 11 passed
- **Test count before feature**: 0
- **Test count after feature**: 11 (9 at iteration 2; two added, none removed, no assertion weakened)
- **Skipped tests**: none
- **Failures**: none

---

## Fix Plans

None required.

---

## Requirement Traceability Update

Not applied to `spec.md` (the Verifier writes only this report). Proposed statuses:

| Requirement | Previous Status | New Status |
| ----------- | --------------- | ---------- |
| FND-01 to FND-08, FND-27 to FND-29 | Implementing | ✅ Verified |
| FND-09, FND-10 | Implementing | ✅ Verified (stdio launch) |
| FND-11 to FND-16, FND-18, FND-19 | Implementing | ✅ Verified |
| FND-17 | Implementing | ✅ Verified on file content; CI run pending push |
| FND-20 to FND-25 | Implementing | ✅ Verified |
| FND-26 | Pending | Pending (post-PASS closing step) |

---

## Summary

**Overall**: ✅ Ready

**Spec-anchored check**: 28/29 ACs matched the spec outcome; FND-26 deferred by design; 0 spec-precision gaps
**Sensor**: 34/37 mutations killed by pytest; 3 survivors, none a gap (S01, S02 out of spec; S03 outside the seam, caught by the stdio launch); M19, M27, N31, N32 all killed
**Gate**: 11 passed, 0 failed; pyright, ruff check, ruff format all exit 0

**What works**: server identity, single `ping` tool, annotations, exact input schema, exact echo including padding and length, null / omission / empty-string semantics, version read from package metadata, error path for non-string input, real stdio launch with a clean stdout, all four quality gates, CI workflow content, all project documents.

**Issues found**: none blocking.

**Optional hardening, not required**: putting one upper-case or non-ASCII character in the FND-28 string (`spec.md:141`, `tests/test_ping.py:90`) would also kill case-folding mutants such as S01.

**Not failures, still open**: FND-17 live CI run (needs a push), FND-26 roadmap update (`docs/ROADMAP.md:9`, `docs/ROADMAP.md:31`).

**Next steps**: mark slice 1 `concluída` in `docs/ROADMAP.md`, then push for the CI run once authorized.
