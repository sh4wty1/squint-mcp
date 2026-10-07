# `boxModel.content` is the layout size; `box` is the transformed rect

`inspect_element` reports two sizes that diverge under a CSS `transform`. `box` is the transformed rect (`getBoundingClientRect()`, in page coordinates): the crop and the colour sampling need the element where it is painted. `boxModel.content` is the layout size: the border box before transforms minus border and padding, in the same untransformed space as the `margin`, `border` and `padding` beside it. We rejected reporting the painted content size, since it has no single answer under a rotation or a skew, and it is what subtracting untransformed edges from the transformed rect got wrong (issue #5).

## Consequences

- For an element with a transform, `box.w` is not `content.w` plus border and padding. A Check that compares the two has to account for the transform itself.
- The layout size is read from `offsetWidth`/`offsetHeight`, which are integers: a fractional layout width is rounded in `content` and not in `box`.
- SVG and MathML elements have no `offsetWidth`; their `content` still comes from the rect, transform included.
