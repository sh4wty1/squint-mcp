# overlap Context

**Gathered:** 2026-10-10
**Spec:** `.specs/features/overlap/spec.md`
**Status:** Ready for design

---

## Feature Boundary

Slice 8 of `docs/ROADMAP.md`: the `overlap` Check, the decision on its false positives, its fixtures with intended overlaps that must not be reported, and the CHANGELOG entry. No interaction states and no iframes.

Standing rule from the maintainer: the roadmap and `docs/SPEC.md` are followed literally. Anything they assign to a later slice or leave out is out of scope without discussion.

---

## Implementation Decisions

The maintainer took the four defaults proposed, at Quick pace, with the answer "Segue os defaults" (2026-10-10).

### What marks an overlap as intended

- Silent: an element that declares itself a layer, and what is inside it. That is a `role` of `menu`, `listbox`, `tooltip` or `dialog`, a `dialog` element that is open, and an open popover.
- Everything else that covers text is reported.
- The severity is lower when what covers the text has a positive `z-index`.

### Reach

- Only the own text of an element, as in the other three Checks. Images and form controls are never "covered content" in this slice.

### Covering without hiding

- Text painted over text is reported too: the negative-margin case, where both texts stay on the page and neither can be read.
- A translucent veil with no text is left to `low-contrast-real`.

### `fixed` and `sticky` elements

- What a `fixed` or `sticky` element covers is never reported in this slice.

### The Finding

- It sits on the covered element. The selector of what covers it goes in `evidence.measured`.
- The severity is `major` or `minor` by the share of the text that is covered.

### Agent's Discretion

None. Every remaining choice is logged in the spec's Assumptions table with its default and rationale.

### Declined / Undiscussed Gray Areas → Assumptions

Logged in the spec's Assumptions & Open Questions: the two share thresholds, the use of `info` for a small cover by a raised layer, where a veil stops being `low-contrast-real`'s and becomes a cover, `alertdialog` in the list of roles, which element is named when several cover one text, the truncation of the share, the evidence keys, the message wording, covers that hit testing does not see, and a descendant that covers its parent's text.

---

## Specific References

A spike against real Chromium on 2026-10-10 (outside the repository) measured 20 patterns. It grounds the decisions above:

- A closed menu (`display: none`, `visibility: hidden`, `opacity: 0`) and the stretched link of a card (`a::after` with `inset: 0`) are given by hit testing over 52% to 100% of the text under them and hide none of its ink. The pixels have to confirm.
- A badge on an avatar or on a button touches no text. A sticky header at scroll zero is in the flow and covers nothing.
- An open menu, an open tooltip, an open dialog with its backdrop and stacked slides do hide text: 27% to 100% of its ink.
- In a Capture a `fixed` element sits where it is in the first viewport: a banner at the bottom of a 900px viewport covers rows 830 to 899 of the page, which scrolling uncovers. A `fixed` bar at the top covers the top of the page, which scrolling does not.
- Real bugs hide 13% to 84% of the ink: a stray card 36%, an image 84%, a shifted label 31%, a column over a column 19%, a corner 13%.
- Two lines of a real font pulled into each other by a negative margin hide 15% of the ink of the line below: the glyphs on top cover that much of it.
- No CSS signal alone tells an intended layer from a bug. The covered share does not (slides and a fixed bar cover 100%), and `z-index` is also set on elements that collide at a narrow viewport.
- Of the existing fixtures, only `#covered` in `low-contrast-bounds.html` and `#veiled-most` in `low-contrast-reach.html` hold covered text. The tests that read those two files name their Check.

### Design spike (2026-10-10 and 2026-10-11, unfinished)

A second spike against real Chromium (headless shell 153, `playwright 1.63`, Windows), outside the repository, on a page holding the cases of the spec. Design is not closed: AD-005 and `design.md` are not written. What it measured:

**A mechanism that gives the Terms.** In batches, not per element:

1. The ink of a text alone: every element gets `visibility: hidden !important` but the ones to paint, which get `visible`; a mark on each element (`data-*` attribute) and one style per root. Clipping, opacity and transforms of hidden ancestors still apply, so text clipped away has no ink.
2. The glyphs of own text only are told apart with the CSS Custom Highlight API: a `Highlight` over the `Range` of each own text node and `::highlight(name) { color: ... }`. Two screenshots, the highlight red, green or blue and then black; the difference in one channel is the ink. `color` in a highlight repaints the glyphs even over an explicit `-webkit-text-fill-color`; `-webkit-text-fill-color` inside `::highlight()` is ignored. A rule in the document reaches open shadow trees.
3. Texts whose own-text boxes cross take different channels, so one pair of screenshots separates up to three texts painted over each other.
4. Three layers per text: alone with its subtree (Text ink), as painted (seen), and alone plus its Silent layers. Hidden ink is Text ink that is unseen as painted and seen with the Silent layers. Texts are grouped by the Silent layers that hold them and kept apart when something one of them shows is painted over another.
5. The Coverer: `elementFromPoint` at the pixels of the Hidden ink, sent back to the page as runs, the page scrolled a viewport at a time. An element the scroll moved from where the Capture has it (a `fixed` or stuck `sticky` one) is passed over.

**Results.** Every case measured gave the value of its criterion: 50, 25, 10 and 20 with `coveredBy` (OVL-02, OVL-05), the three edges and the middle line and the second text node at 10 (OVL-07 to OVL-11), a veil of 0.55 at 100 and of 0.45 at 0 (OVL-12, OVL-22), the shadow tree (OVL-13), inside one dialog and inside one `fixed` element at 50 (OVL-15, OVL-16), 24 for 24.5% (OVL-49), `#mixed`, `#two-covers` and `#tie` (OVL-50 to OVL-52), text under text by a negative margin (OVL-46), and no Hidden ink under each Silent layer of OVL-23 to OVL-30, under an `opacity: 0` cover, a stretched link, a descendant or a badge. A cover of `pointer-events: none` hides 50% and has no Coverer. On a page of 190 real-font texts, only the paragraph under a card lost ink (37%).

**Three things the spec does not say and the mechanism needs.**

- "Seen" has to be relative: a pixel is seen when the ink that shows is at least half of the ink of that pixel alone. With the absolute bound of `low-contrast-real` (ink of 128), the seams between Ahem glyphs fall under 128 beneath a veil of 0.45 and `#veil-45` reports 10%.
- The text has to be rasterized the same way alone and as painted. Chromium picks subpixel or grayscale anti-aliasing per page state: the same glyph edge was 168 alone and 225 as painted, and `#veil-55` gave 95%. Launching Chromium with `--disable-lcd-text` makes both grayscale and the values exact. It changes the pixels of every Capture on Windows; the existing suite has not been run with it.
- `elementFromPoint` answers only inside the viewport, and at whole pixels (`elementsFromPoint` rounds a half pixel up). Hit testing below the first viewport needs the scroll and the rule of point 5.

**Cost** (1440 × 900 viewport, load and idle wait included):

| Page | Today | With the mechanism |
| --- | --- | --- |
| 60 cases, 1440 × 3660, 4 groups | 1.2s | 3.2s (20 more screenshots, 16 of them clipped) |
| 100 texts half covered in one column, 1440 × 6000 (OVL-60) | 2.5s | 10.8s, of which 6.6s are 200,000 hit tests; 3.8s with hit testing on a lattice of every third pixel |
| The same in four columns, 1440 × 1500 | 1.1s | 7.0s, of which 5.3s are hit tests |
| 190 real-font texts, 1440 × 9972 | 2.3s | 6.7s in the first shape (12 full-page screenshots) |

A full-page screenshot costs about 0.03s per megapixel; a hit test 13 to 33 microseconds. All 100 texts of the OVL-60 page came out at 50% with their own cover. The limit of 30s holds.

**Open when the spike stopped.**

- The cheaper shape (`spike2.py`: four full-page screenshots for every Capture, the rest clipped to the texts that lose ink) misses text painted over text (`#collision`, `#z-static`): with all glyphs painted alone, the text on top still hides the one below. Texts whose boxes cross have to go to the second phase whatever the first one says, as the first shape (`spike.py`) did.
- Whether the alone render stays the thinner of the two on a page with a dark root background and a light card (ink measured over a dark backdrop is wider than over a white one: 2118 against 1704 pixels for the same text).
- A cap on hit tests per Capture and what a text beyond it gets.
- Whether the Capture takes these layers on every call or only when `overlap` is asked for.

---

## Deferred Ideas

- Content at the top of a page that a `fixed` header covers and scrolling cannot uncover.
- Covered images and form controls.
- A cover that hit testing does not see (`pointer-events: none`).
- Text covered by one of its own descendants.
- Stacked slides and tab panels kept on the page under the active one: reported today, at a lower severity when the active one has a positive `z-index`.
