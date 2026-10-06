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

## Handoff
