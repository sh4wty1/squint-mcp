// Runs in the page once its layers are taken (AD-004), when the Capture is asked
// for covered text (AD-005). Returns the texts of the page: the elements of the list
// the collector kept that are visible and have an own text node with a box. For each
// one: its index in that list, those of its ancestors, nearest first, the region it
// paints with what is inside it and the indexes of its Silent layers. An element is
// spoken of by that index only, here and in every call below: it is its place in
// the elements of the Capture.
// Installs `globalThis.__squintCovered`, through which the Capture tells the glyphs
// of chosen texts from everything else (`mark`, `ink`), chooses what is painted
// (`show`) and asks which element is on top at a pixel (`hit`).
({ roles }) => {
  const elements = globalThis.__squintElements;
  const index = new Map(elements.map((element, i) => [element, i]));
  // Where the page is scrolled to while the Capture is taken.
  const startX = window.scrollX;
  const startY = window.scrollY;

  // The nearest ancestor of each element that is in the list, a shadow root
  // continuing at its host; -1 when it has none.
  const above = (element) => element.parentElement ?? element.getRootNode().host;
  const parents = elements.map((element) => {
    for (let node = above(element); node; node = above(node)) {
      if (index.has(node)) return index.get(node);
    }
    return -1;
  });
  const ancestorsOf = (i) => {
    const ancestors = [];
    for (let parent = parents[i]; parent >= 0; parent = parents[parent]) ancestors.push(parent);
    return ancestors;
  };
  const children = elements.map(() => []);
  parents.forEach((parent, i) => {
    if (parent >= 0) children[parent].push(i);
  });
  // An element and everything inside it.
  const subtreeOf = (i) => {
    const subtree = [i];
    for (const member of subtree) {
      for (const child of children[member]) subtree.push(child);
    }
    return subtree;
  };

  const facts = elements.map((element) => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return {
      // Only what the page shows is ever shown again: hidden text has no ink.
      visible: style.visibility === "visible",
      // A Silent layer root: an element that declares itself a layer or stays in
      // view while the page scrolls. A list of several roles is not one.
      silent:
        roles.includes((element.getAttribute("role") ?? "").trim().toLowerCase()) ||
        (element.localName === "dialog" && element.hasAttribute("open")) ||
        element.matches(":popover-open") ||
        style.position === "fixed" ||
        style.position === "sticky",
      // `z-index` applies to a positioned element; `auto` parses to no number.
      raised: style.position !== "static" && parseInt(style.zIndex, 10) > 0,
      left: rect.x + startX,
      top: rect.y + startY,
      right: rect.right + startX,
      bottom: rect.bottom + startY,
      // An element with no box, as under `display: none`, shows nothing.
      empty: rect.width === 0 && rect.height === 0,
      // Of a text: a Range over each own text node that paints a box, and its
      // Silent layers.
      ranges: [],
      layers: [],
    };
  });
  const silentRoots = facts.flatMap((fact, i) => (fact.silent ? [i] : []));

  const texts = [];
  facts.forEach((fact, i) => {
    if (!fact.visible) return;
    const region = { left: Infinity, top: Infinity, right: -Infinity, bottom: -Infinity };
    const grow = (left, top, right, bottom) => {
      region.left = Math.min(region.left, left);
      region.top = Math.min(region.top, top);
      region.right = Math.max(region.right, right);
      region.bottom = Math.max(region.bottom, bottom);
    };
    for (const node of elements[i].childNodes) {
      if (node.nodeType !== Node.TEXT_NODE) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      let painted = false;
      for (const rect of range.getClientRects()) {
        if (rect.width > 0 && rect.height > 0) {
          painted = true;
          // The own text is part of the region: an element of `display: contents`
          // has text and no box.
          grow(rect.x + startX, rect.y + startY, rect.right + startX, rect.bottom + startY);
        }
      }
      if (painted) fact.ranges.push(range);
    }
    if (!fact.ranges.length) return;
    for (const member of subtreeOf(i)) {
      const inside = facts[member];
      if (inside.visible && !inside.empty) {
        grow(inside.left, inside.top, inside.right, inside.bottom);
      }
    }
    const ancestors = ancestorsOf(i);
    // A Silent layer that holds the text is not one for it.
    fact.layers = silentRoots.filter((root) => root !== i && !ancestors.includes(root));
    texts.push({
      index: i,
      ancestors,
      region: {
        x: region.left,
        y: region.top,
        w: region.right - region.left,
        h: region.bottom - region.top,
      },
      layers: fact.layers,
    });
  });

  // A style does not cross a shadow boundary: one per root, as when filling. Two
  // in each: what is painted, and the colours of the highlights.
  const roots = [document];
  for (const root of roots) {
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
    }
  }
  const styleIn = (root) => {
    const style = document.createElement("style");
    (root.documentElement ?? root).append(style);
    return style;
  };
  const painting = roots.map(styleIn);
  const colors = roots.map(styleIn);

  // One highlight per channel of a screenshot. Red and blue at full strength and
  // green at a quarter of it: Chromium paints a bright green glyph fatter than a
  // black one over a dark backdrop, and a dim one as it paints black. The Capture
  // multiplies the green it reads by four.
  const INK = ["rgb(255, 0, 0)", "rgb(0, 64, 0)", "rgb(0, 0, 255)"];
  const highlightOf = (channel) => `squint-${channel}`;

  const SHOWN = "data-squint-show";
  const TEXT = "data-squint-text";
  // The elements that carry one of the two attributes.
  let revealed = [];
  const reveal = (members, attribute) => {
    for (const member of members) {
      if (!facts[member].visible) continue;
      elements[member].setAttribute(attribute, "");
      revealed.push(member);
    }
  };

  // The first element at a point of the viewport that the scroll has not moved from
  // where the Capture has it, so not a `fixed` or a stuck `sticky` one. A root
  // names the elements of its own tree: the search goes on inside a host.
  const moved = (element, i) => {
    const rect = element.getBoundingClientRect();
    return (
      Math.abs(rect.x + window.scrollX - facts[i].left) > 0.5 ||
      Math.abs(rect.y + window.scrollY - facts[i].top) > 0.5
    );
  };
  const topmost = (root, x, y) => {
    for (const element of root.elementsFromPoint(x, y)) {
      const i = index.get(element);
      if (i === undefined || moved(element, i)) continue;
      if (element.shadowRoot && element.getRootNode() === root) {
        return topmost(element.shadowRoot, x, y) ?? i;
      }
      return i;
    }
    return undefined;
  };

  globalThis.__squintCovered = {
    // Which glyphs are told apart: `channels` gives the channel of each text.
    mark(channels) {
      const highlights = INK.map(() => new Highlight());
      for (const [i, channel] of Object.entries(channels)) {
        // One at a time: a text can have more ranges than a call takes arguments.
        for (const range of facts[i].ranges) highlights[channel].add(range);
      }
      highlights.forEach((highlight, channel) => {
        CSS.highlights.set(highlightOf(channel), highlight);
      });
    },

    // The marked glyphs in the colour of their channel, or all of them in black:
    // the difference of the two screenshots is their ink. `color` in a highlight
    // repaints a glyph even over the fill the Capture forced (AD-004).
    ink(on) {
      const css = INK.map((color, channel) => {
        const painted = on ? color : "rgb(0, 0, 0)";
        return `::highlight(${highlightOf(channel)}) { color: ${painted} !important; }`;
      }).join(" ");
      for (const style of colors) style.textContent = css;
    },

    // What is painted. "page": everything, as the page asks. "glyphs": the glyphs
    // of the texts `indexes` and nothing else. "alone": the texts `indexes`, each
    // with what is inside it and, with `withLayers`, with its Silent layers.
    show(what, indexes = [], withLayers = false) {
      for (const member of revealed) {
        elements[member].removeAttribute(SHOWN);
        elements[member].removeAttribute(TEXT);
      }
      revealed = [];
      let css = "";
      if (what === "glyphs") {
        reveal(indexes, TEXT);
        css =
          "* { visibility: hidden !important; } " +
          `[${TEXT}] { visibility: visible !important; background: none !important;` +
          " border-color: transparent !important; outline-color: transparent !important;" +
          " box-shadow: none !important; } " +
          `[${TEXT}]::before, [${TEXT}]::after { visibility: hidden !important; }`;
      } else if (what === "alone") {
        const members = new Set();
        const add = (root) => {
          // An element is added with everything inside it.
          if (members.has(root)) return;
          for (const member of subtreeOf(root)) members.add(member);
        };
        for (const i of indexes) {
          add(i);
          if (withLayers) facts[i].layers.forEach(add);
        }
        reveal(members, SHOWN);
        css =
          "* { visibility: hidden !important; } " +
          `[${SHOWN}] { visibility: visible !important; }`;
      }
      for (const style of painting) style.textContent = css;
    },

    // Hit testing. `jobs` gives, for each text, the pixels to test as runs along
    // rows of the page, `[y, left, right]` with `right` not included; every
    // `step`th pixel of every `step`th row is tested. Returns, for each job, the
    // Other elements found, in document order: the index of each, at how many
    // pixels it was found and whether it is in a Raised layer.
    hit(jobs, step) {
      const width = window.innerWidth;
      const height = window.innerHeight;
      const points = [];
      jobs.forEach(({ runs }, job) => {
        const before = points.length;
        for (const [y, left, right] of runs) {
          if (y % step !== 0) continue;
          for (let x = Math.ceil(left / step) * step; x < right; x += step) {
            points.push([x, y, job]);
          }
        }
        // A text the step passes over whole is still tested once.
        if (points.length === before) {
          const [y, left, right] = runs[runs.length >> 1];
          points.push([(left + right) >> 1, y, job]);
        }
      });
      // `elementsFromPoint` answers inside the viewport only: the page is scrolled
      // a viewport at a time, each one reached once.
      const column = ([x]) => Math.floor(x / width);
      const row = ([, y]) => Math.floor(y / height);
      points.sort((a, b) => row(a) - row(b) || column(a) - column(b));

      const kin = jobs.map(({ index: text }) => new Set([text, ...ancestorsOf(text)]));
      const counts = jobs.map(() => new Map());
      for (const point of points) {
        const [x, y, job] = point;
        const inView =
          x >= window.scrollX &&
          x < window.scrollX + width &&
          y >= window.scrollY &&
          y < window.scrollY + height;
        if (!inView) {
          // Never a smooth scroll: the next line reads the position.
          window.scrollTo({
            left: column(point) * width,
            top: row(point) * height,
            behavior: "instant",
          });
        }
        const found = topmost(document, x - window.scrollX, y - window.scrollY);
        if (found === undefined) continue;
        // An Other element: not the text, an ancestor of it or a descendant of it.
        if (kin[job].has(found) || ancestorsOf(found).includes(jobs[job].index)) continue;
        counts[job].set(found, (counts[job].get(found) ?? 0) + 1);
      }
      window.scrollTo({ left: startX, top: startY, behavior: "instant" });

      return jobs.map((_, job) =>
        [...counts[job]]
          .sort(([one], [other]) => one - other)
          .map(([i, pixels]) => ({
            index: i,
            pixels,
            // It, or an ancestor of it that is not an ancestor of the text, is
            // positioned with a `z-index` above 0.
            raised: [i, ...ancestorsOf(i)].some(
              (layer) => !kin[job].has(layer) && facts[layer].raised,
            ),
          })),
      );
    },
  };
  return texts;
};
