// Runs in the page once it is collected. Paints every glyph of the page in `color`,
// or not at all when it is `transparent`: the Capture takes the page without its text
// and the ink of its text from screenshots taken under different fills (AD-004).
// The fill colour, not `color`: borders, underlines and shadows follow `color` and
// have to stay as they are.
(color) => {
  // A style does not cross a shadow boundary: one per root, as when stabilizing.
  const roots = [document];
  for (const root of roots) {
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
    }
  }

  for (const root of roots) {
    let style = root.querySelector("style[data-squint-fill]");
    if (!style) {
      style = document.createElement("style");
      style.setAttribute("data-squint-fill", "");
      (root.documentElement ?? root).append(style);
    }
    style.textContent = `*, *::before, *::after { -webkit-text-fill-color: ${color} !important; }`;
  }
};
