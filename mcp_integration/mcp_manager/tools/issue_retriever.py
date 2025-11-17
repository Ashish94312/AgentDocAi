from crewai.tools import BaseTool
from ..utils import mcp_tool, mcp_tool_sync


class GetIssueTool(BaseTool):
    name: str = "get_issue"
    description: str = (
        "Fetch and provide a list of open issues from a GitHub repository using the MCP server. "
        "Required parameters: owner (string) - the GitHub repository owner, repo (string) - the repository name. "
        "Example: get_issue(owner='vercel', repo='next.js')"
    )
    
    def _run(self, owner: str, repo: str) -> list:
        print(f"Getting issues for {owner}/{repo}")
        result = mcp_tool_sync(['tools', 'list_issues', '--owner', owner, '--repo', repo, '--state', 'OPEN', '--perPage', '5'])
        
        if isinstance(result, dict) and 'issues' in result:
            issues = result['issues']
            if isinstance(issues, list):
                print(f"Got {len(issues)} issues")
                return issues
        elif isinstance(result, list):
            print(f"Got {len(result)} issues")
            return result
        print("Got 0 issues")
        return []
    
    async def _arun(self, owner: str, repo: str) -> list:
        print(f"Getting issues for {owner}/{repo}")
        result = await mcp_tool(['tools', 'list_issues', '--owner', owner, '--repo', repo, '--state', 'OPEN', '--perPage', '5'])
        
        if isinstance(result, dict) and 'issues' in result:
            issues = result['issues']
            if isinstance(issues, list):
                print(f"Got {len(issues)} issues")
                return issues
        elif isinstance(result, list):
            print(f"Got {len(result)} issues")
            return result
        print("Got 0 issues")
        return []


get_issue = GetIssueTool()

