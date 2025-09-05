# RepoDoc-AI

An intelligent documentation generation system that leverages AI agents and the Model Context Protocol (MCP) to automatically analyze GitHub repositories and generate comprehensive documentation.

## Overview

RepoDoc-AI combines the power of CrewAI multi-agent systems with GitHub's MCP server to create an automated documentation pipeline. The system analyzes repository structure, issues, pull requests, and branches to generate structured, markdown-based documentation that helps developers quickly understand project organization and status.

## Architecture Design

### System Components

The RepoDoc-AI system consists of several key components working together to provide intelligent repository analysis and documentation generation:

#### 1. **Django Web Application** (`mcp_integration/`)
- **Purpose**: Provides the web interface and orchestrates the documentation generation process
- **Key Files**:
  - `mcp_manager/views.py`: Main view controllers handling user requests
  - `mcp_manager/settings.py`: Configuration management with environment variables
  - `mcp_manager/urls.py`: URL routing for the web interface

#### 2. **CrewAI Multi-Agent System** (`mcp_manager/agents/`, `mcp_manager/crews/`, `mcp_manager/tasks/`)
- **Purpose**: Orchestrates specialized AI agents to perform different aspects of repository analysis
- **Agents**:
  - **Repository Structure Auditor**: Analyzes folder and file structure
  - **GitHub Issue Analyst**: Fetches and prioritizes open issues
  - **Pull Request Reporter**: Lists and analyzes recent pull requests
  - **Branch Reporter**: Examines repository branches and their purposes
- **Crew Management**: Sequential task execution with specialized tools for each agent

#### 3. **MCP Integration Layer** (`mcp_manager/tools/`, `mcp_manager/utils.py`)
- **Purpose**: Bridges the Django application with the GitHub MCP server
- **Key Components**:
  - **Custom Tools**: CrewAI-compatible tools that wrap MCP server calls
  - **MCP Utility**: Direct communication with GitHub MCP server via subprocess
  - **Tool Implementations**:
    - `directory_scanner.py`: Repository file structure analysis
    - `issue_retriever.py`: GitHub issues fetching
    - `pull_request_lister.py`: Pull request analysis
    - `branch_lister.py`: Branch information retrieval

#### 4. **GitHub MCP Server** (`github-mcp-server/`)
- **Purpose**: Provides direct access to GitHub's API through the Model Context Protocol
- **Features**:
  - Comprehensive GitHub API coverage (repos, issues, PRs, actions, security)
  - Toolset-based configuration for selective functionality
  - Both local and remote deployment options
  - Support for GitHub Enterprise Server

### Data Flow Architecture

```
User Input (GitHub URL)
    ↓
Django Web Interface
    ↓
Repository URL Parsing (extract_owner_repo)
    ↓
CrewAI Crew Initialization
    ↓
Multi-Agent Task Distribution:
    ├── Repository Structure Analysis
    ├── Issues Analysis
    ├── Pull Requests Analysis
    └── Branches Analysis
    ↓
MCP Tool Execution (via utils.py)
    ↓
GitHub MCP Server Communication
    ↓
GitHub API Calls
    ↓
Data Processing & Analysis
    ↓
Markdown Documentation Generation
    ↓
HTML Conversion & Display
```

### Technology Stack

#### Backend Technologies
- **Django 4.2**: Web framework for the main application
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and tool management
- **OpenAI GPT-3.5-turbo**: Language model for analysis and content generation

#### Integration Technologies
- **Model Context Protocol (MCP)**: Standardized communication protocol
- **GitHub MCP Server**: Go-based server providing GitHub API access
- **Subprocess Communication**: Direct process communication for MCP calls

#### Frontend Technologies
- **Django Templates**: Server-side rendering
- **HTML/CSS**: User interface presentation
- **Markdown**: Documentation format with HTML conversion

### Configuration Management

The system uses environment-based configuration for security and flexibility:

```python
# Environment Variables
GITHUB_PERSONAL_ACCESS_TOKEN  # GitHub API authentication
OPENAI_API_KEY               # OpenAI API for LLM operations
```

### Security Considerations

1. **Token Management**: GitHub tokens are stored as environment variables, never in code
2. **Input Validation**: Repository URL validation and sanitization
3. **Error Handling**: Comprehensive error handling for API failures and timeouts
4. **Process Isolation**: MCP server runs in isolated subprocess environment

### Scalability Features

1. **Modular Agent Design**: Each agent can be scaled independently
2. **Toolset Configuration**: Selective GitHub API access based on requirements
3. **Caching Support**: CrewAI provides built-in caching mechanisms
4. **Async Processing**: Subprocess-based MCP communication for non-blocking operations

### Deployment Architecture

#### Local Development
- Django development server
- Local GitHub MCP server binary
- SQLite database for session management

#### Production Considerations
- WSGI/ASGI deployment (Gunicorn/Uvicorn)
- PostgreSQL/MySQL for production database
- Docker containerization for MCP server
- Environment variable configuration
- Static file serving optimization

### API Integration Points

1. **GitHub API**: Repository data, issues, pull requests, branches
2. **OpenAI API**: Content analysis and documentation generation
3. **MCP Protocol**: Standardized tool communication
4. **Django ORM**: Local data persistence and session management

This architecture provides a robust, scalable foundation for automated repository documentation while maintaining security, flexibility, and extensibility for future enhancements.

## Installation

### Prerequisites

1. **Python 3.8+**: Required for Django and CrewAI
2. **Go 1.19+**: Required for building the GitHub MCP server
3. **Git**: For cloning the repository
4. **GitHub Personal Access Token**: For GitHub API access
5. **OpenAI API Key**: For AI-powered analysis

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd AgentDocAi
```

#### 2. Build the GitHub MCP Server
```bash
cd github-mcp-server
go build -o github-mcp-server cmd/github-mcp-server/main.go
cd ..
```

#### 3. Set Up Python Environment
```bash
cd mcp_integration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the `mcp_integration` directory:
```bash
# GitHub Configuration
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

#### 5. Set Up Django Database
```bash
python manage.py migrate
```

#### 6. Run the Application
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. **Access the Documentation Interface**: Navigate to the web interface
2. **Enter Repository URL**: Provide a GitHub repository URL (e.g., `https://github.com/owner/repo`)
3. **Generate Documentation**: Click the generate button to start the analysis
4. **View Results**: The system will display comprehensive documentation including:
   - Repository structure analysis
   - Open issues summary and prioritization
   - Recent pull requests overview
   - Branch information and analysis

### Generated Documentation Structure

The system generates the following documentation files:

- **`repo_structure.md`**: Hierarchical file and folder structure with clickable links
- **`report_issues.md`**: Analysis of open issues with prioritization recommendations
- **`pull_requests.md`**: Summary of recent pull requests and their status
- **`branches.md`**: Overview of repository branches and their purposes
- **`summary.md`**: Combined documentation with all analyses

### API Integration

The system can also be integrated programmatically:

```python
from mcp_manager.crews.crew import build_crew

# Initialize crew for repository analysis
crew = build_crew("owner", "repository_name")

# Execute analysis
result = crew.kickoff()

# Access generated documentation
# Files are saved in the generate_docs/ directory
```

## Features

### Multi-Agent Analysis
- **Repository Structure Auditor**: Creates navigable file trees with GitHub links
- **Issue Analyst**: Identifies and prioritizes critical issues
- **Pull Request Reporter**: Analyzes recent development activity
- **Branch Reporter**: Examines branching strategy and purposes

### Intelligent Documentation
- **Markdown Generation**: Clean, readable documentation format
- **HTML Conversion**: Web-friendly display with proper formatting
- **Link Integration**: Direct links to GitHub resources
- **Categorization**: Intelligent grouping of related information

### GitHub Integration
- **Comprehensive API Access**: Full GitHub repository data access
- **Real-time Data**: Always up-to-date information
- **Secure Authentication**: Token-based secure access
- **Rate Limit Handling**: Proper API usage management

## Development

### Project Structure
```
AgentDocAi/
├── github-mcp-server/          # GitHub MCP server (Go)
│   ├── cmd/                   # Server binaries
│   ├── pkg/                   # GitHub API tools
│   └── internal/              # Internal server components
├── mcp_integration/           # Django application
│   ├── mcp_manager/          # Main Django app
│   │   ├── agents/           # CrewAI agents
│   │   ├── crews/            # Agent orchestration
│   │   ├── tasks/            # Task definitions
│   │   ├── tools/            # MCP integration tools
│   │   └── templates/        # Web interface templates
│   └── generate_docs/        # Generated documentation output
└── README.md                 # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Testing

```bash
# Run Django tests
python manage.py test

# Test MCP integration
python test_mcp_direct.py
python test_mcp_robust.py
```

## Troubleshooting

### Common Issues

1. **MCP Server Not Found**: Ensure the GitHub MCP server is built and in the correct path
2. **Authentication Errors**: Verify your GitHub token has the necessary permissions
3. **OpenAI API Errors**: Check your API key and account limits
4. **Permission Denied**: Ensure proper file permissions for the MCP server binary

### Debug Mode

Enable debug logging by setting `DEBUG = True` in Django settings and check the console output for detailed error information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **GitHub MCP Server**: Model Context Protocol implementation
- **Django**: Web framework
- **OpenAI**: Language model services