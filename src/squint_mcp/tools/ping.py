"""The `ping` tool: confirms the server is alive."""

from pydantic import BaseModel

from squint_mcp import SERVER_NAME, __version__


class PingResult(BaseModel):
    name: str
    version: str
    message: str | None


def ping(message: str | None = None) -> PingResult:
    """Confirm the server is alive.

    Returns the server name and version, and echoes `message` when given.
    """
    return PingResult(name=SERVER_NAME, version=__version__, message=message)
