from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from ..agents.agents import repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tasks.tasks import analyze_repo_structure_task, get_issue_tasks, list_pull_requests_tasks, list_branches_tasks


def build_crew(owner, repo):
    tasks = []

    result = analyze_repo_structure_task(owner, repo)
    tasks.extend(result)

    tasks.extend(get_issue_tasks(owner, repo))
    tasks.extend(list_pull_requests_tasks(owner, repo))
    tasks.extend(list_branches_tasks(owner, repo))

    # Create a manager LLM for hierarchical process
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
