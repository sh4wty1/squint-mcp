"""`detect_visual_bugs` through the MCP tool boundary, against real Chromium."""

import base64
import io
import time
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
from mcp.types import TextContent, Tool
from PIL import Image

from squint_mcp import config

pytestmark = pytest.mark.anyio

BUG = fixture_url("text-clipped-bug.html")
RESPONSIVE = fixture_url("responsive.html")
SELECTORS = fixture_url("selectors.html")
MANY = fixture_url("many.html")
HUGE = fixture_url("huge-text.html")


async def detect_tool(client: Client) -> Tool:
    (tool,) = (
        t for t in (await client.list_tools()).tools if t.name == "detect_visual_bugs"
    )
    return tool


async def test_detect_visual_bugs_is_read_only_and_open_world(client: Client) -> None:
    annotations = (await detect_tool(client)).annotations
    assert annotations is not None
    assert annotations.read_only_hint is True
    assert annotations.open_world_hint is True


async def test_detect_visual_bugs_takes_url_and_optional_viewports_and_checks(
    client: Client,
) -> None:
    schema = (await detect_tool(client)).input_schema
    properties = schema["properties"]
    assert set(properties) == {"url", "viewports", "checks"}
    assert properties["url"]["type"] == "string"
    assert schema["required"] == ["url"]

    def resolved(option: dict[str, Any]) -> dict[str, Any]:
        if "$ref" in option:
            return schema["$defs"][option["$ref"].removeprefix("#/$defs/")]
        return option

    def item_of(name: str) -> dict[str, Any]:
        """The item schema of the array `name` accepts, which is an array or null."""
        options = properties[name]["anyOf"]
        assert {option["type"] for option in options} == {"array", "null"}
        (array,) = (option for option in options if option["type"] == "array")
        return resolved(array["items"])

    viewport = item_of("viewports")
    assert viewport["type"] == "object"
    assert set(viewport["properties"]) == {"width", "height"}
    assert item_of("checks")["type"] == "string"


async def test_success_returns_exactly_findings_and_captures(client: Client) -> None:
    result = await call(client, BUG)
    assert result.is_error is False
    assert result.structured_content is not None
    assert set(result.structured_content) == {"findings", "captures"}


async def test_each_capture_has_exactly_viewport_and_stabilized(client: Client) -> None:
    content = await detect(client, RESPONSIVE, viewports=[DESKTOP, MOBILE])
    assert len(content["captures"]) == 2
    for captured in content["captures"]:
        assert set(captured) == {"viewport", "stabilized"}


async def test_default_is_one_stabilized_capture_at_1440_by_900(client: Client) -> None:
    content = await detect(client, BUG)
    assert content["captures"] == [
        {"viewport": {"width": 1440, "height": 900}, "stabilized": True}
    ]


async def test_null_viewports_or_checks_match_omitting_them(client: Client) -> None:
    omitted = await detect(client, BUG)
    assert await detect(client, BUG, viewports=None) == omitted
    assert await detect(client, BUG, checks=None) == omitted


async def test_bug_fixture_yields_two_text_clipped_findings(client: Client) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert [finding["check"] for finding in findings] == ["text-clipped"] * 2


async def test_naming_the_text_clipped_check_matches_omitting_checks(
    client: Client,
) -> None:
    omitted = await detect(client, BUG)
    assert await detect(client, BUG, checks=["text-clipped"]) == omitted


async def test_summary_counts_findings_viewports_and_severities(client: Client) -> None:
    result = await call(client, BUG)
    first = result.content[0]
    assert isinstance(first, TextContent)
    assert first.text == "Found 2 findings in 1 viewport: 1 major, 1 minor."


async def test_summary_says_finding_in_the_singular_for_one(client: Client) -> None:
    result = await call(client, RESPONSIVE)
    assert texts(result) == ["Found 1 finding in 1 viewport: 1 major."]


async def test_the_same_call_returns_the_same_structured_content(
    client: Client,
) -> None:
    assert await detect(client, BUG) == await detect(client, BUG)


async def test_finding_has_exactly_the_documented_keys(client: Client) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert len(findings) == 2
    for finding in findings:
        assert set(finding) == {
            "check",
            "category",
            "severity",
            "message",
            "selector",
            "text",
            "box",
            "viewport",
            "evidence",
            "suggestion",
            "source",
        }
        assert set(finding["evidence"]) == {"computed", "measured", "cropIndex"}


async def test_findings_are_ordered_by_severity_before_document_order(
    client: Client,
) -> None:
    findings = (await detect(client, BUG))["findings"]
    assert [finding["severity"] for finding in findings] == ["major", "minor"]
    # `#badge` comes first in the document and last in the Findings.
    assert await findings_on(client, BUG, "h1", findings) == [findings[0]]
    assert await findings_on(client, BUG, "#badge", findings) == [findings[1]]


async def test_text_longer_than_40_characters_is_cut_to_39_and_an_ellipsis(
    client: Client,
) -> None:
    findings = (await detect(client, SELECTORS))["findings"]
    (finding,) = await findings_on(client, SELECTORS, "#long", findings)
    assert finding["text"] == "X" * 39 + "…"


async def test_text_of_exactly_40_characters_is_not_cut(client: Client) -> None:
    findings = (await detect(client, SELECTORS))["findings"]
    assert [f["text"] for f in findings if len(f["text"]) == 40] == [
        "X" * 39 + "…",  # `#long`, cut from 60
        "X" * 40,
    ]


async def test_findings_of_equal_severity_are_in_document_order(
    client: Client,
) -> None:
    findings = (await detect(client, SELECTORS))["findings"]
    assert {finding["severity"] for finding in findings} == {"major"}
    # The element of 16 glyphs is inside a shadow root: it sits at its host's place.
    assert [finding["text"] for finding in findings] == [
        "X" * 39 + "…",
        "XXXXX XXXXX",
        *("X" * glyphs for glyphs in range(8, 19)),
        "X" * 40,
        *("X" * glyphs for glyphs in range(19, 27)),
    ]
    many = (await detect(client, MANY))["findings"]
    assert [finding["selector"] for finding in many] == [
        "#m1",
        "#m2",
        "#m3",
        "#m4",
        "#m5",
        "#m6",
        "#small",
    ]


async def test_a_crop_is_cut_from_the_pixels_of_its_own_viewport(
    client: Client,
) -> None:
    result = await call(client, RESPONSIVE, viewports=[DESKTOP, MOBILE])
    assert result.structured_content is not None
    findings = result.structured_content["findings"]
    (finding,) = await findings_on(client, RESPONSIVE, "#half", findings, MOBILE)
    crop_index: int = finding["evidence"]["cropIndex"]
    image = images(result)[crop_index]
    crop = Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")
    assert crop.size == (227, 62)  # the 195x30 box of the 390px viewport, plus 16px
    assert crop.getpixel((208, 31)) == (0, 0, 0)  # the last glyph the box shows
    # Past the box the text is cut here; at 1440px wide it would go on.
    assert crop.getpixel((213, 31)) == (255, 255, 255)


async def test_text_whitespace_is_collapsed_to_single_spaces(client: Client) -> None:
    findings = (await detect(client, SELECTORS))["findings"]
    (finding,) = await findings_on(client, SELECTORS, "#spaced", findings)
    assert finding["text"] == "XXXXX XXXXX"


async def test_several_viewports_are_captured_and_reported_in_the_order_given(
    client: Client,
) -> None:
    result = await call(client, RESPONSIVE, viewports=[DESKTOP, MOBILE])
    content = result.structured_content
    assert content is not None
    assert content["captures"] == [
        {"viewport": DESKTOP, "stabilized": True},
        {"viewport": MOBILE, "stabilized": True},
    ]
    findings = content["findings"]
    assert [(finding["viewport"], finding["severity"]) for finding in findings] == [
        (DESKTOP, "major"),
        (MOBILE, "major"),
        (MOBILE, "minor"),
    ]
    on = [
        await findings_on(client, RESPONSIVE, "#fixed", findings, DESKTOP),
        await findings_on(client, RESPONSIVE, "#fixed", findings, MOBILE),
        await findings_on(client, RESPONSIVE, "#half", findings, MOBILE),
    ]
    assert on == [[findings[0]], [findings[1]], [findings[2]]]
    assert findings[2]["evidence"]["measured"]["overflowPx"] == 5
    assert texts(result) == ["Found 3 findings in 2 viewports: 2 major, 1 minor."]


async def test_a_page_that_never_goes_network_idle_is_reported_unstabilized(
    client: Client, local_server: str
) -> None:
    content = await detect(client, f"{local_server}/polling.html")
    assert content["captures"][0]["stabilized"] is False


async def test_response_is_one_text_block_then_a_png_per_finding_up_to_five(
    client: Client,
) -> None:
    for url, crops in ((BUG, 2), (MANY, 5)):
        result = await call(client, url)
        assert isinstance(result.content[0], TextContent)
        assert result.content[1:] == images(result)
        assert [image.mime_type for image in images(result)] == ["image/png"] * crops


async def test_crops_go_to_the_five_most_severe_findings(client: Client) -> None:
    findings = (await detect(client, MANY))["findings"]
    assert [finding["evidence"]["cropIndex"] for finding in findings] == [
        0,
        1,
        2,
        3,
        4,
        None,
        None,
    ]
    assert findings[6]["severity"] == "minor"
    assert await findings_on(client, MANY, "#small", findings) == [findings[6]]


async def test_each_crop_shows_the_box_of_its_own_finding(client: Client) -> None:
    result = await call(client, MANY)
    assert result.structured_content is not None
    findings = result.structured_content["findings"]
    text_colors = {
        "#m1": (200, 0, 0),
        "#m2": (0, 120, 0),
        "#m3": (0, 0, 200),
        "#m4": (160, 0, 160),
        "#m5": (0, 130, 130),
    }
    for selector, text_color in text_colors.items():
        (finding,) = await findings_on(client, MANY, selector, findings)
        crop_index: int = finding["evidence"]["cropIndex"]
        image = images(result)[crop_index]
        crop = Image.open(io.BytesIO(base64.b64decode(image.data))).convert("RGB")
        assert crop.size == (182, 62)  # the 150x30 box plus 16px on each side
        assert crop.getpixel((20, 31)) == text_color  # inside the first glyph


async def test_a_repeated_viewport_is_captured_once(client: Client) -> None:
    once = await detect(client, RESPONSIVE, viewports=[MOBILE])
    twice = await detect(client, RESPONSIVE, viewports=[MOBILE, MOBILE])
    assert twice["captures"] == [{"viewport": MOBILE, "stabilized": True}]
    assert len(once["findings"]) == 2
    assert twice["findings"] == once["findings"]


async def test_a_repeated_viewport_keeps_its_first_place(client: Client) -> None:
    content = await detect(client, RESPONSIVE, viewports=[DESKTOP, MOBILE, DESKTOP])
    assert content["captures"] == [
        {"viewport": DESKTOP, "stabilized": True},
        {"viewport": MOBILE, "stabilized": True},
    ]


async def test_a_repeated_check_name_runs_once(client: Client) -> None:
    once = await detect(client, BUG, checks=["text-clipped"])
    twice = await detect(client, BUG, checks=["text-clipped", "text-clipped"])
    assert len(once["findings"]) == 2
    assert twice["findings"] == once["findings"]


async def error_text(client: Client, arguments: dict[str, Any]) -> str:
    """Call the tool, expect a tool error and return its text."""
    result = await client.call_tool("detect_visual_bugs", arguments)
    assert result.is_error is True
    return " ".join(texts(result))


async def test_a_page_with_one_very_large_text_node_is_checked(client: Client) -> None:
    # 100,000 lines in one text node: one client rect each.
    assert (await detect(client, HUGE))["findings"] == []


async def test_unknown_check_is_an_error_listing_the_valid_ones(client: Client) -> None:
    text = await error_text(client, {"url": BUG, "checks": ["nope"]})
    assert (
        'Unknown check "nope". Valid checks: low-contrast-real, text-clipped.' in text
    )


async def test_unknown_check_after_a_valid_one_is_still_an_error(
    client: Client,
) -> None:
    text = await error_text(client, {"url": BUG, "checks": ["text-clipped", "nope"]})
    assert (
        'Unknown check "nope". Valid checks: low-contrast-real, text-clipped.' in text
    )


async def test_the_first_unknown_check_in_the_order_given_is_the_one_named(
    client: Client,
) -> None:
    text = await error_text(client, {"url": BUG, "checks": ["zzz", "nope"]})
    assert 'Unknown check "zzz". Valid checks: low-contrast-real, text-clipped.' in text


async def test_unknown_check_is_reported_before_any_browser_work(
    client_without_chromium: Client,
) -> None:
    arguments = {"url": BUG, "checks": ["nope"]}
    text = await error_text(client_without_chromium, arguments)
    assert (
        'Unknown check "nope". Valid checks: low-contrast-real, text-clipped.' in text
    )
    assert "Could not launch Chromium" not in text


async def test_empty_checks_is_rejected(client: Client) -> None:
    assert "checks" in await error_text(client, {"url": BUG, "checks": []})


async def test_empty_viewports_is_rejected(client: Client) -> None:
    assert "viewports" in await error_text(client, {"url": BUG, "viewports": []})


async def test_viewport_smaller_than_one_pixel_is_rejected(client: Client) -> None:
    for field in ("width", "height"):
        viewport = {"width": 1440, "height": 900, field: 0}
        text = await error_text(client, {"url": BUG, "viewports": [viewport]})
        assert field in text


async def test_missing_url_is_rejected(client: Client) -> None:
    assert "url" in await error_text(client, {})


async def test_unsupported_url_scheme_is_an_error(client: Client) -> None:
    text = await error_text(client, {"url": "ftp://example.com/page.html"})
    assert 'Unsupported URL scheme "ftp"; use http://, https:// or file://.' in text


async def test_page_that_cannot_be_loaded_is_an_error(client: Client) -> None:
    url = fixture_url("no-such-page.html")
    assert f"Could not load {url}" in await error_text(client, {"url": url})


async def test_missing_chromium_names_the_install_command(
    client_without_chromium: Client,
) -> None:
    text = await error_text(client_without_chromium, {"url": BUG})
    assert "Could not launch Chromium" in text
    assert "playwright install chromium" in text


async def test_total_timeout_covers_all_viewports_together_and_server_recovers(
    client: Client, local_server: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Each viewport of the polling page takes the 3s idle wait: one fits in 4s,
    # two do not. Patching the config is the only reach past the MCP boundary.
    arguments = {
        "url": f"{local_server}/polling.html",
        "viewports": [DESKTOP, MOBILE],
    }
    with monkeypatch.context() as patch:
        patch.setattr(config, "TOTAL_TIMEOUT_S", 4.0)
        started = time.monotonic()
        text = await error_text(client, arguments)
        elapsed = time.monotonic() - started
    assert "Timed out after 4s" in text
    assert 4 <= elapsed < 5
    assert len((await detect(client, BUG))["findings"]) == 2


ORDER = fixture_url("checks-order.html")
IN_DOCUMENT_ORDER = [
    ("#a", "low-contrast-real"),
    ("#b", "text-clipped"),
    ("#c", "low-contrast-real"),
    ("#c", "text-clipped"),
    ("#d", "text-clipped"),
    ("#e", "low-contrast-real"),
]


async def test_findings_of_two_checks_come_in_document_order(client: Client) -> None:
    findings = (await detect(client, ORDER))["findings"]
    assert {finding["severity"] for finding in findings} == {"minor"}
    assert [(f["selector"], f["check"]) for f in findings] == IN_DOCUMENT_ORDER


async def test_two_findings_on_one_element_come_in_check_name_order(
    client: Client,
) -> None:
    findings = (await detect(client, ORDER))["findings"]
    on_c = await findings_on(client, ORDER, "#c", findings)
    assert [finding["check"] for finding in on_c] == [
        "low-contrast-real",
        "text-clipped",
    ]


async def test_the_order_of_the_checks_argument_changes_nothing(client: Client) -> None:
    named = await detect(client, ORDER, checks=["text-clipped", "low-contrast-real"])
    assert named == await detect(client, ORDER)
    assert len(named["findings"]) == 6


async def test_the_crops_go_to_the_first_five_findings_across_checks(
    client: Client,
) -> None:
    result = await call(client, ORDER)
    assert result.structured_content is not None
    findings = result.structured_content["findings"]
    assert [(f["selector"], f["check"]) for f in findings] == IN_DOCUMENT_ORDER
    assert len(images(result)) == 5
    assert [f["evidence"]["cropIndex"] for f in findings] == [0, 1, 2, 3, 4, None]
