"""The `overlap` Check through `detect_visual_bugs`, against real Chromium."""

from typing import Any

import pytest
from helpers import DESKTOP, MOBILE, call, detect, findings_on, fixture_url, texts
from mcp import Client

pytestmark = pytest.mark.anyio

BUG = fixture_url("overlap-bug.html")
ONLY = ["overlap"]


def covered(findings: list[dict[str, Any]]) -> list[tuple[str, str, int, str]]:
    """What each Finding says of its text: which one, how bad, how much of it is
    hidden and by which element."""
    return [
        (
            finding["selector"],
            finding["severity"],
            finding["evidence"]["measured"]["hiddenPercent"],
            finding["evidence"]["measured"]["coveredBy"],
        )
        for finding in findings
    ]


async def finding_on(client: Client, url: str, selector: str) -> dict[str, Any]:
    """The one Finding of the Check on the element `selector` matches."""
    findings = (await detect(client, url, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, url, selector, findings)
    return finding


async def test_each_covered_text_yields_one_finding(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    for selector in ("#half", "#corner", "#quarter", "#collision"):
        (finding,) = await findings_on(client, BUG, selector, findings)
        assert finding["check"] == "overlap"
    assert len(findings) == 4


async def test_the_findings_say_how_much_is_hidden_and_by_what_in_order(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    # `#corner` stands before `#quarter` in the document and after it here.
    assert covered(findings) == [
        ("#half", "major", 50, "#half-cover"),
        ("#quarter", "major", 25, "#quarter-cover"),
        ("#corner", "minor", 10, "#corner-cover"),
        ("#collision", "minor", 20, "#stray"),
    ]


async def test_the_summary_counts_the_findings_of_the_bug_fixture(
    client: Client,
) -> None:
    result = await call(client, BUG)
    assert texts(result)[0] == "Found 4 findings in 1 viewport: 2 major, 2 minor."


async def test_the_same_call_returns_the_same_content(client: Client) -> None:
    assert await detect(client, BUG) == await detect(client, BUG)


async def test_text_under_the_text_of_another_element_is_reported(
    client: Client,
) -> None:
    finding = await finding_on(client, BUG, "#collision")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 20


async def test_the_text_on_top_of_another_is_not_reported(client: Client) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert await findings_on(client, BUG, "#stray", findings) == []


async def test_a_text_covered_at_one_viewport_only_is_reported_there(
    client: Client,
) -> None:
    content = await detect(client, BUG, viewports=[DESKTOP, MOBILE], checks=ONLY)
    findings = content["findings"]
    assert await findings_on(client, BUG, "#narrow", findings, DESKTOP) == []
    (finding,) = await findings_on(client, BUG, "#narrow", findings, MOBILE)
    assert finding["selector"] == "#narrow"
    assert finding["viewport"] == MOBILE


async def test_the_finding_carries_the_share_the_coverer_and_the_styles(
    client: Client,
) -> None:
    findings = (await detect(client, BUG, checks=ONLY))["findings"]
    assert findings[0] == {
        "check": "overlap",
        "category": "visual-bug",
        "severity": "major",
        "message": "50% of the text is covered by another element",
        "selector": "#half",
        "text": "XXXXXXXXXX",
        "box": {"x": 40, "y": 20, "w": 200, "h": 30},
        "viewport": {"width": 1440, "height": 900},
        "evidence": {
            "computed": {"position": "static", "z-index": "auto"},
            "measured": {"hiddenPercent": 50, "coveredBy": "#half-cover"},
            "cropIndex": 0,
        },
        "suggestion": "Move one of the two elements or give the text its own space",
        "source": "Squint heuristic",
    }


async def test_the_message_states_the_hidden_share(client: Client) -> None:
    finding = await finding_on(client, BUG, "#corner")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 10
    assert finding["message"] == "10% of the text is covered by another element"


async def test_overlap_runs_when_no_check_is_named(client: Client) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert [(finding["selector"], finding["check"]) for finding in findings] == [
        ("#half", "overlap"),
        ("#quarter", "overlap"),
        ("#corner", "overlap"),
        ("#collision", "overlap"),
    ]


async def test_naming_the_other_checks_leaves_this_one_out(client: Client) -> None:
    others = ["low-contrast-real", "offscreen-overflow", "text-clipped"]
    assert (await detect(client, BUG, checks=others))["findings"] == []


async def test_the_tool_description_says_what_overlap_reports(client: Client) -> None:
    tools = (await client.list_tools()).tools
    (tool,) = (tool for tool in tools if tool.name == "detect_visual_bugs")
    assert tool.description is not None
    assert "`overlap` (text another element is painted over" in " ".join(
        tool.description.split()
    )


async def test_each_finding_of_the_first_viewport_has_one_in_the_second(
    client: Client,
) -> None:
    content = await detect(client, BUG, viewports=[DESKTOP, MOBILE], checks=ONLY)
    desktop, mobile = (
        {
            (finding["selector"], finding["check"])
            for finding in content["findings"]
            if finding["viewport"] == viewport
        }
        for viewport in (DESKTOP, MOBILE)
    )
    assert len(desktop) == 4
    assert desktop <= mobile
