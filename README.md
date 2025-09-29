# Francisco - MCP Server with Agentic AI

Francisco is a Model Context Protocol (MCP) server that exposes an intelligent AI agent specialized in Python development and self-replication. The agent, named Francisco, is designed to assist with creating, improving, and replicating Python projects using modern development practices.

## Features

- 🤖 **Intelligent AI Agent**: Francisco agent specialized in Python development and self-replication
- 🔧 **MCP Integration**: Simplified FastMCP server implementation
- 🚀 **Self-Replication**: Agent designed to create and improve Python projects
- 📦 **Modern Tooling**: Built with pixi, Pydantic, loguru, typer, and rich
- 🧪 **Comprehensive Testing**: Full test suite with pytest
- 🎨 **Beautiful CLI**: Rich terminal interface with colorful output
- ⚙️ **Configurable**: YAML-based agent configuration with template system
- 🔌 **Easy Integration**: FastMCP decorator-based tool registration

## Quick Start

### Prerequisites

- Python 3.11+
- [pixi](https://pixi.sh/) package manager
- OpenAI API key

### Installation

1. **Clone and setup the project:**

   ```bash
   git clone <repository-url>
   cd francisco
   ```

2. **Install dependencies with pixi:**

   ```bash
   pixi install
   ```

3. **Set your OpenAI API key:**

   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Start the MCP server:**

   ```bash
   pixi run serve
   ```

## Usage

### CLI Commands

#### Show Version

```bash
pixi run cli version
```

#### View Agent Configuration

```bash
pixi run config
```

#### Test Agent

```bash
pixi run cli test-agent "Create a simple Python CLI tool"
```

#### Start MCP Server

```bash
pixi run serve
```

### MCP Tools

When the MCP server is running, it exposes two tools:

#### `invoke`

Invoke Francisco agent for Python development and self-replication tasks.

**Parameters:**

- `input` (required): The request or task description for Francisco agent
- `context` (optional): Additional context information

**Example:**

```json
{
  "input": "Create a Python project for data analysis with pandas and matplotlib",
  "context": {
    "project_name": "data-analyzer",
    "target_directory": "/path/to/project"
  }
}
```

#### `status`

Get Francisco agent status and capabilities.

**Parameters:** None

**Example:**

```json
{}
```

## Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Francisco Agent Configuration
DEBUG=false
LOG_LEVEL=INFO
APP_NAME=francisco

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Agent Configuration
AGENT_NAME=francisco
AGENT_MODEL=gpt-4o
AGENT_MAX_ITERATIONS=10

# Self-replication settings
REPLICATION_TARGET_DIR=replicated_projects
ENABLE_GIT_OPERATIONS=true
ENABLE_GITHUB_OPERATIONS=false
```

### Agent Configuration (francisco.yaml)

The agent's personality, capabilities, and behavior are configured in `francisco.yaml`. This file defines:

- **Personality traits** and communication style
- **Core objectives** and goals
- **Capabilities** and supported technologies
- **Self-replication strategy** and quality standards
- **Working principles** and interaction guidelines
- **Success metrics** for evaluating agent performance
- **Limitations and boundaries** for safe operation

The configuration uses a structured Pydantic model system with individual components:

- `SuccessMetrics`: Defines measurable success criteria
- `LimitationsAndBoundaries`: Sets operational constraints
- `Personality`, `Capabilities`, `Strategy`: Modular configuration components

Each component renders to XML format in the agent's prompt template, providing clear structure and easy customization.

## Development

### Project Structure

```text
francisco/
├── src/francisco/           # Main package
│   ├── __init__.py         # Package initialization
│   ├── agent.py            # Francisco agent implementation
│   ├── agent_models.py     # Pydantic models for agent configuration
│   ├── config/             # Configuration files
│   │   ├── __init__.py
│   │   ├── francisco.yaml  # Agent configuration
│   │   └── francisco_prompt.txt # Agent prompt template
│   ├── logger.py           # Logging configuration
│   ├── main.py             # CLI entry point
│   └── mcp_server.py       # Simplified FastMCP server implementation
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_logger.py
│   └── test_main.py
├── francisco.yaml          # Root agent configuration
├── pyproject.toml          # Project configuration with pixi tasks
└── README.md              # This file
```

### Development Commands

```bash
# Install dependencies
pixi install

# Run tests
pixi run test

# Format code
pixi run format

# Lint code
pixi run lint

# Run both lint and test
pixi run check

# Run the CLI (shows help)
pixi run cli

# Start the MCP server
pixi run serve

# Show agent configuration
pixi run config
```

### Testing

The project includes comprehensive tests:

```bash
# Run all tests
pixi run test

# Run specific test file
pixi run pytest tests/test_agent.py -v

# Run with coverage
pixi run pytest --cov=src/francisco tests/
```

## Agent Configuration Templates

Francisco's capabilities, personality, and behavior are defined in template files:

### Agent Configuration

See [`src/francisco/config/francisco.yaml`](src/francisco/config/francisco.yaml) for the complete agent configuration including:

- **Personality traits** and communication style
- **Core objectives** and goals
- **Programming languages** and frameworks
- **Project types** and capabilities
- **Working principles** and quality standards
- **Success metrics** and limitations

### Agent Prompt Template

The agent's system prompt is defined in [`src/francisco/config/francisco_prompt.txt`](src/francisco/config/francisco_prompt.txt), which uses placeholder substitution to incorporate all configuration elements into a structured prompt.

### Configuration Model

The [`src/francisco/agent_models.py`](src/francisco/agent_models.py) file contains the Pydantic models that define the structure and validation for all agent configuration components.

## Self-Replication Strategy

Francisco follows a systematic approach to self-replication:

1. **Analyze** existing projects and identify improvement opportunities
2. **Create** new Python projects with modern tooling and best practices
3. **Establish** automated workflows and CI/CD pipelines
4. **Document** and share knowledge through comprehensive README files
5. **Iterate** and improve based on feedback and usage patterns

### Quality Standards

- Code is executable and functional
- Code is clean and readable
- Code is maintainable and scalable
- Code is documented and has good comments
- Always use pixi for dependency management
- Implement comprehensive testing with pytest
- Use Pydantic for data validation and configuration
- Follow modern Python packaging standards (PEP 621)
- Include proper logging with loguru
- Create beautiful CLIs with typer and rich
- Set up automated formatting and linting with ruff
- Use FastMCP for simplified MCP server implementation
- Document everything thoroughly

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pixi run test`
5. Format and lint: `pixi run format && pixi run lint`
6. Commit your changes: `git commit -m "Add feature"`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [FastMCP](https://github.com/pydantic/fastmcp) for simplified MCP server implementation
- [OpenAI Agents](https://openai.github.io/openai-agents-python/) for agent capabilities
- [pixi](https://pixi.sh/) for modern Python package management
- [Pydantic](https://pydantic.dev/) for data validation and configuration modeling
- All the amazing open-source tools that make this project possible

---

**Francisco** - *Intelligent Python development assistant with self-replication capabilities* 🤖✨
