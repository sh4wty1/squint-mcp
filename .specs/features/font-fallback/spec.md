# font-fallback Specification

Slice 9 of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md). Source of truth: the roadmap section "9. font-fallback", then [`docs/SPEC.md`](../../../docs/SPEC.md), [`CONTEXT.md`](../../../CONTEXT.md), ADR-0002, the decisions AD-001 to AD-007 in [`.specs/STATE.md`](../../STATE.md) and the decisions of [`context.md`](context.md). Decisions made there are final and are not restated as open here. The specs of slices 3, 4, 6, 7 and 8 stay in force except where this one says it supersedes a criterion.

Scope size: Large. The Check needs facts the Capture does not hold (the faces of `document.fonts` and two widths of a text), so Design runs; Tasks run too.

## Problem Statement

A web font that answers 404, a wrong path in an `@font-face` rule, an icon font that never arrives: the DOM is valid, `font-family` computes to what the stylesheet says, and the text is painted in another font. A tool that reads only computed styles reports the font that was asked for. Squint can read which faces of the page failed and confirm on the rendered text that it is as wide as it is without the family: the text is in a fallback.

## Goals

- [ ] `font-fallback` reports every family of its "bug" fixture that did not load, once, and nothing on its "clean" fixture, which holds loaded web fonts, a stack of system fonts, families that are declared and never used, and text that is not on the page.
- [ ] A Finding names the family and says how many elements render their text in a fallback.
- [ ] Every outcome a test asserts is the same on Windows and on Linux.
- [ ] Slice 9 is marked done in `docs/ROADMAP.md` once verification passes.

## Terms

Used by the criteria below; each is defined once here.

- **Own text**: the text nodes that are direct children of an element (same reach as the other Checks).
- **Face**: an entry of `document.fonts` when the Capture is taken: the faces of the `@font-face` rules of the page and those a script added.
- **Failed family**: a family name that at least one Face with a `status` of `error` has. Family names are compared without their quotes and whatever their case.
- **First family** of an element: the first name of its computed `font-family`.
- **Tail** of an element: its computed `font-family` without its first name; when no name is left, the initial value of `font-family`.
- **Line width** of an element in a list of families: the width its Own text takes set on one line, with every style of the element that shapes text and that list as `font-family`. The widths of several text nodes are added.
- **Judged element**: an element whose Own text is not only whitespace and paints at least one box in the Capture, and whose computed `visibility` is `visible`.
- **Falls back**: a Judged element falls back when its First family is a Failed family and its Line width in its computed `font-family` is equal to its Line width in its Tail.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| `layout-shift`; any judgement of typographic quality (a bold or an italic that the browser synthesizes, a fallback that is a poor match) | Roadmap, "Não entra" |
| A family the page names and does not declare, which is not installed on the machine (`"Helvetica Neue"` on Windows, `-apple-system` anywhere but macOS) | The roadmap fixes the signal: a family not loaded in `document.fonts`, which holds only what the page declares. Stacks of system fonts name such families on purpose, and the result would change with the machine |
| A Failed family that is not the First family of an element | Decided with the maintainer (2026-10-12). The families after the first are the fallbacks the CSS itself names. `"Segoe UI", "Brand"` with `Brand` failed gets no Finding. Known limit of this Check |
| A family that loaded and does not render the text: `font-display: optional` with a font that answers late | Its Face has the status `loaded` and the text stays in the Tail for as long as the page lives (measured, [`context.md`](context.md)). The roadmap asks for a family not loaded, and `optional` is the page's own instruction to fall back. Known limit of this Check |
| A text of which only some glyphs fall back: a loaded font that lacks them, or a family with one Face per `unicode-range` of which one failed | The text is not as wide as in its Tail, so the width does not confirm (FNT-22). Known limit of this Check |
| Text of pseudo-elements | Own text only, as in the other Checks. An icon font used through `::before` and `content` gets no Finding when it fails (FNT-24). Known limit of this Check |
| A Failed family that has the name of a font installed on the machine | Chromium renders the text in the installed font of that name (measured for a page that declares its own `Arial`). The Finding then depends on whether the Tail gives the same font: it differs from one machine to the next. No fixture uses such a name. Known limit of this Check |
| A Tail whose font is as wide as the family for a text, when the element renders in a loaded Face of a Failed family | The two widths are equal and the element counts as fallen back. It takes a family with one Face failed and another loaded, and a fallback of the same metrics. Known limit of this Check |
| A Tail that starts with a family the page declares and no text has used | The copy of the text that measures the Tail asks for that font, a request the page had not made, and the width read is of the family after it when the font is not there yet ([`design.md`](design.md), Risks). It touches only an element that renders in a loaded Face of a Failed family, which then counts as fallen back only if that Face is as wide as the family after. Known limit of this Check |
| Text in a vertical writing mode | The width of a line that runs down the page is its thickness, not its length. An element that renders in a loaded Face of a Failed family can count as fallen back there. Known limit of this Check |
| A font whose request never ends | `load` does not fire and the call fails with the total timeout, as it has since slice 2 (measured, [`context.md`](context.md)) |
| A Face that is still `loading` when the Capture is taken, or that fails after it | Only a `status` of `error` makes a Failed family. A Capture waits for `document.fonts.ready` before anything else (slice 2) |
| Text that is not seen for another reason than `visibility`: `opacity: 0`, clipped away, off the page | It is judged and counted as any other. Only text whose `visibility` is not `visible`, text that paints no box and text that is only whitespace are left out |
| Which source of a Face failed (the URL of its `src`) | A Face does not say it, and the stylesheet that does may be of another origin. The Finding names the family |
| One Finding per element; a severity that changes with the fault | Decided with the maintainer (2026-10-12) |
| Iframes; closed shadow trees | `docs/SPEC.md` |
| Any other Check, Profile, Audit, score, `compare_viewports` | Not in this slice |
| A parameter for any of the rules | `docs/SPEC.md`: behaviour changes only through `url`, `viewports`, `checks` |
| Changes to the behaviour of `inspect_element` or `ping`, or to the Findings of the other four Checks | Earlier slices are closed (FNT-38) |
| The residuals of the fifth validation pass of slice 8, a page whose Content Security Policy refuses inline styles, a right-to-left page that scrolls sideways | Left in the Handoff of slice 8 without an issue; the maintainer keeps them out of this slice. Under such a policy this Check may be as blind as the others |
| A test that holds the fix of issue #18 | The spike of this slice shows the fault on Linux too, in the Playwright image ([`context.md`](context.md), "Found on the way"). FNT-14 fails without the fix wherever the fault shows; a test of its own for AD-006 is the maintainer's call |
| Tests outside the MCP tool boundary | `docs/SPEC.md` Testing Decisions: one seam |
| Pushing the branch and opening the pull request | Remote actions; they need the maintainer's go-ahead |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

The maintainer accepted the spec on 2026-10-12 and took every default of the table below: all of them are confirmed. The same day the maintainer accepted what the design asked for: the criteria FNT-49 to FNT-51, on a fixture of their own, and one row of Out of Scope ("A Tail that starts with a family the page declares and no text has used"). With the tasks, still on 2026-10-12, the maintainer accepted FNT-52 to FNT-54: three rules that the Terms state and no criterion held (text that paints no box, a Face that is `unloaded`, the widths of several text nodes added), each on one case more of `font-fallback-bounds.html`, and the two rows FNT-15 gains for them.

On 2026-10-13 the Verifier's first pass ([`validation.md`](validation.md)) found ten mutants alive on rules that the Terms, the Assumptions or the design state and that no criterion held. The criteria FNT-55 to FNT-62 pin those rules, on two fixtures of their own and on two cases more of `font-fallback-shaping.html`. With them came one word on whitespace, which the design had and the Terms did not: in the Term "Judged element", in the row "Which elements are judged" below and in the row of Out of Scope on text that is not seen; and the clause of FNT-49 that names `#lower-mixed`. No behaviour changes. They were the orchestrator's defaults, written from the report. The maintainer read them on 2026-10-13, after the second pass, and accepted each as written; with them the last sentence of the row "Fixtures" below was reworded to say what a Tail may name ([`tasks.md`](tasks.md), "The maintainer's decisions after the second pass"). On 2026-10-15 the maintainer accepted FNT-63, for issue #20 (I-1 of the second pass): a Failed family whose name holds a backslash, on one case more of `font-fallback-names.html`.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| How many Findings a font that failed gives | One per Failed family and per Capture, on the first element in document order that falls back in it; `evidence.measured.elements` counts those that do | Decided with the maintainer (2026-10-12). A brand font broken across a page is one cause and one fix. `offscreen-overflow` is already one Finding per viewport, and each Finding still sits on one element (`docs/SPEC.md`) | y |
| Severity | Always `minor` | Decided with the maintainer (2026-10-12). The text can be read; `major` is kept for content that cannot. Nothing measured grades the fault: the width in the font that was asked for is not known | y |
| Which family of the list is judged | The First family only | Decided with the maintainer (2026-10-12). It is the font the CSS asks for. Measured: a family named after a generic one is never even asked for by Chromium | y |
| The platforms the spike ran on | Windows 11 and Linux (the Playwright image for Docker), the same Chromium 153 | Decided with the maintainer (2026-10-12), and done: every figure this spec relies on is the same on both ([`context.md`](context.md)) | y |
| Which families can be reported | Only those that have a Face: declared by an `@font-face` rule or added by a script | The roadmap names `document.fonts`. A family that is only named cannot fail to load, it can only be missing from a machine | y |
| What "not loaded" means | A Face with a `status` of `error`. `unloaded` and `loading` do not make a Failed family | Measured: after `document.fonts.ready` a Face that was needed and could not be had is `error`, whatever the cause (a missing file, a 404, bytes that are not a font, a `local()` font that is not installed). `unloaded` is a Face no text needed: a weight nobody uses, a `unicode-range` without the text, a family behind a generic one. `document.fonts.check()` answers `true` for a family that nothing declares and is not used | y |
| Which Face of a family has to fail | Any. The Check does not match Faces to elements by weight, style or `unicode-range`; the width does it | Measured: when the Face that matches an element fails, Chromium goes to the next family, not to another Face of the same one. An element that renders in a loaded Face of the family is wider or narrower than in its Tail (FNT-20) | y |
| How the width confirms | The element falls back when its Line width in its computed `font-family` is equal to its Line width in its Tail | "Confirmada pela métrica de largura" (roadmap). The width in the font that failed cannot be measured; that the family changes nothing can. It is what `.docs/START.md` calls "differs from the expected" read from the other side | y |
| Why on one line | Both widths are of the Own text set on one line, not of its boxes on the page | Measured: a justified paragraph 300px wide has a box of 300px in the family and in its Tail, though the family renders it. On one line it is 1380px against 2070px | y |
| Equality | Exact: no tolerance and no threshold. `config` gains no value for this Check | Both widths are of the same text, laid out twice in one page by one browser: measured equal to the last fraction on both platforms, twice in a row. A tolerance would be a number tuned on one machine | y |
| The Tail of a list of one family | The initial value of `font-family` | Measured: text whose only family failed is as wide as with `font-family: initial`. Icon fonts are named alone | y |
| Which elements are judged | Those whose Own text is not only whitespace and paints at least one box, and whose `visibility` is `visible` | An element of `display: none` paints no box, and Chromium does not even ask for its font. Text of `visibility: hidden` is hidden on purpose, as `overlap` takes it (slice 8). Other ways of not being seen are not read: Out of Scope | y |
| The name a family is reported under | As the first of its Faces in `document.fonts` gives it, without quotes; elements that write it in another case are counted with it | A Face gives the name without quotes (measured). Chromium matches `half` and `HALF` to a family declared as `Half` (measured) | y |
| `evidence.measured` | Exactly `family` (a string), `elements` (an integer) and `textWidthPx` (the Line width of the element the Finding sits on, the same in its `font-family` and in its Tail, rounded to two decimal places) | What an agent needs to act: which font, and how far the fault reaches. `textWidthPx` is the measurement that confirms the claim (`docs/SPEC.md`, story 47). On a text that wraps it is wider than `box.w`: it is of one line | y |
| `evidence.computed` | Exactly `font-family`, `font-weight` and `font-style` of the element. `font-style` is a new property collected for a Capture; `inspect_element` does not return it | The three say which Face the element asked for. As `z-index` in slice 8 | y |
| Message, suggestion, source, category | `The font "{family}" did not load: the text of {elements} element(s) is rendered in a fallback font`, with `element` for one and `elements` otherwise; `Fix the source the page loads "{family}" from, or take the family out of font-family`; `Squint heuristic`; `visual-bug` | As `text-clipped` and `overlap`: no outside norm defines this | y |
| Unknown-Check message (supersedes the literal in force since slice 8) | `Valid checks: font-fallback, low-contrast-real, offscreen-overflow, overlap, text-clipped.` | Same rule, alphabetical; the list grew. It changes four assertions: `tests/test_detect_visual_bugs.py` lines 342, 353, 364 and 376 | y |
| Order of Findings | Unchanged: severity, then viewport, then document order of the element, then Check name | Settled in slice 4 (LCR-37 to LCR-39, LCR-53) | y |
| How the Capture learns the Faces and the two widths | On request, as covered text is (AD-005): only when `font-fallback` is among the Checks of a call. They are held in the Capture in fields the Check reads (AD-003). The shape is [`design.md`](design.md)'s | The maintainer asked for the path of AD-005 and AD-003. Measured: two widths for 1,000 elements take 45 to 66ms when read together, and a page with no Failed family has nothing to measure | y |
| The layout the widths are of | Both Line widths of an element are read in the layout the boxes of the Capture are of: after the Capture has settled it (AD-006) | Measured on both platforms: the first screenshot beyond the viewport changes the font of the generic `monospace` family, and fifteen glyphs go from 164.95px (Windows) or 150px (Linux) to 180.03px. The two widths move together; one read before and one after would differ and the Finding be lost | y |
| Outcomes on two platforms | A criterion asserts whether a Finding is there, where it sits, its severity, `family` and `elements`. It asserts `textWidthPx` as a figure only for text in Ahem; for text in a system font it asserts that it equals another value of the same response (FNT-14). No criterion compares a width with a figure from another machine | Chromium rasterizes and picks system fonts differently on Windows and on Linux (slice 8: two tests failed on the CI's first run). An equality of two widths of one Capture does not depend on either | y |
| Fixtures | Ahem at `font-size: 20px` and `line-height: 30px`: a glyph is 20px wide. `Wide` is Ahem with `size-adjust: 150%`: a glyph is 30px wide (measured on both platforms). A family that fails is declared with a `src` that names a file that is not there. A text is a block 200px wide, 40px from the left of the page, unless a criterion says otherwise. Each rule has its own family, so one Finding has one cause. No fixture declares a family that a machine can have installed; a Tail may name fonts of a machine (FNT-16, FNT-62) | Exact widths need a font whose glyphs are whole pixels, and a fallback that can be told from it | y |
| Criteria not observable through the tool boundary (FNT-40 to FNT-46) | Verified by the Verifier from file evidence, not by pytest | The source docs forbid a second test seam. As in slices 3, 4 and 8 | y |
| When the discrimination sensor is satisfied | As in slice 8: the mutants that a validation report or a task names die, with those of the code the last fix round changed. One found alive later is a residual or an issue and does not fail the feature | The maintainer decided it for slice 8 (2026-10-12); carried over here | y |

**Open questions:** none - all resolved or logged above.

**Implicit-requirement dimensions:**

- Input validation & bounds: FNT-34 (the list of valid Checks); FNT-39 (a page with a thousand elements in a font that failed); no new parameter.
- Failure / partial-failure states: N/A because the Check adds no failure of its own; a Capture that fails still fails the call (AD-002), and a font that never answers ends in the total timeout as before (Out of Scope).
- Idempotency / retry / duplicate handling: FNT-04.
- Auth boundaries & rate limits: N/A because the server is a local stdio process with no caller identity.
- Concurrency / ordering: FNT-02, FNT-15, FNT-36.
- Data lifecycle / expiry: N/A because a call keeps nothing: whatever the Capture changes on a page to measure it dies with the browser context of that call (AD-001), and FNT-38 holds that the other Checks read the same page as before.
- Observability: N/A because the slice adds no log line or metric; logs stay on stderr as set in slice 1.
- External-dependency failure: the font file is a dependency of the page, and its failure is what the Check reports (FNT-01). The Check itself calls nothing outside the Capture.
- State-transition integrity: N/A because a Check is a pure function of a Capture.

---

## User Stories

### P1: Report a font that did not load ⭐ MVP

**User Story**: As a front-end developer, I want Squint to report a web font that the page declares and that did not load, so that I catch a wrong path or a 404 before users see the page in another font.

**Why P1**: It is the Check.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN at least one Judged element of a Capture falls back in a Failed family THEN the `font-fallback` Check SHALL return exactly one Finding for that family, on the first of those elements in document order. <!-- FNT-01 -->
2. WHEN `detect_visual_bugs` is called on `font-fallback-bug.html` with `checks` equal to `["font-fallback"]` THEN the `(selector, severity, evidence.measured.family, evidence.measured.elements)` of `findings` SHALL be, in this order, `(#heading, minor, Brand, 3)` and `(#icon, minor, Icon Set, 1)`; the page declares `Icon Set` and then `Brand`, each with a `src` that names no file, and holds in the document `#wrap` (`font-family: Brand, Ahem`, no Own text) with `#heading`, `#lead` and `#note` inside it, then `#icon` (`font-family: "Icon Set"`) and `#fine` (`font-family: Ahem`). <!-- FNT-02 -->
3. WHEN `detect_visual_bugs` is called on `font-fallback-bug.html` without `checks` THEN the first content block SHALL be a text block equal to `Found 2 findings in 1 viewport: 2 minor.` <!-- FNT-03 -->
4. WHEN `detect_visual_bugs` is called twice with the same arguments on `font-fallback-bug.html` THEN both calls SHALL return equal structured content. <!-- FNT-04 -->
5. WHEN the Face that failed was added to `document.fonts` by a script and not by an `@font-face` rule (`#scripted` in `font-fallback-bounds.html`, `font-family: Scripted, Ahem`; a script of the page builds the Face of `Scripted` with a `src` that names no file, adds it and loads it) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Scripted`. <!-- FNT-05 -->
6. WHEN elements write the name of a Failed family in another case than its Face has it (in `font-fallback-bounds.html`, `#lower`, `font-family: missing brand, Ahem`, and after it `#quoted`, `font-family: "Missing Brand", Ahem`; the page declares `"Missing Brand"`) THEN the Check SHALL return one Finding for the family, on `#lower`, with `evidence.measured.elements` equal to 2. <!-- FNT-06 -->
7. WHEN the First family of an element is the only name of its `font-family` and is a Failed family (`#icon` in `font-fallback-bug.html`, whose text is `home`) THEN the Check SHALL return one Finding for the element: its Tail is the initial value of `font-family`. <!-- FNT-07 -->
8. WHEN a family has a Face that loaded and a Face that failed, and an element asks for the one that failed (`#half-bold` in `font-fallback-bounds.html`, `font-family: Half, Wide` and `font-weight: 700`; `Half` has a Face of weight 400 from the file of Ahem and one of weight 700 with a `src` that names no file) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Half` and `evidence.measured.elements` equal to 1. <!-- FNT-08 -->
9. WHEN a family has one Face per `unicode-range`, one of them failed, and every character of the Own text of an element is in the range of that one (`#mixed-lower` in `font-fallback-bounds.html`, `font-family: Mixed, Wide` and the text `xxxxxxxxxx`; `Mixed` has a Face for `U+0041-005A` from the file of Ahem and one for `U+0061-007A` with a `src` that names no file) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Mixed` and `evidence.measured.elements` equal to 1. <!-- FNT-09 -->
10. WHEN an element in an open shadow tree falls back in a family the document declares (`[data-testid="shadow-text"]` in the shadow tree of `#host` in `font-fallback-bounds.html`, `font-family: "Shadow Brand", Ahem`, and after the host `#after-host`, with the same `font-family`) THEN the Check SHALL return one Finding for the family, with `selector` equal to `[data-testid="shadow-text"]` and `evidence.measured.elements` equal to 2. <!-- FNT-10 -->
11. WHEN an element falls back and a child of it has text in a font that loaded (in `font-fallback-bounds.html`, `#own-parent`, `font-family: "Parent Brand", Ahem`, with the Own text `XXXXX` and a child `#own-child` of `font-family: Ahem` and the text `XXXXX`; after it `#bare-parent`, with the same `font-family`, no Own text and a child `#bare-child` of `font-family: Ahem`) THEN the Check SHALL return one Finding for the family, on `#own-parent`, with `evidence.measured.elements` equal to 1 and `evidence.measured.textWidthPx` equal to 100: an element is judged on its Own text. <!-- FNT-11 -->
12. WHEN an element whose First family loaded has a child that falls back (in `font-fallback-bounds.html`, `#clean-parent`, `font-family: Ahem`, with Own text and a child `#fallen-child` of `font-family: "Child Brand", Ahem`) THEN the Check SHALL return one Finding for the family, on `#fallen-child`, with `evidence.measured.elements` equal to 1. <!-- FNT-12 -->
13. WHEN `detect_visual_bugs` is called on `font-fallback-bug.html` with `viewports` of 1440 × 900 and 390 × 844 THEN `#narrow` (`font-family: "Narrow Only", Ahem`, of `display: none` while the viewport is more than 600px wide; `Narrow Only` has a `src` that names no file) SHALL get one Finding whose `viewport` is 390 × 844, with `evidence.measured.family` equal to `Narrow Only`, and none whose `viewport` is 1440 × 900. <!-- FNT-13 -->
14. WHEN the Tail of an element that falls back is the generic `monospace` family and the page is taller than the viewport (`font-fallback-monospace.html`, a page 3900px high at 1440 × 900: `#code`, an inline element that holds fifteen glyphs on one line and nothing else, of `font-family: Brand, monospace`, with `Brand` declared with a `src` that names no file) THEN `detect_visual_bugs` called with `checks` equal to `["font-fallback"]` SHALL return exactly one Finding, on `#code`, with `evidence.measured.family` equal to `Brand`, `evidence.measured.elements` equal to 1 and `evidence.measured.textWidthPx` equal to the `w` of its `box` rounded to two decimal places: both widths are read in the layout the boxes of the Capture are of (AD-006). <!-- FNT-14 -->
15. WHEN `detect_visual_bugs` is called on `font-fallback-bounds.html` with `checks` equal to `["font-fallback"]` THEN the `(selector, evidence.measured.family, evidence.measured.elements)` of `findings` SHALL be, in this order, `(#half-bold, Half, 1)`, `(#mixed-lower, Mixed, 1)`, `(#lower, Missing Brand, 2)`, `(#scripted, Scripted, 1)`, `(#seen, Veiled Brand, 1)`, `(#shown, Unshown Brand, 1)`, `(#own-parent, Parent Brand, 1)`, `(#fallen-child, Child Brand, 1)`, `(#long, Long Brand, 1)`, `(#split, Split Brand, 1)`, `(#twice-normal, Twice, 2)` and `([data-testid="shadow-text"], Shadow Brand, 2)`, all with `severity` equal to `minor`. <!-- FNT-15 -->
16. WHEN the Face that failed is the italic one of a family and an element asks for it (in `font-fallback-shaping.html`, `Slant` has a Face of `font-style: normal` from the file of Ahem and one of `font-style: italic` with a `src` that names no file; `#slant-normal` and after it `#slant-italic`, of `font-style: italic`, both have `font-family: Slant, Wide`) THEN the Check SHALL return one Finding for the family, on `#slant-italic`, with `evidence.measured.elements` equal to 1 and `evidence.computed` equal to `{"font-family": "Slant, Wide", "font-weight": "400", "font-style": "italic"}`. <!-- FNT-50 -->
17. WHEN the name of a Failed family holds a comma (`#comma` in `font-fallback-names.html`, `font-family: "Acme, Inc", Ahem`; the page declares `"Acme, Inc"` with a `src` that names no file) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Acme, Inc`: a `font-family` is split at the commas outside its quotes. <!-- FNT-59 -->
18. WHEN the name of a Failed family holds a quotation mark, which a computed `font-family` writes with a backslash before it (`#inch` in `font-fallback-names.html`, of `font-family: 'Vinyl 12"', Ahem`; the page declares the family `Vinyl 12"` with a `src` that names no file) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Vinyl 12"`, and `evidence.computed` SHALL hold the `font-family` of the element as computed, `"Vinyl 12\"", Ahem`. <!-- FNT-60 -->
19. WHEN the name of a Failed family holds a backslash, which a computed `font-family` writes with a second backslash before it (`#slash` in `font-fallback-names.html`, of `font-family: "Back\\slash", Ahem`; the page declares the family `Back\slash` with a `src` that names no file) THEN the Check SHALL return one Finding for the element with `evidence.measured.family` equal to `Back\slash`: the name of a Face is taken as `document.fonts` gives it, with no quote and no escape taken off. <!-- FNT-63 -->

**Independent Test**: Call `detect_visual_bugs` on `font-fallback-bug.html` and read the two Findings: `Brand` on three elements, `Icon Set` on one.

---

### P1: Stay silent when the text is in the font it asks for

**User Story**: As a front-end developer, I want Squint not to report text that is in the font the CSS asks for, nor a font the page never needed, so that I can trust a Finding when I see one.

**Why P1**: Every page names fonts that are not on the machine and declares faces it never uses. A Check that reports them is switched off.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `font-fallback-clean.html` without `checks` THEN the server SHALL return `isError: false`, `findings` equal to `[]`, no image content block and one text block equal to `No findings in 1 viewport.`; the page holds text in Ahem and in `Wide`, both loaded, a stack of system fonts (`#stack`, `font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif`) and the elements of FNT-17 to FNT-19 and FNT-23 to FNT-25. <!-- FNT-16 -->
2. IF the First family of an element has no Face (`#undeclared` in `font-fallback-clean.html`, `font-family: "Squint No Such Font", Ahem`) THEN the Check SHALL return no Finding for the element. <!-- FNT-17 -->
3. IF a Failed family is in the `font-family` of an element and is not its First family (`#second` in `font-fallback-clean.html`, `font-family: "Squint No Such Font", "Second Choice", Ahem`; `Second Choice` is declared with a `src` that names no file and its Face has the `status` `error`) THEN the Check SHALL return no Finding for the family. <!-- FNT-18 -->
4. IF no element has a Failed family as its First family (`Preloaded` in `font-fallback-clean.html`, whose Face a script of the page adds and loads from a `src` that names no file, and which no `font-family` names) THEN the Check SHALL return no Finding for the family. <!-- FNT-19 -->
5. IF the First family of an element is a Failed family and the element renders in a Face of it that loaded (`#half-normal` in `font-fallback-bounds.html`, `font-family: Half, Wide` and `font-weight: 400`: ten glyphs 200px wide, 300px in its Tail) THEN the Check SHALL return no Finding on the element and SHALL not count it. <!-- FNT-20 -->
6. IF such an element is a text that wraps and fills its lines, so that its box on the page is as wide in the family as in its Tail (`#wrapped` in `font-fallback-bounds.html`, a justified paragraph 300px wide of fourteen words of four glyphs, `font-family: Half, Wide` and `font-weight: 400`) THEN the Check SHALL return no Finding on the element and SHALL not count it: the widths compared are of one line. <!-- FNT-21 -->
7. IF only some of the characters of the Own text of an element are in the `unicode-range` of the Face that failed (`#mixed-both` in `font-fallback-bounds.html`, `font-family: Mixed, Wide` and the text `XXXXXxxxxx`: 250px wide, 300px in its Tail) THEN the Check SHALL return no Finding on the element and SHALL not count it. <!-- FNT-22 -->
8. IF the only element whose First family is a Failed family has a computed `visibility` of `hidden` (`#hidden` in `font-fallback-clean.html`, `font-family: "Hidden Brand", Ahem`; the Face of `Hidden Brand` has the `status` `error`) THEN the Check SHALL return no Finding for the family. <!-- FNT-23 -->
9. IF a Failed family is named only by the `content` of a pseudo-element (`#pseudo` in `font-fallback-clean.html`, an element with no Own text whose `::before` has `content: "XXXXXXXXXX"` and `font-family: "Pseudo Brand", Ahem`) THEN the Check SHALL return no Finding for the family. <!-- FNT-24 -->
10. IF no Face of the First family of an element has a `status` of `error` THEN the Check SHALL return no Finding for that family; in `font-fallback-clean.html` the Faces of these families, each declared with a `src` that names no file, are `unloaded`: `Unused` (no `font-family` names it), `After Generic` (`#after-generic`, `font-family: sans-serif, "After Generic"`), `Never Shown` (`#none`, of `display: none`) and `Blank` (`#blank`, whose text is whitespace). <!-- FNT-25 -->
11. WHEN a Failed family has an element of `visibility: hidden` before the first element that falls back in it (in `font-fallback-bounds.html`, `#veiled`, `font-family: "Veiled Brand", Ahem` and `visibility: hidden`, and after it `#seen`, with the same `font-family`) THEN the Finding of the family SHALL sit on `#seen` and have `evidence.measured.elements` equal to 1. <!-- FNT-26 -->
12. IF the `text-transform` of an element puts its characters in the `unicode-range` of a Face that loaded (`#upper-mixed` in `font-fallback-shaping.html`, `font-family: Mixed, Wide`, the text `xxxxxxxxxx` and `text-transform: uppercase`: 200px wide, 300px in its Tail; `Mixed` is declared as in FNT-09, and `#lower-mixed` after it, the same text without the transform, asks for the Face that failed) THEN the Check SHALL return no Finding on the element and SHALL not count it. <!-- FNT-49 -->
13. WHEN a Failed family has an element of `display: none` before the first element that falls back in it (in `font-fallback-bounds.html`, `#unshown`, `font-family: "Unshown Brand", Ahem` and `display: none`, and after it `#shown`, with the same `font-family`) THEN the Finding of the family SHALL sit on `#shown` and have `evidence.measured.elements` equal to 1: text that paints no box is not judged, though its two Line widths are equal. <!-- FNT-52 -->
14. IF the First family of an element has a Face, none of its Faces has a `status` of `error` and the element renders in its Tail (`#out-of-range` in `font-fallback-bounds.html`, `font-family: "Upper Only", Ahem` and the text `xxxxxxxxxx`; the one Face of `Upper Only` is for `U+0041-005A`, has a `src` that names no file and stays `unloaded`, since no character of the text is in its range: 200px wide, 200px in its Tail) THEN the Check SHALL return no Finding for the family. <!-- FNT-53 -->
15. IF the First family of an element is a Failed family and the element renders in a Face of it that loaded and is wider than its Tail (`#broad-normal` in `font-fallback-judged.html`, `font-family: Broad, Ahem` and `font-weight: 400`: ten glyphs 300px wide, 200px in its Tail; `Broad` has a Face of weight 400 from the file of Ahem with `size-adjust: 150%` and one of weight 700 with a `src` that names no file, which `#broad-bold`, after it and with the same `font-family`, asks for) THEN the Check SHALL return no Finding on the element and SHALL not count it: the Finding of `Broad` sits on `#broad-bold`, with `evidence.measured.elements` equal to 1. <!-- FNT-55 -->
16. WHEN a Failed family has an element whose computed `visibility` is neither `visible` nor `hidden` before the first element that falls back in it (in `font-fallback-judged.html`, `#folded`, `font-family: "Folded Brand", Ahem` and `visibility: collapse`, and after it `#unfolded`, with the same `font-family`) THEN the Finding of the family SHALL sit on `#unfolded` and have `evidence.measured.elements` equal to 1: an element is judged only when its `visibility` is `visible`. <!-- FNT-56 -->
17. WHEN a Failed family has an element whose Own text is only whitespace and paints a box before the first element that falls back in it (in `font-fallback-judged.html`, `#spaces`, `font-family: "Space Brand", Ahem` and `white-space: pre`, whose text is five spaces, and after it `#after-spaces`, with the same `font-family`) THEN the Finding of the family SHALL sit on `#after-spaces` and have `evidence.measured.elements` equal to 1: Own text that is only whitespace is not judged, though it paints a box and its two Line widths are equal. <!-- FNT-57 -->

**Independent Test**: Call `detect_visual_bugs` on `font-fallback-clean.html`: four faces of the page failed and nothing is reported.

---

### P1: Read the Finding

**User Story**: As a coding agent, I want the Finding to name the family that did not load and say how far the fault reaches, so that I can go to the one place that loads it.

**Why P1**: The element a Finding sits on is where the fault shows, not where it is fixed. Without the family the agent has to work it out from `font-family`.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called on `font-fallback-bug.html` with `checks` equal to `["font-fallback"]` THEN the Finding of `#heading` SHALL equal `{"check": "font-fallback", "category": "visual-bug", "severity": "minor", "message": "The font \"Brand\" did not load: the text of 3 elements is rendered in a fallback font", "selector": "#heading", "text": "XXXXXXXXXX", "box": {"x": 40, "y": 20, "w": 200, "h": 30}, "viewport": {"width": 1440, "height": 900}, "evidence": {"computed": {"font-family": "Brand, Ahem", "font-weight": "400", "font-style": "normal"}, "measured": {"family": "Brand", "elements": 3, "textWidthPx": 200}, "cropIndex": 0}, "suggestion": "Fix the source the page loads \"Brand\" from, or take the family out of font-family", "source": "Squint heuristic"}`. <!-- FNT-27 -->
2. WHEN one element falls back in a Failed family THEN the `message` of its Finding SHALL say `element`, not `elements`: for `#icon` in `font-fallback-bug.html`, `The font "Icon Set" did not load: the text of 1 element is rendered in a fallback font`. <!-- FNT-28 -->
3. WHEN the element a Finding sits on writes the family in another case than its Face has it (`#lower` in `font-fallback-bounds.html`) THEN `evidence.measured.family` SHALL be the name as the Face has it, `Missing Brand`, and `evidence.computed` SHALL hold the `font-family` of the element as computed, `"missing brand", Ahem`. <!-- FNT-29 -->
4. WHEN the Own text of the element a Finding sits on wraps (`#long` in `font-fallback-bounds.html`, a block 100px wide with the text `XXXX XXXX XXXX` and `font-family: "Long Brand", Ahem`) THEN `evidence.measured.textWidthPx` SHALL be its width on one line, 280, and the `w` of its `box` SHALL be 100. <!-- FNT-30 -->
5. WHEN the element a Finding sits on is not of normal weight (`#half-bold` in `font-fallback-bounds.html`) THEN `evidence.computed` SHALL equal `{"font-family": "Half, Wide", "font-weight": "700", "font-style": "normal"}` and `evidence.measured.textWidthPx` SHALL be 300, the width of its ten glyphs in `Wide`. <!-- FNT-31 -->
6. WHEN the `selector` of any Finding of `font-fallback-bug.html` or `font-fallback-bounds.html` is passed to `inspect_element` with the same `url` and `viewport` THEN `inspect_element` SHALL return `isError: false` with a `box` equal to the Finding's `box`. <!-- FNT-32 -->
7. WHEN the element a Finding sits on has a `letter-spacing` and a `word-spacing` (`#spaced` in `font-fallback-shaping.html`, an inline element of `font-family: "Spaced Brand", Ahem`, `letter-spacing: 2px` and `word-spacing: 6px` with the text `XXXX XXXXX`) THEN `evidence.measured.textWidthPx` SHALL be 226: nine glyphs of 20px, a space of 20px, 2px after each of the ten characters and 6px at the space. <!-- FNT-51 -->
8. WHEN the Own text of the element a Finding sits on is more than one text node (`#split` in `font-fallback-bounds.html`, `font-family: "Split Brand", Ahem`, which holds the text `XXX`, a child `#split-child` of `font-family: Ahem` with the text `XX`, and the text `XXXX`) THEN `evidence.measured.textWidthPx` SHALL be 140, the widths of its two text nodes added, and `evidence.measured.elements` SHALL be 1. <!-- FNT-54 -->
9. WHEN the Faces of a Failed family write its name in different cases (in `font-fallback-names.html`, the Face of weight 400 is declared as `Dual` and after it the Face of weight 700 as `DUAL`, each with a `src` that names no file; `#dual-normal` and after it `#dual-bold`, of `font-weight: 700`, both have `font-family: Dual, Ahem`) THEN the Check SHALL return one Finding for the family, on `#dual-normal`, with `evidence.measured.family` equal to `Dual`, the name as the first of its Faces has it, and `evidence.measured.elements` equal to 2. <!-- FNT-58 -->
10. WHEN the element a Finding sits on is a block of `direction: rtl` whose text is in a font of the machine and ends in a full stop (`#turned` in `font-fallback-shaping.html`, of `display: inline-block`, `direction: rtl` and `font-family: "Turned Brand", serif`, with the text `PLAY.`) THEN `evidence.measured.textWidthPx` SHALL equal the `w` of its `box` rounded to two decimal places: the text is measured in the direction of its element, in which the full stop stands apart from the letter before it and is not kerned with it. <!-- FNT-61 -->
11. WHEN the element a Finding sits on has `text-rendering: optimizeSpeed` and its text is in a font of the machine that has ligatures (`#swift` in `font-fallback-shaping.html`, an inline element of `font-family: "Swift Brand", Calibri, FreeSerif` that holds the text `fifth office file` on one line and nothing else; Calibri is a font of Windows and FreeSerif one of the Linux the tests run on) THEN `evidence.measured.textWidthPx` SHALL equal the `w` of its `box` rounded to two decimal places: the text is measured without its ligatures, as it is painted. <!-- FNT-62 -->

**Independent Test**: Read the Finding of `#heading` and compare it with the literal above.

---

### P1: With the other Checks

**User Story**: As a coding agent, I want `font-fallback` to run with the other Checks in one call and in the same order of Findings, so that nothing about how I read a result changes.

**Why P1**: A fifth Check must not change what the first four report.

**Acceptance Criteria**:

1. WHEN `detect_visual_bugs` is called without `checks` THEN the server SHALL run `font-fallback`, `low-contrast-real`, `offscreen-overflow`, `overlap` and `text-clipped`. <!-- FNT-33 -->
2. IF `checks` holds a name that is not a Check THEN the server SHALL return `isError: true` with a text block containing `Unknown check "nope". Valid checks: font-fallback, low-contrast-real, offscreen-overflow, overlap, text-clipped.` (for `["nope"]`); this supersedes the literal in force since slice 8. <!-- FNT-34 -->
3. WHEN `detect_visual_bugs` is called with `checks` equal to `["low-contrast-real", "offscreen-overflow", "overlap", "text-clipped"]` on `font-fallback-bug.html` THEN `findings` SHALL equal `[]`. <!-- FNT-35 -->
4. WHEN Findings of the same severity and viewport come from `font-fallback` and from another Check THEN they SHALL be ordered by the document order of their elements and, on one element, by Check name; on `font-fallback-order.html`, whose elements in document order are `#a` (`font-family: One, Ahem`, with `One` failed), `#b` (`font-family: Two, Ahem`, with `Two` failed, and text of `rgb(119, 119, 119)` on white) and `#c` (`font-family: Ahem`, text of `rgb(119, 119, 119)` on white), all `minor`, the `(selector, check)` pairs of `findings` SHALL be `(#a, font-fallback)`, `(#b, font-fallback)`, `(#b, low-contrast-real)`, `(#c, low-contrast-real)`. <!-- FNT-36 -->
5. WHEN the tools are listed THEN the description of `detect_visual_bugs` SHALL name `font-fallback` and say that it reports a font the page declares that did not load, one Finding per family. <!-- FNT-37 -->
6. WHEN the tests of the earlier slices run after this slice THEN every test SHALL pass with no change other than the literal of FNT-34 in the four assertions of `tests/test_detect_visual_bugs.py` that hold it (lines 342, 353, 364 and 376 before this slice). <!-- FNT-38 -->
7. WHEN `detect_visual_bugs` is called with `checks` equal to `["font-fallback"]` on `font-fallback-many.html`, a page of 1,000 elements of two glyphs each in `font-family: Brand, Ahem` with `Brand` failed, THEN the server SHALL return `isError: false` and exactly one Finding, with `evidence.measured.elements` equal to 1000. <!-- FNT-39 -->

**Independent Test**: Call `detect_visual_bugs` on `font-fallback-order.html` and read the four pairs in order.

---

### P2: Check contract, Capture and documents

**User Story**: As the maintainer, I want the Check to follow the contract of slice 3 and the Capture to pay for its facts only when they are read, so that the next Check is as cheap as this one.

**Why P2**: Not observable by a client; required by the roadmap and by AD-003 and AD-005.

**Acceptance Criteria**:

1. The `font-fallback` Check SHALL be one module under `src/squint_mcp/checks/` holding a function from a Capture to a list of Findings, registered by name in `checks/__init__.py` (AD-003). <!-- FNT-40 -->
2. The modules under `src/squint_mcp/checks/` SHALL NOT import `playwright` (ADR-0002). <!-- FNT-41 -->
3. The Check SHALL read the Faces and the Line widths from the Capture, and the Capture SHALL measure them only when a Check that reads them is among the Checks of the call (AD-003, AD-005). <!-- FNT-42 -->
4. The `font-fallback` module SHALL compare the two Line widths of an element for equality and SHALL hold no tolerance; the `config` module SHALL gain no threshold for this Check. <!-- FNT-43 -->
5. `CHANGELOG.md` SHALL list the `font-fallback` Check under the unreleased version: one Finding per family, its severity, that only the first family of `font-family` is judged and only when the page declares it, and what it does not report (a family that is only named, a font that loaded and is not used, text of pseudo-elements, text of `visibility: hidden`). <!-- FNT-44 -->
6. `README.md` SHALL name `font-fallback` among the Checks that `detect_visual_bugs` runs and give their number as five. <!-- FNT-45 -->
7. WHEN the Verifier's report is PASS THEN `docs/ROADMAP.md` SHALL show slice 9 as `concluída`, in the table and in its section, with a link to this feature's directory. <!-- FNT-46 -->

**Independent Test**: Read the files named above.

---

## Edge Cases

- WHEN `detect_visual_bugs` is called on `font-fallback-bug.html` with two viewports THEN each Finding of the first viewport SHALL have a Finding of the same `selector`, `check` and `evidence.measured.family` in the second. <!-- FNT-47 -->
- WHEN every Face of a family failed and elements ask for different ones (in `font-fallback-bounds.html`, `Twice` has a Face of weight 400 and one of weight 700, each with a `src` that names no file; `#twice-normal` and after it `#twice-bold`, of `font-weight: 700`, both have `font-family: Twice, Ahem`) THEN the Check SHALL return one Finding for the family, on `#twice-normal`, with `evidence.measured.elements` equal to 2: Findings are per family, not per Face. <!-- FNT-48 -->

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| FNT-01 | P1: Report a font that did not load | T2 | Implemented |
| FNT-02 | P1: Report a font that did not load | T2 | Implemented |
| FNT-03 | P1: Report a font that did not load | T2 | Implemented |
| FNT-04 | P1: Report a font that did not load | T2 | Implemented |
| FNT-05 | P1: Report a font that did not load | T5 | Implemented |
| FNT-06 | P1: Report a font that did not load | T5 | Implemented |
| FNT-07 | P1: Report a font that did not load | T2 | Implemented |
| FNT-08 | P1: Report a font that did not load | T5 | Implemented |
| FNT-09 | P1: Report a font that did not load | T5 | Implemented |
| FNT-10 | P1: Report a font that did not load | T5 | Implemented |
| FNT-11 | P1: Report a font that did not load | T6 | Implemented |
| FNT-12 | P1: Report a font that did not load | T6 | Implemented |
| FNT-13 | P1: Report a font that did not load | T2 | Implemented |
| FNT-14 | P1: Report a font that did not load | T8 | Implemented |
| FNT-15 | P1: Report a font that did not load | T5 | Implemented |
| FNT-16 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-17 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-18 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-19 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-20 | P1: Stay silent when the text is in the font it asks for | T6 | Implemented |
| FNT-21 | P1: Stay silent when the text is in the font it asks for | T6 | Implemented |
| FNT-22 | P1: Stay silent when the text is in the font it asks for | T6 | Implemented |
| FNT-23 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-24 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-25 | P1: Stay silent when the text is in the font it asks for | T4 | Implemented |
| FNT-26 | P1: Stay silent when the text is in the font it asks for | T6 | Implemented |
| FNT-27 | P1: Read the Finding | T3 | Implemented |
| FNT-28 | P1: Read the Finding | T2 | Implemented |
| FNT-29 | P1: Read the Finding | T5 | Implemented |
| FNT-30 | P1: Read the Finding | T6 | Implemented |
| FNT-31 | P1: Read the Finding | T6 | Implemented |
| FNT-32 | P1: Read the Finding | T6 | Implemented |
| FNT-33 | P1: With the other Checks | T2 | Implemented |
| FNT-34 | P1: With the other Checks | T1 | Implemented |
| FNT-35 | P1: With the other Checks | T2 | Implemented |
| FNT-36 | P1: With the other Checks | T9 | Implemented |
| FNT-37 | P1: With the other Checks | T1 | Implemented |
| FNT-38 | P1: With the other Checks | T1 | Implemented |
| FNT-39 | P1: With the other Checks | T9 | Implemented |
| FNT-40 | P2: Check contract, Capture and documents | T1 | Implemented |
| FNT-41 | P2: Check contract, Capture and documents | T2 | Implemented |
| FNT-42 | P2: Check contract, Capture and documents | T2 | Implemented |
| FNT-43 | P2: Check contract, Capture and documents | T2 | Implemented |
| FNT-44 | P2: Check contract, Capture and documents | T11 | Implemented |
| FNT-45 | P2: Check contract, Capture and documents | T11 | Implemented |
| FNT-46 | P2: Check contract, Capture and documents | T12 | Implemented |
| FNT-47 | Edge cases | T2 | Implemented |
| FNT-48 | Edge cases | T5 | Implemented |
| FNT-49 | P1: Stay silent when the text is in the font it asks for | T7 | Implemented |
| FNT-50 | P1: Report a font that did not load | T7 | Implemented |
| FNT-51 | P1: Read the Finding | T7 | Implemented |
| FNT-52 | P1: Stay silent when the text is in the font it asks for | T6 | Implemented |
| FNT-53 | P1: Stay silent when the text is in the font it asks for | T5 | Implemented |
| FNT-54 | P1: Read the Finding | T6 | Implemented |
| FNT-55 | P1: Stay silent when the text is in the font it asks for | F1 | Implemented |
| FNT-56 | P1: Stay silent when the text is in the font it asks for | F1 | Implemented |
| FNT-57 | P1: Stay silent when the text is in the font it asks for | F1 | Implemented |
| FNT-58 | P1: Read the Finding | F2 | Implemented |
| FNT-59 | P1: Report a font that did not load | F2 | Implemented |
| FNT-60 | P1: Report a font that did not load | F2 | Implemented |
| FNT-61 | P1: Read the Finding | F3 | Implemented |
| FNT-62 | P1: Read the Finding | F3 | Implemented |
| FNT-63 | P1: Report a font that did not load | F4 | Implemented |

**Coverage:** 63 total, 63 mapped to tasks, 0 unmapped. The Phase column names the task of [`tasks.md`](tasks.md).

---

## Success Criteria

- [ ] All 63 requirements verified by the Verifier, FNT-40 to FNT-46 from file evidence.
- [ ] The gate passes: typecheck, lint, format check and the whole test suite.
- [ ] The first run of the suite on the CI's Linux passes the tests of this slice with no assertion changed for it.
- [ ] The discrimination sensor leaves alive none of the mutants that a validation report or a task names, nor any of the code the last fix round changed, in the Check and in what the Capture gains for it (Assumptions, "When the discrimination sensor is satisfied").
