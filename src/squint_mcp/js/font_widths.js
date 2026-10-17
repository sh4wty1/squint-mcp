// Runs in the page, after the collector. Returns the Faces of `document.fonts` and,
// for each element whose own text asks first for a family with a Face that failed,
// how wide that text is set on one line: in its `font-family` and in that list
// without its first name (AD-008). The widths are read from copies of the text put
// outside the flow, all in one layout; no style of the page is changed. `shaping`
// names the properties a copy takes from its element besides the `font-` ones.
({ shaping }) => {
  // The names of a `font-family` as the computed value writes them: split at the
  // commas outside strings, a backslash taking the character after it.
  // Only CSS whitespace can separate a name from the commas around it.
  const trimCssWhitespace = (name) =>
    name.replace(/^[ \t\n\r\f]+|[ \t\n\r\f]+$/g, "");

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
        names.push(trimCssWhitespace(name));
        name = "";
      } else {
        name += char;
      }
    }
    names.push(trimCssWhitespace(name));
    return names;
  };

  // A name without the quotes and the escapes Chromium serializes it with.
  const bare = (name) =>
    name.replace(/^(["'])(.*)\1$/s, "$2").replace(
      /\\(?:([0-9a-f]{1,6})[ \t\n\r\f]?|(.))/gis,
      (_, hex, char) => (hex ? String.fromCodePoint(parseInt(hex, 16)) : char),
    );

  // Before any copy is made: a copy can ask for a font, and change a status.
  const faces = [...document.fonts].map((face) => ({
    family: face.family,
    status: face.status,
  }));
  // `document.fonts` gives the name of a Face of an `@font-face` rule as written,
  // and that of a Face a script adds serialized, quoted and escaped; the string
  // cannot tell which, so a Face answers to its name as given and decoded. A
  // family is matched whatever the case of its name and named as the first of its
  // Faces has it, a name as given before any decoded one.
  // ponytail: a failed Face of a rule whose name reads as a serialized one, such
  // as "Quoted" with its quotation marks, also catches the family of its decoded
  // name. Names are compared with toLowerCase, not Chromium's case folding: a
  // final sigma written differently in the Face name is not reported.
  const named = new Map();
  const failed = new Set();
  for (const read of [(name) => name, bare]) {
    for (const face of faces) {
      const name = read(face.family);
      const key = name.toLowerCase();
      if (!named.has(key)) named.set(key, name);
      if (face.status === "error") failed.add(key);
    }
  }

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
  // ponytail: a copy carries the `font-` properties of the element and those
  // of `shaping`, and nothing else of it. What a pseudo-element such as
  // `::first-letter` sets, and a property that differs along the text, are not
  // in it.
  const copyOf = (node, shaped, fontFamily) => {
    const copy = document.createElement("span");
    copy.textContent = node.nodeValue;
    important(copy, [
      ["all", "initial"],
      ["position", "absolute"],
      ["white-space", "nowrap"],
      ...shaped,
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
    const key = bare(names[0]).toLowerCase();
    if (!failed.has(key)) return;
    const family = named.get(key);
    // ponytail: the Tail can start with a family the page declares and no text had
    // used; its copy then asks for that font, one request the page had not made.
    const tail = names.slice(1).join(", ") || "initial";
    const shaped = [
      ...[...style].filter(
        (name) => name.startsWith("font-") && name !== "font-family",
      ),
      ...shaping,
    ].map((name) => [name, style.getPropertyValue(name)]);
    measured.push({
      index,
      family,
      own: nodes.map((node) => copyOf(node, shaped, style.fontFamily)),
      tail: nodes.map((node) => copyOf(node, shaped, tail)),
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
