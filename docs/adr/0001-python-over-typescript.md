# Python over TypeScript

Most MCP servers are TypeScript and ship via `npx`, but Squint is written in Python (3.12+, `uv`, `pyright` strict, `ruff`) and ships via `uvx squint-mcp`. The roadmap needs real computer vision (mockup alignment, SSIM, region detection, font-metric comparison), where Python's ecosystem (OpenCV, NumPy, scikit-image, coloraide) has no TypeScript equivalent, and the sole maintainer reviews every AI-written diff and is far more comfortable reading Python.

## Consequences

- Install is two steps (`uvx squint-mcp` plus `playwright install chromium`) instead of one `npx`.
- Code that runs inside the page is still JavaScript; it lives in separate `.js` files, never inline strings.
