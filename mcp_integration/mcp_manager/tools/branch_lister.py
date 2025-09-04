from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool


class GetRepoBranchesTool(BaseTool):
    name: str = "get_repo_branches"
    description: str = "Fetch and provide a list of branches of the GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str, per_page: int = 5, page: int = 1) -> list:
        """Fetch and provide a list of branches of the GitHub repository using the MCP server.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            per_page: Number of results per page (default: 5, max: 100)
            page: Page number (default: 1)
        
        Returns:
            List of branches in the repository
        """
        print(f"Branch Lister: Getting branches of {owner}/{repo}")
        result = mcp_tool([
            'tools', 'list_branches',
            '--owner', owner,
            '--repo', repo,
            '--perPage', str(per_page),
            '--page', str(page)
        ])
        
        if isinstance(result, list):
            return result
        elif isinstance(result, str):
            try:
                import json
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"Branch Lister: Failed to parse JSON result: {result}")
                return []
        else:
            print(f"Branch Lister: Unexpected result type: {type(result)}, value: {result}")
            return []


class GetRepoFileStructureTool(BaseTool):
    name: str = "get_repo_file_structure"
    description: str = "Fetch and provide the file structure/directory contents of a GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str, path: str = "/", ref: str = None) -> list:
        """Fetch and provide the file structure/directory contents of a GitHub repository using the MCP server.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            path: Path to directory (default: "/" for root, must end with "/" for directories)
            ref: Git reference (branch, tag, or commit SHA) (optional)
        
        Returns:
            List of files and directories in the specified path
        """
        print(f"File Structure Tool: Getting file structure of {owner}/{repo} at path: {path}")
        
        # Ensure path ends with "/" for directories
        if not path.endswith("/"):
            path += "/"
        
        command_args = [
            'tools', 'get_file_contents',
            '--owner', owner,
            '--repo', repo,
            '--path', path
        ]
        
        if ref:
            command_args.extend(['--ref', ref])
        
        result = mcp_tool(command_args)
        
        if isinstance(result, list):
            return result
        elif isinstance(result, str):
            try:
                import json
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"File Structure Tool: Failed to parse JSON result: {result}")
                return []
        else:
            print(f"File Structure Tool: Unexpected result type: {type(result)}, value: {result}")
            return []


# Create instances of the tools
get_repo_branches = GetRepoBranchesTool()
get_repo_file_structure = GetRepoFileStructureTool()