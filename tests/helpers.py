"""Shared by the `detect_visual_bugs` test modules."""

import base64
import io
from pathlib import Path
from typing import Any

from mcp import Client
from mcp.types import CallToolResult, ImageContent, TextContent
from PIL import Image

FIXTURES = Path(__file__).parent / "fixtures"

DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}


def fixture_url(name: str) -> str:
    return (FIXTURES / name).as_uri()


def texts(result: CallToolResult) -> list[str]:
    return [block.text for block in result.content if isinstance(block, TextContent)]


def images(result: CallToolResult) -> list[ImageContent]:
    return [block for block in result.content if isinstance(block, ImageContent)]


def decode(image: ImageContent) -> Image.Image:
    """The picture an image block of a response carries, in RGB."""
    return Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")


async def call(client: Client, url: str, **extra: Any) -> CallToolResult:
    return await client.call_tool("detect_visual_bugs", {"url": url, **extra})


async def detect(client: Client, url: str, **extra: Any) -> dict[str, Any]:
    """Call the tool and return its structured content, failing on a tool error."""
    result = await call(client, url, **extra)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


async def findings_on(
    client: Client,
    url: str,
    selector: str,
    findings: list[dict[str, Any]],
    viewport: dict[str, int] = DESKTOP,
) -> list[dict[str, Any]]:
    """The Findings of `viewport` that sit on the one element `selector` matches.

    The element is located by `inspect_element`, so the lookup does not depend
    on the selector the Finding carries.
    """
    arguments = {"url": url, "selector": selector, "viewport": viewport}
    result = await client.call_tool("inspect_element", arguments)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    box = result.structured_content["box"]
    return [f for f in findings if f["box"] == box and f["viewport"] == viewport]
