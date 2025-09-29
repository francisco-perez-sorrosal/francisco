#!/usr/bin/env python3
"""Test script to verify Francisco setup."""

import sys
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from francisco import get_logger
        from francisco.logger import LogConfig, LogLevel
        from francisco.agent import FranciscoAgent, AgentConfig, AgentPersonality, AgentCapabilities
        from francisco.mcp_server import FranciscoMCPServer
        from francisco.main import app
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_logger():
    """Test logger configuration."""
    try:
        from francisco.logger import LogConfig, LogLevel, configure_logger, get_logger
        
        # Test configuration
        config = LogConfig(level=LogLevel.INFO)
        assert config.level == LogLevel.INFO
        assert config.colorize is True
        
        # Test logger creation
        logger = get_logger("test")
        assert logger is not None
        
        print("✅ Logger configuration successful")
        return True
    except Exception as e:
        print(f"❌ Logger test error: {e}")
        return False

def test_agent_config():
    """Test agent configuration models."""
    try:
        from francisco.agent import AgentConfig, AgentPersonality, AgentCapabilities
        
        # Test personality
        personality = AgentPersonality(
            primary_traits=["intelligent", "methodical"],
            communication_style=["direct", "precise"]
        )
        assert len(personality.primary_traits) == 2
        
        # Test capabilities
        capabilities = AgentCapabilities(
            programming_languages={"primary": "Python"},
            frameworks_and_tools=["pixi", "pydantic"],
            project_types=["CLI", "API"]
        )
        assert capabilities.programming_languages["primary"] == "Python"
        
        print("✅ Agent configuration models successful")
        return True
    except Exception as e:
        print(f"❌ Agent config test error: {e}")
        return False

def test_yaml_config():
    """Test YAML configuration file exists and is valid."""
    try:
        import yaml
        from pathlib import Path
        
        config_path = Path(__file__).parent.parent / "francisco.yaml"
        assert config_path.exists(), "francisco.yaml not found"
        
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        assert "agent" in config_data, "No 'agent' section in YAML"
        agent_data = config_data["agent"]
        assert "name" in agent_data, "No 'name' in agent config"
        assert agent_data["name"] == "francisco", "Agent name should be 'francisco'"
        
        print("✅ YAML configuration file valid")
        return True
    except Exception as e:
        print(f"❌ YAML config test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Francisco setup...\n")
    
    tests = [
        test_imports,
        test_logger,
        test_agent_config,
        test_yaml_config,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Francisco setup is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
