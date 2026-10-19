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

### AD-009
- **Decision**: A Capture reads what the tokens of a page are made of on every call, not on request. The collector reads twelve more computed properties (the four border colours, the four corner radii, `box-shadow`, `text-shadow`, `row-gap`, `column-gap`) and gives each element `auto_margins`, the sides whose computed margin is `auto`. `Capture.srgb` holds each computed colour of the elements that Chromium does not write as `rgb()` or `rgba()`, converted to `color(srgb ...)` by the browser itself. `capture(..., descendants=True)` holds the matches of the selector and every element under one of them, open shadow trees included, each once. A tool that reads no pixel still gets the three pixel layers of AD-004.
- **Reason**: `extract_tokens` reads values and the maintainer decided the Capture gains no third fact on request (`.specs/features/extract-tokens/context.md`). `getComputedStyle` gives a margin as laid out, 620px for `auto`; only `computedStyleMap()` gives the keyword. Chromium keeps a colour in the notation it was written in, and a conversion in Python with the matrices of CSS Color 4 differed from the painted pixel for `rec2020` and by one step for a `display-p3` colour, where the browser's own (`fillStyle` of a detached `OffscreenCanvas` set to `color(from <text> srgb r g b / alpha)`) differed on none of 30 colours. With `descendants`, the selector stays the `scope` the caller wrote, so the errors quote it as written. Spiked for slice 10 on Chromium 153.
- **Trade-off**: Every tool pays for what one tool reads. The collector takes 12% to 27% longer (865ms to 968ms for 1,004 elements, 5.35s to 6.79s for 5,004; 7% to 8% of it the properties, the rest the margin flags) and its output is 37% larger. `extract_tokens` takes four screenshots it does not read, 0.3s to 0.9s of a call of 1s to 2s: the layers stay because making them optional would touch every Check. The conversion of colours and the margin flags use `OffscreenCanvas` and `computedStyleMap` of the page's own world. A Capture has one more argument that changes which elements it holds.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/config.py`, `src/squint_mcp/js/collect_elements.js`, `src/squint_mcp/js/srgb_colors.js`, `src/squint_mcp/models.py`, `src/squint_mcp/tokens.py`, `src/squint_mcp/tools/extract_tokens.py`, every Check that comes to read a colour.
- **Date**: 2026-10-13
- **Status**: active. Written with the design of slice 10 (`.specs/features/extract-tokens/design.md`); confirmed by the maintainer on 2026-10-13.

### AD-010
- **Decision**: `inspect_element`, `detect_visual_bugs` and `extract_tokens` take `storageState`, the absolute path of a Playwright storage state file. `capture.capture` reads it whole before the browser is asked for, and creates the context of each Capture with its cookies and `localStorage`. The file is never written; a relative path, an unreadable file and a file that is not a storage state are `ToolError`s that never quote it.
- **Reason**: ADR-0002 keeps interaction out of the tools and names attaching over CDP as the way past the initial-state limit. A page behind a login, such as the Admin of central-jogos-gc2 (an `HttpOnly` session cookie scoped to its API path), needs no interaction for its first screen after the login, only the session. Playwright already defines the file and writes it (`playwright codegen --save-storage`); a path keeps the cookies out of the agent's transcript, and only an absolute one reads the same file whatever the server's working directory.
- **Trade-off**: A second way past the initial state beside the CDP one of ADR-0002, reaching only the first screen after a login. `sessionStorage` is not carried. An expired session is examined as the login screen, with no error.
- **Scope**: `src/squint_mcp/capture.py`, `src/squint_mcp/tools/inspect_element.py`, `src/squint_mcp/tools/detect_visual_bugs.py`, `src/squint_mcp/tools/extract_tokens.py`, every tool that opens a URL.
- **Date**: 2026-10-17
- **Status**: active. Written with the plan of slice 12 (`.specs/features/storage-state/plan.md`), approved by the maintainer on 2026-10-17.

## Handoff

- **Feature**: `font-fallback` (slice 9) / `.specs/features/font-fallback/`: the round of issue #20 is **done** and waits for the merge of pull request #29. Criteria FNT-63 to FNT-67, tasks F4 to F8. The seventh Verifier is a **PASS**, limited in scope by the maintainer, after passes 3 to 6 each found a class of family name no case held (quotation marks, apostrophes, whitespace, the hexadecimal decoder). `validate_state.py font-fallback` exits 0. Every traceability row reads Verified, and every Goal and Success Criterion of `spec.md` is ticked. The third Success Criterion cites CI run 38928445283 on `f26e730`. The next slice of the roadmap is still 11, Release 0.2.0 (`tlc-implement`).
- **Phase / Task**: sessions of 2026-10-15 and 2026-10-16, the resume after slice 10, in four parts:
  1. Git cleanup: #22 merged (`f5ec283`); `feat/offscreen-overflow`, `origin/feat/font-fallback` and `feat/extract-tokens` (local and remote) deleted, each proven contained in `origin/main` first.
  2. Lessons: the maintainer approved merging L-094 into L-050 (`4015689`). L-091, L-092, L-093 and L-095 stay candidates. `lessons.py` cannot confirm or delete a lesson by hand, so L-092 and L-094 expire around 2026-11-28.
  3. Issue #20: F4 to F6 by this session. F7 was written by Codex from a prompt of this session; its commit was reworded to `fix(...)` as `d02f632`. F8 by this session. Seven validation passes in all, the history in `validation.md`.
  4. The items without an issue, decided by the maintainer:
     - opened: #23 (OVL-120 tripwire), #24 (paint wait bound and `PAINT_WAIT_MAX_S`), #25 (20,001 px of Hidden ink), #26 (`style-src` and `bypass_csp`, `needs-triage`), #27 (RTL page that scrolls sideways, `needs-triage`), #28 (residual mutants of font-fallback R7, `needs-triage`; N60-unescape-quotes-only is now dead);
     - fixed: the docstring of `_settle_layout` in pull request #30, with a comment on #18 giving the Linux measurement;
     - left as is: the 0ms timer of the fifth pass of slice 8 (no defect shown), and R8 (the maintainer's decision of 2026-10-13).
- **Completed**: `f5ec283..087cf37` on `fix/font-name-backslash` (pull request #29, CI green on `f26e730`, a new run started by the push of `087cf37`), and `3293d08` on `docs/settle-layout-linux` (pull request #30). Gates: the Build of `bdbef50` passed (503 in 22m30s), and so did that of `3293d08` (498 in 21m51s).
- **In-progress** (file:line): none.
- **Next step**: the maintainer's call: merge #29 and #30. Then delete `fix/font-name-backslash` and `docs/settle-layout-linux`, local and remote, and the worktree `C:\Fassi\squint-mcp-settle` (`git worktree remove`). Then slice 11.
- **Open for the maintainer**:
  1. The candidate lessons L-096 to L-098 of this round. L-097 and L-098 say the same thing as L-096 from two sides: pin a value that must be kept exactly with cases of every character class at once.
  2. From the seventh pass:
     - `CHANGELOG.md:24` lists the font-fallback fix under `### Fixed` for a Check that is itself unreleased: settle it at the release;
     - the Linux gate is not recorded under T10 of `tasks.md`; the seventh pass ran it on `bdbef50` (58 passed);
     - `bare` departs from CSS Syntax only on inputs Chromium never writes (code point 0, surrogates, above 0x10FFFF);
     - the final sigma (`Σ` against `ς`) is an accepted limit, `ponytail:` at `font_widths.js:53`;
     - the Capture changes of slice 10 were not verified mutant by mutant.
  3. The other local branches (`ci/publish-workflow`, `docs/close-slice-5`, `feat/capture-pixel-budget`, `feat/pypi-release`, and `fix/pixel-work-timeout` with its worktree `C:\Fassi\squint-mcp-pixel-timeout`) were not examined.
- **Blockers**: none.
- **Docker on this machine**: killing Docker Desktop leaves Unix sockets that Windows can no longer open, rename or delete (error 1920). Folders moved aside so far, all deletable after a restart of Windows: `%LOCALAPPDATA%\Docker\run.stale-20261014`, `run.stale2-20261014`, `run.stale3-20261014`, `run.stale-150548`, `run.stale`, and `%LOCALAPPDATA%\docker-secrets-engine.stale-20261014`, `docker-secrets-engine.stale-150548`. Quit Docker Desktop from its menu or with `docker desktop stop`, never with `Stop-Process -Force`. It ran through this session; the image `mcr.microsoft.com/playwright/python:v1.63.0-noble` holds the same Chromium 153.0.8010.12 as Windows.
- **Uncommitted files**: none.
- **Branch**: `fix/font-name-backslash`, with this Handoff commit local and one ahead of `origin/fix/font-name-backslash` (`087cf37`); push it with the next change to #29, or drop it into `main` after the merge. The local `main` is at `f5ec283`, as `origin/main`.
- **Notes for the next session**:
  - **Timing**: the whole suite takes 20 to 23 minutes; run it in the background with a log ending in `BUILD_EXIT=<code>`, and wait for the notice. A fresh Verifier sub-agent takes 15 minutes in a limited scope and 40 to 80 minutes with a sensor of its own and a Build.
  - **Line endings**: keep each file as it is and check with a count of `\r` bytes. Almost all of `src/`, `tests/`, `spec.md`, `tasks.md`, `design.md` and `STATE.md` is CRLF; a `validation.md` written by a Verifier is LF in the working copy. The Edit tool keeps CRLF.
  - **Escapes**: shell heredocs can eat backslashes, so write scripts and texts that hold backslashes with the Write tool. The Edit tool turns `\u00a0` in its new text into the raw character; write such escapes from a script.
  - **Python**: `python3` is 3.11; use `uv run python`.
  - **Mutants**: copy `src/squint_mcp` to the scratchpad, apply `(old, new)` byte pairs each asserted to occur once, run pytest with `PYTHONPATH` set to the copy, and assert that `squint_mcp.__file__` is in it.
  - **Commits**: headers are Conventional Commits of at most 72 characters; check them with `.claude/skills/tlc-spec-driven/scripts/check_commit.py`.
  - **Linux**: run Linux checks in the Playwright image with `MSYS_NO_PATHCONV=1` in Git Bash.
  - **Font names**: a family name is read from `document.fonts` as is; the computed `font-family` writes control characters as `\<hex> ` (lower case, one space after) and leaves other characters raw. The probe and sweep scripts of the passes were in scratchpads and are gone; `validation.md` describes them.
  - **Older notes**: the notes of the earlier sessions are in git, in the Handoff of `d0fcc41`.
