// Runs in the page once it is collected. Paints every glyph of the page in `color`,
// or not at all when it is `transparent`: the Capture takes the page without its text
// and the ink of its text from screenshots taken under different fills (AD-004).
// The fill colour, not `color`: borders, underlines and shadows follow `color` and
// have to stay as they are.
(color) => {
  // A sheet does not cross a shadow boundary: one per root, as when stabilizing,
  // kept from one fill to the next.
  const roots = [document];
  for (const root of roots) {
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
    }
  }

  globalThis.__squintFills ??= new WeakMap();
  for (const root of roots) {
    let sheet = globalThis.__squintFills.get(root);
    if (!sheet) {
      sheet = new CSSStyleSheet();
      globalThis.__squintFills.set(root, sheet);
      globalThis.__squintSheets.add(sheet);
      root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet];
    }
    sheet.replaceSync(
      `*, *::before, *::after { -webkit-text-fill-color: ${color} !important; }`,
    );
  }
};
