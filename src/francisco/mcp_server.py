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

    status_text = f"""# Francisco Agent Status

{agent.config}"""

    return status_text


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Francisco MCP server...")
    mcp.run()


if __name__ == "__main__":
    main()
