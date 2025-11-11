import asyncio
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from mcp_manager.tools.directory_scanner import get_repo_files
from mcp_manager.tools.issue_retriever import get_issue
from mcp_manager.tools.pull_request_lister import get_pull_requests
from mcp_manager.tools.branch_lister import get_repo_branches


@dataclass
class TaskResult:
    task_name: str
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0


class ConcurrentGitHubExecutor:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.results: Dict[str, TaskResult] = {}
    
    async def execute_all_tasks(self) -> Dict[str, TaskResult]:
        start_time = time.time()
        
        tasks = {
            'repo_structure': self._get_repo_structure(),
            'issues': self._get_issues(),
            'pull_requests': self._get_pull_requests(),
            'branches': self._get_branches()
        }
        
        # Execute all tasks concurrently
        print(f"Starting concurrent execution of {len(tasks)} tasks for {self.owner}/{self.repo}")
        task_results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        # Process results
        for i, (task_name, task_coro) in enumerate(tasks.items()):
            result = task_results[i]
            if isinstance(result, Exception):
                self.results[task_name] = TaskResult(
                    task_name=task_name,
                    success=False,
                    data=None,
                    error=str(result),
                    execution_time=0.0
                )
            else:
                self.results[task_name] = result
        
        total_time = time.time() - start_time
        print(f"Concurrent execution completed in {total_time:.2f} seconds")
        
        return self.results
    
    async def _get_repo_structure(self) -> TaskResult:
        start_time = time.time()
        try:
            data = await get_repo_files._arun(self.owner, self.repo, "/")
            return TaskResult(
                task_name='repo_structure',
                success=True,
                data=data,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TaskResult(
                task_name='repo_structure',
                success=False,
                data=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _get_issues(self) -> TaskResult:
        start_time = time.time()
        try:
            data = await get_issue._arun(self.owner, self.repo)
            return TaskResult(
                task_name='issues',
                success=True,
                data=data,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TaskResult(
                task_name='issues',
                success=False,
                data=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _get_pull_requests(self) -> TaskResult:
        start_time = time.time()
        try:
            data = await get_pull_requests._arun(self.owner, self.repo)
            return TaskResult(
                task_name='pull_requests',
                success=True,
                data=data,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TaskResult(
                task_name='pull_requests',
                success=False,
                data=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    async def _get_branches(self) -> TaskResult:
        start_time = time.time()
        try:
            data = await get_repo_branches._arun(self.owner, self.repo)
            return TaskResult(
                task_name='branches',
                success=True,
                data=data,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TaskResult(
                task_name='branches',
                success=False,
                data=None,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def get_successful_results(self) -> Dict[str, Any]:
        return {
            name: result.data 
            for name, result in self.results.items() 
            if result.success
        }
    
    def get_failed_tasks(self) -> List[str]:
        return [
            name 
            for name, result in self.results.items() 
            if not result.success
        ]
    
    def get_execution_summary(self) -> Dict[str, Any]:
        total_time = sum(result.execution_time for result in self.results.values())
        successful_count = sum(1 for result in self.results.values() if result.success)
        failed_count = len(self.results) - successful_count
        
        return {
            'total_tasks': len(self.results),
            'successful_tasks': successful_count,
            'failed_tasks': failed_count,
            'total_execution_time': total_time,
            'average_task_time': total_time / len(self.results) if self.results else 0,
            'failed_task_names': self.get_failed_tasks()
        }


async def execute_concurrent_github_analysis(owner: str, repo: str) -> Dict[str, Any]:
    executor = ConcurrentGitHubExecutor(owner, repo)
    results = await executor.execute_all_tasks()
    
    return {
        'results': results,
        'successful_data': executor.get_successful_results(),
        'summary': executor.get_execution_summary()
    }


class PerformanceComparator:
    @staticmethod
    async def compare_execution_methods(owner: str, repo: str) -> Dict[str, Any]:
        print(f"Comparing execution methods for {owner}/{repo}")
        
        start_time = time.time()
        async_results = await execute_concurrent_github_analysis(owner, repo)
        async_time = time.time() - start_time
        
        start_time = time.time()
        sync_results = await _simulate_sync_execution(owner, repo)
        sync_time = time.time() - start_time
        
        improvement = ((sync_time - async_time) / sync_time) * 100 if sync_time > 0 else 0
        
        return {
            'async_execution': {
                'time': async_time,
                'results': async_results
            },
            'sync_execution': {
                'time': sync_time,
                'results': sync_results
            },
            'performance_improvement': {
                'time_saved': sync_time - async_time,
                'percentage_improvement': improvement
            }
        }


async def _simulate_sync_execution(owner: str, repo: str) -> Dict[str, Any]:
    results = {}
    
    start_time = time.time()
    try:
        results['repo_structure'] = await get_repo_files._arun(owner, repo, "/")
    except Exception as e:
        results['repo_structure'] = {'error': str(e)}
    
    try:
        results['issues'] = await get_issue._arun(owner, repo)
    except Exception as e:
        results['issues'] = {'error': str(e)}
    
    try:
        results['pull_requests'] = await get_pull_requests._arun(owner, repo)
    except Exception as e:
        results['pull_requests'] = {'error': str(e)}
    
    try:
        results['branches'] = await get_repo_branches._arun(owner, repo)
    except Exception as e:
        results['branches'] = {'error': str(e)}
    
    return {
        'results': results,
        'execution_time': time.time() - start_time
    }
