// Spike. Installs window.__sq: what the Capture needs in the page to measure covered text.
(cfg) => {
  const els = [];
  const walk = (root) => {
    for (const el of root.querySelectorAll("*")) {
      els.push(el);
      if (el.shadowRoot) walk(el.shadowRoot);
    }
  };
  walk(document);
  const index = new Map(els.map((el, i) => [el, i]));
  const parentOf = (el) => el.parentElement ?? el.getRootNode().host ?? null;
  const roots = [document, ...els.filter((el) => el.shadowRoot).map((el) => el.shadowRoot)];
  const sx = window.scrollX, sy = window.scrollY;

  const info = els.map((el) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const role = (el.getAttribute("role") ?? "").trim().toLowerCase();
    const silent =
      cfg.roles.includes(role) ||
      (el.localName === "dialog" && el.hasAttribute("open")) ||
      (el.hasAttribute("popover") && el.matches(":popover-open")) ||
      cs.position === "fixed" || cs.position === "sticky";
    const z = parseInt(cs.zIndex, 10);
    return {
      el, visible: cs.visibility === "visible", silent,
      raised: cs.position !== "static" && z > 0,
      box: [r.x + sx, r.y + sy, r.x + sx + r.width, r.y + sy + r.height],
      top: r.y + sy, ranges: [], boxes: [],
    };
  });
  const parent = els.map((el) => { const p = parentOf(el); return p ? index.get(p) : -1; });
  const chain = (i) => { const out = []; for (let p = parent[i]; p >= 0; p = parent[p]) out.push(p); return out; };
  const related = (a, b) => a === b || chain(a).includes(b) || chain(b).includes(a);
  // Subtree lists, for showing an element with what is inside it.
  const kids = els.map(() => []);
  parent.forEach((p, i) => { if (p >= 0) kids[p].push(i); });
  const subtree = (i) => { const out = [i]; for (let k = 0; k < out.length; k++) out.push(...kids[out[k]]); return out; };

  const silentRoots = info.map((x, i) => (x.silent ? i : -1)).filter((i) => i >= 0);
  const texts = [];
  info.forEach((x, i) => {
    if (!x.visible) return;
    for (const node of x.el.childNodes) {
      if (node.nodeType !== Node.TEXT_NODE) continue;
      const r = document.createRange();
      r.selectNodeContents(node);
      let any = false;
      for (const t of r.getClientRects()) {
        if (t.width > 0 && t.height > 0) { x.boxes.push([t.x + sx, t.y + sy, t.right + sx, t.bottom + sy]); any = true; }
      }
      if (any) x.ranges.push(r);
    }
    if (!x.boxes.length) return;
    const anc = chain(i);
    // The Silent layers of this text: the roots that do not hold it.
    const layers = silentRoots.filter((s) => s !== i && !anc.includes(s));
    let region = [Infinity, Infinity, -Infinity, -Infinity];
    for (const d of subtree(i)) {
      if (!info[d].visible) continue;
      const b = info[d].box;
      region = [Math.min(region[0], b[0]), Math.min(region[1], b[1]), Math.max(region[2], b[2]), Math.max(region[3], b[3])];
    }
    texts.push({ idx: i, sel: x.el.id ? "#" + x.el.id : x.el.dataset.testid ?? x.el.localName + i,
                 boxes: x.boxes, region, anc, layers: layers.join(",") });
  });

  const addStyle = (root) => {
    const s = document.createElement("style");
    (root.documentElement ?? root).append(s);
    return s;
  };
  const styles = roots.map(addStyle);
  const hl = roots.map(addStyle);
  const SHOW = "data-sq-show", TEXT = "data-sq-text";
  const clear = () => { for (const x of info) { x.el.removeAttribute(SHOW); x.el.removeAttribute(TEXT); } };

  window.__sq = {
    // Which glyphs are told apart: {idx: channel}.
    mark(assign) {
      const sets = [[], [], []];
      for (const [i, c] of Object.entries(assign)) sets[c].push(...info[i].ranges);
      sets.forEach((ranges, c) => CSS.highlights.set("sq" + c, new Highlight(...ranges)));
    },
    ink(on) {
      const colors = on ? ["255,0,0", "0,64,0", "0,0,255"] : ["0,0,0", "0,0,0", "0,0,0"];
      const css = colors.map((c, i) => `::highlight(sq${i}){color:rgb(${c}) !important}`).join("");
      for (const s of hl) s.textContent = css;
    },
    // What is painted: "page", "glyphs" (the given texts, nothing else) or "alone"
    // (the given elements with what is inside them, plus their Silent layers).
    show(mode, list, withLayers) {
      clear();
      let css = "";
      if (mode === "glyphs") {
        for (const i of list) info[i].el.setAttribute(TEXT, "");
        css = `*{visibility:hidden !important}` +
          `[${TEXT}]{visibility:visible !important;background:none !important;border-color:transparent !important;box-shadow:none !important;outline-color:transparent !important}` +
          `[${TEXT}]::before,[${TEXT}]::after{visibility:hidden !important}`;
      } else if (mode === "alone") {
        const shown = new Set();
        for (const i of list) {
          for (const d of subtree(i)) shown.add(d);
          if (withLayers) {
            const anc = chain(i);
            for (const s of silentRoots) if (s !== i && !anc.includes(s)) for (const d of subtree(s)) shown.add(d);
          }
        }
        for (const d of shown) if (info[d].visible) info[d].el.setAttribute(SHOW, "");
        css = `*{visibility:hidden !important}[${SHOW}]{visibility:visible !important}`;
      }
      for (const s of styles) s.textContent = css;
    },
    // Hit testing at the pixels given as runs [y, x0, x1) per text, every `step`th
    // pixel of every `step`th row. Gives, per text, how many of them each Other
    // element got.
    hit(jobs, step) {
      const rows = [];
      for (const job of jobs) for (const [y, x0, x1] of job.runs) if (y % step === 0) rows.push([y, x0, x1, job.idx]);
      rows.sort((a, b) => a[0] - b[0]);
      const out = {};
      let tests = 0;
      const vh = window.innerHeight, vw = window.innerWidth;
      const deep = (x, y) => {
        // The first element at the point that the scroll has not moved from where
        // the Capture has it.
        let found = null;
        for (const el of document.elementsFromPoint(x, y)) {
          const i = index.get(el);
          if (i === undefined) continue;
          if (Math.abs(el.getBoundingClientRect().y + window.scrollY - info[i].top) > 0.5) continue;
          found = el; break;
        }
        while (found?.shadowRoot) {
          const inner = found.shadowRoot.elementFromPoint(x, y);
          if (!inner || inner === found || !index.has(inner)) break;
          found = inner;
        }
        return found;
      };
      for (const [y, x0, x1, t] of rows) {
        if (y < window.scrollY || y >= window.scrollY + vh) window.scrollTo(window.scrollX, Math.floor(y / vh) * vh);
        for (let x = x0 + ((step - (x0 % step)) % step); x < x1; x += step) {
          if (x < window.scrollX || x >= window.scrollX + vw) window.scrollTo(Math.floor(x / vw) * vw, window.scrollY);
          tests++;
          const el = deep(x - window.scrollX, y - window.scrollY);
          if (!el) continue;
          const i = index.get(el);
          if (related(i, t)) continue;
          (out[t] ??= {})[i] = (out[t][i] ?? 0) + 1;
        }
      }
      window.scrollTo(sx, sy);
      const named = {};
      for (const [t, counts] of Object.entries(out)) {
        const mine = chain(Number(t));
        named[t] = Object.entries(counts).map(([i, n]) => {
          const el = info[i].el;
          // Raised: it, or an ancestor of it that is not an ancestor of the text.
          const up = [Number(i), ...chain(Number(i))].filter((a) => !mine.includes(a));
          return { idx: Number(i), sel: el.id ? "#" + el.id : el.dataset.testid ?? el.localName + i, n,
                   raised: up.some((a) => info[a].raised) };
        });
      }
      return { covers: named, tests };
    },
  };
  return texts;
};
