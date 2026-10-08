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
BOUNDS = fixture_url("low-contrast-bounds.html")
CLEAN = fixture_url("low-contrast-clean.html")
REACH = fixture_url("low-contrast-reach.html")
FILL = fixture_url("low-contrast-fill.html")
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
                "-webkit-text-fill-color": "rgb(119, 119, 119)",
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
    for url, count in ((BUG, 4), (BOUNDS, 8)):
        findings = (await detect(client, url, checks=ONLY))["findings"]
        assert len(findings) == count
        for finding in findings:
            arguments = {
                "url": url,
                "selector": finding["selector"],
                "viewport": DESKTOP,
            }
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


async def bounds(client: Client, selector: str) -> list[dict[str, Any]]:
    """The Findings of the Check on one element of the bounds fixture."""
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    return await findings_on(client, BOUNDS, selector, findings)


async def test_only_the_low_contrast_texts_of_the_bounds_fixture_are_reported(
    client: Client,
) -> None:
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert sorted(finding["selector"] for finding in findings) == [
        "#below-floor",
        "#bottom",
        "#large-low",
        "#nested-child",
        "#right",
        "#same",
        "#semibold",
        "#small-bold",
    ]


async def test_a_tenth_of_the_text_at_its_right_edge_is_enough(client: Client) -> None:
    (finding,) = await bounds(client, "#right")
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6


async def test_a_tenth_of_the_text_at_its_bottom_edge_is_enough(client: Client) -> None:
    (finding,) = await bounds(client, "#bottom")
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6


async def test_under_a_tenth_of_the_text_at_its_left_edge_is_not_reported(
    client: Client,
) -> None:
    assert await bounds(client, "#left") == []


async def test_under_a_tenth_of_the_text_at_its_top_edge_is_not_reported(
    client: Client,
) -> None:
    assert await bounds(client, "#top") == []


async def test_text_of_the_colour_of_its_background_is_major(client: Client) -> None:
    (finding,) = await bounds(client, "#same")
    assert finding["severity"] == "major"
    assert finding["evidence"]["measured"]["contrastRatio"] == 1


async def test_each_element_is_judged_on_its_own_text(client: Client) -> None:
    assert await bounds(client, "#nested") == []
    assert len(await bounds(client, "#nested-child")) == 1


async def test_hidden_text_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#hidden") == []


async def test_transparent_text_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#transparent") == []


async def test_faded_text_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#faded") == []


async def test_text_of_a_faded_ancestor_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#faded-child") == []


async def test_text_clipped_away_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#clipped-away") == []


async def test_covered_text_is_not_reported(client: Client) -> None:
    assert await bounds(client, "#covered") == []


async def test_a_band_behind_the_clipped_part_of_a_text_is_not_reported(
    client: Client,
) -> None:
    assert await bounds(client, "#clipped-part") == []


async def test_text_without_a_box_is_not_reported(client: Client) -> None:
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert "#no-box" not in [finding["selector"] for finding in findings]
    assert len(findings) == 8


async def test_bold_text_of_18px_needs_the_full_ratio(client: Client) -> None:
    (finding,) = await bounds(client, "#small-bold")
    assert finding["evidence"]["measured"]["requiredRatio"] == 4.5


async def test_semibold_text_of_20px_needs_the_full_ratio(client: Client) -> None:
    (finding,) = await bounds(client, "#semibold")
    assert finding["evidence"]["measured"]["requiredRatio"] == 4.5


async def test_large_text_under_3_to_1_is_major(client: Client) -> None:
    (finding,) = await bounds(client, "#large-low")
    assert finding["evidence"]["measured"]["requiredRatio"] == 3
    assert finding["severity"] == "major"


async def test_the_message_and_the_suggestion_name_the_large_ratio(
    client: Client,
) -> None:
    (finding,) = await bounds(client, "#large-low")
    assert finding["message"] == (
        "Text contrast 2.84:1 against the painted background #ffffff "
        "is below the 3:1 minimum"
    )
    assert finding["suggestion"].endswith("to reach 3:1")


async def test_a_ratio_under_3_is_major_and_one_from_3_up_is_minor(
    client: Client,
) -> None:
    (below,) = await bounds(client, "#below-floor")
    assert below["evidence"]["measured"]["contrastRatio"] == 2.99
    assert below["severity"] == "major"
    above = await finding_on(client, BUG, "#almost-large")
    assert above["evidence"]["measured"]["contrastRatio"] == 3.03
    assert above["severity"] == "minor"


async def reach(client: Client, selector: str) -> list[dict[str, Any]]:
    """The Findings of the Check on one element of the reach fixture."""
    findings = (await detect(client, REACH, checks=ONLY))["findings"]
    return await findings_on(client, REACH, selector, findings)


async def test_only_five_texts_of_the_reach_fixture_are_reported(
    client: Client,
) -> None:
    findings = (await detect(client, REACH, checks=ONLY))["findings"]
    assert sorted(finding["selector"] for finding in findings) == [
        "#in-plain",
        "#split",
        "#three-lines",
        "#two-lines",
        "#veiled-little",
    ]


async def test_a_parent_is_not_judged_on_the_text_of_its_child(client: Client) -> None:
    assert await reach(client, "#parent") == []
    assert await reach(client, "#badge") == []


async def test_every_line_of_a_text_is_judged(client: Client) -> None:
    (finding,) = await reach(client, "#two-lines")
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6
    assert finding["evidence"]["measured"]["sampledBackground"] == "#cccccc"


async def test_a_line_between_two_others_is_judged(client: Client) -> None:
    (finding,) = await reach(client, "#three-lines")
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6


async def test_every_text_node_of_an_element_is_judged(client: Client) -> None:
    (finding,) = await reach(client, "#split")
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6


async def test_text_mostly_hidden_by_a_translucent_layer_is_not_reported(
    client: Client,
) -> None:
    assert await reach(client, "#veiled-most") == []


async def test_text_mostly_seen_through_a_translucent_layer_is_reported(
    client: Client,
) -> None:
    (finding,) = await reach(client, "#veiled-little")
    assert finding["evidence"]["measured"]["textColor"] == "#777777"
    assert finding["evidence"]["measured"]["contrastRatio"] == 4.47


async def test_text_in_a_shadow_tree_is_judged(client: Client) -> None:
    (finding,) = await reach(client, "#in-plain")
    assert finding["evidence"]["measured"]["contrastRatio"] == 4.47


async def test_text_in_the_shadow_tree_of_a_faded_host_is_not_reported(
    client: Client,
) -> None:
    assert await reach(client, "#in-faded") == []


async def test_slotted_text_under_a_faded_element_of_the_shadow_tree_is_not_reported(
    client: Client,
) -> None:
    assert await reach(client, "#slotted") == []


async def test_text_off_the_page_is_not_reported(client: Client) -> None:
    findings = (await detect(client, REACH, checks=ONLY))["findings"]
    assert "#off-page" not in [finding["selector"] for finding in findings]
    assert len(findings) == 5


async def fill(client: Client, selector: str) -> list[dict[str, Any]]:
    """The Findings of the Check on one element of the fill fixture."""
    findings = (await detect(client, FILL, checks=ONLY))["findings"]
    return await findings_on(client, FILL, selector, findings)


async def test_text_filled_with_a_readable_colour_is_not_reported(
    client: Client,
) -> None:
    assert await fill(client, "#fill-dark") == []


async def test_text_is_judged_on_the_fill_that_paints_its_glyphs(
    client: Client,
) -> None:
    (finding,) = await fill(client, "#fill-light")
    assert finding["severity"] == "major"
    assert finding["evidence"]["measured"]["contrastRatio"] == 1.6
    assert finding["evidence"]["measured"]["textColor"] == "#cccccc"


async def test_the_finding_carries_the_fill_next_to_the_colour(client: Client) -> None:
    (finding,) = await fill(client, "#fill-light")
    assert finding["evidence"]["computed"]["color"] == "rgb(0, 0, 0)"
    assert (
        finding["evidence"]["computed"]["-webkit-text-fill-color"]
        == "rgb(204, 204, 204)"
    )


async def test_gradient_text_is_not_reported(client: Client) -> None:
    assert await fill(client, "#gradient-text") == []
