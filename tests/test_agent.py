"""Tests for Francisco agent."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from francisco.agent import FranciscoAgent, Config, Personality, Capabilities
from francisco.logger import LogConfig, LogLevel


class TestConfig:
    """Test Config model."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config(
            name="test-agent",
            description="Test agent description"
        )
        
        assert config.name == "test-agent"
        assert config.description == "Test agent description"
        assert config.model == "gpt-5-mini"
        assert config.max_iterations == 10
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            name="custom-agent",
            description="Custom agent",
            model="gpt-3.5-turbo",
            max_iterations=5
        )
        
        assert config.model == "gpt-3.5-turbo"
        assert config.max_iterations == 5


class TestPersonality:
    """Test Personality model."""
    
    def test_default_personality(self):
        """Test default personality configuration."""
        personality = Personality()
        
        assert personality.primary_traits == []
        assert personality.communication_style == []
    
    def test_custom_personality(self):
        """Test custom personality configuration."""
        personality = Personality(
            primary_traits=["intelligent", "methodical"],
            communication_style=["direct", "precise"]
        )
        
        assert personality.primary_traits == ["intelligent", "methodical"]
        assert personality.communication_style == ["direct", "precise"]


class TestCapabilities:
    """Test Capabilities model."""
    
    def test_default_capabilities(self):
        """Test default capabilities configuration."""
        capabilities = Capabilities()
        
        assert capabilities.programming_languages == {}
        assert capabilities.frameworks_and_tools == []
        assert capabilities.project_types == []
    
    def test_custom_capabilities(self):
        """Test custom capabilities configuration."""
        capabilities = Capabilities(
            programming_languages={"primary": "Python", "secondary": ["Bash"]},
            frameworks_and_tools=["pixi", "pydantic"],
            project_types=["CLI", "API"]
        )
        
        assert capabilities.programming_languages["primary"] == "Python"
        assert capabilities.frameworks_and_tools == ["pixi", "pydantic"]
        assert capabilities.project_types == ["CLI", "API"]


class TestFranciscoAgent:
    """Test FranciscoAgent class."""
    
    @pytest.fixture
    def mock_config_file(self, tmp_path):
        """Create a mock configuration file."""
        config_data = {
            "agent": {
                "name": "test-francisco",
                "description": "Test Francisco agent",
                "model": "gpt-4o",
                "max_iterations": 5,
                "personality": {
                    "primary_traits": ["intelligent", "methodical"],
                    "communication_style": ["direct", "precise"]
                },
                "core_objectives": {
                    "primary_goal": "Test self-replication",
                    "secondary_goals": ["Learn", "Improve"]
                },
                "capabilities": {
                    "programming_languages": {"primary": "Python"},
                    "frameworks_and_tools": ["pixi", "pydantic"],
                    "project_types": ["CLI", "API"]
                },
                "self_replication_strategy": {
                    "approach": "Test approach",
                    "quality_standards": ["Clean code", "Tests"]
                },
                "working_principles": {
                    "code_quality": ["Write tests", "Use type hints"]
                },
                "interaction_guidelines": {
                    "when_invoked": ["Be helpful", "Be precise"]
                },
                "limitations_and_boundaries": ["Python only", "No breaking changes"]
            }
        }
        
        config_file = tmp_path / "francisco.yaml"
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        return str(config_file)
    
    @patch('francisco.agent.Agent')
    def test_agent_initialization(self, mock_agent_class, mock_config_file):
        """Test agent initialization."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        
        assert agent.config.name == "test-francisco"
        assert agent.config.description == "Test Francisco agent"
        assert agent.config.model == "gpt-4o"
        assert agent.config.max_iterations == 5
        assert agent.api_key == "test-api-key"
        mock_agent_class.assert_called_once()
    
    @patch('francisco.agent.Agent')
    def test_agent_initialization_without_config(self, mock_agent_class):
        """Test agent initialization without config file."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        with patch('francisco.agent.Path') as mock_path:
            mock_path.return_value.parent.parent.parent = Path("/fake/path")
            mock_config_file = Mock()
            mock_config_file.exists.return_value = False
            
            with pytest.raises(Exception):
                FranciscoAgent(api_key="test-api-key")
    
    @patch('francisco.agent.Agent')
    def test_build_system_prompt(self, mock_agent_class, mock_config_file):
        """Test system prompt building."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        prompt = agent._build_system_prompt()
        
        assert "test-francisco" in prompt
        assert "Test Francisco agent" in prompt
        assert "Test self-replication" in prompt
        assert "Python" in prompt
        assert "Clean code" in prompt
    
    @patch('francisco.agent.Agent')
    @patch('francisco.agent.Runner')
    @pytest.mark.asyncio
    async def test_invoke_agent(self, mock_runner, mock_agent_class, mock_config_file):
        """Test agent invocation."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = Mock()
        mock_result.final_output = "Test response"
        mock_runner.run = AsyncMock(return_value=mock_result)
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        response = await agent.invoke("Test input")
        
        assert response == "Test response"
        mock_runner.run.assert_called_once()
    
    @patch('francisco.agent.Agent')
    @patch('francisco.agent.Runner')
    @pytest.mark.asyncio
    async def test_invoke_agent_with_context(self, mock_runner, mock_agent_class, mock_config_file):
        """Test agent invocation with context."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = Mock()
        mock_result.final_output = "Test response with context"
        mock_runner.run = AsyncMock(return_value=mock_result)
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        context = {"project": "test-project"}
        response = await agent.invoke("Test input", context)
        
        assert response == "Test response with context"
        mock_runner.run.assert_called_once()
        # Check that context was included in the input
        call_args = mock_runner.run.call_args
        input_text = call_args[1]["input"]
        assert "Additional context: {'project': 'test-project'}" in input_text
    
    @patch('francisco.agent.Agent')
    def test_str_representation(self, mock_agent_class, mock_config_file):
        """Test string representation of agent."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        agent_str = str(agent)
        
        assert agent_str == "test-francisco: Test Francisco agent"
    
    @patch('francisco.agent.Agent')
    @patch('francisco.agent.Runner')
    def test_invoke_sync(self, mock_runner, mock_agent_class, mock_config_file):
        """Test synchronous agent invocation."""
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = Mock()
        mock_result.final_output = "Test sync response"
        mock_runner.run_sync.return_value = mock_result
        
        agent = FranciscoAgent(mock_config_file, "test-api-key")
        response = agent.invoke_sync("Test sync input")
        
        assert response == "Test sync response"
        mock_runner.run_sync.assert_called_once()
