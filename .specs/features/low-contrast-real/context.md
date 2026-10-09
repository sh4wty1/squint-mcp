# low-contrast-real Context

**Gathered:** 2026-10-07
**Spec:** `.specs/features/low-contrast-real/spec.md`
**Status:** Ready for design

---

## Feature Boundary

Slice 4 of `docs/ROADMAP.md`: the `low-contrast-real` Check (category `a11y`, WCAG 2.2 SC 1.4.3), its thresholds in `config`, its fixtures including text over an image and over a gradient, the CHANGELOG entry, and the Finding order across Checks (issue #8). Nothing from slice 5.

Standing rule from the maintainer: the roadmap and `docs/SPEC.md` are followed literally. Anything they assign to a later slice or leave out of v0.1 is out of scope without discussion.

---

## Implementation Decisions

### Background over many colours

- Worst part. The contrast is measured where it is lowest, after ignoring the worst 10% of the pixels behind the glyphs as noise.
- The 10% lives in config.

### Severity

- Two levels, both WCAG numbers: `critical` when the ratio is below 3:1, `major` otherwise.

### Text under `opacity` below 1

- No Finding when the effective opacity (the element's and its ancestors') is below 1. Known limit, listed in Out of Scope.
- A text colour with alpha is still judged, composited over the sampled background.

### Agent's Discretion

None. Every remaining choice is logged in the spec's Assumptions table with its default and rationale.

### Declined / Undiscussed Gray Areas → Assumptions

Logged in the spec's Assumptions & Open Questions: what a glyph pixel is, the fill colour as the text colour, colour syntaxes, large-text sizes, rounding, the reported background colour, evidence keys, message wording, the text-box limit, and the place of two Findings on one element (alphabetical by Check name).

---

## Specific References

- `docs/SPEC.md`, sections Finding, Images, Checks in v0.1, Testing Decisions.
- WCAG 2.2 SC 1.4.3 and technique G18.
- Issue #8.

---

## Deferred Ideas

- Text under `opacity` below 1; text under a scaling transform.
- Invisible text (same colour as its background): the future `invisible-content` Check.
- WCAG 1.4.6 and 1.4.11.
