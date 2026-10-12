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
- **Decision**: A Capture lets the page paint two animation frames before every screenshot it takes, and waits for them 250ms at most.
- **Reason**: On a page with several layers of its own, a screenshot taken right after a change of style now and then shows a band of the page beyond the viewport not painted. Ink read there is zero: a covered text at the foot of `overlap-low.html` got no Finding on about six calls in ten. With the two frames no miss was measured in 60 calls, and no screenshot differed from one taken again at once. Tried and dropped: every screenshot taken twice (right, at twice the cost), `--run-all-compositor-stages-before-draw` (7 misses in 10), a small screenshot taken first (20 misses in 20).
- **Trade-off**: An eighth to a fifth more time per Capture, for every tool (165s to 187s on 71 tests; the whole suite from 14:00 to 17:13, 18s of that a new test). The frames are asked of the page's own world: a page that puts a function that never calls back where `requestAnimationFrame` is failed every tool with the total timeout until the wait was given its bound (`PAINT_WAIT_MAX_S`), and is now captured after 250ms per screenshot, about 2s more on a page of one covered text. The two frames take about 30ms, and 90ms at most were measured. The timer is of the page's own world too: a page that replaces `setTimeout` as well still fails with the total timeout, until the wait is bounded from the server's side. The rate of the fault moves with the machine and the day: the fifth validation pass measured 7 misses in 30 calls without the wait, where the fourth had 20 in 30.
- **Scope**: `src/squint_mcp/capture.py`, every tool.
- **Date**: 2026-10-11
- **Status**: active. Taken by the agent in the third fix round of slice 8 with the maintainer away; confirmed by the maintainer on 2026-10-12, who had the wait bounded.

## Handoff

- **Feature**: `overlap` (roadmap slice 8) / `.specs/features/overlap/`
- **Phase / Task**: Execute, under `tlc-spec-driven`, scope Complex: closed. The fifth validation pass is a PASS and the branch is pushed (2026-10-12, on the maintainer's word). What is left of the closing step is the pull request, which closes issue #18: opening it waits for the maintainer's go-ahead.
- **Completed**: T1 to T13 and the fixes F1 to F17 (`89385b0` to `a8feee6`), four validation passes (the fourth, `ad6c911`, FAIL on nine surviving mutants). The maintainer's three decisions of 2026-10-12: AD-007 stays with a bound on its wait, the Fix 1 to 5 of the fourth report are written, and a PASS asks that the named mutants die. The fourth fix round F18 to F24 (F18 `bd77a0c`, F19 `081e6a1`, F20 `9f58aab`, F21 `a58e816`, F22 `f99e424`, F23 `788732c`, F24 `c14cd2f`). The fifth pass (`de3e1e4`, PASS: 131 of 131 criteria due, 9 of 9 survivors killed, gate green with 368 tests in about 22 minutes). After it: the wording of the bound (`b364efc`), the spike and its `extend-exclude` removed (`0b9af3a`), the roadmap and OVL-67 (`c00b172`). The spec has 132 criteria.
- **In-progress** (file:line): none.
- **Next step**: with the maintainer's go-ahead, open the pull request of `feat/overlap` with `Closes #18`; read the first run on the CI's Linux, where the branch has never run (the timing of AD-007 and the system font of `overlap-font.html` are untested there). Then the next roadmap slice: 9, `font-fallback`, under `tlc-spec-driven`.
- **Blockers**: the go-ahead for the pull request.
- **Uncommitted files**: none.
- **Branch**: `feat/overlap`, from `origin/main` at `8aa017c`, pushed to `origin/feat/overlap`. No pull request yet.
- **Residuals of the fifth pass** (`validation.md`, "Residuals and proposed issues"; none has an issue yet, and opening one is the maintainer's call): (1) the test of OVL-120 fails on a minority of runs with the wait taken out (3 of 10): it is a tripwire, and twelve calls would hold the wait on most runs. (2) The bound of the wait is a timer of the page's own world: a page that replaces `setTimeout` as well as `requestAnimationFrame` still fails every tool with `Timed out after 30s.`; a timeout around the `evaluate` of `_screenshot` (`src/squint_mcp/capture.py`), on the server's side, would end it. (3) A timer of 0ms did as well as two frames in 78 calls: whether a frame is needed is not shown. (4) `PAINT_WAIT_MAX_S` is held by its comment, not by a test. (5) No fixture holds 20,001 pixels of Hidden ink.
- **Found outside this slice**: under a Content Security Policy that refuses inline styles (`style-src file:`), a page with a covered text and a low-contrast text returns `No findings`: the styles a Capture injects are refused, for every Check (`design.md` names `bypass_csp` to try). On a right-to-left page that scrolls sideways every tool reads the wrong pixels. Both are rows of Out of Scope of the spec; neither has an issue yet.
- **Notes for the next session**: the suite takes 18 to 23 minutes and does not fit a 10-minute foreground timeout, run it in the background. The working tree mixes line endings (`spec.md`, `tasks.md`, `STATE.md`, `docs/ROADMAP.md`, `pyproject.toml`, most of `src/` CRLF; `tests/test_overlap.py`, the overlap fixtures, `checks/overlap.py`, `validation.md` LF): keep each file as it is, and check with a byte count, since `grep -c $'\r$'` counts every line in Git Bash. A heredoc with an odd number of single quotes fails in the shell wrapper: write scripts to files. `validate_tasks.py` only parses ids of the form `T<n>`. Sub-agents cannot write `.md` files with the Write tool. To run tests against a mutant without touching the tree, copy `src/squint_mcp` to a temp directory, mutate the copy and run pytest with `PYTHONPATH` set to it. To commit tasks one by one after one gate on all of them, record each task's files as blobs when it is done (`git hash-object -w --path`) and stage them with `git update-index --cacheinfo` in order. A mutant on a page of many layers is judged on several runs: the fault AD-007 fixes changes such results from one call to the next.
