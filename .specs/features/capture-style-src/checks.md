# Measure a page whose policy refuses inline styles - checks

Profile: light
Plan: `.specs/features/capture-style-src/plan.md`

9 checks in 1 slice · 1 one-way door · 0 open

## Checks

### S1 - a page under a style-src policy gets its Findings · 6 files · 25 KB · ~7k

`style-src.html` holds its styles in `style-src.css`, under `<meta http-equiv="Content-Security-Policy" content="style-src file:">`. `style-src-refused.html` is the same policy with one inline `<style>` of its own.

**C1** - On `style-src.html`, `detect_visual_bugs` with `checks: ["low-contrast-real"]` returns exactly one Finding on `#flat`, a text of `rgb(119, 119, 119)` on white (4.47:1) (AC 1)
Proof: `uv run pytest tests/test_style_src.py -k "test_a_text_of_low_contrast_is_reported_under_the_policy"`
**C2** - On `style-src.html`, `detect_visual_bugs` with `checks: ["overlap"]` returns exactly one Finding on `#covered`, whose last 120px of 200px an opaque box covers (60%) (AC 2)
Proof: `uv run pytest tests/test_style_src.py -k "test_a_covered_text_is_reported_under_the_policy"`
**C3** - On `style-src.html`, `detect_visual_bugs` with `checks: ["low-contrast-real"]` returns exactly one Finding on `#shadow-host span`, a text of 4.47:1 inside an open shadow root (AC 3)
Proof: `uv run pytest tests/test_style_src.py -k "test_a_text_in_an_open_shadow_root_is_reported_under_the_policy"`
**C4** - On `style-src.html`, `detect_visual_bugs` returns the same list of `(selector, check)` pairs, in the same order, as on a copy of the page without the `<meta>` policy, and that list is not empty (AC 1, 2, 3, 5)
Proof: `uv run pytest tests/test_style_src.py -k "test_the_policy_changes_no_finding"`
**C5** - On `style-src-refused.html`, `inspect_element` on `#refused` returns `computed.color` `rgb(0, 0, 0)` from the sheet, not the `rgb(255, 0, 0)` of the page's inline `<style>` (AC 4)
Proof: `uv run pytest tests/test_style_src.py -k "test_the_page_policy_still_refuses_its_own_inline_style"`
**C6** - On `style-src.html`, whose script sets `document.adoptedStyleSheets` at load to a sheet that paints `#adopted` `rgb(119, 119, 119)`, `detect_visual_bugs` with `checks: ["low-contrast-real"]` returns exactly one Finding on `#adopted` (AC 5)
Proof: `uv run pytest tests/test_style_src.py -k "test_a_sheet_the_page_adopts_is_kept"`
**C7** - `extract_tokens` on `tokens-author.html` with no style returns `authorStyles: false` (AC 6)
Proof: `uv run pytest tests/test_extract_tokens.py -k "test_a_page_with_no_style_says_its_values_are_the_defaults"`
**C8** - `extract_tokens` on `tokens-author.html?shadow`, an open shadow root holding one unstyled `<span>` and no style anywhere, returns `authorStyles: false` (AC 6, door 1)
Proof: `uv run pytest tests/test_extract_tokens.py -k "test_a_shadow_root_with_no_style_is_no_author_style"`
**C9** - On `style-src.html`, `#late`, whose class changes 200ms after `load` to start a 10s `color` transition from `rgb(0, 0, 0)` to `rgb(119, 119, 119)`, gets exactly one `low-contrast-real` Finding: the stabilizing rules apply under the policy, so the transition takes no time (door 1)
Proof: `uv run pytest tests/test_style_src.py -k "test_a_transition_started_after_load_takes_no_time_under_the_policy"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| page scripts that add rules (3) | `stabilize.js` C9 · `fill_text.js` C1 · `covered_text.js` C2 | - |
| roots a rule is added to (2) | document C1 · open shadow root C3 | - |
| the page's own styles the Capture must not change (2) | its adopted sheets C6 · its inline style the policy refuses C5 | - |
| sheets `author_styles.js` leaves out, by root (2) | document C7 · open shadow root C8 | - |
| Checks reading text pixels on the page (2) | `low-contrast-real` C1 · `overlap` C2 | - |

- No check claims a route, status or response shape: the plan's `Surface` is `None`
- C4 is the only claim over the whole list of Findings; its proof compares both pages in one test

## Swept

- validation: n/a - no new input; the tools' arguments are unchanged
- failure modes: C1, C2 - the refused fill was a silent failure; under the policy the fill now applies
- idempotency: n/a - a Capture opens a fresh context on every call
- authorization: C5 - the page's own policy keeps refusing the page's inline style; the Capture does not lift it
- concurrency: n/a - page scripts run one after another in one page, as today
- data lifecycle: n/a - nothing is persisted
- dependency failure: n/a - no new dependency; `CSSStyleSheet` and `adoptedStyleSheets` ship with Chromium
- state transitions: C9 - a transition the page starts after load
- observability: n/a - no logging requirement; the outcome is in the Findings

## Handoff

- S1 = `wc -c` of the four page scripts (17 KB), the new test and fixtures (~5 KB), the fixture and test edited for C8 (~3 KB of 42 KB read in part) = ~25 KB / 4 = ~7k, under the 150k budget - one builder
