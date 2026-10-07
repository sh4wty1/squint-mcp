"""`detect_visual_bugs` through the MCP tool boundary, against real Chromium."""

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

pytestmark = pytest.mark.anyio

BUG = fixture_url("text-clipped-bug.html")
RESPONSIVE = fixture_url("responsive.html")
SELECTORS = fixture_url("selectors.html")


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


async def test_findings_carry_no_crop_yet(client: Client) -> None:
    result = await call(client, BUG)
    assert result.structured_content is not None
    findings = result.structured_content["findings"]
    assert [finding["evidence"]["cropIndex"] for finding in findings] == [None, None]
    assert images(result) == []
