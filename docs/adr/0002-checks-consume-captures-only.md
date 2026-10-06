# Checks consume Captures only; Playwright stays behind the Capture

Playwright (the library) is used as an ordinary dependency to drive Chromium, but only the code that produces a Capture may import it; Checks receive a Capture and never touch the browser. We rejected talking CDP directly or porting Playwright internals, since driving a browser is solved plumbing and Squint's value starts after pixels and DOM data arrive.

Every tool call is stateless: open the URL, stabilize, capture, close. This means Squint only sees a page's initial state (no modals, hover states, or post-login screens). That limit is deliberate for v0.1; the intended way past it is attaching to an already-open browser over CDP to produce the Capture, not adding interaction actions to Squint's tools.
