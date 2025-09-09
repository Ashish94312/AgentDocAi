from crewai.tools import BaseTool
from mcp_manager.utils_optimized import mcp_tool_optimized


class GetPullRequestsTool(BaseTool):
    name: str = "get_pull_requests"
    description: str = "Fetch and provide a list of 5 most recently created pull requests from a GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str) -> list:
        """Fetch and provide a list of 5 most recently created pull requests from a GitHub repository using the MCP server.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
        
        Returns:
            List of pull requests in the repository
        """
        print(f"Pull Requests Lister: Get the pull requests issues for {owner}/{repo}")
        result = mcp_tool_optimized([
            'tools', 'list_pull_requests',
            '--owner', owner,
            '--repo', repo,
            '--sort', "updated",
            '--direction', 'desc',
            '--perPage', '5',
            '--page', '1'
        ])
        if isinstance(result, list):
            return result
        else:
            print(f"Pull Request Lister: Unexpected result: {result}")
            return []


get_pull_requests = GetPullRequestsTool()

