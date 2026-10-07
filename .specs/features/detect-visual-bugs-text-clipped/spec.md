# detect_visual_bugs + text-clipped Specification

Slice 3 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: the roadmap section "3. detect_visual_bugs + text-clipped", then [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0001, ADR-0002, ADR-0003, and the decisions AD-001 and AD-002 in [`.specs/STATE.md`](../../STATE.md). Decisions made there are final and are not restated as open here. The four decisions taken with the maintainer for this slice are in [`context.md`](context.md).

Scope size: Large. It adds the Finding model, the Check contract, selector generation, a second browser tool and the first Check. Design and Tasks both run.

## Problem Statement

Squint can inspect one element the caller already knows about, but it cannot yet answer "what is wrong on this page?". This slice delivers the whole flow Capture → Check → Finding[] through the `detect_visual_bugs` tool, with `text-clipped` as the first Check, so that slice 4 only has to add a Check.

## Goals

- [ ] An MCP client can call `detect_visual_bugs` with a URL and get Findings, `stabilized` per viewport and up to five crops.
- [ ] `text-clipped` reports every planted problem in its "bug" fixture and nothing in its "clean" fixture.
- [ ] Every Finding selector is unique on the page and works as the `selector` of `inspect_element`.
- [ ] Adding a Check needs one new module under the Checks package and no change to browser code.
- [ ] Slice 3 is marked done in `docs/ROADMAP.md` once verification passes.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| `low-contrast-real`, any other Check | Slice 4 and later |
| Profile, Audit, score | Not in v0.1 |
| Vertical clipping (`scrollHeight > clientHeight`) | `docs/SPEC.md` defines the signal as `scrollWidth > clientWidth` |
| Text clipped by an ancestor that holds no text itself | Decided in `context.md`; known limit of this Check |
| Right-to-left text (`direction: rtl`) | The cut is on the other edge; not asked for by the roadmap |
| Intended ellipsis (`text-overflow: ellipsis`) | Belongs to the future `ellipsis-unintended` Check |
| Clipped text in an element painted at another size than it is laid out (a `transform` that scales, rotates or skews it, on the element or on an ancestor) | `scrollWidth` and `clientWidth` are layout pixels and the pixels are painted ones; the edge strip has no single place under a rotation or a skew (ADR-0003). Known limit of this Check |
| Text inside form controls (`input`, `textarea`, `select`) | They hold no text node; not asked for by the roadmap |
| Role selectors in Playwright syntax, computed accessible name | Decided in `context.md`: selectors are CSS only |
| Any change to the behaviour of `inspect_element` or `ping` | Slices 1 and 2 are closed |
| Iframe contents, closed shadow roots | Out of scope for v0.1 |
| `numpy`, `coloraide` dependencies | Nothing in this slice needs them; Pillow reads the pixels |
| A parameter for thresholds or the crop limit | `docs/SPEC.md`: behaviour changes only through `url`, `viewports`, `checks` |
| Tests outside the MCP tool boundary | `docs/SPEC.md` Testing Decisions: one seam |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Role + name selector step | CSS only: `tag[aria-label="…"]`, or `[role="…"][aria-label="…"]` when the element has an explicit `role` attribute; no `aria-label` means the step is skipped | Decided with the maintainer; keeps every selector usable in `inspect_element` | y |
| Axis | Horizontal only | Decided with the maintainer; literal `docs/SPEC.md` | y |
| Severity of `text-clipped` | `minor` when `overflowPx` is below 8, `major` at 8 or more; the threshold lives in config | Decided with the maintainer; makes severity ordering testable in this slice | y |
| Reach | Only an element with a non-whitespace text node as a direct child and the clipping overflow on itself | Decided with the maintainer | y |
| Slice 2's CAP-01 ("exactly two tools") | Superseded by DVB-01: exactly three. Both exact tool-list assertions are rewritten to the new list: the tool-list test of `tests/test_ping.py` and the one inside `test_server_answers_ping_while_chromium_cannot_be_launched` of `tests/test_inspect_element.py` | Same precedent as CAP-01 over FND-02 | n |
| Structured content shape | `{"findings": Finding[], "captures": [{"viewport", "stabilized"}]}`, `captures` in the order the viewports were requested | `docs/SPEC.md` asks for `Finding[]` plus `stabilized` per viewport; "Capture" is the glossary term for one page at one viewport | n |
| Key casing | camelCase in structured content, except the CSS property names inside `evidence.computed` | Same as slice 2 | n |
| Optional Finding fields | `suggestion` and `source` are always present as keys, `null` when a Check has none | A fixed key set is easier to depend on than a varying one | n |
| Finding order | Severity (`critical`, `major`, `minor`, `info`), then the order the viewports were requested, then document order (a shadow tree sits at its host's position) | `docs/SPEC.md` fixes only severity; the two tie-breakers make the order deterministic | n |
| `cropIndex` | Zero-based index among the image content blocks of the response, not counting the text block | `docs/SPEC.md`: "index of the image in this response" | n |
| Crop limit | Five per call across all viewports; the first five Findings in the returned order get them | `docs/SPEC.md` Images | n |
| Crop geometry | Same as `inspect_element`: border box plus 16px, clamped to the page, at most 512px on the longest side, PNG | Reuses slice 2's vision code and config | n |
| Text summary | `No findings in N viewport(s).` or `Found N finding(s) in M viewport(s): 2 major, 1 minor.`, listing only severities that occur, most severe first, with `finding`/`viewport` singular for 1 | `docs/SPEC.md` asks for "a short text summary" without wording | n |
| `text` excerpt | The element's text content with runs of whitespace collapsed to one space and trimmed; when longer than 40 characters, the first 39 followed by `…` (U+2026). The limit lives in config | `docs/SPEC.md`: "visible text excerpt, ~40 chars" | n |
| `evidence.computed` for `text-clipped` | Exactly `overflow-x`, `white-space`, `text-overflow`, `width`, `font-size` | The properties that explain the cut. `docs/SPEC.md`'s example shows the `overflow` shorthand; the axis-specific longhand is what the Check reads | n |
| `evidence.measured` for `text-clipped` | Exactly `overflowPx`, `scrollWidth`, `clientWidth`, with `overflowPx = scrollWidth - clientWidth` | Lets the reader verify the number in the message | n |
| Clipping overflow values | `overflow-x: hidden` and `overflow-x: clip` | `auto` and `scroll` leave the text reachable by scrolling | n |
| Minimum overflow | 2px; a 1px difference is not reported. The threshold lives in config | `scrollWidth` and `clientWidth` are rounded integers, so 1px can be rounding alone | n |
| Pixel confirmation ("the crop ending on a cut glyph") | Confirmed when the strip of the element's padding box within one `font-size` of its right edge is painted in more than one colour. A strip of a single colour means no text is visibly cut and yields no Finding | A single pixel column would miss a cut that falls between two glyphs; one `font-size` is wider than any letter gap. Rejects screen-reader-only text, hidden text and overflow made of whitespace | n |
| Ids that "look generated" | An id is skipped when it contains a character outside `[A-Za-z0-9_-]` or three or more digits | Catches `:r1:`, `radix-:r0:`, `ember1234`, `css-1a2b3c`. A real id wrongly skipped only costs a fall-through to the next step | n |
| `data-testid` variants | Only the `data-testid` attribute | `docs/SPEC.md` names only that one | n |
| Selector quoting | Attribute values are always double-quoted and escaped (`[data-testid="hero-title"]`); ids go through CSS identifier escaping. `docs/SPEC.md`'s example shows the value unquoted | A quoted value is valid for every string | n |
| Uniqueness | "Unique on the page" counts matches across the document and every open shadow tree, the way `inspect_element` resolves selectors | A selector that is unique only in the light DOM would match twice in `inspect_element` | n |
| CSS path | Tag names joined by ` > ` from `body`, with `:nth-of-type(n)` only on a segment that has a sibling of the same tag. For an element in an open shadow tree: the host's own generated selector, ` > `, then the path inside the shadow tree | Deterministic and short enough. Spiked at Design: in the selector engine `inspect_element` uses, the child combinator reaches the children of a host's shadow root, and it is stricter than the descendant combinator, which also matches slotted light-DOM elements | n |
| `viewports` / `checks` explicit `null` | Accepted, equal to omitting | Lesson L-002; same as `viewport` in slice 2 | n |
| `viewports` / `checks` as an empty list | Validation error naming the field | "Run nothing" is never what the caller meant | n |
| Duplicate entries | Equal viewports, and repeated Check names, are collapsed to their first occurrence | Keeps "one Finding per element, per viewport, per Check" true | n |
| Upper bound on `viewports` | None; the 30s total timeout bounds the call | Same reasoning as slice 2's viewport size | n |
| Total timeout | 30s for the whole call, all viewports together | `docs/SPEC.md`: "every tool call bounded by a total timeout" | n |
| One viewport failing | The whole call fails; no partial result | AD-002 | n |
| Unknown Check | Checked before any browser work. The message names the first unknown name in the order given and lists the valid names alphabetically | A wrong call should fail without paying for a browser | n |
| Element under a `transform` | An element whose painted border box (`box`) differs from its layout border box (`boxModel.content` plus padding and border) by 1px or more in width or in height yields no Finding. A transform that keeps both sizes is treated as none: a translated element is reported, with `box` at its painted position and `overflowPx` in layout pixels; so is a mirrored or half-turned one | ADR-0003: `box` is painted, the box model is layout, and a Check that crosses the two has to account for the transform. Staying silent costs a missed Finding; guessing where the cut is painted costs a false one, and a Finding has to be trustworthy. The 1px tolerance is the one the Capture already uses to tell a transform from none | y |
| Fix of issue #5 | The branch takes in the fix of issue #5 (PR #6) before Design is approved | The rule above compares `box` with `boxModel.content`, which is the layout size only since that fix; before it the two were always equal and DVB-69 could not be met without a new Capture field | n |
| Fixture text geometry | Fixtures set their text in the Ahem test font (from web-platform-tests, every glyph a 1em square of ink), bundled with the fixtures, at `font-size: 20px` and `line-height: 30px`, so `XXXXXXXXXX` is exactly 200px wide in a 30px-high box with 5px of page background above and below the glyphs. Verified at Design against real Chromium: the font declares itself public domain (CC0 fallback), Chromium loads it from a `file://` URL next to the page, and the widths are exact. Ahem's no-break space is a full square of ink; only the regular space is blank | System fonts differ between machines and CI, so exact `overflowPx` values need a font with known advances. The 30px line keeps the edge strip from being solid ink, which the pixel confirmation would read as a single colour | n |
| Criteria not observable through the tool boundary (DVB-60 to DVB-68) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam | n |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:**

- Input validation & bounds: DVB-03, DVB-50 to DVB-55.
- Failure / partial-failure states: DVB-47, DVB-56 to DVB-59; a failing viewport fails the call (AD-002).
- External-dependency failure: DVB-57 (page), DVB-58 (Chromium).
- State-transition integrity: DVB-59 (the server keeps serving after a timeout).
- Concurrency / ordering: DVB-15 (Finding order), DVB-45 (`captures` order). Whether viewports are captured in sequence or together is a Design choice; the output order does not depend on it.
- Idempotency / retry: DVB-12 (the same call returns the same structured content).
- Data lifecycle: N/A because nothing is persisted; crops exist only in the response.
- Auth boundaries & rate limits: N/A because the server is a local stdio process.
- Observability: N/A beyond slice 1's rule (logs to stderr only); this slice adds no log line.

**Fixtures named below** (all under `tests/fixtures/`, white page, black Ahem text at 20px on a 30px line, each clipped element one line of `X` glyphs with `white-space: nowrap`):

- `text-clipped-bug.html`: `#badge` (first in the document, 10 glyphs in a 196px box, `overflow-x: hidden`) and `[data-testid="hero-title"]` (an `h1`, 10 glyphs in a 150px box at x 40, y 120, `overflow-x: hidden`).
- `text-clipped-clean.html`: the near-misses of DVB-24 to DVB-33 and DVB-69, one element each.
- `text-clipped-bounds.html`: 10 glyphs in boxes of 199px (`#over-1`), 198px (`#over-2`), 193px (`#over-7`) and 192px (`#over-8`), plus `#clip` (150px box, `overflow-x: clip`) and `#moved` (150px box, `overflow-x: hidden`, absolutely positioned at left 40px, top 400px, with `transform: translate(30px, 10px)`).
- `selectors.html`: one clipped element per selector case of DVB-34 to DVB-42, each with its own number of glyphs, plus `#long` and `#spaced` (DVB-16, DVB-17) and one element per bound of the Assumptions on selectors and excerpts: exactly 40 glyphs, ids of three and of two digits, an id that needs escaping, a `data-testid` repeated inside the shadow root, and the same path under two sibling containers.
- `text-clipped-strip.html`: three elements that pin where the cut is looked for (Assumptions: pixel confirmation): `#bordered` (borders on the left, top and bottom, blank overflow, no Finding), `#right-border` (a 30px right border, one Finding), `#narrow` (a 10px box showing no ink, no Finding), `#gap-at-edge` (the edge falls in a space between glyphs, one Finding) and `#two-colours` (transparent text over two flat bands, one Finding).
- `many.html`: seven clipped elements, each in its own text colour: `#small` first (4px cut), then `#m1` to `#m6` (50px cut each).
- `responsive.html`: `#fixed` (10 glyphs in a 150px box) then `#half` (10 glyphs in a box of `width: 50vw`).

---

## User Stories

### P1: Run Checks on a page ⭐ MVP

**User Story**: As a coding agent, I want `detect_visual_bugs` to run Checks against a page and return Findings, so that I learn what is visually wrong without a baseline.

**Why P1**: It is the slice's deliverable: the full Capture → Check → Finding[] flow.

**Acceptance Criteria**:

1. WHEN an MCP client lists tools THEN the server SHALL return exactly three tools, named `ping`, `inspect_element` and `detect_visual_bugs`. <!-- DVB-01 -->
2. The `detect_visual_bugs` tool SHALL declare the annotations `readOnlyHint: true` and `openWorldHint: true`. <!-- DVB-02 -->
3. The `detect_visual_bugs` tool SHALL declare an input schema whose properties are exactly `url`, `viewports` and `checks`, with `url` of type string and required, `viewports` not required and accepting an array of viewport objects or null, and `checks` not required and accepting an array of strings or null. <!-- DVB-03 -->
4. WHEN `detect_visual_bugs` succeeds THEN the server SHALL return `isError: false` and structured content whose keys are exactly `findings` and `captures`. <!-- DVB-04 -->
5. WHEN `detect_visual_bugs` succeeds THEN each entry of `captures` SHALL have exactly the keys `viewport` and `stabilized`. <!-- DVB-05 -->
6. WHEN `detect_visual_bugs` is called without `viewports` THEN `captures` SHALL equal `[{"viewport": {"width": 1440, "height": 900}, "stabilized": true}]` for a page that goes idle. <!-- DVB-06 -->
7. WHEN `detect_visual_bugs` is called with `viewports` or `checks` explicitly set to `null` THEN the server SHALL return the same structured content as when that parameter is omitted. <!-- DVB-07 -->
8. WHEN `detect_visual_bugs` is called on `text-clipped-bug.html` without `checks` THEN `findings` SHALL hold exactly 2 Findings, each with `check` equal to `text-clipped`. <!-- DVB-08 -->
9. WHEN `detect_visual_bugs` is called on `text-clipped-bug.html` with `checks` set to `["text-clipped"]` THEN the server SHALL return the same structured content as when `checks` is omitted. <!-- DVB-09 -->
10. WHEN `detect_visual_bugs` is called on `text-clipped-clean.html` THEN the server SHALL return `isError: false`, `findings` equal to `[]`, no image content block and one text block equal to `No findings in 1 viewport.` <!-- DVB-10 -->
11. WHEN `detect_visual_bugs` is called on `text-clipped-bug.html` THEN the first content block SHALL be a text block equal to `Found 2 findings in 1 viewport: 1 major, 1 minor.` <!-- DVB-11 -->
12. WHEN `detect_visual_bugs` is called twice with the same arguments on `text-clipped-bug.html` THEN both calls SHALL return equal structured content. <!-- DVB-12 -->

**Independent Test**: Call `detect_visual_bugs` on the `text-clipped` fixture pair over `file://` through the in-memory client and compare the structured content and content blocks.

---

### P1: Read a Finding

**User Story**: As a coding agent, I want each Finding to name its Check, element, measurements and evidence in a fixed shape, so that I can verify the claim and locate the element.

**Why P1**: The Finding is the output contract every later Check reuses.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` returns a Finding THEN its keys SHALL be exactly `check`, `category`, `severity`, `message`, `selector`, `text`, `box`, `viewport`, `evidence`, `suggestion` and `source`, and the keys of `evidence` SHALL be exactly `computed`, `measured` and `cropIndex`. <!-- DVB-13 -->
2. WHEN `detect_visual_bugs` is called on `text-clipped-bug.html` THEN `findings[0]` SHALL equal `{"check": "text-clipped", "category": "visual-bug", "severity": "major", "message": "Text clipped by 50px by its container width", "selector": "[data-testid=\"hero-title\"]", "text": "XXXXXXXXXX", "box": {"x": 40, "y": 120, "w": 150, "h": 30}, "viewport": {"width": 1440, "height": 900}, "evidence": {"computed": {"overflow-x": "hidden", "white-space": "nowrap", "text-overflow": "clip", "width": "150px", "font-size": "20px"}, "measured": {"overflowPx": 50, "scrollWidth": 200, "clientWidth": 150}, "cropIndex": 0}, "suggestion": "Allow wrapping or reduce font-size at this width", "source": "Squint heuristic"}`. <!-- DVB-14 -->
3. WHEN `detect_visual_bugs` returns several Findings THEN they SHALL be ordered by severity (`critical`, `major`, `minor`, `info`), then by the order the viewports were requested, then by document order; on `text-clipped-bug.html` the `major` Finding of the `h1` SHALL precede the `minor` Finding of `#badge`, which comes first in the document. <!-- DVB-15 -->
4. WHEN the element's text, with runs of whitespace collapsed to one space and trimmed, is longer than 40 characters THEN `text` SHALL be its first 39 characters followed by `…`; `#long` in `selectors.html`, holding 60 glyphs, SHALL have a `text` of 39 `X` and `…`. <!-- DVB-16 -->
5. WHEN the element's text holds line breaks or repeated spaces THEN `text` SHALL carry single spaces in their place; `#spaced` in `selectors.html`, holding `XXXXX`, a line break and several spaces, then `XXXXX`, SHALL have `text` equal to `XXXXX XXXXX`. <!-- DVB-17 -->
6. WHEN the `selector` of any Finding is passed to `inspect_element` with the same `url` and `viewport` THEN `inspect_element` SHALL return `isError: false` with a `box` equal to the Finding's `box`; this SHALL hold for every Finding of `text-clipped-bug.html` and `selectors.html`. <!-- DVB-18 -->

**Independent Test**: Compare `findings[0]` of `text-clipped-bug.html` with the literal above, then feed each `selector` back to `inspect_element`.

---

### P1: Detect clipped text

**User Story**: As a front-end developer, I want Squint to report text cut off by its own box and stay silent on text that fits, so that I can trust a Finding when I see one.

**Why P1**: The first Check, and the proof that DOM data and pixels are crossed in a Finding.

**Acceptance Criteria**:

1. WHEN an element has a non-whitespace text node as a direct child, `overflow-x: hidden`, `scrollWidth - clientWidth` of at least 2 and a painted cut (Assumptions: pixel confirmation) THEN the `text-clipped` Check SHALL return exactly one Finding for that element. <!-- DVB-19 -->
2. WHEN an element meets DVB-19 with `overflow-x: clip` in place of `hidden` (`#clip` in `text-clipped-bounds.html`) THEN the `text-clipped` Check SHALL return one Finding for it with `evidence.computed["overflow-x"]` equal to `clip`. <!-- DVB-20 -->
3. WHEN `overflowPx` is 8 or more THEN the Finding SHALL have `severity` equal to `major`; `#over-8` in `text-clipped-bounds.html` SHALL be `major` with `overflowPx` equal to 8. <!-- DVB-21 -->
4. WHEN `overflowPx` is between 2 and 7 THEN the Finding SHALL have `severity` equal to `minor`; `#over-7` and `#over-2` in `text-clipped-bounds.html` SHALL be `minor` with `overflowPx` equal to 7 and 2. <!-- DVB-22 -->
5. IF `scrollWidth - clientWidth` is 1 (`#over-1` in `text-clipped-bounds.html`) THEN the `text-clipped` Check SHALL return no Finding for that element, so that the fixture yields exactly 5 Findings. <!-- DVB-23 -->
6. IF the text is exactly as wide as its box (`#fits` in `text-clipped-clean.html`, 200px of glyphs in a 200px box with `overflow-x: hidden`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-24 -->
7. IF the text wraps inside a box with `overflow-x: hidden` and `white-space: normal` (`#wraps`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-25 -->
8. IF the text overflows a box with `overflow-x: visible` (`#visible`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-26 -->
9. IF the text overflows a box with `overflow-x: auto` (`#scrolls`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-27 -->
10. IF the element has `text-overflow: ellipsis` (`#ellipsis`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-28 -->
11. IF the element is hidden with the screen-reader-only pattern, a 1×1px box with `overflow: hidden` and `clip-path: inset(50%)` (`#sr-only`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-29 -->
12. IF the element has `visibility: hidden` (`#invisible`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-30 -->
13. IF only whitespace overflows, 5 glyphs followed by 10 spaces kept by `white-space: pre` in a 150px box (`#blank-tail`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-31 -->
14. IF the box with `overflow-x: hidden` holds no text node of its own and the overflowing text belongs to a child with `overflow-x: visible` (`#ancestor`) THEN the `text-clipped` Check SHALL return no Finding for either element. <!-- DVB-32 -->
15. IF the element has `direction: rtl` (`#rtl`) THEN the `text-clipped` Check SHALL return no Finding for it. <!-- DVB-33 -->
16. IF the element is painted at a size that differs from its layout size by 1px or more in width or in height THEN the `text-clipped` Check SHALL return no Finding for it; this SHALL hold in `text-clipped-clean.html` for `#scaled` (`transform: scale(1.5)`), `#stretched` (`transform: scaleY(2)`, width unchanged), `#widened` (`transform: scaleX(1.5)`, height unchanged), `#turned` (`transform: rotate(90deg)`) and `#in-scaled` (no transform of its own, inside a parent with `transform: scale(0.5)`), each of which overflows its 150px box by 50px. <!-- DVB-69 -->
17. WHEN an element that meets DVB-19 is moved by a transform that keeps its size (`#moved` in `text-clipped-bounds.html`) THEN the `text-clipped` Check SHALL return one Finding for it with `box` equal to `{"x": 70, "y": 410, "w": 150, "h": 30}` and `evidence.measured.overflowPx` equal to 50. <!-- DVB-70 -->

**Independent Test**: Call `detect_visual_bugs` on `text-clipped-bug.html`, `text-clipped-clean.html` and `text-clipped-bounds.html` and compare the Findings.

---

### P1: Stable selectors

**User Story**: As a coding agent, I want each Finding to carry a selector that is unique on the page and prefers stable attributes, so that I can find the element in source and re-inspect it.

**Why P1**: A Finding that cannot be located cannot be fixed.

**Acceptance Criteria** (every element below is in `selectors.html` and is reported by `text-clipped`):

1. WHEN the element has a `data-testid` that no other element shares, and also an `id` THEN `selector` SHALL be `[data-testid="save"]`. <!-- DVB-34 -->
2. WHEN the element's `data-testid` is shared by another element and its `id` is `first-row` THEN `selector` SHALL be `#first-row`. <!-- DVB-35 -->
3. WHEN the element is a `button` whose only `id` is `:r1:` and whose `aria-label` is `Close dialog` THEN `selector` SHALL be `button[aria-label="Close dialog"]`. <!-- DVB-36 -->
4. WHEN the element's `id` is `item-48213` and it has `role="tab"` and `aria-label="Settings"` THEN `selector` SHALL be `[role="tab"][aria-label="Settings"]`. <!-- DVB-37 -->
5. WHEN the element shares its `id` with another element and has no `data-testid` or `aria-label` THEN `selector` SHALL be its CSS path, `body > main > p:nth-of-type(2)`. <!-- DVB-38 -->
6. WHEN two `button` elements share the same `aria-label` and have no `data-testid` or `id` THEN the `selector` of each SHALL be its CSS path, and the two SHALL differ. <!-- DVB-39 -->
7. WHEN the element has none of those attributes and is the only `h2` among its siblings THEN `selector` SHALL be `body > main > h2`, with no `:nth-of-type`. <!-- DVB-40 -->
8. WHEN the element is an `h3` inside the open shadow root of a host whose selector is `[data-testid="card"]`, and has no attributes of its own THEN `selector` SHALL be `[data-testid="card"] > h3`. <!-- DVB-41 -->
9. WHEN the element's `data-testid` is `say "hi"` THEN `selector` SHALL be `[data-testid="say \"hi\""]`. <!-- DVB-42 -->

**Independent Test**: Call `detect_visual_bugs` on `selectors.html` and compare each Finding's `selector`, matched to its element by `text`.

---

### P1: Bounded crops

**User Story**: As a coding agent, I want at most five crops per call, given to the most severe Findings, so that one call never floods my context and never costs me a Finding.

**Why P1**: The roadmap lists the crop limit as part of the slice.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` returns N Findings THEN the response SHALL carry one text block followed by exactly min(N, 5) image content blocks of MIME type `image/png`. <!-- DVB-43 -->
2. WHEN `detect_visual_bugs` is called on `many.html` THEN `findings` SHALL hold 7 Findings whose `evidence.cropIndex` values are, in order, `0`, `1`, `2`, `3`, `4`, `null`, `null`, the last Finding being the `minor` one of `#small`. <!-- DVB-44 -->
3. WHEN a Finding has a non-null `cropIndex` THEN the image at that index SHALL be the crop of that Finding's box: on `many.html` each of the five images SHALL be 182×62 px (a 150×30 box plus 16px on each side) and SHALL show, at offset (20, 31), the text colour of its own Finding's element. <!-- DVB-45 -->

**Independent Test**: Call `detect_visual_bugs` on `many.html`, count the image blocks and decode each one.

---

### P1: Several viewports

**User Story**: As a coding agent, I want to pass several viewports in one call, so that I can examine desktop and mobile together.

**Why P1**: The roadmap puts one Capture per viewport in the slice.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `responsive.html` with `viewports` set to `[{"width": 1440, "height": 900}, {"width": 390, "height": 844}]` THEN `captures` SHALL hold two entries with those viewports in that order, and `findings` SHALL hold exactly 3 Findings: `#fixed` at 1440×900 (`major`), `#fixed` at 390×844 (`major`), `#half` at 390×844 (`minor`, `overflowPx` equal to 5), in that order, with the text block `Found 3 findings in 2 viewports: 2 major, 1 minor.` <!-- DVB-46 -->
2. IF a page does not reach network idle within 3 seconds (`polling.html`) THEN `detect_visual_bugs` SHALL return `isError: false` with `captures[0].stabilized` equal to `false`. <!-- DVB-47 -->
3. WHEN `viewports` holds the same viewport twice THEN `captures` SHALL hold it once and `findings` SHALL equal those of a call with that viewport given once. <!-- DVB-48 -->
4. WHEN `checks` holds the same name twice THEN `findings` SHALL equal those of a call with that name given once. <!-- DVB-49 -->

**Independent Test**: Call `detect_visual_bugs` on `responsive.html` with two viewports and compare `captures` and `findings`.

---

### P1: Clear errors

**User Story**: As a coding agent, I want a clear error for each way a call can fail, so that I can correct the call or tell a broken page from a clean one.

**Why P1**: The roadmap names the unknown-Check error; the rest keeps the new tool as strict as `inspect_element`.

**Acceptance Criteria**:

1. IF `checks` holds a name that is not a Check THEN the server SHALL return `isError: true` with a text block containing `Unknown check "nope". Valid checks: text-clipped.` (for `["nope"]`). <!-- DVB-50 -->
2. IF `checks` holds an unknown name WHILE Chromium cannot be launched THEN the server SHALL return the unknown-Check error of DVB-50, not the Chromium error. <!-- DVB-51 -->
3. IF `checks` is an empty list THEN the server SHALL return `isError: true` with a text block that names `checks`. <!-- DVB-52 -->
4. IF `viewports` is an empty list THEN the server SHALL return `isError: true` with a text block that names `viewports`. <!-- DVB-53 -->
5. IF a viewport's `width` or `height` is less than 1 THEN the server SHALL return `isError: true` with a text block that names the offending field. <!-- DVB-54 -->
6. IF `detect_visual_bugs` is called without `url` THEN the server SHALL return `isError: true` with a text block that names `url`. <!-- DVB-55 -->
7. IF the URL scheme is not `http`, `https` or `file` THEN the server SHALL return `isError: true` with a text block containing `Unsupported URL scheme "ftp"; use http://, https:// or file://.` (for an `ftp://` URL). <!-- DVB-56 -->
8. IF the navigation fails THEN the server SHALL return `isError: true` with a text block containing `Could not load ` followed by the URL. <!-- DVB-57 -->
9. IF Chromium cannot be launched THEN the server SHALL return `isError: true` with a text block containing `Could not launch Chromium` and `playwright install chromium`. <!-- DVB-58 -->
10. IF a call, all its viewports together, has not finished within `config.TOTAL_TIMEOUT_S` seconds THEN the server SHALL return `isError: true` with a text block containing `Timed out after Ns` (as in CAP-35) no later than 1 second after the timeout elapses, and SHALL answer the next call on the same connection normally. <!-- DVB-59 -->

**Independent Test**: Call `detect_visual_bugs` with each bad input and compare `isError` and the text block.

---

### P2: Check contract, configuration and documents

**User Story**: As a contributor, I want a Check to be one module that turns a Capture into Findings, so that I can add one without touching browser code.

**Why P2**: Required by the slice and by ADR-0002; no user-facing behaviour depends on it.

**Acceptance Criteria**:

1. The `text-clipped` Check SHALL live in its own module under a Checks package and SHALL be a function that receives a Capture and returns a list of Findings. <!-- DVB-60 -->
2. The Capture module SHALL be the only module under `src/` that imports `playwright`. <!-- DVB-61 -->
3. The server SHALL resolve Check names through one registry, so that adding a Check is one new module and one registry entry. <!-- DVB-62 -->
4. The JavaScript that runs inside the page SHALL live in `.js` files, with no JavaScript function bodies in Python strings. <!-- DVB-63 -->
5. The `config` module SHALL define the crop limit (5), the text excerpt length (40), the minimum overflow (2px) and the `major` overflow threshold (8px), each with its source cited in a comment. <!-- DVB-64 -->
6. The project SHALL declare no dependency that slice 2 did not declare. <!-- DVB-65 -->
7. The tests of `inspect_element` SHALL pass without any change to their assertions other than the exact tool list of DVB-01. <!-- DVB-66 -->
8. The `Unreleased` section of `CHANGELOG.md` SHALL list the `detect_visual_bugs` tool and the `text-clipped` Check, and the tool table of `README.md` SHALL list `detect_visual_bugs`. <!-- DVB-67 -->
9. WHEN the Verifier reports PASS for this feature THEN `docs/ROADMAP.md` SHALL show slice 3 as `concluída` in both the table and the slice 3 section. <!-- DVB-68 -->

**Independent Test**: Read the Checks package, `config.py`, `pyproject.toml` and the documents; grep `src/` for `playwright` imports.

---

## Edge Cases

- WHEN a clipped element sits inside an open shadow root THEN the `text-clipped` Check SHALL report it (covered by DVB-41). <!-- DVB-41 -->
- IF only whitespace overflows THEN the `text-clipped` Check SHALL return no Finding (covered by DVB-31). <!-- DVB-31 -->
- WHEN a `data-testid` holds a double quote THEN the selector SHALL escape it (covered by DVB-42). <!-- DVB-42 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| DVB-01 | P1: Run Checks on a page | T2 | Implemented |
| DVB-02 | P1: Run Checks on a page | T2 | Implemented |
| DVB-03 | P1: Run Checks on a page | T2 | Implemented |
| DVB-04 | P1: Run Checks on a page | T2 | Implemented |
| DVB-05 | P1: Run Checks on a page | T2 | Implemented |
| DVB-06 | P1: Run Checks on a page | T2 | Implemented |
| DVB-07 | P1: Run Checks on a page | T2 | Implemented |
| DVB-08 | P1: Run Checks on a page | T2 | Implemented |
| DVB-09 | P1: Run Checks on a page | T2 | Implemented |
| DVB-10 | P1: Run Checks on a page | T3 | Implemented |
| DVB-11 | P1: Run Checks on a page | T2 | Implemented |
| DVB-12 | P1: Run Checks on a page | T2 | Implemented |
| DVB-13 | P1: Read a Finding | T2 | Implemented |
| DVB-14 | P1: Read a Finding | T6 | Implemented |
| DVB-15 | P1: Read a Finding | T2 | Implemented |
| DVB-16 | P1: Read a Finding | T2 | Implemented |
| DVB-17 | P1: Read a Finding | T2 | Implemented |
| DVB-18 | P1: Read a Finding | T6 | Implemented |
| DVB-19 | P1: Detect clipped text | T2 | Implemented |
| DVB-20 | P1: Detect clipped text | T2 | Implemented |
| DVB-21 | P1: Detect clipped text | T2 | Implemented |
| DVB-22 | P1: Detect clipped text | T2 | Implemented |
| DVB-23 | P1: Detect clipped text | T2 | Implemented |
| DVB-24 | P1: Detect clipped text | T3 | Implemented |
| DVB-25 | P1: Detect clipped text | T3 | Implemented |
| DVB-26 | P1: Detect clipped text | T3 | Implemented |
| DVB-27 | P1: Detect clipped text | T3 | Implemented |
| DVB-28 | P1: Detect clipped text | T3 | Implemented |
| DVB-29 | P1: Detect clipped text | T3 | Implemented |
| DVB-30 | P1: Detect clipped text | T3 | Implemented |
| DVB-31 | P1: Detect clipped text | T3 | Implemented |
| DVB-32 | P1: Detect clipped text | T3 | Implemented |
| DVB-33 | P1: Detect clipped text | T3 | Implemented |
| DVB-34 | P1: Stable selectors | T6 | Implemented |
| DVB-35 | P1: Stable selectors | T6 | Implemented |
| DVB-36 | P1: Stable selectors | T6 | Implemented |
| DVB-37 | P1: Stable selectors | T6 | Implemented |
| DVB-38 | P1: Stable selectors | T6 | Implemented |
| DVB-39 | P1: Stable selectors | T6 | Implemented |
| DVB-40 | P1: Stable selectors | T6 | Implemented |
| DVB-41 | P1: Stable selectors | T6 | Implemented |
| DVB-42 | P1: Stable selectors | T6 | Implemented |
| DVB-43 | P1: Bounded crops | T5 | Implemented |
| DVB-44 | P1: Bounded crops | T5 | Implemented |
| DVB-45 | P1: Bounded crops | T5 | Implemented |
| DVB-46 | P1: Several viewports | T2 | Implemented |
| DVB-47 | P1: Several viewports | T2 | Implemented |
| DVB-48 | P1: Several viewports | T7 | Implemented |
| DVB-49 | P1: Several viewports | T7 | Implemented |
| DVB-50 | P1: Clear errors | T8 | Implemented |
| DVB-51 | P1: Clear errors | T8 | Implemented |
| DVB-52 | P1: Clear errors | T8 | Implemented |
| DVB-53 | P1: Clear errors | T8 | Implemented |
| DVB-54 | P1: Clear errors | T8 | Implemented |
| DVB-55 | P1: Clear errors | T8 | Implemented |
| DVB-56 | P1: Clear errors | T8 | Implemented |
| DVB-57 | P1: Clear errors | T8 | Implemented |
| DVB-58 | P1: Clear errors | T8 | Implemented |
| DVB-59 | P1: Clear errors | T8 | Implemented |
| DVB-60 | P2: Check contract, configuration and documents | T2 | Implemented |
| DVB-61 | P2: Check contract, configuration and documents | T2 | Implemented |
| DVB-62 | P2: Check contract, configuration and documents | T2 | Implemented |
| DVB-63 | P2: Check contract, configuration and documents | T2 | Implemented |
| DVB-64 | P2: Check contract, configuration and documents | T1 | Implemented |
| DVB-65 | P2: Check contract, configuration and documents | Verifier | In Tasks |
| DVB-66 | P2: Check contract, configuration and documents | T2 | Implemented |
| DVB-67 | P2: Check contract, configuration and documents | T9 | Implemented |
| DVB-68 | P2: Check contract, configuration and documents | Closing step | In Tasks |
| DVB-69 | P1: Detect clipped text | T4 | Implemented |
| DVB-70 | P1: Detect clipped text | T2 | Implemented |

**Coverage:** 70 total, 68 mapped to tasks, DVB-65 checked by the Verifier from file evidence, DVB-68 a closing step.

**Verification method:** pytest through the in-memory MCP client for DVB-01 to DVB-59, DVB-69 and DVB-70; the Verifier checks DVB-60 to DVB-68 from file evidence.

---

## Success Criteria

- [ ] `uv run pytest` passes locally and in CI with real Chromium, with the `inspect_element` assertions untouched.
- [ ] `detect_visual_bugs` on the "bug" fixture returns the two planted Findings; on the "clean" fixture it returns none.
- [ ] Every Finding selector of the fixtures resolves to exactly one element in `inspect_element`.
- [ ] A call with seven Findings returns seven Findings and five images.
- [ ] Slice 3 reads `concluída` in `docs/ROADMAP.md`.
