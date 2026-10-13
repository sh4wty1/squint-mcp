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
BOUNDS = fixture_url("font-fallback-bounds.html")
SHAPING = fixture_url("font-fallback-shaping.html")
MONOSPACE = fixture_url("font-fallback-monospace.html")
ORDER = fixture_url("font-fallback-order.html")
MANY = fixture_url("font-fallback-many.html")
JUDGED = fixture_url("font-fallback-judged.html")
NAMES = fixture_url("font-fallback-names.html")

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


def elements(finding: dict[str, Any]) -> int:
    return finding["evidence"]["measured"]["elements"]


async def of_family(client: Client, url: str, name: str) -> dict[str, Any]:
    """The one Finding of the Check for the family `name`."""
    findings = (await detect(client, url, checks=ONLY))["findings"]
    (finding,) = (finding for finding in findings if family(finding) == name)
    return finding


async def sits_on(client: Client, url: str, selector: str) -> dict[str, Any]:
    """The one Finding of the Check on the element `selector` matches."""
    findings = (await detect(client, url, checks=ONLY))["findings"]
    (finding,) = await findings_on(client, url, selector, findings)
    return finding


async def test_the_findings_of_the_bounds_follow_the_elements(client: Client) -> None:
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert [
        (finding["selector"], family(finding), elements(finding))
        for finding in findings
    ] == [
        ("#half-bold", "Half", 1),
        ("#mixed-lower", "Mixed", 1),
        ("#lower", "Missing Brand", 2),
        ("#scripted", "Scripted", 1),
        ("#seen", "Veiled Brand", 1),
        ("#shown", "Unshown Brand", 1),
        ("#own-parent", "Parent Brand", 1),
        ("#fallen-child", "Child Brand", 1),
        ("#long", "Long Brand", 1),
        ("#split", "Split Brand", 1),
        ("#twice-normal", "Twice", 2),
        ('[data-testid="shadow-text"]', "Shadow Brand", 2),
    ]
    assert [finding["severity"] for finding in findings] == ["minor"] * 12


async def test_a_face_a_script_added_is_reported_when_it_failed(
    client: Client,
) -> None:
    finding = await sits_on(client, BOUNDS, "#scripted")
    assert family(finding) == "Scripted"
    assert await of_family(client, BOUNDS, "Scripted") == finding


async def test_a_family_written_in_another_case_is_one_family(client: Client) -> None:
    finding = await of_family(client, BOUNDS, "Missing Brand")
    assert finding == await sits_on(client, BOUNDS, "#lower")
    assert elements(finding) == 2


async def test_an_element_that_asks_for_the_face_that_failed_is_reported(
    client: Client,
) -> None:
    finding = await sits_on(client, BOUNDS, "#half-bold")
    assert (family(finding), elements(finding)) == ("Half", 1)
    assert await of_family(client, BOUNDS, "Half") == finding


async def test_a_text_all_in_the_range_of_the_face_that_failed_is_reported(
    client: Client,
) -> None:
    finding = await sits_on(client, BOUNDS, "#mixed-lower")
    assert (family(finding), elements(finding)) == ("Mixed", 1)
    assert await of_family(client, BOUNDS, "Mixed") == finding


async def test_a_text_in_a_shadow_tree_is_reported_with_the_family_of_the_document(
    client: Client,
) -> None:
    finding = await of_family(client, BOUNDS, "Shadow Brand")
    assert finding["selector"] == '[data-testid="shadow-text"]'
    assert elements(finding) == 2
    assert await sits_on(client, BOUNDS, '[data-testid="shadow-text"]') == finding


async def test_the_family_is_named_as_its_face_has_it(client: Client) -> None:
    finding = await sits_on(client, BOUNDS, "#lower")
    assert family(finding) == "Missing Brand"
    assert finding["evidence"]["computed"]["font-family"] == '"missing brand", Ahem'


async def test_a_family_whose_faces_all_failed_gets_one_finding(
    client: Client,
) -> None:
    finding = await of_family(client, BOUNDS, "Twice")
    assert finding == await sits_on(client, BOUNDS, "#twice-normal")
    assert elements(finding) == 2
    findings = (await detect(client, BOUNDS, checks=ONLY))["findings"]
    assert await findings_on(client, BOUNDS, "#twice-bold", findings) == []


async def test_a_family_with_no_face_that_failed_is_not_reported(
    client: Client,
) -> None:
    families = ("Upper Only",)
    assert (
        await reported(client, BOUNDS, families=families, on=("#out-of-range",)) == []
    )


def width(finding: dict[str, Any]) -> float:
    return finding["evidence"]["measured"]["textWidthPx"]


async def test_an_element_is_judged_on_its_own_text(client: Client) -> None:
    finding = await of_family(client, BOUNDS, "Parent Brand")
    assert finding == await sits_on(client, BOUNDS, "#own-parent")
    assert (elements(finding), width(finding)) == (1, 100)
    assert await reported(client, BOUNDS, families=(), on=("#bare-parent",)) == []


async def test_a_child_that_falls_back_is_reported_and_not_its_parent(
    client: Client,
) -> None:
    finding = await of_family(client, BOUNDS, "Child Brand")
    assert finding == await sits_on(client, BOUNDS, "#fallen-child")
    assert elements(finding) == 1
    assert await reported(client, BOUNDS, families=(), on=("#clean-parent",)) == []


async def test_a_text_in_a_face_that_loaded_is_not_counted(client: Client) -> None:
    assert await reported(client, BOUNDS, families=(), on=("#half-normal",)) == []
    assert elements(await of_family(client, BOUNDS, "Half")) == 1


async def test_a_text_that_fills_its_lines_in_a_face_that_loaded_is_not_counted(
    client: Client,
) -> None:
    assert await reported(client, BOUNDS, families=(), on=("#wrapped",)) == []
    assert elements(await of_family(client, BOUNDS, "Half")) == 1


async def test_a_text_partly_in_the_range_of_the_face_that_failed_is_not_counted(
    client: Client,
) -> None:
    assert await reported(client, BOUNDS, families=(), on=("#mixed-both",)) == []
    assert elements(await of_family(client, BOUNDS, "Mixed")) == 1


async def test_hidden_text_before_the_first_that_falls_back_is_not_judged(
    client: Client,
) -> None:
    finding = await of_family(client, BOUNDS, "Veiled Brand")
    assert finding == await sits_on(client, BOUNDS, "#seen")
    assert elements(finding) == 1
    assert await reported(client, BOUNDS, families=(), on=("#veiled",)) == []


async def test_text_that_paints_no_box_is_not_judged(client: Client) -> None:
    # `#unshown` has no box to find it by: the Finding is told from its selector.
    finding = await of_family(client, BOUNDS, "Unshown Brand")
    assert finding["selector"] == "#shown"
    assert finding == await sits_on(client, BOUNDS, "#shown")
    assert elements(finding) == 1


async def test_the_width_of_a_text_that_wraps_is_of_one_line(client: Client) -> None:
    finding = await sits_on(client, BOUNDS, "#long")
    assert width(finding) == 280
    assert finding["box"]["w"] == 100


async def test_the_finding_of_a_bold_text_carries_its_weight(client: Client) -> None:
    finding = await sits_on(client, BOUNDS, "#half-bold")
    assert finding["evidence"]["computed"] == {
        "font-family": "Half, Wide",
        "font-weight": "700",
        "font-style": "normal",
    }
    assert width(finding) == 300


async def test_the_selector_of_a_finding_works_in_inspect_element(
    client: Client,
) -> None:
    for url, viewports, count in ((BUG, [DESKTOP, MOBILE], 5), (BOUNDS, [DESKTOP], 12)):
        content = await detect(client, url, viewports=viewports, checks=ONLY)
        assert len(content["findings"]) == count
        for finding in content["findings"]:
            arguments = {
                "url": url,
                "selector": finding["selector"],
                "viewport": finding["viewport"],
            }
            result = await client.call_tool("inspect_element", arguments)
            assert result.is_error is False, texts(result)
            assert result.structured_content is not None
            assert result.structured_content["box"] == finding["box"]


async def test_the_widths_of_the_text_nodes_of_an_element_are_added(
    client: Client,
) -> None:
    finding = await sits_on(client, BOUNDS, "#split")
    assert (width(finding), elements(finding)) == (140, 1)


async def test_a_text_put_in_capitals_that_loaded_is_not_counted(
    client: Client,
) -> None:
    finding = await of_family(client, SHAPING, "Mixed")
    assert finding["selector"] == "#lower-mixed"
    assert finding == await sits_on(client, SHAPING, "#lower-mixed")
    assert elements(finding) == 1
    assert await reported(client, SHAPING, families=(), on=("#upper-mixed",)) == []


async def test_an_element_that_asks_for_the_italic_face_that_failed_is_reported(
    client: Client,
) -> None:
    finding = await of_family(client, SHAPING, "Slant")
    assert finding == await sits_on(client, SHAPING, "#slant-italic")
    assert elements(finding) == 1
    assert finding["evidence"]["computed"] == {
        "font-family": "Slant, Wide",
        "font-weight": "400",
        "font-style": "italic",
    }
    assert await reported(client, SHAPING, families=(), on=("#slant-normal",)) == []


async def test_the_width_holds_the_spacing_of_letters_and_words(
    client: Client,
) -> None:
    finding = await sits_on(client, SHAPING, "#spaced")
    assert width(finding) == 226


async def test_the_width_is_of_the_layout_the_box_is_of(client: Client) -> None:
    findings = (await detect(client, MONOSPACE, checks=ONLY))["findings"]
    (finding,) = findings
    assert finding["selector"] == "#code"
    assert findings == await findings_on(client, MONOSPACE, "#code", findings)
    assert (family(finding), elements(finding)) == ("Brand", 1)
    assert width(finding) == round(finding["box"]["w"], 2)


async def test_findings_of_this_check_and_another_come_in_document_order(
    client: Client,
) -> None:
    findings = (await detect(client, ORDER))["findings"]
    assert {finding["severity"] for finding in findings} == {"minor"}
    assert [(f["selector"], f["check"]) for f in findings] == [
        ("#a", "font-fallback"),
        ("#b", "font-fallback"),
        ("#b", "low-contrast-real"),
        ("#c", "low-contrast-real"),
    ]


async def test_a_page_of_a_thousand_texts_gets_one_finding(client: Client) -> None:
    result = await call(client, MANY, checks=ONLY)
    assert result.is_error is False
    assert result.structured_content is not None
    (finding,) = result.structured_content["findings"]
    assert elements(finding) == 1000


async def test_a_text_wider_in_a_face_that_loaded_than_in_its_tail_is_not_counted(
    client: Client,
) -> None:
    finding = await of_family(client, JUDGED, "Broad")
    assert (finding["selector"], elements(finding)) == ("#broad-bold", 1)
    assert finding == await sits_on(client, JUDGED, "#broad-bold")
    assert await reported(client, JUDGED, families=(), on=("#broad-normal",)) == []


async def test_text_whose_visibility_is_collapse_is_not_judged(client: Client) -> None:
    finding = await of_family(client, JUDGED, "Folded Brand")
    assert (finding["selector"], elements(finding)) == ("#unfolded", 1)
    assert finding == await sits_on(client, JUDGED, "#unfolded")
    assert await reported(client, JUDGED, families=(), on=("#folded",)) == []


async def test_own_text_that_is_only_whitespace_is_not_judged(client: Client) -> None:
    finding = await of_family(client, JUDGED, "Space Brand")
    assert (finding["selector"], elements(finding)) == ("#after-spaces", 1)
    assert finding == await sits_on(client, JUDGED, "#after-spaces")
    assert await reported(client, JUDGED, families=(), on=("#spaces",)) == []


async def test_a_family_is_named_as_the_first_of_its_faces_has_it(
    client: Client,
) -> None:
    finding = await sits_on(client, NAMES, "#dual-normal")
    assert (family(finding), elements(finding)) == ("Dual", 2)
    assert await reported(client, NAMES, families=("DUAL",), on=("#dual-bold",)) == []


async def test_a_family_name_that_holds_a_comma_is_read_whole(client: Client) -> None:
    families = ("Acme, Inc",)
    assert await reported(client, NAMES, families=families, on=("#comma",)) == [
        ("#comma", "Acme, Inc")
    ]


async def test_a_family_name_written_with_a_backslash_is_matched_to_its_face(
    client: Client,
) -> None:
    families = ('Vinyl 12"',)
    assert await reported(client, NAMES, families=families, on=("#inch",)) == [
        ("#inch", 'Vinyl 12"')
    ]
    finding = await sits_on(client, NAMES, "#inch")
    assert finding["evidence"]["computed"]["font-family"] == '"Vinyl 12\\"", Ahem'
