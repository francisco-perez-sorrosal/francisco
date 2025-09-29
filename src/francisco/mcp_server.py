"""Simplified MCP server implementation for Francisco agent using FastMCP."""

import os
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from .agent import FranciscoAgent
from .logger import get_logger

# Initialize the FastMCP server
mcp = FastMCP("Francisco Agent")

# Initialize the agent
logger = get_logger("francisco-mcp-server")
agent: Optional[FranciscoAgent] = None


def initialize_agent():
    """Initialize the Francisco agent with configuration."""
    global agent
    if agent is None:
        config_path = os.getenv("FRANCISCO_CONFIG_PATH")
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        agent = FranciscoAgent(config_path, api_key)
        logger.info("Francisco agent initialized")


@mcp.tool()
async def invoke(input: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Invoke Francisco agent for Python development and self-replication tasks.

    Args:
        input: The request or task description for Francisco agent
        context: Optional context information for the agent

    Returns:
        Agent response as a string
    """

    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("[bold red]❌  Warning: OPENAI_API_KEY not found in environment[/bold red]")
        logger.error("[dim]Set OPENAI_API_KEY environment variable or use --api-key option[/dim]")
        return "OPENAI_API_KEY not found in environment!"
    
    
    initialize_agent()
    logger.info(f"Invoking agent with input: {input}")

    if agent is None:
        raise RuntimeError("Agent not properly initialized")

    try:
        response = await agent.invoke(input, context)
        return response
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise


@mcp.tool()
async def status() -> str:
    """Get Francisco agent status and capabilities.

    Returns:
        Agent status and configuration information
    """
    initialize_agent()

    if agent is None:
        raise RuntimeError("Agent not properly initialized")

    status_text = f"""# Francisco Agent Status\n\n{agent.config}"""

    return status_text


def main(transport: str = "stdio"):
    """Main entry point for the MCP server.

    Args:
        transport: Transport type - "stdio" or "streamable-http"
    """
    match transport:
        case "streamable-http":
            # Configure for HTTP transport
            mcp.run(transport="streamable-http")
        case "stdio":
            # Default to stdio transport for "stdio" or any other value
            mcp.run(transport="stdio")
        case _:
            raise ValueError(f"Invalid transport: {transport}")

    logger.info(f"Starting Francisco MCP server with {transport} transport...")


if __name__ == "__main__":
    main()
