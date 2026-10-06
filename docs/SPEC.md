# Spec: Squint v0.1 — ping, inspect_element, detect_visual_bugs with 2 Checks

Origem: issue #1. Este arquivo é a fonte de verdade a partir de agora.

Related documents:

- [`CONTEXT.md`](../CONTEXT.md): domain glossary (Capture, Check, Finding, Profile, Audit)
- [`docs/adr/0001-python-over-typescript.md`](adr/0001-python-over-typescript.md)
- [`docs/adr/0002-checks-consume-captures-only.md`](adr/0002-checks-consume-captures-only.md)
- [`docs/ROADMAP.md`](ROADMAP.md): v0.1 delivery slices
- [`.docs/START.md`](../.docs/START.md): initial specification and grill decisions (section 14)

## Problem Statement

A coding agent (or the front-end developer driving it) that has just produced UI cannot tell whether the page actually *looks* right. The DOM can be "correct" while the render is broken: text is cut off by its container, or text sits on an image or gradient where its real contrast is far below what the CSS `background-color` suggests.

The tools available today do not close that gap:

- Visual regression tools (Percy, Chromatic, Playwright's `toHaveScreenshot`) need a baseline and do not explain what broke.
- `@playwright/mcp` navigates and takes screenshots, but does not measure or diagnose. The agent is left to guess from a full-page image, at high token cost.

There is no way to ask, on the first visit to a page and with no baseline, "what is visually wrong here, on which element, and what is the evidence?"

## Solution

Squint v0.1 is an MCP server, installed with `uvx squint-mcp`, that an MCP client runs over stdio. It examines a rendered page by crossing what the browser reports (DOM/CSS) with what is actually painted (pixels), and reports problems without a baseline.

v0.1 ships three tools:

- `ping`: confirms the server is alive and reports its name and version.
- `inspect_element`: for one element on a page, returns its computed styles, box model, a crop of how it is painted, and the colour actually sampled from its pixels.
- `detect_visual_bugs`: runs Checks against a Capture of the page and returns Findings, each pointing at one element with a stable selector, its box, the relevant computed styles, the measured values, and a small crop.

v0.1 ships two Checks, chosen because they show the pixel-plus-DOM differentiator that a DOM-only tool cannot reproduce:

- `low-contrast-real`: text contrast computed against the background colour **sampled from the pixels**, so it is correct over images and gradients.
- `text-clipped`: text cut off by its container, signalled by the DOM and confirmed in the pixels.

Every call is stateless: open the URL, stabilize, capture, close. Squint sees only the page's initial state and complements `@playwright/mcp` rather than replacing it.

## User Stories

### Installing and connecting

1. As a front-end developer, I want to install Squint with `uvx squint-mcp`, so that I can add it to my MCP client without cloning a repository.
2. As a front-end developer, I want the README to tell me that Chromium is a second install step (`playwright install chromium`), so that my first call does not fail mysteriously.
3. As a front-end developer, I want a clear error naming the missing-browser fix when Chromium is not installed, so that I can recover without reading source code.
4. As an MCP client, I want Squint to speak MCP over stdio, so that I can launch it as a local subprocess.
5. As an MCP client, I want Squint to write logs only to stderr, so that the stdio protocol stream is never corrupted.
6. As a coding agent, I want a `ping` tool that returns the server name and version and echoes an optional message, so that I can verify the connection before spending a browser launch.
7. As a coding agent, I want every tool to carry MCP annotations (`readOnlyHint`, `openWorldHint`), so that my client can decide what needs approval.
8. As a coding agent, I want every tool input validated against a typed schema with a clear error on invalid input, so that I can correct my call without guessing.

### Pointing Squint at a page

9. As a front-end developer, I want to pass an `http://` or `https://` URL, so that I can examine a deployed page.
10. As a front-end developer, I want to pass a `localhost` URL, so that I can examine my dev server before opening a PR.
11. As a front-end developer, I want to pass a `file://` URL, so that I can examine a static HTML file without running a server.
12. As a coding agent, I want a clear error when I pass an unsupported scheme, so that I know what Squint accepts.
13. As a coding agent, I want to choose the viewport per call, so that I can examine the page at the size I care about.
14. As a coding agent, I want a sensible default viewport when I pass none, so that the simplest call works.
15. As a coding agent, I want each call to be isolated from every other call (no shared cookies, storage or page state), so that results are reproducible.
16. As a coding agent, I want repeated calls to reuse the already-running browser, so that I am not paying a browser launch on every call.

### Stable, reproducible captures

17. As a coding agent, I want Squint to wait for the page to load and for web fonts to be ready before capturing, so that I do not get Findings caused by a half-rendered page.
18. As a coding agent, I want animations and transitions zeroed before capture, so that the same page yields the same pixels each time.
19. As a coding agent, I want Squint to wait briefly for the network to go idle but not fail when it never does, so that pages with polling or analytics can still be examined.
20. As a coding agent, I want the response to tell me when the page did not fully stabilize, so that I can weigh the Findings accordingly.
21. As a coding agent, I want every tool call bounded by a total timeout with a clear error, so that a hanging page never hangs my session.
22. As a coding agent, I want a clear error when the page cannot be loaded at all, so that I can tell "page is broken" apart from "page has no Findings".

### Inspecting an element

23. As a coding agent, I want `inspect_element` to return an element's computed styles, so that I can see what the browser resolved rather than what the stylesheet says.
24. As a coding agent, I want `inspect_element` to return the element's box model in CSS pixels, so that I can reason about its size and position.
25. As a coding agent, I want `inspect_element` to return a crop of the element as painted, so that I can look at it without a full-page screenshot.
26. As a coding agent, I want `inspect_element` to return the colours actually sampled from the element's pixels, so that I know what a user sees when the background is an image or gradient.
27. As a coding agent, I want a clear error when my selector matches nothing, so that I can fix the selector.
28. As a coding agent, I want a clear error when my selector matches more than one element, so that I never get data about the wrong element.
29. As a coding agent, I want `inspect_element` to find elements inside open shadow roots, so that pages built with web components are not opaque to me.

### Detecting visual problems

30. As a coding agent, I want `detect_visual_bugs` to run all available Checks by default, so that the simplest call gives me the full picture.
31. As a coding agent, I want to restrict a call to named Checks, so that I can re-verify one fix cheaply.
32. As a coding agent, I want to pass several viewports in one call, so that I can examine desktop and mobile together.
33. As a coding agent, I want a clear error when I name a Check that does not exist, listing the valid names, so that I can correct the call.
34. As a coding agent, I want an empty Finding list (not an error) when nothing is wrong, so that I can treat "no Findings" as a pass.
35. As a front-end developer, I want Squint to report text whose real contrast against the painted background is below the WCAG threshold, so that I catch unreadable text over images and gradients that DOM-only tools miss.
36. As a front-end developer, I want Squint not to report text that has adequate real contrast, so that I can trust a Finding when I see one.
37. As a front-end developer, I want Squint to report text that is cut off by its container, so that I catch truncated headings and labels before users do.
38. As a front-end developer, I want Squint not to report text that fits its container, so that I am not chasing false positives.
39. As a front-end developer, I want Checks to look inside open shadow roots, so that problems in web components are reported too.

### Reading a Finding

40. As a coding agent, I want each Finding to name the Check that produced it, so that I know what kind of problem it is.
41. As a coding agent, I want each Finding to carry a category and a severity, so that I can prioritise.
42. As a coding agent, I want each Finding to carry a human-readable message in English with the measured numbers, so that I can relay it to the developer as is.
43. As a coding agent, I want each Finding to carry a stable selector that is unique on the page, so that I can locate the element in the source and re-inspect it.
44. As a coding agent, I want the selector to prefer `data-testid`, then a non-generated `id`, then role and accessible name, then a CSS path, so that it survives unrelated markup changes.
45. As a coding agent, I want each Finding to carry a short excerpt of the element's visible text, so that I can find the element in source even when the selector is a CSS path.
46. As a coding agent, I want each Finding to carry the element's box and the viewport it was captured at, so that I know where and at what size the problem occurs.
47. As a coding agent, I want each Finding to carry the relevant computed styles and the measured values as evidence, so that I can verify the claim rather than take it on faith.
48. As a coding agent, I want each Finding to cite its source (for example the WCAG success criterion), so that I can justify the fix.
49. As a coding agent, I want each Finding to carry a suggestion where one is obvious, so that I have a starting point for the fix.
50. As a coding agent, I want one Finding per element, per viewport, per Check, so that I can count and deduplicate predictably.

### Token cost

51. As a coding agent, I want results as structured content plus a short text summary, so that I can parse them without scraping prose.
52. As a coding agent, I want crops returned inline in the MCP response, so that I can see evidence without filesystem access.
53. As a coding agent, I want at most five crops per call, chosen by severity, so that one call never floods my context.
54. As a coding agent, I want crops downscaled to roughly 512px on the longest side, so that each image is cheap.
55. As a coding agent, I want each Finding to say which image in the response is its crop, or that it has none, so that I can pair evidence with Findings.
56. As a coding agent, I want Findings beyond the crop limit still returned in full as data, so that the limit costs me images and never Findings.

### Maintaining and contributing

57. As the maintainer, I want strict typing, lint, format and tests to run locally and in CI with one command each, so that an AI agent implementing a ticket gets fast feedback and corrects itself.
58. As the maintainer, I want every threshold in one config module with its source cited, so that I can review and tune them in one place.
59. As the maintainer, I want each Check in its own file with a paired "bug planted" and "no bug" fixture, so that each Check can be reviewed as one small diff.
60. As a contributor, I want README, LICENSE (MIT), CONTRIBUTING, CHANGELOG, SECURITY and GitHub issue/PR templates in place, so that I know how to use, report on and contribute to the project.
61. As a contributor, I want adding a Check to require no change to browser code, so that I can contribute one without understanding Playwright.
62. As a user, I want the CHANGELOG to record every new Check and every threshold change, so that I can explain why results differ between versions.
63. As a user, I want removing or renaming a Finding field, a tool or a tool parameter to be treated as a breaking change, so that I can depend on the output shape.

## Implementation Decisions

### Stack (ADR-0001)

- Python 3.12+, managed with `uv`; `pyright` strict; `ruff` for lint and format; `pytest` for tests.
- Official MCP Python SDK (FastMCP); stdio transport only.
- Official Playwright for Python (async API), headless Chromium, local only.
- `pydantic` for tool input schemas and the Finding model.
- `Pillow` + `numpy` for crop, resize and pixel sampling; `coloraide` for contrast and colour maths.
- Not added in v0.1: OpenCV, scikit-image, axe-core. Nothing in v0.1 needs them; they arrive with the phases that do.
- Published to PyPI as `squint-mcp`, run with `uvx squint-mcp`. MIT licence. English for everything public, including Finding messages.

### Modules

- **Server**: creates the MCP server, registers the three tools, owns annotations and the stdio entry point. Logs go to stderr only.
- **Tools**: one module per tool, each holding its input schema and handler. Handlers orchestrate; they contain no browser or pixel logic.
- **Capture production**: the only code allowed to import `playwright` (ADR-0002). Owns the single browser instance, stabilization, DOM/CSS collection and pixel capture, and returns a Capture.
- **Collectors**: the JavaScript that runs inside the page lives in separate `.js` files loaded by the Capture code, never as inline strings (ADR-0001).
- **Vision**: crop, downscale and colour sampling over a Capture's pixels. No browser access.
- **Checks**: one module per Check. A Check is a function of a Capture that returns `Finding[]`. Checks never import `playwright` (ADR-0002). This replaces the "detectors" and "audit rules" split of the original draft.
- **Config**: every threshold and default, each with its source cited in a comment. No user config file; behaviour is changed only through tool parameters.
- **Finding model**: the single output type of every Check.

Profile and Audit are defined in the glossary but have no code in v0.1.

### Capture

- A Capture is a stabilized snapshot of one page at one viewport: its DOM/CSS data together with its rendered pixels, plus a `stabilized` flag.
- One Capture per viewport. A call with several viewports produces several Captures.
- Captures are taken with `deviceScaleFactor: 1`.
- The DOM/CSS collection traverses open shadow roots. Iframe contents are not collected.
- The Capture is the whole contract between browser code and Checks: whatever a Check needs must be in it.

### Browser lifecycle

- One Chromium instance, launched lazily on the first call that needs it and reused until the server exits. No pool, no concurrency limit.
- Each tool call opens a fresh isolated browser context, and closes it when the call ends, on success or failure.
- Stateless: open the URL, stabilize, capture, close. No `actions` parameter, no interaction.

### Stabilization

In order:

1. Wait for `load`.
2. Wait for `document.fonts.ready`.
3. Zero all animations and transitions.
4. Wait for `networkidle` with a timeout of about 3s. On timeout, do **not** fail: record `stabilized: false` on the Capture and continue.

No lazy-load scrolling. No pausing of carousels or video. The `stabilized` flag is surfaced in the tool output.

### URL input

- Accepted: `http://`, `https://` (including `localhost`) and `file://`. Anything else is rejected with a clear error.
- No raw HTML input.
- No private-IP blocking in v0.1, because the server is stdio-only and runs on the user's machine. Blocking private IPs becomes mandatory when the HTTP transport is added.

### Tools

All tools: typed input schema, structured content plus a text summary, MCP annotations, and a total timeout of 30s with a clear error.

| Tool | Input | Output |
|---|---|---|
| `ping` | `message?` | server name, version, echoed message |
| `inspect_element` | `url`, `selector`, `viewport?` | computed styles, box model, sampled colours, `stabilized`, one crop image |
| `detect_visual_bugs` | `url`, `viewports?`, `checks?` | `Finding[]`, `stabilized` per viewport, up to five crop images |

- The `detect_visual_bugs` filter parameter is named `checks`, not `detectors` as in the original draft, following the glossary.
- `checks` omitted means all Checks. An unknown Check name is an error that lists the valid names.
- `viewport` / `viewports` omitted means the single default viewport from config.
- `inspect_element` errors when the selector matches zero elements or more than one.
- There is no `screenshot` tool in v0.1.

### Finding

One Finding = one element × one viewport × one Check. A Finding has no id of its own.

```jsonc
{
  "check": "text-clipped",            // the Check that produced it (was "id" in the draft)
  "category": "visual-bug",           // visual-bug | a11y | consistency | ux | responsive
  "severity": "major",                // critical | major | minor | info
  "message": "Text clipped by 14px by its container width",
  "selector": "[data-testid=hero-title]",
  "text": "Welcome to the new dashboard exper…", // visible text excerpt, ~40 chars
  "box": { "x": 120, "y": 340, "w": 480, "h": 56 }, // CSS px
  "viewport": { "width": 1440, "height": 900 },
  "evidence": {
    "computed": { "overflow": "hidden", "font-size": "48px" },
    "measured": { "overflowPx": 14 },
    "cropIndex": 0                    // index of the image in this response, or null (was "cropPath")
  },
  "suggestion": "Allow wrapping or reduce font-size at this width", // optional
  "source": "Squint heuristic"        // optional, e.g. "WCAG 2.2 SC 1.4.3"
}
```

Findings are returned ordered by severity, most severe first.

### Images

- Inline in the MCP response. Nothing is written to disk.
- At most five crops per call, allocated to Findings in severity order. Findings past the limit are still returned, with a null crop index.
- Each crop includes a margin around the element and is downscaled to about 512px on its longest side.
- Both limits are defaults in config.

### Selector generation

Preference order: `data-testid` > `id` (skipping ids that look generated) > role + accessible name > CSS path. A candidate is accepted only if it is unique on the page; otherwise fall through to the next.

### Checks in v0.1

- **`low-contrast-real`** (category `a11y`, source WCAG 2.2 SC 1.4.3): takes the computed text colour from the DOM and the background colour sampled from the pixels behind the text, and reports when the contrast ratio is below the WCAG threshold for that text size. The pixel-sampled background is the point: it resolves images and gradients that a computed `background-color` cannot.
- **`text-clipped`** (category `visual-bug`, source Squint heuristic): DOM signal is `scrollWidth > clientWidth` with clipping overflow; confirmed visually by the crop ending on a cut glyph. Reports the overflow in pixels.

### Project foundation

- README, LICENSE (MIT), CONTRIBUTING, CHANGELOG, SECURITY, GitHub issue and PR templates.
- CI runs typecheck, lint, format check and tests, and installs Chromium.
- Comments explain the *why* of heuristics and thresholds.
- Conventional Commits, small commits per Check.

### Versioning

0.x while the Finding schema is still changing. Breaking = removing or renaming a Finding field, a tool or a tool parameter. Changing a threshold or adding a Check is not breaking but goes in the CHANGELOG.

## Testing Decisions

- **One seam: the MCP tool boundary.** Tests drive the server through an in-memory MCP client, call the tools, and assert on the structured content and images that come back. This is the same surface a real client uses, so tests survive any internal restructuring.
- **Real Chromium, no mocks.** Playwright is not mocked and Captures are not hand-built. The value of Squint is in crossing real pixels with real DOM data; a mocked browser would test nothing of interest.
- **A good test asserts external behaviour only**: which Findings come back for a given page, with which fields, and which images. It does not assert on Capture internals, on which collector script ran, or on private helpers. Checks, vision, selector generation and stabilization are all covered through the tools, not by direct unit tests.
- **Fixtures are HTML files with planted problems**, loaded over `file://`. Where a behaviour needs a network (a page that never reaches `networkidle`, a page that fails to load), the test serves the fixture from a standard-library local HTTP server.
- **Every Check has a pair of fixtures**: one with the problem planted, one without. Its tests assert detection on the first and zero Findings on the second. The `low-contrast-real` pair must include text over an image or gradient, since that is the case a DOM-only tool gets wrong.
- **Determinism**: `deviceScaleFactor: 1`, animations disabled, one browser shared across the test session.
- Behaviours to cover through the seam: `ping` echo and version; `inspect_element` output shape, zero-match and multi-match errors, open shadow DOM; `detect_visual_bugs` default and filtered Checks, unknown Check error, multiple viewports, empty result on a clean page; Finding shape and severity ordering; selector preference order and uniqueness; five-crop limit with null crop index beyond it; crop size limit; `stabilized: false` without failure; unsupported scheme error; unloadable page error.
- **Prior art**: none. The repository has no code yet; these are the first tests and set the pattern.

## Out of Scope

- Tools: `screenshot`, `extract_tokens`, `compare_viewports`, `compare_with_mockup`, `audit_ui`.
- Checks other than `low-contrast-real` and `text-clipped` (`overlap`, `font-fallback`, `offscreen-overflow`, `ellipsis-unintended`, `invisible-content`, `broken-image`, `tap-target-small`, `layout-shift`).
- Profiles, Audits and scoring. axe-core integration.
- Interaction of any kind: clicks, typing, login flows, hover states, modals. Squint sees only the initial state of a page.
- Attaching to an existing browser over CDP (the intended future path past the initial-state limit).
- Iframe contents. Closed shadow DOM.
- Raw HTML input.
- Lazy-load scrolling; pausing carousels or video.
- HTTP transport, and the private-IP blocking that must come with it.
- Browser pool and concurrency limits. Firefox and WebKit. Remote browser execution.
- A user config file.
- Writing crops or reports to disk.
- Docker image and MCP registry listings (phase 5).
- Bypassing anti-bot protection.

## Further Notes

- Source of truth: the "Decididas no grill (2026-10-06)" subsection of the initial specification, which overrides its sections 5–13; vocabulary from `CONTEXT.md`; ADR-0001 and ADR-0002. Nothing here contradicts either ADR.
- v0.1 deliberately pulls two Checks forward from phase 2. Phases 0 and 1 alone would not show any advantage over `@playwright/mcp`.
- Points this spec settled that the grill left implicit. Each is cheap to change before tickets are cut:
  - the `detectors` parameter is renamed `checks`;
  - the crop reference field is named `evidence.cropIndex` and is null when the Finding got no image;
  - the visible-text excerpt field is named `text`;
  - `inspect_element` errors on a selector matching more than one element, rather than picking the first;
  - the default viewport is a single desktop size (1440×900, as in the draft's example), held in config;
  - `low-contrast-real` is categorised `a11y` and `text-clipped` `visual-bug`.
- Deferred decisions that do not block v0.1: `overlap` false positives (phase 2), mockup formats (phase 3), Audit score formula (phase 4).
