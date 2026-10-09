"""The `offscreen-overflow` Check through `detect_visual_bugs`, against Chromium."""

from typing import Any

import pytest
from helpers import DESKTOP, MOBILE, detect, findings_on, fixture_url
from mcp import Client

pytestmark = pytest.mark.anyio

ONLY = ["offscreen-overflow"]


def page(name: str) -> str:
    return fixture_url(f"overflow-{name}.html")


async def findings(client: Client, name: str, **extra: Any) -> list[dict[str, Any]]:
    """The Findings of the Check alone on the fixture `name`."""
    return (await detect(client, page(name), checks=ONLY, **extra))["findings"]


async def the_finding_on(client: Client, name: str, selector: str) -> dict[str, Any]:
    """The one Finding of the fixture `name`, which has to sit on `selector`."""
    found = await findings(client, name)
    assert len(found) == 1
    (finding,) = await findings_on(client, page(name), selector, found)
    return finding


async def test_a_page_that_scrolls_sideways_yields_one_finding_per_viewport(
    client: Client,
) -> None:
    found = await findings(client, "bug", viewports=[DESKTOP, MOBILE])
    assert [finding["viewport"] for finding in found] == [DESKTOP, MOBILE]
    overflows = [finding["evidence"]["measured"]["overflowPx"] for finding in found]
    assert overflows == [200, 1250]
    for finding in found:
        assert finding["check"] == "offscreen-overflow"
        assert finding["category"] == "responsive"
        assert finding["severity"] == "major"
        assert finding["source"] == "Squint heuristic"


async def test_the_first_of_two_elements_on_the_edge_is_the_one_named(
    client: Client,
) -> None:
    await the_finding_on(client, "bug", "#first")


async def test_the_finding_carries_the_widths_the_styles_and_the_message(
    client: Client,
) -> None:
    finding = await the_finding_on(client, "bug", "#first")
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
    assert finding["message"] == (
        "Extends 200px past the 1440px viewport, so the page scrolls horizontally"
    )


async def test_a_parent_on_the_edge_is_named_instead_of_its_child(
    client: Client,
) -> None:
    await the_finding_on(client, "nested", "#parent")


async def test_a_child_past_a_parent_that_fits_is_the_one_named(client: Client) -> None:
    await the_finding_on(client, "child", "#child")


async def test_an_element_1px_short_of_the_edge_is_not_named(client: Client) -> None:
    await the_finding_on(client, "near", "#edge")


async def test_an_element_under_1px_short_of_the_edge_is_named(client: Client) -> None:
    finding = await the_finding_on(client, "fraction", "#fraction")
    assert finding["evidence"]["measured"]["pageWidth"] == 1640
    assert finding["evidence"]["measured"]["overflowPx"] == 200


async def test_a_word_that_cannot_break_names_the_element_that_holds_it(
    client: Client,
) -> None:
    finding = await the_finding_on(client, "word", "#word")
    assert finding["box"]["w"] == 400
    assert finding["evidence"]["measured"] == {
        "overflowPx": 560,
        "pageWidth": 2000,
        "viewportWidth": 1440,
    }


async def test_a_translated_element_is_reported_where_it_is_painted(
    client: Client,
) -> None:
    finding = await the_finding_on(client, "moved", "#moved")
    assert finding["box"]["x"] == 1400
    assert finding["box"]["w"] == 200
    assert finding["evidence"]["measured"]["overflowPx"] == 160


async def test_one_pixel_past_the_viewport_is_reported_and_none_is_not(
    client: Client,
) -> None:
    narrow = {"width": 399, "height": 300}
    exact = {"width": 400, "height": 300}
    (finding,) = await findings(client, "400", viewports=[narrow, exact])
    assert finding["viewport"] == narrow
    assert finding["evidence"]["measured"] == {
        "overflowPx": 1,
        "pageWidth": 400,
        "viewportWidth": 399,
    }


@pytest.mark.parametrize(
    "case",
    [
        "left",
        "fixed",
        "hidden-ancestor",
        "scroll-container",
        "shadow",
        "margin",
        "taller",
    ],
)
async def test_a_page_as_wide_as_the_viewport_is_not_reported(
    client: Client, case: str
) -> None:
    assert await findings(client, f"none-{case}") == []


@pytest.mark.parametrize(
    "case", ["html-hidden", "html-clip", "body-hidden", "body-clip"]
)
async def test_a_page_that_hides_its_horizontal_overflow_is_not_reported(
    client: Client, case: str
) -> None:
    assert await findings(client, case) == []


async def test_a_hidden_overflow_on_body_under_a_scrolling_html_is_reported(
    client: Client,
) -> None:
    finding = await the_finding_on(client, "body-under-html", "body")
    assert finding["evidence"]["measured"]["overflowPx"] == 200


async def test_a_right_to_left_page_is_not_reported(client: Client) -> None:
    assert await findings(client, "rtl") == []


async def test_a_page_widened_by_no_element_is_not_reported(client: Client) -> None:
    assert await findings(client, "pseudo") == []


async def test_naming_the_check_returns_its_finding_alone(client: Client) -> None:
    found = await findings(client, "with-clipped")
    assert [finding["check"] for finding in found] == ["offscreen-overflow"]


async def test_omitting_checks_returns_the_finding_among_the_others(
    client: Client,
) -> None:
    found = (await detect(client, page("with-clipped")))["findings"]
    assert [finding["check"] for finding in found] == [
        "offscreen-overflow",
        "text-clipped",
    ]
    assert [finding["evidence"]["cropIndex"] for finding in found] == [0, 1]


async def test_the_tool_description_names_the_check_and_what_it_reports(
    client: Client,
) -> None:
    (tool,) = [
        tool
        for tool in (await client.list_tools()).tools
        if tool.name == "detect_visual_bugs"
    ]
    assert tool.description is not None
    assert "`offscreen-overflow`" in tool.description
    assert "scroll" in tool.description
