# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Squint stays on 0.x while the Finding schema is still changing: removing or renaming a Finding field, a tool or a tool parameter is a breaking change. Adding a Check or changing a threshold is not breaking, but is always recorded here.

## [Unreleased]

### Added

- `offscreen-overflow` Check: on a page that scrolls horizontally, reports the element that sets the width of the page, one per viewport, with by how many pixels the page passes the viewport. Its severity is always `major`. It reports nothing while the page hides its horizontal overflow (`overflow-x: hidden` or `clip` on `html` or `body`), and nothing on a right-to-left page.
- `overlap` Check: reports text that another element is painted over, text painted over text included. The Finding sits on the covered text and carries the share of its ink that is hidden, read from the pixels (`hiddenPercent`), and the selector of the element that covers it (`coveredBy`), which works in `inspect_element`. A text is reported from 10% hidden; from 25% the Finding is `major`, below that `minor`. The severity is one level lower, `minor` or `info`, when the cover is in a raised layer: the cover, or an ancestor of it that does not also hold the text, is positioned with a `z-index` above 0. It is the first use of `info`. It does not report what is covered by a layer that declares itself (an element with a `role` of `menu`, `listbox`, `tooltip`, `dialog` or `alertdialog`, an open `dialog` element, an open popover, or anything inside one of them) or by a `fixed` or `sticky` element. Nor does it report a cover that paints nothing over the text (a link stretched over its card, an element of `opacity: 0`) or that lets at least half of the ink through, a cover that hit testing does not give (`pointer-events: none`), or text covered by one of its own descendants. A call that runs it takes about twice as long per viewport; a call whose `checks` leaves it out does not pay for it.

### Changed

- Text is rasterized in grayscale in every Capture: Chromium is launched with `--disable-lcd-text`. With subpixel text the same glyph is painted differently over different backdrops, so the ink of a text could not be compared between two renders of a page. Where Chromium used subpixel text, as on Windows, the edges of glyphs lose their colour fringe: crops, `sampledColors` and the contrast of a text can differ slightly from 0.1.0.
- The `low-contrast-real` Check stays fast on a page of many texts painted over millions of colours: it counts at most 262,144 pixels (512x512) across the texts of a page at one viewport, where the limit was per element. A text small enough is still counted whole; the larger ones share what is left equally, so on a page with more text than that their contrast comes from a sample, and a text of very little ink may not be judged on such a page ([#11](https://github.com/sh4wty1/squint-mcp/issues/11)).
- A sampled region no longer loses a colour of a 1px or 2px pattern, such as stripes or a checkerboard: `inspect_element` and `low-contrast-real` pick its pixels at varying offsets instead of at a regular step. The offsets are the same on every call, so the result of a call does not change from one run to the next; the `sampledColors` shares and the contrast of a sampled region differ slightly from 0.1.0 ([#11](https://github.com/sh4wty1/squint-mcp/issues/11)).

### Fixed

- The layout of a Capture on a page that uses the generic `monospace` font on Windows. The first screenshot that reached beyond the viewport made Chromium change that font and lay the page out again, so boxes were read from one layout and pixels from another, in every tool. A Capture now settles the layout before it measures anything ([#18](https://github.com/sh4wty1/squint-mcp/issues/18)).

## [0.1.0] - 2026-10-08

First release, on PyPI as `squint-mcp`.

### Added

- MCP server over stdio, started with the `squint-mcp` command.
- `ping` tool: returns the server name and version and echoes an optional `message`.
- `inspect_element` tool: for one element of a page (`url`, `selector`, optional `viewport`), returns its computed styles, box model, the colours sampled from its pixels, whether the page stabilized, and a crop.
- `detect_visual_bugs` tool: for a page (`url`, optional `viewports`, optional `checks`), runs Checks on one Capture per viewport and returns Findings ordered by severity, whether each viewport stabilized, and up to five crops. Each Finding carries a selector that is unique on the page and works in `inspect_element`.
- `text-clipped` Check: reports text cut off horizontally by its own box (`overflow-x: hidden` or `clip`), confirmed in the pixels. A cut of 8px or more is `major`, a smaller one `minor`; a cut of 1px is not reported.
- `low-contrast-real` Check (WCAG 2.2 SC 1.4.3): reports text whose contrast is below 4.5:1, or 3:1 for large text (24px, or 18.66px bold), against the background painted behind it. The background is sampled from the pixels, so it is right over an image or a gradient; where it varies, the worst tenth of the text decides. A ratio under 3:1 is `major`, any other `minor`. Text with an `opacity` below 1, on itself or on an ancestor, is not judged.
- `evidence.measured` of a Finding can hold strings besides numbers: `low-contrast-real` reports `textColor` and `sampledBackground` as `#rrggbb`.
- Findings of the same severity and viewport come in document order whatever the Check that reported them, and two Findings on one element in the order of their Check names. The order of `checks` does not change the result.
- `inspect_element` and the `low-contrast-real` Check stay fast on a large element painted in millions of colours, such as a long photo-heavy page: an element, or the text of an element, of more than 262,144 pixels (512x512) is sampled down to that many before its colours are counted, so `sampledColors` and the contrast of such an element come from the sample. Smaller ones are counted whole, as before ([#4](https://github.com/sh4wty1/squint-mcp/issues/4)).
