# Login session from a file checks

Profile: light
Plan: `.specs/features/storage-state/plan.md`

16 checks in 3 slices · 2 one-way doors · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. Where `uv` is not on the path, `uv run <tool>` is `.venv/bin/<tool>`. Feature base: `21a397e`.

The page of the proofs is `tests/fixtures/storage-state.html`, served by `local_server`: its script asks `/api/v1/admin/me`, which answers 200 only to the cookie `sid=s3cret-session` and 401 otherwise, and renders `#campaigns` (with the clipped text `#clipped` and the text colour `#123456`) on 200, `#login` on 401. The file of the proofs holds that cookie with `HttpOnly`, `Secure`, `SameSite=Strict` and `Path=/api/v1/admin`, for `127.0.0.1`, and a `localStorage` entry `radio=s3cret-radio`.

## Checks

### S1 - a call sees the page as the session does · 7 files · 50 KB · ~13k

**C1** - `inspect_element` on `#campaigns` of the page with `storageState` naming the file returns that element (AC 1)
Proof: `uv run pytest "tests/test_storage_state.py::test_inspect_element_sees_the_screen_after_login" -v`

**C2** - `detect_visual_bugs` on the page with `storageState` and the viewports 1440x900 and 390x844 reports a `text-clipped` Finding on `#clipped` in each of the two viewports (AC 2)
Proof: `uv run pytest "tests/test_storage_state.py::test_detect_visual_bugs_judges_the_screen_after_login_in_every_viewport" -v`

**C3** - `extract_tokens` on the page with `storageState` reports `#123456` among the text colours (AC 3)
Proof: `uv run pytest "tests/test_storage_state.py::test_extract_tokens_reads_the_screen_after_login" -v`

**C4** - Without `storageState`, each tool sees the login screen: `inspect_element` on `#campaigns` fails with the zero-match error it gives today, `detect_visual_bugs` reports no Finding on `#clipped`, and `extract_tokens` reports no `#123456` (AC 4)
Proof: `uv run pytest "tests/test_storage_state.py::test_without_a_storage_state_a_call_sees_the_login_screen" -v` runs 3 cases

**C5** - After a call with `storageState` on a page that sets the cookie `seen=1` from its script, a second call with the same file sends `/api/v1/admin/me` a `Cookie` header with `sid=s3cret-session` and without `seen` (AC 5)
Proof: `uv run pytest "tests/test_storage_state.py::test_a_cookie_a_page_sets_does_not_reach_the_next_call" -v`

**C6** - The file of `storageState` holds the same bytes after a call as before it (AC 6)
Proof: `uv run pytest "tests/test_storage_state.py::test_the_storage_state_file_is_never_written" -v`

**C7** - `storageState` given as `state.json` fails the call with exactly `storageState must be an absolute path: "state.json".` (AC 7, door 2)
Proof: `uv run pytest "tests/test_storage_state.py::test_a_relative_storage_state_is_refused" -v`

**C8** - `storageState` naming an absolute path that does not exist fails the call with a message that starts `Could not read the storage state "<path>": ` and ends with `.` (AC 8)
Proof: `uv run pytest "tests/test_storage_state.py::test_a_storage_state_that_cannot_be_read_is_refused" -v`

**C9** - A file that is not JSON, a JSON array, and an object whose `cookies` is a string each fail the call with exactly `"<path>" is not a Playwright storage state.` (AC 9)
Proof: `uv run pytest "tests/test_storage_state.py::test_a_file_that_is_not_a_storage_state_is_refused" -v` runs 3 cases

**C10** - For a file that is not JSON but holds `s3cret-session`, and for an object holding the cookie `sid=s3cret-session` with no domain and the `localStorage` value `s3cret-radio`, the error text contains neither `s3cret-session` nor `s3cret-radio` (AC 10)
Proof: `uv run pytest "tests/test_storage_state.py::test_a_refused_storage_state_is_not_quoted" -v` runs 2 cases

**C11** - `tools/list` publishes `storageState` as an optional string input of `inspect_element`, `detect_visual_bugs` and `extract_tokens`, and of no other tool (door 1)
Proof: `uv run pytest "tests/test_storage_state.py::test_the_three_tools_take_an_optional_storage_state" -v`

### S2 - the record · 5 files · 30 KB · ~8k

**C12** - The published description of each of the three tools names `storageState` and says it is an absolute path that is never written (AC 11)
Proof: `uv run pytest "tests/test_storage_state.py::test_the_three_tools_describe_storage_state" -v` runs 3 cases

**C13** - `README.md` gives `playwright codegen --save-storage=`, and in the same section says the file must not be committed, that `sessionStorage` is not carried, and that an expired session shows the login page (AC 12)
Proof: `grep -c -- "--save-storage=" README.md` prints `1` or more
Proof: `grep -c "sessionStorage" README.md` prints `1` or more
Proof: `grep -ci "commit" README.md` prints `1` or more
Proof: `grep -ci "expire" README.md` prints `1` or more

**C14** - The `[Unreleased]` section of `CHANGELOG.md` has an entry under `### Added` that names `storageState` (AC 13)
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### /p' | grep -c "storageState"` prints `1` or more

**C15** - `.specs/STATE.md` records AD-010, active, for `storageState` beside ADR-0002 (plan, Impact)
Proof: `sed -n '/^### AD-010/,/^## Handoff/p' .specs/STATE.md | grep -c "storageState"` prints `1` or more

### S3 - gate

**C16** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| one-way doors (2) | door 1, the input C11 · door 2, absolute only C7 | - |
| tools that take `storageState` (3) | `inspect_element` C1 · `detect_visual_bugs` C2 · `extract_tokens` C3 | - |
| tools without `storageState` (3) | `inspect_element` C4 · `detect_visual_bugs` C4 · `extract_tokens` C4 | - |
| outcomes of a `storageState` (5) | loaded C1 · relative C7 · unreadable C8 · not a storage state C9 · not quoted C10 | - |
| ways a file is not a storage state (3) | not JSON C9 · not an object C9 · rejected by Playwright C9 | - |
| what isolation keeps out (2) | a cookie the page set C5 · a write to the file C6 | - |
| viewports of one call (2) | 1440x900 C2 · 390x844 C2 | - |

- C1 to C11 cross the MCP boundary; the error checks C7 to C10 call `inspect_element`, since the three tools reach `storageState` only through `capture.capture`
- C4, C9, C10 and C12 are table-driven over their sets, sizes 3, 3, 2 and 3

## Swept

- validation: C7, C8, C9
- failure modes: C8, C9 - a call that fails on its `storageState` fails before a context exists, so nothing is left open
- idempotency: C5, C6 - the file is read, never written, and a call leaves nothing behind for the next
- authorization: n/a - a local stdio server; whoever runs it can already read the files it reads
- concurrency: n/a - each Capture reads the file and builds its own context; calls share nothing but the browser, as today
- data lifecycle: C6 - Squint keeps no copy; the file's lifetime is the user's (the README, C13)
- dependency failure: C9 - a state Playwright rejects is a `ToolError`, not a crash
- state transitions: n/a - no state is held between calls
- observability: C10 - nothing of the file is logged or echoed; no log requirement otherwise

## Handoff

- S1-S2 = 50 KB of the files touched plus a new test module and fixture, ~16k tokens, one surface (`capture.capture` and the three tools), under the 150k budget - one builder

- **Boundary:** C1-C16 closed at the build commit of this branch
- **Settled mid-build:** C15 named AD-009, a number slice 10 had taken; renumbered to AD-010, the claim unchanged. The SDK calls a tool with the alias of a Field as the keyword, so door 1's `storageState` is the Python name of the parameter itself (ruff selects no naming rules), as the door's literal shape reads
- **Abandoned:** `Annotated[str | None, Field(alias="storageState")]` on a `storage_state` parameter - the SDK passed `storageState=` to the function, a `TypeError`
