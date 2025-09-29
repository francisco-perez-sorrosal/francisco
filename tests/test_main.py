"""Tests for main CLI module."""

import pytest
from unittest.mock import patch, Mock
import typer
from typer.testing import CliRunner

from francisco.main import app


class TestMainCLI:
    """Test main CLI functionality."""
    
    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()
    
    def test_version_command(self, runner):
        """Test version command."""
        result = runner.invoke(app, ["version"])
        
        assert result.exit_code == 0
        assert "Francisco" in result.output
        assert "v0.1.0" in result.output
    
    @patch('francisco.main.FranciscoAgent')
    def test_config_command(self, mock_agent_class, runner):
        """Test config command."""
        # Mock agent instance
        mock_agent = Mock()
        mock_config = Mock()
        mock_config.__str__ = Mock(return_value="Name: test-francisco\nDescription: Test agent\nModel: gpt-4o\nMax Iterations: 10\n\nCapabilities:\nPrimary Language: Python\nSecondary Languages: \nFrameworks & Tools: 2 tools\nProject Types: 1 types\n\nSelf-Replication Strategy:\nApproach: Test approach\nTargets: 1 categories\nQuality Standards: 1 standards")
        mock_agent.config = mock_config
        mock_agent_class.return_value = mock_agent
        
        result = runner.invoke(app, ["config"])
        
        assert result.exit_code == 0
        assert "test-francisco" in result.output
        assert "Test agent" in result.output
    
    @patch('francisco.main.FranciscoAgent')
    def test_config_command_with_options(self, mock_agent_class, runner):
        """Test config command with options."""
        mock_agent = Mock()
        mock_config = Mock()
        mock_config.__str__ = Mock(return_value="Name: test-francisco\nDescription: Test agent\nModel: gpt-4o\nMax Iterations: 10\n\nCapabilities:\nPrimary Language: Python\nSecondary Languages: \nFrameworks & Tools: 0 tools\nProject Types: 0 types\n\nSelf-Replication Strategy:\nApproach: Test approach\nTargets: 0 categories\nQuality Standards: 0 standards")
        mock_agent.config = mock_config
        mock_agent_class.return_value = mock_agent
        
        result = runner.invoke(app, [
            "config",
            "--config", "/fake/config.yaml",
            "--api-key", "fake-key",
            "--log-level", "DEBUG"
        ])
        
        assert result.exit_code == 0
        mock_agent_class.assert_called_once_with("/fake/config.yaml", "fake-key")
    
    @patch('francisco.main.FranciscoAgent')
    @patch('francisco.main.asyncio.run')
    def test_test_agent_command(self, mock_asyncio_run, mock_agent_class, runner):
        """Test test-agent command."""
        mock_agent = Mock()
        mock_agent.invoke = Mock(return_value="Test response")
        mock_agent_class.return_value = mock_agent
        
        # Mock the async run to call the coroutine directly
        async def mock_run(coro):
            return await coro
        
        mock_asyncio_run.side_effect = mock_run
        
        result = runner.invoke(app, [
            "test-agent",
            "Hello Francisco"
        ])
        
        assert result.exit_code == 0
        assert "Testing Francisco Agent" in result.output
        assert "Hello Francisco" in result.output
    
    @patch('francisco.main.FranciscoMCPServer')
    @patch('francisco.main.asyncio.run')
    def test_serve_command(self, mock_asyncio_run, mock_server_class, runner):
        """Test serve command."""
        mock_server = Mock()
        mock_server.run = Mock()
        mock_server_class.return_value = mock_server
        
        # Mock the async run
        async def mock_run(coro):
            await coro
        
        mock_asyncio_run.side_effect = mock_run
        
        with patch('francisco.main.time.sleep') as mock_sleep:
            mock_sleep.side_effect = KeyboardInterrupt()
            
            result = runner.invoke(app, ["serve"])
            
            assert result.exit_code == 0
            assert "Starting Francisco MCP Server" in result.output
    
    @patch('francisco.main.Path')
    @patch('francisco.main.shutil.copy')
    def test_init_command(self, mock_copy, mock_path, runner):
        """Test init command."""
        mock_path_instance = Mock()
        mock_path_instance.resolve.return_value = Mock()
        mock_path_instance.resolve.return_value.__truediv__ = Mock(return_value=Mock())
        mock_path.return_value = mock_path_instance
        
        # Mock file existence
        mock_env_file = Mock()
        mock_env_file.exists.return_value = False
        mock_env_example = Mock()
        mock_env_example.exists.return_value = True
        
        mock_path_instance.resolve.return_value.__truediv__.side_effect = [
            mock_env_file,  # .env
            mock_env_example,  # env.example
            Mock()  # francisco.yaml
        ]
        
        result = runner.invoke(app, ["init"])
        
        assert result.exit_code == 0
        assert "Initializing Francisco" in result.output
        assert "initialization complete" in result.output
    
    @patch('francisco.main.Path')
    def test_init_command_with_target(self, mock_path, runner):
        """Test init command with target directory."""
        mock_path_instance = Mock()
        mock_path_instance.resolve.return_value = Mock()
        mock_path_instance.resolve.return_value.__truediv__ = Mock(return_value=Mock())
        mock_path.return_value = mock_path_instance
        
        # Mock file existence
        mock_env_file = Mock()
        mock_env_file.exists.return_value = True  # .env already exists
        mock_path_instance.resolve.return_value.__truediv__.return_value = mock_env_file
        
        result = runner.invoke(app, ["init", "--target", "/fake/path"])
        
        assert result.exit_code == 0
        assert "Initializing Francisco in" in result.output
