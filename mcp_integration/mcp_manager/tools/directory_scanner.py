from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool


class GetRepoFilesTool(BaseTool):
    name: str = "get_repo_files"
    description: str = "List files and folders at a given path in a GitHub repository using MCP server"
    
    def _run(self, owner: str, repo: str, path: str = "/") -> list:
        """List files and folders at a given path in a GitHub repository using MCP server.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            path: Path to file/directory (default: "/")
        
        Returns:
            List of files and folders in the repository
        """
        print(f"Repo structure Lister: Get files at {path} for {owner}/{repo}")
        result = mcp_tool([
            "tools", "get_file_contents",
            "--owner", owner,
            "--repo", repo,
            "--path", path
        ])
        return result if isinstance(result, list) else []


get_repo_files = GetRepoFilesTool()
