"""The Squint MCP server: creates it and registers its tools."""

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from squint_mcp import SERVER_NAME, __version__
from squint_mcp.capture import browser_lifespan
from squint_mcp.tools.detect_visual_bugs import detect_visual_bugs
from squint_mcp.tools.inspect_element import inspect_element
from squint_mcp.tools.ping import ping

server = MCPServer(SERVER_NAME, version=__version__, lifespan=browser_lifespan)

server.add_tool(
    ping,
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
server.add_tool(
    inspect_element,
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True),
)
server.add_tool(
    detect_visual_bugs,
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True),
)


def main() -> None:
    """Serve MCP over stdio. stdout belongs to the protocol; logs go to stderr."""
    server.run()
