# Login session from a file (`storageState`) - verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 21a397e..c8a0068
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

## Binding sources

Step 1 does not run under `light`. Read for context only: `docs/ROADMAP.md` section 12 ("Entra": optional parameter on the tools that open a URL, clear error for a missing or unreadable file, README on `codegen --save-storage`, tests over MCP with an `HttpOnly` cookie, CHANGELOG entry; "Não entra": `sessionStorage`, login flow, post-click states). The plan, checks and diff agree with it. The two playwright.dev pages were not opened (step 1 is `ui`-only).

## Checks

All C1-C12 proofs, plus the three existing schema tests the plan's Impact names, ran in one invocation:
`.venv/bin/pytest tests/test_storage_state.py "tests/test_inspect_element.py::test_inspect_element_takes_url_selector_and_optional_viewport" "tests/test_detect_visual_bugs.py::test_detect_visual_bugs_takes_url_and_optional_viewports_and_checks" "tests/test_extract_tokens.py::test_extract_tokens_is_listed_with_its_hints_and_its_schemas" -v` - exit 0, **22 passed in 16.16s**, each test and each parametrized case listed individually as PASSED. Every named test exists in `tests/test_storage_state.py` (defined at lines 87, 100, 114, 124, 137, 167, 181, 188, 202, 229, 247, 262) and the module is new in the diff.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | `inspect_element` on `#campaigns` with `storageState` returns that element | same invocation, `test_inspect_element_sees_the_screen_after_login` PASSED | `tests/test_storage_state.py:56` - `assert result.is_error is False` (in `succeed`, a zero-match selector is an error); `:97` - `assert inspected["computed"]["color"] == "rgb(18, 52, 86)"` (= `#123456`, only `#campaigns` has it) | PASS |
| C2 | `detect_visual_bugs`, viewports 1440x900 and 390x844, one `text-clipped` on `#clipped` in each | same invocation, `test_detect_visual_bugs_judges_the_screen_after_login_in_every_viewport` PASSED | `tests/test_storage_state.py:107` - `viewports=[DESKTOP, MOBILE]` (`tests/helpers.py:14-15` = 1440x900, 390x844); `:110-111` - `for viewport in (DESKTOP, MOBILE): assert clipped(content["findings"], viewport) == ["#clipped"]` (`clipped` filters `check == "text-clipped"`, `:75`) | PASS |
| C3 | `extract_tokens` reports `#123456` among text colours | same invocation, `test_extract_tokens_reads_the_screen_after_login` PASSED | `tests/test_storage_state.py:120` - `assert "#123456" in text_colors(tokens)` (`text_colors` keeps tokens with `roles["text"] > 0`, `:83`) | PASS |
| C4 | without `storageState`: zero-match error / no `#clipped` Finding / no `#123456`, 3 cases | same invocation, `[inspect_element]`, `[detect_visual_bugs]`, `[extract_tokens]` PASSED | `tests/test_storage_state.py:129` - `assert await fail(client, url) == 'Selector "#campaigns" matched no elements.'`; `:132` - `assert clipped(content["findings"], DESKTOP) == []`; `:134` - `assert "#123456" not in text_colors(...)` | PASS |
| C5 | after a page sets `seen=1`, the next call with the same file sends `sid=s3cret-session` and not `seen` | same invocation, `test_a_cookie_a_page_sets_does_not_reach_the_next_call` PASSED | `tests/test_storage_state.py:141-147` - first call must find `#seen-sent` (the cookie did come back within the call); `:149-155` - next call finds `#campaigns` (`sid` sent; API at `tests/conftest.py:54` answers 200 only to `sid == SESSION_COOKIE`); `:163-164` - `assert result.is_error is True` / `assert texts(result)[-1].endswith('Selector "#seen-sent" matched no elements.')` (`seen` not sent). Header asserted indirectly through the fixture's rendering, not on the raw `Cookie` header | PASS |
| C6 | file holds the same bytes after a call | same invocation, `test_the_storage_state_file_is_never_written` PASSED | `tests/test_storage_state.py:178` - `assert state.read_bytes() == before` (call on `?set-cookie`, `:174`) | PASS |
| C7 | `state.json` fails with exactly `storageState must be an absolute path: "state.json".` | same invocation, `test_a_relative_storage_state_is_refused` PASSED | `tests/test_storage_state.py:185` - `assert message == 'storageState must be an absolute path: "state.json".'` | PASS |
| C8 | missing absolute path: starts `Could not read the storage state "<path>": `, ends `.` | same invocation, `test_a_storage_state_that_cannot_be_read_is_refused` PASSED | `tests/test_storage_state.py:193-194` - `assert message.startswith(f'Could not read the storage state "{missing}": ')` / `assert message.endswith(".")` | PASS |
| C9 | not JSON, JSON array, `cookies` a string: exactly `"<path>" is not a Playwright storage state.`, 3 cases | same invocation, `[not-json]`, `[array]`, `[rejected]` PASSED | `tests/test_storage_state.py:199` - `["not json", "[]", '{"cookies": "nope"}']`; `:208` - `assert message == f'"{path}" is not a Playwright storage state.'` | PASS |
| C10 | not-JSON file holding `s3cret-session`, and object with domainless `sid` cookie + `s3cret-radio`: error contains neither, 2 cases | same invocation, `[not-json]`, `[no-domain]` PASSED | `tests/test_storage_state.py:214-225` - the two contents; `:241` - `assert result.is_error is True`; `:243-244` - `assert SESSION_COOKIE not in text` / `assert RADIO not in text` (`SESSION_COOKIE = "s3cret-session"`, `tests/helpers.py:17`; `RADIO = "s3cret-radio"`, `:15`) | PASS |
| C11 | `tools/list`: optional string `storageState` on exactly the three tools | same invocation, `test_the_three_tools_take_an_optional_storage_state` PASSED | `tests/test_storage_state.py:252` - `assert taking == set(TOOLS)`; `:256` - `assert "storageState" not in schema.get("required", [])`; `:258` - `assert {option["type"] for option in options} == {"string", "null"}` | PASS |
| C12 | each description names `` `storageState` ``, "absolute path", "never written", 3 cases | same invocation, 3 cases PASSED | `tests/test_storage_state.py:268-270` - `assert "`storageState`" in description` / `"absolute path" in description` / `"never written" in description` | PASS |
| C13 | README: `--save-storage=`, and in the same section: not committed, `sessionStorage` not carried, expired session shows login | the four `grep -c` commands of checks.md, literally: `1`, `1`, `1`, `1` | `README.md` section `## Pages behind a login` (diff `README.md:55-68`): `codegen --save-storage=/home/me/admin-state.json`; "do not commit it"; "`sessionStorage` is not carried"; "When the session expires, the calls examine the login screen again". Each grep's single hit lies in that section (read, since the greps are not section-scoped) | PASS |
| C14 | `[Unreleased]` `### Added` names `storageState` | the sed/sed/grep pipeline of checks.md, literally: `1` | `CHANGELOG.md:11` - `` - `storageState` on `inspect_element`, `detect_visual_bugs` and `extract_tokens`: ... `` under `### Added` of `[Unreleased]` | PASS |
| C15 | `.specs/STATE.md` records AD-010, active, for `storageState`, beside ADR-0002 | the sed/grep pipeline of checks.md, literally: `1` | `.specs/STATE.md:77-83` - `### AD-010`, Decision names `storageState`, Reason cites ADR-0002, `**Status**: active.` | PASS |
| C16 | pyright, ruff check, ruff format --check, full pytest green | `.venv/bin/pyright --pythonpath .venv/bin/python` exit 0 (`0 errors, 0 warnings, 0 informations`); `.venv/bin/ruff check` exit 0 (`All checks passed!`); `.venv/bin/ruff format --check` exit 0 (`132 files already formatted`); `.venv/bin/pytest` exit 0, `523 passed in 1641.13s` | gate outputs, this run at HEAD `c8a0068` | PASS |

## Coverage

Not recomputed: the `Coverage` join runs only under `standard` and `ui`.

## Test policy rows

None: `checks.md` carries no `Test policy` section, and the verdicts run only under `standard` and `ui`.

## Faults injected

None: fault injection runs only under `standard` and `ui`.

## Level and sampling

- Level: C1-C11 go through the in-memory MCP client (`client.call_tool` / `client.list_tools`) against real Chromium and a real HTTP fixture with a `Secure; HttpOnly; SameSite=Strict; Path=/api/v1/admin` cookie, which is the boundary the plan's Surface names. C7-C10 reach `capture.capture` only through `inspect_element`, as the checks state; all three tools share the one `_read_storage_state` call at `src/squint_mcp/capture.py:346`, so that is sufficient.
- C4's `detect_visual_bugs` case asserts the absence on DESKTOP only (the default viewports); the claim names no viewport, so not a gap.
- C5 settles the `Cookie` header through the page's rendering (`#campaigns` / `#seen-sent`), not on the header itself. The fixture API is the only reader of the header (`tests/conftest.py:51-64`), so the inference holds.

## Swept existing

None: every `Swept` row in `checks.md` either names checks (C5-C10, C13) or is `n/a`. The one structural claim inside a row, "fails before a context exists, so nothing is left open" (failure modes), holds: `_read_storage_state` runs at `src/squint_mcp/capture.py:346` before `session.browser()` and `new_context`; a `new_context` rejection raises before any context is assigned (`:348-360`).

## Intent vs code

- Flow: holds. The three tools pass `storage_state=storageState` to every Capture (`tools/inspect_element.py`, `tools/detect_visual_bugs.py` per viewport, `tools/extract_tokens.py`); `capture.capture` checks the path, reads it in Python and hands Playwright a dict; nothing after `new_context` changed.
- Door 1: holds - `storageState: str | None = None` on all three signatures, published as camelCase.
- Door 2: holds - `Path(path).is_absolute()` at `src/squint_mcp/capture.py:108`, no resolution against the working directory.
- Impact "existing tests": holds - the only changed existing assertions are the three `set(properties) == {...}` lines, each gaining `storageState`; `tests/conftest.py` and `tests/helpers.py` only add.
- Gap (precision, not covered by any check): a file that is not valid UTF-8 escapes both AC 8 and AC 9. `Path(path).read_text(encoding="utf-8")` at `src/squint_mcp/capture.py:111` raises `UnicodeDecodeError` (a `ValueError`, not `OSError`), outside both `try` blocks. Probed directly: `_read_storage_state("<file starting 0xff 0xfe>")` -> `UnicodeDecodeError 'utf-8' codec can't decode byte 0xff in position 0`. Over MCP the SDK turns it into the opaque `UnexpectedToolError` "Error executing tool inspect_element" (`.venv/.../mcp/server/mcpserver/tools/base.py:161`), so the call fails without either specified message. Nothing of the file is quoted (AC 10 holds). C9's set "ways a file is not a storage state (3)" omitted this member; the fix is reading bytes and moving decoding into the `json.loads` `try` (or catching `UnicodeDecodeError` there).

## Gate

`.venv/bin/pytest` (full suite) - 523 passed, 0 failed in 1641.13s (0:27:21), exit 0. `.venv/bin/pyright --pythonpath .venv/bin/python` exit 0, `.venv/bin/ruff check` exit 0, `.venv/bin/ruff format --check` exit 0. Targeted run: 22 passed, 0 failed.
