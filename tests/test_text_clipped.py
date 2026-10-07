"""The `text-clipped` Check through `detect_visual_bugs`, against real Chromium."""

import pytest
from helpers import call, detect, findings_on, fixture_url, images, texts
from mcp import Client

pytestmark = pytest.mark.anyio

BUG = fixture_url("text-clipped-bug.html")
BOUNDS = fixture_url("text-clipped-bounds.html")
CLEAN = fixture_url("text-clipped-clean.html")
STRIP = fixture_url("text-clipped-strip.html")


async def test_text_cut_by_a_hidden_overflow_yields_one_finding(client: Client) -> None:
    findings = (await detect(client, BUG))["findings"]
    (finding,) = await findings_on(client, BUG, "h1", findings)
    assert finding["check"] == "text-clipped"
    assert finding["evidence"]["computed"]["overflow-x"] == "hidden"


async def test_text_cut_by_a_clip_overflow_yields_one_finding(client: Client) -> None:
    findings = (await detect(client, BOUNDS))["findings"]
    (finding,) = await findings_on(client, BOUNDS, "#clip", findings)
    assert finding["evidence"]["computed"]["overflow-x"] == "clip"


async def test_a_cut_of_8px_is_major(client: Client) -> None:
    findings = (await detect(client, BOUNDS))["findings"]
    (finding,) = await findings_on(client, BOUNDS, "#over-8", findings)
    assert finding["severity"] == "major"
    assert finding["evidence"]["measured"]["overflowPx"] == 8


async def test_a_cut_of_2px_to_7px_is_minor(client: Client) -> None:
    findings = (await detect(client, BOUNDS))["findings"]
    for selector, overflow_px in (("#over-7", 7), ("#over-2", 2)):
        (finding,) = await findings_on(client, BOUNDS, selector, findings)
        assert finding["severity"] == "minor"
        assert finding["evidence"]["measured"]["overflowPx"] == overflow_px


async def test_a_cut_of_1px_is_not_reported(client: Client) -> None:
    findings = (await detect(client, BOUNDS))["findings"]
    assert await findings_on(client, BOUNDS, "#over-1", findings) == []
    assert len(findings) == 5


async def test_a_translated_element_is_reported_where_it_is_painted(
    client: Client,
) -> None:
    findings = (await detect(client, BOUNDS))["findings"]
    (finding,) = await findings_on(client, BOUNDS, "#moved", findings)
    assert finding["box"] == {"x": 70, "y": 410, "w": 150, "h": 30}
    assert finding["evidence"]["measured"]["overflowPx"] == 50


async def reported(client: Client, selectors: tuple[str, ...]) -> list[str]:
    """The elements of the clean fixture, among `selectors`, that got a Finding."""
    findings = (await detect(client, CLEAN))["findings"]
    return [
        selector
        for selector in selectors
        if await findings_on(client, CLEAN, selector, findings)
    ]


async def test_clean_fixture_yields_no_finding_no_image_and_says_so(
    client: Client,
) -> None:
    result = await call(client, CLEAN)
    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["findings"] == []
    assert images(result) == []
    assert texts(result) == ["No findings in 1 viewport."]


async def test_text_that_is_not_visibly_cut_is_not_reported(client: Client) -> None:
    near_misses = (
        "#fits",  # as wide as its box
        "#wraps",
        "#visible",
        "#scrolls",
        "#ellipsis",
        "#sr-only",
        "#invisible",
        "#blank-tail",  # only whitespace overflows
        "#ancestor",  # the text is its child's
        "#ancestor > div",
        "#rtl",
    )
    assert await reported(client, near_misses) == []


async def test_hidden_text_over_a_pattern_is_not_reported(client: Client) -> None:
    # The pattern behind it is not flat, so the pixels alone would confirm a cut.
    assert await reported(client, ("#hidden-over-pattern",)) == []


async def test_fitting_text_beside_an_overflowing_child_is_not_reported(
    client: Client,
) -> None:
    # scrollWidth counts the child; the text itself ends 200px before the edge.
    assert await reported(client, ("#child-overflows",)) == []


async def test_an_element_painted_at_another_size_than_laid_out_is_not_reported(
    client: Client,
) -> None:
    resized = ("#scaled", "#stretched", "#widened", "#turned", "#in-scaled")
    assert await reported(client, resized) == []


async def test_the_cut_is_looked_for_inside_the_padding_box(client: Client) -> None:
    # Only blank overflow reaches the edge; the ink ends a border width before it.
    findings = (await detect(client, STRIP))["findings"]
    assert await findings_on(client, STRIP, "#bordered", findings) == []


async def test_the_cut_is_looked_for_left_of_the_right_border(client: Client) -> None:
    findings = (await detect(client, STRIP))["findings"]
    (finding,) = await findings_on(client, STRIP, "#right-border", findings)
    assert finding["evidence"]["measured"]["overflowPx"] == 50


async def test_the_strip_of_a_box_narrower_than_a_glyph_stays_inside_it(
    client: Client,
) -> None:
    # Nothing is painted inside the 10px box: its only glyph is out of sight.
    findings = (await detect(client, STRIP))["findings"]
    assert await findings_on(client, STRIP, "#narrow", findings) == []


async def test_a_cut_falling_in_a_gap_between_glyphs_is_reported(
    client: Client,
) -> None:
    findings = (await detect(client, STRIP))["findings"]
    (finding,) = await findings_on(client, STRIP, "#gap-at-edge", findings)
    assert finding["evidence"]["measured"]["overflowPx"] == 70


async def test_an_edge_painted_in_two_colours_confirms_the_cut(client: Client) -> None:
    findings = (await detect(client, STRIP))["findings"]
    (finding,) = await findings_on(client, STRIP, "#two-colours", findings)
    assert finding["evidence"]["measured"]["overflowPx"] == 50
    # The fixture paints exactly two colours there, not more.
    inspected = await client.call_tool(
        "inspect_element", {"url": STRIP, "selector": "#two-colours"}
    )
    assert inspected.structured_content is not None
    assert inspected.structured_content["sampledColors"] == [
        {"hex": "#ffffff", "share": 0.5},
        {"hex": "#c8c8c8", "share": 0.5},
    ]
