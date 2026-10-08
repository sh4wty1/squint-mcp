"""The `low-contrast-real` Check through `detect_visual_bugs`, against real Chromium."""

from typing import Any

import pytest
from helpers import (
    DESKTOP,
    MOBILE,
    call,
    detect,
    findings_on,
    fixture_url,
    images,
    texts,
)
from mcp import Client

pytestmark = pytest.mark.anyio

BUG = fixture_url("low-contrast-bug.html")
CLEAN = fixture_url("low-contrast-clean.html")
HERO = '[data-testid="hero"]'
ONLY = ["low-contrast-real"]


async def finding_on(client: Client, url: str, selector: str) -> dict[str, Any]:
    """The one Finding of the Check on the element `selector` matches."""
    findings = (await detect(client, url, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, url, selector, findings)
    return finding


async def test_each_text_below_its_ratio_yields_one_finding(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    for selector in ("#flat", "#alpha", HERO, "#almost-large"):
        (finding,) = await findings_on(client, BUG, selector, findings)
        assert finding["check"] == "low-contrast-real"
    assert len(findings) == 4


async def test_text_over_a_gradient_is_judged_on_the_painted_band(
    client: Client,
) -> None:
    first = (await detect(client, BUG, checks=ONLY))["findings"][0]
    assert first["selector"] == HERO
    assert first["severity"] == "major"
    assert first["evidence"]["measured"]["contrastRatio"] == 1.6
    assert first["evidence"]["measured"]["sampledBackground"] == "#cccccc"
    assert first["evidence"]["computed"]["background-color"] == "rgb(0, 0, 0)"


async def test_the_colours_reported_are_those_of_the_worst_part(
    client: Client,
) -> None:
    measured = (await finding_on(client, BUG, HERO))["evidence"]["measured"]
    assert measured["textColor"] == "#ffffff"
    assert measured["sampledBackground"] == "#cccccc"


async def test_the_summary_counts_the_findings_of_the_bug_fixture(
    client: Client,
) -> None:
    result = await call(client, BUG)
    assert texts(result)[0] == "Found 4 findings in 1 viewport: 1 major, 3 minor."


async def test_the_same_call_returns_the_same_content(client: Client) -> None:
    assert await detect(client, BUG) == await detect(client, BUG)


async def test_grey_text_under_the_ratio_on_a_flat_white_is_minor(
    client: Client,
) -> None:
    assert (await finding_on(client, BUG, "#flat"))["severity"] == "minor"


async def test_a_translucent_colour_is_judged_as_seen_over_its_background(
    client: Client,
) -> None:
    measured = (await finding_on(client, BUG, "#alpha"))["evidence"]["measured"]
    assert measured["textColor"] == "#808080"
    assert measured["contrastRatio"] == 3.94


async def test_the_finding_carries_the_ratio_the_threshold_and_both_colours(
    client: Client,
) -> None:
    assert await finding_on(client, BUG, "#flat") == {
        "check": "low-contrast-real",
        "category": "a11y",
        "severity": "minor",
        "message": (
            "Text contrast 4.47:1 against the painted background #ffffff "
            "is below the 4.5:1 minimum"
        ),
        "selector": "#flat",
        "text": "XXXXXXXXXX",
        "box": {"x": 40, "y": 20, "w": 200, "h": 30},
        "viewport": {"width": 1440, "height": 900},
        "evidence": {
            "computed": {
                "color": "rgb(119, 119, 119)",
                "background-color": "rgba(0, 0, 0, 0)",
                "background-image": "none",
                "font-size": "20px",
                "font-weight": "400",
            },
            "measured": {
                "contrastRatio": 4.47,
                "requiredRatio": 4.5,
                "textColor": "#777777",
                "sampledBackground": "#ffffff",
            },
            "cropIndex": 1,
        },
        "suggestion": (
            "Change the text colour or put a solid background behind the text "
            "to reach 4.5:1"
        ),
        "source": "WCAG 2.2 SC 1.4.3",
    }


async def test_text_just_under_the_large_size_needs_the_full_ratio(
    client: Client,
) -> None:
    finding = await finding_on(client, BUG, "#almost-large")
    assert finding["evidence"]["measured"]["requiredRatio"] == 4.5
    assert finding["severity"] == "minor"


async def test_a_finding_selector_works_in_inspect_element(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert len(findings) == 4
    for finding in findings:
        arguments = {"url": BUG, "selector": finding["selector"], "viewport": DESKTOP}
        result = await client.call_tool("inspect_element", arguments)
        assert result.is_error is False, texts(result)
        assert result.structured_content is not None
        assert result.structured_content["box"] == finding["box"]


async def test_each_viewport_gets_the_same_findings(client: Client) -> None:
    findings = (await detect(client, BUG, viewports=[DESKTOP, MOBILE]))["findings"]
    per_viewport = [
        {(f["selector"], f["check"]) for f in findings if f["viewport"] == viewport}
        for viewport in (DESKTOP, MOBILE)
    ]
    assert len(per_viewport[0]) == 4
    assert per_viewport[0] == per_viewport[1]


async def test_a_page_with_adequate_contrast_has_no_findings(client: Client) -> None:
    result = await call(client, CLEAN)
    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["findings"] == []
    assert images(result) == []
    assert texts(result) == ["No findings in 1 viewport."]


async def reported(client: Client, selector: str) -> list[dict[str, Any]]:
    """The Findings of the Check on one element of the clean fixture."""
    findings = (await detect(client, CLEAN, checks=ONLY))["findings"]
    return await findings_on(client, CLEAN, selector, findings)


async def test_grey_text_over_the_ratio_is_not_reported(client: Client) -> None:
    assert await reported(client, "#flat") == []


async def test_text_readable_over_its_gradient_is_not_reported(client: Client) -> None:
    assert await reported(client, "#gradient") == []


async def test_text_of_24px_needs_only_the_large_ratio(client: Client) -> None:
    assert await reported(client, "#large") == []


async def test_bold_text_of_18_66px_needs_only_the_large_ratio(client: Client) -> None:
    assert await reported(client, "#large-bold") == []


async def test_clipped_black_text_has_no_contrast_finding(client: Client) -> None:
    url = fixture_url("text-clipped-bug.html")
    assert (await detect(client, url, checks=ONLY))["findings"] == []


async def test_both_checks_run_when_none_is_named(client: Client) -> None:
    contrast = (await detect(client, BUG))["findings"]
    clipped = (await detect(client, fixture_url("text-clipped-bug.html")))["findings"]
    assert {finding["check"] for finding in contrast} == {"low-contrast-real"}
    assert {finding["check"] for finding in clipped} == {"text-clipped"}


async def test_naming_the_other_check_leaves_this_one_out(client: Client) -> None:
    assert (await detect(client, BUG, checks=["text-clipped"]))["findings"] == []


async def test_the_tool_description_names_both_checks(client: Client) -> None:
    tools = (await client.list_tools()).tools
    (tool,) = (tool for tool in tools if tool.name == "detect_visual_bugs")
    assert tool.description is not None
    assert "`text-clipped`" in tool.description
    assert "`low-contrast-real`" in tool.description
