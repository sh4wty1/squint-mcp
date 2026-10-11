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

- **Feature**: `overlap` (roadmap slice 8) / `.specs/features/overlap/`
- **Phase / Task**: Design, under `tlc-spec-driven`, scope Complex. Stopped in the middle of the spike; nothing of Design is written.
- **Completed**: Specify (`spec.md`, OVL-01 to OVL-69, and `context.md`; `validate_spec.py --strict` passes). A spike in real Chromium of how the Capture learns Text ink, Hidden ink and the Coverer: one mechanism gives the Terms on every case measured, and the 100 covered texts of OVL-60 take 3.8s to 10.8s against the limit of 30s. Mechanism, results, costs and what is open are in `context.md`, "Design spike".
- **In-progress** (file:line): none in the repository.
- **Next step**: settle the four points listed as open in `context.md` (text painted over text in the cheaper shape, a dark root background, a cap on hit tests, layers on every call or on request), run the existing suite with Chromium launched with `--disable-lcd-text`, then record AD-005 and write `design.md`.
- **Blockers**: the maintainer has not said whether the spec is approved as it stands: the message of 2026-10-10 left "Decisão sobre a spec" unfilled. The spike asks for three additions to the Terms, for the maintainer to accept or change: "seen" relative to the ink of the pixel alone, text rasterized in grayscale (`--disable-lcd-text`, which touches every Capture), and hit testing below the first viewport done with the page scrolled. The five unconfirmed choices of the Assumptions table stand as before.
- **Uncommitted files**: none.
- **Branch**: `feat/overlap`, local only, from `origin/main` at `8aa017c`. Not pushed; no pull request.
- **Spike**: throwaway, outside the repository, in the scratchpad of the session of 2026-10-10, under `%LOCALAPPDATA%/Temp/claude/E--projetos-fassi-squint-mcp/bbc2085e-9df4-4743-8b8f-48d8dee3565a/scratchpad/overlap-spike/` (`build.py`, `page.js`, `spike.py`, `spike2.py`, `probe*.py`). The files may be gone; `context.md` holds what they showed.
