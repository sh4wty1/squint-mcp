# extract-tokens Specification

Roadmap slice 10 (`docs/ROADMAP.md`). Decisions taken with the maintainer are in [`context.md`](context.md).

---

## Problem Statement

An agent that edits a page has no way to learn which colours, type sizes, spacings, radii and shadows the page already uses, short of reading every stylesheet or guessing from a screenshot. `extract_tokens` reads them from the rendered page and returns them as counted lists, with values that differ by less than the eye or the pixel grid can tell folded into one token. It is the first tool that returns no Findings: it reports what the page uses and judges nothing.

## Goals

- [ ] `extract_tokens(url, scope?, viewport?)` returns the palette, the type scale, the spacings, the radii and the shadows of a page as structured content plus a one-line text summary, with no image.
- [ ] A value counts only where it paints, and each token says how many elements use it.
- [ ] Colours closer than one just noticeable difference (ΔE2000 below 2) and px lengths less than 1px apart are one token whose variants stay listed.
- [ ] The result is the same on every call, and each list is bounded with its full count reported.
- [ ] Every threshold lives in `config.py` with its source.

## Terms

Used by the criteria below; each is defined once here.

- **Scope**: without `scope`, every element of the page. With `scope`, every element the selector matches and every descendant of one, elements of open shadow trees included; an element is in the Scope once, however many matches it is under.
- **Read element**: an element of the Scope whose box as painted has a width above 0 and a height above 0, whose computed `visibility` is `visible`, and whose opacity multiplied by that of every ancestor is above 0. Tokens are read from Read elements only.
- **Painted text**: the text nodes that are direct children of an element (Own text, as in the Checks), when at least one of them paints a box.
- **Family**: one of the eight lists of the result: `colors`, `typography.families`, `typography.sizes`, `typography.weights`, `typography.lineHeights`, `spacing`, `radii`, `shadows`.
- **Role**: where a value is used. `colors` has `text`, `background` and `border`; `spacing` has `margin`, `padding` and `gap`. The other Families have a single Role.
- **Value**, by Family:
  - `colors`: a colour of alpha above 0, written in sRGB as `#rrggbb` in lower case, each channel rounded to 8 bits and clipped to 0..255; when its alpha, rounded half up to 8 bits, is below 255, as `#rrggbbaa`. Role `text`: the computed `-webkit-text-fill-color` of an element with Painted text. Role `background`: the computed `background-color`. Role `border`: the computed `border-<side>-color` of each side whose border width is above 0.
  - `typography.*`, on elements with Painted text only: `families` is the computed `font-family` text; `sizes` the computed `font-size` in px; `weights` the computed `font-weight` number; `lineHeights` the computed `line-height` when it is a px length (`normal` is no Value).
  - `spacing`: a px length above 0. Role `margin`: each side's margin that the page does not give as `auto`. Role `padding`: each side's padding. Role `gap`: the computed `row-gap` and `column-gap` of an element whose computed `display` is `flex`, `inline-flex`, `grid` or `inline-grid`.
  - `radii`: the computed value text of each of the four corner radius properties, unless both of its radii are zero.
  - `shadows`: the whole computed `box-shadow` text when it is not `none` (`kind` `box`), and the whole computed `text-shadow` text of an element with Painted text when it is not `none` (`kind` `text`). The `kind` is part of the Value.
- **Length**: a Value that is one number of px: every Value of `typography.sizes`, `typography.lineHeights` and `spacing`, and a Value of `radii` whose text is a single px length.
- **Use**: one Read element having one Value in one Role. The same Value on several sides, corners or axes of one element in one Role is one Use.
- **Near**: two colours are Near when their alphas, as 8 bits, are equal and their ΔE2000 is below 2. Two Lengths of one Family are Near when they differ by less than 1px. No other two Values are Near.
- **ΔE2000**: the CIEDE2000 colour difference (CSS Color Module Level 4, section 20.2) between two colours taken to CIE Lab with a D50 white as that module converts sRGB.
- **Rank order**: by Uses, most first; then by Value, ascending: numbers by size, texts by code point. For `shadows`, `box` before `text`, then the text.
- **Group**: the Values of a Family are walked in Rank order. A Value joins the Group whose Representative is Near it and nearest to it (smallest ΔE2000, or smallest difference in px); when two are equally near, the one opened first. A Value Near no Representative opens a Group and is its Representative. A Value is compared with Representatives only, and never moves once placed.
- **Token**: one Group as it is returned: `value` is its Representative, `uses` the Uses of all its Values, `roles` (where the Family has Roles) those Uses by Role, and `variants` (where the Family can group: `colors`, `sizes`, `lineHeights`, `spacing`, `radii`) each of its Values with its own `uses`, in Rank order.
- **Family order**: `colors`, `typography.families` and `shadows` in Rank order of their Tokens. `typography.sizes`, `typography.weights`, `typography.lineHeights` and `spacing` by `value`, ascending. `radii`: the Tokens whose `value` is a Length by size, ascending, then the others by text.
- **Limit**: 20 Tokens per Family.

## Fixtures

Pages under `tests/fixtures/`, opened by `file://`. Each but `tokens-default.html` sets `margin: 0` on `html` and `body` and gives every element its styles explicitly, so that no value of the browser's default stylesheet is counted unless a criterion says so.

`tokens-page.html` holds, in document order, with `body` set to `font-family: Arial, sans-serif; background-color: #ffffff` and no Own text:

| Element | Own text | Styles |
| --- | --- | --- |
| `#title` | yes | `color: #333333; font-size: 32px; line-height: 40px; font-weight: 700; margin-bottom: 24px` |
| `#lead` | yes | `color: #333333; font-size: 16px; line-height: 24px; font-weight: 400; margin-bottom: 16px` |
| `#card` | no | `display: flex; gap: 8px; padding: 16px; background-color: #eeeeee; border: 1px solid #cccccc; border-radius: 8px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2)` |
| `#card-a`, in `#card` | yes | `color: #1a73e8; font-size: 14px; line-height: 20px; font-weight: 400` |
| `#card-b`, in `#card` | yes | `color: #333333; font-size: 14px; line-height: 20px; font-weight: 700` |
| `#button` | yes | `color: #ffffff; background-color: #1a73e8; font-size: 14px; line-height: 20px; font-weight: 700; padding: 8px 16px; border-radius: 4px` |

The other fixtures (`tokens-used.html`, `tokens-groups.html`, `tokens-scope.html`, `tokens-limit.html`, `tokens-viewport.html`, `tokens-default.html`) are described by the criteria that read them. In them an element named with a colour is a box of 100px by 20px with that `background-color` and no Own text, unless the criterion says otherwise.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Consistency rules, a score, Findings about tokens | Phase 4 (`audit_ui`). This tool reports and does not judge. |
| Comparison with a design system | Not in the slice (roadmap). |
| Reading colours from the pixels | Decided with the maintainer: pixels hold anti-aliasing blends, images and the middle of gradients, none of which is a token. |
| The names of CSS custom properties (`--brand`) | The tool returns the values elements use, not how the stylesheet names them. |
| Gradient stops, SVG `fill` and `stroke`, the colours inside a shadow, `outline-color`, `text-decoration-color` | The palette has three Roles: text, background, border. |
| Styles of pseudo-elements and the text of form controls (values, placeholders) | Neither is in the computed style of an element with Painted text. |
| Telling an element that is clipped away or moved off the page from one that is seen | That needs the pixels; a Read element is defined from CSS and its box. |
| Line heights as ratios, `letter-spacing`, border widths, sizes of boxes | The roadmap names five kinds of token; computed line heights are px. |
| `gap` of multi-column containers, and a `gap` that is not a px length | Rare; a percentage gap has no px value in the computed style. |
| A limit on the `variants` of one Token | A Group is at most 2 ΔE2000 or 1px from its Representative on each side. |
| Several viewports in one call | One Capture per call, as `inspect_element`. |
| Export to a token file format | Not in the slice. |
| Closed shadow roots, iframes, states of interaction (hover, focus) | As every other tool. |
| The two limits found outside slice 8 (a Content Security Policy that refuses inline styles; a right-to-left page that scrolls sideways) | Limits of the Capture, recorded in `.specs/STATE.md`. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Where tokens are read | The computed CSS only; a value counts only where it paints. The Capture gains no fact on request: the generic collector reads more properties, which is for Design | Maintainer, 2026-10-13 (`context.md`) | y |
| `scope` | A CSS selector; the matches and all their descendants, each element once; no match is an error; without it, the whole page | Maintainer, 2026-10-13 | y |
| Typography | Four separate lists, not composite text styles | Maintainer, 2026-10-13 | y |
| Limit per Family | At most N Tokens, the full count in `total` | Maintainer, 2026-10-13 | y |
| ΔE formula and threshold | ΔE2000, Near below 2. CSS Color 4, section 20.2 for the formula and section 14.2.1 (a note) for "using deltaE2000, one JND is 2"; the module compares with `E < JND` | Maintainer, 2026-10-13. The module gives that JND for gamut mapping; reading it as "two colours a viewer cannot tell apart are one token" is ours | y |
| Lengths | Near when less than 1px apart, for every px length of the result | Maintainer, 2026-10-13. Squint default, no norm found: a Capture has one image pixel per CSS pixel, and whole steps of a scale (12, 13, 14) stay apart | y |
| The value of N | 20 | Squint default: eight lists of 20 bound a response to 160 Tokens, and a scale longer than 20 says so through `total`. Not measured on real pages | y |
| Which Group a Value joins | The nearest Representative among those Near it; a tie goes to the Group opened first | In chat the agent said "the first Group whose Representative is Near". Nearest reads better: 16.8px goes with 17px, not with a more used 16px | y |
| What a Use counts | One element, one Value, one Role; four equal sides are one Use. `uses` of a Token is the sum of its Roles | An element with `padding: 8px` uses 8 once | y |
| Text colour | The computed `-webkit-text-fill-color`, which paints the glyphs and equals `color` unless the page sets it (AD-004) | "Only where it paints": a gradient text with a transparent fill has no text colour | y |
| Colours outside sRGB or in another notation | Converted to sRGB and clipped channel by channel | The result is 8-bit hex; gamut mapping is more than a token list needs | y |
| Radii and box shadows | Counted on every Read element that has one, whatever else it paints | What makes a radius show (background, border, shadow, clipping, an image) is a long list, and a radius on an element with none of them is rare | y |
| Values of the browser's default stylesheet | Counted like any other: the 8px margin of a `body` the page does not reset is a Use | The page paints with them; the tool cannot tell who declared a value | y |
| Negative and zero spacing | Not Values | A negative margin is a layout device, zero is the absence of spacing | y |
| `viewport` input | Optional, one viewport, default 1440x900, as `inspect_element`. The roadmap lists only `url` and `scope?` | Tokens change with media queries | y |
| Text of the computed shadows | As Chromium serializes them (`rgba(0, 0, 0, 0.2) 0px 1px 3px 0px`) | The criteria quote these texts from memory; Design confirms them on Chromium 153 | y |
| ΔE2000 is tested below the MCP seam | One test calls the colour-difference function on the 34 pairs of the published test data | The tool takes 8-bit sRGB colours; the test data is in Lab and cannot go through it | y |
| ΔE values quoted in the criteria | Computed for this spec with a script checked on 12 rows of the test data (worst error 0.00004) | Design recomputes them with the shipped function | y |

**Open questions:** none - all resolved or logged above. The maintainer confirmed the spec as written on 2026-10-13, the twelve rows the agent had chosen alone included.

### Implicit-requirement dimensions

- Input validation & bounds: TOK-57 to TOK-61, TOK-67, TOK-69.
- Failure / partial-failure states: TOK-57, TOK-58, TOK-69 to TOK-72.
- Idempotency / retry / duplicate handling: TOK-12.
- Auth boundaries & rate limits: N/A because the server is local, over stdio, and the tool reads one page per call.
- Concurrency / ordering: the order of every list is fixed (TOK-01 to TOK-08, TOK-40, TOK-43, TOK-62); calls share nothing but the browser (AD-001).
- Data lifecycle / expiry: N/A because the tool stores nothing.
- Observability: N/A because stdout belongs to the protocol and no tool logs; `stabilized` is the one signal (TOK-73).
- External-dependency failure: the page is the dependency (TOK-70, TOK-71, TOK-73).
- State-transition integrity: N/A because a call holds no state.

---

## User Stories

### P1: Read the tokens of a page ⭐ MVP

**User Story**: As a coding agent, I want the tokens a page uses, so that what I add matches what is there.

**Why P1**: It is the tool.

**Acceptance Criteria**:

1. WHEN `extract_tokens` is called on `tokens-page.html` without `scope` THEN the `(value, uses, roles.text, roles.background, roles.border)` of `colors.tokens` SHALL be, in this order, `(#333333, 3, 3, 0, 0)`, `(#1a73e8, 2, 1, 1, 0)`, `(#ffffff, 2, 1, 1, 0)`, `(#cccccc, 1, 0, 0, 1)` and `(#eeeeee, 1, 0, 1, 0)`. <!-- TOK-01 -->
2. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses)` of `typography.families.tokens` SHALL be `(Arial, sans-serif, 5)` alone. <!-- TOK-02 -->
3. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses)` of `typography.sizes.tokens` SHALL be, in this order, `(14, 3)`, `(16, 1)` and `(32, 1)`. <!-- TOK-03 -->
4. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses)` of `typography.weights.tokens` SHALL be, in this order, `(400, 2)` and `(700, 3)`. <!-- TOK-04 -->
5. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses)` of `typography.lineHeights.tokens` SHALL be, in this order, `(20, 3)`, `(24, 1)` and `(40, 1)`. <!-- TOK-05 -->
6. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses, roles.margin, roles.padding, roles.gap)` of `spacing.tokens` SHALL be, in this order, `(8, 2, 0, 1, 1)`, `(16, 3, 1, 2, 0)` and `(24, 1, 1, 0, 0)`. <!-- TOK-06 -->
7. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(value, uses)` of `radii.tokens` SHALL be, in this order, `(4px, 1)` and `(8px, 1)`. <!-- TOK-07 -->
8. WHEN `extract_tokens` is called on `tokens-page.html` THEN the `(kind, value, uses)` of `shadows.tokens` SHALL be `(box, rgba(0, 0, 0, 0.2) 0px 1px 3px 0px, 1)` alone. <!-- TOK-08 -->
9. WHEN `extract_tokens` is called on `tokens-page.html` without `scope` or `viewport` THEN the structured content SHALL hold `viewport` equal to `{width: 1440, height: 900}`, `stabilized` equal to `true`, `scope` equal to `null`, `elements` equal to 8 (`html`, `body` and the six elements of the table), and in each Family a `total` equal to the length of its `tokens`. <!-- TOK-09 -->
10. WHEN `extract_tokens` is called on `tokens-page.html` THEN the first content block SHALL be a text block equal to `Tokens: colors 5, font families 1, font sizes 3, font weights 2, line heights 3, spacing 3, radii 2, shadows 1; elements 8; stabilized.` <!-- TOK-10 -->
11. The result of `extract_tokens` SHALL hold exactly one content block, and no image. <!-- TOK-11 -->
12. WHEN `extract_tokens` is called twice with the same arguments on `tokens-page.html` THEN both calls SHALL return equal structured content. <!-- TOK-12 -->
13. The `uses` of a Token that has `variants` SHALL equal the sum of the `uses` of its `variants`, and its `value` SHALL be the `value` of the first of them. <!-- TOK-13 -->
14. The `uses` of a Token of `colors` or of `spacing` SHALL equal the sum of its `roles`. <!-- TOK-14 -->

**Independent Test**: call the tool on `tokens-page.html` and compare the eight lists and the summary with the criteria.

---

### P1: Count a value only where it paints

**User Story**: As a coding agent, I want a colour or a size counted only on the elements that show it, so that an inherited value does not look like the most used one.

**Why P1**: Every element has a computed `color` and `font-size`; without the rule the counts say nothing.

**Acceptance Criteria** (all on `tokens-used.html`, each element with values no other element of the page has. Here and below, a list "holds" a value when it is the `value` of one of its Tokens, and "does not hold" it when it is the `value` of no Token and of no variant):

1. WHEN `#inherit` has `color: #aa0000` and no Own text, and holds `#inherit-child`, which has Own text and no `color` of its own THEN the Token `#aa0000` SHALL have `uses` 1 and `roles.text` 1. <!-- TOK-15 -->
2. WHEN `#fill` has Own text, `color: #111111` and `-webkit-text-fill-color: #222222` THEN `colors.tokens` SHALL hold `#222222` with `roles.text` 1 and SHALL NOT hold `#111111`. <!-- TOK-16 -->
3. WHEN `#clear` has `background-color: rgba(0, 128, 128, 0)` THEN `colors.tokens` SHALL hold no value that starts with `#008080`. <!-- TOK-17 -->
4. WHEN `#clip` has Own text, `color: #445566` and `-webkit-text-fill-color: transparent` THEN `colors.tokens` SHALL hold no value that starts with `#445566` and no value that ends with `00` and has eight digits. <!-- TOK-18 -->
5. WHEN `#veil` has `background-color: rgba(0, 0, 0, 0.5)` THEN `colors.tokens` SHALL hold `#00000080` with `roles.background` 1. <!-- TOK-19 -->
6. WHEN `#edge` has no Own text, `color: #00aa00` and `border-left: 2px solid #0000aa`, its three other sides without a border THEN `colors.tokens` SHALL hold `#0000aa` with `uses` 1 and `roles.border` 1, and SHALL NOT hold `#00aa00`. <!-- TOK-20 -->
7. WHEN `#sides` has a solid border of 1px whose colour is `#800000` on top, `#008000` on the right, `#000080` at the bottom and `#808000` on the left THEN each of the four SHALL be a Token with `roles.border` 1. <!-- TOK-21 -->
8. WHEN `#hidden` has `visibility: hidden` and `background-color: #aa00aa` THEN `colors.tokens` SHALL NOT hold `#aa00aa`. <!-- TOK-22 -->
9. WHEN `#faded` has `opacity: 0` and holds `#faded-child`, of `background-color: #00aaaa` and no `opacity` of its own THEN `colors.tokens` SHALL NOT hold `#00aaaa`. <!-- TOK-23 -->
10. WHEN `#none` has `display: none`, `#flat-w` has a width of 0 and a height of 20px, and `#flat-h` a width of 100px and a height of 0, their `background-color` being `#abcd01`, `#abcd02` and `#abcd03` THEN `colors.tokens` SHALL hold none of the three, and `elements` SHALL count none of the three elements. <!-- TOK-24 -->
11. WHEN `#big` has no Own text and `font: 900 40px/50px Georgia, serif`, and holds `#big-child`, which has Own text and `font: 400 12px/18px Arial, sans-serif` THEN no list of `typography` SHALL hold `40`, `900`, `50` or `Georgia, serif`, and `typography.sizes.tokens` SHALL hold `12`. <!-- TOK-25 -->
12. WHEN `#normal` has Own text, `font-size: 13px` and `line-height: normal`, and no other element has a font size of 13px THEN `typography.sizes.tokens` SHALL hold `13`, and the `uses` of `typography.lineHeights.tokens` SHALL add up to one less than those of `typography.sizes.tokens`. <!-- TOK-26 -->
13. WHEN `#ratio` has Own text, `font-size: 20px` and `line-height: 1.5` THEN `typography.lineHeights.tokens` SHALL hold `30`. <!-- TOK-27 -->
14. WHEN `#margins` has `margin: 51px 53px 55px 57px` THEN `spacing.tokens` SHALL hold `51`, `53`, `55` and `57`, each with `uses` 1 and `roles.margin` 1. <!-- TOK-28 -->
15. WHEN `#paddings` has `padding: 61px 63px 65px 67px` THEN `spacing.tokens` SHALL hold `61`, `63`, `65` and `67`, each with `uses` 1 and `roles.padding` 1. <!-- TOK-29 -->
16. WHEN `#centered` has `width: 200px` and `margin: 0 auto` in a `body` that is 1440px wide, so that each of its side margins is laid out at 620px THEN `spacing.tokens` SHALL NOT hold `620`. <!-- TOK-30 -->
17. WHEN `#pulled` has `margin-top: -71px` and every other margin and padding of it is 0 THEN `spacing.tokens` SHALL hold no `value` at or below 0 and SHALL NOT hold `71`. <!-- TOK-31 -->
18. WHEN `#flex` has `display: flex` and `gap: 81px 83px` THEN `spacing.tokens` SHALL hold `81` and `83`, each with `roles.gap` 1. <!-- TOK-32 -->
19. WHEN `#iflex` has `display: inline-flex` and `gap: 85px`, `#grid` has `display: grid` and `gap: 87px`, and `#igrid` has `display: inline-grid` and `gap: 89px` THEN `spacing.tokens` SHALL hold `85`, `87` and `89`, each with `uses` 1 and `roles.gap` 1. <!-- TOK-33 -->
20. WHEN `#block` has `display: block` and `gap: 91px` THEN `spacing.tokens` SHALL NOT hold `91`. <!-- TOK-34 -->
21. WHEN `#corners` has `border-radius: 41px 43px 45px 47px` THEN `radii.tokens` SHALL hold `41px`, `43px`, `45px` and `47px`, each with `uses` 1, and SHALL hold no `0px`. <!-- TOK-35 -->
22. WHEN `#round` has `border-radius: 50%` and `#oval` has `border-top-left-radius: 10px 20px` THEN `radii.tokens` SHALL hold `50%` and `10px 20px`, each with `uses` 1, after every Token whose `value` is a single px length. <!-- TOK-36 -->
23. WHEN `#glow` has no Own text and `text-shadow: 1px 1px 2px #000000`, and holds `#glow-child`, which has Own text and no `text-shadow` of its own THEN `shadows.tokens` SHALL hold `(text, rgb(0, 0, 0) 1px 1px 2px)` with `uses` 1. <!-- TOK-37 -->
24. WHEN `#layers` has `box-shadow: 0 1px 2px #000000, 0 4px 8px #000000` THEN `shadows.tokens` SHALL hold one Token of `kind` `box` for it, of `value` `rgb(0, 0, 0) 0px 1px 2px 0px, rgb(0, 0, 0) 0px 4px 8px 0px` and `uses` 1. <!-- TOK-38 -->
25. WHEN `#srgb` has `background-color: color(srgb 0.2 0.4 0.6)` THEN `colors.tokens` SHALL hold `#336699`. <!-- TOK-39 -->
26. WHEN `#wide` has `background-color: color(display-p3 1 0 0)`, a colour outside sRGB THEN `colors.tokens` SHALL hold `#ff0000`. <!-- TOK-40 -->

**Independent Test**: call the tool on `tokens-used.html` and look for each value named above.

---

### P1: Fold values that are nearly equal

**User Story**: As a coding agent, I want `#1a73e8` and `#1a78e8`, or 16px and 16.5px, returned as one token with both listed, so that I see one scale and the drift inside it.

**Why P1**: The roadmap asks for it, and phase 4 reads the variants.

**Acceptance Criteria** (all on `tokens-groups.html`):

1. WHEN the page holds, in document order, two elements of `background-color: #1a78e8`, one element with Own text of `color: #1a78e8`, four elements of `background-color: #1a73e8` and one of `background-color: #1a79e8`, where ΔE2000 is 1.8554 between `#1a73e8` and `#1a78e8`, 2.2280 between `#1a73e8` and `#1a79e8`, and 0.3724 between `#1a78e8` and `#1a79e8` THEN `colors.tokens` SHALL hold a Token of `value` `#1a73e8`, `uses` 7, `roles` `{text: 1, background: 6, border: 0}` and `variants`, in this order, `(#1a73e8, 4)` and `(#1a78e8, 3)`: the Representative is the most used Value, not the first of the document, and a Group is formed whatever the Roles. <!-- TOK-41 -->
2. WHEN `extract_tokens` is called on that page THEN `colors.tokens` SHALL hold a Token of `value` `#1a79e8`, `uses` 1 and the one variant `(#1a79e8, 1)`: it is not Near the Representative `#1a73e8`, and being Near the variant `#1a78e8` does not count. <!-- TOK-42 -->
3. WHEN the page holds one element of `background-color: rgba(26, 115, 232, 0.5)` THEN `colors.tokens` SHALL hold a Token of `value` `#1a73e880` and `uses` 1, apart from `#1a73e8`. <!-- TOK-43 -->
4. WHEN the page holds, in document order, two elements of `background-color: #858585` and two of `background-color: #808080`, whose ΔE2000 is 1.8620 THEN `colors.tokens` SHALL hold a Token of `value` `#808080`, `uses` 4 and `variants`, in this order, `(#808080, 2)` and `(#858585, 2)`. <!-- TOK-44 -->
5. WHEN the elements with Own text of the page have these font sizes, each on that many elements: 15px on 1, 16px on 3, 16.5px on 1, 16.75px on 1, 17px on 2 and 17.75px on 1 THEN the `(value, uses)` of `typography.sizes.tokens` SHALL be, in this order, `(15, 1)`, `(16, 4)` and `(17, 4)`: sizes exactly 1px apart are not Near. <!-- TOK-45 -->
6. WHEN `extract_tokens` is called on that page THEN the `variants` of the size Token `17` SHALL be, in this order, `(17, 2)`, `(16.75, 1)` and `(17.75, 1)`: 16.75px is Near 16px and 17px and joins the nearer one, though 16px has more Uses. <!-- TOK-46 -->
7. WHEN `extract_tokens` is called on that page THEN the `variants` of the size Token `16` SHALL be, in this order, `(16, 3)` and `(16.5, 1)`: 16.5px is as near 16px as 17px and joins the Group opened first. <!-- TOK-47 -->
8. WHEN two elements have `padding: 8px` and one has `padding: 8.5px` THEN `spacing.tokens` SHALL hold a Token of `value` `8`, `uses` 3, `roles.padding` 3 and `variants`, in this order, `(8, 2)` and `(8.5, 1)`. <!-- TOK-48 -->
9. WHEN two elements have `border-radius: 4px` and one has `border-radius: 4.5px` THEN `radii.tokens` SHALL hold a Token of `value` `4px`, `uses` 3 and `variants`, in this order, `(4px, 2)` and `(4.5px, 1)`. <!-- TOK-49 -->
10. WHEN every element with Own text of the page has `line-height: 20px` but one, which has `line-height: 20.5px` THEN `typography.lineHeights.tokens` SHALL hold one Token, of `value` `20`, whose `variants` end with `(20.5, 1)`. <!-- TOK-50 -->
11. WHEN one element has `border-radius: 30%` and another `border-radius: 30.5%`, and one has `border-top-left-radius: 10px 20px` and another `border-top-left-radius: 10.5px 20px` THEN `radii.tokens` SHALL hold `30%`, `30.5%`, `10px 20px` and `10.5px 20px` as four Tokens of `uses` 1. <!-- TOK-51 -->

**Independent Test**: call the tool on `tokens-groups.html` and read the `variants` of each Token named above.

---

### P1: Narrow the reading to a part of the page

**User Story**: As a coding agent, I want the tokens of one component, so that I can match a card without reading the whole page.

**Why P1**: `scope` is in the tool's signature in the roadmap.

**Acceptance Criteria** (all on `tokens-scope.html`, which holds, in document order: `#outside` of `#ff0000`; `#one`, of class `card` and `#00ff00`, holding `#one-child` of `#0000ff`; `#two`, of class `card` and `#00ff00`, holding `#inner`, of class `card` and `#ffff00`, and `#host`, with no background, whose open shadow tree holds `#deep` of `#00ffff`; and `#gone`, of `display: none`. No element has Own text, a margin, a padding, a radius or a shadow):

1. WHEN `extract_tokens` is called with `scope` equal to `.card` THEN the `(value, uses)` of `colors.tokens` SHALL be, in this order, `(#00ff00, 2)`, `(#0000ff, 1)`, `(#00ffff, 1)` and `(#ffff00, 1)`, and `scope` in the structured content SHALL be `.card`. <!-- TOK-52 -->
2. WHEN `extract_tokens` is called with `scope` equal to `.card` THEN `elements` SHALL be 6: `#inner`, which is a match and a descendant of a match, is read once. <!-- TOK-53 -->
3. WHEN `extract_tokens` is called without `scope` THEN `colors.tokens` SHALL hold `#ff0000` and `elements` SHALL be 9 (`html`, `body`, `#outside` and the six of the cards). <!-- TOK-54 -->
4. WHEN `extract_tokens` is called with `scope` equal to `#deep` THEN the `(value, uses)` of `colors.tokens` SHALL be `(#00ffff, 1)` alone and `elements` SHALL be 1: a selector reaches into open shadow trees. <!-- TOK-55 -->
5. WHEN `extract_tokens` is called with `scope` equal to `#one-child` THEN every Family but `colors` SHALL be `{total: 0, tokens: []}`. <!-- TOK-56 -->
6. IF `scope` is `.missing`, which matches no element THEN the call SHALL fail with the message `Scope ".missing" matched no elements.` <!-- TOK-57 -->
7. IF `scope` is `div[`, which is not a selector THEN the call SHALL fail with the message `Invalid selector "div[".` <!-- TOK-58 -->
8. WHEN `extract_tokens` is called with `scope` equal to `#gone` THEN the call SHALL succeed with `elements` equal to 0 and every Family equal to `{total: 0, tokens: []}`. <!-- TOK-59 -->
9. WHEN `extract_tokens` is called with `scope` equal to `#gone` THEN the text block SHALL be `Tokens: colors 0, font families 0, font sizes 0, font weights 0, line heights 0, spacing 0, radii 0, shadows 0; elements 0; stabilized.` <!-- TOK-60 -->
10. IF `scope` is an empty string THEN the call SHALL fail, and no Capture SHALL be taken of the whole page in its place. <!-- TOK-61 -->

**Independent Test**: call the tool on `tokens-scope.html` with each `scope` above.

---

### P2: Bound the response

**User Story**: As a coding agent, I want a long list cut to its most used tokens and told how long it was, so that a messy page does not flood my context.

**Why P2**: The tool is useful without it on a tidy page.

**Acceptance Criteria** (all on `tokens-limit.html`, where `#twenty` holds twenty elements whose `margin-top` is 10px, 20px and so on to 200px, one each, and after it come two elements of `margin-top: 210px`; and where twenty-one more elements have each a `background-color` of its own, no two of them Near):

1. WHEN `extract_tokens` is called without `scope` THEN `spacing.total` SHALL be 21 and the `value` of `spacing.tokens` SHALL be, in this order, 10, 20 and so on to 190, and then 210: the 20 first Tokens in Rank order, in Family order. <!-- TOK-62 -->
2. WHEN `extract_tokens` is called with `scope` equal to `#twenty` THEN `spacing.total` SHALL be 20 and `spacing.tokens` SHALL hold the twenty values from 10 to 200. <!-- TOK-63 -->
3. WHEN `extract_tokens` is called without `scope` THEN `colors.total` SHALL be 21 and `colors.tokens` SHALL hold the 20 colours that come first by text, in that order. <!-- TOK-64 -->
4. WHEN `extract_tokens` is called without `scope` THEN the text block SHALL say `colors 21` and `spacing 21`: the summary counts every Token found, not those returned. <!-- TOK-65 -->
5. The `tokens` of each of the eight Families SHALL hold at most 20 Tokens, each Family counted apart. <!-- TOK-66 -->

**Independent Test**: call the tool on `tokens-limit.html` with and without `scope: "#twenty"`.

---

### P2: Tool contract, config and documents

**User Story**: As a maintainer, I want the tool to follow the contract of the others and its thresholds to carry their sources.

**Why P2**: It keeps the server one thing; it changes no token.

**Acceptance Criteria**:

1. The server SHALL list `extract_tokens` with `readOnlyHint` true, `openWorldHint` true and an output schema, whose input takes `url` (required), `scope` (an optional string) and `viewport` (optional, `width` and `height` of at least 1). <!-- TOK-67 -->
2. WHEN `extract_tokens` is called on `tokens-viewport.html`, whose `#box` has `background-color: #999999` and, under `@media (max-width: 600px)`, `#111111`, with `viewport` equal to `{width: 375, height: 812}` THEN `colors.tokens` SHALL hold `#111111` and not `#999999`, and `viewport` in the structured content SHALL be `{width: 375, height: 812}`. <!-- TOK-68 -->
3. IF `url` is `ftp://example.com/` THEN the call SHALL fail with the message `Unsupported URL scheme "ftp"; use http://, https:// or file://.` <!-- TOK-69 -->
4. IF `url` names a file that does not exist THEN the call SHALL fail with a message that starts with `Could not load ` followed by that url. <!-- TOK-70 -->
5. IF a call takes longer than 30s THEN it SHALL fail with the message `Timed out after 30s.` <!-- TOK-71 -->
6. IF a call fails THEN its result SHALL be an error with no structured content. <!-- TOK-72 -->
7. WHEN the network of a page never goes idle THEN `stabilized` SHALL be `false` and the text block SHALL end with `; not stabilized.` <!-- TOK-73 -->
8. The function that computes ΔE2000 SHALL give, for each of the 34 pairs of the test data of Sharma, Wu and Dalal (2005), the published value to four decimal places. <!-- TOK-74 -->
9. `config.py` SHALL hold the ΔE2000 threshold (2), the Length threshold (1px) and the Limit (20), each as a named constant with a comment that gives its source as the Assumptions table does. <!-- TOK-75 -->
10. The README SHALL describe `extract_tokens` (its inputs, the eight Families, what counts as a Use, the two thresholds with their sources, and the Limit), and the CHANGELOG SHALL list it under `Unreleased`. <!-- TOK-76 -->
11. WHEN the test suite is run THEN every test of `ping`, `inspect_element` and `detect_visual_bugs` SHALL pass with no assertion changed but the two lists of tool names (`tests/test_ping.py`, `tests/test_inspect_element.py`), which gain `extract_tokens`. <!-- TOK-77 -->

**Independent Test**: list the tools through an in-memory client; run the suite.

---

## Edge Cases

- IF `#mixed` of `tokens-default.html` has `padding: 40px 40.5px`, two Near Values on one element THEN `spacing.tokens` SHALL hold a Token of `value` `40`, `uses` 2 and `variants`, in this order, `(40, 1)` and `(40.5, 1)`. <!-- TOK-78 -->
- WHEN `extract_tokens` is called on `tokens-default.html`, which does not reset the margin of `body` THEN `spacing.tokens` SHALL hold `8` with `uses` 1 and `roles.margin` 1: values of the browser's default stylesheet are counted. <!-- TOK-79 -->

Covered by the stories: a `scope` that matches nothing (TOK-57), that is not a selector (TOK-58), that matches only elements that are not Read (TOK-59), and a Family with no Value (TOK-56).

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| TOK-01 | P1: Read the tokens of a page | Phase 3, T9 | Implemented |
| TOK-02 | P1: Read the tokens of a page | Phase 3, T10 | Pending |
| TOK-03 | P1: Read the tokens of a page | Phase 3, T10 | Pending |
| TOK-04 | P1: Read the tokens of a page | Phase 3, T10 | Pending |
| TOK-05 | P1: Read the tokens of a page | Phase 3, T10 | Pending |
| TOK-06 | P1: Read the tokens of a page | Phase 3, T11 | Pending |
| TOK-07 | P1: Read the tokens of a page | Phase 3, T12 | Pending |
| TOK-08 | P1: Read the tokens of a page | Phase 3, T12 | Pending |
| TOK-09 | P1: Read the tokens of a page | Phase 3, T8 | Implemented |
| TOK-10 | P1: Read the tokens of a page | Phase 3, T13 | Pending |
| TOK-11 | P1: Read the tokens of a page | Phase 3, T8 | Implemented |
| TOK-12 | P1: Read the tokens of a page | Phase 3, T13 | Pending |
| TOK-13 | P1: Read the tokens of a page | Phase 3, T13 | Pending |
| TOK-14 | P1: Read the tokens of a page | Phase 3, T13 | Pending |
| TOK-15 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-16 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-17 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-18 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-19 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-20 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-21 | P1: Count a value only where it paints | Phase 4, T14 | Pending |
| TOK-22 | P1: Count a value only where it paints | Phase 4, T19 | Pending |
| TOK-23 | P1: Count a value only where it paints | Phase 4, T19 | Pending |
| TOK-24 | P1: Count a value only where it paints | Phase 4, T19 | Pending |
| TOK-25 | P1: Count a value only where it paints | Phase 4, T16 | Pending |
| TOK-26 | P1: Count a value only where it paints | Phase 4, T16 | Pending |
| TOK-27 | P1: Count a value only where it paints | Phase 4, T16 | Pending |
| TOK-28 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-29 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-30 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-31 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-32 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-33 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-34 | P1: Count a value only where it paints | Phase 4, T17 | Pending |
| TOK-35 | P1: Count a value only where it paints | Phase 4, T18 | Pending |
| TOK-36 | P1: Count a value only where it paints | Phase 4, T18 | Pending |
| TOK-37 | P1: Count a value only where it paints | Phase 4, T18 | Pending |
| TOK-38 | P1: Count a value only where it paints | Phase 4, T18 | Pending |
| TOK-39 | P1: Count a value only where it paints | Phase 4, T15 | Pending |
| TOK-40 | P1: Count a value only where it paints | Phase 4, T15 | Pending |
| TOK-41 | P1: Fold values that are nearly equal | Phase 5, T20 | Pending |
| TOK-42 | P1: Fold values that are nearly equal | Phase 5, T20 | Pending |
| TOK-43 | P1: Fold values that are nearly equal | Phase 5, T20 | Pending |
| TOK-44 | P1: Fold values that are nearly equal | Phase 5, T20 | Pending |
| TOK-45 | P1: Fold values that are nearly equal | Phase 5, T21 | Pending |
| TOK-46 | P1: Fold values that are nearly equal | Phase 5, T21 | Pending |
| TOK-47 | P1: Fold values that are nearly equal | Phase 5, T21 | Pending |
| TOK-48 | P1: Fold values that are nearly equal | Phase 5, T22 | Pending |
| TOK-49 | P1: Fold values that are nearly equal | Phase 5, T22 | Pending |
| TOK-50 | P1: Fold values that are nearly equal | Phase 5, T22 | Pending |
| TOK-51 | P1: Fold values that are nearly equal | Phase 5, T22 | Pending |
| TOK-52 | P1: Narrow the reading to a part of the page | Phase 6, T24 | Pending |
| TOK-53 | P1: Narrow the reading to a part of the page | Phase 6, T24 | Pending |
| TOK-54 | P1: Narrow the reading to a part of the page | Phase 6, T24 | Pending |
| TOK-55 | P1: Narrow the reading to a part of the page | Phase 6, T24 | Pending |
| TOK-56 | P1: Narrow the reading to a part of the page | Phase 6, T24 | Pending |
| TOK-57 | P1: Narrow the reading to a part of the page | Phase 6, T25 | Pending |
| TOK-58 | P1: Narrow the reading to a part of the page | Phase 6, T25 | Pending |
| TOK-59 | P1: Narrow the reading to a part of the page | Phase 6, T25 | Pending |
| TOK-60 | P1: Narrow the reading to a part of the page | Phase 6, T25 | Pending |
| TOK-61 | P1: Narrow the reading to a part of the page | Phase 6, T25 | Pending |
| TOK-62 | P2: Bound the response | Phase 6, T26 | Pending |
| TOK-63 | P2: Bound the response | Phase 6, T26 | Pending |
| TOK-64 | P2: Bound the response | Phase 6, T26 | Pending |
| TOK-65 | P2: Bound the response | Phase 6, T26 | Pending |
| TOK-66 | P2: Bound the response | Phase 6, T26 | Pending |
| TOK-67 | P2: Tool contract, config and documents | Phase 3, T8 | Implemented |
| TOK-68 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-69 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-70 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-71 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-72 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-73 | P2: Tool contract, config and documents | Phase 6, T27 | Pending |
| TOK-74 | P2: Tool contract, config and documents | Phase 1, T3 | Implemented |
| TOK-75 | P2: Tool contract, config and documents | Phase 1, T1 | Implemented |
| TOK-76 | P2: Tool contract, config and documents | Phase 6, T29 | Pending |
| TOK-77 | P2: Tool contract, config and documents | Phase 2, T7 | Implemented |
| TOK-78 | Edge Cases | Phase 5, T23 | Pending |
| TOK-79 | Edge Cases | Phase 5, T23 | Pending |

**Coverage:** 79 total, 79 mapped to tasks, 0 unmapped.

---

## Success Criteria

- [ ] Every criterion from TOK-01 to TOK-79 has a test that fails when its rule is dropped, all but TOK-74 through the MCP tool boundary.
- [ ] The Verifier's `validation.md` is a PASS.
- [ ] The tests of the other tools pass with no assertion changed.
