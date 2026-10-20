// Runs in the page after `load`. Waits for web fonts, then takes time out of the
// render so the same page yields the same pixels on every call.
async () => {
  await document.fonts.ready;

  // Neither a style nor getAnimations() crosses a shadow boundary: treat the
  // document and every open shadow root under it, however deeply nested.
  const roots = [document];
  for (const root of roots) {
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
    }
  }

  // Every rule Squint adds to a page is in a constructable sheet: a `style-src`
  // policy refuses a `<style>` the page did not ship, never an adopted sheet
  // (issue #26). The set tells them from the page's own sheets (AD-011).
  globalThis.__squintSheets ??= new WeakSet();
  for (const root of roots) {
    // Animations and transitions that start from now on take no time.
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(
      "*, *::before, *::after {" +
        " animation-duration: 0s !important; animation-delay: 0s !important;" +
        " transition-duration: 0s !important; transition-delay: 0s !important; }",
    );
    globalThis.__squintSheets.add(sheet);
    root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet];

    // Those already running jump to their end. An infinite animation has no end,
    // so it is cancelled.
    for (const animation of root.getAnimations()) {
      try {
        animation.finish();
      } catch {
        animation.cancel();
      }
    }
  }
};
