"""The `overlap` Check through `detect_visual_bugs`, against real Chromium."""

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

BUG = fixture_url("overlap-bug.html")
CLEAN = fixture_url("overlap-clean.html")
ONLY = ["overlap"]
# The colour of the covers of the fixtures.
COVER = "#c80000"


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


async def inspect(client: Client, url: str, selector: str) -> dict[str, Any]:
    """What `inspect_element` returns for the one element `selector` matches."""
    arguments = {"url": url, "selector": selector, "viewport": DESKTOP}
    result = await client.call_tool("inspect_element", arguments)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


def painted(inspected: dict[str, Any]) -> dict[str, float]:
    """The share of the box of an inspected element that each of its most
    frequent colours takes."""
    return {color["hex"]: color["share"] for color in inspected["sampledColors"]}


async def test_a_page_of_overlaps_that_are_meant_has_no_findings(
    client: Client,
) -> None:
    result = await call(client, CLEAN)
    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["findings"] == []
    assert images(result) == []
    assert texts(result) == ["No findings in 1 viewport."]


async def clean(client: Client, selector: str) -> tuple[float, list[dict[str, Any]]]:
    """How much of the box of one element of the clean fixture is painted in the
    colour of the covers, and the Findings of the Check on that element."""
    inspected = await inspect(client, CLEAN, selector)
    findings = (await detect(client, CLEAN, checks=ONLY))["findings"]
    on = [finding for finding in findings if finding["box"] == inspected["box"]]
    return painted(inspected).get(COVER, 0), on


async def test_text_under_a_link_stretched_over_its_card_is_not_reported(
    client: Client,
) -> None:
    # Hit testing gives `#card-link` over all of `#stretched`, which would be
    # reported at 100% if what hit testing gives were taken for hidden.
    assert await clean(client, "#stretched") == (0, [])


async def test_text_under_an_element_faded_out_is_not_reported(client: Client) -> None:
    # `#under-faded` would be reported at 50%, covered by `#faded-cover`.
    assert await clean(client, "#under-faded") == (0, [])


async def test_text_mostly_seen_through_a_veil_is_not_reported(client: Client) -> None:
    # `#veil-45` would be reported at 100% if any loss of ink counted as hidden:
    # its glyphs show as a grey of 55 parts of black in 100, but for the seam
    # between two of them.
    assert painted(await inspect(client, CLEAN, "#veil-45"))["#737373"] == 0.6
    assert await clean(client, "#veil-45") == (0, [])


@pytest.mark.parametrize(
    "role", ["menu", "listbox", "tooltip", "dialog", "alertdialog"]
)
async def test_text_under_an_element_of_a_layer_role_is_not_reported(
    client: Client, role: str
) -> None:
    # Each would be reported at 50%, covered by the element of that role.
    assert await clean(client, f"#under-{role}") == (0.5, [])


async def test_text_under_an_open_dialog_element_is_not_reported(
    client: Client,
) -> None:
    # `#under-open-dialog` would be reported at 50%, covered by `#open-dialog`.
    assert await clean(client, "#under-open-dialog") == (0.5, [])


async def test_text_under_an_open_popover_is_not_reported(client: Client) -> None:
    # `#under-popover` would be reported at 50%, covered by `#popover`, which is
    # of `position: absolute`.
    assert await clean(client, "#under-popover") == (0.5, [])


async def test_text_under_a_fixed_element_is_not_reported(client: Client) -> None:
    # `#under-fixed` would be reported at 50%, covered by `#fixed-cover`.
    assert await clean(client, "#under-fixed") == (0.5, [])


async def test_text_under_a_sticky_element_is_not_reported(client: Client) -> None:
    # `#under-sticky` would be reported at 50%, covered by `#sticky-cover`.
    assert await clean(client, "#under-sticky") == (0.5, [])


async def test_text_under_an_element_inside_a_menu_is_not_reported(
    client: Client,
) -> None:
    # `#under-menu-item` would be reported at 50%, covered by `#menu-item`, which
    # has no role of its own.
    assert await clean(client, "#under-menu-item") == (0.5, [])


async def test_text_under_a_static_child_of_a_fixed_element_is_not_reported(
    client: Client,
) -> None:
    # `#under-fixed-child` would be reported at 50%, covered by `#fixed-child`,
    # which is of `position: static`.
    assert await clean(client, "#under-fixed-child") == (0.5, [])


async def test_under_a_tenth_hidden_along_the_width_is_not_reported(
    client: Client,
) -> None:
    # `#nick` is hidden over 19px of its 200px: reported from 20px on.
    assert await clean(client, "#nick") == (0.095, [])


async def test_under_a_tenth_hidden_along_the_height_is_not_reported(
    client: Client,
) -> None:
    # `#skim` is hidden over 1 of its 20 rows, under a cover of 6 rows of the 30 of
    # its line: reported from 2 rows on.
    assert await clean(client, "#skim") == (0.2, [])


async def test_text_under_its_own_descendant_is_not_reported(client: Client) -> None:
    # `#parent-text` would be reported at 50%, covered by `#child-cover`.
    assert await clean(client, "#parent-text") == (0.5, [])


async def test_text_under_a_cover_hit_testing_passes_through_is_not_reported(
    client: Client,
) -> None:
    # `#under-ghost` is 50% hidden by `#ghost-cover`, which no hit test gives: it
    # would be reported with no element to name.
    assert await clean(client, "#under-ghost") == (0.5, [])


async def test_text_over_an_element_without_text_is_not_reported(
    client: Client,
) -> None:
    # The four glyphs of `#caption` are painted over `#picture`: their black is
    # 1440 of the 6000 pixels of its box. Neither would be reported unless boxes
    # that cross were.
    assert painted(await inspect(client, CLEAN, "#picture"))["#000000"] == 0.24
    findings = (await detect(client, CLEAN, checks=ONLY))["findings"]
    assert await findings_on(client, CLEAN, "#caption", findings) == []
    assert await findings_on(client, CLEAN, "#picture", findings) == []


async def test_a_badge_over_a_corner_of_a_box_and_none_of_its_text_is_not_reported(
    client: Client,
) -> None:
    # `#badge` is 224 of the 4200 pixels of the box of `#inbox`, which would be
    # reported if a cover over a box were one over its text.
    assert await clean(client, "#inbox") == (0.0533, [])


async def test_covered_text_that_is_hidden_is_not_reported(client: Client) -> None:
    # `#hidden-text` would be reported at 50% if text nobody sees had ink.
    assert await clean(client, "#hidden-text") == (0.5, [])


async def test_covered_text_painted_transparent_is_not_reported(
    client: Client,
) -> None:
    # `#transparent-text` would be reported at 50%: the Capture measures it as
    # covered, whatever the colour of its glyphs.
    assert await clean(client, "#transparent-text") == (0.5, [])


async def test_covered_text_that_is_faded_out_is_not_reported(client: Client) -> None:
    # `#faded-text` would be reported at 50% if text faded out had ink.
    assert await clean(client, "#faded-text") == (0.5, [])
