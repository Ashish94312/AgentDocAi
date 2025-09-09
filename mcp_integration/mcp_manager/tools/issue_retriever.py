from crewai.tools import BaseTool
from ..utils_optimized import mcp_tool_optimized


class GetIssueTool(BaseTool):
    name: str = "get_issue"
    description: str = "Fetch and provide a list of open issues from a GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str) -> list:
        """Fetch and provide a list of open issues from a GitHub repository using the MCP server.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
        
        Returns:
            List of open issues in the repository
        """
        print(f"Issue Retriever: getting open issues for {owner}/{repo}")
        result = mcp_tool_optimized([
            'tools', 'list_issues',
            '--owner', owner,
            '--repo', repo,
            '--state', 'open',
            '--perPage', '5',
            '--page', '1'
        ])

        if isinstance(result, list):
            return result
        else:
            print(f"Issue Retriever: Unexpected result: {result}")
            return []


get_issue = GetIssueTool()

