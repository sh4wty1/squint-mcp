"""Finding selectors through `detect_visual_bugs`, against real Chromium."""

import pytest
from helpers import detect, fixture_url, texts
from mcp import Client

pytestmark = pytest.mark.anyio

BUG = fixture_url("text-clipped-bug.html")
SELECTORS = fixture_url("selectors.html")


async def selector_of(client: Client, glyphs: int) -> str:
    """The selector of the Finding whose element holds `glyphs` glyphs.

    Each selector case of the fixture holds its own number of them.
    """
    findings = (await detect(client, SELECTORS))["findings"]
    (finding,) = (f for f in findings if f["text"] == "X" * glyphs)
    return finding["selector"]


async def test_a_unique_data_testid_wins_over_the_id(client: Client) -> None:
    assert await selector_of(client, 8) == '[data-testid="save"]'


async def test_a_shared_data_testid_falls_through_to_the_id(client: Client) -> None:
    assert await selector_of(client, 9) == "#first-row"


async def test_an_id_with_other_characters_falls_through_to_tag_and_aria_label(
    client: Client,
) -> None:
    assert await selector_of(client, 10) == 'button[aria-label="Close dialog"]'


async def test_an_id_with_many_digits_falls_through_to_role_and_aria_label(
    client: Client,
) -> None:
    assert await selector_of(client, 11) == '[role="tab"][aria-label="Settings"]'


async def test_an_id_with_three_digits_looks_generated_and_two_do_not(
    client: Client,
) -> None:
    assert await selector_of(client, 19) == 'div[aria-label="Step"]'
    assert await selector_of(client, 20) == "#col-12"


async def test_a_data_testid_repeated_inside_a_shadow_root_is_not_unique(
    client: Client,
) -> None:
    assert await selector_of(client, 18) == "#outside"


async def test_a_shared_id_falls_through_to_the_css_path(client: Client) -> None:
    assert await selector_of(client, 12) == "body > main > p:nth-of-type(2)"


async def test_a_shared_aria_label_falls_through_to_distinct_css_paths(
    client: Client,
) -> None:
    first = await selector_of(client, 13)
    second = await selector_of(client, 14)
    assert first == "body > main > button:nth-of-type(2)"
    assert second == "body > main > button:nth-of-type(3)"


async def test_css_path_has_no_nth_of_type_for_an_only_tag(client: Client) -> None:
    assert await selector_of(client, 15) == "body > main > h2"


async def test_css_path_inside_a_shadow_root_starts_at_the_host_selector(
    client: Client,
) -> None:
    assert await selector_of(client, 16) == '[data-testid="card"] > h3'


async def test_a_double_quote_in_an_attribute_value_is_escaped(client: Client) -> None:
    assert await selector_of(client, 17) == '[data-testid="say \\"hi\\""]'


async def test_first_finding_of_the_bug_fixture_is_the_documented_one(
    client: Client,
) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert findings[0] == {
        "check": "text-clipped",
        "category": "visual-bug",
        "severity": "major",
        "message": "Text clipped by 50px by its container width",
        "selector": '[data-testid="hero-title"]',
        "text": "XXXXXXXXXX",
        "box": {"x": 40, "y": 120, "w": 150, "h": 30},
        "viewport": {"width": 1440, "height": 900},
        "evidence": {
            "computed": {
                "overflow-x": "hidden",
                "white-space": "nowrap",
                "text-overflow": "clip",
                "width": "150px",
                "font-size": "20px",
            },
            "measured": {"overflowPx": 50, "scrollWidth": 200, "clientWidth": 150},
            "cropIndex": 0,
        },
        "suggestion": "Allow wrapping or reduce font-size at this width",
        "source": "Squint heuristic",
    }


async def test_every_finding_selector_resolves_to_its_element_in_inspect_element(
    client: Client,
) -> None:
    for url, count in ((BUG, 2), (SELECTORS, 16)):
        findings = (await detect(client, url))["findings"]
        assert len(findings) == count
        for finding in findings:
            arguments = {
                "url": url,
                "selector": finding["selector"],
                "viewport": finding["viewport"],
            }
            result = await client.call_tool("inspect_element", arguments)
            assert result.is_error is False, texts(result)
            assert result.structured_content is not None
            assert result.structured_content["box"] == finding["box"]
