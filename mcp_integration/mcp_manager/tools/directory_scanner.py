from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool, mcp_tool_sync
import asyncio

class GetRepoFilesTool(BaseTool):
    name: str = "get_repo_files"
    description: str = "List files and folders at a given path in a GitHub repository using MCP server"
    
    def _run(self, owner: str, repo: str, path: str = "/") -> list:
        print(f"Getting files at {path} for {owner}/{repo}")
        result = mcp_tool_sync([
            "tools", "get_file_contents",
            "--owner", owner,
            "--repo", repo,
            "--path", path
        ])
        return result if isinstance(result, list) else []
    
    async def _arun(self, owner: str, repo: str, path: str = "/") -> list:
        print(f"Getting files at {path} for {owner}/{repo}")
        result = await mcp_tool([
            "tools", "get_file_contents",
            "--owner", owner,
            "--repo", repo,
            "--path", path
        ])
        return result if isinstance(result, list) else []

get_repo_files = GetRepoFilesTool()
