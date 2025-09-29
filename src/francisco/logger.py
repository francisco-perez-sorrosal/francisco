"""Logging configuration using loguru with custom colors and formatting."""

from enum import Enum
from typing import Optional

from loguru import logger
from pydantic import BaseModel


class LogLevel(str, Enum):
    """Log level enumeration."""
    
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogConfig(BaseModel):
    """Logging configuration model."""
    
    level: LogLevel = LogLevel.INFO
    format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    colorize: bool = True


def configure_logger(config: Optional[LogConfig] = None) -> None:
    """Configure loguru logger with custom colors and formatting.
    
    Args:
        config: Optional logging configuration. If None, uses default settings.
    """
    if config is None:
        config = LogConfig()
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with custom formatting and colors
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format=config.format,
        level=config.level.value,
        colorize=config.colorize,
        backtrace=True,
        diagnose=True,
    )


def get_logger(name: Optional[str] = None):
    """Get a configured logger instance.
    
    Args:
        name: Optional logger name. If provided, returns a child logger.
        
    Returns:
        Configured loguru logger instance.
    """
    if name:
        return logger.bind(name=name)
    return logger


# Configure default logger on import
configure_logger()
