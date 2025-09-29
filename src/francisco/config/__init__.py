"""Configuration files for the Francisco agent package."""

from pathlib import Path

# Get the directory containing this file
CONFIG_DIR = Path(__file__).parent

# Default configuration files
DEFAULT_CONFIG_FILE = CONFIG_DIR / "francisco.yaml"
DEFAULT_PROMPT_FILE = CONFIG_DIR / "francisco_prompt.txt"

__all__ = ["CONFIG_DIR", "DEFAULT_CONFIG_FILE", "DEFAULT_PROMPT_FILE"]
