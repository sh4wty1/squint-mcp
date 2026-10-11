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
BOUNDS = fixture_url("overlap-bounds.html")
ORDER = fixture_url("overlap-order.html")
MANY = fixture_url("overlap-many.html")
SCROLLED = fixture_url("overlap-scrolled.html")
ONLY = ["overlap"]
# The colour of the covers of the fixtures.
COVER = "#c80000"
# A text and its cover in one open shadow tree of the bounds fixture.
SHADOW_TEXT = '[data-testid="shadow-text"]'
SHADOW_COVER = '[data-testid="shadow-cover"]'


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


async def test_text_under_a_role_written_with_spaces_and_a_capital_is_not_reported(
    client: Client,
) -> None:
    # `#under-spaced-role` would be reported at 50%, covered by `#spaced-role`, if
    # its `role` of " Menu " were compared as it is written.
    assert await clean(client, "#under-spaced-role") == (0.5, [])


async def test_text_under_what_one_of_its_ancestors_paints_is_not_reported(
    client: Client,
) -> None:
    # `#under-own-row` is 50% hidden by the `::after` of `#decorated-row`, which
    # is what hit testing gives there: it would be reported, covered by its row.
    assert await clean(client, "#under-own-row") == (0.5, [])


async def test_text_whose_own_descendant_is_what_hit_testing_gives_is_not_reported(
    client: Client,
) -> None:
    # `#own-link-text` is 50% hidden by `#linked-cover`, and hit testing gives
    # `#own-link` there, above the cover: it would be reported, covered by its
    # own link.
    assert await clean(client, "#own-link-text") == (0.5, [])


async def test_covered_text_faded_to_under_half_of_its_ink_is_not_reported(
    client: Client,
) -> None:
    # `#opacity-40` would be reported at 50% if ink fainter than half made text.
    assert await clean(client, "#opacity-40") == (0.5, [])


async def bounds(client: Client, selector: str) -> dict[str, Any]:
    """The one Finding of the Check on one element of the bounds fixture."""
    return await finding_on(client, BOUNDS, selector)


async def test_only_the_covered_texts_of_the_bounds_fixture_are_reported(
    client: Client,
) -> None:
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert sorted(finding["selector"] for finding in findings) == [
        "#almost-quarter",
        "#bottom",
        "#in-dialog",
        "#in-fixed",
        "#label",
        "#layer-ancestor",
        "#layered-corner",
        "#layered-half",
        "#left",
        "#mixed",
        "#opacity-60",
        "#shared-layer",
        "#split",
        "#three-lines",
        "#tie",
        "#top",
        "#two-covers",
        "#under-label",
        "#under-role-list",
        "#veil-55",
        "#z-static",
        "#z-zero",
        SHADOW_TEXT,
    ]


@pytest.mark.parametrize("selector", ["#left", "#top", "#bottom"])
async def test_a_tenth_of_the_text_hidden_at_one_of_its_edges_is_enough(
    client: Client, selector: str
) -> None:
    finding = await bounds(client, selector)
    assert finding["evidence"]["measured"]["hiddenPercent"] == 10


async def test_a_line_between_two_others_is_measured(client: Client) -> None:
    finding = await bounds(client, "#three-lines")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 10


async def test_every_text_node_of_an_element_is_measured(client: Client) -> None:
    finding = await bounds(client, "#split")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 10


async def test_text_mostly_hidden_by_a_veil_is_hidden_whole(client: Client) -> None:
    finding = await bounds(client, "#veil-55")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 100
    assert finding["severity"] == "major"


async def test_text_covered_inside_its_shadow_tree_names_the_cover_of_that_tree(
    client: Client,
) -> None:
    finding = await bounds(client, SHADOW_TEXT)
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 50,
        "coveredBy": SHADOW_COVER,
    }


async def test_text_covered_by_its_neighbour_inside_one_dialog_is_reported(
    client: Client,
) -> None:
    assert (await bounds(client, "#in-dialog"))["severity"] == "major"


async def test_text_covered_by_its_neighbour_inside_one_fixed_element_is_reported(
    client: Client,
) -> None:
    assert (await bounds(client, "#in-fixed"))["severity"] == "major"


async def test_text_under_an_element_in_the_shadow_tree_of_a_menu_is_not_reported(
    client: Client,
) -> None:
    # `#under-shadow-menu` would be reported at 50%, covered by an element whose
    # only ancestor of a layer role is the host of its tree.
    inspected = await inspect(client, BOUNDS, "#under-shadow-menu")
    assert painted(inspected)[COVER] == 0.5
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert [f for f in findings if f["box"] == inspected["box"]] == []


async def test_a_quarter_hidden_is_major_and_just_under_it_is_minor(
    client: Client,
) -> None:
    quarter = await finding_on(client, BUG, "#quarter")
    assert quarter["evidence"]["measured"]["hiddenPercent"] == 25
    assert quarter["severity"] == "major"
    almost = await bounds(client, "#almost-quarter")
    assert almost["severity"] == "minor"


async def test_the_hidden_share_is_truncated_to_whole_percents(client: Client) -> None:
    # 49px of 200px: 24.5%.
    finding = await bounds(client, "#almost-quarter")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 24
    assert finding["message"] == "24% of the text is covered by another element"


def share_and_severity(finding: dict[str, Any]) -> tuple[int, str]:
    return finding["evidence"]["measured"]["hiddenPercent"], finding["severity"]


async def test_half_hidden_by_a_positioned_cover_with_a_z_index_is_minor(
    client: Client,
) -> None:
    assert share_and_severity(await bounds(client, "#layered-half")) == (50, "minor")


async def test_a_tenth_hidden_by_a_positioned_cover_with_a_z_index_is_info(
    client: Client,
) -> None:
    assert share_and_severity(await bounds(client, "#layered-corner")) == (10, "info")


async def test_a_cover_inside_a_positioned_element_with_a_z_index_is_one_level_lower(
    client: Client,
) -> None:
    finding = await bounds(client, "#layer-ancestor")
    assert finding["evidence"]["measured"]["coveredBy"] == "#layer-cover"
    assert share_and_severity(finding) == (50, "minor")


async def test_a_z_index_on_an_ancestor_of_both_does_not_lower_the_severity(
    client: Client,
) -> None:
    assert share_and_severity(await bounds(client, "#shared-layer")) == (50, "major")


async def test_a_z_index_of_zero_does_not_lower_the_severity(client: Client) -> None:
    assert share_and_severity(await bounds(client, "#z-zero")) == (50, "major")


async def test_a_z_index_on_a_static_cover_does_not_lower_the_severity(
    client: Client,
) -> None:
    finding = await bounds(client, "#z-static")
    assert finding["evidence"]["measured"]["coveredBy"] == "#z-static-next"
    assert share_and_severity(finding) == (50, "major")


async def test_what_a_silent_layer_hides_is_left_out_of_the_share_and_the_coverer(
    client: Client,
) -> None:
    # `#mixed-menu` lies over 100px of the text and `#mixed-card` over 40px.
    finding = await bounds(client, "#mixed")
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 20,
        "coveredBy": "#mixed-card",
    }
    assert finding["severity"] == "minor"


async def test_the_cover_over_most_of_the_hidden_ink_is_the_one_named(
    client: Client,
) -> None:
    # `#small-cover` comes first in the document and hides half as much.
    finding = await bounds(client, "#two-covers")
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 60,
        "coveredBy": "#large-cover",
    }


async def test_of_two_covers_that_hide_as_much_the_first_in_the_document_is_named(
    client: Client,
) -> None:
    # `#tie-first` is over the end of the text: a scan from the left meets
    # `#tie-second` first.
    finding = await bounds(client, "#tie")
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 40,
        "coveredBy": "#tie-first",
    }


async def test_text_under_an_element_with_a_list_of_roles_is_reported(
    client: Client,
) -> None:
    # `#role-list` has a `role` of "menu navigation": it would hide
    # `#under-role-list` unreported if one role of a list made a layer.
    finding = await bounds(client, "#under-role-list")
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 50,
        "coveredBy": "#role-list",
    }
    assert finding["severity"] == "major"


async def test_covered_text_that_keeps_over_half_of_its_ink_is_reported(
    client: Client,
) -> None:
    # `#opacity-60` shows 60 parts in 100 of its ink: text, where 40 are not.
    finding = await bounds(client, "#opacity-60")
    assert finding["evidence"]["measured"]["hiddenPercent"] == 50


async def test_two_covered_texts_painted_over_each_other_are_each_measured(
    client: Client,
) -> None:
    # `#label` hides half of `#under-label`, and `#label-cover` one of the two
    # glyphs of `#label`: neither share is exact unless each text is told from
    # the other, in the pixels of the page and when it is painted alone.
    under = await bounds(client, "#under-label")
    assert under["evidence"]["measured"] == {
        "hiddenPercent": 50,
        "coveredBy": "#label",
    }
    label = await bounds(client, "#label")
    assert label["evidence"]["measured"] == {
        "hiddenPercent": 50,
        "coveredBy": "#label-cover",
    }


async def test_the_selectors_of_a_finding_work_in_inspect_element(
    client: Client,
) -> None:
    for url, count in ((BUG, 4), (BOUNDS, 23)):
        findings = (await detect(client, url, checks=ONLY))["findings"]
        assert len(findings) == count
        for finding in findings:
            inspected = await inspect(client, url, finding["selector"])
            assert inspected["box"] == finding["box"]
            # `inspect` fails on a selector that does not match one element.
            await inspect(client, url, finding["evidence"]["measured"]["coveredBy"])


async def test_text_under_an_opaque_cover_of_an_earlier_fixture_is_reported(
    client: Client,
) -> None:
    url = fixture_url("low-contrast-bounds.html")
    (finding,) = (await detect(client, url, checks=ONLY))["findings"]
    assert finding["selector"] == "#covered"
    assert finding["evidence"]["measured"]["hiddenPercent"] == 100
    assert finding["severity"] == "major"


async def test_text_under_a_veil_of_an_earlier_fixture_is_reported(
    client: Client,
) -> None:
    url = fixture_url("low-contrast-reach.html")
    (finding,) = (await detect(client, url, checks=ONLY))["findings"]
    assert finding["selector"] == "#veiled-most"
    assert finding["evidence"]["measured"]["hiddenPercent"] == 100


async def test_an_element_behind_the_clipped_part_of_a_text_does_not_cover_it(
    client: Client,
) -> None:
    # `#backdrop` lies where the text of `#in-scaled` would go on if its parent
    # did not cut it off.
    url = fixture_url("text-clipped-clean.html")
    assert (await detect(client, url, checks=ONLY))["findings"] == []


async def test_findings_of_overlap_and_another_check_come_in_document_order(
    client: Client,
) -> None:
    findings = (await detect(client, ORDER))["findings"]
    assert {finding["severity"] for finding in findings} == {"minor"}
    assert [(finding["selector"], finding["check"]) for finding in findings] == [
        ("#a", "overlap"),
        ("#b", "low-contrast-real"),
        ("#b", "overlap"),
        ("#c", "overlap"),
    ]


async def test_a_page_of_a_hundred_covered_texts_is_checked(client: Client) -> None:
    result = await call(client, MANY, checks=ONLY)
    assert result.is_error is False
    assert result.structured_content is not None
    findings = result.structured_content["findings"]
    assert len(findings) == 100
    # More hidden pixels than are hit tested: each text still names its own cover.
    assert covered(findings) == [
        (f"#text-{place}", "major", 50, f"#cover-{place}") for place in range(100)
    ]


async def test_an_element_the_scroll_brings_over_a_text_is_not_what_covers_it(
    client: Client,
) -> None:
    # Hit testing scrolls the page 900px to reach `#far`, which brings
    # `#fixed-bar` over the half of it that `#far-cover` hides.
    (finding,) = (await detect(client, SCROLLED, checks=ONLY))["findings"]
    assert finding["selector"] == "#far"
    assert finding["evidence"]["measured"] == {
        "hiddenPercent": 50,
        "coveredBy": "#far-cover",
    }
