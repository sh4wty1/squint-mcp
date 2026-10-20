"""A page whose Content Security Policy refuses inline styles, against real Chromium.

The Capture adds rules of its own to every page (AD-004, AD-005); under
`style-src file:` none of them may be an inline style, or every Check reads a
page with no ink (issue #26).
"""

import shutil
from pathlib import Path

import pytest
from helpers import FIXTURES, detect, findings_on, fixture_url, texts
from mcp import Client

pytestmark = pytest.mark.anyio

PAGE = fixture_url("style-src.html")
REFUSED = fixture_url("style-src-refused.html")
POLICY = '    <meta http-equiv="Content-Security-Policy" content="style-src file:" />\n'
CONTRAST = ["low-contrast-real"]


async def one_finding(client: Client, selector: str, checks: list[str]) -> None:
    findings = (await detect(client, PAGE, checks=checks))["findings"]
    (finding,) = await findings_on(client, PAGE, selector, findings)
    assert finding["check"] == checks[0]


async def test_a_text_of_low_contrast_is_reported_under_the_policy(
    client: Client,
) -> None:
    await one_finding(client, "#flat", CONTRAST)


async def test_a_covered_text_is_reported_under_the_policy(client: Client) -> None:
    await one_finding(client, "#covered", ["overlap"])


async def test_a_text_in_an_open_shadow_root_is_reported_under_the_policy(
    client: Client,
) -> None:
    await one_finding(client, "#shadow-host span", CONTRAST)


async def test_a_sheet_the_page_adopts_is_kept(client: Client) -> None:
    await one_finding(client, "#adopted", CONTRAST)


async def test_a_transition_started_after_load_takes_no_time_under_the_policy(
    client: Client,
) -> None:
    await one_finding(client, "#late", CONTRAST)


async def test_the_policy_changes_no_finding(client: Client, tmp_path: Path) -> None:
    source = (FIXTURES / "style-src.html").read_text(encoding="utf-8")
    assert POLICY in source
    (tmp_path / "style-src.html").write_text(source.replace(POLICY, ""), "utf-8")
    for name in ("style-src.css", "Ahem.ttf"):
        shutil.copy(FIXTURES / name, tmp_path / name)
    open_page = (tmp_path / "style-src.html").as_uri()

    def pairs(findings: list[dict[str, str]]) -> list[tuple[str, str]]:
        return [(finding["selector"], finding["check"]) for finding in findings]

    under = pairs((await detect(client, PAGE))["findings"])
    assert under != []
    assert under == pairs((await detect(client, open_page))["findings"])


async def test_the_page_policy_still_refuses_its_own_inline_style(
    client: Client,
) -> None:
    arguments = {"url": REFUSED, "selector": "#refused"}
    result = await client.call_tool("inspect_element", arguments)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    assert result.structured_content["computed"]["color"] == "rgb(0, 0, 0)"
