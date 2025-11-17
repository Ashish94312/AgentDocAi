from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool, mcp_tool_sync

class GetRepoFilesTool(BaseTool):
    name: str = "get_repo_files"
    description: str = (
        "List files and folders at a given path in a GitHub repository using MCP server. "
        "Required parameters: owner (string) - the GitHub repository owner, repo (string) - the repository name, "
        "path (string, optional) - the path to list (default: '/'). "
        "Example: get_repo_files(owner='vercel', repo='next.js', path='/')"
    )
    
    def _run(self, owner: str, repo: str, path: str = "/") -> list:
        print(f"Getting files for {owner}/{repo} at {path}")
        result = mcp_tool_sync(["tools", "get_file_contents", "--owner", owner, "--repo", repo, "--path", path])
        print(f"Got {len(result) if isinstance(result, list) else 0} files")
        return result if isinstance(result, list) else []
    
    async def _arun(self, owner: str, repo: str, path: str = "/") -> list:
        print(f"Getting files for {owner}/{repo} at {path}")
        result = await mcp_tool(["tools", "get_file_contents", "--owner", owner, "--repo", repo, "--path", path])
        print(f"Got {len(result) if isinstance(result, list) else 0} files")
        return result if isinstance(result, list) else []

get_repo_files = GetRepoFilesTool()
