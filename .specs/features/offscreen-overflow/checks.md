# `offscreen-overflow` checks

Profile: light
Plan: `.specs/features/offscreen-overflow/plan.md`

21 checks in 4 slices · 2 one-way doors · 0 open

The proofs are the commands of `.github/workflows/ci.yml`. Where `uv` is not on the path, `uv run <tool>` is `.venv/bin/<tool>`. Feature base: `9923762`.

Every fixture is `tests/fixtures/offscreen-overflow-<name>.html`, named below by `<name>`. The widths were measured against Chromium on `a5013d4` before these checks were written: the pages of C3 to C8 and C11 to C13 are captured at 400x300, and each of them is wider than that in the full-page `pixels`.

## Checks

### S1 - the element that makes the page scroll is named · 10 files · 53 KB · ~13k

**C1** - `detect_visual_bugs` with `checks: ["offscreen-overflow"]` on `bug` at 1440x900 (a `#wide` of 1640px) returns exactly one Finding, on `#wide`, with `check == "offscreen-overflow"`, `category == "responsive"`, `severity == "major"` and `source == "Squint heuristic"` (AC 1, door 1)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_wider_than_its_viewport_yields_one_finding" -v`

**C2** - That Finding carries `measured == {"overflowPx": 200, "pageWidth": 1640, "viewportWidth": 1440}`, `computed == {"display": "block", "position": "static", "width": "1640px", "white-space": "normal"}` and the message `Extends 200px past the 1440px viewport, so the page scrolls horizontally` (AC 3, door 1)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_the_finding_carries_the_widths_and_the_styles_that_explain_it" -v`

**C3** - On `nested` (`#outer` of 600px holding `#inner`, which ends at the same edge) the one Finding is on `#outer` (AC 2, AC 4, door 2)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_at_the_edge_is_named_instead_of_its_child_at_the_same_edge" -v`

**C4** - On `child` (`#parent` of 300px holding `#child` of 600px) the one Finding is on `#child` (AC 5)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_child_at_the_edge_is_named_instead_of_its_parent_that_fits" -v`

**C5** - On `near` (`#near` of 599px before `#edge` of 600px) the one Finding is on `#edge` (AC 2, AC 6)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_one_pixel_short_of_the_edge_is_not_the_one_named" -v`

**C6** - An element under 1px from the page's right edge is named, on either side of it: `#fraction` of `fraction-short` (600.6px on a page of 601px) with `overflowPx == 201`, and `#fraction` of `fraction-past` (600.4px on a page of 600px) with `overflowPx == 200` (AC 2)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_under_a_pixel_from_the_edge_is_named" -v` runs 2 cases

**C7** - On `word` (`#word`, a box of 200px whose one word of 30 Ahem glyphs at 20px ends at 600px) the one Finding is on `#word`, with a `box` 200px wide and `overflowPx == 200` (AC 2, AC 7)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_word_that_cannot_break_names_the_element_whose_text_it_is" -v`

**C8** - On `moved` (`#moved`, 100x20 under `translateX(450px)`) the one Finding has `box == {"x": 450, "y": 0, "w": 100, "h": 20}` and `overflowPx == 150` (AC 8)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_moved_by_a_transform_is_reported_where_it_is_painted" -v`

**C9** - One call on `one` (`#box` of 400px) at 399x300 and at 400x300 returns exactly one Finding, at the viewport of 399, with `measured == {"overflowPx": 1, "pageWidth": 400, "viewportWidth": 399}` (AC 9)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_one_pixel_past_the_viewport_is_reported_and_none_is_not" -v`

**C10** - `detect_visual_bugs` on `clean` at 1440x900 returns no Finding. The page is 1440px wide and holds an element 200px out to the left, one `position: fixed` that ends at 1640px, one of 1640px inside `overflow: hidden`, one of 1640px inside `overflow-x: auto`, a shadow 200px past the right edge, a right margin 200px past it, and an element 2000px tall (AC 10)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_as_wide_as_its_viewport_yields_no_finding" -v`

**C11** - A page of 600px in `pixels` whose `#wide` ends at its right edge yields no Finding when `overflow-x` is `hidden` or `clip` on `html`, or on `body` with `html` left `visible`: `hidden-html`, `clip-html`, `hidden-body`, `clip-body` (AC 11)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_that_hides_its_horizontal_overflow_yields_no_finding" -v` runs 4 cases

**C12** - On `rtl` (`direction: rtl` on `body`, a page of 600px in `pixels`, and a `#pinned` that ends at 600px) there is no Finding (AC 12)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_right_to_left_page_yields_no_finding" -v`

**C13** - On `pseudo` (a `#host::after` of 600px, no element past 400px) there is no Finding (AC 13)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_widened_by_a_pseudo_element_yields_no_finding" -v`

### S2 - the Check is reachable through the tool · 2 files · 24 KB · ~6k

**C14** - `detect_visual_bugs` with `checks: ["offscreen-overflow"]` on `bug`, which also holds the clipped text `#clipped`, returns `[("#wide", "offscreen-overflow")]` and no `text-clipped` Finding (AC 14)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_naming_the_check_returns_its_finding_alone" -v`

**C15** - `detect_visual_bugs` with no `checks` on `bug` returns `[("#wide", "offscreen-overflow"), ("#clipped", "text-clipped")]`, both `major`, in that order (AC 15)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_omitting_checks_returns_the_findings_of_every_check" -v`

**C16** - The error for an unknown name in `checks` holds `Valid checks: low-contrast-real, offscreen-overflow, text-clipped.` in each of the four tests that quote the list (AC 16)
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_is_an_error_listing_the_valid_ones" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_after_a_valid_one_is_still_an_error" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_the_first_unknown_check_in_the_order_given_is_the_one_named" -v`
Proof: `uv run pytest "tests/test_detect_visual_bugs.py::test_unknown_check_is_reported_before_any_browser_work" -v`
Proof: `grep -c "Valid checks: low-contrast-real, offscreen-overflow, text-clipped\." tests/test_detect_visual_bugs.py` prints `4`

**C17** - The description of `detect_visual_bugs`, its whitespace collapsed, holds `` `offscreen-overflow` (the element that sets the width of a page that scrolls horizontally `` (AC 17)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_the_tool_description_says_what_offscreen_overflow_reports" -v`

**C18** - The test files that exist at `9923762` lose exactly four lines, the four assertions of C16, and the output of `inspect_element` keeps its six keys with `Element` carrying `tag` (AC 18, Impact: Capture)
Proof: `git diff 9923762..HEAD -- tests/conftest.py tests/helpers.py tests/test_detect_visual_bugs.py tests/test_inspect_element.py tests/test_low_contrast_real.py tests/test_ping.py tests/test_selectors.py tests/test_text_clipped.py tests/test_vision.py | grep -c "^-[^-]"` prints `4`
Proof: `uv run pytest "tests/test_inspect_element.py::test_structured_content_has_exactly_the_documented_keys" -v`

### S3 - the record · 2 files · 7 KB · ~2k

**C19** - `CHANGELOG.md` has, under `[Unreleased]` and above `## [0.1.0]`, an `### Added` section whose `offscreen-overflow` entry says `one per viewport`, `` `major` `` and `hides its horizontal overflow` (AC 19)
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### Changed/p' | grep "offscreen-overflow" | grep -c "one per viewport"` prints `1`
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### Changed/p' | grep "offscreen-overflow" | grep -c '`major`'` prints `1`
Proof: `sed -n '/^## \[Unreleased\]/,/^## \[0.1.0\]/p' CHANGELOG.md | sed -n '/^### Added/,/^### Changed/p' | grep "offscreen-overflow" | grep -c "hides its horizontal overflow"` prints `1`

**C20** - The sentence of `README.md` that names the Checks reads `runs three Checks` and names `offscreen-overflow` (AC 20)
Proof: `grep "runs three Checks" README.md | grep -c '`offscreen-overflow`'` prints `1`
Proof: `grep -c "runs two Checks" README.md` prints `0`

### S4 - gate

**C21** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| one-way doors (2) | door 1, the values of the Finding C1 · door 2, which element is named C3 | - |
| door 1, the values (6) | `check` C1 · `category` C1 · `severity` C1 · `source` C1 · `evidence.measured` C2 · `evidence.computed` C2 | - |
| the reach of an element (2) | the right edge of its box C3 · the right edge of its own text C7 | - |
| distance to the page's edge (4) | 0px C2 · under 1px, short of it C6 · under 1px, past it C6 · 1px C5 | - |
| elements at the same edge (2) | an ancestor and its child C3 · a child alone, its parent fitting C4 | - |
| the page against the viewport (2) | 1px wider C9 · as wide C9 | - |
| near misses of AC 10 (7) | out to the left C10 · `position: fixed` past the right edge C10 · cut by `overflow: hidden` C10 · inside a container that scrolls C10 · a shadow past the edge C10 · a right margin past it C10 · taller than the viewport C10 | - |
| `overflow-x` of the viewport (4) | `hidden` on `html` C11 · `clip` on `html` C11 · `hidden` on `body` C11 · `clip` on `body` C11 | - |
| the `checks` argument (3) | the new name alone C14 · omitted C15 · an unknown name C16 | - |
| assertions that quote the valid Checks (4) | `..._is_an_error_listing_the_valid_ones` C16 · `..._after_a_valid_one_is_still_an_error` C16 · `the_first_unknown_check_...` C16 · `..._before_any_browser_work` C16 | - |

- Claims naming an error text or a response shape: C1, C2, C14, C15, C16 - each proof calls the tool through the MCP client
- C6 and C11 are table-driven over their sets, sizes 2 and 4; C10 is one page, so any of its seven members that made the page scroll, or got named, fails it
- No other check claims more than the single case its proof exercises

## Swept

- validation: C16 - the one input the change touches is the list of names `checks` accepts
- failure modes: C13 - a page wider than its viewport with no element at its edge yields nothing instead of a wrong element; an element with no box has a reach of 0 and is never at the edge
- idempotency: n/a - the Check is a function of the Capture and holds no state; `tests/test_detect_visual_bugs.py::test_the_same_call_returns_the_same_structured_content` covers the tool
- authorization: n/a - a local stdio server, no caller to tell apart
- concurrency: n/a - one pass over the elements of a Capture, with nothing shared between calls
- data lifecycle: n/a - nothing is retained between calls
- dependency failure: n/a - no new dependency; the Check reads the Capture only (ADR-0002)
- state transitions: n/a - no state
- observability: n/a - no log requirement; the Finding is the output

## Handoff

- S1-S3 = 84 KB of reading, ~21k tokens, one surface (a Check module, the collector field it needs and the tool that lists it), under the 150k budget - one builder
- **Boundary:** C1-C21 closed at `2bd6d5d`
- **Settled mid-build:** nothing - the user gave no clarification during the build
- **Abandoned:** nothing
