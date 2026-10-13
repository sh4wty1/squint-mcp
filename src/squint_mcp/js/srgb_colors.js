// Runs in the page over the texts of computed colours and returns, for each, the
// colour as the browser itself converts it to sRGB: `color(srgb r g b)`, or
// `color(srgb r g b / a)` when it is not opaque, with channels that can be outside
// 0 to 1. A text that is no colour gives null. Nothing of the page is read or
// changed: the canvas is not attached to the document (AD-009).
(texts) => {
  // A fill style that is refused leaves the one before it: this one, which no
  // conversion gives, since each is read back as `color(srgb ...)`.
  const sentinel = "#010203";
  const pen = new OffscreenCanvas(1, 1).getContext("2d");
  return texts.map((text) => {
    pen.fillStyle = sentinel;
    pen.fillStyle = `color(from ${text} srgb r g b / alpha)`;
    return pen.fillStyle === sentinel ? null : pen.fillStyle;
  });
};
