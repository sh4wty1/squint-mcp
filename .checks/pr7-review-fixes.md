# PR #7 review fixes

Profile: light (none declared in `AGENTS.md`).

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/7#pullrequestreview-5445952012 - findings F1 to F5, with the repro and the fix each one asks for
- https://github.com/sh4wty1/squint-mcp/pull/7 (Codex review 5445082640) - two P2 comments: line breaks in attribute values, order between Checks
- conversation - F1 is settled: fix it with one more condition, numbers unchanged; the Codex comment on Check order becomes an issue for slice 4; one atomic commit per finding, each starting from a failing fixture case through the MCP tool boundary

## Out of scope

- Global document order across Checks (Codex, `detect_visual_bugs.py:99`) - only one Check exists; an issue is opened for slice 4
- Changing `overflowPx`, the thresholds or the literal of DVB-14 - decided by the user
- Escaping NUL in attribute values - the HTML parser never yields one; only script can set it
- Anything in `inspect_element`'s output - the new `Element` field is not part of `InspectElementResult`
- `design.md`, `tasks.md` - the user asked for the decision in `spec.md` only

## Landing

Touches `checks/text_clipped.py` (two clauses in `_is_clipped`), `js/collect_elements.js` (`attribute`, `segment`, `layout`, one new field), `capture.py` (one argument key), `models.py` (one `Element` field), the fixtures `text-clipped-clean.html` and `selectors.html`, their two test modules, and `spec.md`. Reuses `detect`, `findings_on`, `selector_of` and the `reported` helper.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| How the Check tells own text from an overflowing child (F1) | `Element.own_text_right: float \| None`: the largest `right` of the client rects of a `Range` over each direct text node, in page coordinates as painted, `null` when they have no rect. The Check reports only when it is greater than `box.x + border.left + clientWidth` | Listing the case under Out of Scope in `spec.md` - leaves a reproduced false Finding. Changing `overflowPx` to the text's own overflow - changes the documented numbers. Decided by the user |
| Line breaks in a quoted attribute value | `\a `, `\d `, `\c ` (hex escape plus one space) after the existing `\\` and `\"` | `CSS.escape(value)` - it also escapes spaces, which changes `button[aria-label="Close dialog"]` (DVB-36) |

- Nothing else in this change is hard to reverse

## Checks

### S1 - Hidden text over a pattern (F2) · 3 files · 14 KB · ~4k

**C1** - `#hidden-over-pattern` (`.clipped`, `visibility: hidden`, inside a parent with a `repeating-linear-gradient` background) yields no Finding
Proof: `uv run pytest "tests/test_text_clipped.py::test_hidden_text_over_a_pattern_is_not_reported" -v`

### S2 - Selector escaping (F4, Codex) · 3 files · 15 KB · ~4k

**C2** - A clipped `<o:p>` gets the selector `body > main > o\:p`
Proof: `uv run pytest "tests/test_selectors.py::test_a_tag_name_with_a_colon_is_escaped_in_the_css_path" -v`

**C3** - A `data-testid` holding a line break gets the selector `[data-testid="line\a break"]`
Proof: `uv run pytest "tests/test_selectors.py::test_a_line_break_in_an_attribute_value_is_escaped" -v`

**C4** - Every Finding selector of `selectors.html`, the two new ones included (21 Findings), resolves in `inspect_element` to the Finding's box
Proof: `uv run pytest "tests/test_selectors.py::test_every_finding_selector_resolves_to_its_element_in_inspect_element" -v`

### S3 - One transform tolerance (F5) · 3 files · 12 KB · ~3k

**C5** - The collector has no literal tolerance: it reads the one passed from `config.TRANSFORM_MIN_SIZE_DIFF_PX`
Proof: `grep -c "< 1" src/squint_mcp/js/collect_elements.js` prints 0
Proof: `grep -c "TRANSFORM_MIN_SIZE_DIFF_PX" src/squint_mcp/capture.py` prints 1
Proof: `uv run pytest "tests/test_inspect_element.py::test_box_model_content_keeps_the_fractional_size_of_an_untransformed_element" -v`

No failing case exists for C5: the two values are equal today, so nothing observable changes.

### S4 - Own text against the padding edge (F1) · 6 files · 60 KB · ~15k

**C6** - `#child-overflows` (100px of text in a 300px box, an absolutely positioned child reaching 340px) yields no Finding
Proof: `uv run pytest "tests/test_text_clipped.py::test_fitting_text_beside_an_overflowing_child_is_not_reported" -v`

**C7** - `findings[0]` of `text-clipped-bug.html` still equals the literal of DVB-14
Proof: `uv run pytest "tests/test_selectors.py::test_first_finding_of_the_bug_fixture_is_the_documented_one" -v`

**C8** - `spec.md` records the decision and a new criterion, DVB-71, traced
Proof: `grep -c "DVB-71" .specs/features/detect-visual-bugs-text-clipped/spec.md` prints 2 or more

### S5 - Gate

**C9** - Type check, lint, format and the whole suite are green, with no existing assertion changed other than the two that enumerate the Findings of `selectors.html`: the count in `test_selectors.py` (19 to 21) and the document-order list in `test_detect_visual_bugs.py` (two texts appended)
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: C2, C3 - a generated selector must be accepted back by `inspect_element`
- failure modes: C6 - an element whose text nodes have no rect serialises `null`, not `NaN` (`-Infinity` guarded)
- idempotency: not in scope - the tool is read-only
- authorization: not in scope
- concurrency: not in scope - Check order across Checks goes to an issue
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope - no log requirement

## Handoff

S1-S5 = ~26k of reading, two surfaces (Check, collector). One agent, no handoff.
