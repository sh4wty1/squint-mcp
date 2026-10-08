# low-contrast-real Design

**Spec**: `.specs/features/low-contrast-real/spec.md`
**Status**: Executed; not reviewed by the maintainer

Every choice marked "spiked" was run against `playwright 1.63` and real Chromium (headless shell 153, build 1243) on 2026-10-08, on a page holding the cases of the spec. Conforms to AD-001, AD-002 and AD-003; adds AD-004.

---

## Architecture Overview

```mermaid
graph TD
    C[MCP client] -->|call_tool| T[tools/detect_visual_bugs.py<br/>order across Checks, crops, result]
    T -->|capture url, viewport, "*"| K[capture.py<br/>only importer of playwright]
    K --> J[js/collect_elements.js<br/>+ ownTextBoxes, opacity]
    K --> F[js/fill_text.js<br/>force the fill colour of all text]
    K -->|Capture: pixels, background, ink| T
    T -->|Capture| X[checks/low_contrast_real.py<br/>WCAG ratio, worst part, thresholds]
    X -->|background, ink, boxes| V[vision.py<br/>text_backgrounds]
    X -->|Finding list| T
```

The Capture gains two pixel layers next to `pixels`, both the size of the page:

- `background`: the page with no text painted.
- `ink`: how much text ink each pixel gets, 0 to 255.

`capture()` takes them after the screenshot it already takes: it forces `-webkit-text-fill-color` on every element (document and open shadow roots) to `transparent`, then black, then white, with a screenshot after each. The transparent one is `background`. `ink` is the difference between the black one and the white one: a pixel fully covered by a glyph differs by 255, an anti-aliased edge by its coverage, anything that is not text by 0.

The Check then needs no geometry of its own. The text pixels of an element (spec, Terms) are the pixels inside the boxes of its own text nodes whose `ink` is at least 128. Their Background is `background` at the same place.

### Approaches considered

All three deliver the same Check; they differ in how the background behind text is known.

| Approach | What it is | Verdict |
| --- | --- | --- |
| **A. Text layers in the Capture (chosen)** | Three more screenshots with the text fill forced: none, black, white | Chosen. Spiked: the layers give exactly the Terms of the spec. Clipped, covered and hidden text has no ink; text of the colour of its background still has ink (LCR-09); borders, underlines and shadows are untouched because only the fill of glyphs changes |
| B. Sample the one screenshot inside the text's box | Take the colours in the box that are not the text colour | Rejected. Anti-aliased edges are blends of text and background and would be read as a low-contrast background; text of the background's colour cannot be told from no text; the box says nothing about clipping or covering |
| C. Two screenshots: normal and text hidden | Text pixels are where the two differ | Rejected. Text of the same colour as its background differs nowhere, so LCR-09 cannot be met, and over a photo the mask has holes wherever a pixel happens to match |

Cost of A, spiked on a 1440 × 900 page: 0.12s for the three screenshots together, against 0.21s for the first. Accepted; every Capture pays it, `inspect_element` included (see Risks).

### What the spike showed

| Case | Result |
| --- | --- |
| Ahem, 20px/30px, ten glyphs at x 40 | One own-text box of 200 × 20 starting 5px under the top of the line; 4000 pixels with ink of 243 or more; the columns just outside have ink of 8 and 22 |
| Hard-stop gradient under the last 40px | Backgrounds behind the text: 3200 of `(0, 0, 0)`, 800 of `(204, 204, 204)`, nothing else |
| Hard-stop gradient under the last 2 rows | 3600 and 400 |
| White text on white | 4000 text pixels, all with a white background |
| `visibility: hidden`; a 1px box clipping all its text; text under an opaque element | No pixel with ink |
| Text clipped to 150px of 200px | 3000 text pixels |
| Arial 16px, with a `currentColor` border and an underline | 560 of 2210 box pixels have ink of 128 or more; outside the ink the transparent layer equals the normal screenshot on the whole page (0 pixels differ) |
| Ahem at 18.66px bold | 3553 text pixels, one background colour |
| `opacity: 0.5` on the parent | Ink of about half everywhere: the pixels cannot tell a faded text, the collector has to |

---

## Code Reuse Analysis

### Existing Components to Leverage

| Component | Location | How to Use |
| --- | --- | --- |
| `capture()` | `src/squint_mcp/capture.py:71` | Extended after the screenshot at line 120; signature unchanged |
| The walk over open shadow roots | `src/squint_mcp/js/stabilize.js:8-13` | Same walk in `fill_text.js`, one `<style>` per root |
| The `Range` over own text nodes | `src/squint_mcp/js/collect_elements.js:117-126` | The same loop also collects every rect, for `ownTextBoxes` |
| `Element`, `Capture`, `Evidence`, `Finding` | `src/squint_mcp/models.py` | `Element` gains two fields, `Capture` two, `Evidence.measured` one value type |
| `_region` | `src/squint_mcp/vision.py:20` | Rounds a fractional box outwards and clamps it to the page; used for each text box |
| `Image.getcolors` | Pillow | Counts the colours of a region in C, as `sample_colors` does. With the ink mask as alpha band it counts only text pixels |
| `text_clipped.py` | `src/squint_mcp/checks/text_clipped.py` | The shape of a Check module: guards, `_finding`, `check` |
| `CHECKS` | `src/squint_mcp/checks/__init__.py:14` | One more entry. The unknown-Check message already sorts the names |
| `helpers.py`, session `client` | `tests/` | `detect`, `findings_on`, `fixture_url`, `images` reused unchanged |

### Integration Points

| System | Integration Method |
| --- | --- |
| `detect_visual_bugs` | Sort key grows from severity to (severity, viewport, element position, Check name); docstring names the new Check |
| `inspect_element` | Unchanged. It builds its result field by field, so the new `Element` fields do not reach its output |

---

## Components

### Text fill script (`fill_text.js`)

- **Purpose**: Paint every glyph of the page in one colour, or not at all.
- **Location**: `src/squint_mcp/js/fill_text.js`
- **Interfaces**: `(color) => void`. Finds or creates one `<style data-squint-fill>` in the document and in every open shadow root and sets it to `*, *::before, *::after { -webkit-text-fill-color: <color> !important; }`
- **Dependencies**: none
- **Reuses**: the root walk of `stabilize.js`

### Collector (`collect_elements.js`)

- **Purpose**: unchanged; two more facts per element.
- **Interfaces**: adds to each element
  - `ownTextBoxes`: the client rects of the text nodes that are direct children, each `{x, y, w, h}` in page coordinates, zero-area rects left out
  - `opacity`: the element's computed `opacity` multiplied by that of every ancestor, a shadow root continuing at its host. Memoized per element, so the walk stays linear
- **Reuses**: the existing `Range` loop; `ownTextRight` stays as it is (slice 3 is closed)

### Capture (`capture.py`, `models.py`)

- **Purpose**: unchanged; two more layers.
- **Interfaces**:
  - `Capture.background: Image.Image`, RGB, the page without text
  - `Capture.ink: Image.Image`, mode `L`, `ImageChops.difference(black, white).convert("L")`
  - `Element.own_text_boxes: list[Box]`, `Element.opacity: float`
- **Order inside `capture()`**: collect, screenshot (`pixels`), then fill `transparent`, `rgb(0, 0, 0)`, `rgb(255, 255, 255)` with a screenshot after each. The collector runs before any fill so `computed` is the page's own

### Text background sampling (`vision.py`)

- **Purpose**: Say what is painted behind the text inside some boxes.
- **Interfaces**: `text_backgrounds(background: Image.Image, ink: Image.Image, boxes: list[Box]) -> list[tuple[int, tuple[int, int, int]]]`: `(count, rgb)` for every colour of `background` under a pixel whose `ink` is at least `config.TEXT_INK_MIN`, over all boxes. Empty when no pixel has ink.
- **How**: per box, `_region(..., 0)` of both layers; the ink region thresholded to 0/255 becomes the alpha band of the background region; `getcolors(maxcolors=area)`; keep the entries whose alpha is 255. Counts of the same colour in several boxes are added.
- **Dependencies**: Pillow only

### Check (`checks/low_contrast_real.py`)

- **Purpose**: `Capture -> list[Finding]` for SC 1.4.3.
- **Rules**, in order, for each element:
  1. `own_text`. Hidden text needs no rule of its own: it has no ink, so rule 4 drops it (LCR-16; spiked, and a visible child of a hidden parent is still judged).
  2. `opacity` is 1 (LCR-18, LCR-19).
  3. `computed["color"]` parses as `rgb(r, g, b)` or `rgba(r, g, b, a)` and `a` is above 0 (LCR-17). Any other serialization yields no Finding (see Risks).
  4. `text_backgrounds` over `own_text_boxes` is not empty (LCR-20, LCR-21, LCR-51).
  5. For each background colour: the text colour is `color` composited over it when `a < 1` (each channel rounded), and the ratio is `(L1 + 0.05) / (L2 + 0.05)` with the WCAG relative luminance.
  6. Worst part: colours sorted by ratio, ascending; the first one at which the cumulative count times 100 reaches `LOW_CONTRAST_WORST_PART_PERCENT` times the total. Integer arithmetic, so "exactly 10%" is exact (LCR-07, LCR-08, LCR-14, LCR-15).
  7. Required ratio: `CONTRAST_MIN_RATIO_LARGE` when `font-size >= LARGE_TEXT_MIN_PX`, or `font-size >= LARGE_BOLD_TEXT_MIN_PX` and `font-weight >= BOLD_MIN_WEIGHT`; else `CONTRAST_MIN_RATIO`.
  8. A Finding when the unrounded ratio is below the Required ratio; `major` when it is below `LOW_CONTRAST_MAJOR_BELOW_RATIO`.
- **Finding**: `contrastRatio` is `floor(ratio * 100) / 100`; the message prints it with two decimals and the Required ratio with `:g` (`4.5:1`, `3:1`); `textColor` and `sampledBackground` are the two colours of the worst-part entry as `#rrggbb`.
- **Dependencies**: `config`, `models`, `vision`. No `playwright` (ADR-0002)

### Order across Checks (`tools/detect_visual_bugs.py`)

- **Purpose**: LCR-37 to LCR-39, LCR-48 (issue #8).
- **How**: each Finding is kept with the index of its viewport, the position of its element in `capture.elements` (looked up by `selector`, which is unique on the page) and its Check name; the sort key is `(severity, viewport, position, check name)`. Crop allocation is untouched: it already takes the first five of the sorted list. No change to `Finding`.

---

## Data Models

```python
class Element(BaseModel):
    ...
    own_text_boxes: list[Box]
    """The boxes, as painted and in page coordinates, of the text nodes that are
    direct children."""
    opacity: float
    """The element's opacity multiplied by that of every ancestor."""


@dataclass(frozen=True)
class Capture:
    ...
    background: Image.Image
    """The full page in RGB with no text painted."""
    ink: Image.Image
    """How much text ink each pixel gets, 0 to 255, in mode L."""


class Evidence(BaseModel):
    measured: dict[str, int | float | str]
```

Config (each with its source in a comment):

| Name | Value | Source |
| --- | --- | --- |
| `CONTRAST_MIN_RATIO` | 4.5 | WCAG 2.2 SC 1.4.3 |
| `CONTRAST_MIN_RATIO_LARGE` | 3.0 | WCAG 2.2 SC 1.4.3 |
| `LARGE_TEXT_MIN_PX` | 24.0 | WCAG: 18pt |
| `LARGE_BOLD_TEXT_MIN_PX` | 18.66 | WCAG: 14pt bold, "typically 18.66px" |
| `BOLD_MIN_WEIGHT` | 700 | CSS: `bold` computes to 700 |
| `LOW_CONTRAST_MAJOR_BELOW_RATIO` | 3.0 | Squint default, decided with the maintainer; WCAG's own floor |
| `LOW_CONTRAST_WORST_PART_PERCENT` | 10 | Squint default (spec, Assumptions) |
| `TEXT_INK_MIN` | 128 | Squint default: a pixel at least half covered by a glyph is text |

---

## Error Handling Strategy

| Error Scenario | Handling | User Impact |
| --- | --- | --- |
| A fill script or a layer screenshot fails | Same path as any Capture failure (AD-002) | The call fails; no partial result |
| The three layers push a slow page past 30s | The existing total timeout | `Timed out after 30s.` |
| `color` is not `rgb()` / `rgba()` | The element yields no Finding | A missed Finding, never a wrong one |

---

## Risks & Concerns

| Concern | Location (file:line) | Impact | Mitigation |
| --- | --- | --- | --- |
| Every Capture takes four screenshots, `inspect_element` included, which reads only the first | `src/squint_mcp/capture.py:120` | About 0.12s more per call on a small page; more on a very tall one | Accepted and marked `ponytail:` in code; a flag on `capture()` is the upgrade if calls get slow |
| A page that repaints between the screenshots (a polling page, a video) gives ink where there is no text | `src/squint_mcp/capture.py:103` | Noise in `ink`, only inside text boxes, only on Captures already reported `stabilized: false` or with moving media | Accepted; animations are already stopped. The 10% share absorbs scattered pixels |
| Text with `-webkit-text-fill-color` set inline with `!important`, or painted by `background-clip: text` | page content | The fill cannot be forced: no ink, no Finding | Spec, Out of Scope |
| Ink inside an element's text boxes can belong to another element painted above it | `vision.text_backgrounds` | A covered text whose cover also holds text in the same place is judged on the cover's glyphs | Accepted as a known limit; noted in the Check's docstring |
| A text box is rounded outwards, so its edge column can hold the ink of a neighbouring inline element | `src/squint_mcp/vision.py:26-29` | At most one column of foreign ink per box | Accepted; far under the 10% share |
| `color` in a modern colour space serializes as `color(...)` or `oklch(...)` | Check rule 3 | No Finding for that text | Accepted for v0.1; marked `ponytail:` |
| Glyph rasterization differs between Windows (DirectWrite) and the Linux of CI (FreeType); the fixtures count exact shares of Ahem pixels | `tests/fixtures/low-contrast-bounds.html` | A row or column of Ahem falling under ink 128 on CI would move the 10% boundary cases | Spiked on Windows only: ink of the glyph block is 243 or more, the columns outside 22 or less. Slice 3's pixel tests on the same font pass on both. CI on the pull request is the check; if it fails there, the bands move off the exact boundary |
| The gate takes about 2m40s for 135 tests | `tests/` | Slow loop | None in this slice |

---

## Tech Decisions (only non-obvious ones)

| Decision | Choice | Rationale |
| --- | --- | --- |
| How text is hidden and marked | `-webkit-text-fill-color`, not `color` | `color` is `currentColor` for borders, outlines, shadows and underlines; changing it repaints them and they would count as ink or vanish from the background. Spiked: with the fill property nothing outside the glyphs changes |
| Two marker colours | Black and white | One marker is invisible on a background of its own colour. Black and white differ by 255 in every channel, so the difference is the coverage itself |
| Where the opacity rule lives | The collector multiplies opacities | The pixels show half ink for a faded text and for an anti-aliased edge alike |
| `numpy`, `coloraide` | Not added | `getcolors` with an alpha mask counts the colours in C; the WCAG formula is six lines. `docs/SPEC.md` names both libraries for later Checks |
| Document position of a Finding | Looked up from `selector` in the tool | No new field on `Finding` (roadmap: no Finding change beyond what the Check needs) |
| The pixel layers as a project rule | AD-004 in `.specs/STATE.md` | Later Checks (`invisible-content`, `font-fallback`) can read the same layers |
