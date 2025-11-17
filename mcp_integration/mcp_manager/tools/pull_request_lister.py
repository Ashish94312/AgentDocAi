from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool, mcp_tool_sync


class GetPullRequestsTool(BaseTool):
    name: str = "get_pull_requests"
    description: str = (
        "Fetch and provide a list of 5 most recently created pull requests from a GitHub repository using the MCP server. "
        "Required parameters: owner (string) - the GitHub repository owner, repo (string) - the repository name. "
        "Example: get_pull_requests(owner='vercel', repo='next.js')"
    )
    
    def _run(self, owner: str, repo: str) -> list:
        print(f"Getting pull requests for {owner}/{repo}")
        result = mcp_tool_sync(['tools', 'list_pull_requests', '--owner', owner, '--repo', repo, '--sort', "updated", '--direction', 'desc', '--perPage', '5', '--page', '1'])
        print(f"Got {len(result) if isinstance(result, list) else 0} pull requests")
        if isinstance(result, list):
            return result
        return []
    
    async def _arun(self, owner: str, repo: str) -> list:
        print(f"Getting pull requests for {owner}/{repo}")
        result = await mcp_tool(['tools', 'list_pull_requests', '--owner', owner, '--repo', repo, '--sort', "updated", '--direction', 'desc', '--perPage', '5', '--page', '1'])
        print(f"Got {len(result) if isinstance(result, list) else 0} pull requests")
        if isinstance(result, list):
            return result
        return []


get_pull_requests = GetPullRequestsTool()

