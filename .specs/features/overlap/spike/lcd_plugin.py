"""pytest plugin: every Chromium of the run is launched with --disable-lcd-text."""
from playwright.async_api import BrowserType

_launch = BrowserType.launch


async def launch(self, *args, **kwargs):
    kwargs["args"] = [*(kwargs.get("args") or []), "--disable-lcd-text"]
    return await _launch(self, *args, **kwargs)


BrowserType.launch = launch
