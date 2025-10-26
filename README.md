# AgentDocAi

A Django app that generates documentation for GitHub repositories using AI agents and the Model Context Protocol (MCP).

## What it does

This tool analyzes GitHub repos and creates markdown documentation covering:
- Repository structure and file organization
- Open issues and their priority
- Recent pull requests
- Branch information

## Setup

### Prerequisites
- Python 3.8+
- Go 1.19+ (for the MCP server)
- GitHub Personal Access Token
- OpenAI API Key

### Installation

1. Clone the repo:
```bash
git clone <repository-url>
cd AgentDocAi
```

2. Build the MCP server:
```bash
cd github-mcp-server
go build -o github-mcp-server cmd/github-mcp-server/main.go
cd ..
```

3. Set up Python environment:
```bash
cd mcp_integration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Create `.env` file in `mcp_integration` directory:
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to use the web interface.

## How it works

The app uses CrewAI to coordinate multiple AI agents:
- **Repository Structure Auditor**: Scans file structure
- **Issue Analyst**: Fetches and prioritizes issues  
- **Pull Request Reporter**: Lists recent PRs
- **Branch Reporter**: Analyzes repository branches

Each agent uses MCP tools to communicate with the GitHub MCP server, which provides direct access to GitHub's API.

## Usage

1. Enter a GitHub repository URL in the web interface
2. Click generate to start the analysis
3. View the generated documentation

The system creates several markdown files in the `generate_docs/` directory:
- `repo_structure.md` - File tree with GitHub links
- `report_issues.md` - Issue analysis and priorities
- `pull_requests.md` - Recent PR summary
- `branches.md` - Branch information
- `summary.md` - Combined documentation

## Project Structure

```
AgentDocAi/
├── github-mcp-server/          # Go-based MCP server
├── mcp_integration/            # Django app
│   ├── mcp_manager/           # Main app
│   │   ├── agents/            # CrewAI agents
│   │   ├── crews/             # Agent orchestration
│   │   ├── tasks/             # Task definitions
│   │   ├── tools/             # MCP integration tools
│   │   └── templates/         # Web interface
│   └── generate_docs/         # Generated documentation
└── README.md
```

## Development

Run tests:
```bash
python manage.py test
```

## Troubleshooting

- **MCP Server Not Found**: Make sure you built the server binary
- **Authentication Errors**: Check your GitHub token permissions
- **OpenAI API Errors**: Verify your API key and account limits

## License

MIT License