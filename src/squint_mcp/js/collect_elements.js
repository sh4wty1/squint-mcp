// Runs in the page over the elements matched by the selector and returns them in
// document order. For each one: its border box as painted, in page coordinates, its
// box model as laid out, the requested computed styles, an excerpt of its text, the
// right edge of its own text, its scroll and client width and a selector that is
// unique on the page.
(elements, { properties, textLimit, transformMinSizeDiffPx }) => {
  // Document order, an open shadow tree right after its host. Playwright lists the
  // matches inside shadow trees after the whole light tree, so its order is not used.
  // ponytail: the whole page is walked and every match is serialized, whatever the
  // Checks read; collect only the elements a Check can use if large pages get slow.
  const order = new Map();
  // How many elements of the page, shadow trees included, match each stable selector.
  const matches = new Map();

  // Attribute values are always quoted, which is valid for every string once the
  // quote, the backslash and the line breaks are escaped: a CSS string cannot hold a
  // raw line break.
  const quoted = (value) =>
    value
      .replace(/[\\"]/g, "\\$&")
      .replace(/[\n\r\f]/g, (lineBreak) => `\\${lineBreak.charCodeAt(0).toString(16)} `);
  const attribute = (element, name) => {
    const value = element.getAttribute(name);
    return value === null ? null : `[${name}="${quoted(value)}"]`;
  };
  // The selectors by attribute that `element` matches; null where it lacks the attribute.
  const stableSelectors = (element) => {
    const label = attribute(element, "aria-label");
    const role = attribute(element, "role");
    return {
      testId: attribute(element, "data-testid"),
      id: element.id ? `#${CSS.escape(element.id)}` : null,
      tagLabel: label && element.localName + label,
      roleLabel: label && role && role + label,
    };
  };
  // Frameworks generate ids like ":r1:", "ember1234" or "css-1a2b3c", which change
  // between builds. A real id wrongly skipped only falls through to the next step.
  const looksGenerated = (id) =>
    /[^A-Za-z0-9_-]/.test(id) || id.replace(/\D/g, "").length >= 3;

  const walk = (root) => {
    for (const element of root.querySelectorAll("*")) {
      order.set(element, order.size);
      for (const selector of Object.values(stableSelectors(element))) {
        if (selector) matches.set(selector, (matches.get(selector) || 0) + 1);
      }
      if (element.shadowRoot) walk(element.shadowRoot);
    }
  };
  walk(document);

  // The first of these that matches this element alone: its `data-testid`, its id
  // unless it looks generated, its `aria-label` with its explicit role or else its
  // tag. Failing them all, the CSS path: tag names joined by " > " from `body`, with
  // `:nth-of-type` only where a sibling shares the tag. Inside a shadow tree the path
  // starts at the host's selector: the child combinator reaches the children of a
  // host's shadow root.
  // Known limit: a host with a slotted child and a shadow-root child of the same tag
  // at the same position gives both the same path when neither has a stable selector.
  const segment = (element) => {
    // A tag name can hold a colon, as in `o:p`.
    const tag = CSS.escape(element.localName);
    const twins = [...element.parentNode.children].filter(
      (sibling) => sibling.localName === element.localName,
    );
    return twins.length > 1 ? `${tag}:nth-of-type(${twins.indexOf(element) + 1})` : tag;
  };
  const selectorOf = (element) => {
    const { testId, id, tagLabel, roleLabel } = stableSelectors(element);
    const stable = [testId, looksGenerated(element.id) ? null : id, roleLabel || tagLabel];
    const unique = stable.find((selector) => selector && matches.get(selector) === 1);
    if (unique) return unique;
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
    // ponytail: a transform that changes a size by under the tolerance is read as none;
    // read computed width if that matters.
    const layout = (offset, painted) =>
      offset === undefined || Math.abs(painted - offset) < transformMinSizeDiffPx
        ? painted
        : offset;
    const layoutWidth = layout(element.offsetWidth, rect.width);
    const layoutHeight = layout(element.offsetHeight, rect.height);
    // Where the element's own text ends, as painted: a Range over each text node that
    // is a direct child. scrollWidth cannot tell it from an overflowing child.
    // A running maximum: one text node can paint more rects than a call takes arguments.
    const range = document.createRange();
    let ownTextRight = null;
    for (const node of element.childNodes) {
      if (node.nodeType !== Node.TEXT_NODE) continue;
      range.selectNodeContents(node);
      for (const textRect of range.getClientRects()) {
        const right = textRect.right + window.scrollX;
        if (ownTextRight === null || right > ownTextRight) ownTextRight = right;
      }
    }
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
      ownTextRight,
      scrollWidth: element.scrollWidth,
      clientWidth: element.clientWidth,
      selector: selectorOf(element),
    };
  };

  return [...elements].sort((a, b) => order.get(a) - order.get(b)).map(describe);
};
