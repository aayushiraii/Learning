from mcp.server.fastmcp import FastMCP

mcp = FastMCP("VoiceAgentServer")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather information."""
    return f"The weather in {city} is sunny."

if __name__ == "__main__":
    mcp.run()