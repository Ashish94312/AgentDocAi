from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from ..agents.agents import repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tasks.tasks import analyze_repo_structure_task, get_issue_tasks, list_pull_requests_tasks, list_branches_tasks
from ..github_data import fetch_github_data
import asyncio


async def build_crew_async(owner, repo):
    await fetch_github_data(owner, repo)
    
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
        verbose=False,
        cache=False
    )

    return crew


async def execute_crew_async(owner, repo):
    crew = await build_crew_async(owner, repo)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, crew.kickoff)
    return result
