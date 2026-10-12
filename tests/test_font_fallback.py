"""The `font-fallback` Check through `detect_visual_bugs`, against real Chromium."""

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

BUG = fixture_url("font-fallback-bug.html")
CLEAN = fixture_url("font-fallback-clean.html")

ONLY = ["font-fallback"]


def family(finding: dict[str, Any]) -> str:
    return finding["evidence"]["measured"]["family"]


async def test_a_family_that_failed_gets_one_finding_on_its_first_element(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert [f["selector"] for f in findings if family(f) == "Brand"] == ["#heading"]
    assert len(await findings_on(client, BUG, "#heading", findings)) == 1
    assert await findings_on(client, BUG, "#lead", findings) == []
    assert await findings_on(client, BUG, "#note", findings) == []


async def test_findings_follow_the_elements_and_count_those_that_fall_back(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert [
        (
            finding["selector"],
            finding["severity"],
            family(finding),
            finding["evidence"]["measured"]["elements"],
        )
        for finding in findings
    ] == [("#heading", "minor", "Brand", 3), ("#icon", "minor", "Icon Set", 1)]


async def test_the_summary_counts_the_two_families(client: Client) -> None:
    result = await call(client, BUG)
    assert texts(result)[0] == "Found 2 findings in 1 viewport: 2 minor."


async def test_two_calls_return_the_same_findings(client: Client) -> None:
    first = await detect(client, BUG, checks=ONLY)
    second = await detect(client, BUG, checks=ONLY)
    assert first["findings"]
    assert first == second


async def test_a_family_named_alone_is_judged_against_the_initial_font(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, BUG, "#icon", findings)
    assert finding["check"] == "font-fallback"
    assert family(finding) == "Icon Set"


async def test_a_text_rendered_at_one_viewport_only_is_reported_there(
    client: Client,
) -> None:
    content = await detect(client, BUG, viewports=[DESKTOP, MOBILE], checks=ONLY)
    assert [
        (finding["viewport"], family(finding))
        for finding in content["findings"]
        if finding["selector"] == "#narrow" or family(finding) == "Narrow Only"
    ] == [(MOBILE, "Narrow Only")]


async def test_the_message_of_one_element_says_element(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, BUG, "#icon", findings)
    assert finding["message"] == (
        'The font "Icon Set" did not load: the text of 1 element is rendered in a '
        "fallback font"
    )


async def test_the_finding_says_which_face_the_element_asked_for(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, BUG, "#heading", findings)
    assert finding == {
        "check": "font-fallback",
        "category": "visual-bug",
        "severity": "minor",
        "message": (
            'The font "Brand" did not load: the text of 3 elements is rendered in a '
            "fallback font"
        ),
        "selector": "#heading",
        "text": "XXXXXXXXXX",
        "box": {"x": 40, "y": 20, "w": 200, "h": 30},
        "viewport": {"width": 1440, "height": 900},
        "evidence": {
            "computed": {
                "font-family": "Brand, Ahem",
                "font-weight": "400",
                "font-style": "normal",
            },
            "measured": {"family": "Brand", "elements": 3, "textWidthPx": 200},
            "cropIndex": 0,
        },
        "suggestion": (
            'Fix the source the page loads "Brand" from, or take the family out of '
            "font-family"
        ),
        "source": "Squint heuristic",
    }


async def test_font_fallback_runs_when_no_check_is_named(client: Client) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert [(finding["selector"], finding["check"]) for finding in findings] == [
        ("#heading", "font-fallback"),
        ("#icon", "font-fallback"),
    ]


async def test_naming_the_other_checks_leaves_this_one_out(client: Client) -> None:
    others = ["low-contrast-real", "offscreen-overflow", "overlap", "text-clipped"]
    assert (await detect(client, BUG, checks=others))["findings"] == []


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


async def test_each_finding_of_the_first_viewport_has_one_in_the_second(
    client: Client,
) -> None:
    content = await detect(client, BUG, viewports=[DESKTOP, MOBILE], checks=ONLY)
    desktop, mobile = (
        {
            (finding["selector"], finding["check"], family(finding))
            for finding in content["findings"]
            if finding["viewport"] == viewport
        }
        for viewport in (DESKTOP, MOBILE)
    )
    assert len(desktop) == 2
    assert desktop <= mobile


async def test_a_page_whose_text_is_in_the_font_it_asks_for_has_no_findings(
    client: Client,
) -> None:
    result = await call(client, CLEAN)
    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["findings"] == []
    assert images(result) == []
    assert texts(result) == ["No findings in 1 viewport."]


async def reported(
    client: Client,
    url: str,
    *,
    families: tuple[str, ...],
    on: tuple[str, ...] = (),
) -> list[tuple[str, str]]:
    """The `(selector, family)` of the Findings of the Check that name one of
    `families` or sit on one of the elements `on`."""
    findings = (await detect(client, url, checks=ONLY))["findings"]
    found = [finding for finding in findings if family(finding) in families]
    for selector in on:
        for finding in await findings_on(client, url, selector, findings):
            if finding not in found:
                found.append(finding)
    return [(finding["selector"], family(finding)) for finding in found]


async def test_a_family_that_is_only_named_is_not_reported(client: Client) -> None:
    families = ("Squint No Such Font",)
    assert await reported(client, CLEAN, families=families, on=("#undeclared",)) == []


async def test_a_failed_family_that_is_not_the_first_of_the_list_is_not_reported(
    client: Client,
) -> None:
    families = ("Second Choice",)
    assert await reported(client, CLEAN, families=families, on=("#second",)) == []


async def test_a_failed_family_no_element_asks_for_is_not_reported(
    client: Client,
) -> None:
    assert await reported(client, CLEAN, families=("Preloaded",)) == []


async def test_a_failed_family_only_hidden_text_asks_for_is_not_reported(
    client: Client,
) -> None:
    families = ("Hidden Brand",)
    assert await reported(client, CLEAN, families=families, on=("#hidden",)) == []


async def test_a_failed_family_only_a_pseudo_element_asks_for_is_not_reported(
    client: Client,
) -> None:
    families = ("Pseudo Brand",)
    assert await reported(client, CLEAN, families=families, on=("#pseudo",)) == []


async def test_a_family_whose_faces_were_never_needed_is_not_reported(
    client: Client,
) -> None:
    # `#none` and `#blank` paint no box to find them by: their families stand
    # for them.
    families = ("Unused", "After Generic", "Never Shown", "Blank")
    on = ("#after-generic",)
    assert await reported(client, CLEAN, families=families, on=on) == []
