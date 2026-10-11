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

## Handoff

- **Feature**: `overlap` (roadmap slice 8) / `.specs/features/overlap/`
- **Phase / Task**: Execute, under `tlc-spec-driven`, scope Complex. T1 to T13 and the fixes F1 to F8 are done and committed; the third validation pass is FAIL and the loop is escalated to the maintainer.
- **Completed**: T1 to T13 (`89385b0` to `cb8d81b`), the first validation pass (`aef0799`, FAIL on eleven untested rules), F1 to F4 (`7c32a5b` to `f5f190b`), the second pass (`0a25cca`, FAIL on eleven more), F5 to F8 (`c6dd9f1` to `a11b13e`), the third pass (`validation.md`, FAIL on twelve). The gate passes: 325 tests, pyright and ruff clean. The spec has 91 criteria.
- **In-progress** (file:line): none.
- **Next step**: the maintainer decides, on the third report's "Fix Plans": (1) text under a colour-changing `filter` gets no Finding (`design.md:263` accepts it; neither Out of Scope nor the CHANGELOG lists it): a row and a line, or a change to the Capture; (2) a glyph colour of alpha 0 that Chromium does not compute to `rgb()` is reported (`src/squint_mcp/checks/overlap.py:25-31`, against the rule of OVL-38): fix the parse, or a row in Out of Scope; (3) a third fix round for the ten rules that are right today and that no test holds, asked per side, axis and order of each rule, or accept them as a listed residual. Then a Verifier pass, and only on PASS the closing step of `tasks.md` (roadmap, the spike and its `extend-exclude` removed, issue #18 through the pull request).
- **Blockers**: the three decisions above.
- **Uncommitted files**: none.
- **Branch**: `feat/overlap`, local only, from `origin/main` at `8aa017c`. Not pushed; no pull request.
- **Spike**: in `.specs/features/overlap/spike/` until the slice closes.
