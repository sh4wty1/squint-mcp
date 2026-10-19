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

The server exposes four tools:

| Tool | Input | Output |
| --- | --- | --- |
| `ping` | `message` (optional string) | server `name`, `version`, and the echoed `message` |
| `inspect_element` | `url`, `selector`, `viewport` (optional), `storageState` (optional) | one element's computed styles, box model, sampled colours, `stabilized`, and a crop |
| `detect_visual_bugs` | `url`, `viewports` (optional), `checks` (optional), `storageState` (optional) | Findings ordered by severity, `stabilized` per viewport, and up to five crops |
| `extract_tokens` | `url`, `scope` (optional), `viewport` (optional), `storageState` (optional) | the design tokens the page uses, in eight Families, each token with how many elements use it, and `stabilized` |

`detect_visual_bugs` runs five Checks: `text-clipped` (text cut off by its own box), `low-contrast-real` (text whose contrast against the background sampled from the pixels is below WCAG 2.2 SC 1.4.3, so it is right over images and gradients), `offscreen-overflow` (the element that makes the page scroll horizontally), `overlap` (text that another element is painted over, with how much of it is hidden and which element covers it) and `font-fallback` (a web font the page declares that did not load, with how many elements render their text in a fallback font). See [`docs/SPEC.md`](https://github.com/sh4wty1/squint-mcp/blob/main/docs/SPEC.md) for the v0.1 specification and [`CHANGELOG.md`](https://github.com/sh4wty1/squint-mcp/blob/main/CHANGELOG.md) for what each release contains.

`extract_tokens` reads the values a rendered page is styled with. `scope` is a CSS selector that reaches into open shadow roots: the reading is narrowed to its matches and every element under them. It returns eight Families: `colors` (by role: `text`, `background`, `border`), `typography.families`, `typography.sizes`, `typography.weights`, `typography.lineHeights`, `spacing` in px (by role: `margin`, `padding`, `gap`), `radii` and `shadows`. A token counts its uses: one use is one element that paints a box, is visible and is not under an opacity of 0, having that value in that role, and a value on several sides, corners or axes of one element is one use. Type values and text shadows count only on elements whose own text is painted, where the text is. Values nearly equal are one token, whose `value` is the most used and whose `variants` list each with its own count:

- colours of one alpha whose ΔE2000 is below 2, the just noticeable difference of [CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/) (section 20.2 for the formula, section 14.2.1 for the value; reading it as one token is Squint's);
- font sizes, line heights, spacings and px radii less than 1px apart, a Squint default with no norm behind it: a Capture has one image pixel per CSS pixel, and the whole steps of a scale stay apart.

Each Family returns at most 20 tokens, the most used, and its `total` counts every token it found.

## Pages behind a login

Every call opens its page with no cookies, so a page behind a login is examined as its login screen. To examine it logged in, log in once and save the session to a file in Playwright's storage state format:

```bash
uvx --from squint-mcp playwright codegen --save-storage=/home/me/admin-state.json https://example.com/admin
```

Log in in the window that opens, then close it: the file holds the cookies and `localStorage` of the session. Pass its absolute path as `storageState` to `inspect_element`, `detect_visual_bugs` or `extract_tokens`. Each call loads it into a fresh context and never writes it, so calls stay isolated from one another.

- The file holds the secrets of the session: anyone who has it is logged in. Keep it out of the repository; do not commit it.
- `sessionStorage` is not carried. A page that keeps its session there opens logged out.
- When the session expires, the calls examine the login screen again, with no error: save the file anew.
- The calls see the first screen after the login. A state reached only by clicking, such as a dialog or an editor with no URL of its own, is out of reach.

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
