# font-fallback Design

**Spec**: `.specs/features/font-fallback/spec.md`
**Status**: Approved by the maintainer on 2026-10-12

Every choice marked "spiked" was run on 2026-10-12 against `playwright 1.63.0` and real Chromium (headless shell 153.0.8010.12, launched with `--disable-lcd-text`) on Windows 11 and on Linux (the Playwright image for Docker), with the page script as drafted here, run where `capture()` would run it: after the repository's own `stabilize.js`, the settle screenshot, `collect_elements.js`, the pixels and the three fills. The page held every case of the spec. Every figure below is the same on both platforms unless a line says otherwise. The spike was outside the repository and is not kept; this file holds what it showed.

Conforms to AD-001 to AD-007. Follows AD-003 (a new fact is a field of the Capture) and the path of AD-005 (measured on request). Adds AD-008.

The design asked the maintainer for three criteria the spec did not have and one row of Out of Scope. The maintainer accepted the four; they are listed under "What the maintainer accepted" and are in the spec.

---

## Architecture Overview

```mermaid
graph TD
    C[MCP client] -->|call_tool| T[tools/detect_visual_bugs.py<br/>asks for fonts when font-fallback runs]
    T -->|capture url, viewport, "*", fonts| K[capture.py<br/>only importer of playwright]
    K --> J[js/collect_elements.js<br/>its element list stays on the page]
    K --> W[js/font_widths.js<br/>faces, copies of the texts, two widths]
    K -->|Capture: faces, Element.line_widths| T
    T -->|Capture| X[checks/font_fallback.py<br/>Failed family, Judged element, equality, one Finding per family]
    X -->|Finding list| T
```

A Capture taken with `fonts=True` holds two new facts. `Capture.faces` is every Face of `document.fonts`, with its family and its status. `Element.line_widths` is, for an element whose Own text asks first for a family that has a Face of `error`, the width of that text on one line in its `font-family` and in its Tail. The Check is a comparison of those two numbers and a grouping by family.

**How the two widths are measured.** On copies of the text, outside the flow. For each text node of the Own text the script makes two `span` elements with the text of the node: one with the computed `font-family` of the element, one with its Tail. Each copy carries the computed value of every style of the element that shapes text, has `white-space: nowrap` and is absolutely positioned inside one unseen host of no size, appended to the root element. Every copy is on the page before the first width is read, so the page is laid out once; then the host is removed, in the same task. The page never paints with the copies on it, and no style of the page is changed.

**Why copies and not the text itself.** The box of the text on the page is the wrong measure (spec, Assumptions, "Why on one line"), and changing the `font-family` of an element to read it lays the page out again for every element.

**What keeps the page's own rules off the copies.** `all: initial` and `!important` on every declaration of the host and of each copy, set through the style object. Spiked with rules a page could have (`html > div:last-child { display: none !important }`, and for a `span` with no id a `font-family`, a `font-size`, a `letter-spacing`, a `text-transform`, a `width` and a `padding`, all `!important`): every Finding is the same as without them.

**Which elements are measured.** Only those whose First family has a Face of `error`. A page whose fonts all loaded is not touched: the script reads the Faces and returns. The whole rule stays in the Check, which applies it again to what it is given.

### Approaches considered

All three deliver the same Check; they differ in how the Capture learns that a text is not in its First family.

| Approach | What it is | Verdict |
| --- | --- | --- |
| **A. Copies outside the flow, where a Face failed (chosen)** | Two copies of each text node, on one line, read in one layout | Chosen. Spiked: every case of the spec gives the value of its criterion on both platforms; 16 to 22ms for 30 elements, 133 to 165ms for 1,000 |
| B. The text itself, with the `font-family` of its element changed and put back | A `Range` over the Own text nodes, read twice | Rejected. Spiked: the widths agree with A for text on one line, but a justified paragraph gives 300 and 300 (FNT-21 fails), each element costs a layout of the page (1.1 to 1.2s for 1,000) and the styles of the page are changed while it is measured |
| C. Ask Chromium which font it used (`CSS.getPlatformFontsForNode`, over CDP) | The direct answer, no width | Rejected. The roadmap fixes the confirmation as the width metric and ADR-0002 turns down talking CDP directly. Spiked: it names the font file, not the family: text in `Half` and text in `Wide` both come back as `Ahem`, and a family that failed and is named after an installed font as that font |

### What the spike showed

| Case | Result |
| --- | --- |
| The cases of `font-fallback-bug.html` | `(#heading, Brand, 3)` with a width of 200 and `(#icon, Icon Set, 1)`, in that order (FNT-02). `#wrap`, with no Own text, is not measured. At 390 × 844 `(#narrow, Narrow Only, 1)` is added; at 1440 × 900 its Face is `unloaded` (FNT-13) |
| The cases of `font-fallback-bounds.html` | `(#half-bold, Half, 1)` 300, `(#mixed-lower, Mixed, 1)` 300, `(#lower, Missing Brand, 2)` 200, `(#scripted, Scripted, 1)`, `(#seen, Veiled Brand, 1)`, `(#own-parent, Parent Brand, 1)` 100, `(#fallen-child, Child Brand, 1)`, `(#long, Long Brand, 1)` 280, `(#twice-normal, Twice, 2)`, `([data-testid="shadow-text"], Shadow Brand, 2)`, in that order (FNT-15) |
| Not counted, each with its two widths | `#half-normal` 200 and 300 (FNT-20); `#wrapped` 1380 and 2070, with a box of 300 (FNT-21); `#mixed-both` 250 and 300 (FNT-22); `#veiled` and `#hidden` 200 and 200, left out by the Check for their `visibility` (FNT-23, FNT-26) |
| The cases of `font-fallback-clean.html` | No Finding. Four Faces are `error` (`Second Choice`, `Preloaded`, `Hidden Brand`, `Pseudo Brand`) and four `unloaded` (`Unused`, `After Generic`, `Never Shown`, `Blank`), before the script and after it. `#second`, `#undeclared` and `#stack` are not measured: their First family has no Face of `error` |
| `#code`, fifteen glyphs in `"Mono Brand", monospace` on a page 3000px taller than the viewport | 180.03125 in the family, in the Tail and as the width of the box the collector read (FNT-14). Windows and Linux: the same figure, in Courier New and in Liberation Mono |
| Styles that shape text | `text-transform: uppercase` on `xxxxxxxxxx` in `Mixed, Wide`: 200 and 300, not counted, because the characters painted are in the range of the Face that loaded. An italic Face that failed beside a normal one that loaded: 300 and 300 for the element of `font-style: italic`, 200 and 300 for the other. `letter-spacing: 2px` and `word-spacing: 6px` on `XXXX XXXXX`: 226 and 226 |
| A `pre` with a line break and four spaces between two pairs of glyphs | 100: on one line the white space is one space |
| A page of 1,000 elements of two glyphs in a font that failed, 1440 × 1260 | One Finding with 1000 elements; the script takes 133ms on Windows and 165ms on Linux (FNT-39) |
| The page's scroll size before the script and after it | The same |
| A Tail that starts with a family the page declares and no text has used yet | The copy asks for that font: its Face goes from `unloaded` to `loaded` within half a second. From a URL the page has not fetched, the width read is of the family after it in the Tail; from one it has, of the family itself. See Risks |
| A Face a script builds with quotes inside its name (`new FontFace('"Quoted Script"', ...)`) | Chromium takes the quotes as part of the name: `font-family: "Quoted Script"` does not ask for it. Nothing to handle |

### What the maintainer accepted

The Term "Line width" says "every style of the element that shapes text". The spike shows three places where a style changes the outcome and no criterion of the spec would notice a script that left it out. The design proposed one fixture more, `font-fallback-shaping.html`, and these criteria; they are in the spec as worded here.

1. **FNT-49** (P1: Stay silent): IF the `text-transform` of an element puts its characters in the `unicode-range` of a Face that loaded (`#upper-mixed` in `font-fallback-shaping.html`, `font-family: Mixed, Wide`, the text `xxxxxxxxxx` and `text-transform: uppercase`: 200px wide, 300px in its Tail; `Mixed` is the family of FNT-09) THEN the Check SHALL return no Finding on the element and SHALL not count it.
2. **FNT-50** (P1: Report): WHEN the Face that failed is the italic one of a family and an element asks for it (in `font-fallback-shaping.html`, `Slant` has a Face of `font-style: normal` from the file of Ahem and one of `font-style: italic` with a `src` that names no file; `#slant-normal` and after it `#slant-italic`, of `font-style: italic`, both have `font-family: Slant, Wide`) THEN the Check SHALL return one Finding for the family, on `#slant-italic`, with `evidence.measured.elements` equal to 1 and `evidence.computed` equal to `{"font-family": "Slant, Wide", "font-weight": "400", "font-style": "italic"}`.
3. **FNT-51** (P1: Read the Finding): WHEN the element a Finding sits on has a `letter-spacing` and a `word-spacing` (`#spaced` in `font-fallback-shaping.html`, an inline element of `font-family: "Spaced Brand", Ahem`, `letter-spacing: 2px` and `word-spacing: 6px` with the text `XXXX XXXXX`) THEN `evidence.measured.textWidthPx` SHALL be 226: nine glyphs of 20px, a space of 20px, 2px after each of the ten characters and 6px at the space.
4. **Out of Scope, one row more**: "A Tail that starts with a family the page declares and no text has used" — the copy that measures the Tail asks for that font, and the width read is of the family after it when the font is not there yet. It touches only an element that renders in a loaded Face of a Failed family, which the Check then counts only if that Face is as wide as the family after. Known limit of this Check.

Nothing else in the spec changes. FNT-43 holds: `config` gains a list of property names, no threshold.

---

## Code Reuse Analysis

### Existing Components to Leverage

| Component | Location | How to Use |
| --- | --- | --- |
| `capture()` | `src/squint_mcp/capture.py:248` | One more keyword, `fonts`; the new call goes after the fills at line 313 and before covered text at line 315 |
| The collector's element list | `src/squint_mcp/js/collect_elements.js:189` | `globalThis.__squintElements`, in the order of `Capture.elements`: the script names an element by its index (AD-005) |
| `_settle_layout` | `src/squint_mcp/capture.py:98` | Already runs before the collector: the boxes and the two widths are of one layout (FNT-14) |
| `Element.own_text_boxes`, `computed["visibility"]` | `src/squint_mcp/models.py:81`, `src/squint_mcp/config.py:56` | The two halves of "Judged element", already in every Capture |
| `CAPTURE_COMPUTED_PROPERTIES` | `src/squint_mcp/config.py:74` | Gains `font-style`, as it gained `z-index` in slice 8; `inspect_element` reads the other tuple |
| `COVERED_TEXT_CHECKS` and how the tool reads it | `src/squint_mcp/checks/__init__.py:28`, `src/squint_mcp/tools/detect_visual_bugs.py:91` | The same shape for `FONT_CHECKS` |
| The shape of a Check module | `src/squint_mcp/checks/offscreen_overflow.py` | `_EVIDENCE_PROPERTIES`, `_finding`, `check`; one Finding for several elements, on the first in document order |
| `CHECKS` | `src/squint_mcp/checks/__init__.py:19` | One more entry; the unknown-Check message already sorts the names |
| `helpers.py`, session `client`, `local_server` | `tests/` | `detect`, `findings_on`, `fixture_url`, `images` reused unchanged |
| `Ahem.ttf` | `tests/fixtures/` | The font that loads, and `Wide` through `size-adjust: 150%` |

### Integration Points

| System | Integration Method |
| --- | --- |
| `detect_visual_bugs` | Passes `fonts` when a Check that reads them is among the names; the docstring names the new Check. Sort and crops untouched |
| `inspect_element` | Unchanged. It never asks for fonts and builds its result from `INSPECT_COMPUTED_PROPERTIES`, so `font-style` does not reach it |
| The other four Checks | Unchanged. `font-style` is one more key of `Element.computed`, which each reads by name |

---

## Components

### Font script (`font_widths.js`)

- **Purpose**: everything the Capture does in the page for fonts. One call, synchronous.
- **Location**: `src/squint_mcp/js/font_widths.js`
- **Interfaces**: `({ shaping }) => ({ faces, widths })`.
  - `faces`: for each entry of `document.fonts`, in its order, `family` (without the quotes and the escapes Chromium serializes a name with) and `status`. Read before any copy is made.
  - `widths`: by index in the collector's list, `{ family, own, tail }` for each element that has a text node as a direct child that is not whitespace and whose First family, in lower case, is the family of a Face of `error`. `family` is the First family without quotes; `own` and `tail` are the sums over those text nodes of the width of their two copies.
- **The names of a `font-family`**: the computed value split at the commas outside strings, a backslash taking the character after it. The Tail is the names after the first joined by `, `, or `initial`.
- **A copy**: a `span` with the `nodeValue` of the text node; `all: initial`, `position: absolute`, `white-space: nowrap`, the computed value of each shaping property of the element, and the `font-family`, each `!important`.
- **The shaping properties**: every longhand of the computed style whose name starts with `font-`, but `font-family`, and the names passed in `shaping`.
- **The host**: a `div` with `all: initial`, `position: absolute`, at the origin, of no width and no height, `overflow: hidden` and `visibility: hidden`, each `!important`; appended to `document.documentElement` once every copy is in it and removed after the last width is read.
- **Dependencies**: the collector's list
- **Reuses**: nothing

### Capture (`capture.py`, `models.py`)

- **Purpose**: unchanged; fonts on request.
- **Interfaces**: `capture(session, url, viewport, selector, *, covered_text: bool = False, fonts: bool = False)`. A helper `_measure_fonts(page, elements) -> list[Face]` evaluates the script, gives each element named in `widths` its `line_widths` and returns the Faces.
- **Order inside `capture()`**: load, stabilize, idle wait, `_settle_layout`, collect, `scroll_width`, `pixels`, the three fills, then fonts when asked, then covered text when asked. After the pixels, so that nothing the script does can reach them; before covered text, which scrolls the page.
- **Reuses**: the pattern of `_measure_covered_text`

### Check (`checks/font_fallback.py`)

- **Purpose**: `Capture -> list[Finding]`.
- **Rules**, in order:
  1. `capture.faces` is `None`: no Finding.
  2. The Failed families: for each Face of `error`, its `family` in lower case, kept with the name of the first Face of that family in the list.
  3. For each element, in the order of the Capture: `line_widths` is not `None` and its `family`, in lower case, is a Failed family; `own_text_boxes` is not empty; `computed["visibility"]` is `visible`; `own == tail`. Such an element falls back in that family.
  4. One Finding per family with at least one such element, on the first of them. Elements are walked in document order, so the first found is the first of the document and the Findings come out in the order of their elements.
- **Finding**: `severity` `minor`; `family` the name kept in rule 2; `elements` the count; `textWidthPx` is `round(own, 2)` of the element it sits on; `computed` holds `font-family`, `font-weight` and `font-style`; the message says `element` for a count of 1 and `elements` otherwise.
- **Dependencies**: `models`. No `playwright`, no pixels, no value of `config`

### Tool (`tools/detect_visual_bugs.py`, `checks/__init__.py`)

- `checks/__init__.py` gains the entry of `CHECKS` and `FONT_CHECKS = frozenset({"font-fallback"})`, the Checks that read `Capture.faces` and `Element.line_widths`.
- The tool calls `capture(..., covered_text=..., fonts=not FONT_CHECKS.isdisjoint(names))`. Its docstring names `font-fallback` and says it reports a font the page declares that did not load, one Finding per family (FNT-37).

### Fixtures and tests

- `tests/test_font_fallback.py`, through the tool boundary only.
- `font-fallback-bug.html`, `-clean.html`, `-bounds.html`, `-monospace.html`, `-order.html`, `-many.html`, and `-shaping.html`. A family that fails is declared with a `src` that names a file that is not in `tests/fixtures/`; the Faces of `Scripted` and `Preloaded` are built by a script of the page.
- `tests/test_detect_visual_bugs.py`: the literal of FNT-34 in four assertions (lines 342, 353, 364 and 376).

### Documents

- `CHANGELOG.md` (FNT-44), `README.md` (FNT-45), and `docs/ROADMAP.md` at the closing step (FNT-46).

---

## Data Models

```python
class Face(BaseModel):
    """An entry of `document.fonts` when the Capture was taken."""

    family: str
    """Without quotes."""
    status: Literal["unloaded", "loading", "loaded", "error"]


class LineWidths(BaseModel):
    """How wide the own text of an element is set on one line (AD-008)."""

    family: str
    """The first name of its computed `font-family`, without quotes."""
    own: float
    """In its computed `font-family`."""
    tail: float
    """In that list without its first name; in the initial `font-family` when
    no name is left."""


class Element(BaseModel):
    ...
    line_widths: LineWidths | None = None
    """None when the Capture was not asked for fonts, and for an element with
    no own text or whose first family has no face that failed."""


@dataclass(frozen=True)
class Capture:
    ...
    faces: list[Face] | None = None
    """The faces of `document.fonts`, in its order; None when the Capture was
    not asked for fonts."""
```

Config (each with its source in a comment):

| Name | Value | Source |
| --- | --- | --- |
| `CAPTURE_COMPUTED_PROPERTIES` | adds `"font-style"` | Spec, Assumptions |
| `TEXT_SHAPING_PROPERTIES` | `("letter-spacing", "word-spacing", "text-transform", "text-rendering", "direction")` | Squint default: what changes the width of a text or the characters painted, besides the `font-` properties, which the script takes from the computed style |

---

## Error Handling Strategy

| Error Scenario | Handling | User Impact |
| --- | --- | --- |
| The font script fails | Same path as any Capture failure (AD-002) | The call fails; no partial result |
| `font-fallback` is given a Capture taken without fonts | `faces` is `None` | No Finding. Only the tool calls Checks, and it asks |
| A page with no Face, or none of `error` | The script returns the Faces and no width | No Finding; nothing was added to the page |
| A page with thousands of texts in a font that failed | Two copies per text node, one layout | 133 to 165ms for 1,000 elements; the total timeout stays the only clock |
| A font whose request never ends | Nothing new: `load` does not fire | `Timed out after 30s.`, as since slice 2 |

---

## Risks & Concerns

| Concern | Location (file:line) | Impact | Mitigation |
| --- | --- | --- | --- |
| A copy in the Tail asks for a font no text had used | `font_widths.js` | One request the page had not made; the Face goes from `unloaded` to `loaded` after the script. The width read is of the family after it when the font is not there yet | The Faces are read before any copy is made. It reaches only elements that render in a loaded Face of a Failed family: an element that fell back is already painted in its Tail. Accepted, marked `ponytail:`; a row of Out of Scope of the spec says it. No fixture has such a Tail. Waiting for the font would put copies on a page that paints, behind a bound of its own |
| The comment of `_settle_layout` says Linux does not show the fault of issue #18 | `src/squint_mcp/capture.py:98-105` | Stale: the Playwright image shows it. Nothing breaks | Outside this slice (spec, Out of Scope). FNT-14 fails without the fix wherever the fault shows |
| The family is compared in lower case twice, by `toLowerCase()` in the script and by `str.lower()` in the Check | `font_widths.js`, `checks/font_fallback.py` | A name outside ASCII that the two lower differently is measured and not reported, or not measured: no Finding | Accepted. Never a wrong Finding |
| A name that Chromium serializes with a hexadecimal escape (a control character in a family name) | `font_widths.js` | Its First family does not match its Face: no Finding | Accepted; `ponytail:` |
| What a copy does not carry: `::first-letter` and `::first-line` rules, `lang`, `zoom` | `font_widths.js` | `textWidthPx` is of the text without them. The two copies lack them alike, so the comparison holds | Accepted; `ponytail:` |
| A page script that watches the document sees a `div` come and go under the root element | `font_widths.js` | A `MutationObserver` callback runs once after the script; the host is gone by then | Accepted. Only on a page with a Face of `error` |
| A page whose Content Security Policy refuses inline styles | `font_widths.js` | Not verified. The copies are styled through the style object, not through a `style` element as the fills of AD-004 are | Outside this slice (spec, Out of Scope) |
| Every Capture pays for the three layers of AD-004, whatever reads them | `src/squint_mcp/capture.py:309` (`ponytail:`) | A call with `checks` equal to `["font-fallback"]` takes four full-page screenshots it does not read | Not touched: `detect_visual_bugs` crops from `pixels`, and the layers on request are a change of every Check |
| No existing fixture declares a font that fails | `tests/fixtures/` | None: the 69 fixtures hold 43 `@font-face` rules and every one loads `Ahem.ttf`, so no test of an earlier slice gains a Finding (FNT-38) | Checked by a search of their `src`; the gate confirms it |

---

## Tech Decisions (only non-obvious ones)

| Decision | Choice | Rationale |
| --- | --- | --- |
| Where the text is measured | On copies outside the flow | One line whatever the box of the element, one layout for the whole page, no style of the page changed |
| What a copy is given | Every `font-` longhand of the computed style and the names of `TEXT_SHAPING_PROPERTIES` | Spiked: `text-transform` and `font-style` decide which Face is asked for; `letter-spacing` and `word-spacing` are part of the width. Taking the `font-` names from the computed style keeps the list right when Chromium gains one |
| Where the copies go | One host under the root element, of no size | `body` can be a flex or a grid container, and an absolutely positioned child of the root element lays nothing else out. No size and `overflow: hidden` keep the scroll size of the page |
| Which elements are measured | Those whose First family has a Face of `error` | A page whose fonts loaded is not touched, and a Tail is only laid out where it can already be on the page |
| Where the rule lives | In the Check, whole | The script's filter is what to measure, not what to report: the Check compares the family again, and "Judged element" and the equality are only there |
| The Tail of one name | `initial` | Spiked in Specify: the same width as text whose only family failed |
| When, inside a Capture | After the three fills, before covered text | Nothing the script does can reach a pixel of the Capture; covered text scrolls the page |
| `textWidthPx` | `round(own, 2)`, a float | FNT-14 compares it with `box.w` rounded the same way; a whole number of pixels compares equal to the integer of FNT-27 |
| No module beside the Check | The script returns what the models hold | There is no arithmetic to keep out of `capture.py`, unlike covered text |

### Project-level decisions

AD-008 (the fonts of a page are read on request; widths come from copies of the text outside the flow, only where a face failed) is in `.specs/STATE.md`.
