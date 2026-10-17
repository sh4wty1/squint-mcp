# Login session from a file (`storageState`)

Roadmap slice 12.

## Problem

Every call opens its page in a context with no cookies and no storage. A page behind a login is examined as its login screen: the Admin of central-jogos-gc2 keeps its session in a cookie `HttpOnly; Secure; SameSite=Strict; Path=/api/v1/admin` (12h), so `detect_visual_bugs`, `inspect_element` and `extract_tokens` pointed at it see the login form and never the list of Campaigns. An agent asked to check the Admin falls back to driving a browser by hand (Playwright MCP), and gets none of the Checks.

No measurement in the source; the report is the maintainer's, on the Admin as it stands today.

When this ships: a call given the file of a session logged in once opens the page as that session sees it, and is still isolated from every other call.

## Flow

Reuses Playwright's own storage state format and its loading into a new context (`browser.new_context(storage_state=...)`): no new module, no format of Squint's own.

1. a tool call with `storageState` -> `tools/inspect_element.py`, `tools/detect_visual_bugs.py`, `tools/extract_tokens.py` (exist) - pass it to every Capture they take (door 1)
2. `capture.capture` (exists) - checks that the path is absolute (door 2), reads the file and creates the context of the call with that state; everything after `new_context` is unchanged
3. out: the same result shapes; the file is only read, and the context is closed at the end of the Capture as today

## Impact

| Front | What changes |
| --- | --- |
| domain | new term: Storage state - a file of cookies and `localStorage` per origin in Playwright's format, loaded into the context of one call. Lives in `capture.py` and the three tools |
| domain | "each call is isolated" (`docs/SPEC.md` story 15) still holds: the state is loaded into a fresh context per Capture and never written back |
| contract | the three tools gain one optional input; a call without it behaves as today |
| docs | `docs/adr/0002-checks-consume-captures-only.md` names attaching over CDP as the way past the initial-state limit; this slice adds a second, narrower way for the first screen after a login. Recorded as AD-009 in `.specs/STATE.md` |
| stored data | nothing to migrate - nothing is persisted |

## Relations

`None - no stored-data shape change`

## Surface

`None - no HTTP route: the three tools are MCP tools over stdio, whose only outcomes are a result or a ToolError (AD-002). The input they gain is door 1; its outcomes are AC 1 to 10`

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1. The input | `storageState: str \| None`, the path of a JSON file in Playwright's storage state format, the same name on the three tools | `storage_state` - every name on the wire is camelCase (AD-002), and the SDK publishes a Field alias as the input name. The state inline as a JSON object - puts the session's cookies into the agent's transcript and the client's logs. A `cookies` list - cannot carry `localStorage`, and invents a format that `playwright codegen --save-storage` already writes |
| 2. Which paths | absolute only; a relative path is a `ToolError` | resolving a relative path against the server's working directory - the agent does not know the working directory of a stdio server its client started, so the same call would read different files from different clients |

- Nothing else in this change is hard to reverse

## Criteria

### S1: a call sees the page as the session does (P1)

A page that asks its API for a session cookie renders its logged-in screen when the call carries the file of that session.

**Acceptance Criteria**

1. WHEN `inspect_element` is called on a page that renders `#campaigns` only if its request to `/api/v1/admin/` carries a cookie `HttpOnly; Secure; SameSite=Strict; Path=/api/v1/admin`, with `storageState` naming a file that holds that cookie, THEN the system SHALL return the element `#campaigns`
2. WHEN `detect_visual_bugs` is called on that page with that `storageState` and two viewports THEN the system SHALL report, in each viewport, the Finding of the clipped text that only the logged-in screen has
3. WHEN `extract_tokens` is called on that page with that `storageState` THEN the system SHALL report the text colour that only the logged-in screen uses
4. WHEN any of the three tools is called on that page without `storageState` THEN the system SHALL see the login screen: `inspect_element` on `#campaigns` SHALL fail with the zero-match error it gives today
5. WHEN a call with `storageState` loads a page that sets a cookie of its own THEN a later call with the same file SHALL not send that cookie
6. WHEN a call with `storageState` ends THEN the file SHALL hold the same bytes it held before the call
7. IF `storageState` is not an absolute path THEN the system SHALL fail the call with `ToolError` `storageState must be an absolute path: "<value>".`
8. IF the file of `storageState` does not exist or cannot be read THEN the system SHALL fail the call with `ToolError` `Could not read the storage state "<path>": <reason>.`
9. IF the file of `storageState` is not a JSON object, or Playwright rejects it as a storage state THEN the system SHALL fail the call with `ToolError` `"<path>" is not a Playwright storage state.`
10. IF a call fails on its `storageState` THEN the message SHALL contain no cookie value nor any `localStorage` value of the file

**Independent test:** serve the fixture over HTTP, call `inspect_element` on `#campaigns` with and without the file.

### S2: the record (P2)

**Acceptance Criteria**

11. The docstrings of the three tools SHALL describe `storageState`: an absolute path, Playwright's format, loaded into each call and never written
12. The README SHALL have a section on pages behind a login that gives the command `playwright codegen --save-storage=<file> <url>`, says the file holds the session's secrets and must not be committed, that `sessionStorage` is not carried, and that an expired session shows the login page
13. The `[Unreleased]` section of `CHANGELOG.md` SHALL have an `Added` entry for `storageState` on the three tools

**Independent test:** read the three places.

## Out of scope

| Excluded | Why |
| --- | --- |
| `sessionStorage` | Playwright's storage state does not carry it; roadmap slice 12, "Não entra" |
| Logging in from Squint (credentials, a login flow) | roadmap slice 12, "Não entra"; ADR-0002 rules out interaction in the tools |
| States reached after a click (an editor, a dialog, a page with no route) | roadmap slice 13, by attaching to an open Chrome over CDP |
| Writing the state back after a call | would make calls depend on each other (`docs/SPEC.md` story 15) |
| Telling an expired session apart from a valid one | Squint cannot tell a login page from any other page; the README says what an expired session looks like |
| The state inline in the call | door 1 |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| A JSON object with neither `cookies` nor `origins` | accepted, as Playwright accepts it: the page opens with no session | measured: `new_context(storage_state={"foo": 1})` succeeds on Playwright 1.63; a second validator would reject files Playwright reads | n |
| IndexedDB in a file written by `codegen --save-storage` | passed to Playwright as it is | codegen writes it (playwright.dev/python/docs/codegen); Squint reads the file as a whole and does not pick keys | n |
| Where the file is read | in Python, before the context, and handed to Playwright as an object | tells a missing file (AC 8) from a bad one (AC 9), and keeps Playwright's own error text, which may quote the file, out of the message (AC 10) | n |
| The page of the tests | an HTTP fixture whose script asks `/api/v1/admin/me` and renders `#campaigns` on 200, `#login` on 401, served by the existing `local_server` | the Admin's own shape: a single page whose screen depends on an API answer, with the cookie scoped to the API path. Measured: Chromium sends a `Secure` cookie to `http://127.0.0.1` and `http://localhost` | n |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| tools `inspect_element`, `detect_visual_bugs`, `extract_tokens` | response shape | existing - no field added, removed or renamed |
| tools `inspect_element`, `detect_visual_bugs`, `extract_tokens` | error shape and codes | AC 7, AC 8, AC 9, AC 10 - `ToolError` with a concrete message (AD-002) |
| tools `inspect_element`, `detect_visual_bugs`, `extract_tokens` | who may call | n/a - a local stdio server: whoever runs it can already read the files it can read |
| tools `inspect_element`, `detect_visual_bugs`, `extract_tokens` | rate limits | n/a - a local stdio server, as before |
| tools `inspect_element`, `detect_visual_bugs`, `extract_tokens` | versioning | AC 13 - an optional input is added, nothing breaks; recorded in the CHANGELOG |
| document `README.md` | structure, depth, what the reader does next | AC 12 - one section: how to make the file, what it holds, what it does not carry |
| document `CHANGELOG.md` | structure | AC 13 - one entry under `[Unreleased]`, in the form of the existing ones |

## Sources

- `docs/ROADMAP.md`, section 12 - what enters and what does not
- https://playwright.dev/python/docs/api/class-browser - `new_context(storage_state=...)`: a path or a dict of `cookies` and `origins` with `localStorage`
- https://playwright.dev/python/docs/codegen - `--save-storage` saves cookies, `localStorage` and IndexedDB at the end of the session
