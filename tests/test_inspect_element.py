"""`inspect_element` through the MCP tool boundary, against real Chromium."""

import base64
import io
import time
from pathlib import Path
from typing import Any

import anyio
import pytest
from mcp import Client
from mcp.types import CallToolResult, ImageContent, TextContent, Tool
from PIL import Image

from squint_mcp import config
from squint_mcp.capture import BrowserSession
from squint_mcp.server import server

pytestmark = pytest.mark.anyio

FIXTURES = Path(__file__).parent / "fixtures"
BOX = (FIXTURES / "box.html").as_uri()
MOTION = (FIXTURES / "motion.html").as_uri()
VISIT = (FIXTURES / "visit.html").as_uri()
PIXEL_COST = (FIXTURES / "pixel-cost.html").as_uri()

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


async def call(client: Client, url: str, selector: str, **extra: Any) -> CallToolResult:
    arguments = {"url": url, "selector": selector, **extra}
    return await client.call_tool("inspect_element", arguments)


async def inspect(
    client: Client, url: str, selector: str, **extra: Any
) -> dict[str, Any]:
    """Call the tool and return its structured content, failing on a tool error."""
    result = await call(client, url, selector, **extra)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


async def crop(client: Client, selector: str) -> Image.Image:
    """Decode the one image the tool returns for `selector` in the box fixture."""
    result = await call(client, BOX, selector)
    (image,) = (block for block in result.content if isinstance(block, ImageContent))
    return Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")


async def crop_size(client: Client, selector: str) -> tuple[int, int]:
    return (await crop(client, selector)).size


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


async def test_box_model_content_is_the_layout_size_of_a_scaled_element(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#scaled")
    assert content["boxModel"]["content"] == {"w": 50, "h": 30}


async def test_box_of_a_scaled_element_is_the_transformed_rect(client: Client) -> None:
    content = await inspect(client, BOX, "#scaled")
    assert content["box"] == {"x": 40, "y": 1000, "w": 200, "h": 120}


async def test_box_model_content_is_the_layout_size_of_a_rotated_element(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#rotated")
    assert content["boxModel"]["content"] == {"w": 50, "h": 30}


async def test_box_model_content_of_an_svg_element_falls_back_to_its_rect(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#vector")
    assert content["boxModel"]["content"] == {"w": 40, "h": 20}


async def test_box_model_content_keeps_the_fractional_size_of_an_untransformed_element(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#frac")
    assert content["boxModel"]["content"] == {"w": 100.5, "h": 60}


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
    assert (await inspect(client, BOX, "#screen"))["box"]["h"] == 900


async def test_viewport_argument_sets_the_page_size(client: Client) -> None:
    viewport = {"width": 390, "height": 844}
    content = await inspect(client, BOX, "#full", viewport=viewport)
    assert content["viewport"] == viewport
    assert content["box"]["w"] == 390
    screen = await inspect(client, BOX, "#screen", viewport=viewport)
    assert screen["box"]["h"] == 844


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


async def test_a_page_idle_only_after_five_seconds_is_returned_unstabilized(
    client: Client, local_server: str
) -> None:
    url = f"{local_server}/polling-briefly.html?ms=5000"
    assert (await inspect(client, url, "#probe"))["stabilized"] is False


async def test_a_page_idle_after_a_second_and_a_half_is_stabilized(
    client: Client, local_server: str
) -> None:
    url = f"{local_server}/polling-briefly.html?ms=1500"
    assert (await inspect(client, url, "#probe"))["stabilized"] is True


async def test_animations_and_transitions_are_taken_to_their_end(
    client: Client,
) -> None:
    assert (await inspect(client, MOTION, "#animated"))["computed"]["opacity"] == "1"
    assert (await inspect(client, MOTION, "#transitioned"))["computed"][
        "opacity"
    ] == "1"


async def test_animations_inside_an_open_shadow_root_are_taken_to_their_end(
    client: Client,
) -> None:
    content = await inspect(client, MOTION, "#shadow-animated")
    assert content["computed"]["opacity"] == "1"


async def test_transitions_starting_later_inside_an_open_shadow_root_take_no_time(
    client: Client,
) -> None:
    content = await inspect(client, MOTION, "#shadow-late")
    assert content["computed"]["opacity"] == "1"


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


async def test_structured_content_has_exactly_the_documented_keys(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#solid")
    assert set(content) == {
        "viewport",
        "stabilized",
        "box",
        "boxModel",
        "computed",
        "sampledColors",
    }


async def test_sampled_colors_are_the_painted_colors_by_share(client: Client) -> None:
    content = await inspect(client, BOX, "#solid")
    assert content["sampledColors"] == [
        {"hex": "#ff0000", "share": 0.7857},
        {"hex": "#0000ff", "share": 0.2143},
    ]


async def test_sampled_colors_keep_the_three_most_frequent(client: Client) -> None:
    content = await inspect(client, BOX, "#many")
    assert content["sampledColors"] == [
        {"hex": "#0a0a0a", "share": 0.4},
        {"hex": "#141414", "share": 0.3},
        {"hex": "#1e1e1e", "share": 0.2},
    ]


async def test_sampled_color_is_the_painted_one_not_the_computed_one(
    client: Client,
) -> None:
    content = await inspect(client, BOX, "#over-image")
    assert content["computed"]["background-color"] == "rgb(255, 255, 255)"
    assert content["sampledColors"][0]["hex"] == "#000000"


async def test_a_region_over_the_limit_keeps_its_painted_colours_and_shares(
    client: Client,
) -> None:
    content = await inspect(client, PIXEL_COST, "#halves")
    assert content["sampledColors"] == [
        {"hex": "#ff0000", "share": 0.5},
        {"hex": "#0000ff", "share": 0.5},
    ]


async def test_an_element_of_millions_of_colours_adds_little_to_the_call(
    client: Client,
) -> None:
    async def seconds(selector: str, height: int) -> float:
        started = time.monotonic()
        content = await inspect(client, PIXEL_COST, selector)
        elapsed = time.monotonic() - started
        assert content["box"]["h"] == height
        return elapsed

    # The same page both times, so the capture costs the same: what differs is
    # the work on the pixels of the element.
    small = await seconds("#big-text", 600)
    assert await seconds("#noise", 10000) - small < 3


async def test_success_carries_a_summary_and_one_png_crop(client: Client) -> None:
    result = await call(client, BOX, "#solid")
    assert result.is_error is False
    assert any("#solid" in text for text in texts(result))
    images = [block for block in result.content if isinstance(block, ImageContent)]
    assert [image.mime_type for image in images] == ["image/png"]


async def test_crop_is_the_box_plus_a_16px_margin_at_one_pixel_per_css_pixel(
    client: Client,
) -> None:
    assert await crop_size(client, "#solid") == (152, 102)


async def test_crop_shows_the_element_as_painted(client: Client) -> None:
    image = await crop(client, "#solid")
    assert image.getpixel((0, 0)) == (255, 255, 255)  # margin: page background
    assert image.getpixel((16, 16)) == (0, 0, 255)  # first pixel of the border
    assert image.getpixel((21, 21)) == (255, 0, 0)  # first pixel inside the border
    assert image.getpixel((76, 51)) == (255, 0, 0)  # centre


async def test_crop_margin_is_clamped_to_the_page(client: Client) -> None:
    assert await crop_size(client, "#corner") == (66, 66)  # top-right of the page
    assert await crop_size(client, "#below") == (116, 66)  # bottom-left of the page


async def test_crop_is_downscaled_to_512px_on_its_longest_side(client: Client) -> None:
    assert await crop_size(client, "#wide") == (512, 65)
    assert (await crop_size(client, "#screen"))[1] == 512  # 1x900: tall, not wide


async def test_an_element_below_the_fold_has_pixels(client: Client) -> None:
    content = await inspect(client, BOX, "#below")
    assert content["box"]["y"] == 2000
    assert content["sampledColors"][0]["hex"] == "#008000"


async def test_box_stays_in_page_coordinates_when_the_page_is_scrolled(
    client: Client,
) -> None:
    # The fragment scrolls the page to the element before it is captured.
    content = await inspect(client, f"{BOX}#below", "#below")
    assert content["box"]["y"] == 2000
    assert content["sampledColors"][0]["hex"] == "#008000"


async def error_text(client: Client, url: str, selector: str) -> str:
    """Call the tool, expect a tool error and return its text."""
    result = await call(client, url, selector)
    assert result.is_error is True
    return " ".join(texts(result))


async def test_selector_matching_nothing_is_an_error(client: Client) -> None:
    text = await error_text(client, BOX, "#missing")
    assert 'Selector "#missing" matched no elements.' in text


async def test_selector_matching_several_elements_is_an_error(client: Client) -> None:
    text = await error_text(client, BOX, ".dup")
    assert 'Selector ".dup" matched 2 elements; it must match exactly one.' in text


async def test_invalid_selector_is_an_error(client: Client) -> None:
    assert 'Invalid selector "div[".' in await error_text(client, BOX, "div[")


async def test_element_with_no_rendered_box_is_an_error(client: Client) -> None:
    text = await error_text(client, BOX, "#hidden")
    assert 'Selector "#hidden" matched an element with no rendered box.' in text


async def test_element_outside_the_page_origin_has_no_rendered_box(
    client: Client,
) -> None:
    for selector in ("#left-of-page", "#above-page"):
        text = await error_text(client, BOX, selector)
        assert f'Selector "{selector}" matched an element with no rendered box.' in text


async def test_unsupported_url_scheme_is_an_error(client: Client) -> None:
    text = await error_text(client, "ftp://example.com/page.html", "#solid")
    assert 'Unsupported URL scheme "ftp"; use http://, https:// or file://.' in text


async def test_page_that_cannot_be_loaded_is_an_error(client: Client) -> None:
    url = (FIXTURES / "no-such-page.html").as_uri()
    assert f"Could not load {url}" in await error_text(client, url, "#solid")


async def test_missing_chromium_names_the_install_command(
    client_without_chromium: Client,
) -> None:
    text = await error_text(client_without_chromium, BOX, "#solid")
    assert "Could not launch Chromium" in text
    assert "playwright install chromium" in text


async def test_server_answers_ping_while_chromium_cannot_be_launched(
    client_without_chromium: Client,
) -> None:
    tools = (await client_without_chromium.list_tools()).tools
    assert sorted(tool.name for tool in tools) == [
        "detect_visual_bugs",
        "inspect_element",
        "ping",
    ]
    result = await client_without_chromium.call_tool("ping", {})
    assert result.is_error is False


async def test_call_that_outlives_the_total_timeout_is_an_error_and_server_recovers(
    client: Client, local_server: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The only reach past the MCP boundary: 30 real seconds would slow every run.
    with monkeypatch.context() as patch:
        patch.setattr(config, "TOTAL_TIMEOUT_S", 1.0)
        started = time.monotonic()
        text = await error_text(client, f"{local_server}/hang", "#solid")
        elapsed = time.monotonic() - started
    assert "Timed out after 1s" in text
    assert 1 <= elapsed < 2
    assert (await inspect(client, BOX, "#solid"))["box"]["w"] == 120


@pytest.fixture
def browsers(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """Every browser the server hands to a call, in order.

    A reach past the MCP boundary: no tool reports the open contexts of the
    browser, and none can kill it.
    """
    handed_out: list[Any] = []
    original = BrowserSession.browser

    async def spy(self: BrowserSession) -> Any:
        browser = await original(self)
        handed_out.append(browser)
        return browser

    monkeypatch.setattr(BrowserSession, "browser", spy)
    return handed_out


async def test_call_cancelled_by_the_client_leaves_no_browser_context_open(
    client: Client, local_server: str, browsers: list[Any]
) -> None:
    with anyio.move_on_after(1.5) as cancelled:
        await call(client, f"{local_server}/hang", "#solid")
    assert cancelled.cancelled_caught
    with anyio.move_on_after(3):
        while browsers[-1].contexts:
            await anyio.sleep(0.05)
    assert browsers[-1].contexts == []


async def test_call_after_the_browser_died_relaunches_it(browsers: list[Any]) -> None:
    # Its own server run: the browser of the shared client is left alone.
    async with Client(server) as own:
        assert (await inspect(own, BOX, "#solid"))["box"]["w"] == 120
        await browsers[-1].close()
        assert (await inspect(own, BOX, "#solid"))["box"]["w"] == 120
