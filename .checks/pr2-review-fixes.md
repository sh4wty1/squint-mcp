# PR #2 review fixes

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/2#pullrequestreview-5430958753 - the four findings (F1 to F4) and the fix each one asks for
- `docs/agents/triage-labels.md` - the five label strings the tracker must carry
- `.specs/features/foundation-ping/spec.md:63` - the roadmap is written in Portuguese, by decision

## Out of scope

- Translating `docs/ROADMAP.md` or `REQUIREMENTS.md` to English - F4 is settled by stating the exemption; `AGENTS.md` keys on the Portuguese status words
- A CI step that checks template labels against the repo (the review's lint-rule idea) - new capability nobody asked for
- `git push` - needs an explicit go-ahead

## Landing

Touches `tests/test_ping.py` and `CONTRIBUTING.md`, plus two repository settings on GitHub (private vulnerability reporting, labels). The new test reuses the `client` fixture and the `VERSION` constant already in `tests/test_ping.py`.

None - a test, one sentence of prose, a settings toggle with a documented `DELETE`, and labels that can be deleted are all reversible at no cost.

## Checks

### S1 - Repository settings (F1, F2) · 0 files · ~0k

**C1** - Private vulnerability reporting is enabled on `sh4wty1/squint-mcp`
Proof: `gh api repos/sh4wty1/squint-mcp/private-vulnerability-reporting --jq .enabled` prints `true`

**C2** - Each of the five triage labels in `docs/agents/triage-labels.md` exists in the repo: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`
Proof: `gh label list --limit 200 --json name --jq '[.[].name] as $have | ["needs-triage","needs-info","ready-for-agent","ready-for-human","wontfix"] - $have'` prints `[]`

### S2 - Server version is pinned by a test (F3) · 2 files · 3 KB · ~1k

**C3** - On initialize, `serverInfo.version` equals the installed `squint-mcp` package version
Proof: `uv run pytest "tests/test_ping.py::test_server_reports_its_version" -v`

### S3 - English rule states its exemption (F4) · 1 file · 2 KB · ~1k

**C4** - The Language section of `CONTRIBUTING.md` names `docs/ROADMAP.md` and `REQUIREMENTS.md` as maintainer planning notes kept in Portuguese
Proof: `grep -n -E 'ROADMAP\.md.*REQUIREMENTS\.md.*Portuguese' CONTRIBUTING.md` exits 0 with a hit under `## Language`

## Swept

- validation: not in scope - no input surface changes
- failure modes: not in scope - no runtime code changes
- idempotency: C2 - `gh label create` on an existing label fails, so only the missing ones are created
- authorization: C1 needs repo admin; the `gh` user owns the repo
- concurrency: not in scope
- data lifecycle: not in scope
- dependency failure: not in scope
- state transitions: not in scope
- observability: not in scope

## Handoff

S1-S3 = ~2k, one agent, no handoff.
