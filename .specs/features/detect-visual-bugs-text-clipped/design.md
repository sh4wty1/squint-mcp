# detect_visual_bugs + text-clipped Design

**Spec**: `.specs/features/detect-visual-bugs-text-clipped/spec.md`
**Status**: Draft

Every choice marked "spiked" was run against `mcp 2.3.0`, `playwright 1.63.0`, `pydantic 2.13` and real Chromium before this document was written. Conforms to AD-001 and AD-002; adds AD-003.

---

## Architecture Overview

```mermaid
graph TD
    C[MCP client] -->|call_tool| T[tools/detect_visual_bugs.py<br/>schema, timeout, order, crops, result]
    T -->|check names| R[checks/__init__.py<br/>registry: name -> Check]
    T -->|capture url, viewport, "*"| K[capture.py<br/>only importer of playwright]
    K --> J[js/collect_elements.js<br/>box, styles, text, widths, selector]
    K -->|Capture, one per viewport| T
    T -->|Capture| X[checks/text_clipped.py]
    X -->|strip box| V[vision.py<br/>is_flat, crop_png]
    X -->|Finding list| T
    T -->|pixels, box| V
    T -->|text + PNGs + structured content| C
```

One call: reject unknown Check names, collapse duplicates, then for each viewport in turn take a Capture of every element of the page. Each requested Check turns each Capture into Findings. The tool sorts them, gives crops to the first five and builds the result.

### Approaches considered

All three deliver the same slice; they differ in what crosses from the page to the Checks.

| Approach | What it is | Verdict |
| --- | --- | --- |
| **A. One generic Capture (chosen)** | The collector records every element with the same fields (box, styles, text, scroll and client width, selector). A Check is a pure Python function over that | Chosen. It is ADR-0002 read literally: the Capture is the whole contract. A new Check that needs no new field touches no browser code |
| B. One page script per Check | Each Check ships a `.js` file that finds its own candidates; the Capture code runs them all | Rejected. The Capture would know every Check, and half of each Check would live in the page where it cannot see the pixels |
| C. Collect only text-clipping candidates | The collector filters to elements with clipping overflow | Rejected. It bakes one Check's rule into the Capture; slice 4 would have to widen it again |

Cost of A: every element is serialized, on every call. Accepted for v0.1 and marked in code (see Risks).

---

## Code Reuse Analysis

### Existing Components to Leverage

| Component | Location | How to Use |
| --- | --- | --- |
| `capture()` and `BrowserSession` | `src/squint_mcp/capture.py:71` | Called once per viewport with the selector `*`. Signature unchanged |
| Scheme, load, launch and stabilization handling | `src/squint_mcp/capture.py:79-105` | Reused as is; this is where DVB-47 and DVB-56 to DVB-58 get their behaviour and messages |
| Collector | `src/squint_mcp/js/collect_elements.js` | Extended with the new fields; still one function expression |
| `Element`, `Box`, `BoxModel`, `Viewport`, `Capture` | `src/squint_mcp/models.py` | `Element` gains fields; the Finding models are added next to them |
| `crop_png`, `_region` | `src/squint_mcp/vision.py:20-40` | Finding crops use `crop_png` unchanged; `is_flat` is built on `_region` |
| Tool module shape, timeout block, `CallToolResult` assembly | `src/squint_mcp/tools/inspect_element.py:44-86` | Same shape for `tools/detect_visual_bugs.py` (AD-002) |
| Session client, `local_server`, `client_without_chromium` | `tests/conftest.py` | Reused unchanged; `/hang` serves the timeout test, `polling.html` the not-stabilized one |
| `PIL.Image.getcolors(maxcolors=1)` | dependency | Returns `None` when a region has more than one colour: the whole of `is_flat` |
| pydantic `Field(min_length=1)` | dependency | Empty-list validation and the schema's `minItems`, with no handler code (spiked) |

### Integration Points

| System | Integration Method |
| --- | --- |
| MCP SDK | `server.add_tool(detect_visual_bugs, annotations=...)`; handler returns `Annotated[CallToolResult, DetectVisualBugsResult]` |
| `inspect_element` | Reads the same `Element`; it now filters `computed` down to `INSPECT_COMPUTED_PROPERTIES`, because the Capture carries one property more (`direction`) |

---

## Components

### Collector (`collect_elements.js`)

- **Purpose**: Describe each matched element: geometry, styles, text, scroll and client width, and its stable selector.
- **Location**: `src/squint_mcp/js/collect_elements.js`
- **Interfaces**: `(elements, { properties, textLimit }) => object[]`, returned in document order
- **Dependencies**: none
- **Reuses**: the existing box and box-model code

Steps:

1. Walk the document once, entering each open shadow root right after its host. The walk gives every element its document-order index and fills three count maps: `data-testid` value, `id` value, and `aria-label` keyed both by tag and by explicit `role`.
2. Sort the matched elements by that index. Spiked: Playwright returns shadow-tree matches after the whole light tree, so its order cannot be used.
3. For each element, emit the existing fields plus `text` (text content, whitespace collapsed, trimmed, cut to `textLimit` with `…`), `ownText` (it has a non-whitespace text node as a direct child), `scrollWidth`, `clientWidth` and `selector`.

Selector, first candidate whose count is 1:

1. `[data-testid="…"]`
2. `#id`, unless the id holds a character outside `[A-Za-z0-9_-]` or three or more digits
3. `[role="…"][aria-label="…"]` when the element has a `role` attribute, else `tag[aria-label="…"]`; skipped without `aria-label`
4. CSS path: tag names joined by ` > ` from `body`, `:nth-of-type(n)` only when a sibling shares the tag. Inside a shadow tree the path starts at the host's own selector, joined with ` > `.

Attribute values are escaped for `\` and `"`; ids go through `CSS.escape`.

### Capture

- **Purpose**: Unchanged: one stabilized Capture of a page at one viewport.
- **Location**: `src/squint_mcp/capture.py`
- **Interfaces**: `async capture(session, url, viewport, selector) -> Capture` (unchanged)
- **Dependencies**: as before
- **Reuses**: itself; the only edit is the argument handed to the collector: `{properties: config.CAPTURE_COMPUTED_PROPERTIES, textLimit: config.TEXT_EXCERPT_MAX_CHARS}`

### Check contract and registry

- **Purpose**: Name the Checks and fix their shape.
- **Location**: `src/squint_mcp/checks/__init__.py`
- **Interfaces**:
  - `Check = Callable[[Capture], list[Finding]]`
  - `CHECKS: dict[str, Check]` - `{"text-clipped": text_clipped.check}`
- **Dependencies**: `models`
- **Reuses**: nothing

A Check returns its Findings in the order of `Capture.elements` (document order) with `evidence.crop_index` unset; the tool assigns crops. A Check never imports `playwright`.

### text-clipped Check

- **Purpose**: Report text cut off horizontally by its own box.
- **Location**: `src/squint_mcp/checks/text_clipped.py`
- **Interfaces**: `check(capture: Capture) -> list[Finding]`
- **Dependencies**: `vision.is_flat`, `config`
- **Reuses**: `Element` fields only

An element yields a Finding when all hold:

1. `own_text`
2. `computed["overflow-x"]` is `hidden` or `clip`
3. `computed["text-overflow"]` is `clip`
4. `computed["direction"]` is `ltr`
5. `scroll_width - client_width >= config.TEXT_CLIPPED_MIN_OVERFLOW_PX`
6. the edge strip is not flat. The strip is the part of the padding box within one `font-size` of its right edge: x from `box.x + border.left + client_width - font_size` (not left of the padding box) to `box.x + border.left + client_width`, y over the padding box's height.

Severity is `major` at `config.TEXT_CLIPPED_MAJOR_OVERFLOW_PX` or more, else `minor`. Message, suggestion and source are the fixed strings of the spec.

### vision.is_flat

- **Purpose**: Say whether a region of the page is painted in a single colour.
- **Location**: `src/squint_mcp/vision.py`
- **Interfaces**: `is_flat(pixels: Image, box: Box) -> bool` - true for a single colour and for a region with no pixels
- **Dependencies**: Pillow
- **Reuses**: `_region(pixels, box, 0)`

### detect_visual_bugs tool

- **Purpose**: Input schema, orchestration, Finding order, crop allocation, summary and result. No browser or pixel logic.
- **Location**: `src/squint_mcp/tools/detect_visual_bugs.py`
- **Interfaces**:
  - `async detect_visual_bugs(url: str, ctx: Context[BrowserSession], viewports: Annotated[list[Viewport], Field(min_length=1)] | None = None, checks: Annotated[list[str], Field(min_length=1)] | None = None) -> Annotated[CallToolResult, DetectVisualBugsResult]`
- **Dependencies**: `capture`, `checks.CHECKS`, `vision.crop_png`, `config`
- **Reuses**: the `tools/inspect_element.py` shape

Steps, in order:

1. Resolve `checks`: `None` means every name in `CHECKS`; otherwise collapse duplicates and raise `ToolError` for the first name not in `CHECKS`, listing `sorted(CHECKS)`. This runs before any browser work (DVB-51).
2. Resolve `viewports`: `None` means the default; otherwise collapse equal viewports, keeping the first.
3. Under `asyncio.timeout(config.TOTAL_TIMEOUT_S)`, capture each viewport in turn.
4. Run each Check on each Capture, in viewport order. A stable sort by severity rank then gives severity, viewport order, document order.
5. For the first `config.MAX_CROPS` Findings: set `crop_index` to the position and append `crop_png(capture.pixels, finding.box)` as an image block.
6. Build the summary line and return text + images + structured content.

### Fixtures and tests

- **Location**: `tests/fixtures/` (`Ahem.ttf`, `text-clipped-bug.html`, `text-clipped-clean.html`, `text-clipped-bounds.html`, `selectors.html`, `many.html`, `responsive.html`), `tests/test_detect_visual_bugs.py`, `tests/test_text_clipped.py`, `tests/test_selectors.py`
- **Reuses**: `tests/conftest.py` fixtures. `tests/test_inspect_element.py` is not edited. `tests/test_ping.py`'s exact-tool-list test is rewritten to three names (DVB-01).

---

## Data Models

```python
class Element(BaseModel):  # one element as collected in the page; camelCase on the wire
    box: Box
    box_model: BoxModel
    computed: dict[str, str]
    text: str          # excerpt: whitespace collapsed, at most 40 chars
    own_text: bool     # has a non-whitespace text node as a direct child
    scroll_width: int
    client_width: int
    selector: str      # unique on the page


Severity = Literal["critical", "major", "minor", "info"]
Category = Literal["visual-bug", "a11y", "consistency", "ux", "responsive"]


class Evidence(BaseModel):  # camelCase on the wire
    computed: dict[str, str]
    measured: dict[str, float]
    crop_index: int | None = None


class Finding(BaseModel):
    check: str
    category: Category
    severity: Severity
    message: str
    selector: str
    text: str
    box: Box
    viewport: Viewport
    evidence: Evidence
    suggestion: str | None = None
    source: str | None = None


class CaptureSummary(BaseModel):
    viewport: Viewport
    stabilized: bool


class DetectVisualBugsResult(BaseModel):  # structured content
    findings: list[Finding]
    captures: list[CaptureSummary]
```

**Relationships**: `Capture.elements` now means "the elements matched by the selector, in document order"; with `*` that is the whole page. `Finding` copies `selector`, `text` and `box` from its `Element` and `viewport` from its `Capture`. `Finding` and `Evidence` live in `models.py`; the two result models live in the tool module, like `InspectElementResult`.

`measured` holds integers for this Check (`overflowPx`, `scrollWidth`, `clientWidth`); they are dumped as JSON integers. The type stays numeric so slice 4 can put a contrast ratio there.

New config values: `CAPTURE_COMPUTED_PROPERTIES` (the 20 inspect properties plus `direction`), `MAX_CROPS = 5`, `TEXT_EXCERPT_MAX_CHARS = 40`, `TEXT_CLIPPED_MIN_OVERFLOW_PX = 2`, `TEXT_CLIPPED_MAJOR_OVERFLOW_PX = 8`.

---

## Error Handling Strategy

Every anticipated failure is a `ToolError` (AD-002). No partial result is ever returned.

| Error Scenario | Handling | Message |
| --- | --- | --- |
| Unknown Check name | Checked in the tool before any browser work | `Unknown check "nope". Valid checks: text-clipped.` |
| `checks` or `viewports` empty | SDK validation, `min_length=1` (spiked) | pydantic's message, naming the field |
| Viewport side below 1, `url` missing | SDK validation (spiked) | pydantic's message, naming `viewports.0.width` or `url` |
| Scheme, navigation failure, Chromium launch | Raised by `capture`, unchanged | Same messages as `inspect_element` |
| Total timeout, all viewports together | `TimeoutError` from `asyncio.timeout` caught in the tool | `Timed out after 30s.` |
| One viewport fails | The error propagates; Captures already taken are dropped | The error of that viewport |
| Network never idle | Not an error | `stabilized: false` on that entry of `captures` |
| No Findings | Not an error | `No findings in 1 viewport.` |

---

## Risks & Concerns

| Concern | Location (file:line) | Impact | Mitigation |
| --- | --- | --- | --- |
| The exact-tool-list test breaks when a tool is added | `tests/test_ping.py:34` | Fails on registration of `detect_visual_bugs` | Expected (DVB-01). Rewritten in the task that registers the tool |
| `computed` gains `direction`, and `inspect_element` promises exactly 20 keys (CAP-07) | `src/squint_mcp/tools/inspect_element.py:75` | The untouched inspect tests would fail | The tool filters `computed` to `INSPECT_COMPUTED_PROPERTIES`; DVB-66 keeps the old assertions as the guard |
| Every element of the page is serialized with 21 styles | `src/squint_mcp/js/collect_elements.js` | A page with thousands of elements sends megabytes over the browser pipe and may hit the 30s timeout | Accepted for v0.1; a `ponytail:` comment names the upgrade (collect only elements a Check can use). The count maps keep selector generation linear |
| Viewports are captured one after another | `src/squint_mcp/tools/detect_visual_bugs.py` (new) | Each one pays a page load and up to 3s of idle wait | Accepted; a `ponytail:` comment names the upgrade (capture them concurrently) |
| A host with a light-DOM child and a shadow-root child of the same tag | `src/squint_mcp/js/collect_elements.js` | Spiked: `host > h3` matches both, so the CSS path of either is not unique and `inspect_element` reports two matches | Accepted as a known limit with a comment in the collector. It needs a slotted child and a shadow child of the same tag at the same position, with no usable id or test id on either |
| Text over a gradient or a photo | `src/squint_mcp/checks/text_clipped.py` (new) | The edge strip is never flat, so hidden text that still overflows is reported | Accepted: the DOM signal must already hold; the pixel step only removes the cases where nothing is painted |
| `_region` rounds a fractional box outwards | `src/squint_mcp/vision.py:26-29` | A strip on a fractional box may include one pixel column outside the clip edge | Accepted; it can only turn a flat strip into a non-flat one when the neighbouring pixel differs |
| Ahem's no-break space is ink, not blank | `tests/fixtures/` (new) | A "whitespace only" fixture built with `&nbsp;` would be reported | Spiked: the fixture uses regular spaces under `white-space: pre` (scrollWidth 300, strip flat) |
| A solid strip of Ahem ink is one colour | `tests/fixtures/` (new) | With `line-height` equal to `font-size` the confirmation would depend on sub-pixel fringes | Fixtures use a 30px line for 20px glyphs: the strip always holds page background and ink |
| `uv` is not installed on the maintainer's machine at the moment | environment | `uv run pytest` fails before any test | Spikes ran through `pipx run uv`. Execute needs `uv` on `PATH` or the same wrapper |

---

## Tech Decisions

| Decision | Choice | Rejected alternative | Rationale |
| --- | --- | --- | --- |
| What the Capture carries | Every element, generic fields, collected by one script | A script per Check; candidates only | See Approaches. Recorded as AD-003 |
| Where selectors are generated | In the collector, for every element | In Python after the Capture; in the page on demand | It needs the live DOM, and the browser context is closed before any Check runs |
| Uniqueness test | Three count maps filled in one walk | `querySelectorAll` per candidate per element | Linear instead of quadratic; exact for the three candidate forms |
| Shadow boundary in the CSS path | ` > ` | A space | Spiked: `[data-testid="card"] > h3` matches the shadow root's child; the descendant form also matches slotted elements |
| Document order | Own walk in the collector, shadow tree right after its host | Playwright's match order | Spiked: Playwright lists shadow matches after the entire light tree |
| How all elements are selected | `capture(..., selector="*")` | A second capture function or a `None` selector | `*` already pierces open shadow roots; no new code path in `capture` |
| Pixel confirmation | `getcolors(maxcolors=1) is None` on the edge strip | Comparing against a sampled background colour; a single pixel column | No background model needed, and one `font-size` of width cannot fall entirely inside a letter gap |
| Capturing several viewports | A loop, one fresh context each | `asyncio.TaskGroup`; one context resized between captures | Simplest thing that meets the spec; a resized page keeps layout state from the previous size |
| Crop allocation | In the tool, after sorting | In each Check | Only the tool sees every Finding of the call |
| Empty lists | `Field(min_length=1)` in the signature | A check in the handler | The schema publishes `minItems: 1` and the SDK names the field (spiked) |
| Fixture font | Ahem, loaded from `tests/fixtures/Ahem.ttf` by `@font-face` | System monospace; a data URI | Spiked: loads over `file://`, 10 glyphs at 20px measure exactly 200px. The font's name table declares it public domain with a CC0 fallback |
| Test files | One for the tool, one for the Check, one for selectors | One file | Each stays reviewable; all three go through the MCP boundary |

Project-level decision recorded in `.specs/STATE.md` as AD-003.
