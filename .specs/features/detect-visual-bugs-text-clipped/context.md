# detect_visual_bugs + text-clipped Context

**Gathered:** 2026-10-06
**Spec:** `.specs/features/detect-visual-bugs-text-clipped/spec.md`
**Status:** Ready for design

---

## Feature Boundary

Slice 3 of `docs/ROADMAP.md`: the Finding model, the Check contract, stable selector generation, the `detect_visual_bugs` tool and the `text-clipped` Check with its fixture pair. Nothing from slices 4 and 5.

Standing rule from the maintainer: the roadmap and `docs/SPEC.md` are followed literally. Anything they assign to a later slice or leave out of v0.1 is out of scope without discussion.

---

## Implementation Decisions

### Selector step "role + accessible name"

- CSS only. The step produces `tag[aria-label="…"]`, or `[role="…"][aria-label="…"]` when the element has an explicit `role` attribute.
- The name comes from `aria-label` alone. An element without `aria-label` skips this step and falls through to the CSS path.
- Every Finding selector works as the `selector` of `inspect_element`. Slice 2's contract does not change.

### Axis examined by `text-clipped`

- Horizontal only: `scrollWidth > clientWidth`, as written in `docs/SPEC.md`.

### Severity of `text-clipped`

- Two levels by size of the cut: `minor` below a pixel threshold held in config (8px), `major` at or above it.
- This makes severity ordering and crop allocation observable through the MCP boundary in this slice.

### Reach of `text-clipped`

- Only an element that both holds text directly and has the clipping overflow itself.
- Text clipped by an ancestor is a known limit, recorded in Out of Scope.

### Agent's Discretion

None. Every remaining choice is logged in the spec's Assumptions table with its default and rationale.

### Declined / Undiscussed Gray Areas → Assumptions

Logged in the spec's Assumptions & Open Questions: result shape (`findings`, `captures`), summary text, generated-id rule, CSS path format, text excerpt rule, pixel confirmation rule, minimum overflow, empty and duplicate list handling, fixture font, and (added 2026-10-07, after issue #5 and ADR-0003) elements under a `transform`.

---

## Specific References

- `docs/SPEC.md`, sections Finding, Images, Selector generation, Checks in v0.1.
- The Finding example in `docs/SPEC.md` fixes the message wording, the suggestion and the source of `text-clipped`.

---

## Deferred Ideas

- Vertical clipping (`scrollHeight > clientHeight`).
- Text clipped by an ancestor container.
- Role selectors in Playwright syntax (`role=button[name="…"]`) with a computed accessible name.
- Right-to-left text.
- Clipped text under a transform that scales, rotates or skews the element.
