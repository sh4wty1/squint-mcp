// Runs in the page over the elements matched by the selector and returns them in
// document order. For each one: its border box as painted, in page coordinates, its
// box model as laid out, the requested computed styles, an excerpt of its text, its
// scroll and client width and a selector that is unique on the page.
(elements, { properties, textLimit }) => {
  // Document order, an open shadow tree right after its host. Playwright lists the
  // matches inside shadow trees after the whole light tree, so its order is not used.
  // ponytail: the whole page is walked and every match is serialized, whatever the
  // Checks read; collect only the elements a Check can use if large pages get slow.
  const order = new Map();
  const walk = (root) => {
    for (const element of root.querySelectorAll("*")) {
      order.set(element, order.size);
      if (element.shadowRoot) walk(element.shadowRoot);
    }
  };
  walk(document);

  // Tag names joined by " > " from `body`, with `:nth-of-type` only where a sibling
  // shares the tag. Inside a shadow tree the path starts at the host's selector: the
  // child combinator reaches the children of a host's shadow root.
  const segment = (element) => {
    const tag = element.localName;
    const twins = [...element.parentNode.children].filter(
      (sibling) => sibling.localName === tag,
    );
    return twins.length > 1 ? `${tag}:nth-of-type(${twins.indexOf(element) + 1})` : tag;
  };
  const selectorOf = (element) => {
    const segments = [segment(element)];
    let node = element;
    while (node !== document.body && node.parentElement) {
      node = node.parentElement;
      segments.unshift(segment(node));
    }
    const root = node.getRootNode();
    if (root instanceof ShadowRoot) segments.unshift(selectorOf(root.host));
    return segments.join(" > ");
  };

  const excerpt = (text) => {
    const flat = text.replace(/\s+/g, " ").trim();
    return flat.length > textLimit ? `${flat.slice(0, textLimit - 1)}…` : flat;
  };

  const describe = (element) => {
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
      text: excerpt(element.textContent),
      ownText: [...element.childNodes].some(
        (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "",
      ),
      scrollWidth: element.scrollWidth,
      clientWidth: element.clientWidth,
      selector: selectorOf(element),
    };
  };

  return [...elements].sort((a, b) => order.get(a) - order.get(b)).map(describe);
};
