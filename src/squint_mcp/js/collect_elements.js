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
    // too (ADR-0003). SVG and MathML elements have no offsetWidth and keep the rect.
    // ponytail: offsetWidth is an integer; read computed width if sub-pixel matters.
    const layoutWidth = element.offsetWidth ?? rect.width;
    const layoutHeight = element.offsetHeight ?? rect.height;
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
