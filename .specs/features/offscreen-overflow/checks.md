# `offscreen-overflow` checks

Profile: light
Plan: `.specs/features/offscreen-overflow/plan.md`

23 checks in 4 slices · 2 one-way doors · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. Where `uv` is not on the path, `uv run <tool>` is `.venv/bin/<tool>`. Feature base: `9923762`.

Unless a check says otherwise, a page has no margin on `html` and `body`, is captured at 1440x900 and is called with `checks: ["offscreen-overflow"]`; "reported" means the Finding sits on that element, found by its box as `findings_on` does.

## Checks

### S1 - the element that makes the page scroll is named · 9 files · 40 KB · ~10k

**C1** - A page that holds an element of 1640px, called at 1440x900 and at 390x844, returns exactly two Findings, one per viewport in the order given, each with `check == "offscreen-overflow"`, `category == "responsive"`, `severity == "major"` and `source == "Squint heuristic"`, and with `overflowPx` 200 and 1250 (AC 1, door 1)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_that_scrolls_sideways_yields_one_finding_per_viewport" -v`

**C2** - On a page with two siblings of 1640px, `#first` before `#second`, the one Finding is on `#first` (AC 2, door 2)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_the_first_of_two_elements_on_the_edge_is_the_one_named" -v`

**C3** - The Finding on an element of 1640px (`display: block`, `position: static`, `white-space: normal`) carries `measured == {"overflowPx": 200, "pageWidth": 1640, "viewportWidth": 1440}`, `computed == {"display": "block", "position": "static", "width": "1640px", "white-space": "normal"}` and `message == "Extends 200px past the 1440px viewport, so the page scrolls horizontally"` (AC 3, door 1)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_the_finding_carries_the_widths_the_styles_and_the_message" -v`

**C4** - On a page where `#parent` of 1640px holds `#child` of the same width, the one Finding is on `#parent` (AC 4)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_parent_on_the_edge_is_named_instead_of_its_child" -v`

**C5** - On a page where `#parent` of 400px holds `#child` of 1640px, the one Finding is on `#child` (AC 5)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_child_past_a_parent_that_fits_is_the_one_named" -v`

**C6** - On a page where `#near` of 1639px stands before `#edge` of 1640px, the one Finding is on `#edge` (AC 6)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_1px_short_of_the_edge_is_not_named" -v`

**C7** - An element of 1639.6px alone on a page is reported, with `pageWidth == 1640` and `overflowPx == 200`: under 1px from the edge is on it (AC 2)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_under_1px_short_of_the_edge_is_named" -v`

**C8** - `#word`, 400px wide and holding one word of 100 Ahem glyphs at 20px, is reported with `box.w == 400` and `measured == {"overflowPx": 560, "pageWidth": 2000, "viewportWidth": 1440}` (AC 7, door 2)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_word_that_cannot_break_names_the_element_that_holds_it" -v`

**C9** - `#moved`, 200px wide and under `transform: translateX(1400px)`, is reported with `box.x == 1400`, `box.w == 200` and `overflowPx == 160` (AC 8)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_translated_element_is_reported_where_it_is_painted" -v`

**C10** - A page that holds an element of 400px, called at 399x300 and at 400x300, returns exactly one Finding, at 399x300, with `measured == {"overflowPx": 1, "pageWidth": 400, "viewportWidth": 399}` (AC 9)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_one_pixel_past_the_viewport_is_reported_and_none_is_not" -v`

**C11** - Each of seven pages as wide as the viewport returns no Finding: an element that sticks out to the left, one `position: fixed` past the right edge, one cut by an ancestor with `overflow: hidden`, one inside a container that scrolls, one that casts a shadow past the edge, one with a right margin past it, and a page taller than the viewport (AC 10)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_as_wide_as_the_viewport_is_not_reported" -v` runs 7 cases

**C12** - Each of four pages that hold an element of 1640px returns no Finding: `overflow-x: hidden` on `html`, `overflow-x: clip` on `html`, and each of the two on `body` with `html` left at `visible` (AC 11)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_that_hides_its_horizontal_overflow_is_not_reported" -v` runs 4 cases

**C13** - On a page with `overflow-x: auto` on `html` and a `body` of 1640px with `overflow-x: hidden`, `body` is reported with `overflowPx == 200`: the `overflow-x` of `body` counts only while that of `html` is `visible` (AC 11, AC 1)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_hidden_overflow_on_body_under_a_scrolling_html_is_reported" -v`

**C14** - A page with `direction: rtl` on `body` that holds an element of 1640px returns no Finding (AC 12)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_right_to_left_page_is_not_reported" -v`

**C15** - A page made 1640px wide by `body::after` alone, where no element reaches the right edge, returns no Finding (AC 13)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_widened_by_no_element_is_not_reported" -v`

### S2 - the Check is reachable through the tool · 3 files · 24 KB · ~6k

The page of C16 and C17 holds, in this order, a text cut by 4px (a `minor` `text-clipped` Finding) and an element of 1640px, black on white.

**C16** - `detect_visual_bugs` with `checks: ["offscreen-overflow"]` on that page returns exactly one Finding, whose `check` is `offscreen-overflow` (AC 14)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_naming_the_check_returns_its_finding_alone" -v`

**C17** - `detect_visual_bugs` with no `checks` on that page returns exactly two Findings, whose `check` are `["offscreen-overflow", "text-clipped"]` in that order and whose `evidence.cropIndex` are 0 and 1 (AC 15)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_omitting_checks_returns_the_finding_among_the_others" -v`

**C18** - An unknown name in `checks` is an error that holds `Valid checks: low-contrast-real, offscreen-overflow, text-clipped.` in each of the four existing tests that quote the list (AC 16)
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_is_an_error_listing_the_valid_ones" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_after_a_valid_one_is_still_an_error" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_the_first_unknown_check_in_the_order_given_is_the_one_named" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_is_reported_before_any_browser_work" -v`
Proof: `grep -c "Valid checks: low-contrast-real, offscreen-overflow, text-clipped\." tests/test_detect_visual_bugs.py` prints `1` or more
Proof: `grep -c "Valid checks: low-contrast-real, text-clipped\." tests/test_detect_visual_bugs.py` prints `0`

**C19** - The description of `detect_visual_bugs` holds `` `offscreen-overflow` `` and the word `scroll` (AC 17)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_the_tool_description_names_the_check_and_what_it_reports" -v`

**C20** - Every test that exists at `9923762` passes, and the only lines taken out of `tests/` are the four that quote the old list of valid Checks and the parentheses around them (AC 18)
Proof: `uv run pytest`
Proof: `git diff 9923762..HEAD -- tests | grep -c "^-.*Valid checks: low-contrast-real, text-clipped\."` prints `4`
Proof: `git diff 9923762..HEAD -- tests | grep "^-[^-]" | grep -Evc "Valid checks: low-contrast-real, text-clipped\.|^-    (assert \(|\))$"` prints `0`

### S3 - the record · 2 files · 7 KB · ~2k

**C21** - The `Added` part of `[Unreleased]` in `CHANGELOG.md`, above `## [0.1.0]`, has one entry that names `offscreen-overflow`, says `one element per viewport`, says `major` and says that nothing is reported while the page hides its horizontal overflow (AC 19)
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### /p' | grep "offscreen-overflow" | grep "one element per viewport" | grep "major" | grep -c "hides its horizontal overflow"` prints `1`

**C22** - The sentence of `README.md` that counts the Checks says `runs three Checks` and names `offscreen-overflow`, and `runs two Checks` is gone (AC 20)
Proof: `grep "runs three Checks" README.md | grep -c "offscreen-overflow"` prints `1`
Proof: `grep -c "runs two Checks" README.md` prints `0`

### S4 - gate

**C23** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| one-way doors (2) | door 1, the values C1 · door 2, the element named C2 | - |
| values of door 1 (7) | `check` C1 · `category` C1 · `severity` C1 · `source` C1 · `measured` C3 · `computed` C3 · `message` C3 | - |
| reach of an element (2) | right edge of its box C2 · right edge of its own text C8 | - |
| who is named among several (4) | first of two siblings C2 · parent over child C4 · child past a parent that fits C5 · the one on the edge after one 1px short C6 | - |
| distance to the page's edge (3) | 0px C3 · 0.4px C7 · 1px C6 | - |
| page against viewport (3) | 1px wider C10 · equal C10 · much wider, two viewports C1 | - |
| pages as wide as the viewport (7) | `left` C11 · `fixed` C11 · `hidden-ancestor` C11 · `scroll-container` C11 · `shadow` C11 · `margin` C11 · `taller` C11 | - |
| `overflow-x` of the viewport (5) | `html hidden` C12 · `html clip` C12 · `body hidden` C12 · `body clip` C12 · `body hidden` under `html auto` C13 | - |
| pages that are not reported for what they are (2) | `direction: rtl` C14 · no element on the edge C15 | - |
| `checks` argument (3) | the name alone C16 · omitted C17 · unknown C18 | - |
| assertions that quote the valid Checks (4) | `listing_the_valid_ones` C18 · `after_a_valid_one` C18 · `first_unknown_check` C18 · `before_any_browser_work` C18 | - |
| documents (2) | `CHANGELOG.md` C21 · `README.md` C22 | - |

- The plan's `Surface` and `Relations` are `None`: no route, status or entity owes a row. The one claim on an error shape is C18, and its proofs cross the tool boundary
- C11 and C12 are table-driven over their sets, sizes 7 and 4
- `Element.tag` (Flow, hop 1) has no check of its own: it is a means, and C12 to C14 fail without it. That `inspect_element` does not change (Impact) is C20, through the tests of its exact keys

## Swept

- validation: C18 - the one input that changes is the set of names `checks` accepts
- failure modes: C15 - a page wider than the viewport with no element to name yields nothing, not an error
- idempotency: existing - a Check is a function of the Capture and holds nothing: `tests/test_detect_visual_bugs.py::test_the_same_call_returns_the_same_structured_content`
- authorization: n/a - a local stdio server, no caller to tell apart
- concurrency: n/a - no new work off the event loop; one pass over the elements of a Capture
- data lifecycle: n/a - nothing is retained between calls
- dependency failure: n/a - no new dependency, no new page script and no new screenshot
- state transitions: n/a - the Check holds no state
- observability: n/a - no log requirement in this slice

## Handoff

- S1-S3 = 71 KB of reading, ~18k tokens, one surface (a new Check module, one field of the collector, the tool's description) - one builder
