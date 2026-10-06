"""`inspect_element` through the MCP tool boundary, against real Chromium."""

from pathlib import Path
from typing import Any

import pytest
from mcp import Client
from mcp.types import CallToolResult, TextContent, Tool

pytestmark = pytest.mark.anyio

FIXTURES = Path(__file__).parent / "fixtures"
BOX = (FIXTURES / "box.html").as_uri()
MOTION = (FIXTURES / "motion.html").as_uri()
VISIT = (FIXTURES / "visit.html").as_uri()

COMPUTED_PROPERTIES = {
    "display",
    "position",
    "box-sizing",
    "width",
    "height",
    "color",
    "background-color",
    "background-image",
    "opacity",
    "visibility",
    "overflow-x",
    "overflow-y",
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "letter-spacing",
    "text-align",
    "text-overflow",
    "white-space",
}


async def inspect_tool(client: Client) -> Tool:
    (tool,) = (
        t for t in (await client.list_tools()).tools if t.name == "inspect_element"
    )
    return tool


def texts(result: CallToolResult) -> list[str]:
    return [block.text for block in result.content if isinstance(block, TextContent)]


async def inspect(
    client: Client, url: str, selector: str, **extra: Any
) -> dict[str, Any]:
    """Call the tool and return its structured content, failing on a tool error."""
    result = await client.call_tool(
        "inspect_element", {"url": url, "selector": selector, **extra}
    )
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


async def test_inspect_element_is_read_only_and_open_world(client: Client) -> None:
    annotations = (await inspect_tool(client)).annotations
    assert annotations is not None
    assert annotations.read_only_hint is True
    assert annotations.open_world_hint is True


async def test_inspect_element_takes_url_selector_and_optional_viewport(
    client: Client,
) -> None:
    schema = (await inspect_tool(client)).input_schema
    properties = schema["properties"]
    assert set(properties) == {"url", "selector", "viewport"}
    assert properties["url"]["type"] == "string"
    assert properties["selector"]["type"] == "string"
    assert set(schema["required"]) == {"url", "selector"}

    def type_of(option: dict[str, Any]) -> str:
        if "$ref" in option:
            option = schema["$defs"][option["$ref"].removeprefix("#/$defs/")]
        return option["type"]

    assert {type_of(option) for option in properties["viewport"]["anyOf"]} == {
        "object",
        "null",
    }


async def test_box_is_the_border_box_in_page_coordinates(client: Client) -> None:
    content = await inspect(client, BOX, "#solid")
    assert content["box"] == {"x": 40, "y": 60, "w": 120, "h": 70}


async def test_box_model_reports_margin_border_padding_and_content(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#solid")
    assert content["boxModel"] == {
        "margin": {"top": 60, "right": 10, "bottom": 20, "left": 40},
        "border": {"top": 5, "right": 5, "bottom": 5, "left": 5},
        "padding": {"top": 10, "right": 15, "bottom": 10, "left": 15},
        "content": {"w": 80, "h": 40},
    }


async def test_computed_holds_exactly_the_configured_properties(client: Client) -> None:
    content = await inspect(client, BOX, "#solid")
    assert set(content["computed"]) == COMPUTED_PROPERTIES


async def test_computed_values_are_what_the_browser_resolved(client: Client) -> None:
    computed = (await inspect(client, BOX, "#solid"))["computed"]
    assert computed["font-size"] == "20px"
    assert computed["background-color"] == "rgb(255, 0, 0)"
    assert computed["display"] == "block"


async def test_default_viewport_is_1440_by_900(client: Client) -> None:
    content = await inspect(client, BOX, "#full")
    assert content["viewport"] == {"width": 1440, "height": 900}
    assert content["box"]["w"] == 1440


async def test_viewport_argument_sets_the_page_size(client: Client) -> None:
    viewport = {"width": 390, "height": 844}
    content = await inspect(client, BOX, "#full", viewport=viewport)
    assert content["viewport"] == viewport
    assert content["box"]["w"] == 390


async def test_null_viewport_matches_omitting_it(client: Client) -> None:
    omitted = await inspect(client, BOX, "#full")
    assert await inspect(client, BOX, "#full", viewport=None) == omitted


async def test_selector_reaches_into_an_open_shadow_root(client: Client) -> None:
    content = await inspect(client, BOX, "#inner")
    assert content["computed"]["color"] == "rgb(0, 0, 255)"


async def test_a_page_that_goes_network_idle_is_stabilized(client: Client) -> None:
    assert (await inspect(client, BOX, "#solid"))["stabilized"] is True


async def test_a_page_that_never_goes_network_idle_is_returned_unstabilized(
    client: Client, local_server: str
) -> None:
    content = await inspect(client, f"{local_server}/polling.html", "#probe")
    assert content["stabilized"] is False


async def test_animations_and_transitions_are_taken_to_their_end(
    client: Client,
) -> None:
    assert (await inspect(client, MOTION, "#animated"))["computed"]["opacity"] == "1"
    assert (await inspect(client, MOTION, "#transitioned"))["computed"][
        "opacity"
    ] == "1"


async def test_http_urls_are_accepted(client: Client, local_server: str) -> None:
    content = await inspect(client, f"{local_server}/box.html", "#solid")
    assert content["box"] == {"x": 40, "y": 60, "w": 120, "h": 70}


async def test_calls_do_not_share_browser_storage(client: Client) -> None:
    first_visit = "rgb(0, 128, 0)"
    for _ in range(2):
        content = await inspect(client, VISIT, "#probe")
        assert content["computed"]["background-color"] == first_visit


async def test_missing_selector_is_rejected(client: Client) -> None:
    result = await client.call_tool("inspect_element", {"url": BOX})
    assert result.is_error is True
    assert any("selector" in text for text in texts(result))


async def test_viewport_smaller_than_one_pixel_is_rejected(client: Client) -> None:
    for field in ("width", "height"):
        viewport = {"width": 1440, "height": 900, field: 0}
        result = await client.call_tool(
            "inspect_element", {"url": BOX, "selector": "#solid", "viewport": viewport}
        )
        assert result.is_error is True
        assert any(field in text for text in texts(result))
