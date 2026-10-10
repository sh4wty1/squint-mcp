# LESSONS - auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2

## Confirmed (load these at Plan/Checks)

Corroborated across multiple features. Safe to apply as guidance.

### L-012 - Give a geometric rule an outcome in the spec for every axis and every edge it applies to, not for one corner
- signal: `spec_precision_gap` · recurrence: 2 feature(s) · scope: `spec,geometry` · harmful: 0
- features: capture-inspect-element, detect-visual-bugs-text-clipped
- evidence: spec.md:49, spec.md:53 (mutants N1, N7, N8; CAP-14, CAP-20) (spec,geometry) (+1 more)
- last seen: 2026-10-07T16:30:33Z

### L-020 - Assert the full order of a returned list on a fixture with several items of equal rank, not only the place of one item
- signal: `surviving_mutant` · recurrence: 2 feature(s) · scope: `tests,ordering` · harmful: 0
- features: detect-visual-bugs-text-clipped, low-contrast-real
- evidence: mutants J09, J10, src/squint_mcp/js/collect_elements.js:41,133 (DVB-15) (tests,ordering) (+1 more)
- last seen: 2026-10-08T05:06:17Z

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

### L-018 - Test a value taken from one of several captures with a call that produces more than one capture, not only one
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant T03, src/squint_mcp/tools/detect_visual_bugs.py:105 (DVB-45) (tests,vision)
- last seen: 2026-10-07T16:30:32Z

### L-019 - Give each clause of an or-condition a fixture that only that clause catches
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,checks` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant C11, src/squint_mcp/checks/text_clipped.py:50 (DVB-69) (tests,checks)
- last seen: 2026-10-07T16:30:33Z

### L-021 - Pin a count threshold with a case exactly at it and a case one past it, not only with a case far past it
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,thresholds` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutants J01, J03, src/squint_mcp/js/collect_elements.js:79,33 (DVB-16, DVB-37) (tests,thresholds)
- last seen: 2026-10-07T16:30:33Z

### L-022 - Pin each edge of a sampled pixel region with a fixture whose pixels differ just inside and just outside that edge
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutants C13, C14, src/squint_mcp/checks/text_clipped.py:65,63 (DVB-19) (tests,vision)
- last seen: 2026-10-07T16:30:33Z

### L-023 - Measure the colours a fixture really paints before pinning a colour count, because text anti-aliasing adds colours that differ between machines
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant V01, src/squint_mcp/vision.py:48 (DVB-19) (tests,vision)
- last seen: 2026-10-07T16:30:33Z

### L-024 - When a new requirement supersedes an older one, name in the spec every existing test assertion it changes
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: DVB-66 against DVB-01 (tests/test_inspect_element.py:421) (spec)
- last seen: 2026-10-07T16:30:33Z

### L-025 - Test a generated path with a repeated tag at an ancestor level, not only at the last segment
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,selectors` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N11 (collect_elements.js:70) (tests,selectors)
- last seen: 2026-10-07T17:06:39Z

### L-026 - Test an escaped identifier with a value that needs escaping and still passes every earlier filter
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,selectors` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N8 (collect_elements.js:25) (tests,selectors)
- last seen: 2026-10-07T17:06:39Z

### L-027 - Test the validation of a list input with the invalid item after a valid one, not only alone
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,validation` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N10 (detect_visual_bugs.py:73) (tests,validation)
- last seen: 2026-10-07T17:06:40Z

### L-028 - Test a message that counts things with a count of exactly one for every noun it pluralizes
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,messages` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N5 (detect_visual_bugs.py:46) (tests,messages)
- last seen: 2026-10-07T17:06:40Z

### L-029 - Test deduplication with a repeat that is not adjacent to its first occurrence, so that keeping the first differs from keeping the last
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,ordering` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N6 (detect_visual_bugs.py:82) (tests,ordering)
- last seen: 2026-10-07T17:06:40Z

### L-030 - Pin a rule that counts characters in a string with a case where those characters are not adjacent
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,selectors` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N7 (collect_elements.js:33) (tests,selectors)
- last seen: 2026-10-07T17:06:40Z

### L-031 - Pin a clamp with an input that would cross the bound it guards, not only with inputs that stay inside it
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,geometry` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant N4 (text_clipped.py:65) (tests,geometry)
- last seen: 2026-10-07T17:06:40Z

### L-032 - Test a rule that reports the first of several offending items with an input that holds two of them, not one
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,validation` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant M1 (detect_visual_bugs.py:73) (tests,validation)
- last seen: 2026-10-07T17:41:29Z

### L-033 - Pin which box of an element a measurement uses with a fixture whose padding makes the padding box and the content box differ
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,geometry` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant M4 (text_clipped.py:64) (tests,geometry)
- last seen: 2026-10-07T17:41:29Z

### L-034 - Name in the spec every character an escaping rule covers, not only the one its example shows
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec` · harmful: 0
- features: detect-visual-bugs-text-clipped
- evidence: mutant M6 (collect_elements.js:17); Assumptions: selector quoting (spec)
- last seen: 2026-10-07T17:41:29Z

### L-035 - Give every component of a sort order its own acceptance criterion whose outcome changes when that component is dropped
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,ordering` · harmful: 0
- features: low-contrast-real
- evidence: mutant S3; spec.md:68 against LCR-37 (spec.md:186) (spec,ordering)
- last seen: 2026-10-08T05:06:17Z

### L-036 - Pin a rule that judges an element on its own content with a fixture where its child's content would change the outcome
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,checks` · harmful: 0
- features: low-contrast-real
- evidence: mutant C3b, src/squint_mcp/js/collect_elements.js:132 (LCR-10) (tests,checks)
- last seen: 2026-10-08T05:06:18Z

### L-037 - Test a rule that reads a list of regions with an element that has more than one region and whose outcome depends on a later one
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: low-contrast-real
- evidence: mutant V3, src/squint_mcp/vision.py:64 (tests,vision)
- last seen: 2026-10-08T05:06:18Z

### L-038 - Pin a pixel-intensity threshold with fixture pixels just on each side of it, not only with pixels at the two ends of the range
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,thresholds` · harmful: 0
- features: low-contrast-real
- evidence: mutants G8, G8b, src/squint_mcp/config.py:98 (tests,thresholds)
- last seen: 2026-10-08T05:06:18Z

### L-039 - Give every Squint default threshold in config an acceptance criterion whose outcome changes when the value changes
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,config` · harmful: 0
- features: low-contrast-real
- evidence: LCR-21 (spec.md:130), Terms: Text pixels (spec.md:23); mutants G8, G8b (spec,config)
- last seen: 2026-10-08T05:06:18Z

### L-040 - State in the spec whether a rule reaches open shadow trees, with a fixture that has a shadow root, whenever the code walks them
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec,shadow-dom` · harmful: 0
- features: low-contrast-real
- evidence: mutant C2, src/squint_mcp/js/collect_elements.js:95; design.md:101 (spec,shadow-dom)
- last seen: 2026-10-08T05:06:18Z

### L-041 - Give each instance a criterion lists in parentheses its own fixture, or name only the instance the test pins
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec` · harmful: 0
- features: low-contrast-real
- evidence: LCR-51 (spec.md:219), tests/test_low_contrast_real.py:299 (spec)
- last seen: 2026-10-08T05:06:18Z

### L-042 - Pin a rule that pools a list of regions with a fixture whose outcome depends on a region that is neither the first nor the last
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,vision` · harmful: 0
- features: low-contrast-real
- evidence: mutant V5, src/squint_mcp/vision.py:64 (LCR-55) (tests,vision)
- last seen: 2026-10-08T05:47:06Z

### L-043 - Test a rule over the own text of an element with text that a child splits into several text nodes, not only with one text node
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `tests,checks` · harmful: 0
- features: low-contrast-real
- evidence: mutant C4, src/squint_mcp/js/collect_elements.js:139 (LCR-55) (tests,checks)
- last seen: 2026-10-08T05:47:06Z

### L-044 - When a criterion says all of a set, give it a fixture where each member alone decides the outcome, or name the members it pins
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `spec` · harmful: 0
- features: low-contrast-real
- evidence: LCR-55 (spec.md:111); mutants V5, C4 (spec)
- last seen: 2026-10-08T05:47:06Z

### L-045 - Run the grep proofs of the checks after the last edit of a file, since a new comment can bring back the reference a check forbids
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `checks,comments` · harmful: 0
- features: capture-pixel-budget
- evidence: C14 - src/squint_mcp/vision.py:69 (checks,comments)
- last seen: 2026-10-09T14:40:32Z

### L-046 - Prove a limit on a fixture whose result differs on each side of the limit, not on one that reads the same either way
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `tests,limits` · harmful: 0
- features: capture-pixel-budget
- evidence: C3 - src/squint_mcp/vision.py:49 (tests,limits)
- last seen: 2026-10-09T14:40:32Z

### L-047 - Back every design claim about what a browser or library API covers with a test that fails when the claim is false
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `design, external-apis` · harmful: 0
- features: offscreen-overflow
- evidence: C11 - tests/test_offscreen_overflow.py:140 (verification.md precision gap 1) (design, external-apis)
- last seen: 2026-10-10T02:52:15Z

### L-048 - Assert where a criterion places a text in a message, such as at its end, with an assertion of that place, not with substring membership
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `tests,messages` · harmful: 0
- features: offscreen-overflow
- evidence: C16 - tests/test_detect_visual_bugs.py:341 (verification.md precision gap 2) (tests,messages)
- last seen: 2026-10-10T02:52:15Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
