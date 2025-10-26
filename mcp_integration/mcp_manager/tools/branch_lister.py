from crewai.tools import BaseTool
from mcp_manager.utils import mcp_tool, mcp_tool_sync
import asyncio
import json

class GetRepoBranchesTool(BaseTool):
    name: str = "get_repo_branches"
    description: str = "Fetch and provide a list of branches of the GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str, per_page: int = 5, page: int = 1) -> list:
        print(f"Getting branches of {owner}/{repo}")
        result = mcp_tool_sync([
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
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"JSON parse error: {result}")
                return []
        else:
            print(f"Unexpected result type: {type(result)}")
            return []
    
    async def _arun(self, owner: str, repo: str, per_page: int = 5, page: int = 1) -> list:
        print(f"Getting branches of {owner}/{repo}")
        result = await mcp_tool([
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
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"JSON parse error: {result}")
                return []
        else:
            print(f"Unexpected result type: {type(result)}")
            return []


class GetRepoFileStructureTool(BaseTool):
    name: str = "get_repo_file_structure"
    description: str = "Fetch and provide the file structure/directory contents of a GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str, path: str = "/", ref: str = None) -> list:
        print(f"Getting file structure of {owner}/{repo} at {path}")
        
        # make sure path ends with "/" for directories
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
        
        result = mcp_tool_sync(command_args)
        
        if isinstance(result, list):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"JSON parse error: {result}")
                return []
        else:
            print(f"Unexpected result type: {type(result)}")
            return []
    
    async def _arun(self, owner: str, repo: str, path: str = "/", ref: str = None) -> list:
        print(f"Getting file structure of {owner}/{repo} at {path}")
        
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
        
        result = await mcp_tool(command_args)
        
        if isinstance(result, list):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"JSON parse error: {result}")
                return []
        else:
            print(f"Unexpected result type: {type(result)}")
            return []

# tool instances
get_repo_branches = GetRepoBranchesTool()
get_repo_file_structure = GetRepoFileStructureTool()