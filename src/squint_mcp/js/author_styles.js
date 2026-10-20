// Runs in the page once it is stabilized. Whether the page has an Author style:
// a rule in a style sheet of the document or of an open shadow root, or a
// declaration in a `style` attribute. The styles Squint adds are not the page's.
() => {
  const roots = [document];
  for (const root of roots) {
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
      if (element.style?.length) return true;
    }
  }

  for (const root of roots) {
    for (const sheet of [...root.styleSheets, ...root.adoptedStyleSheets]) {
      if (sheet.disabled) continue;
      if (globalThis.__squintSheets?.has(sheet)) continue;
      try {
        if (sheet.cssRules.length > 0) return true;
      } catch {
        // A sheet of another origin loaded, and its rules are not the page's
        // to read: it is a style of the page all the same.
        return true;
      }
    }
  }
  return false;
};
