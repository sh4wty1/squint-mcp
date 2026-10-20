# Measure a page whose policy refuses inline styles

Issue [#26](https://github.com/sh4wty1/squint-mcp/issues/26).

## Problem

A Capture adds styles of its own to the page it examines: the one that takes time out of the render (`stabilize.js`), the text fills of AD-004 (`fill_text.js`) and the paint and highlight colours of covered text (`covered_text.js`). Each is a `<style>` element the Capture appends. A page whose Content Security Policy refuses inline styles (`style-src file:`, or any `style-src` without `'unsafe-inline'`) refuses every one of them. The fills never apply, so `background` and `ink` hold the page as painted, no text has ink, and every Check that reads text pixels finds nothing.

The cost: an agent asks for Findings on such a page and gets `No findings`, with no error. A clean result is indistinguishable from a page that could not be measured, and the agent reports a broken page as clean.

Evidence, from the issue: on Chromium 153 on Windows, a page with `style-src file:`, a covered text and a low-contrast text returns `No findings` from `detect_visual_bugs`. Found while slice 8 was verified (`.specs/features/overlap/design.md:267`).

Spiked for this plan on Chromium 153 (a `style-src file:` meta policy and a same-folder sheet):

| Route | Fill applied | Page's policy |
| --- | --- | --- |
| `<style>` appended (today) | no, refused with a console error | in force |
| `<style>` appended, context with `bypass_csp=True` | yes | not applied |
| constructable sheet (`new CSSStyleSheet()` + `replaceSync`, added to `adoptedStyleSheets`) | yes, in the document, in an open shadow root, and for `::highlight()` | in force |
| `element.style.setProperty` (already used by `font_widths.js` and `covered_text.js`) | yes | in force |

When this ships: a page under a `style-src` policy gets the same Findings as the same page without it, and the page's policy still applies to the page's own styles.

## Flow

Reuses every page script the Capture already runs and the walk over open shadow roots they share. Only the way each one adds its rules changes, from a `<style>` element to a constructable sheet the policy does not cover.

1. a call -> `capture.capture` (exists) - opens the context as today, with no change to its options
2. `js/stabilize.js` (exists) - adds its rules to each root as a constructable sheet (door 1)
3. `js/author_styles.js` (exists) - leaves out the sheets the Capture added (door 1), as it leaves out its `<style>` elements today
4. `js/fill_text.js` (exists) - sets the fill in one constructable sheet per root, replaced on each of the three fills (door 1)
5. `js/covered_text.js` (exists) - its two rule sets per root, what is painted and the highlight colours, become constructable sheets (door 1)
6. out: the same Capture, now with ink on such a page, to every tool and Check

## Impact

| Front | What changes |
| --- | --- |
| domain | no term changes. "The styles Squint adds" (`author_styles.js`) are now sheets on `adoptedStyleSheets`, not `<style>` elements |
| Capture | the `<style data-squint-stabilize>` elements are no longer in the page when the collector runs, so `*` no longer collects them as elements of the page. No Check reads a `<style>` element; any test that counts every element of a page changes by one per root |
| page | a page that sets `adoptedStyleSheets` itself keeps its own sheets: the Capture appends to the list and never replaces it |
| contract | no tool result changes shape. On a page with a `style-src` policy, the Findings change from none to those the page has |
| stored data | nothing to migrate - nothing is persisted |

## Relations

`None - no stored-data shape change`

## Surface

`None - no route changes: the three tools keep their arguments and results (AD-002); what changes is what their Captures measure on one kind of page`

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1. How the Capture adds a style to a page | `const sheet = new CSSStyleSheet(); sheet.replaceSync(css); root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet];`, each sheet kept in `globalThis.__squintSheets` (a `WeakSet`, after `__squintElements` of AD-005), which `author_styles.js` skips. Every later page script copies this, so it is precedent; recorded as AD-011 | `bypass_csp=True` on the context, the issue's first route - the page's own policy stops applying, so a page whose policy refuses one of its own inline styles or a third-party sheet is captured with them: Findings on a page nobody sees. A `ToolError` when the fill is refused, the issue's second route - the page is measurable, and an error would leave it unexamined |

- Nothing else in this change is hard to reverse: the marker set and which root holds which sheet are internal to the page scripts

## Criteria

### S1: a page under a style-src policy gets its Findings (P1)

The same page, with and without a policy that refuses inline styles, gives the same Findings, and the page's policy still holds for the page.

**Acceptance Criteria**

1. WHEN `detect_visual_bugs` is called on a page whose policy is `<meta http-equiv="Content-Security-Policy" content="style-src file:">`, with its styles in a same-folder sheet, holding one text of 4.47:1 on white THEN the system SHALL return one `low-contrast-real` Finding on that text, as it does on the same page without the policy
2. WHEN `detect_visual_bugs` is called on that page holding one text that an opaque box covers by 60% THEN the system SHALL return one `overlap` Finding on that text, as it does on the same page without the policy
3. WHEN `detect_visual_bugs` is called on that page holding a text of 4.47:1 inside an open shadow root THEN the system SHALL return one `low-contrast-real` Finding on that text
4. WHEN the page under that policy also holds an inline `<style>` that paints one text `rgb(255, 0, 0)` THEN `inspect_element` on that text SHALL return its colour from the same-folder sheet, not `rgb(255, 0, 0)`: the page's policy still refuses the page's own inline style
5. WHEN the page sets `document.adoptedStyleSheets` to a sheet of its own at load that paints one text at 4.47:1 on white THEN `detect_visual_bugs` SHALL return one `low-contrast-real` Finding on that text: the Capture keeps the page's adopted sheets
6. WHEN `extract_tokens` is called on a page with no style of its own THEN the system SHALL still return `authorStyles: false`: the sheets the Capture adds are not the page's

**Independent test:** `tests/fixtures/csp-*.html` through `detect_visual_bugs` and `inspect_element`; without the change AC 1, 2, 3 and 5 return no Finding.

## Out of scope

| Excluded | Why |
| --- | --- |
| An error when a page refuses something else the Capture needs | Nothing else is refused: page scripts run through Playwright's `evaluate`, which `script-src` does not reach, and the other style changes go through `element.style`, which `style-src` does not reach (spiked) |
| A policy sent as an HTTP header | The tests serve `file://` pages, which carry no headers; Chromium applies `style-src` the same way from a header and from a `<meta>`, and a constructable sheet is outside both |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| A page that replaces `adoptedStyleSheets` after the Capture added its sheets | Not handled: its sheets drop the Capture's, as today a page that removes a `<style>` it did not add would | A page script that reassigns the list between two screenshots is as rare as one that removes foreign `<style>` elements; same ceiling as today | n |
| The route itself, instead of the two the issue names | Constructable sheets, no `bypass_csp` and no error | The issue asks the maintainer to decide `bypass_csp` because it changes how the page behaves; this route does not, so it needs only the plan's review | y |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| `detect_visual_bugs`, `inspect_element`, `extract_tokens` | result and error shape | existing - unchanged (AD-002) |
| the three tools | what a page under a `style-src` policy returns | AC 1 to 5 |

## Sources

- Issue [#26](https://github.com/sh4wty1/squint-mcp/issues/26) - the measured case and the two routes it names
- `.specs/features/overlap/design.md:267` - where the risk was first written down
