# extract-tokens Context

**Gathered:** 2026-10-13
**Spec:** `.specs/features/extract-tokens/spec.md`
**Status:** Ready for design

---

## Feature Boundary

The tool `extract_tokens(url, scope?, viewport?)` returns the palette, the type scale, the spacings, the radii and the shadows that a rendered page uses, each as a counted list, with nearly equal colours and lengths folded into one token whose variants stay listed. It returns no Findings, no score and no image, and compares the page with nothing.

---

## Implementation Decisions

Asked one area at a time, in this order, on 2026-10-13. The maintainer took the recommended answer in each.

### Where a token is read

- The computed CSS only. The pixels are not read: they hold anti-aliasing blends, images and the middle of gradients, and a pixel cannot be given to a declared value with certainty.
- A value counts only where it paints: `color` only on an element with text of its own, `background-color` only with alpha above 0, a border colour only where the border has width, and nothing on an element with no rendered box.
- The Capture gains no third fact on request (unlike AD-005 and AD-008): the generic collector reads more properties. How is for Design.

### `scope`

- A CSS selector. Tokens are read from every element it matches and from all their descendants.
- Several matches are added up, each element once, even when a match is inside another match.
- No match fails with a `ToolError`: an empty result would read as "the page has no tokens" (AD-002).
- Without `scope`, the whole page. A region in coordinates is not accepted.

### The shape of the result

- Structured content plus a short text summary (`docs/SPEC.md`), and no image.
- Typography is four separate lists (families, sizes, weights, line heights), not composite text styles.
- Each list returns at most N tokens, the most used, and says how many it found in all.

### Colour difference

- ΔE2000, and two colours are one token below 2.
- Source: CSS Color Module Level 4 (W3C Candidate Recommendation Draft), read on 2026-10-13. Section 20.2 gives the formula and says its sample code was validated against the published test suite; the note of section 14.2.1 says "using deltaE2000, one JND is 2", and the pseudocode of section 14.2.2 compares with `E < JND`.
- The module gives that JND for gamut mapping. Reading it as "two colours a viewer cannot tell apart are one token" is this project's; a wider threshold would be a number of ours.
- Not chosen: ΔEOK with 0.02 (sections 20.3 and 14.2.1; section 20.4 says it under-estimates differences in colourfulness), and ΔE76 with 2.3 (Mahy et al., 1994, known to the agent only at second hand).

### Lengths

- Two px lengths are one token when they are less than 1px apart, for every px length of the result: font sizes, line heights, spacings and radii. A radius in percent groups only with an identical one.
- No norm was found for "nearly equal sizes": 1px is a Squint default. Its reason: a Capture has one image pixel per CSS pixel (`device_scale_factor=1` in `capture.py`), so it folds the fractional noise of `rem`, `em`, `calc` and percentages (13.3333px beside 13px) and keeps the whole steps of a scale (12, 13, 14) apart.

### Agent's Discretion

None was given explicitly. What the agent chose without asking is in the next section.

### Declined / Undiscussed Gray Areas → Assumptions

Each is a row of the Assumptions table of the spec. The agent chose them alone, and the maintainer confirmed all twelve as written on 2026-10-13, with the spec:

- The value of N is 20, not measured on real pages.
- A value joins the nearest Representative among those Near it, not the first one in Rank order as the agent had said in chat.
- A Use is one element, one value, one Role; four equal sides are one Use.
- The text colour is the computed `-webkit-text-fill-color`.
- A colour outside sRGB is clipped channel by channel.
- Radii and box shadows count on every Read element, painted or not.
- Values of the browser's default stylesheet count.
- Negative and zero spacing are not tokens.
- The tool takes an optional `viewport`, which the roadmap does not list.
- The computed text of shadows is quoted from memory.
- ΔE2000 has one test below the MCP seam.
- The ΔE values quoted in the criteria come from a scratch script.

---

## Specific References

- CSS Color Module Level 4, https://www.w3.org/TR/css-color-4/ : sections 14.2.1, 14.2.2, 20.2, 20.3 and 20.4.
- G. Sharma, W. Wu, E. N. Dalal, "The CIEDE2000 Color-Difference Formula: Implementation Notes, Supplementary Test Data, and Mathematical Observations", Color Research and Application, vol. 30, no. 1, pp. 21-30, February 2005. Test data: https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt (34 pairs in Lab, ΔE00 to four decimal places).
- `inspect_element` is the tool to follow for a result that holds no Findings (`src/squint_mcp/tools/inspect_element.py`).

## Notes for Design

Facts found while writing the spec; none is a decision.

- The collector reads `CAPTURE_COMPUTED_PROPERTIES` for every element. The spec needs, beyond them: the four border colours, the four corner radii, `box-shadow`, `text-shadow`, `row-gap` and `column-gap`. AD-003 has every element serialized on every call of every tool, and TOK-77 holds the other tools unchanged.
- `Element.box_model.margin` is the margin as laid out: an `auto` margin shows there as a px length (TOK-30). Telling `auto` needs the computed keyword, which `getComputedStyle` does not give for a margin.
- A Capture takes four screenshots whatever the tool (AD-004), and this tool reads no pixel.
- Chromium keeps a computed colour in its notation (`color(srgb ...)`, `oklch(...)`, `color(display-p3 ...)`): the value has to be taken to sRGB somewhere (TOK-39, TOK-40).
- `capture(...)` takes one selector and raises `Invalid selector "<selector>".` with the selector it was given: the message of TOK-58 has to quote `scope` as the caller wrote it.
- The scratch script that computed the ΔE values of the criteria matched 12 rows of the test data with a worst error of 0.00004. It used the sRGB to XYZ matrix, the Bradford D65 to D50 matrix and the D50 white of the sample code of CSS Color 4, typed from memory: Design takes them from the module.
- The computed texts of `box-shadow` and `text-shadow` in TOK-08, TOK-37 and TOK-38, and that a `padding` or a `font-size` with a fraction is reported as written (TOK-45 to TOK-48), were not checked on Chromium 153.

---

## Deferred Ideas

- Painted-area share of each colour, read from the pixels (the second option of the first area).
- Composite text styles (family, size, weight and line height together).
- The names of the CSS custom properties behind the values.
- Gradient stops and SVG `fill` and `stroke` in the palette.
