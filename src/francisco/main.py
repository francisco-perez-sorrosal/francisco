"""Main CLI entry point for Francisco MCP server."""

import os
import asyncio
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from . import __version__
from .agent import FranciscoAgent
from .mcp_server import main as run_mcp_server
from .logger import get_logger, LogConfig, LogLevel

# Load environment variables
load_dotenv()

# Initialize CLI app and console
app = typer.Typer(
    name="francisco",
    help="Francisco - MCP server with agentic AI for self-replication",
    add_completion=False
)
console = Console()
logger = get_logger("francisco-cli")


@app.command()
def version():
    """Show Francisco version information."""
    rprint(f"[bold blue]Francisco[/bold blue] v[bold green]{__version__}[/bold green]")
    rprint(f"[dim]MCP server with agentic AI for self-replication[/dim]")


@app.command()
def config(
    config_path: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to Francisco configuration file"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k", help="OpenAI API key"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level"
    )
):
    """Show Francisco agent configuration and status."""
    try:
        # Configure logging
        log_config = LogConfig(level=LogLevel(log_level.upper()))
        from .logger import configure_logger
        configure_logger(log_config)
        
        # Initialize agent
        agent = FranciscoAgent(config_path, api_key)
        
        # Create rich display using the agent's __str__ method
        title = Text("Francisco Agent Configuration", style="bold blue")

        # Use the agent's configuration __str__ method for clean display
        # Avoid Rich markup conflicts by using str() directly
        content = str(agent.config)

        panel = Panel(
            content,
            title=title,
            border_style="blue",
            padding=(1, 2)
        )
        
        console.print(panel)
        
    except Exception as e:
        rprint(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def test_agent(
    input_text: str = typer.Argument(..., help="Input text for the agent"),
    config_path: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to Francisco configuration file"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k", help="OpenAI API key"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level"
    )
):
    """Test Francisco agent with input text."""
    async def run_test():
        try:
            # Configure logging
            log_config = LogConfig(level=LogLevel(log_level.upper()))
            from .logger import configure_logger
            configure_logger(log_config)
            
            # Initialize agent
            agent = FranciscoAgent(config_path, api_key)
            
            rprint(f"[bold blue]Testing Francisco Agent[/bold blue]")
            rprint(f"[dim]Input:[/dim] {input_text}")
            rprint()
            
            # Invoke agent
            response = await agent.invoke(input_text)
            
            # Display response
            title = Text("Francisco Agent Response", style="bold green")
            panel = Panel(
                response,
                title=title,
                border_style="green",
                padding=(1, 2)
            )
            
            console.print(panel)
            
        except Exception as e:
            rprint(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(1)
    
    asyncio.run(run_test())


@app.command()
def serve(
    config_path: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to Francisco configuration file"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k", help="OpenAI API key"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level"
    )
):
    """Start the Francisco MCP server."""
    try:
        # Configure logging
        log_config = LogConfig(level=LogLevel(log_level.upper()))
        from .logger import configure_logger
        configure_logger(log_config)

        # Set environment variables for the MCP server
        if config_path:
            os.environ["FRANCISCO_CONFIG_PATH"] = config_path
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        rprint("[bold blue]🚀 Starting Francisco MCP Server[/bold blue]")
        rprint("[dim]✨ Initializing agent with self-replication capabilities...[/dim]")
        rprint("[dim]🎯 Ready to assist with Python development tasks![/dim]")
        rprint()

        # Run the simplified MCP server
        run_mcp_server()

    except KeyboardInterrupt:
        rprint("\n[bold yellow]👋 Francisco MCP Server stopped[/bold yellow]")
    except Exception as e:
        rprint(f"[bold red]❌ Error starting server:[/bold red] {e}")
        raise typer.Exit(1)



def main():
    """Main entry point."""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        rprint("[bold yellow]⚠️  Warning: OPENAI_API_KEY not found in environment[/bold yellow]")
        rprint("[dim]Set OPENAI_API_KEY environment variable or use --api-key option[/dim]")
    
    app()


if __name__ == "__main__":
    main()
