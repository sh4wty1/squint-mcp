// Runs in the page after `load`. Waits for web fonts, then takes time out of the
// render so the same page yields the same pixels on every call.
async () => {
  await document.fonts.ready;

  // Animations and transitions that start from now on take no time.
  const style = document.createElement("style");
  style.textContent =
    "*, *::before, *::after {" +
    " animation-duration: 0s !important; animation-delay: 0s !important;" +
    " transition-duration: 0s !important; transition-delay: 0s !important; }";
  document.documentElement.append(style);

  // Those already running jump to their end. This also reaches open shadow trees,
  // which the style above does not. An infinite animation has no end, so it is cancelled.
  for (const animation of document.getAnimations()) {
    try {
      animation.finish();
    } catch {
      animation.cancel();
    }
  }
};
