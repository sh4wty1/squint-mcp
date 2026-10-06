"""Tests drive the server only through an in-memory MCP client."""

import threading
from collections.abc import AsyncIterator, Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest
from mcp import Client

from squint_mcp.server import server

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def client(anyio_backend: str) -> AsyncIterator[Client]:
    """One client for the whole run: one server lifespan, so one Chromium."""
    async with Client(server) as connected:
        yield connected


@pytest.fixture
async def client_without_chromium(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> AsyncIterator[Client]:
    """A second server lifespan, whose Playwright driver finds no browser installed."""
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", str(tmp_path))
    async with Client(server) as connected:
        yield connected


_server_closing = threading.Event()


class _FixtureHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/tick":
            self.send_response(204)
            self.end_headers()
        elif self.path == "/hang":
            # Never answers: the page stays stuck before `load`.
            _server_closing.wait()
        else:
            super().do_GET()

    def log_message(self, format: str, *args: Any) -> None:
        pass


@pytest.fixture(scope="session")
def local_server() -> Iterator[str]:
    """Serves the fixtures over HTTP, for behaviour that needs a network."""
    handler = partial(_FixtureHandler, directory=str(FIXTURES))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as httpd:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        yield f"http://127.0.0.1:{httpd.server_port}"
        _server_closing.set()
        httpd.shutdown()
