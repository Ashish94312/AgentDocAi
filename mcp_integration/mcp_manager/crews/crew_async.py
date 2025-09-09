import asyncio
import concurrent.futures
from crewai import Crew, Process
from ..agents.agents import repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tasks.tasks import analyze_repo_structure_task, get_issue_tasks, list_pull_requests_tasks, list_branches_tasks


async def build_crew_async(owner, repo):
    """
    Build and execute crew with async processing for independent tasks
    """
    # Create separate crews for independent tasks
    repo_structure_crew = Crew(
        agents=[repo_structure_auditor],
        tasks=analyze_repo_structure_task(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    issues_crew = Crew(
        agents=[issue_analyst],
        tasks=get_issue_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    pr_crew = Crew(
        agents=[pull_requests_fetcher_reporter],
        tasks=list_pull_requests_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    branches_crew = Crew(
        agents=[repo_branch_reporter],
        tasks=list_branches_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    # Execute all crews concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all crew executions to the thread pool
        future_repo = executor.submit(repo_structure_crew.kickoff)
        future_issues = executor.submit(issues_crew.kickoff)
        future_pr = executor.submit(pr_crew.kickoff)
        future_branches = executor.submit(branches_crew.kickoff)
        
        # Wait for all to complete
        results = await asyncio.gather(
            asyncio.wrap_future(future_repo),
            asyncio.wrap_future(future_issues),
            asyncio.wrap_future(future_pr),
            asyncio.wrap_future(future_branches),
            return_exceptions=True
        )
    
    return results


def build_crew_parallel(owner, repo):
    """
    Synchronous version that runs independent tasks in parallel
    """
    import threading
    import time
    
    results = {}
    threads = []
    
    def run_crew(crew, result_key):
        try:
            result = crew.kickoff()
            results[result_key] = result
        except Exception as e:
            results[result_key] = f"Error: {str(e)}"
    
    # Create separate crews for independent tasks
    repo_structure_crew = Crew(
        agents=[repo_structure_auditor],
        tasks=analyze_repo_structure_task(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    issues_crew = Crew(
        agents=[issue_analyst],
        tasks=get_issue_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    pr_crew = Crew(
        agents=[pull_requests_fetcher_reporter],
        tasks=list_pull_requests_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    branches_crew = Crew(
        agents=[repo_branch_reporter],
        tasks=list_branches_tasks(owner, repo),
        process=Process.sequential,
        verbose=False,
        cache=True,
        max_rpm=100,
        max_execution_time=120
    )
    
    # Start all crews in separate threads
    threads.append(threading.Thread(target=run_crew, args=(repo_structure_crew, 'repo_structure')))
    threads.append(threading.Thread(target=run_crew, args=(issues_crew, 'issues')))
    threads.append(threading.Thread(target=run_crew, args=(pr_crew, 'pull_requests')))
    threads.append(threading.Thread(target=run_crew, args=(branches_crew, 'branches')))
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results
