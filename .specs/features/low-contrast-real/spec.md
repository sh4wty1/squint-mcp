# low-contrast-real Specification

Slice 4 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: the roadmap section "4. low-contrast-real", then [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0002, ADR-0003, the decisions AD-001 to AD-003 in [`.specs/STATE.md`](../../STATE.md) and issue #8. Decisions made there are final and are not restated as open here. The spec of slice 3 ([`detect-visual-bugs-text-clipped`](../detect-visual-bugs-text-clipped/spec.md)) stays in force except where this one says it supersedes a criterion.

Scope size: Large. It adds a Check that needs a new fact from the Capture (where text is painted and what is painted behind it), a rule for a background that varies, and the order of Findings across two Checks. Design and Tasks both run.

## Problem Statement

Text over an image or a gradient can be unreadable while every DOM-only tool calls it fine, because they compare the text colour with the CSS `background-color` and not with what is painted. Squint already holds the pixels; this slice adds the Check that reads the background from them. It is also the second Check, so the order of Findings across Checks (issue #8) has to be settled here.

## Goals

- [ ] `low-contrast-real` reports every planted problem of its "bug" fixture, including text over a gradient whose `background-color` alone passes, and nothing on its "clean" fixture, including text over a gradient whose `background-color` alone fails.
- [ ] A Finding states the contrast ratio, the ratio required for that text size, the text colour and the background colour sampled from the pixels.
- [ ] Findings of two Checks come back in document order within a severity and a viewport, and the first five of that order get the crops (issue #8).
- [ ] Slice 4 is marked done in `docs/ROADMAP.md` once verification passes.

## Terms

Used by the criteria below; each is defined once here.

- **Own text**: the text nodes that are direct children of an element (same reach as `text-clipped`).
- **Text pixels** of an element: the page pixels where its own text paints ink that is seen on the page, that is, not clipped away and not covered by something painted above it.
- **Background** of a text pixel: the colour the page paints at that pixel when the text is not painted.
- **Text colour** at a text pixel: the element's computed `color`; when its alpha is below 1, that colour composited over the Background of the pixel.
- **Pixel contrast**: the WCAG 2.2 contrast ratio between the Text colour and the Background of one text pixel.
- **Worst-part contrast** of an element: the smallest value `v` such that at least 10% of its text pixels have a Pixel contrast of `v` or less. The **worst-part pixel** is a text pixel whose Pixel contrast is `v`.
- **Large text**: computed `font-size` of at least 24px, or of at least 18.66px with a computed `font-weight` of at least 700 (WCAG: 18pt, or 14pt bold).
- **Required ratio**: 3 for Large text, 4.5 for any other text (WCAG 2.2 SC 1.4.3).

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| axe-core, any other WCAG rule (SC 1.4.6 enhanced contrast, SC 1.4.11 non-text contrast) | Roadmap, "Não entra" |
| Any other Check, Profile, Audit, score | Not in this slice |
| Text of an element with `opacity` below 1, on itself or on an ancestor | The colour that reaches the screen depends on the group's own background, which the Capture does not hold. Staying silent costs a missed Finding; guessing costs a false one. Known limit of this Check |
| Text painted through `mix-blend-mode`, `filter`, `background-clip: text`, `-webkit-text-fill-color` or a gradient fill | The computed `color` is not the painted colour there. Not detected; a Finding on such text can carry a wrong ratio. Known limit of this Check |
| Text inside form controls (`input`, `textarea`, `select`), placeholders, `::before` / `::after` content | They hold no text node of the element |
| The WCAG exemptions of SC 1.4.3 (inactive controls, decoration, logotypes) | Not decidable from a Capture |
| A Finding per text node or per line | A Finding is one element × one viewport × one Check (`docs/SPEC.md`) |
| Changes to the behaviour of `inspect_element` or `ping` | Slices 1 and 2 are closed |
| A parameter for thresholds | `docs/SPEC.md`: behaviour changes only through `url`, `viewports`, `checks` |
| Tests outside the MCP tool boundary | `docs/SPEC.md` Testing Decisions: one seam |
| Closing issue #8 and pushing the branch | Remote actions; they need the maintainer's go-ahead |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Background that varies behind the text | The worst part decides: the Worst-part contrast is compared with the Required ratio | Decided with the maintainer (2026-10-08) | y |
| Severity | `major` when the Worst-part contrast is below 3, `minor` otherwise. Large text that fails is therefore always `major` | Decided with the maintainer (2026-10-08); 3:1 is WCAG's own floor | y |
| Size of "the worst part" | 10% of the text pixels; the share lives in config | One glyph in a word of ten. Small enough to catch a title that half disappears, large enough that a few stray pixels of a photo do not make a Finding | n |
| Text pixels and Background come from the pixels, not from the box | The Capture gains what the Check needs to know both (for instance a second pixel layer of the page without its text). The mechanism is a Design decision and is spiked there against real Chromium; if no mechanism gives the Terms above, this spec comes back for revision | Anti-aliased edges, clipped text and covered text make "the pixels inside the text's box" wrong as a background. Roadmap allows Capture changes "que o Check exigir"; AD-003 says how a Check gets a new fact | n |
| Text of the same colour as its Background | Reported, with a ratio of 1 (`major`), as long as it has text pixels | It is the worst contrast there is. Text hidden on purpose is caught by the rules on `visibility`, transparent `color`, `opacity` and clipping | n |
| `color` with alpha 0 | No Finding | Text replaced by an image is hidden on purpose | n |
| Comparison and rounding | The unrounded ratio is compared with the Required ratio; `contrastRatio` is the ratio truncated to two decimals (4.478 gives 4.47) | WCAG: a ratio is not rounded up to meet the threshold | n |
| `evidence.measured` values | `measured` accepts strings besides numbers, for the two colours. Adding a value type removes or renames nothing, so it is not breaking (`docs/SPEC.md`, Versioning) | The sampled background is the point of the Check and an agent needs it as data, not only inside `message` | n |
| Colour format | Lowercase `#rrggbb`, as `sampledColors` of `inspect_element` | One format across tools | n |
| `evidence.computed` for this Check | Exactly `color`, `background-color`, `background-image`, `font-size`, `font-weight` | The styles that explain the Finding; `background-color` next to the sampled colour shows what a DOM-only tool would have compared | n |
| Reach | Each element with own text is judged on its own text pixels with its own `color`; an element whose text is all inside children yields nothing itself | Same reach as `text-clipped`; one Finding per element | n |
| Order of Findings (supersedes the tie-break of DVB-15) | Severity, then the order the viewports were requested, then the document order of the element whatever the Check, then the Check name in alphabetical order | Issue #8. Alphabetical order makes the result independent of the order of `checks` | n |
| Unknown-Check message (supersedes the literal of DVB-50) | `Valid checks: low-contrast-real, text-clipped.` | Same rule as DVB-50, alphabetical; the list grew | n |
| Bold | `font-weight` of 700 or more | CSS: `bold` computes to 700 | n |
| Fixtures | Ahem at `font-size: 20px` and `line-height: 30px` unless a criterion gives another size, as in slice 3: ten glyphs are a block of 200 × 20 text pixels with no anti-aliasing. Bands of background are hard-stop gradients, so every share of pixels is exact | Exact ratios need exact pixels | n |
| New dependencies (`numpy`, `coloraide`) | Decided at Design | `docs/SPEC.md` names both; whether this Check needs them is not a requirement | n |
| Criteria not observable through the tool boundary (LCR-40 to LCR-46) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam | n |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:**

- Concurrency / ordering: LCR-30 to LCR-33.
- Idempotency / retry: LCR-04.
- Failure / partial-failure states: N/A because the Check adds no failure of its own; a Capture that fails still fails the call (AD-002, DVB-56 to DVB-59).
- Input validation & bounds: LCR-34 to LCR-36; no new parameter.
- Remaining dimensions (auth, data lifecycle, observability, external dependency, state transitions): N/A because the Check is a pure function of a Capture.

---

## User Stories

### P1: Detect text with low real contrast ⭐ MVP

**User Story**: As a front-end developer, I want Squint to report text whose contrast against the painted background is below the WCAG threshold, so that I catch unreadable text over images and gradients that DOM-only tools miss.

**Why P1**: It is the Check that shows what Squint does that others do not.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN an element has text pixels and its Worst-part contrast is below its Required ratio THEN the `low-contrast-real` Check SHALL return exactly one Finding for that element. <!-- LCR-01 -->
2. WHEN `detect_visual_bugs` is called on `low-contrast-bug.html` with `checks` equal to `["low-contrast-real"]` THEN `findings[0]` SHALL be on `[data-testid="hero"]`, white text of 20px whose `background-color` is `rgb(0, 0, 0)` and whose `background-image` paints `rgb(204, 204, 204)` behind the last 40px of its 200px of text, with `severity` equal to `major`, `evidence.measured.contrastRatio` equal to 1.6, `evidence.measured.sampledBackground` equal to `#cccccc` and `evidence.computed["background-color"]` equal to `rgb(0, 0, 0)`. <!-- LCR-02 -->
3. WHEN `detect_visual_bugs` is called on `low-contrast-bug.html` THEN the first content block SHALL be a text block equal to `Found 4 findings in 1 viewport: 1 major, 3 minor.` (`[data-testid="hero"]`, then `#flat`, `#alpha` and `#almost-large` in document order) <!-- LCR-03 -->
4. WHEN `detect_visual_bugs` is called twice with the same arguments on `low-contrast-bug.html` THEN both calls SHALL return equal structured content. <!-- LCR-04 -->
5. WHEN text of `rgb(119, 119, 119)` and 20px is painted on a flat `rgb(255, 255, 255)` (`#flat` in `low-contrast-bug.html`) THEN the Check SHALL return one Finding for it with `severity` equal to `minor`. <!-- LCR-05 -->
6. WHEN the `color` of an element has an alpha below 1 and above 0 THEN the Check SHALL use that colour composited over the Background; `#alpha` in `low-contrast-bug.html`, `rgba(0, 0, 0, 0.5)` on white, SHALL get one Finding with `evidence.measured.textColor` equal to `#808080` and `evidence.measured.contrastRatio` equal to 3.94. <!-- LCR-06 -->
7. WHEN the low-contrast Background lies behind exactly 10% of the text pixels at the right edge of the text (`#right` in `low-contrast-bounds.html`: the last 20px of 200px) THEN the Check SHALL return one Finding for the element. <!-- LCR-07 -->
8. WHEN the low-contrast Background lies behind exactly 10% of the text pixels at the bottom edge of the text (`#bottom` in `low-contrast-bounds.html`: the last 2 rows of 20) THEN the Check SHALL return one Finding for the element. <!-- LCR-08 -->
9. WHEN text has the same colour as its Background and is not hidden by any rule of the next story (`#same` in `low-contrast-bounds.html`, `rgb(255, 255, 255)` on white) THEN the Check SHALL return one Finding for it with `severity` equal to `major` and `evidence.measured.contrastRatio` equal to 1. <!-- LCR-09 -->
10. WHEN a parent and its child both hold own text and only the child's text is below its Required ratio (`#nested` in `low-contrast-bounds.html`) THEN the Check SHALL return one Finding, on the child. <!-- LCR-10 -->

**Independent Test**: Call `detect_visual_bugs` on `low-contrast-bug.html` and see the gradient case reported with the colour sampled from the gradient.

---

### P1: Stay silent when the text can be read

**User Story**: As a front-end developer, I want Squint not to report text that has adequate real contrast, so that I can trust a Finding when I see one.

**Why P1**: A Check that cries wolf is switched off.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `low-contrast-clean.html` THEN the server SHALL return `isError: false`, `findings` equal to `[]`, no image content block and one text block equal to `No findings in 1 viewport.` <!-- LCR-11 -->
2. WHEN text of `rgb(118, 118, 118)` and 20px is painted on a flat `rgb(255, 255, 255)` (ratio 4.54; `#flat` in `low-contrast-clean.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-12 -->
3. WHEN white text has a `background-color` of `rgb(255, 255, 255)` and a `background-image` that paints `rgb(0, 0, 0)` behind all of it (`#gradient` in `low-contrast-clean.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-13 -->
4. WHEN the low-contrast Background lies behind less than 10% of the text pixels at the left edge of the text (`#left` in `low-contrast-bounds.html`: the first 19px of 200px) THEN the Check SHALL return no Finding for the element. <!-- LCR-14 -->
5. WHEN the low-contrast Background lies behind less than 10% of the text pixels at the top edge of the text (`#top` in `low-contrast-bounds.html`: the first row of 20) THEN the Check SHALL return no Finding for the element. <!-- LCR-15 -->
6. IF an element has `visibility: hidden` (`#hidden` in `low-contrast-bounds.html`, otherwise equal to `#flat` of the bug fixture) THEN the Check SHALL return no Finding for it. <!-- LCR-16 -->
7. IF the `color` of an element has an alpha of 0 (`#transparent` in `low-contrast-bounds.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-17 -->
8. IF an element has a computed `opacity` below 1 (`#faded` in `low-contrast-bounds.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-18 -->
9. IF an ancestor of an element has a computed `opacity` below 1 (`#faded-child` in `low-contrast-bounds.html`) THEN the Check SHALL return no Finding for the element. <!-- LCR-19 -->
10. IF all the own text of an element is clipped away (`#clipped-away` in `low-contrast-bounds.html`: a 1px × 1px box with `overflow: hidden` whose text starts outside it) THEN the Check SHALL return no Finding for it. <!-- LCR-20 -->
11. IF all the own text of an element is covered by an opaque element painted above it (`#covered` in `low-contrast-bounds.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-21 -->
12. WHEN part of the own text of an element is clipped away and the low-contrast Background lies only behind the clipped part (`#clipped-part` in `low-contrast-bounds.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-22 -->
13. WHEN `detect_visual_bugs` is called with `checks` equal to `["low-contrast-real"]` on `text-clipped-bug.html` THEN `findings` SHALL equal `[]`. <!-- LCR-23 -->

**Independent Test**: Call `detect_visual_bugs` on `low-contrast-clean.html` and get an empty list.

---

### P1: Thresholds by text size and severity

**User Story**: As a front-end developer, I want the WCAG threshold that applies to the size of the text, so that large headings are not held to the ratio of body text.

**Why P1**: Without it every light heading is a false Finding.

**Acceptance Criteria**:

1. WHEN text of `rgb(148, 148, 148)` on white (ratio 3.03) has a `font-size` of 24px (`#large` in `low-contrast-clean.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-24 -->
2. WHEN the same text has a `font-size` of 23px (`#almost-large` in `low-contrast-bug.html`) THEN the Check SHALL return one Finding for it with `evidence.measured.requiredRatio` equal to 4.5 and `severity` equal to `minor`. <!-- LCR-25 -->
3. WHEN the same text has a `font-size` of 18.66px and a `font-weight` of 700 (`#large-bold` in `low-contrast-clean.html`) THEN the Check SHALL return no Finding for it. <!-- LCR-26 -->
4. WHEN the same text has a `font-size` of 18px and a `font-weight` of 700 (`#small-bold` in `low-contrast-bounds.html`) THEN the Check SHALL return one Finding for it with `evidence.measured.requiredRatio` equal to 4.5. <!-- LCR-27 -->
5. WHEN the same text has a `font-size` of 20px and a `font-weight` of 600 (`#semibold` in `low-contrast-bounds.html`) THEN the Check SHALL return one Finding for it with `evidence.measured.requiredRatio` equal to 4.5. <!-- LCR-28 -->
6. WHEN Large text of `rgb(153, 153, 153)` and 24px on white (ratio 2.84; `#large-low` in `low-contrast-bounds.html`) fails THEN the Check SHALL return one Finding for it with `evidence.measured.requiredRatio` equal to 3 and `severity` equal to `major`. <!-- LCR-29 -->
7. WHEN text of 20px and `rgb(149, 149, 149)` on white (ratio 2.99; `#below-floor` in `low-contrast-bounds.html`) fails THEN its Finding SHALL have `severity` equal to `major`, and the Finding of `#almost-large` (ratio 3.03) SHALL have `severity` equal to `minor`. <!-- LCR-47 -->

**Independent Test**: The same grey passes at 24px and fails at 23px.

---

### P1: Read the Finding

**User Story**: As a coding agent, I want the Finding to carry the ratio, the threshold and both colours, so that I can fix the colour without measuring anything myself.

**Why P1**: A Finding without the sampled colour is no better than a DOM-only one.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `low-contrast-bug.html` with `checks` equal to `["low-contrast-real"]` THEN the Finding of `#flat` SHALL equal `{"check": "low-contrast-real", "category": "a11y", "severity": "minor", "message": "Text contrast 4.47:1 against the painted background #ffffff is below the 4.5:1 minimum", "selector": "#flat", "text": "XXXXXXXXXX", "box": {"x": 40, "y": 20, "w": 200, "h": 30}, "viewport": {"width": 1440, "height": 900}, "evidence": {"computed": {"color": "rgb(119, 119, 119)", "background-color": "rgba(0, 0, 0, 0)", "background-image": "none", "font-size": "20px", "font-weight": "400"}, "measured": {"contrastRatio": 4.47, "requiredRatio": 4.5, "textColor": "#777777", "sampledBackground": "#ffffff"}, "cropIndex": 1}, "suggestion": "Change the text colour or put a solid background behind the text to reach 4.5:1", "source": "WCAG 2.2 SC 1.4.3"}`. <!-- LCR-30 -->
2. WHEN the Required ratio of a Finding is 3 THEN its `message` SHALL end with `is below the 3:1 minimum` and its `suggestion` with `to reach 3:1`; the Finding of `#large-low` SHALL have a `message` equal to `Text contrast 2.84:1 against the painted background #ffffff is below the 3:1 minimum`. <!-- LCR-31 -->
3. WHEN the Background varies behind the text THEN `evidence.measured.sampledBackground` SHALL be the Background of the worst-part pixel and `evidence.measured.textColor` the Text colour at that pixel. <!-- LCR-32 -->
4. WHEN the `selector` of any Finding of `low-contrast-bug.html` or `low-contrast-bounds.html` is passed to `inspect_element` with the same `url` and `viewport` THEN `inspect_element` SHALL return `isError: false` with a `box` equal to the Finding's `box`. <!-- LCR-33 -->

**Independent Test**: Read the Finding of `#flat` and compare it with the literal above.

---

### P1: Two Checks in one call

**User Story**: As a coding agent, I want the Findings of all Checks in one predictable order, so that the crops go to the Findings I read first.

**Why P1**: Issue #8 has to be settled before a second Check merges.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called without `checks` THEN the server SHALL run `low-contrast-real` and `text-clipped`. <!-- LCR-34 -->
2. IF `checks` holds a name that is not a Check THEN the server SHALL return `isError: true` with a text block containing `Unknown check "nope". Valid checks: low-contrast-real, text-clipped.` (for `["nope"]`); this supersedes the literal of DVB-50. <!-- LCR-35 -->
3. WHEN `detect_visual_bugs` is called with `checks` equal to `["text-clipped"]` on `low-contrast-bug.html` THEN `findings` SHALL equal `[]`. <!-- LCR-36 -->
4. WHEN Findings of the same severity and viewport come from different Checks THEN they SHALL be ordered by the document order of their elements; on `checks-order.html`, whose elements in document order are `#a` (low contrast), `#b` (clipped), `#c` (clipped and low contrast), `#d` (clipped) and `#e` (low contrast), all `minor`, the `(selector, check)` pairs of `findings` SHALL be `(#a, low-contrast-real)`, `(#b, text-clipped)`, `(#c, low-contrast-real)`, `(#c, text-clipped)`, `(#d, text-clipped)`, `(#e, low-contrast-real)`. <!-- LCR-37 -->
5. WHEN two Checks report the same element at the same severity and viewport THEN the Finding whose `check` comes first in alphabetical order SHALL come first. <!-- LCR-38 -->
6. WHEN `detect_visual_bugs` is called on `checks-order.html` with `checks` equal to `["text-clipped", "low-contrast-real"]` THEN the structured content SHALL equal that of the call without `checks`. <!-- LCR-39 -->
7. WHEN `detect_visual_bugs` is called on `checks-order.html` THEN the response SHALL hold five image content blocks, the first five Findings of LCR-37 SHALL have `evidence.cropIndex` 0 to 4 in that order and the sixth SHALL have `null`. <!-- LCR-48 -->
8. WHEN the tools are listed THEN the description of `detect_visual_bugs` SHALL name both `text-clipped` and `low-contrast-real`. <!-- LCR-49 -->
9. WHEN the test suite of slice 3 runs after this slice THEN every test SHALL pass with no change other than the literal of LCR-35. <!-- LCR-50 -->

**Independent Test**: Call `detect_visual_bugs` on `checks-order.html` and read the six pairs in order.

---

### P2: Check contract, configuration and documents

**User Story**: As the maintainer, I want the Check to follow the contract of slice 3 and its thresholds to be cited, so that the next Check is as cheap as this one should have been.

**Why P2**: Not observable by a client; required by the roadmap.

**Acceptance Criteria**:

1. The `low-contrast-real` Check SHALL be one module under `src/squint_mcp/checks/` holding a function from a Capture to a list of Findings, registered by name in `checks/__init__.py` (AD-003). <!-- LCR-40 -->
2. The modules under `src/squint_mcp/checks/` and `src/squint_mcp/vision.py` SHALL NOT import `playwright` (ADR-0002). <!-- LCR-41 -->
3. The `config` module SHALL hold the two Required ratios, the two Large-text sizes, the bold weight, the `major` floor and the worst-part share, each with a comment citing its source (WCAG 2.2 SC 1.4.3 or "Squint default" with the reason). <!-- LCR-42 -->
4. The `low-contrast-real` module SHALL hold no literal of those thresholds. <!-- LCR-43 -->
5. `CHANGELOG.md` SHALL list the `low-contrast-real` Check, the string values of `evidence.measured` and the order of Findings across Checks under the unreleased version. <!-- LCR-44 -->
6. `README.md` SHALL name `low-contrast-real` as a Check that `detect_visual_bugs` runs. <!-- LCR-45 -->
7. WHEN the Verifier's report is PASS THEN `docs/ROADMAP.md` SHALL show slice 4 as `concluída`, in the table and in its section, with a link to this feature's directory. <!-- LCR-46 -->

**Independent Test**: Read the files named above.

---

## Edge Cases

- IF an element has own text but no text pixels (zero-size box, off the page, `display: none`) THEN the Check SHALL return no Finding for it. <!-- LCR-51 -->
- WHEN `detect_visual_bugs` is called on `low-contrast-bug.html` with two viewports THEN each Finding of the first viewport SHALL have a Finding of the same `selector` and `check` in the second. <!-- LCR-52 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| LCR-01 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-02 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-03 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-04 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-05 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-06 | P1: Detect text with low real contrast | T4 | Implemented |
| LCR-07 | P1: Detect text with low real contrast | - | Pending |
| LCR-08 | P1: Detect text with low real contrast | - | Pending |
| LCR-09 | P1: Detect text with low real contrast | - | Pending |
| LCR-10 | P1: Detect text with low real contrast | - | Pending |
| LCR-11 | P1: Stay silent when the text can be read | T4 | Implemented |
| LCR-12 | P1: Stay silent when the text can be read | T4 | Implemented |
| LCR-13 | P1: Stay silent when the text can be read | T4 | Implemented |
| LCR-14 | P1: Stay silent when the text can be read | - | Pending |
| LCR-15 | P1: Stay silent when the text can be read | - | Pending |
| LCR-16 | P1: Stay silent when the text can be read | - | Pending |
| LCR-17 | P1: Stay silent when the text can be read | - | Pending |
| LCR-18 | P1: Stay silent when the text can be read | - | Pending |
| LCR-19 | P1: Stay silent when the text can be read | - | Pending |
| LCR-20 | P1: Stay silent when the text can be read | - | Pending |
| LCR-21 | P1: Stay silent when the text can be read | - | Pending |
| LCR-22 | P1: Stay silent when the text can be read | - | Pending |
| LCR-23 | P1: Stay silent when the text can be read | T4 | Implemented |
| LCR-24 | P1: Thresholds by text size and severity | T4 | Implemented |
| LCR-25 | P1: Thresholds by text size and severity | T4 | Implemented |
| LCR-26 | P1: Thresholds by text size and severity | T4 | Implemented |
| LCR-27 | P1: Thresholds by text size and severity | - | Pending |
| LCR-28 | P1: Thresholds by text size and severity | - | Pending |
| LCR-29 | P1: Thresholds by text size and severity | - | Pending |
| LCR-30 | P1: Read the Finding | T4 | Implemented |
| LCR-31 | P1: Read the Finding | - | Pending |
| LCR-32 | P1: Read the Finding | T4 | Implemented |
| LCR-33 | P1: Read the Finding | T4 | Implemented |
| LCR-34 | P1: Two Checks in one call | T4 | Implemented |
| LCR-35 | P1: Two Checks in one call | T4 | Implemented |
| LCR-36 | P1: Two Checks in one call | T4 | Implemented |
| LCR-37 | P1: Two Checks in one call | - | Pending |
| LCR-38 | P1: Two Checks in one call | - | Pending |
| LCR-39 | P1: Two Checks in one call | - | Pending |
| LCR-40 | P2: Check contract, configuration and documents | T4 | Implemented |
| LCR-41 | P2: Check contract, configuration and documents | T3 | Implemented |
| LCR-42 | P2: Check contract, configuration and documents | T1 | Implemented |
| LCR-43 | P2: Check contract, configuration and documents | T4 | Implemented |
| LCR-44 | P2: Check contract, configuration and documents | - | Pending |
| LCR-45 | P2: Check contract, configuration and documents | - | Pending |
| LCR-46 | P2: Check contract, configuration and documents | - | Pending |
| LCR-47 | P1: Thresholds by text size and severity | - | Pending |
| LCR-48 | P1: Two Checks in one call | - | Pending |
| LCR-49 | P1: Two Checks in one call | T4 | Implemented |
| LCR-50 | P1: Two Checks in one call | T4 | Implemented |
| LCR-51 | Edge cases | - | Pending |
| LCR-52 | Edge cases | T4 | Implemented |

**Coverage:** 52 total, 0 mapped to tasks, 52 unmapped (Tasks has not run).

---

## Success Criteria

- [ ] All 52 requirements verified by the Verifier, LCR-40 to LCR-46 from file evidence.
- [ ] The gate passes: typecheck, lint, format check and the whole test suite.
- [ ] The discrimination sensor leaves no surviving mutant in the Check, the sampling code and the ordering of Findings.
