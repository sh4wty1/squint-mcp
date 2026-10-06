"""Tests drive the server only through an in-memory MCP client."""

from collections.abc import AsyncIterator

import pytest
from mcp import Client

from squint_mcp.server import server


@pytest.fixture
async def client() -> AsyncIterator[Client]:
    async with Client(server) as connected:
        yield connected
