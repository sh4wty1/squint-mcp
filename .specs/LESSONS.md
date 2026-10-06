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

### L-004 - Assert pixel values at known offsets of a returned image, not only its dimensions
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: capture-inspect-element
- evidence: tests/test_inspect_element.py:76 (mutant M07, CAP-13) (tests,vision)
- last seen: 2026-10-06T16:48:46Z

### L-005 - Test page-coordinate values on a page that is scrolled when they are read, not only at scroll zero
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,capture` · harmful: 0
- features: capture-inspect-element
- evidence: src/squint_mcp/js/collect_elements.js:19 (mutant M27, CAP-20) (tests,capture)
- last seen: 2026-10-06T16:48:46Z

### L-006 - Assert the elapsed time of a timeout test, not only that the timeout error is returned
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,timeouts` · harmful: 0
- features: capture-inspect-element
- evidence: tests/test_inspect_element.py:334 (mutant M25, CAP-35) (tests,timeouts)
- last seen: 2026-10-06T16:48:46Z

### L-007 - Pin a time threshold with a case that ends just past it, not only with one that never ends
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,timeouts` · harmful: 0
- features: capture-inspect-element
- evidence: src/squint_mcp/config.py:11 (mutant M23, CAP-22) (tests,timeouts)
- last seen: 2026-10-06T16:48:46Z

### L-008 - When a criterion names the document section a line belongs to, put the line in that section
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `docs` · harmful: 0
- features: capture-inspect-element
- evidence: CAP-46 (README.md:47) (docs)
- last seen: 2026-10-06T16:48:46Z

### L-009 - Give every field of a structured tool input an outcome in the spec that depends on that field
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,mcp-tools` · harmful: 0
- features: capture-inspect-element
- evidence: CAP-17 (spec.md:110, mutant M34) (spec,mcp-tools)
- last seen: 2026-10-06T16:48:46Z

### L-010 - Pin a time threshold from both sides, with one case that ends shortly before it and one shortly after it
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,timeouts` · harmful: 0
- features: capture-inspect-element
- evidence: src/squint_mcp/config.py:11 (mutant N9, CAP-21) (tests,timeouts)
- last seen: 2026-10-06T17:05:32Z

### L-011 - Patch a config value in a test with a value of the same type the config holds
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,config` · harmful: 0
- features: capture-inspect-element
- evidence: tests/test_inspect_element.py:364 (mutant N11, CAP-35) (tests,config)
- last seen: 2026-10-06T17:05:32Z

### L-012 - Give a geometric rule an outcome in the spec for every axis and every edge it applies to, not for one corner
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,geometry` · harmful: 0
- features: capture-inspect-element
- evidence: spec.md:49, spec.md:53 (mutants N1, N7, N8; CAP-14, CAP-20) (spec,geometry)
- last seen: 2026-10-06T17:05:32Z

### L-013 - Set a latency tolerance in the spec as a fraction of the timeout the test uses, not as a fixed number of seconds larger than it
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec, timing` · harmful: 0
- features: capture-inspect-element
- evidence: CAP-35, mutants Y11 and Y15 (tests/test_inspect_element.py:377) (spec, timing)
- last seen: 2026-10-06T17:26:23Z

### L-014 - Give a geometric rule an outcome in the spec for coordinates below zero on each axis, not only for those past the far edge
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec, geometry` · harmful: 0
- features: capture-inspect-element
- evidence: PR #3 review F1 (src/squint_mcp/vision.py:25, src/squint_mcp/tools/inspect_element.py:66) (spec, geometry)
- last seen: 2026-10-06T17:47:43Z

### L-015 - Back every design claim about what a browser or library API covers with a test that fails when the claim is false
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `design, external-apis` · harmful: 0
- features: capture-inspect-element
- evidence: PR #3 review F2 (design.md:227, src/squint_mcp/js/stabilize.js:16) (design, external-apis)
- last seen: 2026-10-06T17:47:43Z

### L-016 - Give every resource a call acquires an outcome in the spec for each way the call can end: success, error, timeout and client cancellation
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec, lifecycle` · harmful: 0
- features: capture-inspect-element
- evidence: PR #3 review F3 (design.md:212, src/squint_mcp/capture.py:116) (spec, lifecycle)
- last seen: 2026-10-06T17:47:43Z

### L-017 - State in the spec what a long-lived cached handle does when the process behind it dies
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec, lifecycle` · harmful: 0
- features: capture-inspect-element
- evidence: PR #3 review F4 (src/squint_mcp/capture.py:35) (spec, lifecycle)
- last seen: 2026-10-06T17:47:43Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
