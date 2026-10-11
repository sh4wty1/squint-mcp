# overlap Specification

Slice 8 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: the roadmap section "8. overlap", then [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0002, ADR-0003, the decisions AD-001 to AD-004 in [`.specs/STATE.md`](../../STATE.md) and the decisions of [`context.md`](context.md). Decisions made there are final and are not restated as open here. The specs of slices 3, 4, 6 and 7 stay in force except where this one says it supersedes a criterion.

Scope size: Complex. The Check needs facts the Capture does not hold (what is painted over a text and how much of the text it hides), and the roadmap left open which overlaps are meant. Design and Tasks both run.

## Problem Statement

A card that slides over a paragraph, a label pushed onto a price, two lines pulled into each other by a negative margin: the DOM is valid and the text cannot be read. A check of boxes alone cannot report this, because most boxes that intersect are meant to: the stretched link of a card, a closed menu, a badge. Squint holds the pixels, so it can say how much of a text is really hidden, and this slice settles which covers are meant and stay unreported.

## Goals

- [ ] `overlap` reports every planted problem of its "bug" fixture, text painted over text included, and nothing on its "clean" fixture, which holds the intended overlaps: a stretched link, closed and open menus, a tooltip, dialogs, a popover, `fixed` and `sticky` elements, a badge and a caption over a picture.
- [ ] A Finding states the share of the text that is hidden and names the element that covers it by a selector that works in `inspect_element`.
- [ ] The decision on false positives deferred since `.docs/START.md` is taken and held by fixtures.
- [ ] Slice 8 is marked done in `docs/ROADMAP.md` once verification passes.

## Terms

Used by the criteria below; each is defined once here.

- **Own text**: the text nodes that are direct children of an element (same reach as the other Checks).
- **Other element**, for an element: any element that is not the element, one of its ancestors or one of its descendants. The elements of a shadow tree have the host of that tree as an ancestor.
- **Seen**: a pixel of text ink is seen when the ink that shows on the page is at least half of the ink that pixel has when nothing outside the element is painted over it. The bound is relative to the pixel, so a veil gives the same answer on a full glyph and on an anti-aliased edge.
- **Text ink** of an element: the page pixels its own text covers by at least half when nothing outside the element is painted over it. Text that is clipped away, off the page, of `visibility: hidden` or faded below half by `opacity` has no Text ink.
- **Silent layer**: an element that declares itself a layer or stays in view while the page scrolls, together with its descendants. It is an element with a `role` attribute of `menu`, `listbox`, `tooltip`, `dialog` or `alertdialog`, a `dialog` element with the `open` attribute, an open popover, or an element whose computed `position` is `fixed` or `sticky`. A Silent layer that holds an element is not one for that element.
- **Hidden ink** of an element: its Text ink that is not seen in the Capture and that would be seen if, of everything outside the element, only its Silent layers were painted.
- **Hidden share**: Hidden ink divided by Text ink.
- **Coverer** of an element: of the Other elements that hit testing gives at its Hidden ink, the one it gives over the largest part of that ink; on a tie, the first of them in document order. Hit testing is what `document.elementFromPoint` answers, continued into open shadow roots, with the page scrolled so that the point is in the viewport; an element the scroll moved from where the Capture has it is passed over for the next one at the point. When a Capture has more than 20,000 pixels of Hidden ink to test, every nth pixel of every nth row is tested, and each element at least once: the largest part is then of that sample.
- **Raised layer**: a Coverer is in a Raised layer when it, or one of its ancestors that is not an ancestor of the covered element, has a computed `position` other than `static` and a computed `z-index` above 0.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Interaction states (hover, an opened modal, a focused control) | Roadmap, "Não entra". Squint sees the initial state of a page (ADR-0002) |
| Iframes | Roadmap, "Não entra" |
| Covered images, form controls and any element without own text | Decided with the maintainer (2026-10-10). A caption over a picture would make every picture a candidate |
| What a `fixed` or `sticky` element covers, including the top of a page under a fixed header that scrolling cannot uncover | Decided with the maintainer (2026-10-10). Banners and headers are everywhere and a Capture cannot tell which of them can be dismissed. Known limit of this Check |
| A cover that hit testing does not give (`pointer-events: none`, as on a fade over the end of a text) | The roadmap fixes the mechanism: `elementFromPoint`, confirmed in the pixels. Known limit of this Check |
| Text covered by one of its own descendants, or by something an ancestor paints (a pseudo-element of an ancestor) | A badge inside a button covers its parent on purpose. Known limit of this Check |
| A collision in which the text on top hides under 10% of the ink of the text below | Under the reporting threshold. A real-font collision measured 15% in the spike |
| Telling stacked slides or tab panels kept under the active one from a bug | They are reported, at a lower severity when the active one is in a Raised layer. No signal in a Capture separates them |
| A `z-index` that applies without `position`, as on a flex or grid item | Such a Coverer is not in a Raised layer and keeps the full severity. Known limit of this Check |
| More than one Coverer named in a Finding | `evidence.measured` holds numbers and strings, not lists |
| Any other Check, Profile, Audit, score, `compare_viewports` | Not in this slice |
| A parameter for thresholds or for the list of Silent layers | `docs/SPEC.md`: behaviour changes only through `url`, `viewports`, `checks` |
| Changes to the behaviour of `inspect_element` or `ping`, or to the Findings of the other three Checks | Earlier slices are closed. Two changes reach every Capture and are in scope: text is rasterized in grayscale, and a Capture settles the layout before it measures (issue #18). Neither changes a result of the existing fixtures (OVL-59) |
| Tests outside the MCP tool boundary | `docs/SPEC.md` Testing Decisions: one seam |
| Pushing the branch and opening the pull request | Remote actions; they need the maintainer's go-ahead |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

The maintainer accepted the spec on 2026-10-11, with the three changes the design asked for ("seen" relative to the pixel, grayscale text, hit testing with the page scrolled and capped): every default below is confirmed.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| What marks an overlap as meant | The Silent layers of the Terms stay unreported; everything else that hides text is reported; a Coverer in a Raised layer lowers the severity | Decided with the maintainer (2026-10-10) | y |
| Reach | Own text only | Decided with the maintainer (2026-10-10) | y |
| Text painted over text | Reported: the glyphs on top hide ink of the text below, so it needs no rule of its own | Decided with the maintainer (2026-10-10). The spike measured 15% hidden for two lines of a real font | y |
| `fixed` and `sticky` | Never reported as what covers a text | Decided with the maintainer (2026-10-10) | y |
| Where the Finding sits | On the covered element; the Coverer's selector is `evidence.measured.coveredBy` | Decided with the maintainer (2026-10-10). The harm is on the text that cannot be read | y |
| Severity by share | `major` or `minor` by the Hidden share | Decided with the maintainer (2026-10-10) | y |
| Reporting threshold | A Hidden share of at least 10%; the value lives in config | One glyph in a word of ten, the same share `low-contrast-real` takes as its worst part. The smallest real bug of the spike hid 13%, a badge 0% | y |
| `major` threshold | A Hidden share of at least 25%; the value lives in config | A quarter of a text gone leaves a sentence or a price unreadable; less than that costs a word | y |
| Severity under a Raised layer | One level lower: `major` becomes `minor`, `minor` becomes `info`. It is the first use of `info` | "Lower" has to hold for a small cover too. An element given a positive `z-index` was put on top on purpose more often than not, and the five crops of a call go to the Findings above it | y |
| A translucent veil | It hides the ink it lets less than half of through, and none of the ink it lets at least half of through | The same bound as `low-contrast-real`, so every text under a veil is judged by exactly one of the two Checks: the one that sees it, or the one that says it is covered. Refines "a veil is left to `low-contrast-real`", which holds for a veil that leaves the text seen | y |
| `alertdialog` | A Silent layer, with `dialog` | It is the same widget for this purpose; the decision named `dialog` | y |
| The `role` attribute | Compared whole, in lower case and trimmed; a list of several roles is not a Silent layer | The four roles are written alone in practice; a fallback list is rare | y |
| Popovers and modal dialogs | An open popover is a Silent layer whatever its `position`; a `dialog` opened as a modal is one by its `open` attribute | Both are layers by construction. The fixture gives its popover `position: absolute`, so the criterion does not pass by the `fixed` rule alone | y |
| A Silent layer around the covered element | Not a Silent layer for that element: a text covered by its neighbour inside one dialog or one fixed header is reported | The layer explains why the two are above the page, not why one is above the other | y |
| Several elements cover one text | One Finding: the Hidden share counts all of the Hidden ink; `coveredBy` and the Raised-layer rule read the Coverer of the Terms | A Finding is one element × one viewport × one Check (`docs/SPEC.md`) | y |
| Hit testing gives no Other element at the Hidden ink | No Finding | A Finding without `coveredBy` cannot be acted on, and the roadmap asks for both signals | y |
| Comparison and rounding | The unrounded Hidden share is compared with the thresholds; `hiddenPercent` is the share in percent, truncated to an integer (24.5% gives 24) | As in `low-contrast-real`: a reported value never contradicts the severity next to it | y |
| `evidence.measured` | Exactly `hiddenPercent` (integer) and `coveredBy` (a selector unique on the page, as `selector` is) | What an agent needs to act: how bad, and which element to move. The Coverer's styles are one `inspect_element` call away | y |
| `evidence.computed` | Exactly `position` and `z-index` of the covered element. `z-index` is a new property collected for a Capture; `inspect_element` does not return it | The styles of the covered element that decide what is painted above it | y |
| Message, suggestion, source, category | `"{hiddenPercent}% of the text is covered by another element"`, `"Move one of the two elements or give the text its own space"`, `"Squint heuristic"`, `visual-bug` | As `text-clipped`: no outside norm defines this | y |
| Text hidden on purpose | No Finding for text of `visibility: hidden`, of a glyph colour with alpha 0, or with no Text ink | It is not text a reader was meant to see | y |
| Unknown-Check message (supersedes the literal in force since slice 7) | `Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | Same rule, alphabetical; the list grew. It changes four assertions: `tests/test_detect_visual_bugs.py` lines 342, 352, 362 and 373 | y |
| Order of Findings | Unchanged: severity, then viewport, then document order of the element, then Check name | Settled in slice 4 (LCR-37 to LCR-39, LCR-53) | y |
| How the Capture learns Text ink, Hidden ink and the Coverer | On request, from screenshots in which the glyphs of chosen text nodes are repainted through CSS highlights, alone and as painted, and by hit testing: AD-005 and [`design.md`](design.md). Spiked against real Chromium on 2026-10-11: every case of this spec gives the value of its criterion | AD-003 says how a Check gets a new fact; ADR-0002 keeps the browser out of the Check | y |
| Text rasterization | Chromium is launched with `--disable-lcd-text`, so text is anti-aliased in grayscale in every Capture (AD-006) | With subpixel text the same glyph is rasterized differently alone and as painted: `#veil-55` measured 95% for 100%. The existing suite passes with the flag | y |
| The layout of a Capture | A Capture takes one small screenshot beyond the viewport before it measures anything (AD-006, issue #18) | On Windows that first screenshot changes the font of the generic `monospace` family and the page is laid out again: boxes read before it are off | y |
| Fixtures | Ahem at `font-size: 20px` and `line-height: 30px`, as in slice 4: ten glyphs are a block of 200 × 20 pixels of ink. A cover is an opaque box unless a criterion says otherwise, so every share is exact. No text of a fixture is covered by anything its criterion does not name | Exact shares need exact pixels | y |
| Criteria not observable through the tool boundary (OVL-61 to OVL-67) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam | y |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:**

- Input validation & bounds: OVL-55 (the list of valid Checks); OVL-60 (a page with many covered texts); no new parameter.
- Failure / partial-failure states: N/A because the Check adds no failure of its own; a Capture that fails still fails the call (AD-002), and the total timeout of a call stays the only clock (OVL-60).
- Idempotency / retry / duplicate handling: OVL-04.
- Auth boundaries & rate limits: N/A because the server is a local stdio process with no caller identity.
- Concurrency / ordering: OVL-02, OVL-52, OVL-57.
- Data lifecycle / expiry: N/A because a call keeps nothing: whatever the Capture changes on a page to measure it dies with the browser context of that call (AD-001), and OVL-59 holds that the other Checks read the same page as before.
- Observability: N/A because the slice adds no log line or metric; logs stay on stderr as set in slice 1.
- External-dependency failure: N/A because the Check calls nothing outside the Capture.
- State-transition integrity: N/A because a Check is a pure function of a Capture.

---

## User Stories

### P1: Report text that another element covers ⭐ MVP

**User Story**: As a front-end developer, I want Squint to report text that another element is painted over, so that I catch a card over a paragraph or two lines run into each other before users do.

**Why P1**: It is the Check.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN an element has Text ink, its Hidden share is at least 10% and it has a Coverer THEN the `overlap` Check SHALL return exactly one Finding for that element. <!-- OVL-01 -->
2. WHEN `detect_visual_bugs` is called on `overlap-bug.html` with `checks` equal to `["overlap"]` THEN the `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` of `findings` SHALL be, in this order, `(#half, major, 50, #half-cover)`, `(#quarter, major, 25, #quarter-cover)`, `(#corner, minor, 10, #corner-cover)` and `(#collision, minor, 20, #stray)`; the elements stand in the document as `#half` (a cover over the last 100px of its 200px of text), `#corner` (over the last 20px), `#quarter` (over the last 50px) and `#collision`. <!-- OVL-02 -->
3. WHEN `detect_visual_bugs` is called on `overlap-bug.html` without `checks` THEN the first content block SHALL be a text block equal to `Found 4 findings in 1 viewport: 2 major, 2 minor.` <!-- OVL-03 -->
4. WHEN `detect_visual_bugs` is called twice with the same arguments on `overlap-bug.html` THEN both calls SHALL return equal structured content. <!-- OVL-04 -->
5. WHEN the own text of an Other element that paints no background is painted over the Text ink of an element (`#stray` in `overlap-bug.html`, two glyphs over the third and fourth of the ten of `#collision`) THEN the Check SHALL return one Finding for the element underneath with `evidence.measured.hiddenPercent` equal to 20. <!-- OVL-05 -->
6. WHEN the own text of an element is painted over the text of another and none of its own Text ink is hidden (`#stray` in `overlap-bug.html`) THEN the Check SHALL return no Finding for it. <!-- OVL-06 -->
7. WHEN the Hidden ink is exactly 10% of the Text ink at the left edge of the text (`#left` in `overlap-bounds.html`: the first 20px of 200px) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10. <!-- OVL-07 -->
8. WHEN the Hidden ink is exactly 10% of the Text ink at the top edge of the text (`#top` in `overlap-bounds.html`: the first 2 rows of 20) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10. <!-- OVL-08 -->
9. WHEN the Hidden ink is exactly 10% of the Text ink at the bottom edge of the text (`#bottom` in `overlap-bounds.html`: the last 2 rows of 20) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10. <!-- OVL-09 -->
10. WHEN the own text of an element paints several boxes and the Hidden ink lies only in one that is neither the first nor the last (`#three-lines` in `overlap-bounds.html`: three lines of ten glyphs, a cover over 60px of the middle one) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10. <!-- OVL-10 -->
11. WHEN the own text of an element is several text nodes and the Hidden ink lies only in one that is not the first (`#split` in `overlap-bounds.html`: `XXXXX`, an empty `b`, `XXXXX`, a cover over the last 20px) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10. <!-- OVL-11 -->
12. WHEN an Other element with no text lets less than half of the ink of a text through (`#veil-55` in `overlap-bounds.html`, all of it under a layer of `rgba(255, 255, 255, 0.55)`) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 100 and `severity` equal to `major`. <!-- OVL-12 -->
13. WHEN an element in an open shadow tree is covered by an Other element of the same tree (`[data-testid="shadow-text"]` in the shadow tree of `#host` in `overlap-bounds.html`, the last 100px of its text under `[data-testid="shadow-cover"]`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `[data-testid="shadow-cover"]`. <!-- OVL-13 -->
14. WHEN `detect_visual_bugs` is called on `overlap-bug.html` with `viewports` of 1440 × 900 and 390 × 844 THEN `#narrow`, half of whose text is covered only while the viewport is at most 600px wide, SHALL get one Finding whose `viewport` is 390 × 844 and none whose `viewport` is 1440 × 900. <!-- OVL-14 -->
15. WHEN an element and the Other element that covers it are both inside one element with a `role` of `dialog` (`#in-dialog` in `overlap-bounds.html`, half covered) THEN the Check SHALL return one Finding for it with `severity` equal to `major`. <!-- OVL-15 -->
16. WHEN an element and the Other element that covers it are both inside one element of `position: fixed` (`#in-fixed` in `overlap-bounds.html`, half covered) THEN the Check SHALL return one Finding for it with `severity` equal to `major`. <!-- OVL-16 -->
17. WHEN `detect_visual_bugs` is called with `checks` equal to `["overlap"]` on `low-contrast-bounds.html` THEN `findings` SHALL hold exactly one Finding, on `#covered`, with `evidence.measured.hiddenPercent` equal to 100 and `severity` equal to `major`. <!-- OVL-17 -->
18. WHEN `detect_visual_bugs` is called with `checks` equal to `["overlap"]` on `low-contrast-reach.html` THEN `findings` SHALL hold exactly one Finding, on `#veiled-most` (under a layer of `rgba(255, 255, 255, 0.7)`), with `evidence.measured.hiddenPercent` equal to 100. <!-- OVL-18 -->

**Independent Test**: Call `detect_visual_bugs` on `overlap-bug.html` and read the four Findings, the collision among them.

---

### P1: Stay silent on overlaps that are meant

**User Story**: As a front-end developer, I want Squint not to report the overlaps a page is built with, so that I can trust a Finding when I see one.

**Why P1**: It is the decision the roadmap deferred to this slice. A Check that reports every card with a stretched link is switched off.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `overlap-clean.html` without `checks` THEN the server SHALL return `isError: false`, `findings` equal to `[]`, no image content block and one text block equal to `No findings in 1 viewport.` <!-- OVL-19 -->
2. IF hit testing gives an Other element over all the text of an element and that Other element paints nothing there (`#stretched` in `overlap-clean.html`, under the `::after` of a link stretched over its card with `position: absolute` and `inset: 0`) THEN the Check SHALL return no Finding for the element. <!-- OVL-20 -->
3. IF the Other element over a text has a computed `opacity` of 0 (`#under-faded` in `overlap-clean.html`, half under an opaque box of `opacity: 0`) THEN the Check SHALL return no Finding for the text. <!-- OVL-21 -->
4. IF an Other element with no text lets at least half of the ink of a text through (`#veil-45` in `overlap-clean.html`, all of it under a layer of `rgba(255, 255, 255, 0.45)`) THEN the Check SHALL return no Finding for the text. <!-- OVL-22 -->
5. IF the only element that hides ink of a text has a `role` attribute of `menu`, `listbox`, `tooltip`, `dialog` or `alertdialog` (`#under-menu`, `#under-listbox`, `#under-tooltip`, `#under-dialog` and `#under-alertdialog` in `overlap-clean.html`, each half covered by an element of one of those roles) THEN the Check SHALL return no Finding for the text. <!-- OVL-23 -->
6. IF the only element that hides ink of a text is a `dialog` element with the `open` attribute (`#under-open-dialog` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the text. <!-- OVL-24 -->
7. IF the only element that hides ink of a text is an open popover (`#under-popover` in `overlap-clean.html`, half covered by a popover of `position: absolute` that a script of the page shows on load) THEN the Check SHALL return no Finding for the text. <!-- OVL-25 -->
8. IF the only element that hides ink of a text has a computed `position` of `fixed` (`#under-fixed` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the text. <!-- OVL-26 -->
9. IF the only element that hides ink of a text has a computed `position` of `sticky` (`#under-sticky` in `overlap-clean.html`, half under a sticky element pulled over it by a negative margin) THEN the Check SHALL return no Finding for the text. <!-- OVL-27 -->
10. IF the only element that hides ink of a text is a descendant of an element with a `role` of `menu` and has no `role` itself (`#under-menu-item` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the text. <!-- OVL-28 -->
11. IF the only element that hides ink of a text is of `position: static` and a descendant of an element of `position: fixed` (`#under-fixed-child` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the text. <!-- OVL-29 -->
12. IF the only element that hides ink of a text is in the open shadow tree of a host with a `role` of `menu` (`#under-shadow-menu` in `overlap-bounds.html`) THEN the Check SHALL return no Finding for the text. <!-- OVL-30 -->
13. IF the Hidden share of an element is below 10% along the width of its text (`#nick` in `overlap-clean.html`: a cover over the last 19px of 200px, 9.5%) THEN the Check SHALL return no Finding for it. <!-- OVL-31 -->
14. IF the Hidden share of an element is below 10% along the height of its text (`#skim` in `overlap-clean.html`: a cover over the first row of 20, 5%) THEN the Check SHALL return no Finding for it. <!-- OVL-32 -->
15. IF the only element painted over the own text of an element is one of its descendants (`#parent-text` in `overlap-clean.html`, half of its own text under a child of `position: absolute`) THEN the Check SHALL return no Finding for the element. <!-- OVL-33 -->
16. IF the only element painted over a text has `pointer-events: none` (`#under-ghost` in `overlap-clean.html`, half covered) THEN the Check SHALL return no Finding for the text. <!-- OVL-34 -->
17. WHEN a text is painted over an element that holds no own text (`#caption` over `#picture` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the text and none for the element under it. <!-- OVL-35 -->
18. WHEN a badge is painted over a corner of the box of an element and over none of its Text ink (`#badge` on `#inbox` in `overlap-clean.html`) THEN the Check SHALL return no Finding for the element. <!-- OVL-36 -->
19. IF a covered text has `visibility: hidden` (`#hidden-text` in `overlap-clean.html`, half under a cover) THEN the Check SHALL return no Finding for it. <!-- OVL-37 -->
20. IF the glyphs of a covered text are painted with a colour of alpha 0 (`#transparent-text` in `overlap-clean.html`, `color: transparent`, half under a cover) THEN the Check SHALL return no Finding for it. <!-- OVL-38 -->
21. IF a covered text has a computed `opacity` of 0 (`#faded-text` in `overlap-clean.html`, half under a cover) THEN the Check SHALL return no Finding for it. <!-- OVL-39 -->

**Independent Test**: Call `detect_visual_bugs` on `overlap-clean.html` and get an empty list.

---

### P1: Severity

**User Story**: As a coding agent, I want the worst covers first and the likely intended ones last, so that the five crops of a call go where they help.

**Why P1**: Severity orders the Findings and decides which get a crop.

**Acceptance Criteria**:

1. WHEN the Hidden share of an element is at least 25% and its Coverer is in no Raised layer THEN its Finding SHALL have `severity` equal to `major`, and `minor` below 25%; `#quarter` in `overlap-bug.html` (25%) SHALL be `major` and `#almost-quarter` in `overlap-bounds.html` (a cover over the last 49px of 200px, 24.5%) SHALL be `minor`. <!-- OVL-40 -->
2. WHEN the Hidden share of an element is at least 25% and its Coverer has `position: absolute` and a `z-index` of 1 (`#layered-half` in `overlap-bounds.html`, half covered) THEN its Finding SHALL have `severity` equal to `minor`. <!-- OVL-41 -->
3. WHEN the Hidden share of an element is below 25% and its Coverer has `position: absolute` and a `z-index` of 1 (`#layered-corner` in `overlap-bounds.html`, a cover over the last 20px) THEN its Finding SHALL have `severity` equal to `info`. <!-- OVL-42 -->
4. WHEN the Coverer has no `z-index` and an ancestor of it that is not an ancestor of the covered element has `position: relative` and a `z-index` of 2 (`#layer-ancestor` in `overlap-bounds.html`, half covered) THEN the Finding SHALL have `severity` equal to `minor`. <!-- OVL-43 -->
5. WHEN the only element with a positive `z-index` around the Coverer is also an ancestor of the covered element (`#shared-layer` in `overlap-bounds.html`, half covered) THEN the Finding SHALL have `severity` equal to `major`. <!-- OVL-44 -->
6. WHEN the Coverer has `position: absolute` and a `z-index` of 0 (`#z-zero` in `overlap-bounds.html`, half covered) THEN the Finding SHALL have `severity` equal to `major`. <!-- OVL-45 -->
7. WHEN the Coverer has `position: static` and a `z-index` of 5 (`#z-static` in `overlap-bounds.html`, half of its text under the text of the next block, pulled up by a negative margin) THEN the Finding SHALL have `severity` equal to `major`. <!-- OVL-46 -->

**Independent Test**: The same half-covered text is `major` under a plain cover and `minor` under one with `z-index: 1`.

---

### P1: Read the Finding

**User Story**: As a coding agent, I want the Finding to say how much of the text is hidden and by which element, so that I can move the right one without measuring anything myself.

**Why P1**: A Finding that only says "something overlaps" sends the agent back to the page.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `overlap-bug.html` with `checks` equal to `["overlap"]` THEN the Finding of `#half` SHALL equal `{"check": "overlap", "category": "visual-bug", "severity": "major", "message": "50% of the text is covered by another element", "selector": "#half", "text": "XXXXXXXXXX", "box": {"x": 40, "y": 20, "w": 200, "h": 30}, "viewport": {"width": 1440, "height": 900}, "evidence": {"computed": {"position": "static", "z-index": "auto"}, "measured": {"hiddenPercent": 50, "coveredBy": "#half-cover"}, "cropIndex": 0}, "suggestion": "Move one of the two elements or give the text its own space", "source": "Squint heuristic"}`. <!-- OVL-47 -->
2. WHEN a Finding has an `evidence.measured.hiddenPercent` of 10 THEN its `message` SHALL equal `10% of the text is covered by another element` (`#corner` in `overlap-bug.html`). <!-- OVL-48 -->
3. WHEN the Hidden share is not a whole number of percent THEN `evidence.measured.hiddenPercent` SHALL be the share in percent truncated to an integer; `#almost-quarter` in `overlap-bounds.html` (24.5%) SHALL have 24. <!-- OVL-49 -->
4. WHEN a Silent layer and an Other element that is in no Silent layer hide different parts of one text (`#mixed` in `overlap-bounds.html`: `#mixed-menu`, of `role` `menu`, over its first 100px and `#mixed-card` over its last 40px) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 20, `evidence.measured.coveredBy` equal to `#mixed-card` and `severity` equal to `minor`. <!-- OVL-50 -->
5. WHEN two Other elements hide different shares of one text (`#two-covers` in `overlap-bounds.html`: `#small-cover`, first in the document, over its first 40px and `#large-cover` over its last 80px) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 60 and `evidence.measured.coveredBy` equal to `#large-cover`. <!-- OVL-51 -->
6. WHEN two Other elements hide equal shares of one text (`#tie` in `overlap-bounds.html`: `#tie-first`, first in the document, over its last 40px and `#tie-second` over its first 40px) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 40 and `evidence.measured.coveredBy` equal to `#tie-first`. <!-- OVL-52 -->
7. WHEN the `selector` or the `evidence.measured.coveredBy` of any Finding of `overlap-bug.html` or `overlap-bounds.html` is passed to `inspect_element` with the same `url` and `viewport` THEN `inspect_element` SHALL return `isError: false`, with a `box` equal to the Finding's `box` when it was passed the `selector`. <!-- OVL-53 -->

**Independent Test**: Read the Finding of `#half` and compare it with the literal above.

---

### P1: With the other Checks

**User Story**: As a coding agent, I want `overlap` to run with the other Checks in one call and in the same order of Findings, so that nothing about how I read a result changes.

**Why P1**: A fourth Check must not change what the first three report.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called without `checks` THEN the server SHALL run `low-contrast-real`, `offscreen-overflow`, `overlap` and `text-clipped`. <!-- OVL-54 -->
2. IF `checks` holds a name that is not a Check THEN the server SHALL return `isError: true` with a text block containing `Unknown check "nope". Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` (for `["nope"]`); this supersedes the literal in force since slice 7. <!-- OVL-55 -->
3. WHEN `detect_visual_bugs` is called with `checks` equal to `["low-contrast-real", "offscreen-overflow", "text-clipped"]` on `overlap-bug.html` THEN `findings` SHALL equal `[]`. <!-- OVL-56 -->
4. WHEN Findings of the same severity and viewport come from `overlap` and from another Check THEN they SHALL be ordered by the document order of their elements and, on one element, by Check name; on `overlap-order.html`, whose elements in document order are `#a` (a cover over its last 40px), `#b` (text of `rgb(119, 119, 119)` on white with a cover over its last 40px) and `#c` (a cover over its last 40px), all `minor`, the `(selector, check)` pairs of `findings` SHALL be `(#a, overlap)`, `(#b, low-contrast-real)`, `(#b, overlap)`, `(#c, overlap)`. <!-- OVL-57 -->
5. WHEN the tools are listed THEN the description of `detect_visual_bugs` SHALL name `overlap` and say that it reports text another element is painted over. <!-- OVL-58 -->
6. WHEN the tests of the earlier slices run after this slice THEN every test SHALL pass with no change other than the literal of OVL-55 in the four assertions of `tests/test_detect_visual_bugs.py` that hold it (lines 342, 352, 362 and 373 before this slice). <!-- OVL-59 -->
7. WHEN `detect_visual_bugs` is called with `checks` equal to `["overlap"]` on `overlap-many.html`, a page of 100 texts each half covered, THEN the server SHALL return `isError: false` and 100 Findings. <!-- OVL-60 -->

**Independent Test**: Call `detect_visual_bugs` on `overlap-order.html` and read the four pairs in order.

---

### P2: Check contract, configuration and documents

**User Story**: As the maintainer, I want the Check to follow the contract of slice 3 and its thresholds to be cited, so that the next Check is as cheap as this one should have been.

**Why P2**: Not observable by a client; required by the roadmap.

**Acceptance Criteria**:

1. The `overlap` Check SHALL be one module under `src/squint_mcp/checks/` holding a function from a Capture to a list of Findings, registered by name in `checks/__init__.py` (AD-003). <!-- OVL-61 -->
2. The modules under `src/squint_mcp/checks/` and `src/squint_mcp/vision.py` SHALL NOT import `playwright` (ADR-0002). <!-- OVL-62 -->
3. The `config` module SHALL hold the reporting threshold, the `major` threshold and the roles that make a Silent layer, each with a comment citing its source ("Squint default" with the reason, or WAI-ARIA for the roles). <!-- OVL-63 -->
4. The `overlap` module SHALL hold no literal of those thresholds or roles. <!-- OVL-64 -->
5. `CHANGELOG.md` SHALL list the `overlap` Check under the unreleased version, with its two thresholds, the lower severity under a Raised layer and what it does not report: Silent layers, `fixed` and `sticky` elements, and covers that paint nothing. <!-- OVL-65 -->
6. `README.md` SHALL name `overlap` among the Checks that `detect_visual_bugs` runs and give their number as four. <!-- OVL-66 -->
7. WHEN the Verifier's report is PASS THEN `docs/ROADMAP.md` SHALL show slice 8 as `concluída`, in the table and in its section, with a link to this feature's directory. <!-- OVL-67 -->

**Independent Test**: Read the files named above.

---

## Edge Cases

- WHEN `detect_visual_bugs` is called on `overlap-bug.html` with two viewports THEN each Finding of the first viewport SHALL have a Finding of the same `selector` and `check` in the second. <!-- OVL-68 -->
- IF hit testing gives an Other element only where the own text of an element is clipped away by an ancestor (`#in-scaled` in `text-clipped-clean.html`, with `#backdrop` behind the part of its text that is cut off) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` on that file SHALL return `findings` equal to `[]`. <!-- OVL-69 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| OVL-01 | P1: Report text that another element covers | T9 | Implemented |
| OVL-02 | P1: Report text that another element covers | T9 | Implemented |
| OVL-03 | P1: Report text that another element covers | T9 | Implemented |
| OVL-04 | P1: Report text that another element covers | T9 | Implemented |
| OVL-05 | P1: Report text that another element covers | T9 | Implemented |
| OVL-06 | P1: Report text that another element covers | T9 | Implemented |
| OVL-07 | P1: Report text that another element covers | T11 | Implemented |
| OVL-08 | P1: Report text that another element covers | T11 | Implemented |
| OVL-09 | P1: Report text that another element covers | T11 | Implemented |
| OVL-10 | P1: Report text that another element covers | T11 | Implemented |
| OVL-11 | P1: Report text that another element covers | T11 | Implemented |
| OVL-12 | P1: Report text that another element covers | T11 | Implemented |
| OVL-13 | P1: Report text that another element covers | T11 | Implemented |
| OVL-14 | P1: Report text that another element covers | T9 | Implemented |
| OVL-15 | P1: Report text that another element covers | T11 | Implemented |
| OVL-16 | P1: Report text that another element covers | T11 | Implemented |
| OVL-17 | P1: Report text that another element covers | T12 | Implemented |
| OVL-18 | P1: Report text that another element covers | T12 | Implemented |
| OVL-19 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-20 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-21 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-22 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-23 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-24 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-25 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-26 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-27 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-28 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-29 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-30 | P1: Stay silent on overlaps that are meant | T11 | Implemented |
| OVL-31 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-32 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-33 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-34 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-35 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-36 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-37 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-38 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-39 | P1: Stay silent on overlaps that are meant | T10 | Implemented |
| OVL-40 | P1: Severity | T11 | Implemented |
| OVL-41 | P1: Severity | T11 | Implemented |
| OVL-42 | P1: Severity | T11 | Implemented |
| OVL-43 | P1: Severity | T11 | Implemented |
| OVL-44 | P1: Severity | T11 | Implemented |
| OVL-45 | P1: Severity | T11 | Implemented |
| OVL-46 | P1: Severity | T11 | Implemented |
| OVL-47 | P1: Read the Finding | T9 | Implemented |
| OVL-48 | P1: Read the Finding | T9 | Implemented |
| OVL-49 | P1: Read the Finding | T11 | Implemented |
| OVL-50 | P1: Read the Finding | T11 | Implemented |
| OVL-51 | P1: Read the Finding | T11 | Implemented |
| OVL-52 | P1: Read the Finding | T11 | Implemented |
| OVL-53 | P1: Read the Finding | T11 | Implemented |
| OVL-54 | P1: With the other Checks | T9 | Implemented |
| OVL-55 | P1: With the other Checks | T9 | Implemented |
| OVL-56 | P1: With the other Checks | T9 | Implemented |
| OVL-57 | P1: With the other Checks | T12 | Implemented |
| OVL-58 | P1: With the other Checks | T9 | Implemented |
| OVL-59 | P1: With the other Checks | T12 | Implemented |
| OVL-60 | P1: With the other Checks | T12 | Implemented |
| OVL-61 | P2: Check contract, configuration and documents | T9 | Implemented |
| OVL-62 | P2: Check contract, configuration and documents | T7, T9 | Implemented |
| OVL-63 | P2: Check contract, configuration and documents | T3 | Implemented |
| OVL-64 | P2: Check contract, configuration and documents | T9 | Implemented |
| OVL-65 | P2: Check contract, configuration and documents | T13 | Pending |
| OVL-66 | P2: Check contract, configuration and documents | T13 | Pending |
| OVL-67 | P2: Check contract, configuration and documents | closing step | Pending |
| OVL-68 | Edge cases | T9 | Implemented |
| OVL-69 | Edge cases | T12 | Implemented |

**Coverage:** 69 total, 69 mapped to tasks, 0 unmapped. The Phase column names the task of [`tasks.md`](tasks.md).

---

## Success Criteria

- [ ] All 69 requirements verified by the Verifier, OVL-61 to OVL-67 from file evidence.
- [ ] The gate passes: typecheck, lint, format check and the whole test suite.
- [ ] The discrimination sensor leaves no surviving mutant in the Check, in what the Capture gains for it and in the rules of Silent and Raised layers.
