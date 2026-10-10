# Squint

Squint is an MCP server that examines a rendered web page by crossing what the browser reports (DOM/CSS) with what is actually painted (pixels), and reports the visual problems it finds without needing a baseline.

It is built for coding agents that have just produced UI and need to know whether the page actually looks right: which element is broken, and what the evidence is.

## Install

Requires [uv](https://docs.astral.sh/uv/). uv installs Python 3.12 for you if it is missing. Two steps:

```bash
uvx --from squint-mcp playwright install chromium   # the browser Squint drives
uvx squint-mcp                                       # the server
```

The first step goes through `squint-mcp` so the Chromium downloaded is the one its Playwright expects; uv warns that `playwright` comes from a dependency, which is expected. On Linux, add `--with-deps` to also install the system libraries Chromium needs.

The server speaks MCP over stdio, so started by hand it just waits for a client. Register it in your MCP client instead:

```json
{
  "mcpServers": {
    "squint": {
      "command": "uvx",
      "args": ["squint-mcp"]
    }
  }
}
```

In Claude Code: `claude mcp add squint -- uvx squint-mcp`.

Then call `ping` to confirm the connection.

## Tools

The server exposes three tools:

| Tool | Input | Output |
| --- | --- | --- |
| `ping` | `message` (optional string) | server `name`, `version`, and the echoed `message` |
| `inspect_element` | `url`, `selector`, `viewport` (optional) | one element's computed styles, box model, sampled colours, `stabilized`, and a crop |
| `detect_visual_bugs` | `url`, `viewports` (optional), `checks` (optional) | Findings ordered by severity, `stabilized` per viewport, and up to five crops |

`detect_visual_bugs` runs three Checks: `text-clipped` (text cut off by its own box), `low-contrast-real` (text whose contrast against the background sampled from the pixels is below WCAG 2.2 SC 1.4.3, so it is right over images and gradients) and `offscreen-overflow` (the element that makes the page scroll horizontally). See [`docs/SPEC.md`](https://github.com/sh4wty1/squint-mcp/blob/main/docs/SPEC.md) for the v0.1 specification and [`CHANGELOG.md`](https://github.com/sh4wty1/squint-mcp/blob/main/CHANGELOG.md) for what each release contains.

## Development

Run from a checkout:

```bash
git clone https://github.com/sh4wty1/squint-mcp.git
cd squint-mcp
uv sync
uv run playwright install chromium   # the tests drive a real Chromium
uv run squint-mcp
```

To point an MCP client at the checkout, use `"command": "uv"` with `"args": ["run", "--directory", "/path/to/squint-mcp", "squint-mcp"]`.

One command each:

```bash
uv run pyright              # typecheck (strict)
uv run ruff check           # lint
uv run ruff format --check  # format check
uv run pytest               # tests
```

Tests drive the server through an in-memory MCP client, the same surface a real client uses. See [`CONTRIBUTING.md`](https://github.com/sh4wty1/squint-mcp/blob/main/CONTRIBUTING.md).

## Documentation

- [`CONTEXT.md`](https://github.com/sh4wty1/squint-mcp/blob/main/CONTEXT.md): domain glossary (Capture, Check, Finding, Profile, Audit)
- [`docs/SPEC.md`](https://github.com/sh4wty1/squint-mcp/blob/main/docs/SPEC.md): v0.1 specification
- [`docs/adr/`](https://github.com/sh4wty1/squint-mcp/tree/main/docs/adr): architecture decision records

## License

[MIT](https://github.com/sh4wty1/squint-mcp/blob/main/LICENSE)
