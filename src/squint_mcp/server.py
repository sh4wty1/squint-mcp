"""The Squint MCP server: creates it and registers its tools."""

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from squint_mcp import SERVER_NAME, __version__
from squint_mcp.tools.ping import ping

server = MCPServer(SERVER_NAME, version=__version__)

server.add_tool(
    ping,
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
