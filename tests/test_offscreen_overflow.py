"""`offscreen-overflow` through `detect_visual_bugs`, against real Chromium."""

import base64
import io
from typing import Any

import pytest
from helpers import DESKTOP, detect, fixture_url, images, texts
from mcp import Client
from PIL import Image

pytestmark = pytest.mark.anyio

ONLY = ["offscreen-overflow"]
# Narrower than every page captured at it.
SMALL = {"width": 400, "height": 300}


def page(name: str) -> str:
    return fixture_url(f"offscreen-overflow-{name}.html")


BUG = page("bug")


async def small(client: Client, name: str) -> list[dict[str, Any]]:
    """The Findings of the Check on one of its fixtures, at 400x300."""
    content = await detect(client, page(name), viewports=[SMALL], checks=ONLY)
    return content["findings"]


async def crop_width(
    client: Client, name: str, selector: str, viewport: dict[str, int] = SMALL
) -> int:
    """How wide the crop of one element is: its box and 16px on each side.

    The crop stops where the pixels of the page do, so its width tells where
    they end.
    """
    arguments = {"url": page(name), "selector": selector, "viewport": viewport}
    result = await client.call_tool("inspect_element", arguments)
    assert result.is_error is False, texts(result)
    (image,) = images(result)
    return Image.open(io.BytesIO(base64.b64decode(image.data))).width


async def test_a_page_wider_than_its_viewport_yields_one_finding(
    client: Client,
) -> None:
    (finding,) = (await detect(client, BUG, checks=ONLY))["findings"]
    assert finding["selector"] == "#wide"
    assert finding["check"] == "offscreen-overflow"
    assert finding["category"] == "responsive"
    assert finding["severity"] == "major"
    assert finding["source"] == "Squint heuristic"


async def test_the_finding_carries_the_widths_and_the_styles_that_explain_it(
    client: Client,
) -> None:
    (finding,) = (await detect(client, BUG, checks=ONLY))["findings"]
    assert finding["message"] == (
        "Extends 200px past the 1440px viewport, so the page scrolls horizontally"
    )
    assert finding["evidence"]["measured"] == {
        "overflowPx": 200,
        "pageWidth": 1640,
        "viewportWidth": 1440,
    }
    assert finding["evidence"]["computed"] == {
        "display": "block",
        "position": "static",
        "width": "1640px",
        "white-space": "normal",
    }


async def test_an_element_at_the_edge_is_named_instead_of_its_child_at_the_same_edge(
    client: Client,
) -> None:
    findings = await small(client, "nested")
    assert [finding["selector"] for finding in findings] == ["#outer"]


async def test_a_child_at_the_edge_is_named_instead_of_its_parent_that_fits(
    client: Client,
) -> None:
    findings = await small(client, "child")
    assert [finding["selector"] for finding in findings] == ["#child"]


async def test_an_element_one_pixel_short_of_the_edge_is_not_the_one_named(
    client: Client,
) -> None:
    findings = await small(client, "near")
    assert [finding["selector"] for finding in findings] == ["#edge"]


@pytest.mark.parametrize(
    ("name", "page_width"), [("fraction-short", 601), ("fraction-past", 600)]
)
async def test_an_element_under_a_pixel_from_the_edge_is_named(
    client: Client, name: str, page_width: int
) -> None:
    (finding,) = await small(client, name)
    assert finding["selector"] == "#fraction"
    assert finding["evidence"]["measured"] == {
        "overflowPx": page_width - 400,
        "pageWidth": page_width,
        "viewportWidth": 400,
    }


async def test_a_word_that_cannot_break_names_the_element_whose_text_it_is(
    client: Client,
) -> None:
    (finding,) = await small(client, "word")
    assert finding["selector"] == "#word"
    # The box fits the viewport; only its text reaches the edge.
    assert finding["box"]["w"] == 200
    assert finding["evidence"]["measured"]["overflowPx"] == 200


async def test_an_element_moved_by_a_transform_is_reported_where_it_is_painted(
    client: Client,
) -> None:
    (finding,) = await small(client, "moved")
    assert finding["box"] == {"x": 450, "y": 0, "w": 100, "h": 20}
    assert finding["evidence"]["measured"]["overflowPx"] == 150


async def test_one_pixel_past_the_viewport_is_reported_and_none_is_not(
    client: Client,
) -> None:
    narrower = {"width": 399, "height": 300}
    content = await detect(
        client, page("one"), viewports=[narrower, SMALL], checks=ONLY
    )
    (finding,) = content["findings"]
    assert finding["viewport"] == narrower
    assert finding["evidence"]["measured"] == {
        "overflowPx": 1,
        "pageWidth": 400,
        "viewportWidth": 399,
    }


async def test_a_page_as_wide_as_its_viewport_yields_no_finding(client: Client) -> None:
    assert (await detect(client, page("clean")))["findings"] == []
    # The pixels end at 1440px, 100px into `#fixed`: 16px of margin and those.
    assert await crop_width(client, "clean", "#fixed", DESKTOP) == 116


@pytest.mark.parametrize(
    "name", ["hidden-html", "clip-html", "hidden-body", "clip-body"]
)
async def test_a_page_that_hides_its_horizontal_overflow_yields_no_finding(
    client: Client, name: str
) -> None:
    assert await small(client, name) == []
    # The pixels end at 480px, with `#wide`: no margin on either side of it.
    assert await crop_width(client, name, "#wide") == 480


async def test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named(
    client: Client,
) -> None:
    # The viewport takes the overflow-x of body only while that of html is visible.
    findings = await small(client, "body-under-html")
    assert [finding["selector"] for finding in findings] == ["body"]


async def test_a_right_to_left_page_yields_no_finding(client: Client) -> None:
    assert await small(client, "rtl") == []
    # The pixels end at 600px, with `#pinned`: 16px of margin and its 100px.
    assert await crop_width(client, "rtl", "#pinned") == 116


async def test_a_page_widened_by_a_pseudo_element_yields_no_finding(
    client: Client,
) -> None:
    assert await small(client, "pseudo") == []
    # The pixels go on past `#host`, 400px wide: its 400px and 16px of margin.
    assert await crop_width(client, "pseudo", "#host") == 416


async def test_naming_the_check_returns_its_finding_alone(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert [(finding["selector"], finding["check"]) for finding in findings] == [
        ("#wide", "offscreen-overflow")
    ]


async def test_omitting_checks_returns_the_findings_of_every_check(
    client: Client,
) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert [(finding["selector"], finding["check"]) for finding in findings] == [
        ("#wide", "offscreen-overflow"),
        ("#clipped", "text-clipped"),
    ]
    assert {finding["severity"] for finding in findings} == {"major"}


async def test_the_tool_description_says_what_offscreen_overflow_reports(
    client: Client,
) -> None:
    tools = (await client.list_tools()).tools
    (tool,) = (tool for tool in tools if tool.name == "detect_visual_bugs")
    assert tool.description is not None
    assert (
        "`offscreen-overflow` (the element that sets the width of a page that "
        "scrolls horizontally"
    ) in " ".join(tool.description.split())
