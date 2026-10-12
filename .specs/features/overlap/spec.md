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
- **Text ink** of an element: the page pixels its own text covers by at least half when nothing outside the element is painted over it. Text that is clipped away, off the page, of `visibility: hidden` or faded below half by `opacity` or by a `filter` has no Text ink.
- **Silent layer**: an element that declares itself a layer or stays in view while the page scrolls, together with its descendants. It is an element with a `role` attribute of `menu`, `listbox`, `tooltip`, `dialog` or `alertdialog`, a `dialog` element with the `open` attribute, an open popover, or an element whose computed `position` is `fixed` or `sticky`. A Silent layer that holds an element is not one for that element.
- **Hidden ink** of an element: its Text ink that is not seen in the Capture and that would be seen if, of everything outside the element, only its Silent layers were painted.
- **Hidden share**: Hidden ink divided by Text ink.
- **Coverer** of an element: of the Other elements that hit testing gives at its Hidden ink, the one it gives over the largest part of that ink; on a tie, the first of them in document order. Hit testing is what `document.elementFromPoint` answers, continued into open shadow roots, with the page scrolled so that the point is in the viewport; an element the scroll moved from where the Capture has it is passed over for the next one at the point. The Hidden ink to test is that of the elements whose Hidden share is at least 10%, those that get no Finding included; an element under that share is not hit tested and its Hidden ink does not count. When a Capture has more than 20,000 pixels of Hidden ink to test, every nth pixel of every nth row is tested, counted from the origin of the page (the pixels whose column and whose row on the page are both multiples of n, n being the smallest whole number for which the pixels of Hidden ink to test, divided by n × n, are at most 20,000), and each element at least once: the largest part is then of that sample.
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
| Text covered by a pseudo-element that is painted outside the box of its element and the boxes of that element's descendants, when an element that shows the pseudo-element (the one that paints it, or one that holds that one) is itself measured for covered text: it has own text, and what is not seen of that text, together with the glyphs of other texts that stand in its lines, comes to at least 10% of its ink | The two are measured in one screenshot unless a third text keeps them apart, and what the second shows hides the first there too: the first is measured with no Hidden ink and gets no Finding. With the pseudo-element inside the box of its element, or when no element that shows it is measured (OVL-111), the text is reported. Known limit of this Check ([`design.md`](design.md), Risks) |
| Text on an element with `mix-blend-mode`, or inside one | The colours that tell its glyphs from the rest of the page are blended with what is behind them. Under some modes (`difference` over white, for one) nothing of them is left: the text has no Text ink and gets no Finding. Known limit of this Check ([`design.md`](design.md), Risks) |
| A cover that changes the colours behind it with `backdrop-filter` | The text under it can still be read and is measured as not seen: it is reported, with that cover as `coveredBy`. A `filter` is another matter (Assumptions, "A `filter`"): it is on the text or around it, and its colour functions are left out when ink is measured. Known limit of this Check ([`design.md`](design.md), Risks) |
| A page that moves when it is scrolled (a header that shrinks, content that loads on scroll) | Hit testing scrolls the page to reach Hidden ink below or right of the viewport, after every pixel is read. `hiddenPercent` is not affected; `coveredBy` can name another element, or the Finding be missing, when what was over the text has moved. Known limit of this Check ([`design.md`](design.md), Risks) |
| A page whose Content Security Policy refuses inline styles | The styles a Capture injects, those of slice 4 included, are refused, and no text has ink for any Check: under `style-src file:` a page with a covered text and a text of low contrast comes back with no Finding (verified by the fourth validation pass). A follow-up outside this slice ([`design.md`](design.md), Risks) |
| A right-to-left page that scrolls sideways | The screenshot of such a page does not start where the boxes of its elements are counted from: every tool reads the wrong pixels there, `inspect_element` included, and a covered text gets no Finding. A right-to-left page that does not scroll sideways is measured as any other. Older than this slice. Known limit of the Capture; a follow-up outside this slice |
| A collision in which the text on top hides under 10% of the ink of the text below | Under the reporting threshold. A real-font collision measured 15% in the spike |
| Telling stacked slides or tab panels kept under the active one from a bug | They are reported, at a lower severity when the active one is in a Raised layer. No signal in a Capture separates them |
| A `z-index` that applies without `position`, as on a flex or grid item | Such a Coverer is not in a Raised layer and keeps the full severity. Known limit of this Check |
| More than one Coverer named in a Finding | `evidence.measured` holds numbers and strings, not lists |
| Any other Check, Profile, Audit, score, `compare_viewports` | Not in this slice |
| A parameter for thresholds or for the list of Silent layers | `docs/SPEC.md`: behaviour changes only through `url`, `viewports`, `checks` |
| Changes to the behaviour of `inspect_element` or `ping`, or to the Findings of the other three Checks | Earlier slices are closed. Three changes reach every Capture and are in scope: text is rasterized in grayscale, a Capture settles the layout before it measures (issue #18), and a Capture lets the page paint before every screenshot (AD-007). None changes a result of the existing fixtures (OVL-59) |
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
| Text hidden on purpose | No Finding for text of `visibility: hidden`, of a glyph colour with alpha 0, or with no Text ink. The alpha is read in every notation a browser computes a colour to: the fourth value of `rgba()`, or what follows the slash of `oklch()`, `oklab()`, `lab()`, `lch()` and `color()`, where `none` is 0; a colour without one is opaque | It is not text a reader was meant to see. The notations: decided with the maintainer (2026-10-11), after the third validation pass | y |
| A `filter` on a text, around it or on what covers it | Ink is measured with the functions of every `filter` that change colours left out (`grayscale()`, `invert()`, `hue-rotate()` and the like) and those that keep them (`blur()`, `drop-shadow()`, `opacity()`) applied. An element keeps a `filter` while it is measured, so it goes on holding what is positioned inside it and being painted as one layer | Decided with the maintainer (2026-10-11), after the third validation pass: a text is as covered in a grey-scaled section or on an inverted page as without the filter, and what `filter: opacity()` fades is faded. Spiked: with a `filter` set to `none`, boxes move and another element comes on top | y |
| Unknown-Check message (supersedes the literal in force since slice 7) | `Valid checks: low-contrast-real, offscreen-overflow, overlap, text-clipped.` | Same rule, alphabetical; the list grew. It changes four assertions: `tests/test_detect_visual_bugs.py` lines 342, 352, 362 and 373 | y |
| Order of Findings | Unchanged: severity, then viewport, then document order of the element, then Check name | Settled in slice 4 (LCR-37 to LCR-39, LCR-53) | y |
| How the Capture learns Text ink, Hidden ink and the Coverer | On request, from screenshots in which the glyphs of chosen text nodes are repainted through CSS highlights, alone and as painted, and by hit testing: AD-005 and [`design.md`](design.md). Spiked against real Chromium on 2026-10-11: every case of this spec gives the value of its criterion | AD-003 says how a Check gets a new fact; ADR-0002 keeps the browser out of the Check | y |
| Text rasterization | Chromium is launched with `--disable-lcd-text`, so text is anti-aliased in grayscale in every Capture (AD-006) | With subpixel text the same glyph is rasterized differently alone and as painted: `#veil-55` measured 95% for 100%. The existing suite passes with the flag | y |
| The layout of a Capture | A Capture takes one small screenshot beyond the viewport before it measures anything (AD-006, issue #18) | On Windows that first screenshot changes the font of the generic `monospace` family and the page is laid out again: boxes read before it are off | y |
| A screenshot that shows a part of the page unpainted | A Capture lets the page paint two frames before every screenshot, and waits for them a quarter of a second at most (AD-007) | Found in the third fix round, while the new tests were run against their mutants: on a page with several layers of its own, a screenshot taken right after a change of style now and then shows a band of the page beyond the viewport blank. A covered text in that band had no ink in one picture and got no Finding, on about six calls in ten on `overlap-low.html`. Measured: no miss in 60 calls with the two frames; a second screenshot costs twice as much, `--run-all-compositor-stages-before-draw` does not end it, and a small screenshot taken first makes every call miss. An eighth to a fifth more time per Capture. The frames are asked of the page's own world, where a page can put a function that never calls back: the wait races a timer of 250ms (OVL-121), about eight times what the two frames take. The timer is of the page's own world too: a page that replaces `setTimeout` as well by a function that never calls back still fails the call with the total timeout (fifth validation pass, residual 2). Known limit of the Capture; a follow-up outside this slice | y. Taken by the agent on 2026-10-11 with the maintainer away; confirmed by the maintainer on 2026-10-12, with the bound |
| Fixtures | Ahem at `font-size: 20px` and `line-height: 30px`, as in slice 4: ten glyphs are a block of 200 × 20 pixels of ink. A cover is an opaque box unless a criterion says otherwise, so every share is exact. No text of a fixture is covered by anything its criterion does not name. `overlap-font.html` alone is in the system `sans-serif` font, whose pixels differ from one platform to the next: its outcomes are shares of whole glyphs, which do not | Exact shares need exact pixels | y |
| Criteria not observable through the tool boundary (OVL-61 to OVL-67) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam | y |
| When the discrimination sensor is satisfied | The mutants that a validation report or a task names die, with those of the code the last fix round changed. The pass that confirms it writes no new mutants; one found alive later is a residual or an issue and does not fail the feature | Decided with the maintainer (2026-10-12). Four passes of fresh mutants left 11, 11, 12 and 9 alive: a reader who has not seen the tests finds a few each time, and "none" is not a bar a fix round can meet | y |

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
19. WHEN the element that hides ink of a text has a `role` attribute that lists several roles, one of them the role of a Silent layer (`#under-role-list` in `overlap-bounds.html`, half covered by `#role-list`, whose `role` attribute is `"menu navigation"`) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#role-list` and `severity` equal to `major`: a list of several roles is not a Silent layer. <!-- OVL-71 -->
20. WHEN a covered text is faded by `opacity` and keeps at least half of its ink (`#opacity-60` in `overlap-bounds.html`, of `opacity: 0.6`, half under a cover) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50. <!-- OVL-75 -->
21. WHEN two elements that both have Hidden ink are painted over each other (in `overlap-bounds.html`, `#under-label`, a text of ten glyphs, under `#label` over its first 100px; `#label` has a background and two glyphs of its own, and `#label-cover` lies over the second of those glyphs) THEN the Check SHALL return one Finding for each of the two: for `#under-label` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#label`, and for `#label` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#label-cover`. <!-- OVL-76 -->
22. WHEN the hit tests of a Capture are a sample and all the Hidden ink of an element lies on pixels the sample leaves out (`#speck` in `overlap-sampled.html`, a page with 26,610 pixels of Hidden ink, so tested at every second pixel of every second row: one glyph of `font-size: 10px`, 100 pixels of ink, with `#speck-cover`, one pixel wide, over column 45 of the page, 10 pixels) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10, `severity` equal to `minor` and `evidence.measured.coveredBy` equal to `#speck-cover`. <!-- OVL-78 -->
23. WHEN more elements with Hidden ink are painted over each other in one place than the three that one pair of screenshots tells apart (in `overlap-bounds.html`, `#stack-0`, `#stack-1`, `#stack-2` and `#stack-3`, four texts of ten glyphs in one row, each 40px to the right of the one before and painted over it, with `#stack-cover` over the last 50px of the fourth) THEN the Check SHALL return one Finding for each of the four, all with `severity` equal to `major`: for each of the first three with `evidence.measured.hiddenPercent` equal to 80 and `evidence.measured.coveredBy` equal to `#stack-3`, and for `#stack-3` with `evidence.measured.hiddenPercent` equal to 25 and `evidence.measured.coveredBy` equal to `#stack-cover`. <!-- OVL-80 -->
24. WHEN a covered text starts at another column of the page than every other text of the page (`#shifted` in `overlap-bounds.html`, whose text starts 300px from the left of the page, with a cover over its last 20px) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 10 and `severity` equal to `minor`. <!-- OVL-81 -->
25. WHEN the box of an Other element hides ink of a text and the own text of that Other element stands beside the text, over none of it (in `overlap-bounds.html`, `#under-tag`, a text of ten glyphs, under the opaque box of `#tag` over its last 100px; the two glyphs of `#tag` stand to the right of that text, and `#tag-cover` lies over the second of them) THEN the Check SHALL return one Finding for each of the two: for `#under-tag` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#tag`, and for `#tag` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#tag-cover`. <!-- OVL-82 -->
26. WHEN the own text of an element stands around a child that has text of its own (`#around` in `overlap-bounds.html`: `XXXXX`, a `b` of ten glyphs, `XXXXX`, with a cover over the last 20px of its text, 10% of the ten glyphs that are its own) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 10 and `severity` equal to `minor`. <!-- OVL-83 -->
27. WHEN the glyphs of a covered text are painted with a colour of an alpha above 0 and below 1 (`#translucent` in `overlap-bounds.html`, `color: rgba(0, 0, 0, 0.5)`, half under a cover) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50. <!-- OVL-87 -->
28. WHEN a covered text has a `color` of alpha 0 and its glyphs are painted with a `-webkit-text-fill-color` that is opaque (`#filled` in `overlap-bounds.html`, `color: transparent` and `-webkit-text-fill-color: rgb(0, 0, 0)`, half under a cover) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50. <!-- OVL-89 -->
29. WHEN an Other element hides ink of a text and a Silent layer that is not painted lies over the same ink (`#under-closed-menu` in `overlap-bounds.html`, the last 100px of its text under `#plain-cover` and under `#closed-menu`, an element of `role` `menu` and `visibility: hidden`) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#plain-cover` and `severity` equal to `major`: a Silent layer that is not painted hides nothing. <!-- OVL-90 -->
30. WHEN the page is scrolled when the Capture is taken (`overlap-scrolled-on-load.html`, a page 2700px high that a script of the page scrolls 900px while it loads: `#far` is 1000px down the page, the last 100px of its 200px of text under `#far-cover`) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` and a viewport of 1440 × 900 SHALL return exactly one Finding, on `#far`, with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#far-cover`. <!-- OVL-86 -->
31. WHEN a covered text is inside an element with a `filter` that changes colours (`#in-grey` in `overlap-bounds.html`, in a row of `filter: grayscale(1)`, the last 100px of its 200px of text under `#in-grey-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#in-grey-cover` and `severity` equal to `major`. <!-- OVL-92 -->
32. WHEN a covered text has a `filter` of its own that changes colours (`#own-filter` in `overlap-bounds.html`, of `filter: hue-rotate(180deg)`, half under `#own-filter-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#own-filter-cover` and `severity` equal to `major`. <!-- OVL-93 -->
33. WHEN the Other element over a text is placed by an element that holds it only because it has a `filter` (`#held` in `overlap-bounds.html`: `#holder`, of `position: static` and `filter: sepia(1)`, holds `#held-cover`, of `position: absolute`, over the last 100px of the text) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#held-cover` and `severity` equal to `major`: measuring moves nothing on the page. <!-- OVL-94 -->
34. WHEN the root of a page has a `filter` that changes colours (`overlap-inverted.html`, whose `html` element has `filter: invert(1)`: the last 100px of the 200px of text of `#inverted` are under `#inverted-cover`) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return exactly one Finding, on `#inverted`, with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#inverted-cover`. <!-- OVL-95 -->
35. WHEN the glyphs of a covered text are painted with a colour that is not computed to `rgb()` and has no alpha or an alpha above 0 (in `overlap-bounds.html`, each half under a cover: `#opaque-oklch`, `color: oklch(0 0 0)`, and `#translucent-oklch`, `color: oklch(0 0 0 / 0.5)`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50. <!-- OVL-100 -->
36. WHEN a text in a font with anti-aliased edges is wholly under an opaque Other element (`#font-whole` in `overlap-font.html`, a line of the system `sans-serif` font at 16px under `#font-whole-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 100, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#font-whole-cover`: Hidden ink is a part of Text ink, pixel by pixel. <!-- OVL-101 -->
37. WHEN a text in such a font is two lines of the same glyphs at the same columns and the second line is wholly under an opaque Other element (`#font-lines` in `overlap-font.html`, under `#font-lines-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#font-lines-cover`. <!-- OVL-102 -->
38. WHEN a text in such a font is wholly under an Other element that lets less than half of its ink through (`#font-veil-55` in `overlap-font.html`, under `#font-veil-55-cover`, a layer of `rgba(255, 255, 255, 0.55)`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 100, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#font-veil-55-cover`. <!-- OVL-103 -->
39. WHEN a descendant of an element is painted over a part of its own text and an Other element hides at least 10% of the ink the element shows beside that descendant (in `overlap-reach.html`: `#child-first`, with a child of `position: absolute` over the first 80px of its 200px of text and `#child-first-cover` over its last 20px, and `#child-last`, with a child over its last 80px and `#child-last-cover` over its first 20px, each cover over 400 of the 2400 pixels the text shows) THEN the Check SHALL return one Finding for the element with `evidence.measured.hiddenPercent` equal to 16, `severity` equal to `minor` and `evidence.measured.coveredBy` equal to that cover: Text ink is what the element shows with what is inside it painted. <!-- OVL-106 -->
40. WHEN the box of an Other element hides ink of a text, the own text of that Other element stands beside the text and the Other element stands before the text in the document (in `overlap-reach.html`, the row of OVL-82 with the tag first: `#tag-first`, an opaque box over the last 100px of `#under-tag-first` with two glyphs of its own to the right of that text, and `#tag-first-cover` over the second of them) THEN the Check SHALL return one Finding for each of the two: for `#under-tag-first` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#tag-first`, and for `#tag-first` with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#tag-first-cover`. <!-- OVL-107 -->
41. WHEN the element that hides ink of a text has the `open` attribute and is not a `dialog` element (`#under-details` in `overlap-reach.html`, half covered by `#open-details`, a `details` element with the `open` attribute) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#open-details` and `severity` equal to `major`. <!-- OVL-108 -->
42. WHEN ink of a text is hidden by a pseudo-element of an Other element that has own text, all of it seen (in `overlap-reach.html`: `#under-after`, the last 100px of its text under a box that the `::after` of `#after-owner` paints outside its own box, and `#under-before`, the same under the `::before` of `#before-owner`; each owner has two glyphs of its own beside the text) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to the owner of the pseudo-element. <!-- OVL-111 -->
43. WHEN the page is scrolled sideways when the Capture is taken (`overlap-scrolled-sideways-on-load.html`, a page 3000px wide that a script of the page scrolls 1500px sideways while it loads: `#far` is 2000px from the left of the page, the last 100px of its 200px of text under `#far-cover`) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` and a viewport of 1440 × 900 SHALL return exactly one Finding, on `#far`, with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#far-cover`. <!-- OVL-114 -->
44. WHEN a covered text has a `filter` that lists a function that changes colours and one that keeps them (`#listed` in `overlap-filters.html`, of `filter: grayscale(1) opacity(0.6)`, the last 100px of its 200px of text under `#listed-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#listed-cover` and `severity` equal to `major`: the function that changes colours is left out and the one that keeps them applied. <!-- OVL-122 -->
45. WHEN a covered text is inside an element whose `filter` that changes colours is declared `!important` (`#weighty` in `overlap-filters.html`, in a row of `filter: grayscale(1) !important`, half under `#weighty-cover`) THEN the Check SHALL return one Finding for it with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#weighty-cover` and `severity` equal to `major`. <!-- OVL-123 -->
46. WHEN the `drop-shadow()` of an Other element hides ink of a text beside the ink its box hides (`#under-shadow` in `overlap-filters.html`: the box of `#shadow-cover` is over the last 60px of its 200px of text and its shadow, of `filter: drop-shadow(-40px 0 0 rgb(200, 0, 0))`, over the 40px before them) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#shadow-cover` and `severity` equal to `major`: what a `drop-shadow()` hides is hidden. <!-- OVL-124 -->
47. WHEN an element inside a text that is not its child is painted over a part of the own text of that text and an Other element hides at least 10% of the ink the text shows beside it (`#grandchild-first` in `overlap-nested.html`: `#grandchild-badge`, the child of a child of the text, of `position: absolute`, over the first 80px of its 200px of text and `#grandchild-first-cover` over its last 20px, 400 of the 2400 pixels the text shows) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 16, `severity` equal to `minor` and `evidence.measured.coveredBy` equal to `#grandchild-first-cover`: what is inside a text is its descendants, not its children alone. <!-- OVL-127 -->
48. WHEN ink of a text is hidden by the border of an Other element that has own text, all of it seen (`#under-border` in `overlap-border.html`: the last 100px of its 200px of text under the left border, 100px wide, of `#bordered`, which has no background and two glyphs of its own beside the text) THEN the Check SHALL return one Finding for the text with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#bordered`. <!-- OVL-131 -->

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
22. IF the only element that hides ink of a text has a `role` attribute that is one of those roles written with spaces around it or with capitals (`#under-spaced-role` in `overlap-clean.html`, half covered by `#spaced-role`, whose `role` attribute is `" Menu "`) THEN the Check SHALL return no Finding for the text. <!-- OVL-70 -->
23. IF the only thing painted over the own text of an element is painted by one of its ancestors (`#under-own-row` in `overlap-clean.html`, the last 100px of its 200px of text under an opaque box painted by the `::after` of its row, `#decorated-row`) THEN the Check SHALL return no Finding for the element. <!-- OVL-72 -->
24. IF hit testing gives a descendant of an element at all of its Hidden ink (`#own-link-text` in `overlap-clean.html`, half under `#linked-cover`, an Other element of `z-index: 1`, with the `::after` of its own link, `#own-link`, stretched over all of it above that cover by `position: absolute`, `inset: 0` and `z-index: 2`) THEN the Check SHALL return no Finding for the element. <!-- OVL-73 -->
25. IF a covered text is faded below half by `opacity` (`#opacity-40` in `overlap-clean.html`, of `opacity: 0.4`, half under a cover) THEN the Check SHALL return no Finding for it: it has no Text ink. <!-- OVL-74 -->
26. IF the glyphs of a covered text are painted with a `-webkit-text-fill-color` of alpha 0 while its `color` is opaque (`#transparent-fill` in `overlap-clean.html`, `color: rgb(0, 0, 0)` and `-webkit-text-fill-color: transparent`, half under a cover) THEN the Check SHALL return no Finding for it. <!-- OVL-88 -->
27. IF all that lies over a text is a menu that is closed (in `overlap-clean.html`, `#under-removed-menu`, with `#removed-menu`, an element of `role` `menu` and `display: none`, placed over the last 100px of its 200px of text, and `#under-hidden-menu`, with `#hidden-menu`, an element of `role` `menu` and `visibility: hidden`, over the last 100px of its text) THEN the Check SHALL return no Finding for the text, and nothing SHALL be painted over it. <!-- OVL-91 -->
28. IF the Other element over a text is faded out by its `filter` (`#under-filter-faded` in `overlap-clean.html`, half under an opaque box of `filter: opacity(0)`) THEN the Check SHALL return no Finding for the text. <!-- OVL-96 -->
29. IF a covered text is faded out by its `filter` (`#filter-faded-text` in `overlap-clean.html`, of `filter: opacity(0)`, half under a cover) THEN the Check SHALL return no Finding for it. <!-- OVL-97 -->
30. IF a text is painted above an element with a `filter`, and an Other element inside that element has a `z-index` above that of the text (`#above-filter-layer` in `overlap-clean.html`, of `position: relative` and `z-index: 1`: `#layered-cover`, of `z-index: 5`, is inside `#filter-layer`, of `filter: invert(1)`, and lies under the glyphs of the last 100px of the text) THEN the Check SHALL return no Finding for the text: an element with a `filter` is painted as one layer while ink is measured too. <!-- OVL-98 -->
31. IF the glyphs of a covered text are painted with a colour of alpha 0 that is not computed to `rgb()` (in `overlap-clean.html`, each half under a cover: `#transparent-oklch`, `color: oklch(0 0 0 / 0)`; `#transparent-mix`, `color: color-mix(in srgb, rgb(0 0 0) 0%, transparent)`, which is computed to `color(srgb 0 0 0 / 0)`; `#transparent-none`, `color: oklch(0 0 0 / none)`) THEN the Check SHALL return no Finding for it. <!-- OVL-99 -->
32. IF a text in a font with anti-aliased edges is wholly under an Other element that lets at least half of its ink through (`#font-veil-45` in `overlap-font.html`, a line of the system `sans-serif` font at 16px under a layer of `rgba(255, 255, 255, 0.45)`) THEN the Check SHALL return no Finding for it: a pixel is seen by the ink it has, at the edge of a glyph as at its middle. <!-- OVL-104 -->
33. IF a descendant of an element is painted over a part of its own text and an Other element hides under 10% of the ink the element shows beside that descendant (`#child-and-nick` in `overlap-clean.html`: `#nick-badge`, a child of `position: absolute`, over the first 80px of its 200px of text, and `#child-nick-cover` over its last 10px, 200 of the 2400 pixels the text shows) THEN the Check SHALL return no Finding for the element. <!-- OVL-105 -->
34. IF a covered text is blurred by its `filter` until no pixel of it keeps half of the ink of a glyph (`#blurred` in `overlap-filters.html`, of `filter: blur(20px)`, half under a cover) THEN the Check SHALL return no Finding for it: it has no Text ink. <!-- OVL-125 -->
35. IF a covered text is faded below half by two functions of one `filter` that each leave over half of its ink (`#twice-faded` in `overlap-filters.html`, of `filter: opacity(0.6) grayscale(1) opacity(0.6)`, which leaves 36 parts in 100, half under a cover) THEN the Check SHALL return no Finding for it: every function that keeps colours is applied. <!-- OVL-126 -->
36. IF the only element that hides ink of a text is inside an element with a `role` of `menu` and is not its child (`#under-deep-item` in `overlap-nested.html`, half covered by `#deep-item`, the child of a child of the menu) THEN the Check SHALL return no Finding for the text. <!-- OVL-128 -->

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
8. WHEN two Other elements hide ink of one text and only the one that is not its Coverer is in a Raised layer (`#under-raised-small` in `overlap-reach.html`: `#raised-small`, first in the document, of `position: absolute` and `z-index: 1`, over its first 20px and `#plain-large` over its last 80px) THEN the Finding SHALL have `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#plain-large` and `severity` equal to `major`. <!-- OVL-109 -->
9. WHEN two Other elements hide ink of one text and only its Coverer is in a Raised layer (`#under-raised-large` in `overlap-reach.html`: `#plain-small`, first in the document, over its first 20px and `#raised-large`, of `position: absolute` and `z-index: 1`, over its last 80px) THEN the Finding SHALL have `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#raised-large` and `severity` equal to `minor`. <!-- OVL-110 -->
10. WHEN Findings of the severities `major`, `minor` and `info` come from one call THEN `findings` SHALL hold them in that order and the summary line SHALL count each severity apart: on `overlap-info.html`, whose texts stand in the document as `#a` (a cover of `position: absolute` and `z-index: 1` over its last 20px), `#b` (a cover over its last 20px) and `#c` (a cover over its last 100px), `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#c, major, 50, #c-cover)`, `(#b, minor, 10, #b-cover)` and `(#a, info, 10, #a-cover)`, and a first content block that is a text block equal to `Found 3 findings in 1 viewport: 1 major, 1 minor, 1 info.` <!-- OVL-115 -->
11. WHEN two Other elements hide ink of one text, its Coverer stands first of the two in the document and only the other one is in a Raised layer (`#under-plain-first` in `overlap-raised.html`: `#plain-large-first` over its last 80px and `#raised-small-last`, of `position: absolute` and `z-index: 1`, over its first 20px) THEN the Finding SHALL have `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#plain-large-first` and `severity` equal to `major`. <!-- OVL-129 -->
12. WHEN two Other elements hide ink of one text, its Coverer stands first of the two in the document and only the Coverer is in a Raised layer (`#under-raised-first` in `overlap-raised.html`: `#raised-large-first`, of `position: absolute` and `z-index: 1`, over its last 80px and `#plain-small-last` over its first 20px) THEN the Finding SHALL have `evidence.measured.hiddenPercent` equal to 50, `evidence.measured.coveredBy` equal to `#raised-large-first` and `severity` equal to `minor`. <!-- OVL-130 -->

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
8. WHEN hit testing scrolls the page and the scroll brings over the Hidden ink of a text an element that does not lie over it where the Capture has it (`#far` in `overlap-scrolled.html`, a page 2700px high: 1000px down the page, the last 100px of its 200px of text under `#far-cover`; `#fixed-bar`, of `position: fixed`, is 100px down the viewport and lies over those 100px once the page is scrolled 900px) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` and a viewport of 1440 × 900 SHALL return exactly one Finding, on `#far`, with `evidence.measured.hiddenPercent` equal to 50 and `evidence.measured.coveredBy` equal to `#far-cover`. <!-- OVL-77 -->
9. WHEN the hit tests of a Capture are a sample THEN the Coverer SHALL be the Other element found at the largest part of the pixels tested, not of all the Hidden ink: in `overlap-sampled.html`, tested at every second pixel of every second row, `#stripes`, painted as stripes 1px wide on the odd columns of the page, hides 600 pixels of the ink of `#striped`, none of them tested, and `#solid-cover` hides 400, and with `checks` equal to `["overlap"]` the `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` of `findings` SHALL be, in this order, `(#striped, major, 25, #solid-cover)`, `(#row-striped, major, 40, #row-solid-cover)` (the text of OVL-84), `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 11 (the twelve texts that take the page over 20,000 pixels of Hidden ink, each half under a cover of its own) and `(#speck, minor, 10, #speck-cover)`. <!-- OVL-79 -->
10. WHEN the hit tests of a Capture are a sample THEN the rows of the page SHALL be sampled as its columns are: in `overlap-sampled.html`, tested at every second pixel of every second row, `#row-stripes`, painted as stripes 1px high on the odd rows of the page over the first 120px of the text of `#row-striped`, hides 1200 pixels of its ink, none of them tested, and `#row-solid-cover`, over its last 20px, hides 400, and the Finding of `#row-striped` SHALL have `evidence.measured.hiddenPercent` equal to 40, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#row-solid-cover`. <!-- OVL-84 -->
11. WHEN a Capture has no more than 20,000 pixels of Hidden ink to test THEN every one of them SHALL be hit tested: on `overlap-exact.html`, which holds the row of `#striped` of `overlap-sampled.html` alone (1000 pixels of Hidden ink, 600 of them under `#stripes`, on the odd columns of the page, and 400 under `#solid-cover`), `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return exactly one Finding, on `#striped`, with `evidence.measured.hiddenPercent` equal to 25, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#stripes`. <!-- OVL-85 -->
12. WHEN the covered element is positioned THEN `evidence.computed` SHALL hold its computed `position` and `z-index`: in `overlap-reach.html`, `{"position": "relative", "z-index": "1"}` for `#positioned` (of `position: relative` and `z-index: 1`, half under a cover with a `z-index` of 2) and `{"position": "relative", "z-index": "auto"}` for `#relative` (of `position: relative`, half under a cover that comes after it in the document). <!-- OVL-112 -->
13. WHEN Hidden ink lies right of the viewport THEN hit testing SHALL reach it with the page scrolled sideways, as it does down the page: on `overlap-wide.html`, a page 3000px wide and 2000px high whose four texts each have the last 100px of their 200px under a cover of their own (`#near`, 40px from the left of the page; `#right`, 2000px from it; `#edge`, 2780px from it, where the page cannot be scrolled a whole viewport further; `#far`, 2000px from the left and 1000px down) and whose `#fixed-bar`, of `position: fixed`, lies over the Hidden ink of `#right` once the page is scrolled 1440px sideways, `detect_visual_bugs` called with `checks` equal to `["overlap"]` and a viewport of 1440 × 900 SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#near, major, 50, #near-cover)`, `(#right, major, 50, #right-cover)`, `(#edge, major, 50, #edge-cover)` and `(#far, major, 50, #far-cover)`. <!-- OVL-113 -->
14. WHEN an element has Hidden ink and a Hidden share under 10% THEN its Hidden ink SHALL not count towards the 20,000 pixels of the Term "Coverer": on `overlap-count-under.html` (19,000 pixels of Hidden ink in `#striped`, the text of OVL-85, and in nine texts each half under a cover of its own, and 1520 in four texts, `#under-0` to `#under-3`, each with an element of `role` `menu` over its first 100px and a cover over its last 19px, 9.5%) `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#striped, major, 25, #stripes)` and `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 8: every pixel of Hidden ink is hit tested. <!-- OVL-116 -->
15. WHEN an element has a Hidden share of at least 10% and gets no Finding THEN its Hidden ink SHALL count towards the 20,000 pixels: on `overlap-count-unreported.html` (the 19,000 pixels of OVL-116 and 2000 in `#unseen`, of `color: transparent`, half under a cover) `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#striped, major, 25, #solid-cover)` and `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 8: every second pixel of every second row is hit tested. <!-- OVL-117 -->
16. WHEN a Capture has more than 20,000 and no more than 80,000 pixels of Hidden ink to test THEN every second pixel of every second row SHALL be hit tested: on `overlap-step-two.html` (49,000 pixels, in `#striped` and in 24 texts each half under a cover of its own) `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#striped, major, 25, #solid-cover)` and `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 23. <!-- OVL-118 -->
17. WHEN a Capture has more than 80,000 and no more than 180,000 pixels of Hidden ink to test THEN every third pixel of every third row SHALL be hit tested: on `overlap-step-three.html` (81,000 pixels, in `#striped` and in 40 texts each half under a cover of its own), where `#stripes` is found on the 10 odd columns of its 60 that are multiples of 3 and `#solid-cover` on 6, `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#striped, major, 25, #stripes)` and `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 39. <!-- OVL-119 -->
18. WHEN a Capture has exactly 20,000 pixels of Hidden ink to test THEN every one of them SHALL be hit tested: on `overlap-cap.html` (1000 pixels in `#striped`, the text of OVL-85, 18,000 in nine texts each half under a cover of its own and 1000 in `#last`, with a cover over the last 50px of its 200px of text) `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return `findings` whose `(selector, severity, evidence.measured.hiddenPercent, evidence.measured.coveredBy)` are, in this order, `(#striped, major, 25, #stripes)`, `(#filler-n, major, 50, #filler-cover-n)` for n from 0 to 8 and `(#last, major, 25, #last-cover)`. <!-- OVL-132 -->

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
- WHEN `detect_visual_bugs` is called six times in a row with `checks` equal to `["overlap"]` on `overlap-low.html` (a page 1850px high at 1440 × 900: thirty-six rows that a browser paints as layers of their own, a sticky element, a text of `opacity: 0`, a link with a `z-index` and a text of `opacity: 0.4` in turn, and under them `#low`, 1820px down the page, the last 100px of its 200px of text under `#low-cover`) THEN every call SHALL return exactly one Finding, on `#low`, with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#low-cover`: a part of the page that a screenshot shows unpainted is not read as a page with nothing on it. <!-- OVL-120 -->
- WHEN a page never calls an animation frame back (`overlap-no-frames.html`, whose script puts a function that never calls back where `window.requestAnimationFrame` is: the last 100px of the 200px of text of `#still` are under `#still-cover`) THEN `detect_visual_bugs` called with `checks` equal to `["overlap"]` SHALL return exactly one Finding, on `#still`, with `evidence.measured.hiddenPercent` equal to 50, `severity` equal to `major` and `evidence.measured.coveredBy` equal to `#still-cover`: the wait for the frames ends with a timer. <!-- OVL-121 -->

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
| OVL-65 | P2: Check contract, configuration and documents | T13 | Implemented |
| OVL-66 | P2: Check contract, configuration and documents | T13 | Implemented |
| OVL-67 | P2: Check contract, configuration and documents | closing step | Pending |
| OVL-68 | Edge cases | T9 | Implemented |
| OVL-69 | Edge cases | T12 | Implemented |
| OVL-70 | P1: Stay silent on overlaps that are meant | F1 | Implemented |
| OVL-71 | P1: Report text that another element covers | F2 | Implemented |
| OVL-72 | P1: Stay silent on overlaps that are meant | F1 | Implemented |
| OVL-73 | P1: Stay silent on overlaps that are meant | F1 | Implemented |
| OVL-74 | P1: Stay silent on overlaps that are meant | F1 | Implemented |
| OVL-75 | P1: Report text that another element covers | F2 | Implemented |
| OVL-76 | P1: Report text that another element covers | F2 | Implemented |
| OVL-77 | P1: Read the Finding | F3 | Implemented |
| OVL-78 | P1: Report text that another element covers | F4 | Implemented |
| OVL-79 | P1: Read the Finding | F4 | Implemented |
| OVL-80 | P1: Report text that another element covers | F5 | Implemented |
| OVL-81 | P1: Report text that another element covers | F5 | Implemented |
| OVL-82 | P1: Report text that another element covers | F5 | Implemented |
| OVL-83 | P1: Report text that another element covers | F5 | Implemented |
| OVL-84 | P1: Read the Finding | F7 | Implemented |
| OVL-85 | P1: Read the Finding | F7 | Implemented |
| OVL-86 | P1: Report text that another element covers | F8 | Implemented |
| OVL-87 | P1: Report text that another element covers | F5 | Implemented |
| OVL-88 | P1: Stay silent on overlaps that are meant | F6 | Implemented |
| OVL-89 | P1: Report text that another element covers | F5 | Implemented |
| OVL-90 | P1: Report text that another element covers | F5 | Implemented |
| OVL-91 | P1: Stay silent on overlaps that are meant | F6 | Implemented |
| OVL-92 | P1: Report text that another element covers | F9 | Implemented |
| OVL-93 | P1: Report text that another element covers | F9 | Implemented |
| OVL-94 | P1: Report text that another element covers | F9 | Implemented |
| OVL-95 | P1: Report text that another element covers | F9 | Implemented |
| OVL-96 | P1: Stay silent on overlaps that are meant | F9 | Implemented |
| OVL-97 | P1: Stay silent on overlaps that are meant | F9 | Implemented |
| OVL-98 | P1: Stay silent on overlaps that are meant | F9 | Implemented |
| OVL-99 | P1: Stay silent on overlaps that are meant | F10 | Implemented |
| OVL-100 | P1: Report text that another element covers | F10 | Implemented |
| OVL-101 | P1: Report text that another element covers | F11 | Implemented |
| OVL-102 | P1: Report text that another element covers | F11 | Implemented |
| OVL-103 | P1: Report text that another element covers | F11 | Implemented |
| OVL-104 | P1: Stay silent on overlaps that are meant | F11 | Implemented |
| OVL-105 | P1: Stay silent on overlaps that are meant | F12 | Implemented |
| OVL-106 | P1: Report text that another element covers | F12 | Implemented |
| OVL-107 | P1: Report text that another element covers | F12 | Implemented |
| OVL-108 | P1: Report text that another element covers | F12 | Implemented |
| OVL-109 | P1: Severity | F12 | Implemented |
| OVL-110 | P1: Severity | F12 | Implemented |
| OVL-111 | P1: Report text that another element covers | F12 | Implemented |
| OVL-112 | P1: Read the Finding | F12 | Implemented |
| OVL-113 | P1: Read the Finding | F13 | Implemented |
| OVL-114 | P1: Report text that another element covers | F13 | Implemented |
| OVL-115 | P1: Severity | F14 | Implemented |
| OVL-116 | P1: Read the Finding | F15 | Implemented |
| OVL-117 | P1: Read the Finding | F15 | Implemented |
| OVL-118 | P1: Read the Finding | F15 | Implemented |
| OVL-119 | P1: Read the Finding | F15 | Implemented |
| OVL-120 | Edge cases | F17 | Implemented |
| OVL-121 | Edge cases | F18 | Implemented |
| OVL-122 | P1: Report text that another element covers | F19 | Implemented |
| OVL-123 | P1: Report text that another element covers | F19 | Implemented |
| OVL-124 | P1: Report text that another element covers | F19 | Implemented |
| OVL-125 | P1: Stay silent on overlaps that are meant | F19 | Implemented |
| OVL-126 | P1: Stay silent on overlaps that are meant | F19 | Implemented |
| OVL-127 | P1: Report text that another element covers | F20 | Implemented |
| OVL-128 | P1: Stay silent on overlaps that are meant | F20 | Implemented |
| OVL-129 | P1: Severity | F21 | Implemented |
| OVL-130 | P1: Severity | F21 | Implemented |
| OVL-131 | P1: Report text that another element covers | F22 | Implemented |
| OVL-132 | P1: Read the Finding | F23 | Implemented |

**Coverage:** 132 total, 132 mapped to tasks, 0 unmapped. The Phase column names the task of [`tasks.md`](tasks.md).

---

## Success Criteria

- [ ] All 132 requirements verified by the Verifier, OVL-61 to OVL-67 from file evidence.
- [ ] The gate passes: typecheck, lint, format check and the whole test suite.
- [ ] The discrimination sensor leaves alive none of the mutants that a validation report or a task names, nor any of the code the last fix round changed, in the Check, in what the Capture gains for it and in the rules of Silent and Raised layers (Assumptions, "When the discrimination sensor is satisfied").
