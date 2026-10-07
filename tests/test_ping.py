"""`ping` through the MCP tool boundary."""

from importlib.metadata import version

import pytest
from mcp import Client
from mcp.types import CallToolResult, TextContent, Tool

pytestmark = pytest.mark.anyio

NAME = "squint-mcp"
VERSION = version(NAME)


async def ping_tool(client: Client) -> Tool:
    (tool,) = (t for t in (await client.list_tools()).tools if t.name == "ping")
    return tool


def texts(result: CallToolResult) -> list[str]:
    return [block.text for block in result.content if isinstance(block, TextContent)]


async def test_server_reports_its_name(client: Client) -> None:
    assert client.server_info is not None
    assert client.server_info.name == NAME


async def test_server_reports_its_version(client: Client) -> None:
    assert client.server_info is not None
    assert client.server_info.version == VERSION


async def test_tools_are_exactly_the_three_documented_ones(client: Client) -> None:
    tools = (await client.list_tools()).tools
    assert sorted(tool.name for tool in tools) == [
        "detect_visual_bugs",
        "inspect_element",
        "ping",
    ]


async def test_ping_is_read_only_and_closed_world(client: Client) -> None:
    annotations = (await ping_tool(client)).annotations
    assert annotations is not None
    assert annotations.read_only_hint is True
    assert annotations.open_world_hint is False


async def test_ping_takes_only_an_optional_string_message(client: Client) -> None:
    schema = (await ping_tool(client)).input_schema
    assert list(schema["properties"]) == ["message"]
    message = schema["properties"]["message"]
    accepted = {message.get("type")} | {o.get("type") for o in message.get("anyOf", [])}
    assert accepted - {None, "null"} == {"string"}
    assert "message" not in schema.get("required", [])


async def test_ping_echoes_the_message(client: Client) -> None:
    result = await client.call_tool("ping", {"message": "hello"})
    assert result.structured_content == {
        "name": NAME,
        "version": VERSION,
        "message": "hello",
    }


async def test_ping_without_message_returns_null(client: Client) -> None:
    result = await client.call_tool("ping", {})
    assert result.structured_content == {
        "name": NAME,
        "version": VERSION,
        "message": None,
    }


async def test_ping_success_carries_a_text_summary(client: Client) -> None:
    result = await client.call_tool("ping", {})
    assert result.is_error is False
    assert any(NAME in text and VERSION in text for text in texts(result))


async def test_ping_rejects_a_non_string_message(client: Client) -> None:
    result = await client.call_tool("ping", {"message": 123})
    assert result.is_error is True
    assert any("message" in text for text in texts(result))


async def test_ping_echoes_an_empty_message_as_empty(client: Client) -> None:
    result = await client.call_tool("ping", {"message": ""})
    assert result.structured_content == {
        "name": NAME,
        "version": VERSION,
        "message": "",
    }


async def test_ping_echoes_the_message_unchanged(client: Client) -> None:
    message = "  a longer message, padded with spaces  "
    result = await client.call_tool("ping", {"message": message})
    assert result.structured_content == {
        "name": NAME,
        "version": VERSION,
        "message": message,
    }


async def test_ping_with_null_message_matches_omitting_it(client: Client) -> None:
    result = await client.call_tool("ping", {"message": None})
    assert result.structured_content == {
        "name": NAME,
        "version": VERSION,
        "message": None,
    }
