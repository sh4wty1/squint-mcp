# font-fallback Context

**Gathered:** 2026-10-12
**Spec:** `.specs/features/font-fallback/spec.md`
**Status:** Ready for design, once the maintainer accepts the spec

---

## Feature Boundary

Slice 9 of `docs/ROADMAP.md`: the `font-fallback` Check (a family not loaded in `document.fonts`, confirmed by the width metric), what the Capture has to expose about the fonts of a page, its fixtures and the CHANGELOG entry. No `layout-shift` and no judgement of typographic quality.

Standing rule from the maintainer: the roadmap and `docs/SPEC.md` are followed literally. Anything they assign to a later slice or leave out is out of scope without discussion.

---

## Implementation Decisions

The maintainer took the four defaults proposed, in one turn (2026-10-12).

### How many Findings a font that failed gives

- One Finding per family that did not load, per viewport. It sits on the first element in document order whose text fell back.
- `evidence.measured` counts the elements whose text fell back in that family. A brand font broken across a site is one Finding, not hundreds.

### Severity

- Always `minor`. The text can still be read; nothing measured grades the fault, since the width in the font that was asked for is not known.

### Which family of the list is judged

- Only the first family of `font-family`: it is the font the CSS asks for, and the families after it are the fallbacks the CSS itself names.
- A family that failed and stands second or later in the list gets no Finding. Known limit of this Check.

### Linux

- The spike is verified on Linux before the spec is closed, in the official Playwright image for Docker. Done; the results are below.

### Agent's Discretion

None. Every remaining choice is logged in the spec's Assumptions table with its default and rationale, and waits for the maintainer's review.

### Declined / Undiscussed Gray Areas → Assumptions

Logged in the spec's Assumptions & Open Questions: that only families the page declares are judged, that a face is failed by its `error` status alone, how the width confirms (on one line, against the rest of the list), what stands for the rest of a list of one family, which elements are judged (own text that paints a box, `visibility: visible`), the evidence keys and their rounding, the wording of the message and the suggestion, the name a family is reported under, and whether the Capture measures on request.

---

## Specific References

A spike against real Chromium on 2026-10-12 (headless shell 153.0.8010.12, `playwright 1.63.0`, launched with `--disable-lcd-text`), outside the repository, on Windows 11 and on Linux (`mcr.microsoft.com/playwright/python:v1.63.0-noble`). Every number below is the same on both unless a line says otherwise.

### What `document.fonts` says

After `document.fonts.ready`:

| Case | `status` of the face |
| --- | --- |
| `@font-face` whose `src` is a file that does not exist (`file://`), a URL that answers 404, bytes that are not a font (`data:`), or `local()` of a font that is not installed | `error` |
| A face a script builds, adds to `document.fonts` and loads, with a `src` that does not exist | `error` |
| A face declared and used by no text | `unloaded` |
| A face whose `unicode-range` holds none of the characters of the text that names it | `unloaded` |
| A family named after a generic one (`sans-serif, "After Generic"`) | `unloaded`: Chromium never asks for it |
| A family named only by an element of `display: none`, or by an element whose text is whitespace | `unloaded` |
| A family named only by text of `visibility: hidden`, of `opacity: 0`, or by the `content` of a pseudo-element | `error`: the face is asked for |
| `src: url(missing), url(Ahem.ttf)` | `loaded`: the second source is used |

- `FontFace.family` is the name without quotes. A family is matched whatever its case: `half` and `HALF` render in the face declared as `Half`.
- `document.fonts.check()` cannot be the signal: it answers `true` for a family that nothing declares and for a face whose `unicode-range` does not hold the text.

### What renders when a face fails

Ahem at 20px: ten glyphs are 200px wide. `Wide` is Ahem with `size-adjust: 150%`: the same ten glyphs are 300px. Both figures are exact on Windows and on Linux.

| Element | Width | Width with the first family taken out | Reads as |
| --- | --- | --- | --- |
| `"Missing Brand", Ahem` (face failed) | 200 | 200 | fell back |
| `"Missing Brand", Wide` | 300 | 300 | fell back |
| `Half, Wide` at weight 400; `Half` has a face of 400 that loaded and one of 700 that failed | 200 | 300 | rendered in `Half` |
| The same at weight 700 | 300 | 300 | fell back: Chromium does not go to another face of the family, it goes to the next family |
| `Flip, Wide`, the mirror (400 failed, 700 loaded), at weight 400 and at 700 | 300 and 200 | 300 | fell back, and rendered in `Flip` |
| `Mixed, Wide`; `Mixed` has a face for A to Z that loaded and one for a to z that failed. `XXXXXXXXXX`, `xxxxxxxxxx`, `XXXXXxxxxx` | 200, 300, 250 | 300 | in `Mixed`, fell back, half and half |
| `Alone` (failed), the only family of the list | 139.61 | n/a | the same width as with `font-family: initial` |
| `Arial, Wide` with a page that declares its own `Arial` and fails to load it | 133.41 | 300 | rendered in the Arial of the system (Windows) or in the font the system gives for that name (Liberation Sans, Linux) |
| A justified paragraph 300px wide in `Half, Wide` at weight 400 | box of the text 300 | 300 | the same box, though `Half` renders it; set on one line the text is 1380px in `Half` and 2070px in `Wide` |

- The premises of the fixtures the spec names were run too, on both platforms: a failed family that stands second, after a name nothing declares, has a face of `error` (FNT-18); so has a face a script loads and no element names (FNT-19), and both faces of a family when one element asks for each (FNT-48). Own text of five glyphs beside a child of five is 100px on one line (FNT-11); `XXXX XXXX XXXX` in a block 100px wide is 280px on one line (FNT-30); fifteen glyphs in `Brand, monospace` inside an inline element are 180.03px, in the family, in its tail and as the width of the element's box (FNT-14).
- Measured in place (the `font-family` of the element changed and put back) and on a copy of the text outside the flow, the two widths agree in every case.
- Twice in a row, every figure is the same.
- An element in an open shadow tree uses a family the document declares, and falls back the same way.

### `font-display`

A font that answers after 700ms, over HTTP:

| `font-display` | `status` | What renders once the page has loaded |
| --- | --- | --- |
| `swap`, `fallback`, `block` | `loaded` | the font |
| `optional` | `loaded` | the next family, for as long as the page lives |

A font whose request never ends keeps `load` from firing: the call fails with the total timeout, as it has since slice 2.

### Cost

Two widths for each of 1,000 elements: 45 to 66ms when every copy is made first and every width read after (5,000 elements: 258 to 293ms); 1.1 to 1.2s when each element has its `font-family` changed and read in turn. A page with no failed face has nothing to measure.

### The generic `monospace` font (AD-006, issue #18)

`"Brand", monospace` with `Brand` failed, 15 glyphs, on a page 3000px taller than the viewport:

| | Windows | Linux |
| --- | --- | --- |
| At first, and after a screenshot of the viewport | 164.95 (Consolas) | 150 (WenQuanYi Zen Hei Mono) |
| After the first screenshot that reaches beyond the viewport (16 × 16, `full_page`) | 180.03 (Courier New) | 180.03 (Liberation Mono) |

The width with the family and the width without it move together, so they agree as long as both are read in one layout. On a page that fits the viewport nothing moves, on either platform.

**Found on the way.** The fault of issue #18 shows on Linux too, in the Playwright image: the first screenshot beyond the viewport changes the font of the generic `monospace` family there as well. The issue and the comment of `_settle_layout` in `src/squint_mcp/capture.py` say Linux does not show it and that no test can hold the fix. Whether the CI's Linux has the same fonts was not checked. Outside this slice; the maintainer decides whether it gets an issue.

---

## Deferred Ideas

- A family that failed and is not the first of the list.
- A family the page names and does not declare, which is not installed on the machine.
- A family that loaded and does not render: `font-display: optional` with a slow font; a font that lacks some glyphs of the text.
- Text of pseudo-elements, which is how many icon fonts are used.
- Naming in the Finding the URL that failed.
- A test that holds the fix of issue #18, now that Linux shows the fault in the Playwright image.
