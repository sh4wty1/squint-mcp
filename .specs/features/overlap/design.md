# overlap Design

**Spec**: `.specs/features/overlap/spec.md`
**Status**: Approved by the maintainer on 2026-10-11

Every choice marked "spiked" was run against `playwright 1.63` and real Chromium (headless shell 153, Windows) on 2026-10-11, on a page holding the cases of the spec, on every existing fixture at both viewports and on a page of 710 real-font texts. Conforms to AD-001, AD-002, AD-003 and AD-004; adds AD-005 and AD-006. The spike is kept in [`spike/`](spike/) until the slice closes: `cases.py` builds the page of cases and checks the mechanism against it.

The design asked for three changes to the spec and one fix of the Capture that the spec did not name. The maintainer accepted the four; they are listed under "What the maintainer accepted".

---

## Architecture Overview

```mermaid
graph TD
    C[MCP client] -->|call_tool| T[tools/detect_visual_bugs.py<br/>asks for covered text when overlap runs]
    T -->|capture url, viewport, "*", covered_text| K[capture.py<br/>only importer of playwright]
    K --> J[js/collect_elements.js<br/>keeps its element list on the page]
    K --> F[js/fill_text.js]
    K --> O[js/covered_text.js<br/>highlights, what is painted, hit testing]
    K -->|screenshots, boxes| P[covered.py<br/>channels, candidates, groups, Hidden ink]
    K -->|Capture: Element.covered_text| T
    T -->|Capture| X[checks/overlap.py<br/>thresholds, Coverer, severity]
    X -->|Finding list| T
```

A Capture taken with `covered_text=True` gives every element with own text that may be covered three facts (`Element.covered_text`): its Text ink and its Hidden ink in pixels, and the Other elements that hit testing gives at its Hidden ink, each with how many pixels it got and whether it is in a Raised layer. The Check is arithmetic on those facts.

The Capture measures them after the layers of AD-004, in two phases and then hit testing.

**How ink of one text is told from everything else.** The CSS Custom Highlight API: a `Highlight` over a `Range` on each own text node and a rule `::highlight(name) { color: ... }`. Two screenshots, the highlight in a channel colour and then in black; the difference in that channel is the ink of those glyphs and of nothing else, whatever is painted around, under or over them. Texts whose own-text boxes cross get different channels, so one pair of screenshots separates three texts painted over each other. A fourth takes another pair (a "round").

**Phase 1, four full-page screenshots.** The ink of every text as painted (the page untouched but for the highlights), and with only glyphs painted (every element `visibility: hidden`, the elements with own text `visible` with no background, border, shadow or pseudo-element). A text is done, with no Hidden ink worth reporting, when what it loses between the two plus what another text's glyphs could be hiding is under the reporting threshold of its glyph ink. The bound is sound: glyphs-only ink is never less than Text ink, and what a descendant hides counts as lost.

**Phase 2, clipped screenshots, only for the texts left.** Each one alone with what is inside it (Text ink), and alone plus its Silent layers. Texts share a pair of screenshots when nothing one shows touches the text of another. Hidden ink is Text ink that is unseen as painted and seen with the Silent layers.

**Hit testing, only for the texts at or over the threshold.** `elementsFromPoint` at the Hidden ink, the page scrolled a viewport at a time, at most 20,000 points per Capture.

### Approaches considered

All three deliver the same Check; they differ in how the Capture learns what is hidden.

| Approach | What it is | Verdict |
| --- | --- | --- |
| **A. Two phases, on request (chosen)** | Four full-page screenshots find the texts that may be covered; only those are measured alone, in clipped screenshots | Chosen. Spiked: every case of the spec gives the value of its criterion. On a real page of 710 texts, 4 go to phase 2 |
| B. Every text measured alone | No first phase: every text goes into a group and each group is a pair of full-page screenshots | Rejected. Same values, simpler by one rule, but the cost grows with the groups: 12 full-page screenshots on a page of 190 texts in the spike of 2026-10-10 (6.7s) |
| C. Boxes and hit testing, the crop as confirmation | The roadmap's wording taken literally: boxes that intersect, `elementFromPoint` differs, then look at the pixels of the box | Rejected. It cannot give the Hidden share: the pixels inside a box do not say whose glyph they are (AD-004), a stretched link is given by hit testing over 100% of a text it hides none of, and text under text has no cover with a box |

### What the spike showed

| Case | Result |
| --- | --- |
| The cases of the spec on one page (48 texts) | 24 texts come out covered at or over the threshold with a Coverer: the 23 the criteria ask for, each with the percent, the Coverer and the Raised layer of its criterion, and `#transparent-text`, which the Check drops by its fill colour (OVL-38). The values: 50, 25, 10 and 20 (OVL-02, OVL-05), the four edges at 10 (OVL-07 to OVL-09), the middle line and the second text node (OVL-10, OVL-11), the veils (OVL-12, OVL-22), the shadow tree (OVL-13, OVL-30), inside one dialog and one `fixed` element (OVL-15, OVL-16), 24 for 24.5% (OVL-49), every severity case (OVL-40 to OVL-46), `#mixed`, `#two-covers`, `#tie` (OVL-50 to OVL-52). No other text reaches the threshold with a Coverer: the stretched link, the cover of `opacity: 0`, every Silent layer of OVL-23 to OVL-29, the descendant, the badge, the caption; `#under-ghost` is half hidden and has no Coverer (OVL-34) |
| The same page with the layers taken after the fills of AD-004 and hit testing at every second pixel | The same 24 |
| Text under text: `#collision` (two glyphs over ten), `#z-static` (a block pulled up by a negative margin) | 20 and 50. Phase 1 alone sees no loss, since the glyphs on top hide the ones below in both of its renders; the bound sends both to phase 2 |
| Every existing fixture (40 files) at 1440 × 900 and 390 × 844 | Reported: `#covered` in `low-contrast-bounds.html` (100) and `#veiled-most` in `low-contrast-reach.html` (100), as OVL-17 and OVL-18 ask. Nothing else, `text-clipped-clean.html` included (OVL-69) |
| A real page: 1440 × 11942, dark root, light and dark cards, tight headings, inline children, a sticky header, a fixed footer, stretched links, badges, 710 texts | 4 texts go to phase 2. One text over the threshold: the paragraph under a stray card, 17%, with the card as Coverer, hit tested below the first viewport. Two lines pulled 14px into each other hide 1% of each other: no Finding |
| The same glyphs measured over white, `#111` and `#888`, painted and alone | With `--disable-lcd-text`: 2707 text pixels every time for a red and for a blue highlight. Without the flag: 2798 painted on white against 3681 alone over the dark root |
| A green highlight | At `rgb(0, 255, 0)`: 2707 on white, 3272 on dark. Chromium paints a bright glyph fatter. At 88 or less: 2707 (once 2708) |
| Without `--disable-lcd-text` | `#veil-55` gives 95 for 100. The real page sends 157 texts to phase 2 and makes 53,432 hit tests |
| The existing suite with Chromium launched with `--disable-lcd-text` | 237 passed, as without it |
| 100 texts half covered, in one column (1440 × 5000) and in four (1440 × 1250) | 100 Findings of 50% with their own cover. 200,000 hit tests take 9.8s; 12,500 (every fourth pixel) take 0.7s and name the same 100 Coverers |

Cost, at 1440 × 900, on a warm browser:

| Page | Capture today | Added by covered text |
| --- | --- | --- |
| `selectors.html`, 1440 × 1210, 25 texts, none covered | 0.9s | 0.4s |
| The cases of the spec, 1440 × 2360, 37 texts in phase 2 | 1.1s | 1.3s |
| 100 half-covered texts, one column | 1.5s | 1.9s |
| `pixel-cost.html`, 1440 × 11700, one text | 2.4s | 2.1s |
| The real page of 710 texts | 3.5s | 4.0s, of which 2.7s are phase 1 |

A full-page screenshot costs about 0.03s per megapixel, so phase 1 about doubles a Capture. That is why the layers are taken on request.

### A fault of the Capture found on the way

On Windows, the first screenshot that reaches beyond the viewport changes the font Chromium uses for the generic `monospace` family, from Consolas to Courier New, and the page is laid out again. Spiked: a `code` element goes from 122.36px to 132.83px wide, each of 14 sections of the real page grows by 1px, the page from 11944px to 11958px. The screenshot that causes it is already of the new layout, cut at the old height; a viewport screenshot and a resize do not cause it; a second screenshot changes nothing more.

Today the collector runs before that first screenshot (`capture.py:128-137`). On such a page every box is of the old layout and every pixel of the new one, and `pixels` is shorter than `background` and `ink`, which AD-004 says have one size. This is in 0.1.0 and touches every tool.

A clipped screenshot of 16 × 16 pixels taken with `full_page=True` before anything is measured causes the change once, for about 0.09s. With it the real page gives the results above; without it its `code` elements were read 15px off and reported as covered.

### What the maintainer accepted

1. **Spec, Terms, "Seen"**: a pixel of text ink is seen when the ink that shows is at least half of the ink that pixel has alone, not at least 128. Under a veil of 0.45 the seams between Ahem glyphs fall under 128 and `#veil-45` would report 10%.
2. **Spec, Assumptions**: text is rasterized in grayscale in every Capture (`--disable-lcd-text`). It changes the pixels of every tool on Windows; the existing suite passes with it. AD-006.
3. **Spec, Terms, "Coverer"**: hit testing is done with the page scrolled a viewport at a time, and an element the scroll moved from where the Capture has it is passed over for the next one at the point. When a Capture has more than 20,000 pixels of Hidden ink to test, every nth pixel of every nth row is tested, and each text at least once: the Coverer is then the largest part of a sample.
4. **The Capture fault above**: fixed in this slice, as its first task, because every box this Check reads depends on it. It changes `inspect_element` and the other three Checks only on a page where they are wrong today. Recorded as issue #18; the spec's Out of Scope names it.

---

## Code Reuse Analysis

### Existing Components to Leverage

| Component | Location | How to Use |
| --- | --- | --- |
| `capture()` | `src/squint_mcp/capture.py:87` | One more keyword, `covered_text`; the new work goes after the fills at line 144 |
| `_screenshot` | `src/squint_mcp/capture.py:77` | Gains an optional clip, in page coordinates |
| The collector's sorted element list | `src/squint_mcp/js/collect_elements.js:185` | Kept on the page as `globalThis.__squintElements`, so the cover script speaks of elements by their index in `Capture.elements` |
| `Element.own_text_boxes` | `src/squint_mcp/models.py:58` | The region of a text; the cover script does not send boxes again |
| The walk over open shadow roots, one `<style>` per root | `src/squint_mcp/js/fill_text.js:8-23` | Same in `covered_text.js` |
| `_bounds` | `src/squint_mcp/vision.py:22` | Rounds a fractional box outwards and clamps it to the page; made public for `covered.py` |
| `TEXT_INK_MIN` | `src/squint_mcp/config.py:117` | "Covers by at least half" for Text ink |
| The shape of a Check module | `src/squint_mcp/checks/low_contrast_real.py` | Guards, `_finding`, `check`; the parse of the fill colour for alpha 0 |
| `CHECKS` | `src/squint_mcp/checks/__init__.py:14` | One more entry; the unknown-Check message already sorts the names |
| `helpers.py`, session `client` | `tests/` | `detect`, `findings_on`, `fixture_url`, `images` reused unchanged |

### Integration Points

| System | Integration Method |
| --- | --- |
| `detect_visual_bugs` | Passes `covered_text` when a Check that reads it is among the names; docstring names the new Check. Sort and crops untouched |
| `inspect_element` | Unchanged. It never asks for covered text and builds its result from `INSPECT_COMPUTED_PROPERTIES`, so `z-index` does not reach it |
| `BrowserSession` | Launches with `config.CHROMIUM_ARGS` |

---

## Components

### Launch and first screenshot (`capture.py`)

- **Purpose**: the same rasterization for text alone and as painted, and one layout for boxes and pixels.
- **Interfaces**:
  - `self._playwright.chromium.launch(args=list(config.CHROMIUM_ARGS))`
  - `_settle_layout(page)`: one `page.screenshot(full_page=True, clip=16 × 16 at the origin)`, discarded, right after the idle wait and before `matches.count()`. Retried once on a `PlaywrightError`: the spike saw `Unable to capture screenshot` twice in about 240 clips of 1 × 1 and never in 190 of 16 × 16
- **Reuses**: nothing

### Collector (`collect_elements.js`)

- **Purpose**: unchanged; it leaves its element list on the page.
- **Interfaces**: before returning, `globalThis.__squintElements = sorted`. `z-index` arrives through `properties`
- **Reuses**: the list it already sorts

### Cover script (`covered_text.js`)

- **Purpose**: everything the Capture does in the page for covered text. Installed once per Capture, after the fills.
- **Location**: `src/squint_mcp/js/covered_text.js`
- **Interfaces**: `({ roles }) => texts`, which installs `globalThis.__squintCovered` and returns, for every element of the list that has `visibility: visible` and an own text node with a box: `index`, `ancestors` (indexes, nearest first, a shadow root continuing at its host), `region` (the bounding box of the element and of every visible element inside it) and `layers` (the indexes of its Silent layers: the roots that are neither it nor one of its ancestors). Then, on the installed object:
  - `mark({ index: channel })`: one `Highlight` per channel over the `Range`s of the own text nodes of those texts
  - `ink(on)`: the three highlight colours, `rgb(255, 0, 0)`, `rgb(0, 64, 0)` and `rgb(0, 0, 255)`, or black for all
  - `show("page")`, `show("glyphs", indexes)`, `show("alone", indexes, withLayers)`: one `<style>` per root and a `data-squint-show` or `data-squint-text` attribute on what stays visible. Only elements that were `visible` before are ever shown, so text of `visibility: hidden` has no ink (OVL-37)
  - `hit(jobs, step)`: `jobs` are the runs `[y, x0, x1]` of Hidden ink of each text. Per point, the first element of `document.elementsFromPoint` whose box is where the list has it, continued into open shadow roots; kept when it is an Other element. Returns, per text, the Other elements in document order with how many points each got and whether it is in a Raised layer
- **A Silent layer root**: a `role` attribute that, trimmed and in lower case, is one of `roles`; a `dialog` with `open`; `:popover-open`; a computed `position` of `fixed` or `sticky`
- **A Raised layer**: the element given, or an ancestor of it that is not an ancestor of the text, with a computed `position` other than `static` and a `z-index` above 0
- **Dependencies**: the collector's list
- **Reuses**: the root walk of `fill_text.js`

### Covered text arithmetic (`covered.py`)

- **Purpose**: everything about covered text that needs no browser: which channel a text takes, which texts go to phase 2, which share a screenshot, what is hidden, where to hit test.
- **Location**: `src/squint_mcp/covered.py`. No `playwright` (ADR-0002)
- **Interfaces**:
  - `assign_channels(texts) -> int`: gives each text a round and a channel so that two texts whose own-text boxes cross never share both; returns the number of rounds. Greedy, in document order, over a grid of 64px cells
  - `ink_layers(on, off) -> tuple[Image, Image, Image]`: `ImageChops.subtract` per channel, the green one times 4
  - `may_be_covered(text, glyphs, painted) -> bool`: phase 1. Inside the own-text boxes: glyph ink of at least `TEXT_INK_MIN`; of it, the pixels where twice the painted ink is under the glyph ink; and the pixels where another channel has ink of 64 or more and this one has none. True when the last two together reach `OVERLAP_MIN_HIDDEN_PERCENT` of the first
  - `groups(candidates) -> list[list[Text]]`: greedy, in document order. Two texts are kept apart when one is an ancestor of the other or the `region` of one crosses the own-text boxes of the other
  - `hidden_ink(text, alone, painted, layered) -> tuple[int, int, Image]`: Text ink is `alone >= TEXT_INK_MIN` inside the boxes; a pixel is unseen in a layer when twice the layer is under `alone`; Hidden ink is Text ink unseen in `painted` and not unseen in `layered`. In integers, on Pillow point tables and `ImageChops`, counted with `histogram`
  - `runs(mask, origin) -> list[tuple[int, int, int]]` and `hit_step(pixels) -> int`: `max(1, ceil(sqrt(pixels / HIT_TEST_MAX)))`
- **Dependencies**: Pillow, `config`, `models`, `vision._bounds`

### Capture (`capture.py`, `models.py`)

- **Purpose**: unchanged; covered text on request.
- **Interfaces**: `capture(session, url, viewport, selector, *, covered_text: bool = False)`.
- **Order inside `capture()`**: load, stabilize, idle wait, `_settle_layout`, collect, `scroll_width`, `pixels`, the three fills, then, when asked:
  1. install the cover script; `assign_channels`
  2. per round: `mark`, `show("page")`, a pair of screenshots; `show("glyphs", ...)`, a pair
  3. `may_be_covered` for every text; `groups` of the ones left
  4. per group: `mark` all on one channel, `show("alone", group, false)`, a pair clipped to the group's boxes; then, per distinct `layers` among the members that have any, `show("alone", members, true)` and a pair
  5. `hidden_ink` for each; `hit` for the ones at or over the threshold
  6. `Element.covered_text` for every text of phase 2
- A text that never reaches phase 2 keeps `covered_text` at `None`.

### Check (`checks/overlap.py`)

- **Purpose**: `Capture -> list[Finding]`.
- **Rules**, in order, for each element:
  1. `covered_text` is not `None` and its `ink` is above 0.
  2. `computed["-webkit-text-fill-color"]` does not parse to an alpha of 0 (OVL-38). Text of `visibility: hidden` or `opacity: 0` needs no rule: it has no Text ink (OVL-37, OVL-39).
  3. `hidden * 100 >= OVERLAP_MIN_HIDDEN_PERCENT * ink`.
  4. `covers` is not empty (OVL-34). The Coverer is the one with the most pixels; the list is in document order, so the first maximum is the tie rule (OVL-52).
  5. `major` when `hidden * 100 >= OVERLAP_MAJOR_HIDDEN_PERCENT * ink`, else `minor`; one level lower when the Coverer is `raised`.
- **Finding**: `hiddenPercent` is `hidden * 100 // ink`; `coveredBy` the Coverer's selector; `computed` holds `position` and `z-index` of the covered element.
- **Dependencies**: `config`, `models`. No `playwright`, no pixels

### Tool (`tools/detect_visual_bugs.py`, `checks/__init__.py`)

- `checks/__init__.py` gains `COVERED_TEXT_CHECKS = frozenset({"overlap"})`, the Checks that read `Element.covered_text`.
- The tool calls `capture(..., covered_text=not COVERED_TEXT_CHECKS.isdisjoint(names))`.

---

## Data Models

```python
class Cover(BaseModel):
    """An Other element that hit testing gives where ink of a text is hidden."""

    selector: str
    pixels: int
    """How many of the hit-tested pixels it was given at."""
    raised: bool
    """Whether it, or an ancestor of it that is not an ancestor of the text, has
    a `position` other than `static` and a `z-index` above 0."""


class CoveredText(BaseModel):
    ink: int
    """The pixels the own text covers by at least half, painted alone."""
    hidden: int
    """Those of them that are unseen on the page and that its Silent layers
    alone would leave seen."""
    covers: list[Cover]
    """In document order."""


class Element(BaseModel):
    ...
    covered_text: CoveredText | None = None
    """None when the Capture was not asked for it, and for a text that cannot
    reach the reporting threshold."""
```

Config (each with its source in a comment):

| Name | Value | Source |
| --- | --- | --- |
| `CHROMIUM_ARGS` | `("--disable-lcd-text",)` | Squint default, AD-006 |
| `CAPTURE_COMPUTED_PROPERTIES` | adds `"z-index"` | Spec, Assumptions |
| `OVERLAP_MIN_HIDDEN_PERCENT` | 10 | Squint default (spec, Assumptions) |
| `OVERLAP_MAJOR_HIDDEN_PERCENT` | 25 | Squint default (spec, Assumptions) |
| `SILENT_LAYER_ROLES` | `("menu", "listbox", "tooltip", "dialog", "alertdialog")` | WAI-ARIA 1.2 roles; decided with the maintainer |
| `HIT_TEST_MAX` | 20,000 | Squint default, measured: 30 to 60 microseconds a point, so about a second per Capture at most |

---

## Error Handling Strategy

| Error Scenario | Handling | User Impact |
| --- | --- | --- |
| A cover script call or a layer screenshot fails | Same path as any Capture failure (AD-002) | The call fails; no partial result |
| The layers push a slow page past 30s | The existing total timeout | `Timed out after 30s.` |
| The first small screenshot fails twice | Same path as any Capture failure | The call fails |
| More Hidden ink than `HIT_TEST_MAX` | A wider step, and one point at least for each text | The Coverer of a text comes from a sample |
| `overlap` is given a Capture taken without covered text | No element has `covered_text` | No Finding. Only the tool calls Checks, and it asks |

---

## Risks & Concerns

| Concern | Location (file:line) | Impact | Mitigation |
| --- | --- | --- | --- |
| The collector runs before the first screenshot beyond the viewport, which on Windows relays out a page that uses the generic `monospace` font | `src/squint_mcp/capture.py:128-137` | Boxes of one layout, pixels of another; `pixels` shorter than `background` and `ink`. In 0.1.0, every tool | `_settle_layout`, the first task of this slice. Not reproducible on the CI's Linux, so no test holds it: recorded in the CHANGELOG and in a comment |
| Every Capture pays for layers only some read | `src/squint_mcp/capture.py:140` (`ponytail:`) | Covered text about doubles a Capture | On request. The three layers of AD-004 stay as they are |
| The pixel work runs in the event loop | `src/squint_mcp/covered.py` | 0.7s for 710 texts during which a cancellation waits | As the Checks today; the roadmap left cancellable pixel work out in slice 6 |
| Hit testing scrolls the page, and a page can react to scroll | `covered_text.js`, `hit` | A header that shrinks or content that loads on scroll moves what is hit tested | Hit testing is the last thing a Capture does, after every screenshot; an element that moved is passed over. A wrong or missing `coveredBy` is possible, never a wrong percent |
| A pseudo-element of one text of a group, positioned over another text of the group | `covered.py`, `groups` | That other text is measured with less Text ink than it has: a missed Finding | Accepted and marked `ponytail:`; measure a text that shows a positioned pseudo-element in a group of its own if it happens |
| A text with a very large region (own text nodes at the top and at the bottom of a page) is cropped whole | `covered.py`, `hidden_ink` | Pixel work on the full page for that text | Accepted; `ponytail:` |
| More than three texts crossing in one place | `covered.py`, `assign_channels` | Each further round is four more full-page screenshots | Accepted; the real page needed one round |
| A highlight recolours an underline that follows `currentColor` | page content | The underline counts as ink of its text, in every layer alike | Accepted; shares are of the same ink |
| An element with `mix-blend-mode`, on the text or around it | page content | The channels do not hold what the highlights painted: no Text ink, no Finding | Known limit |
| A `filter` that changes colours, on the text or around it | `covered_text.js` | The same, for every text of a grey-scaled section or of a page inverted at its root | Fixed after the third validation pass: the cover script takes the functions that change colours out of every `filter` before it measures, and leaves the others and the `filter` itself, so that nothing moves (spiked: `none` moves what is positioned inside) |
| The page's own `::highlight()` or `::selection` rules | page content | Could repaint the glyphs the Capture marks | The rules of the Capture are `!important`; the page has no selection in a fresh context |
| A page with a `style-src` policy that refuses inline styles would refuse the styles the Capture injects, the fills of AD-004 included | `src/squint_mcp/js/fill_text.js:18`, `stabilize.js:17` | Not verified. If so, no ink on such a page for any Check | Out of this slice; a follow-up issue to check `bypass_csp` on the context |

---

## Tech Decisions (only non-obvious ones)

| Decision | Choice | Rationale |
| --- | --- | --- |
| How glyphs are told apart | `::highlight() { color }` over own text nodes | Spiked: it repaints the glyphs even over an explicit `-webkit-text-fill-color`, reaches open shadow trees and touches no layout. The fill of AD-004 cannot single out one element's own text from its children's |
| Highlight colours | Red and blue at 255, green at 64, against black | Spiked: Chromium paints a bright green glyph fatter than a black one over a dark backdrop; at 64 the mask is the black one. Two exact channels alone would cost a round for a paragraph, a link in it and bold text in the link |
| No white backdrop forced for the renders alone | The root background stays | With the colours above and grayscale text the ink is the same over white, dark and grey; the open point of 2026-10-10 came from a white highlight |
| "Seen" | Twice the ink that shows is at least the ink alone, per pixel | The same veil gives the same answer on a full glyph and on an anti-aliased edge |
| Phase 1 bound | Lost plus possibly-collided, against glyph ink | Sound for the threshold, and the only texts it sends on without need are those whose boxes hold another text's glyphs |
| What phase 2 clips to | The union of the group's own-text boxes | Clipped pairs cost by the megapixel; a group scattered over the page costs a full-page pair |
| Hit testing | `elementsFromPoint`, first element the scroll did not move | `elementFromPoint` answers only inside the viewport; a fixed footer over the point is not what covers the text in the Capture |
| The cap | One step for the whole Capture, at least one point per text | Under the cap every pixel is tested and the fixtures are exact; over it no text is left without a Coverer |
| Where the rules live | Silent and Raised layers in the cover script, thresholds and the Coverer in the Check | The page has to know the Silent layers to paint them; ancestry is not in a Capture. The Check stays a function of numbers |
| What `covered_text` is for a text not measured alone | `None` | Its glyph ink from phase 1 is not its Text ink: a descendant may cover part of it |

### Project-level decisions

AD-005 (covered text measured on request, through CSS highlights and hit testing) and AD-006 (`--disable-lcd-text` and the first small screenshot) are in `.specs/STATE.md`.
