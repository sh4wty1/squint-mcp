# PR #2 review fixes Verification

**Verdict**: PASS
**Profile**: light (none declared in `AGENTS.md`; light is the default)
**Diff range**: 4b30933..d714282 (`HEAD` of `feat/foundation-ping`)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier), read-only

Every proof below was run by the Verifier at `d714282` on 2026-10-06. Items marked *read* were inspected, not executed.

## Binding sources

Step 1 did not run: it applies under the `ui` profile only, and the checklist marks no source as binding.

The three `Sources` entries were opened anyway, as context for step 3:

| Source | Opened | Contradiction |
|---|---|---|
| PR #2 review 5430958753 (body and 4 inline comments) | yes - `gh api .../pulls/2/reviews/5430958753` | none - F1 to F4 map one to one onto C1 to C4 |
| `docs/agents/triage-labels.md` | yes | none - the five strings in C2 match the right-hand column, rows 7 to 11 |
| `.specs/features/foundation-ping/spec.md:63` | yes | none - line 63 reads "The roadmap is written in Portuguese" |

## Checks

| Check | Claim | Proof run | Evidence | Result |
|---|---|---|---|---|
| C1 | Private vulnerability reporting is enabled on `sh4wty1/squint-mcp` | `gh api repos/sh4wty1/squint-mcp/private-vulnerability-reporting --jq .enabled` exit 0 | output: `true` (the review recorded `{"enabled":false}`) | PASS |
| C2 | The five triage labels exist in the repo | `gh label list --limit 200 --json name --jq '[.[].name] as $have \| ["needs-triage","needs-info","ready-for-agent","ready-for-human","wontfix"] - $have'` exit 0 | output: `[]`. Full list, 14 labels, well under the 200 limit: `accessibility, bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix, ready-for-agent, needs-triage, needs-info, ready-for-human` | PASS |
| C3 | On initialize, `serverInfo.version` equals the installed `squint-mcp` package version | `uv run pytest "tests/test_ping.py::test_server_reports_its_version" -v` - `collected 1 item`, `test_server_reports_its_version[asyncio] PASSED`, `1 passed` | `tests/test_ping.py:31` - `assert client.server_info.version == VERSION`; expected value at `tests/test_ping.py:12` - `VERSION = version(NAME)` with `NAME = "squint-mcp"` (line 11), `version` from `importlib.metadata` (line 3) | PASS |
| C4 | The Language section of `CONTRIBUTING.md` names `docs/ROADMAP.md` and `REQUIREMENTS.md` as maintainer planning notes kept in Portuguese | `grep -n -E 'ROADMAP\.md.*REQUIREMENTS\.md.*Portuguese' CONTRIBUTING.md` exit 0, one hit at line 32 | `CONTRIBUTING.md:32` - "The exceptions are [`docs/ROADMAP.md`](docs/ROADMAP.md) and [`REQUIREMENTS.md`](REQUIREMENTS.md), the maintainer's planning notes, which stay in Portuguese." Headings: `## Language` at line 30, next heading `## Changelog` at line 36, so line 32 is inside the section | PASS |

4 of 4 proven.

Notes on existence and relevance:

- C3's test name appears once in the tree, at `tests/test_ping.py:29`, and it is new in this range (`git diff 4b30933..HEAD -- tests/test_ping.py` adds lines 29 to 31). The filter matched one collected item, so the green run is not an empty selection.
- C3's expected value is not vacuous: the installed version is `'0.1.0'` (ran `importlib.metadata.version('squint-mcp')`), matching `pyproject.toml:3`. The review states that a server built without `version=` reports `''`, which would not equal `'0.1.0'`. That failing direction was read, not executed; fault injection does not run under `light`.
- C3's proof sits at the right level: the assertion reads `client.server_info`, the value returned by the MCP initialize handshake, through the in-memory client. The claim names `serverInfo`, and the proof is at that boundary.
- C4's line is new in this range (`git diff 4b30933..HEAD -- CONTRIBUTING.md` changes line 32 only).
- C1 and C2 are live repository state, not properties of a commit. They hold as of this run.

## Swept rows that claim something exists

| Row | Claim | Checked | Result |
|---|---|---|---|
| idempotency | `gh label create` on an existing label fails | *read*: `gh label create --help` says "Create a new label on GitHub, or update an existing one with `--force`" and `-f, --force  Update the label color and description if label already exists`. Not executed, because creating a label is a write | consistent with the claim, not demonstrated |
| authorization | C1 needs repo admin; the `gh` user owns the repo | *ran*: `gh api user --jq .login` prints `sh4wty1`; `gh api repos/sh4wty1/squint-mcp --jq '{owner: .owner.login, admin: .permissions.admin}'` prints `{"admin":true,"owner":"sh4wty1"}` | holds |

The remaining rows say *not in scope*, which is policy and has nothing in the code to be wrong about.

## Test policy rows

Did not run: `Coverage` and `Test policy` work applies under `standard` and `ui`, and the checklist carries neither section.

## Faults injected

Did not run: step 4 applies under `standard` and `ui`.

## Gaps in the checklist

None of these changes a verdict. Ranked by how much they could hide.

1. **Precision gap, C4.** The proof says "exits 0 with a hit under `## Language`", but the grep cannot see headings; it would pass with the sentence in any section. The regex also does not test for "maintainer planning notes". Both were settled by reading `CONTRIBUTING.md:30-36`, not by the proof.
2. **Durability gap, C1 and C2.** Both proofs read live settings, so they are true today and nothing in the repo fails if the setting is switched off or a label is deleted. The checklist puts the CI label check out of scope by decision; this records the consequence, not a disagreement with it.
3. **Precision gap, C3.** The expected value comes from `importlib.metadata.version("squint-mcp")`, the same call the server uses at `src/squint_mcp/__init__.py:6`. That is exactly what the claim states ("equals the installed package version"), and it does catch the regression F3 names. It would not catch a wrong version in `pyproject.toml`, which the claim does not ask for.
4. **Sampling gap, C2: none found.** F2 concerns labels applied by issue templates. Both templates (`.github/ISSUE_TEMPLATE/bug_report.md:4`, `feature_request.md:4`) apply only `needs-triage`, which is in the proven set.

No level gap found.

## Gate

- `uv run pyright` - 0 errors, 0 warnings, 0 informations
- `uv run ruff check` - All checks passed
- `uv run ruff format --check` - 30 files already formatted
- `uv run pytest` - 12 passed, 0 failed

Working tree after the run: clean apart from this report, which is untracked and not committed.
