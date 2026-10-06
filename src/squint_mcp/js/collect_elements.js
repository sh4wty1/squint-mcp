// Runs in the page over the elements matched by the selector. For each one, returns
// its border box in page coordinates, its box model and the requested computed styles.
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
          w: Math.max(0, rect.width - border.left - border.right - padding.left - padding.right),
          h: Math.max(0, rect.height - border.top - border.bottom - padding.top - padding.bottom),
        },
      },
      computed: Object.fromEntries(
        properties.map((property) => [property, style.getPropertyValue(property)]),
      ),
    };
  });
