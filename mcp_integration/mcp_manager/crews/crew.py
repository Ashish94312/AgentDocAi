from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from ..agents.agents import repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tasks.tasks import analyze_repo_structure_task, get_issue_tasks, list_pull_requests_tasks, list_branches_tasks
from ..concurrent_executor import execute_concurrent_github_analysis
import asyncio


def build_crew(owner, repo):
    tasks = []

    result = analyze_repo_structure_task(owner, repo)
    tasks.extend(result)

    tasks.extend(get_issue_tasks(owner, repo))
    tasks.extend(list_pull_requests_tasks(owner, repo))
    tasks.extend(list_branches_tasks(owner, repo))


    manager_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )
    
    crew = Crew(
        agents=[repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter],
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
        cache=False
    )

    return crew


async def build_crew_async(owner, repo):
  
    print(f"Starting concurrent data fetching for {owner}/{repo}")
    concurrent_results = await execute_concurrent_github_analysis(owner, repo)
    
 
    summary = concurrent_results['summary']
    print(f"Concurrent execution completed:")
    print(f"  - Total tasks: {summary['total_tasks']}")
    print(f"  - Successful: {summary['successful_tasks']}")
    print(f"  - Failed: {summary['failed_tasks']}")
    print(f"  - Total time: {summary['total_execution_time']:.2f}s")
    print(f"  - Average task time: {summary['average_task_time']:.2f}s")
    
    if summary['failed_tasks']:
        print(f"  - Failed tasks: {', '.join(summary['failed_tasks'])}")
    
    crew_tasks = []
    crew_tasks.extend(analyze_repo_structure_task(owner, repo))
    crew_tasks.extend(get_issue_tasks(owner, repo))
    crew_tasks.extend(list_pull_requests_tasks(owner, repo))
    crew_tasks.extend(list_branches_tasks(owner, repo))

  
    manager_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )
    
    crew = Crew(
        agents=[repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter],
        tasks=crew_tasks,
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
        cache=False
    )

    return crew


async def execute_crew_async(owner, repo):
    crew = await build_crew_async(owner, repo)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, crew.kickoff)
    return result
