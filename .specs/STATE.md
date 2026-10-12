# STATE

## Decisions

### AD-001
- **Decision**: The Chromium instance lives in a `BrowserSession` yielded by the MCP server lifespan and is read by tools from the request's lifespan context; it is never a module-level global.
- **Reason**: The lifespan gives a real shutdown path and binds the browser to the event loop that created it. Each in-memory test client gets its own lifespan, so tests share one browser through one session-scoped client and can reproduce "Chromium not installed" with a second client.
- **Trade-off**: Every tool that needs a browser must take the SDK `Context` parameter.
- **Scope**: `src/squint_mcp/capture.py`, every tool that produces a Capture, `tests/conftest.py`.
- **Date**: 2026-10-06
- **Status**: active

### AD-002
- **Decision**: A tool that returns images is annotated `Annotated[CallToolResult, <ResultModel>]` and builds its own result: a text summary, the images as MCP image content blocks, and camelCase structured content. Anticipated failures are raised as `ToolError` with a concrete message; nothing is returned as partial data.
- **Reason**: Image blocks are rendered by clients and are not billed as base64 text; the result model still publishes an output schema. One error channel keeps "the page is broken" apart from "the page is clean".
- **Trade-off**: The handler assembles content blocks by hand instead of returning a model.
- **Scope**: Every tool under `src/squint_mcp/tools/` that returns crops.
- **Date**: 2026-10-06
- **Status**: active

### AD-003
- **Decision**: A Capture taken for Checks holds every element of the page (open shadow trees included, in document order) with the same generic fields, among them a selector unique on the page. A Check is a function `Capture -> list[Finding]` in its own module under `src/squint_mcp/checks/`, registered by name in `checks/__init__.py`. Checks hold no page script; the tool, not the Check, orders Findings and allocates crops.
- **Reason**: ADR-0002 makes the Capture the whole contract between browser code and Checks. One generic collector lets a new Check ship as one Python module; selectors need the live DOM, which is gone by the time a Check runs.
- **Trade-off**: Every element is serialized on every `detect_visual_bugs` call, whatever the Checks need. A Check that needs a new fact about an element adds a field to the collector and to `Element`.
- **Scope**: `src/squint_mcp/js/collect_elements.js`, `src/squint_mcp/models.py`, `src/squint_mcp/checks/`, `src/squint_mcp/tools/detect_visual_bugs.py`.
- **Date**: 2026-10-06
- **Status**: active

### AD-004
- **Decision**: A Capture carries three pixel layers of the same size: `pixels` (the page as painted), `background` (the page with no text painted) and `ink` (how much text ink each pixel gets, 0 to 255). The two new ones come from screenshots taken with `-webkit-text-fill-color` forced on every element: transparent for `background`, black and white for `ink`, which is the difference of the two. A Check tells text from what is behind it through these layers, never by guessing from `pixels`.
- **Reason**: Anti-aliased edges, clipped text, covered text and text of the colour of its background all make "the pixels inside the text's box" wrong as a background. The fill property changes glyphs only; `color` would also repaint borders, underlines and shadows. Spiked against real Chromium for slice 4.
- **Trade-off**: Four screenshots per Capture instead of one, for every tool. Text whose fill cannot be forced has no ink.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/js/fill_text.js`, `src/squint_mcp/models.py`, every Check that reads text pixels.
- **Date**: 2026-10-08
- **Status**: active

### AD-005
- **Decision**: A Capture measures covered text only when asked (`capture(..., covered_text=True)`): for each element with own text that may be covered, `Element.covered_text` holds its Text ink, its Hidden ink and the Other elements that hit testing gives there. It is measured from screenshots in which the glyphs of chosen text nodes are repainted through CSS highlights, alone and as painted, and by hit testing with the page scrolled. A Check that reads it is listed in `COVERED_TEXT_CHECKS`.
- **Reason**: Only the pixels say how much of a text is hidden, and only the page can paint a text alone. Spiked for slice 8: the cost about doubles a Capture, which three of the four Checks and `inspect_element` would pay for nothing.
- **Trade-off**: A Capture is no longer one shape: a Check that needs covered text has to be declared, or it reads `None`. The rules of Silent and Raised layers live in a page script.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/covered.py`, `src/squint_mcp/js/covered_text.js`, `src/squint_mcp/models.py`, `src/squint_mcp/checks/__init__.py`, every Check that reads `covered_text`.
- **Date**: 2026-10-11
- **Status**: active

### AD-006
- **Decision**: Chromium is launched with `--disable-lcd-text`, and a Capture takes one small screenshot beyond the viewport before it measures anything.
- **Reason**: With subpixel text Chromium rasterizes the same glyph differently alone and as painted, and ink measured in two renders cannot be compared. The first screenshot beyond the viewport changes the layout of some pages on Windows (issue #18); taken first, boxes and pixels are of one layout.
- **Trade-off**: The pixels of a Capture are not those of a Windows screen with ClearType. About 0.09s more per Capture.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/config.py`, every tool.
- **Date**: 2026-10-11
- **Status**: active

### AD-007
- **Decision**: A Capture lets the page paint two animation frames before every screenshot it takes.
- **Reason**: On a page with several layers of its own, a screenshot taken right after a change of style now and then shows a band of the page beyond the viewport not painted. Ink read there is zero: a covered text at the foot of `overlap-low.html` got no Finding on about six calls in ten. With the two frames no miss was measured in 60 calls, and no screenshot differed from one taken again at once. Tried and dropped: every screenshot taken twice (right, at twice the cost), `--run-all-compositor-stages-before-draw` (7 misses in 10), a small screenshot taken first (20 misses in 20).
- **Trade-off**: An eighth to a fifth more time per Capture, for every tool (165s to 187s on 71 tests; the whole suite from 14:00 to 17:13, 18s of that a new test). A page on which animation frames never come would hang until the total timeout; none is known.
- **Scope**: `src/squint_mcp/capture.py`, every tool.
- **Date**: 2026-10-11
- **Status**: active. Taken by the agent in the third fix round of slice 8 with the maintainer away: the maintainer confirms it or reverts its commit.

## Handoff

- **Feature**: `overlap` (roadmap slice 8) / `.specs/features/overlap/`
- **Phase / Task**: Execute, under `tlc-spec-driven`, scope Complex. T1 to T13 and the fixes F1 to F17 are done and committed. The fourth validation pass is FAIL and the fix loop is at its bound of three rounds: nothing more is done until the maintainer decides.
- **Completed**: T1 to T13 (`89385b0` to `cb8d81b`), three validation passes and their fix rounds F1 to F8 (`aef0799` to `a11b13e`), the third pass (`26d084f`), the third fix round F9 to F17 (`82bbaed` to `a8feee6`: F9 `82bbaed`, F10 `c018ab2`, F11 `b71e582`, F12 `ecdf0e5`, F17 `51ff006`, F13 `3711dee`, F14 `e4fed09`, F15 `70f926d`, F16 `a8feee6`), the fourth pass (`ad6c911`, FAIL on nine surviving mutants). The gate passes: 359 tests in about 17.5 minutes, pyright and ruff clean. The spec has 120 criteria.
- **In-progress** (file:line): none.
- **Next step**: the maintainer decides three things, from the "Fix Plans" and "Next steps" of `validation.md`. (1) AD-007 (`51ff006`), taken by the agent without the maintainer: confirm or revert. The Verifier measured the fault as real (20 misses in 30 calls without the wait) and recommends keeping it, and found that the wait has no bound: a page that replaces `requestAnimationFrame` by a function that never calls back now fails every tool with `Timed out after 30s.` (`src/squint_mcp/capture.py`, `_PAINTED`); a timer raced against the frames inside the same `evaluate` bounds it, one frame may be enough, and `spec.md:55` still counts two changes that reach every Capture. (2) The nine surviving mutants (Fix 1 to 5): accept the feature with that residual, or have about nine fixture rows written with no change to `src/`: a `filter` with a list of functions, `blur()` and `drop-shadow()`, `!important`, a descendant deeper than a child, the Coverer first in the document, a border in the glyphs-only screenshot, exactly 20,000 pixels. (3) The stopping rule: four passes of fresh mutants left 11, 11, 12 and 9 alive, and the spec's third success criterion asks for none. Then Fix 7, a row in Out of Scope for a right-to-left page that scrolls sideways. On an accepted PASS: the closing step of `tasks.md` (roadmap, the spike and its `extend-exclude` removed, issue #18 through the pull request).
- **Blockers**: the three decisions above.
- **Uncommitted files**: none.
- **Branch**: `feat/overlap`, local only, from `origin/main` at `8aa017c`. Not pushed; no pull request. It has never run on the CI's Linux: the timing of AD-007 and the system font of `overlap-font.html` are untested there.
- **Spike**: in `.specs/features/overlap/spike/` until the slice closes.
- **Found outside this slice**: under a Content Security Policy that refuses inline styles (`style-src file:`), a page with a covered text and a low-contrast text returns `No findings`: the styles a Capture injects are refused, for every Check (`design.md` names `bypass_csp` to try). On a right-to-left page that scrolls sideways every tool reads the wrong pixels. Neither has an issue yet.
- **Notes for the next session**: the suite does not fit a 10-minute foreground timeout, run it in the background. The working tree mixes line endings (`spec.md`, `tasks.md`, `STATE.md`, most of `src/` CRLF; `tests/test_overlap.py`, the overlap fixtures, `checks/overlap.py`, `validation.md` LF): keep each file as it is, and check with a byte count, since `grep -c $'\r$'` counts every line in Git Bash. A heredoc with an odd number of single quotes fails in the shell wrapper: write scripts to files. `validate_tasks.py` only parses ids of the form `T<n>`. Sub-agents cannot write `.md` files with the Write tool. To run tests against a mutant without touching the tree, copy `src/squint_mcp` to a temp directory, mutate the copy and run pytest with `PYTHONPATH` set to it. A mutant on `overlap-clean.html` or any page of many layers is judged on several runs: the fault AD-007 fixes made such results change from one call to the next.
