import asyncio
import time
from mcp_manager.tools.directory_scanner import get_repo_files
from mcp_manager.tools.issue_retriever import get_issue
from mcp_manager.tools.pull_request_lister import get_pull_requests
from mcp_manager.tools.branch_lister import get_repo_branches


class GitHubDataFetcher:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.results = {}
    
    async def fetch_all(self):
        print(f"Fetching data for {self.owner}/{self.repo}")
        self.results['repo_structure'] = await self.get_repo_structure()
        print("Repo structure done")
        self.results['issues'] = await self.get_issues()
        print("Issues done")
        self.results['pull_requests'] = await self.get_pull_requests()
        print("Pull requests done")
        self.results['branches'] = await self.get_branches()
        print("Branches done")
        return self.results
    
    async def get_repo_structure(self):
        data = await get_repo_files._arun(self.owner, self.repo, "/")
        return {
            'task_name': 'repo_structure',
            'success': True,
            'data': data
        }
    
    async def get_issues(self):
        data = await get_issue._arun(self.owner, self.repo)
        return {
            'task_name': 'issues',
            'success': True,
            'data': data
        }
    
    async def get_pull_requests(self):
        data = await get_pull_requests._arun(self.owner, self.repo)
        return {
            'task_name': 'pull_requests',
            'success': True,
            'data': data
        }
    
    async def get_branches(self):
        data = await get_repo_branches._arun(self.owner, self.repo)
        return {
            'task_name': 'branches',
            'success': True,
            'data': data
        }
    
    def get_data(self):
        data = {}
        for name, result in self.results.items():
            if result.get('success'):
                data[name] = result.get('data')
        return data


async def fetch_github_data(owner, repo):
    fetcher = GitHubDataFetcher(owner, repo)
    results = await fetcher.fetch_all()
    return {
        'results': results,
        'data': fetcher.get_data()
    }

