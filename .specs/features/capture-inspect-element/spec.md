# Capture + inspect_element Specification

Slice 2 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: the roadmap section "2. Capture + inspect_element", then [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0001, ADR-0002. Decisions made there are final and are not restated as open here.

Scope size: Large. It adds the browser, the Capture, vision and the first tool that uses them. Design and Tasks both run.

## Problem Statement

Squint answers `ping` and nothing else. It cannot open a page, so no later slice can run a Check. This slice produces a stabilized Capture of a page and exposes `inspect_element`, the first tool that crosses what the browser reports (computed styles, box model) with what is painted (a crop and the colours sampled from it).

## Goals

- [ ] An MCP client can call `inspect_element` with a URL and a selector and get computed styles, box model, sampled colours, `stabilized` and one crop.
- [ ] Every error named in the roadmap returns `isError: true` with a concrete message.
- [ ] Tests drive real Chromium through the in-memory MCP client, locally and in CI.
- [ ] Slice 2 is marked done in `docs/ROADMAP.md` once verification passes.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Finding model, Checks, `detect_visual_bugs` | Slices 3 and 4 |
| Stable selector generation | Slice 3 |
| Five-crop limit, `cropIndex` | Slice 3; `inspect_element` returns exactly one crop |
| Several viewports in one call | Slice 3 (`viewports`) |
| Collecting the whole DOM into the Capture | No consumer until slice 3; the Capture holds the elements matched by the call's selector |
| Iframe contents, closed shadow roots | Out of scope for v0.1 |
| Lazy-load scrolling, pausing carousels or video | Out of scope for v0.1 |
| Browser pool, concurrency limit | Out of scope for v0.1 |
| `numpy`, `coloraide` dependencies | Nothing in this slice needs them: Pillow counts colours. They arrive with the slice that uses them |
| Private-IP blocking | Out of scope for v0.1 (stdio only) |
| A parameter to choose which computed properties are returned | The roadmap fixes the parameters: `url`, `selector`, `viewport?` |
| Tests outside the MCP tool boundary | `docs/SPEC.md` Testing Decisions: one seam |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Slice 1's FND-02 ("exactly one tool, `ping`") | Superseded by CAP-01: exactly two tools. `tests/test_ping.py::test_ping_is_the_only_tool` is rewritten to assert the new exact list | The old assertion is no longer the specified behaviour; the new one is just as strict. Pre-authorized by the maintainer | y |
| Slice 1's FND-19 (no `playwright`, `Pillow`) | Superseded by CAP-41 for those two packages | This is the slice that uses them | y |
| SDK class name | `MCPServer` (`mcp` 2.x); `docs/SPEC.md` still says "FastMCP" | Fixed by slice 1 | y |
| Which computed styles are returned | A fixed list of 20 properties held in config: `display`, `position`, `box-sizing`, `width`, `height`, `color`, `background-color`, `background-image`, `opacity`, `visibility`, `overflow-x`, `overflow-y`, `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `text-align`, `text-overflow`, `white-space` | Chromium resolves 350+ properties; returning all of them costs thousands of tokens per call. Margin, border and padding are in `boxModel` | n |
| `box` | The element's border box in CSS px, page coordinates, as `{x, y, w, h}` | Same shape as `Finding.box` in `docs/SPEC.md` | n |
| `boxModel` | `margin`, `border`, `padding` as `{top, right, bottom, left}` and `content` as `{w, h}`, CSS px | Direct reading of "box model in CSS pixels" | n |
| "Sampled colours" | The most frequent exact pixel colours inside the element's border box, at most 3, as `{hex, share}` ordered by `share` descending; `share` is the fraction of the box's pixels, rounded to 4 decimals | Deterministic and exact on flat colours. No clustering: on a gradient the top colours are single bands. Slice 4 defines the background sampling its Check needs | n |
| Pixels of the Capture | A full-page screenshot, so an element below the fold has pixels | A viewport-only screenshot would return no crop for most of a long page | n |
| Crop margin | 16 CSS px on each side, clamped to the page | SPEC says "a margin" without a number; 16px shows the element's surroundings without doubling a small crop | n |
| Crop scaling | Downscaled to 512px on the longest side when larger; never upscaled | SPEC: "downscaled to about 512px on its longest side" | n |
| Crop format | PNG, one MCP image content block; no crop field in the structured content | SPEC: images inline; with exactly one image there is nothing to index | n |
| Key casing in structured content | camelCase (`boxModel`, `sampledColors`) | Matches `cropIndex` and `overflowPx` in the Finding schema | n |
| `viewport` explicit `null` | Accepted, equal to omitting it | Same rule as `ping`'s `message` (lesson L-002) | n |
| `viewport` bounds | `width` and `height` are integers of at least 1; no upper bound | Local stdio server driven by its own user; a huge viewport ends in the total timeout | n |
| `inspect_element` annotations | `readOnlyHint: true`, `openWorldHint: true` | It changes nothing and reaches any URL the caller names | n |
| Selector language | CSS, matched by Playwright's `css` engine, which pierces open shadow roots | Reuses the engine instead of a hand-written deep query | n |
| Element with no rendered box (`display: none`, zero area) | An error, since there are no pixels to crop or sample | Returning an empty crop would be a silent non-answer | n |
| HTTP error status (404, 500) | Not a load failure: the response page is captured | "Cannot be loaded at all" means the navigation failed; an error page still renders | n |
| How the 30s timeout is tested | The test lowers `config.TOTAL_TIMEOUT_S` to 1 and calls the tool through the MCP boundary against a URL that never responds | A real 30s wait would slow every test run. The call and the assertions still go through the single seam | n |
| How "Chromium not installed" is tested | A second in-memory client whose server lifespan starts with `PLAYWRIGHT_BROWSERS_PATH` pointing at an empty directory | Reproduces the real failure without uninstalling anything | n |
| Tests when Chromium is missing on the machine | They fail, showing the tool's own "playwright install chromium" message. They are never skipped | A skip would let CI pass while testing nothing | n |
| Criteria not observable through the tool boundary (CAP-24, CAP-28, CAP-29, the `https` third of CAP-25, CAP-40 to CAP-47) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam | n |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:**

- Input validation & bounds: CAP-03, CAP-32, CAP-36, CAP-37, CAP-38, CAP-39.
- Failure / partial-failure states: CAP-22, CAP-30 to CAP-35.
- External-dependency failure: CAP-33 (page), CAP-34 (Chromium).
- State-transition integrity: CAP-35 (the server keeps serving after a timeout), CAP-29 (the context is closed on every exit path).
- Concurrency / ordering: CAP-26 (calls do not share state); one lock guards the lazy launch. No concurrency limit, per `docs/SPEC.md`.
- Data lifecycle: N/A because nothing is persisted; the context dies with the call and the browser with the server.
- Idempotency / retry: N/A because every call is stateless and read-only.
- Auth boundaries & rate limits: N/A because the server is a local stdio process.
- Observability: N/A beyond slice 1's rule (logs to stderr only); this slice adds no log line.

---

## User Stories

### P1: Inspect one element ⭐ MVP

**User Story**: As a coding agent, I want `inspect_element` to return an element's computed styles, box model, sampled colours and a crop, so that I can see what the browser resolved and what was painted without a full-page screenshot.

**Why P1**: It is the slice's deliverable and the first proof that DOM data and pixels are crossed.

**Acceptance Criteria**:

1. WHEN an MCP client lists tools THEN the server SHALL return exactly two tools, named `ping` and `inspect_element`. <!-- CAP-01 -->
2. The `inspect_element` tool SHALL declare the annotations `readOnlyHint: true` and `openWorldHint: true`. <!-- CAP-02 -->
3. The `inspect_element` tool SHALL declare an input schema whose properties are exactly `url`, `selector` and `viewport`, with `url` and `selector` of type string and required, and `viewport` not required and accepting an object or null. <!-- CAP-03 -->
4. WHEN `inspect_element` succeeds THEN the server SHALL return structured content whose keys are exactly `viewport`, `stabilized`, `box`, `boxModel`, `computed` and `sampledColors`. <!-- CAP-04 -->
5. WHEN `inspect_element` is called on `box.html` with selector `#solid` THEN `box` SHALL equal `{"x": 40, "y": 60, "w": 120, "h": 70}`. <!-- CAP-05 -->
6. WHEN `inspect_element` is called on `box.html` with selector `#solid` THEN `boxModel` SHALL equal `{"margin": {"top": 60, "right": 10, "bottom": 20, "left": 40}, "border": {"top": 5, "right": 5, "bottom": 5, "left": 5}, "padding": {"top": 10, "right": 15, "bottom": 10, "left": 15}, "content": {"w": 80, "h": 40}}`. <!-- CAP-06 -->
7. WHEN `inspect_element` succeeds THEN the keys of `computed` SHALL be exactly the 20 properties listed in Assumptions. <!-- CAP-07 -->
8. WHEN `inspect_element` is called on `box.html` with selector `#solid`, whose stylesheet sets `font-size: 2em` under a 10px parent THEN `computed` SHALL carry the resolved values `"font-size": "20px"`, `"background-color": "rgb(255, 0, 0)"` and `"display": "block"`. <!-- CAP-08 -->
9. WHEN `inspect_element` is called on `box.html` with selector `#solid` (a red padding box inside a 5px blue border) THEN `sampledColors` SHALL equal `[{"hex": "#ff0000", "share": 0.7857}, {"hex": "#0000ff", "share": 0.2143}]`. <!-- CAP-09 -->
10. WHEN `inspect_element` is called on `box.html` with selector `#many`, which paints four colours THEN `sampledColors` SHALL hold exactly 3 entries ordered by `share` descending. <!-- CAP-10 -->
11. WHEN `inspect_element` is called on `box.html` with selector `#over-image`, whose `background-color` is white under a black background image THEN `computed["background-color"]` SHALL be `rgb(255, 255, 255)` and `sampledColors[0].hex` SHALL be `#000000`. <!-- CAP-11 -->
12. WHEN `inspect_element` succeeds THEN the server SHALL return `isError: false`, one text content block containing the selector, and exactly one image content block of MIME type `image/png`. <!-- CAP-12 -->
13. WHEN `inspect_element` is called on `box.html` with selector `#solid` (120×70) THEN the crop SHALL be 152×102 px: the border box plus 16px on each side, at one image pixel per CSS pixel, not upscaled. <!-- CAP-13 -->
14. WHEN `inspect_element` is called on `box.html` with selector `#corner`, a 50×50 element in the top-right corner of the page THEN the crop SHALL be 66×66 px, the margin being clamped to the page. <!-- CAP-14 -->
15. WHEN `inspect_element` is called on `box.html` with selector `#wide` (1000×100, crop source 1032×132) THEN the crop SHALL be 512×65 px. <!-- CAP-15 -->
16. WHEN `inspect_element` is called without `viewport` THEN `viewport` SHALL equal `{"width": 1440, "height": 900}` and the full-width element `#full` SHALL have `box.w` equal to 1440. <!-- CAP-16 -->
17. WHEN `inspect_element` is called with `viewport` set to `{"width": 390, "height": 844}` THEN `viewport` SHALL equal that value and `#full` SHALL have `box.w` equal to 390. <!-- CAP-17 -->
18. WHEN `inspect_element` is called with `viewport` explicitly set to `null` THEN the server SHALL return the same structured content as when `viewport` is omitted. <!-- CAP-18 -->
19. WHEN the selector matches exactly one element inside an open shadow root (`#inner` in `box.html`) THEN the server SHALL return that element's data, with `computed.color` equal to `rgb(0, 0, 255)`. <!-- CAP-19 -->
20. WHEN the selector matches an element below the first viewport (`#below`, at y = 2000 in `box.html`) THEN `box.y` SHALL be 2000 and `sampledColors[0].hex` SHALL be `#008000`. <!-- CAP-20 -->

**Independent Test**: Call `inspect_element` on `tests/fixtures/box.html` over `file://` through the in-memory client and compare the structured content and the decoded crop.

---

### P1: Stabilized, isolated Capture

**User Story**: As a coding agent, I want each Capture taken after the page settles and in isolation from every other call, so that the same page yields the same result each time.

**Why P1**: Without it, results depend on timing and on earlier calls.

**Acceptance Criteria**:

1. WHEN the page reaches network idle within 3 seconds THEN the server SHALL return `stabilized: true`. <!-- CAP-21 -->
2. IF the page does not reach network idle within 3 seconds THEN the server SHALL return `isError: false` with `stabilized: false`. <!-- CAP-22 -->
3. WHEN the page runs a 60-second CSS animation or transition of `opacity` from 0 to 1 THEN `computed.opacity` SHALL be `1` for the animated element and for the transitioned element. <!-- CAP-23 -->
4. The Capture code SHALL wait for `document.fonts.ready` after `load` and before zeroing animations. <!-- CAP-24 -->
5. The server SHALL accept `http://` URLs, `https://` URLs and `file://` URLs. <!-- CAP-25 -->
6. WHEN `inspect_element` is called twice on `visit.html`, which records a visit in `localStorage` THEN both calls SHALL report the first-visit state, `computed["background-color"]` equal to `rgb(0, 128, 0)`. <!-- CAP-26 -->
7. WHILE Chromium cannot be launched the server SHALL still list its tools and answer `ping` with `isError: false`. <!-- CAP-27 -->
8. The server SHALL launch Chromium at most once per server run and reuse it for later calls. <!-- CAP-28 -->
9. WHEN a tool call ends, on success or on failure THEN the server SHALL close the browser context it opened for that call. <!-- CAP-29 -->

**Independent Test**: Call `inspect_element` on `motion.html`, `visit.html` and the polling page served by the local test server, and compare `computed` and `stabilized`.

---

### P1: Clear errors

**User Story**: As a coding agent, I want a clear error for each way a call can fail, so that I can correct the call or tell a broken page from a clean one.

**Why P1**: The roadmap lists these errors as part of the slice.

**Acceptance Criteria**:

1. IF the selector matches no element THEN the server SHALL return `isError: true` with a text block containing `Selector "#missing" matched no elements.` (for selector `#missing`). <!-- CAP-30 -->
2. IF the selector matches more than one element THEN the server SHALL return `isError: true` with a text block containing `Selector ".dup" matched 2 elements; it must match exactly one.` (for `.dup`, which matches two). <!-- CAP-31 -->
3. IF the URL scheme is not `http`, `https` or `file` THEN the server SHALL return `isError: true` with a text block containing `Unsupported URL scheme "ftp"; use http://, https:// or file://.` (for an `ftp://` URL). <!-- CAP-32 -->
4. IF the navigation fails THEN the server SHALL return `isError: true` with a text block containing `Could not load ` followed by the URL. <!-- CAP-33 -->
5. IF Chromium cannot be launched THEN the server SHALL return `isError: true` with a text block containing `Could not launch Chromium` and `playwright install chromium`. <!-- CAP-34 -->
6. IF a call has not finished within the total timeout (`config.TOTAL_TIMEOUT_S` seconds, 30 by default) THEN the server SHALL return `isError: true` with a text block containing `Timed out after Ns`, N being that number, and SHALL answer the next call on the same connection normally. <!-- CAP-35 -->
7. IF `inspect_element` is called without `selector` THEN the server SHALL return `isError: true` with a text block that names `selector`. <!-- CAP-36 -->
8. IF `viewport.width` or `viewport.height` is less than 1 THEN the server SHALL return `isError: true` with a text block that names the offending field. <!-- CAP-37 -->

**Independent Test**: Call `inspect_element` with each bad input and compare `isError` and the text block.

---

### P2: Tooling, configuration and documents

**User Story**: As the maintainer, I want every default in one config module, the browser code behind one import boundary and CI running real Chromium, so that later slices build on a checked base.

**Why P2**: Required by the slice; no user-facing behaviour depends on it.

**Acceptance Criteria**:

1. The `config` module SHALL define the default viewport (1440×900), the total timeout (30s), the network-idle timeout (3s), the crop margin (16px), the crop size limit (512px), the sampled-colour count (3) and the computed-property list, each with its source cited in a comment. <!-- CAP-40 -->
2. The project SHALL declare `playwright` and `Pillow` as dependencies and SHALL NOT declare `numpy` or `coloraide`. <!-- CAP-41 -->
3. The Capture module SHALL be the only module under `src/` that imports `playwright`. <!-- CAP-42 -->
4. The JavaScript that runs inside the page SHALL live in `.js` files, with no JavaScript function bodies in Python strings. <!-- CAP-43 -->
5. WHEN CI runs THEN it SHALL install Chromium before the test step. <!-- CAP-44 -->
6. The `Unreleased` section of `CHANGELOG.md` SHALL list the `inspect_element` tool. <!-- CAP-45 -->
7. `CONTRIBUTING.md` and the development section of `README.md` SHALL give the command that installs Chromium for the tests. <!-- CAP-46 -->
8. WHEN the Verifier reports PASS for this feature THEN `docs/ROADMAP.md` SHALL show slice 2 as `concluída` in both the table and the slice 2 section. <!-- CAP-47 -->

**Independent Test**: Read `config.py`, `pyproject.toml`, the CI workflow and the documents; grep `src/` for `playwright` imports.

---

## Edge Cases

- IF the selector is not valid CSS (for example `div[`) THEN the server SHALL return `isError: true` with a text block containing `Invalid selector "div[".` <!-- CAP-38 -->
- IF the selector matches exactly one element that has no rendered box (`#hidden`, `display: none`) THEN the server SHALL return `isError: true` with a text block containing `Selector "#hidden" matched an element with no rendered box.` <!-- CAP-39 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| CAP-01 | P1: Inspect one element | T3 | Implementing |
| CAP-02 | P1: Inspect one element | T3 | Implementing |
| CAP-03 | P1: Inspect one element | T3 | Implementing |
| CAP-04 | P1: Inspect one element | T4 | Pending |
| CAP-05 | P1: Inspect one element | T3 | Implementing |
| CAP-06 | P1: Inspect one element | T3 | Implementing |
| CAP-07 | P1: Inspect one element | T3 | Implementing |
| CAP-08 | P1: Inspect one element | T3 | Implementing |
| CAP-09 | P1: Inspect one element | T4 | Pending |
| CAP-10 | P1: Inspect one element | T4 | Pending |
| CAP-11 | P1: Inspect one element | T4 | Pending |
| CAP-12 | P1: Inspect one element | T4 | Pending |
| CAP-13 | P1: Inspect one element | T4 | Pending |
| CAP-14 | P1: Inspect one element | T4 | Pending |
| CAP-15 | P1: Inspect one element | T4 | Pending |
| CAP-16 | P1: Inspect one element | T3 | Implementing |
| CAP-17 | P1: Inspect one element | T3 | Implementing |
| CAP-18 | P1: Inspect one element | T3 | Implementing |
| CAP-19 | P1: Inspect one element | T3 | Implementing |
| CAP-20 | P1: Inspect one element | T4 | Pending |
| CAP-21 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-22 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-23 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-24 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-25 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-26 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-27 | P1: Stabilized, isolated Capture | T5 | Pending |
| CAP-28 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-29 | P1: Stabilized, isolated Capture | T3 | Implementing |
| CAP-30 | P1: Clear errors | T5 | Pending |
| CAP-31 | P1: Clear errors | T5 | Pending |
| CAP-32 | P1: Clear errors | T5 | Pending |
| CAP-33 | P1: Clear errors | T5 | Pending |
| CAP-34 | P1: Clear errors | T5 | Pending |
| CAP-35 | P1: Clear errors | T6 | Pending |
| CAP-36 | P1: Clear errors | T3 | Implementing |
| CAP-37 | P1: Clear errors | T3 | Implementing |
| CAP-38 | Edge cases | T5 | Pending |
| CAP-39 | Edge cases | T5 | Pending |
| CAP-40 | P2: Tooling, configuration and documents | T2 | Implementing |
| CAP-41 | P2: Tooling, configuration and documents | T1 | Implementing |
| CAP-42 | P2: Tooling, configuration and documents | T3 | Implementing |
| CAP-43 | P2: Tooling, configuration and documents | T3 | Implementing |
| CAP-44 | P2: Tooling, configuration and documents | T7 | Pending |
| CAP-45 | P2: Tooling, configuration and documents | T8 | Pending |
| CAP-46 | P2: Tooling, configuration and documents | T8 | Pending |
| CAP-47 | P2: Tooling, configuration and documents | Closing step | Pending |

**Coverage:** 47 total, 47 mapped to tasks, 0 unmapped.

**Verification method:** pytest through the in-memory MCP client for every criterion except CAP-24, CAP-28, CAP-29 and CAP-40 to CAP-47, which the Verifier checks from file evidence. CAP-25 is tested for `file://` and `http://`; `https://` shares their code path. CAP-44's live CI run needs the branch pushed, which needs an explicit go-ahead.

---

## Success Criteria

- [ ] `uv run pytest` passes locally and in CI with real Chromium.
- [ ] An MCP client calling `inspect_element` on a local page gets the element's computed styles, box model, sampled colours and a crop no larger than 512px.
- [ ] Each failure listed in the roadmap returns its message.
- [ ] Slice 2 reads `concluída` in `docs/ROADMAP.md`.
