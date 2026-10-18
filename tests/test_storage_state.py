"""`storageState` through the MCP tool boundary, against real Chromium."""

import json
from pathlib import Path
from typing import Any

import pytest
from helpers import DESKTOP, MOBILE, SESSION_COOKIE, texts
from mcp import Client
from mcp.types import CallToolResult

pytestmark = pytest.mark.anyio

TOOLS = ("inspect_element", "detect_visual_bugs", "extract_tokens")
RADIO = "s3cret-radio"


def session(origin: str) -> dict[str, Any]:
    """A storage state logged in to the page, as `codegen --save-storage` writes one."""
    return {
        "cookies": [
            {
                "name": "sid",
                "value": SESSION_COOKIE,
                "domain": "127.0.0.1",
                "path": "/api/v1/admin",
                "expires": -1,
                "httpOnly": True,
                "secure": True,
                "sameSite": "Strict",
            }
        ],
        "origins": [
            {"origin": origin, "localStorage": [{"name": "radio", "value": RADIO}]}
        ],
    }


@pytest.fixture
def state(tmp_path: Path, local_server: str) -> Path:
    path = tmp_path / "state.json"
    path.write_text(json.dumps(session(local_server)))
    return path


def page(local_server: str, query: str = "") -> str:
    return f"{local_server}/storage-state.html{query}"


async def call(client: Client, tool: str, url: str, **extra: Any) -> CallToolResult:
    return await client.call_tool(tool, {"url": url, **extra})


async def succeed(client: Client, tool: str, url: str, **extra: Any) -> dict[str, Any]:
    result = await call(client, tool, url, **extra)
    assert result.is_error is False, texts(result)
    assert result.structured_content is not None
    return result.structured_content


async def fail(client: Client, url: str, **extra: Any) -> str:
    """The message `inspect_element` on `#campaigns` fails with."""
    result = await call(client, "inspect_element", url, selector="#campaigns", **extra)
    assert result.is_error is True
    (text,) = texts(result)
    prefix = "Error executing tool inspect_element: "
    assert text.startswith(prefix), text
    return text.removeprefix(prefix)


def clipped(findings: list[dict[str, Any]], viewport: dict[str, int]) -> list[str]:
    return [
        finding["selector"]
        for finding in findings
        if finding["check"] == "text-clipped" and finding["viewport"] == viewport
    ]


def text_colors(tokens: dict[str, Any]) -> set[str]:
    return {
        token["value"]
        for token in tokens["colors"]["tokens"]
        if token["roles"]["text"] > 0
    }


async def test_inspect_element_sees_the_screen_after_login(
    client: Client, local_server: str, state: Path
) -> None:
    inspected = await succeed(
        client,
        "inspect_element",
        page(local_server),
        selector="#campaigns",
        storageState=str(state),
    )
    assert inspected["computed"]["color"] == "rgb(18, 52, 86)"


async def test_detect_visual_bugs_judges_the_screen_after_login_in_every_viewport(
    client: Client, local_server: str, state: Path
) -> None:
    content = await succeed(
        client,
        "detect_visual_bugs",
        page(local_server),
        viewports=[DESKTOP, MOBILE],
        storageState=str(state),
    )
    for viewport in (DESKTOP, MOBILE):
        assert clipped(content["findings"], viewport) == ["#clipped"]


async def test_extract_tokens_reads_the_screen_after_login(
    client: Client, local_server: str, state: Path
) -> None:
    tokens = await succeed(
        client, "extract_tokens", page(local_server), storageState=str(state)
    )
    assert "#123456" in text_colors(tokens)


@pytest.mark.parametrize("tool", TOOLS)
async def test_without_a_storage_state_a_call_sees_the_login_screen(
    client: Client, local_server: str, tool: str
) -> None:
    url = page(local_server)
    if tool == "inspect_element":
        assert await fail(client, url) == 'Selector "#campaigns" matched no elements.'
    elif tool == "detect_visual_bugs":
        content = await succeed(client, tool, url)
        assert clipped(content["findings"], DESKTOP) == []
    else:
        assert "#123456" not in text_colors(await succeed(client, tool, url))


async def test_a_cookie_a_page_sets_does_not_reach_the_next_call(
    client: Client, local_server: str, state: Path
) -> None:
    # The page sets `seen` before it asks its API, so within one call it comes back.
    await succeed(
        client,
        "inspect_element",
        page(local_server, "?set-cookie"),
        selector="#seen-sent",
        storageState=str(state),
    )
    # The next call with the same file sends the session and not `seen`.
    await succeed(
        client,
        "inspect_element",
        page(local_server),
        selector="#campaigns",
        storageState=str(state),
    )
    result = await call(
        client,
        "inspect_element",
        page(local_server),
        selector="#seen-sent",
        storageState=str(state),
    )
    assert result.is_error is True
    assert texts(result)[-1].endswith('Selector "#seen-sent" matched no elements.')


async def test_the_storage_state_file_is_never_written(
    client: Client, local_server: str, state: Path
) -> None:
    before = state.read_bytes()
    await succeed(
        client,
        "inspect_element",
        page(local_server, "?set-cookie"),
        selector="#campaigns",
        storageState=str(state),
    )
    assert state.read_bytes() == before


async def test_a_relative_storage_state_is_refused(
    client: Client, local_server: str
) -> None:
    message = await fail(client, page(local_server), storageState="state.json")
    assert message == 'storageState must be an absolute path: "state.json".'


async def test_a_storage_state_that_cannot_be_read_is_refused(
    client: Client, local_server: str, tmp_path: Path
) -> None:
    missing = tmp_path / "missing.json"
    message = await fail(client, page(local_server), storageState=str(missing))
    assert message.startswith(f'Could not read the storage state "{missing}": ')
    assert message.endswith(".")


@pytest.mark.parametrize(
    "content",
    ["not json", "[]", '{"cookies": "nope"}'],
    ids=["not-json", "array", "rejected"],
)
async def test_a_file_that_is_not_a_storage_state_is_refused(
    client: Client, local_server: str, tmp_path: Path, content: str
) -> None:
    path = tmp_path / "state.json"
    path.write_text(content)
    message = await fail(client, page(local_server), storageState=str(path))
    assert message == f'"{path}" is not a Playwright storage state.'


@pytest.mark.parametrize(
    "content",
    [
        f"sid={SESSION_COOKIE}",
        json.dumps(
            {
                "cookies": [{"name": "sid", "value": SESSION_COOKIE}],
                "origins": [
                    {
                        "origin": "http://127.0.0.1",
                        "localStorage": [{"name": "radio", "value": RADIO}],
                    }
                ],
            }
        ),
    ],
    ids=["not-json", "no-domain"],
)
async def test_a_refused_storage_state_is_not_quoted(
    client: Client, local_server: str, tmp_path: Path, content: str
) -> None:
    path = tmp_path / "state.json"
    path.write_text(content)
    result = await call(
        client,
        "inspect_element",
        page(local_server),
        selector="#campaigns",
        storageState=str(path),
    )
    assert result.is_error is True
    text = "\n".join(texts(result))
    assert SESSION_COOKIE not in text
    assert RADIO not in text


async def test_the_three_tools_take_an_optional_storage_state(client: Client) -> None:
    tools = (await client.list_tools()).tools
    taking = {
        tool.name for tool in tools if "storageState" in tool.input_schema["properties"]
    }
    assert taking == set(TOOLS)
    for tool in tools:
        if tool.name in TOOLS:
            schema = tool.input_schema
            assert "storageState" not in schema.get("required", [])
            options = schema["properties"]["storageState"]["anyOf"]
            assert {option["type"] for option in options} == {"string", "null"}


@pytest.mark.parametrize("name", TOOLS)
async def test_the_three_tools_describe_storage_state(
    client: Client, name: str
) -> None:
    (tool,) = (t for t in (await client.list_tools()).tools if t.name == name)
    assert tool.description is not None
    description = " ".join(tool.description.split())
    assert "`storageState`" in description
    assert "absolute path" in description
    assert "never written" in description
