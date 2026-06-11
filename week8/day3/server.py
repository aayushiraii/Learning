from mcp.server.fastmcp import FastMCP
import os

print(f"SERVER PID = {os.getpid()}")

mcp = FastMCP("Learning MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello {name}"


if __name__ == "__main__":
    mcp.run()