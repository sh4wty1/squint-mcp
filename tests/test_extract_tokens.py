"""`extract_tokens` through the MCP tool boundary, against real Chromium."""

from typing import Any

import pytest
from helpers import fixture_url, texts
from mcp import Client
from mcp.types import CallToolResult, TextContent, Tool

pytestmark = pytest.mark.anyio

PAGE = "tokens-page.html"


async def tokens_tool(client: Client) -> Tool:
    (tool,) = (
        t for t in (await client.list_tools()).tools if t.name == "extract_tokens"
    )
    return tool


async def call(client: Client, name: str, **arguments: Any) -> CallToolResult:
    """Call the tool on the fixture `name`."""
    return await client.call_tool(
        "extract_tokens", {"url": fixture_url(name), **arguments}
    )


async def extract(client: Client, name: str, **arguments: Any) -> dict[str, Any]:
    """Call the tool on a fixture and return its structured content, failing on
    a tool error."""
    result = await call(client, name, **arguments)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


def families(result: dict[str, Any]) -> list[dict[str, Any]]:
    """The eight Families of a result."""
    typography = result["typography"]
    return [
        result["colors"],
        typography["families"],
        typography["sizes"],
        typography["weights"],
        typography["lineHeights"],
        result["spacing"],
        result["radii"],
        result["shadows"],
    ]


async def test_extract_tokens_is_listed_with_its_hints_and_its_schemas(
    client: Client,
) -> None:
    tool = await tokens_tool(client)
    assert tool.annotations is not None
    assert tool.annotations.read_only_hint is True
    assert tool.annotations.open_world_hint is True
    assert tool.output_schema is not None

    schema = tool.input_schema
    properties = schema["properties"]
    assert set(properties) == {"url", "scope", "viewport"}
    assert schema["required"] == ["url"]
    assert properties["url"]["type"] == "string"

    def options(name: str) -> dict[str, dict[str, Any]]:
        """What an optional argument takes, by JSON type."""
        resolved: dict[str, dict[str, Any]] = {}
        for option in properties[name]["anyOf"]:
            if "$ref" in option:
                option = schema["$defs"][option["$ref"].removeprefix("#/$defs/")]
            resolved[option["type"]] = option
        return resolved

    assert set(options("scope")) == {"string", "null"}
    viewport = options("viewport")
    assert set(viewport) == {"object", "null"}
    sides = viewport["object"]["properties"]
    assert set(sides) == {"width", "height"}
    assert sides["width"]["minimum"] == 1
    assert sides["height"]["minimum"] == 1


async def test_result_tells_the_call_the_elements_read_and_a_total_per_family(
    client: Client,
) -> None:
    result = await extract(client, PAGE)
    assert result["viewport"] == {"width": 1440, "height": 900}
    assert result["stabilized"] is True
    assert result["scope"] is None
    # `html`, `body` and the six elements of the page: those of `head` have no box.
    assert result["elements"] == 8
    for family in families(result):
        assert family["total"] == len(family["tokens"])


async def test_result_is_one_text_block_and_no_image(client: Client) -> None:
    result = await call(client, PAGE)
    assert result.is_error is False, texts(result)
    (block,) = result.content
    assert isinstance(block, TextContent)
