"""Francisco agent implementation with self-replication capabilities."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents import Agent, Runner

from .agent_models import AgentConfig, RuntimeConfig
from .config import DEFAULT_CONFIG_FILE
from .logger import get_logger, LogConfig


class FranciscoAgent:
    """Francisco - A helpful self-replicating AI assistant specialized in self-development and self-improvement."""
    
    def __init__(self, config_path: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize the Francisco agent.
        
        Args:
            config_path: Path to the YAML configuration file. If None, uses default path.
            api_key: OpenAI API key. If None, will try to get from environment.
        """
        self.logger = get_logger("francisco-agent")
        
        # Load configuration
        if config_path is None:
            config_path = str(DEFAULT_CONFIG_FILE)
        
        self.config = self._load_config(config_path)
        
        # Set API key for openai-agents
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Set environment variable for openai-agents
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        # Initialize the openai-agents Agent
        self.agent = Agent(
            name=self.config.name,
            instructions=self._build_system_prompt(),
            model=self.config.model,
        )
        
        self.logger.info(f"Francisco agent initialized: {self.config.description}")
    
    def _load_config(self, config_path: str) -> AgentConfig:
        """Load agent configuration from YAML file.
        
        Args:
            config_path: Path to the configuration file.
            
        Returns:
            Loaded agent configuration.
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            agent_data = config_data.get('agent', {})
            return AgentConfig(**agent_data)
        
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent using template.

        Returns:
            Formatted system prompt string.
        """
        # Get the template from the config
        template = self.config.prompt_template

        # Prepare template data using model string representations
        template_data = {
            'name': self.config.name,
            'description': self.config.description,
            'core_objectives': str(self.config.core_objectives),
            'personality': str(self.config.personality),
            'capabilities': str(self.config.capabilities),
            'self_replication_strategy': str(self.config.self_replication_strategy),
            'working_principles': str(self.config.working_principles),
            'interaction_guidelines': str(self.config.interaction_guidelines),
            'success_metrics': str(self.config.success_metrics),
            'limitations_and_boundaries': str(self.config.limitations_and_boundaries)
        }

        # Format the template
        return template.format(**template_data)
    
    async def invoke(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Invoke the Francisco agent with user input.
        
        Args:
            user_input: The user's request or input.
            context: Optional context information.
            
        Returns:
            Agent's response as a string.
        """
        self.logger.info(f"Francisco agent invoked with input: {user_input[:100]}...")
        
        try:
            # Prepare input with context if provided
            full_input = user_input
            if context:
                context_str = f"Additional context: {context}\n\n"
                full_input = context_str + user_input
            
            # Use openai-agents Runner to execute the agent
            result = await Runner.run(
                self.agent,
                input=full_input,
                max_turns=self.config.max_iterations
            )
            
            agent_response = result.final_output
            self.logger.info("Francisco agent response generated successfully")
            
            return agent_response or "I apologize, but I couldn't generate a response. Please try again."
        
        except Exception as e:
            self.logger.error(f"Error invoking Francisco agent: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    def invoke_sync(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Synchronous version of invoke method.
        
        Args:
            user_input: The user's request or input.
            context: Optional context information.
            
        Returns:
            Agent's response as a string.
        """
        self.logger.info(f"Francisco agent invoked (sync) with input: {user_input[:100]}...")
        
        try:
            # Prepare input with context if provided
            full_input = user_input
            if context:
                context_str = f"Additional context: {context}\n\n"
                full_input = context_str + user_input
            
            # Use openai-agents Runner to execute the agent synchronously
            result = Runner.run_sync(
                self.agent,
                input=full_input,
                max_turns=self.config.max_iterations
            )
            
            agent_response = result.final_output
            self.logger.info("Francisco agent response generated successfully")
            
            return agent_response or "I apologize, but I couldn't generate a response. Please try again."
        
        except Exception as e:
            self.logger.error(f"Error invoking Francisco agent: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.config.name}: {self.config.description}"
