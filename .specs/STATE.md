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

## Handoff

- **Feature**: `detect-visual-bugs-text-clipped` (roadmap slice 3) / `.specs/features/detect-visual-bugs-text-clipped/`
- **Phase / Task**: Execute done (T1 to T9) and validated. The third validation pass failed on four surviving mutants; Fix 16 to Fix 19 answer them and the re-run kills all four (`validation.md`, "Re-run of the survivors of pass 3"). PR #7 is open with both rounds of review answered.
- **Completed**: Specify, discuss, Design (AD-003), Tasks, Execute, three validation passes and the re-run, the fixes of the review of PR #7 (`.checks/pr7-review-fixes.md`, verified), the status lines of F3 (`.checks/pr7-f3-status-lines.md`). Gate: 135 tests pass. Roadmap slice 3 is `concluída` (DVB-68).
- **In-progress** (file:line): none.
- **Next step**: the maintainer merges PR #7. Then slice 4 (`low-contrast-real`, `tlc-spec-lean`); issue #8 (document order across Checks) belongs to it.
- **Blockers**: none. Open decision, not a blocker: text cut inside an inline child of a parent whose own text fits is no longer reported since `bc80575`; the spec does not record it.
- **Uncommitted files**: none
- **Branch**: `feat/detect-visual-bugs-text-clipped`
