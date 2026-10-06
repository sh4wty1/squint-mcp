# Squint

Squint examines a rendered web page by crossing what the browser reports (DOM/CSS) with what is actually painted (pixels), and reports the visual problems it finds without needing a baseline.

## Language

**Capture**:
A stabilized snapshot of one page at one viewport: its DOM/CSS data together with its rendered pixels.
_Avoid_: Snapshot, screenshot, page session

**Check**:
A single named examination of a Capture that yields zero or more Findings.
_Avoid_: Detector, rule, heuristic

**Finding**:
One problem reported by one Check on one element in one Capture, carrying the evidence that supports it.
_Avoid_: Issue, bug, violation, result

**Profile**:
A named set of Checks that are run together.
_Avoid_: Preset, ruleset, suite

**Audit**:
One run of a Profile against a page, producing its Findings and optionally a score.
_Avoid_: Scan, analysis, report
