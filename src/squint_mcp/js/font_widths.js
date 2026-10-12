// Runs in the page, after the collector. Returns the Faces of `document.fonts` and,
// for each element whose own text asks first for a family with a Face that failed,
// how wide that text is set on one line: in its `font-family` and in that list
// without its first name (AD-008). The widths are read from copies of the text put
// outside the flow, all in one layout; no style of the page is changed.
() => {
  // The names of a `font-family` as the computed value writes them: split at the
  // commas outside strings, a backslash taking the character after it.
  const namesOf = (fontFamily) => {
    const names = [];
    let name = "";
    let quote = null;
    for (let at = 0; at < fontFamily.length; at++) {
      const char = fontFamily[at];
      if (char === "\\") {
        name += char + (fontFamily[at + 1] ?? "");
        at++;
      } else if (quote !== null) {
        if (char === quote) quote = null;
        name += char;
      } else if (char === '"' || char === "'") {
        quote = char;
        name += char;
      } else if (char === ",") {
        names.push(name.trim());
        name = "";
      } else {
        name += char;
      }
    }
    names.push(name.trim());
    return names;
  };

  // A name without the quotes and the escapes Chromium serializes it with.
  // ponytail: a hexadecimal escape, which Chromium writes for a name that starts
  // with a digit (`\31 st`), is not decoded; such a family matches no Face and is
  // never reported.
  const bare = (name) =>
    name.replace(/^(["'])(.*)\1$/s, "$2").replace(/\\(.)/gs, "$1");

  // Before any copy is made: a copy can ask for a font, and change a status.
  const faces = [...document.fonts].map((face) => ({
    family: bare(face.family),
    status: face.status,
  }));
  const failed = new Set(
    faces.filter((face) => face.status === "error").map((face) => face.family),
  );

  const important = (element, declarations) => {
    for (const [name, value] of declarations) {
      element.style.setProperty(name, value, "important");
    }
  };

  const host = document.createElement("div");
  important(host, [
    ["all", "initial"],
    ["position", "absolute"],
    ["left", "0"],
    ["top", "0"],
    ["width", "0"],
    ["height", "0"],
    ["overflow", "hidden"],
    ["visibility", "hidden"],
  ]);

  // A copy of one text node, on one line, in the list of families given.
  // ponytail: a copy carries the `font-` properties of the element and nothing
  // else of it. What a pseudo-element such as `::first-letter` sets, and a font
  // property that differs along the text, are not in it.
  const copyOf = (node, shaping, fontFamily) => {
    const copy = document.createElement("span");
    copy.textContent = node.nodeValue;
    important(copy, [
      ["all", "initial"],
      ["position", "absolute"],
      ["white-space", "nowrap"],
      ...shaping,
      ["font-family", fontFamily],
    ]);
    host.append(copy);
    return copy;
  };

  const measured = [];
  globalThis.__squintElements.forEach((element, index) => {
    const nodes = [...element.childNodes].filter(
      (node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "",
    );
    if (nodes.length === 0) return;
    const style = getComputedStyle(element);
    const names = namesOf(style.fontFamily);
    const family = bare(names[0]);
    if (!failed.has(family)) return;
    // ponytail: the Tail can start with a family the page declares and no text had
    // used; its copy then asks for that font, one request the page had not made.
    const tail = names.slice(1).join(", ") || "initial";
    const shaping = [...style]
      .filter((name) => name.startsWith("font-") && name !== "font-family")
      .map((name) => [name, style.getPropertyValue(name)]);
    measured.push({
      index,
      family,
      own: nodes.map((node) => copyOf(node, shaping, style.fontFamily)),
      tail: nodes.map((node) => copyOf(node, shaping, tail)),
    });
  });

  const widths = {};
  if (measured.length > 0) {
    // One layout for every copy: all are in the host before the first width is read.
    document.documentElement.append(host);
    const widthOf = (copies) =>
      copies.reduce((sum, copy) => sum + copy.getBoundingClientRect().width, 0);
    for (const { index, family, own, tail } of measured) {
      widths[index] = { family, own: widthOf(own), tail: widthOf(tail) };
    }
    host.remove();
  }
  return { faces, widths };
};
