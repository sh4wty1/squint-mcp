# PR #17 review fixes

Profile: light (none declared in `AGENTS.md`).

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/17#pullrequestreview-5477643823 - findings F1 to F4, with the repro and the fix each one asks for
- `.specs/features/offscreen-overflow/plan.md` and `checks.md` - the approved criteria and checks of the slice, which these fixes must leave true: AC 18 and its check C18 keep the test files that exist at `9923762` to four removed lines
- conversation - local commits only; `git push` waits for the user

Measured against Chromium at `b987904` before these checks were written, at 400x300: on the repro of F1 (`html { overflow-y: scroll }`, `body { overflow-x: hidden }`, a child of 600px) the full-page pixels are 600px wide, the `scrollWidth` of `html` is 400 and `scrollTo(100000, 0)` leaves `scrollX` at 0. On a page with no doctype and a child of 600px the `scrollWidth` of `html` is 600 and the page scrolls by 200px.

After round 1 of the verification (`.checks/pr17-review-fixes.verified.md`, gap 1) the same measurement was repeated on a page with no doctype whose overflow comes from an out-of-flow element (`position: absolute`, from 500px to 600px): the page scrolls by 200px, the `scrollWidth` of `html` is 400 and that of `body`, which is `document.scrollingElement` there, is 600. With a doctype the two swap. On 2026-10-10 the user chose to read the width from the element that scrolls the viewport, and to leave F3 in part. C5 was rewritten for that and C11 added; C1 to C4 and C6 to C10 are as verified.

## Out of scope

- The three older copies of the crop decode (`tests/test_inspect_element.py:82`, `tests/test_detect_visual_bugs.py:212` and `:298`) - F3 asks for one helper to serve the four, and replacing those three removes lines from test files that AC 18 of the approved plan freezes. The helper lands and the new module uses it; the other three stay as a follow-up, by the user's decision of 2026-10-10
- A page in quirks mode whose `body` is its own scroll container and whose overflow comes from an out-of-flow element - no element scrolls the viewport there (`document.scrollingElement` is null) and no width the browser reports holds the overflow; the code before this pull request did not report it either
- The fix of F2 - the review asks only for the limit to be labelled
- Precision gaps 1a, 2 and 3 of `verification.md` - disclosed in the PR and not raised by the review
- Any check of `.specs/features/offscreen-overflow/checks.md` (C1 to C21) - none is edited; all stay green
- `git push` - waits for the user

## Landing

Touches `src/squint_mcp/checks/offscreen_overflow.py` (where the width of the page comes from, and one comment), `src/squint_mcp/capture.py` and `src/squint_mcp/models.py` (the Capture gains the width the page scrolls, read by a new one-line page script in `src/squint_mcp/js/`), four new fixtures, `tests/test_offscreen_overflow.py`, `tests/helpers.py`, the `Flow` and `Impact` of the slice's plan, `.specs/STATE.md` and the task record.

`None - no stored shape, tool, field or error changes; `pageWidth` keeps its name and now holds the width the page scrolls, which is what its 21 checks already assert. The new field of the Capture is internal: no tool returns it`

- Nothing in this change is hard to reverse

## Checks

### S1 - A page that does not scroll gets no Finding (F1) · 8 files · 30 KB · ~8k

**C1** - On `own-scroller` at 400x300 (`html` with `overflow-y: scroll`, `body` with `overflow-x: hidden`, a `#wide` of 480px) there is no Finding, and the pixels of the page end at 480px, past the viewport: the crop of `#wide` is 480px wide
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_body_that_clips_its_own_overflow_yields_no_finding" -v`

**C2** - On `body-under-html` (a `body` of 600px that hides its overflow, under an `html` that scrolls) the one Finding is still on `body`
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named" -v`

**C3** - On `quirks` at 400x300 (no doctype, a `#wide` of 600px) the one Finding is on `#wide`, with `measured == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_in_quirks_mode_is_measured_like_any_other" -v`

**C4** - The Check takes no width from the pixels of the Capture
Proof: `grep -c "pixels.width" src/squint_mcp/checks/offscreen_overflow.py` prints `0`

**C5** - The `Flow` of the slice's plan says the width of the page is the scroll width of the element that scrolls the viewport, and no longer that the Check reads it from the pixels
Proof: `grep -c "element that scrolls the viewport" .specs/features/offscreen-overflow/plan.md` prints `1` or more
Proof: `grep -c "so the Check reads the page's width from them" .specs/features/offscreen-overflow/plan.md` prints `0`

**C11** - An element out of the flow that ends at 600px (`#out`, `position: absolute`, from 500px) on a page captured at 400x300 gets the one Finding, with `measured == {"overflowPx": 200, "pageWidth": 600, "viewportWidth": 400}`, with a doctype (`absolute`) and without one (`quirks-absolute`)
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_an_element_out_of_the_flow_is_named_with_or_without_a_doctype" -v` runs 2 cases

### S2 - The limit is labelled (F2) · 1 file · 3 KB · ~1k

**C6** - The `ponytail` note of `check` says that a line ending in an inline child names that child
Proof: `grep -c "inline child" src/squint_mcp/checks/offscreen_overflow.py` prints `1`

### S3 - One decode for the new module (F3) · 2 files · 10 KB · ~3k

**C7** - `tests/helpers.py` holds the one decode of a tool image, and `tests/test_offscreen_overflow.py` uses it instead of its own
Proof: `grep -c "b64decode" tests/helpers.py` prints `1`
Proof: `grep -c "b64decode" tests/test_offscreen_overflow.py` prints `0`
Proof: `uv run pytest "tests/test_offscreen_overflow.py::test_a_page_as_wide_as_its_viewport_yields_no_finding" -v`

### S4 - The records (F4) · 2 files · 8 KB · ~2k

**C8** - The Handoff of `.specs/STATE.md` names slice 8 (`overlap`, `tlc-spec-driven`) as the next step and no longer says the commits are local or that the pull request is still to be opened
Proof: `grep -c "Next step.*slice.* 8 (.overlap., .tlc-spec-driven.)" .specs/STATE.md` prints `1`
Proof: `grep -c "every later commit is local\|push and open the pull request" .specs/STATE.md` prints `0`

**C9** - `docs/tasks/2026-10-09-offscreen-overflow.md` records the review of PR #17 and no longer lists the push and the pull request as pending
Proof: `grep -c "pull/17" docs/tasks/2026-10-09-offscreen-overflow.md` prints `1` or more
Proof: `grep -c "push e pull request, quando o mantenedor autorizar" docs/tasks/2026-10-09-offscreen-overflow.md` prints `0`

### S5 - Gate

**C10** - Type check, lint, format and the whole suite are green, and the test files that exist at `9923762` still lose exactly four lines (C18 of the slice)
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`
Proof: `git diff 9923762..HEAD -- tests/conftest.py tests/helpers.py tests/test_detect_visual_bugs.py tests/test_inspect_element.py tests/test_low_contrast_real.py tests/test_ping.py tests/test_selectors.py tests/test_text_clipped.py tests/test_vision.py | grep -c "^-[^-]"` prints `4`

## Swept

- validation: not in scope - no input changes
- failure modes: C1 - a width the page cannot scroll to yields nothing; a document with no `html` element yields nothing instead of an error (no proof: a Capture of such a document is not reachable from a fixture today)
- idempotency: not in scope - the Check is a function of the Capture
- authorization: not in scope
- concurrency: not in scope
- data lifecycle: not in scope - nothing is retained
- dependency failure: not in scope - no new dependency
- state transitions: not in scope
- observability: not in scope - no log requirement

## Handoff

S1-S4 = ~14k of reading, one surface. One agent, no handoff.
