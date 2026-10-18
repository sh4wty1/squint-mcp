# Login session from a file (`storageState`) - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 21a397e..8cc0e20 (round 2 scope: c6e2aeb..8cc0e20, the fix `2cadc83` plus the docs-only `8cc0e20`)
**Round**: 2 - scoped
**Verifier**: independent sub-agent (author != verifier)

Round 1 was PASS at `c8a0068` with one ranked gap (non-UTF-8 file) and one observation (C5). Scope of this round: the fix's diff (`src/squint_mcp/capture.py`, `tests/test_storage_state.py`, `checks.md` Handoff line; `8cc0e20` touches only `docs/tasks/2026-10-18-storage-state.md`) and those two verdicts. Every proof re-ran at `8cc0e20`.

## Binding sources

Carried from c8a0068. Step 1 does not run under `light`, and the fix touched no interface (no schema, description or message text changed).

## Checks

Verified at 8cc0e20. All C1-C12 proofs plus the three schema tests ran in one invocation:
`.venv/bin/pytest tests/test_storage_state.py "tests/test_inspect_element.py::test_inspect_element_takes_url_selector_and_optional_viewport" "tests/test_detect_visual_bugs.py::test_detect_visual_bugs_takes_url_and_optional_viewports_and_checks" "tests/test_extract_tokens.py::test_extract_tokens_is_listed_with_its_hints_and_its_schemas" -v` - exit 0, **23 passed in 15.58s** (22 in round 1, plus `[not-utf-8]`), each test and case listed individually as PASSED. Test definitions in `tests/test_storage_state.py` sit at lines 87, 100, 114, 124, 137, 167, 181, 188, 202, 229, 247, 262 (`rg -n "^async def test_"`), unchanged: the fix's test diff is +4/-4 lines inside C9's parametrize and signature, so no line moved.

Evidence citations in `tests/test_storage_state.py` were refreshed (the file was touched) and hold at the same lines; C9's row carries the new case.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | `inspect_element` on `#campaigns` with `storageState` returns that element | same invocation, PASSED | `tests/test_storage_state.py:56` - `assert result.is_error is False`; `:97` - `assert inspected["computed"]["color"] == "rgb(18, 52, 86)"` | PASS |
| C2 | `detect_visual_bugs`, viewports 1440x900 and 390x844, `text-clipped` on `#clipped` in each | same invocation, PASSED | `tests/test_storage_state.py:107` - `viewports=[DESKTOP, MOBILE]`; `:110-111` - `assert clipped(content["findings"], viewport) == ["#clipped"]` per viewport | PASS |
| C3 | `extract_tokens` reports `#123456` among text colours | same invocation, PASSED | `tests/test_storage_state.py:120` - `assert "#123456" in text_colors(tokens)` | PASS |
| C4 | without `storageState`: zero-match error / no `#clipped` / no `#123456`, 3 cases | same invocation, 3 cases PASSED | `tests/test_storage_state.py:129` - `assert await fail(client, url) == 'Selector "#campaigns" matched no elements.'`; `:132` - `assert clipped(content["findings"], DESKTOP) == []`; `:134` - `assert "#123456" not in text_colors(...)` | PASS |
| C5 | after a page sets `seen=1`, the next call sends `sid=s3cret-session` and not `seen` | same invocation, PASSED | `tests/test_storage_state.py:149-155` - next call finds `#campaigns` (`sid` sent); `:163-164` - `assert result.is_error is True` / `...endswith('Selector "#seen-sent" matched no elements.')` (`seen` not sent). Observation carried from c8a0068: the `Cookie` header is settled through the fixture's rendering, not asserted raw; the fixture API is its only reader (`tests/conftest.py:51-64`), so the inference holds | PASS |
| C6 | file holds the same bytes after a call | same invocation, PASSED | `tests/test_storage_state.py:178` - `assert state.read_bytes() == before` | PASS |
| C7 | `state.json` fails with exactly `storageState must be an absolute path: "state.json".` | same invocation, PASSED | `tests/test_storage_state.py:185` - `assert message == 'storageState must be an absolute path: "state.json".'` | PASS |
| C8 | missing absolute path: starts `Could not read the storage state "<path>": `, ends `.` | same invocation, PASSED | `tests/test_storage_state.py:193-194` - `assert message.startswith(f'Could not read the storage state "{missing}": ')` / `assert message.endswith(".")` | PASS |
| C9 | not JSON, JSON array, `cookies` a string (and now not UTF-8): exactly `"<path>" is not a Playwright storage state.` | same invocation, `[not-json]`, `[array]`, `[rejected]`, `[not-utf-8]` PASSED | `tests/test_storage_state.py:199-200` - `[b"not json", b"[]", b'{"cookies": "nope"}', b"\xff\xfe{}"]`, ids incl. `"not-utf-8"`; `:206` - `path.write_bytes(content)`; `:208` - `assert message == f'"{path}" is not a Playwright storage state.'` | PASS |
| C10 | error text quotes neither `s3cret-session` nor `s3cret-radio`, 2 cases | same invocation, 2 cases PASSED | `tests/test_storage_state.py:241` - `assert result.is_error is True`; `:243-244` - `assert SESSION_COOKIE not in text` / `assert RADIO not in text` | PASS |
| C11 | `tools/list`: optional string `storageState` on exactly the three tools | same invocation, PASSED | `tests/test_storage_state.py:252` - `assert taking == set(TOOLS)`; `:256` - `assert "storageState" not in schema.get("required", [])`; `:258` - `assert {option["type"] for option in options} == {"string", "null"}` | PASS |
| C12 | each description names `` `storageState` ``, "absolute path", "never written", 3 cases | same invocation, 3 cases PASSED | `tests/test_storage_state.py:268-270` - the three `in description` assertions | PASS |
| C13 | README: `--save-storage=`, not committed, `sessionStorage` not carried, expired session | the four `grep -c` commands, literally, at 8cc0e20: `1`, `1`, `1`, `1` | `README.md` section `## Pages behind a login` (section placement carried from c8a0068; README untouched since) | PASS |
| C14 | `[Unreleased]` `### Added` names `storageState` | the sed/sed/grep pipeline, literally: `1` | `CHANGELOG.md:11` (carried from c8a0068; file untouched since) | PASS |
| C15 | `.specs/STATE.md` records AD-010, active, for `storageState`, beside ADR-0002 | the sed/grep pipeline, literally: `1` | `.specs/STATE.md:77-83` (carried from c8a0068; file untouched since) | PASS |
| C16 | pyright, ruff check, ruff format --check, full pytest green | `.venv/bin/pyright --pythonpath .venv/bin/python` exit 0 (`0 errors, 0 warnings, 0 informations`); `.venv/bin/ruff check` exit 0 (`All checks passed!`); `.venv/bin/ruff format --check` exit 0 (`133 files already formatted`); `.venv/bin/pytest` exit 0, `524 passed in 1430.74s` | gate outputs, this run at HEAD `8cc0e20` | PASS |

## Coverage

Carried from c8a0068: not recomputed, the `Coverage` join runs only under `standard` and `ui`. Noted for the record: the fix adds a member (not UTF-8) to "ways a file is not a storage state", now proven by C9 `[not-utf-8]`.

## Test policy rows

Carried from c8a0068: none, `checks.md` carries no `Test policy` section.

## Faults injected

Carried from c8a0068: none, fault injection runs only under `standard` and `ui`.

## Level and sampling

Carried from c8a0068, re-read against the fix. The new case goes through the same MCP boundary (`fail(client, ...)` over `inspect_element`), so its level matches C7-C10.

## Swept existing

Verified at 8cc0e20. The failure-modes claim "fails before a context exists" still holds: `_read_storage_state` runs at `src/squint_mcp/capture.py:347` (was `:346`; the fix added one line above it), before `session.browser()` at `:348` and `new_context` at `:350`.

## Intent vs code

Verified at 8cc0e20 for the fix; the rest carried from c8a0068.

- Gap 1 (round 1, non-UTF-8 file): **closed**. `src/squint_mcp/capture.py:111` now reads `data = Path(path).read_bytes()` inside the `OSError` `try`; `:119` - `state = json.loads(data.decode("utf-8"))` sits inside the `try` whose `except ValueError` (`:120`) sets `state = None`. `UnicodeDecodeError` subclasses `ValueError`, so a non-UTF-8 file reaches `:122-123` and raises `ToolError(f'"{path}" is not a Playwright storage state.')` - AC 9's message, quoting only the path (AC 10 holds). Proven over MCP by C9 `[not-utf-8]` (`b"\xff\xfe{}"`, `tests/test_storage_state.py:199`), PASSED.
- Door 2: holds, `Path(path).is_absolute()` still at `src/squint_mcp/capture.py:108`.
- The fix changed no message text, schema or description, so C7, C8, C11, C12 and the README/CHANGELOG record are untouched by it.
- `checks.md` Handoff gained a "Verification round 1" line recording the fix; C9's claim text left as approved (it names 3 ways, the proof now runs 4). Not a gap: the claim is a subset of what is proven.
- No new gap.

## Gate

`.venv/bin/pytest` (full suite) at 8cc0e20 - 524 passed, 0 failed in 1430.74s (0:23:50), exit 0 (523 in round 1, plus `[not-utf-8]`). `.venv/bin/pyright --pythonpath .venv/bin/python` exit 0, `.venv/bin/ruff check` exit 0, `.venv/bin/ruff format --check` exit 0. Targeted run: 23 passed, 0 failed.
