# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Squint stays on 0.x while the Finding schema is still changing: removing or renaming a Finding field, a tool or a tool parameter is a breaking change. Adding a Check or changing a threshold is not breaking, but is always recorded here.

## [Unreleased]

### Added

- MCP server over stdio, started with the `squint-mcp` command.
- `ping` tool: returns the server name and version and echoes an optional `message`.
- `inspect_element` tool: for one element of a page (`url`, `selector`, optional `viewport`), returns its computed styles, box model, the colours sampled from its pixels, whether the page stabilized, and a crop.
- `detect_visual_bugs` tool: for a page (`url`, optional `viewports`, optional `checks`), runs Checks on one Capture per viewport and returns Findings ordered by severity, whether each viewport stabilized, and up to five crops. Each Finding carries a selector that is unique on the page and works in `inspect_element`.
- `text-clipped` Check: reports text cut off horizontally by its own box (`overflow-x: hidden` or `clip`), confirmed in the pixels. A cut of 8px or more is `major`, a smaller one `minor`; a cut of 1px is not reported.
