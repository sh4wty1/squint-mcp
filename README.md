# Squint

Squint is an MCP server that examines a rendered web page by crossing what the browser reports (DOM/CSS) with what is actually painted (pixels), and reports the visual problems it finds without needing a baseline.

It is built for coding agents that have just produced UI and need to know whether the page actually looks right: which element is broken, and what the evidence is.

## Status

Pre-release. Squint is **not on PyPI yet**, so `uvx squint-mcp` does not work today. For now it runs from a checkout.

The server currently exposes one tool:

| Tool | Input | Output |
| --- | --- | --- |
| `ping` | `message` (optional string) | server `name`, `version`, and the echoed `message` |

`inspect_element` and `detect_visual_bugs` are next. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the delivery slices and [`docs/SPEC.md`](docs/SPEC.md) for what v0.1 will contain.

## Run from a checkout

Requires [uv](https://docs.astral.sh/uv/). uv installs Python 3.12 for you if it is missing.

```bash
git clone https://github.com/sh4wty1/squint-mcp.git
cd squint-mcp
uv sync
uv run playwright install chromium   # the browser inspect_element drives
uv run squint-mcp
```

The server speaks MCP over stdio, so started by hand it just waits for a client. To use it from an MCP client, register the command with the path to your checkout:

```json
{
  "mcpServers": {
    "squint": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/squint-mcp", "squint-mcp"]
    }
  }
}
```

Then call `ping` to confirm the connection.

## Development

One command each:

```bash
uv run pyright              # typecheck (strict)
uv run ruff check           # lint
uv run ruff format --check  # format check
uv run pytest               # tests
```

Tests drive the server through an in-memory MCP client, the same surface a real client uses. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Documentation

- [`CONTEXT.md`](CONTEXT.md): domain glossary (Capture, Check, Finding, Profile, Audit)
- [`docs/SPEC.md`](docs/SPEC.md): v0.1 specification
- [`docs/adr/`](docs/adr/): architecture decision records

## License

[MIT](LICENSE)
