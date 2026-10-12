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

### AD-008
- **Decision**: A Capture reads the fonts of a page only when asked (`capture(..., fonts=True)`): `Capture.faces` holds every face of `document.fonts` with its status, and `Element.line_widths` the width of the own text of an element set on one line, in its `font-family` and in that list without its first name. The widths are read from copies of the text put outside the flow, never by changing a style of the page, and only for elements whose first family has a face of `error`. A Check that reads them is listed in `FONT_CHECKS`.
- **Reason**: Only the page can lay a text out in another list of fonts, and the box of a text on the page is not its width: a justified paragraph is as wide in any font. Copies cost one layout for the whole page (133 to 165ms for 1,000 elements, spiked for slice 9 on Windows and on Linux) where changing each element costs one each. Measuring only where a face failed leaves a page whose fonts loaded untouched.
- **Trade-off**: A second fact a Capture holds only on request, after covered text (AD-005). Which elements are measured is decided in a page script, though the whole rule is applied again in the Check. A copy in the rest of the list can ask for a font no text had used: one request the page had not made.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/js/font_widths.js`, `src/squint_mcp/models.py`, `src/squint_mcp/checks/__init__.py`, every Check that reads `faces` or `line_widths`.
- **Date**: 2026-10-12
- **Status**: active. Written with the design of slice 9; confirmed by the maintainer on 2026-10-12.

## Handoff

- **Feature**: `font-fallback` (roadmap slice 9) / `.specs/features/font-fallback/`
- **Phase / Task**: Tasks, under `tlc-spec-driven`, scope Large: `tasks.md` is written (T1 to T12, five phases) and committed. The maintainer read it on 2026-10-12, accepted the three criteria it asked for (FNT-52 to FNT-54) and had it committed. Execute has not started.
- **Completed**: Slice 8 is closed: pull request #19 is merged into `main` (`0b9ae25`) and issue #18 is closed. For slice 9: the four decisions of `context.md`, a spike against Chromium 153 on Windows and on Linux (in `context.md`), `spec.md` accepted with every default (`1f5524b`), a design spike on both platforms with the page script as drafted, `design.md` approved and AD-008 confirmed. The spec has 51 criteria, FNT-01 to FNT-51: the design added FNT-49 to FNT-51, on a fixture `font-fallback-shaping.html`, and one row of Out of Scope. The Tasks phase added FNT-52 to FNT-54, three rules of the Terms that no criterion held (text that paints no box, a Face that is `unloaded`, the widths of several text nodes added), each on one case more of `font-fallback-bounds.html`, measured on both platforms (`context.md`); FNT-15 gained two rows for them. The spec now has 54 criteria. `tasks.md` maps each of the 54 to one task and passes `validate_tasks.py` (0 errors; three warnings of `Tests: none`, on the Linux run, the documents and the closing task, which the matrix gives as none); the Phase column of the spec's traceability table names the task of each criterion. `design.md` was not touched: its table of what the spike showed lists the ten Findings of the bounds fixture as they were, and the spec is the one followed.
- **In-progress** (file:line): none.
- **Next step**: Execute from T1, on the maintainer's go-ahead: twelve tasks in two batches (phases 1 and 2, then phases 3 and 4), so sub-agents are offered first; T12 follows the Verifier. Tests come before the code in every task, and T2 leaves out on purpose what T3, T4, T5 and T7 add.
- **Blockers**: none.
- **Uncommitted files**: none. `tasks.md`, the spec with its three criteria more and its traceability table, the line of `context.md` that records their measurement and this handoff are committed together.
- **Branch**: `feat/font-fallback`, from `main` at `0b9ae25`; not pushed.
- **Residuals of the fifth pass of slice 8** (`.specs/features/overlap/validation.md`, "Residuals and proposed issues"; none has an issue yet, and opening one is the maintainer's call; not part of slice 9): (1) the test of OVL-120 fails on a minority of runs with the wait taken out (3 of 10): it is a tripwire, and twelve calls would hold the wait on most runs. (2) The bound of the wait is a timer of the page's own world: a page that replaces `setTimeout` as well as `requestAnimationFrame` still fails every tool with `Timed out after 30s.`; a timeout around the `evaluate` of `_screenshot` (`src/squint_mcp/capture.py`), on the server's side, would end it. (3) A timer of 0ms did as well as two frames in 78 calls: whether a frame is needed is not shown. (4) `PAINT_WAIT_MAX_S` is held by its comment, not by a test. (5) No fixture holds 20,001 pixels of Hidden ink.
- **Found outside slice 8** (not part of slice 9 either): under a Content Security Policy that refuses inline styles (`style-src file:`), a page with a covered text and a low-contrast text returns `No findings`: the styles a Capture injects are refused, for every Check (`.specs/features/overlap/design.md` names `bypass_csp` to try). On a right-to-left page that scrolls sideways every tool reads the wrong pixels. Both are rows of Out of Scope of the spec of slice 8; neither has an issue yet.
- **Found outside slice 9**: the fault of issue #18 shows on Linux too. In the Playwright image for Docker, the first screenshot beyond the viewport changes the font of the generic `monospace` family from WenQuanYi Zen Hei Mono to Liberation Mono (fifteen glyphs go from 150px to 180.03px). The issue and the comment of `_settle_layout` (`src/squint_mcp/capture.py`) say Linux does not show it and no test can hold the fix. Whether the CI's Linux has those fonts was not checked. No issue yet; the maintainer's call.
- **Notes for the next session**: the suite takes 18 to 23 minutes and does not fit a 10-minute foreground timeout, run it in the background. The working tree mixes line endings (`spec.md`, `tasks.md`, `STATE.md`, `docs/ROADMAP.md`, `pyproject.toml`, most of `src/` CRLF; `tests/test_overlap.py`, the overlap fixtures, `checks/overlap.py`, `validation.md` and the files of `.specs/features/font-fallback/` LF): keep each file as it is, and check with a byte count, since `grep -c $'\r$'` counts every line in Git Bash. A heredoc with an odd number of single quotes fails in the shell wrapper: write scripts to files. `validate_tasks.py` only parses ids of the form `T<n>`. Sub-agents cannot write `.md` files with the Write tool. To run tests against a mutant without touching the tree, copy `src/squint_mcp` to a temp directory, mutate the copy and run pytest with `PYTHONPATH` set to it. To commit tasks one by one after one gate on all of them, record each task's files as blobs when it is done (`git hash-object -w --path`) and stage them with `git update-index --cacheinfo` in order. A mutant on a page of many layers is judged on several runs: the fault AD-007 fixes changes such results from one call to the next. To run a script on Linux without waiting for the CI: the image `mcr.microsoft.com/playwright/python:v1.63.0-noble` is on this machine (the same Chromium 153 as Windows); mount the script and `tests/fixtures`, `pip install playwright==1.63.0` inside, and set `MSYS_NO_PATHCONV=1` in Git Bash so the mounts keep their paths. The spike scripts of slice 9 were in the session's scratchpad and are gone; `context.md` and `design.md` hold what they measured, and `design.md` describes the page script closely enough to write it again. In slice 9 the gate of a task is the static checks and `tests/test_font_fallback.py`; the whole suite runs once per phase, in the background. To run tests of the repository on Linux, the Linux command of the gate table of `.specs/features/font-fallback/tasks.md` copies `src` and `tests` into the image and runs `uv sync --locked` there: tried on 2026-10-12 with two existing modules (37 passed, one minute in all). The baseline of slice 9 is 368 tests collected at `28360bd`. A shell command that reads a file through an empty variable waits on standard input until the timeout: name the file.
