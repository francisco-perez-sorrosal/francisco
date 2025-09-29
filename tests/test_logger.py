"""Tests for logging configuration."""

import pytest
from francisco.logger import LogConfig, LogLevel, configure_logger, get_logger


class TestLogConfig:
    """Test LogConfig model."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = LogConfig()
        
        assert config.level == LogLevel.INFO
        assert config.colorize is True
        assert "time" in config.format
        assert "level" in config.format
        assert "message" in config.format
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = LogConfig(
            level=LogLevel.DEBUG,
            format="Custom format: {message}",
            colorize=False
        )
        
        assert config.level == LogLevel.DEBUG
        assert config.format == "Custom format: {message}"
        assert config.colorize is False


class TestLogLevel:
    """Test LogLevel enumeration."""
    
    def test_log_levels(self):
        """Test all log levels are available."""
        levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]
        
        for level in levels:
            assert isinstance(level.value, str)
            assert level.value.upper() == level.value


class TestLoggerFunctions:
    """Test logger utility functions."""
    
    def test_get_logger_without_name(self):
        """Test getting logger without name."""
        logger = get_logger()
        assert logger is not None
    
    def test_get_logger_with_name(self):
        """Test getting logger with name."""
        logger = get_logger("test-logger")
        assert logger is not None
    
    def test_configure_logger_default(self):
        """Test configuring logger with default settings."""
        # This should not raise an exception
        configure_logger()
    
    def test_configure_logger_custom(self):
        """Test configuring logger with custom settings."""
        config = LogConfig(level=LogLevel.DEBUG)
        
        # This should not raise an exception
        configure_logger(config)
