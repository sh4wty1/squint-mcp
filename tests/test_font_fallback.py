"""The `font-fallback` Check through `detect_visual_bugs`, against real Chromium."""

import pytest
from mcp import Client

pytestmark = pytest.mark.anyio


async def test_the_tool_description_says_what_font_fallback_reports(
    client: Client,
) -> None:
    tools = (await client.list_tools()).tools
    (tool,) = (tool for tool in tools if tool.name == "detect_visual_bugs")
    assert tool.description is not None
    assert (
        "`font-fallback` (a font the page declares that did not load, one Finding "
        "per family)" in " ".join(tool.description.split())
    )
