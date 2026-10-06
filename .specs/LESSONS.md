# LESSONS - auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2

## Confirmed (load these at Specify/Design)

Corroborated across multiple features. Safe to apply as guidance.

_none_

## Candidates (under observation - do NOT load as guidance yet)

Seen once or not yet corroborated. Tracked, not trusted.

### L-001 - Assert the declared types of a tool input property as an exact set, not by membership of the expected type
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,mcp-tools` · harmful: 0
- features: foundation-ping
- evidence: tests/test_ping.py:46 (mutants M19, M27, FND-04) (tests,mcp-tools)
- last seen: 2026-10-06T15:21:32Z

### L-002 - State in the spec whether an optional tool parameter also accepts explicit null
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,mcp-tools` · harmful: 0
- features: foundation-ping
- evidence: FND-04 (spec.md:83) (spec,mcp-tools)
- last seen: 2026-10-06T15:21:32Z

### L-003 - Test an echoed or passed-through value with input that has surrounding whitespace and more than a few characters, not only a short clean word
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,mcp-tools` · harmful: 0
- features: foundation-ping
- evidence: tests/test_ping.py:51 (mutants N31, N32, FND-05) (tests,mcp-tools)
- last seen: 2026-10-06T15:26:56Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
