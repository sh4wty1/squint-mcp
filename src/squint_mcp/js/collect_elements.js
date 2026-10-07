// Runs in the page over the elements matched by the selector. For each one, returns
// its border box as painted, in page coordinates, its box model as laid out and the
// requested computed styles.
(elements, properties) =>
  elements.map((element) => {
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    const edges = (prefix, suffix = "") =>
      Object.fromEntries(
        ["top", "right", "bottom", "left"].map((side) => [
          side,
          parseFloat(style.getPropertyValue(`${prefix}-${side}${suffix}`)) || 0,
        ]),
      );
    const border = edges("border", "-width");
    const padding = edges("padding");
    // The layout border box, before transforms: border and padding are untransformed
    // too (ADR-0003). offsetWidth is an integer, so the rect is kept while it agrees
    // with it: no transform is in play then, and a fractional size stays exact. SVG
    // and MathML elements have no offsetWidth and keep the rect.
    // ponytail: a transform that changes a size by under 1px is read as none; read
    // computed width if that matters.
    const layout = (offset, painted) =>
      offset === undefined || Math.abs(painted - offset) < 1 ? painted : offset;
    const layoutWidth = layout(element.offsetWidth, rect.width);
    const layoutHeight = layout(element.offsetHeight, rect.height);
    return {
      box: {
        x: rect.x + window.scrollX,
        y: rect.y + window.scrollY,
        w: rect.width,
        h: rect.height,
      },
      boxModel: {
        margin: edges("margin"),
        border,
        padding,
        content: {
          w: Math.max(0, layoutWidth - border.left - border.right - padding.left - padding.right),
          h: Math.max(0, layoutHeight - border.top - border.bottom - padding.top - padding.bottom),
        },
      },
      computed: Object.fromEntries(
        properties.map((property) => [property, style.getPropertyValue(property)]),
      ),
    };
  });
