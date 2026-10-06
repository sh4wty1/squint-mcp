# PR #3 review fixes

Sources:

- https://github.com/sh4wty1/squint-mcp/pull/3#pullrequestreview-5432395853 - the four should-fix findings (F1 to F4), with the repro and the fix each one asks for
- conversation - one commit per finding, test-first, F1 and F2 through the MCP boundary, push without merging

## Out of scope

- The three Codex comments on the same PR (deadline during pixel processing, transformed box model, crop clamp) - only the Judge's F1 to F4 were asked for; the crop clamp one is the same defect as F1
- Closed shadow roots - `element.shadowRoot` is `null` for them, nothing can reach in
- A friendlier error when the relaunch itself fails - the existing `Could not launch Chromium` message already covers it
- Replying to the review comments, merging - round 2 of the Judge checks the resolution

## Landing

Touches `vision._region`, `js/stabilize.js`, and two lines of `capture.py` (`BrowserSession.browser`, the `finally` of `capture`). Tests reuse the `client` and `local_server` fixtures, the `/hang` route and the `inspect`/`error_text` helpers; new elements go into the existing `box.html` and `motion.html`.

None - four local fixes, no schema, contract or dependency changes. `anyio` in the F3 test is already installed through `mcp` and already drives the suite (`pytest.mark.anyio`).

- Nothing else in this change is hard to reverse

Test reach: F3 and F4 cannot be observed through the MCP boundary alone - no tool reports open contexts, and no tool kills Chromium. The minimal reach is a spy on `BrowserSession.browser` that records the `Browser` it hands out; the test then reads `browser.contexts` (F3) or calls `browser.close()` (F4). Every call and every functional assertion still crosses the boundary.

## Checks

### S1 - Element outside the page origin (F1) · 3 files · 19 KB · ~5k

**C1** - `inspect_element` on an element entirely left of the page origin (`left: -9999px`) is a tool error containing `Selector "#left-of-page" matched an element with no rendered box.`
Proof: `uv run pytest "tests/test_inspect_element.py::test_element_outside_the_page_origin_has_no_rendered_box" -v`

**C2** - The same for an element entirely above the page origin (`top: -9999px`), with `#above-page` in the message
Proof: `uv run pytest "tests/test_inspect_element.py::test_element_outside_the_page_origin_has_no_rendered_box" -v`

### S2 - Motion inside open shadow trees (F2) · 4 files · 17 KB · ~4k

**C3** - An opacity 0 to 1 animation of 100s already running inside an open shadow root reports `computed.opacity == "1"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_animations_inside_an_open_shadow_root_are_taken_to_their_end" -v`

**C4** - An opacity 0 to 1 transition of 100s inside an open shadow root that starts 300ms after `load` (after stabilization ran) reports `computed.opacity == "1"`
Proof: `uv run pytest "tests/test_inspect_element.py::test_transitions_starting_later_inside_an_open_shadow_root_take_no_time" -v`

**C5** - The comment in `stabilize.js` and the "Zeroing animations" row of `design.md` no longer say `document.getAnimations()` reaches shadow trees
Proof: `grep -n -E "also reaches open shadow trees|covers shadow trees" src/squint_mcp/js/stabilize.js .specs/features/capture-inspect-element/design.md` exits 1 (no hit)

### S3 - Browser lifecycle (F3, F4) · 3 files · 21 KB · ~5k

**C6** - After the client cancels a call to a URL that never answers (1.5s in), the browser has 0 open contexts within 3s
Proof: `uv run pytest "tests/test_inspect_element.py::test_call_cancelled_by_the_client_leaves_no_browser_context_open" -v`

**C7** - After the cached Chromium is closed, the next `inspect_element` call succeeds (`isError: false`, `box.w == 120` for `#solid`)
Proof: `uv run pytest "tests/test_inspect_element.py::test_call_after_the_browser_died_relaunches_it" -v`

### S4 - Gate

**C8** - Type check, lint, format and the whole suite are green
Proof: `uv run pyright`
Proof: `uv run ruff check`
Proof: `uv run ruff format --check`
Proof: `uv run pytest`

## Swept

- validation: not in scope - no input surface changes
- failure modes: C1, C2 (inverted crop box), C7 (dead browser)
- idempotency: not in scope - the tool is read-only
- authorization: not in scope
- concurrency: C7 - the liveness test sits inside the existing `self._lock`, so two calls after a death still launch once (existing lock, `capture.py:34`)
- data lifecycle: C6 - a cancelled call's context is closed
- dependency failure: C7; a relaunch that fails keeps the existing `Could not launch Chromium` error (`capture.py:41-45`)
- state transitions: C7 - connected -> dead -> relaunched
- observability: not in scope - no log requirement

## Handoff

S1-S4 = ~14k of reading (the test file is shared), one surface. One agent, no handoff.
