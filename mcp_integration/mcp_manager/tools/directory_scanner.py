from mcp_manager.utils import mcp_tool
from langchain.tools import StructuredTool


def list_repo_files(owner,repo,path=".")->list:
    print(f"Repo structure Lister: Get files at {path} for {owner}/{repo}")
    result = mcp_tool(
        [
            "tools", "get_file_content",
            "--owner",owner,
            "--repo", repo,
            "path", path
        ]
    )
    return result if isinstance(result,list) else []


get_repo_files = StructuredTool.from_function(
    name = "get_repo_files",
    func = list_repo_files,
    description = "list files and folders at a give path in Github repo using MCP server"
)
