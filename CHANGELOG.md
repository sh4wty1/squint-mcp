# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Squint stays on 0.x while the Finding schema is still changing: removing or renaming a Finding field, a tool or a tool parameter is a breaking change. Adding a Check or changing a threshold is not breaking, but is always recorded here.

## [Unreleased]

### Added

- `offscreen-overflow` Check: on a page that scrolls horizontally, reports the element that sets the width of the page, one per viewport, with by how many pixels the page passes the viewport. Its severity is always `major`. It reports nothing while the page hides its horizontal overflow (`overflow-x: hidden` or `clip` on `html` or `body`), and nothing on a right-to-left page.

### Changed

- The `low-contrast-real` Check stays fast on a page of many texts painted over millions of colours: it counts at most 262,144 pixels (512x512) across the texts of a page at one viewport, where the limit was per element. A text small enough is still counted whole; the larger ones share what is left equally, so on a page with more text than that their contrast comes from a sample, and a text of very little ink may not be judged on such a page ([#11](https://github.com/sh4wty1/squint-mcp/issues/11)).
- A sampled region no longer loses a colour of a 1px or 2px pattern, such as stripes or a checkerboard: `inspect_element` and `low-contrast-real` pick its pixels at varying offsets instead of at a regular step. The offsets are the same on every call, so the result of a call does not change from one run to the next; the `sampledColors` shares and the contrast of a sampled region differ slightly from 0.1.0 ([#11](https://github.com/sh4wty1/squint-mcp/issues/11)).

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
