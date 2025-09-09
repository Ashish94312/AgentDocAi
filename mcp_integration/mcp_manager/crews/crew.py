from crewai import Crew, Process
from ..agents.agents import repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tasks.tasks import analyze_repo_structure_task, get_issue_tasks, list_pull_requests_tasks, list_branches_tasks


def build_crew(owner, repo):
    tasks = []

    result = analyze_repo_structure_task(owner, repo)
    tasks.extend(result)

    tasks.extend(get_issue_tasks(owner, repo))
    tasks.extend(list_pull_requests_tasks(owner, repo))
    tasks.extend(list_branches_tasks(owner, repo))

    crew = Crew(
        agents=[repo_structure_auditor, issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter],
        tasks=tasks,
        process=Process.hierarchical,  # Changed to hierarchical for better parallelization
        verbose=False,  # Reduced verbosity for better performance
        cache=True,  # Enable caching to avoid repeated API calls
        max_rpm=100,  # Rate limiting to prevent API throttling
        max_execution_time=300  # 5 minute timeout
    )

    return crew
