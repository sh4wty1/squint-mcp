# `offscreen-overflow`

Roadmap slice 7.

## Problem

A page that is wider than its viewport scrolls sideways: on a phone the whole layout slides under the finger, and part of the content starts out of sight. Whoever calls `detect_visual_bugs` on such a page today gets no Finding for it, and nothing in the result says which element is the one that sticks out. The source gives no figure for how often this happens; it is one of the five first Checks of `.docs/START.md`, section 10 ("elemento além da largura do viewport", confirmed by "scroll horizontal na página").

When this ships: for each viewport where the page scrolls horizontally, `detect_visual_bugs` names the element that sets the page's width, with by how many pixels the page passes the viewport.

## Flow

Reuses the Capture as it is: the width of the page is the scroll width of `html`, which every Capture already holds, so the Check needs no new page script, no new screenshot and no change to the tools. Measured on `9923762` with a throwaway spike (29 small pages at 400x300): the width of the full-page screenshot equals `document.documentElement.scrollWidth` in every one of them. The review of PR #17 found the page where the two differ: a `body` that is its own scroll container clips what the screenshot still counts, so the width is no longer read from `pixels`.

1. a page -> `capture.py` (exists) and `js/collect_elements.js` (exists) - unchanged but for one generic fact per element, its tag name, so that a Check can tell `html` and `body` from the rest
2. `detect_visual_bugs` (exists) - unchanged, runs every Check of `checks.CHECKS` (exists) on each Capture
3. `checks/offscreen_overflow.py` (new, no door - placement per conventions, one module per Check as AD-003 says) - compares the scroll width of `html` with the viewport's width, and when the page is wider picks the element whose right edge is the page's right edge, within the tolerance of 1px held in `config.py` (exists)
4. out: a `Finding` (exists, door 1 for its values) in the `findings` of `detect_visual_bugs`, ordered and given a crop by the tool as any other

## Impact

| Front | What changes |
| --- | --- |
| domain | no new term. A new Check name, `offscreen-overflow`, accepted in `checks` of `detect_visual_bugs`, and the first use of the category `responsive`, which the Finding schema already lists |
| results | a call with no `checks` now runs three Checks, so a page that scrolls sideways gets one more Finding per viewport. Its severity is `major`, so it can take one of the five crops from a `minor` Finding |
| existing tests | four assertions in `tests/test_detect_visual_bugs.py` quote `Valid checks: low-contrast-real, text-clipped.`; the list gains the new name. They are the only existing assertions edited. Measured: no existing fixture scrolls sideways at 1440, and the five that do at 390 (`box`, `low-contrast-bounds`, `pixel-budget`, `pixel-cost`, `sampled-patterns`) are never called there with the default Checks |
| Capture | `Element` gains `tag`. `inspect_element` builds its result field by field, so its output does not change |
| stored data | nothing to migrate - nothing is persisted |

## Relations

`None - no stored-data shape change`

## Surface

`None - no tool, parameter or field is added, and no signature changes: `checks` is still a list of names. The new accepted name and the Finding it yields are door 1; the list in the `Unknown check` error is AC 16`

## Landing

Nothing is persisted. Both rows are what a released tool reports, which a caller may come to filter on.

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1. The values of the Finding | `check: "offscreen-overflow"`, `category: "responsive"`, `severity: "major"`, `source: "Squint heuristic"`, `evidence.measured: {"overflowPx", "pageWidth", "viewportWidth"}`, `evidence.computed: {"display", "position", "width", "white-space"}` | `category: "visual-bug"` - live alternative. Rejected because the bug depends on the viewport: the same page is clean at 1440 and broken at 390, which is what `responsive` names and no Check uses yet |
| 2. Which element is named | one Finding per Capture: the first element in document order whose reach is within 1px of the page's right edge, where the reach is the right edge of its box or of its own text, whichever is further | every element past the viewport's right edge - names each descendant of a wide element, and each item of a clipped carousel once anything else makes the page scroll (spike: the page is 600px wide and a track inside `overflow: hidden` is at 2000px). The innermost element at the edge - names every paragraph of a wide column instead of the column |

- Cost of door 2: a page with two culprits of different widths gets the wider one; the other shows once the first is fixed
- Nothing else in this change is hard to reverse

## Criteria

### S1: the element that makes the page scroll is named (P1)

One Finding per viewport where the page scrolls sideways, on the element that sets its width.

**Acceptance Criteria**

1. WHEN the page of a Capture is wider than its viewport THEN the system SHALL report exactly one `offscreen-overflow` Finding for that Capture, with `category == "responsive"`, `severity == "major"` and `source == "Squint heuristic"`
2. WHEN that Finding is reported THEN it SHALL sit on the first element in document order whose right edge, or the right edge of whose own text, is less than 1px from the page's right edge
3. WHEN a page of 1440px holds an element of 1640px THEN the Finding SHALL carry `measured == {"overflowPx": 200, "pageWidth": 1640, "viewportWidth": 1440}`, the element's `display`, `position`, `width` and `white-space` in `computed`, and the message `Extends 200px past the 1440px viewport, so the page scrolls horizontally`
4. WHEN an element at the page's right edge holds a child that ends at the same edge THEN the system SHALL report the element and not the child
5. WHEN an element that fits the viewport holds a child that ends at the page's right edge THEN the system SHALL report the child
6. WHEN an element ends 1px before the page's right edge and stands before the one that ends on it THEN the system SHALL report the one that ends on it
7. WHEN a word that cannot break runs past the viewport out of an element whose box fits it THEN the system SHALL report that element
8. WHEN an element is moved past the viewport by a transform THEN the system SHALL report it with the `box` it is painted at
9. WHEN an element of 400px is captured at a viewport 399px wide and at one 400px wide THEN the system SHALL report it at 399 with `overflowPx == 1` and report nothing at 400
10. IF the page is as wide as the viewport THEN the system SHALL report no `offscreen-overflow` Finding, whether an element sticks out to the left, is `position: fixed` past the right edge, is cut by an ancestor with `overflow: hidden`, sits in a container that scrolls, casts a shadow past the edge, has a right margin past it, or the page is taller than the viewport
11. IF the `overflow-x` of the viewport is `hidden` or `clip` - that of `html`, or that of `body` while that of `html` is `visible` - THEN the system SHALL report no `offscreen-overflow` Finding
12. IF the `direction` of `body` is `rtl` THEN the system SHALL report no `offscreen-overflow` Finding
13. IF the page is wider than the viewport and no element reaches its right edge THEN the system SHALL report no `offscreen-overflow` Finding

**Independent test:** `detect_visual_bugs` on the bug fixture at 1440 and on the clean one.

### S2: the Check is reachable through the tool (P2)

**Acceptance Criteria**

14. WHEN `detect_visual_bugs` is called with `checks: ["offscreen-overflow"]` on a page that also has a clipped text THEN the system SHALL return the `offscreen-overflow` Finding alone
15. WHEN `detect_visual_bugs` is called with no `checks` on that page THEN the system SHALL return both Findings
16. IF `checks` holds an unknown name THEN the error SHALL end with `Valid checks: low-contrast-real, offscreen-overflow, text-clipped.`
17. The description of `detect_visual_bugs` SHALL name `offscreen-overflow` and say what it reports
18. The system SHALL keep every existing test passing, edited only in the four assertions that quote the list of valid Checks

**Independent test:** call the tool with the new name, with none and with a wrong one.

### S3: the record (P3)

**Acceptance Criteria**

19. The `[Unreleased]` section of `CHANGELOG.md` SHALL have an `Added` entry for the `offscreen-overflow` Check that says it reports one element per viewport, with severity `major`, and that it reports nothing while the page hides its horizontal overflow
20. The sentence of `README.md` that counts and names the Checks SHALL name three, `offscreen-overflow` among them

**Independent test:** read the two places.

## Out of scope

| Excluded | Why |
| --- | --- |
| Vertical overflow | roadmap slice 7, "Não entra" |
| Scroll inside containers | roadmap slice 7, "Não entra" |
| `compare_viewports` | roadmap slice 7, "Não entra"; fase 3 |
| Content cut by `overflow-x: hidden` on `html` or `body` | the page does not scroll then; it is content that cannot be reached, another Check's matter |
| Pages in a right-to-left direction | they scroll to the left, and their boxes then start at a negative x that the pixels do not have; `text-clipped` leaves them out too |
| The `100vw` element that is wider than the page by the width of the scrollbar | headless Chromium draws no scrollbar that takes width, so the Capture cannot see it (spike: `width: 100vw` on a tall page, 400 of 400) |
| Naming a pseudo-element | a Finding names an element by a selector; AC 13 stays silent |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Severity | always `major`, no threshold | a page that slides sideways is broken at that viewport whatever the distance, and the scroll is whole pixels, so 1px is not rounding (spike: 400.4px does not scroll, 400.6px scrolls 1px). `minor` under 8px, as `text-clipped`, is the alternative | y |
| The page hides its overflow | not reported (AC 11) | `body { overflow-x: hidden }` is how an off-canvas menu is built on purpose; the roadmap asks for the scroll to confirm | y |
| How many Findings | one per viewport (door 2) | the question is which element sets the width; the others are its children or are clipped | y |
| An element not on the edge by coincidence | accepted limit: a clipped or `position: fixed` element that ends within 1px of the page's edge and stands before the real one is named instead | telling them apart needs the clip chain of every element, which the Capture does not hold | y |
| `README.md` | updated in this slice (AC 20) | its sentence "runs two Checks" becomes false with this change; slice 11 still owns the release text | y |
| Fixtures | several small pages, not one pair | the condition is the page's, so each case that changes the page's width or its `overflow-x` needs a page of its own | y |
| Profile | `light` | `AGENTS.md` declares none | y |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| tool `detect_visual_bugs` | response shape | AC 1, AC 3 - the existing Finding, no field added |
| tool `detect_visual_bugs` | error shape and codes | AC 16 - the existing `Unknown check` error, with the new name in its list |
| tool `detect_visual_bugs` | who may call, rate limits | n/a - a local stdio server, as before |
| tool `detect_visual_bugs` | versioning | AC 19 - adding a Check is not breaking and is recorded in the CHANGELOG, as its header says |
| document `CHANGELOG.md` | structure, depth | AC 19 - one `Added` entry under `[Unreleased]`, in the form of the 0.1.0 ones |
| document `README.md` | structure, depth | AC 20 - the one sentence that names the Checks |

## Sources

- `docs/ROADMAP.md`, section 7 - what enters and what does not
- `.docs/START.md`, section 10 - the DOM signal and the confirmation of the Check
- `.specs/STATE.md`, AD-003 and AD-004 - the Capture is the whole contract; a Check that needs a new fact adds a field to the collector
