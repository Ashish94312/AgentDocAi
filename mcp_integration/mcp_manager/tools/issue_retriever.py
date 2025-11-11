from crewai.tools import BaseTool
from ..utils import mcp_tool, mcp_tool_sync
import asyncio


class GetIssueTool(BaseTool):
    name: str = "get_issue"
    description: str = "Fetch and provide a list of open issues from a GitHub repository using the MCP server"
    
    def _run(self, owner: str, repo: str) -> list:
        print(f"Issue Retriever: getting open issues for {owner}/{repo}")
        result = mcp_tool_sync([
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
    
    async def _arun(self, owner: str, repo: str) -> list:
        print(f"Issue Retriever: getting open issues for {owner}/{repo}")
        result = await mcp_tool([
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

