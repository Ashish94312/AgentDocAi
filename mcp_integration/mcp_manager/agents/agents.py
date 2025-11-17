from crewai import Agent
from langchain_openai import ChatOpenAI
from ..tools.directory_scanner import get_repo_files
from ..tools.issue_retriever import get_issue
from ..tools.pull_request_lister import get_pull_requests
from ..tools.branch_lister import get_repo_branches

agent_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)

repo_structure_auditor = Agent(
    role="Repository Structure Auditor",
    goal="Analyze repo structure and create a markdown file tree with GitHub links",
    backstory="You're good at visualizing repo structures and creating clean markdown docs",
    tools=[get_repo_files],
    llm=agent_llm,
    verbose=False
)

issue_analyst = Agent(
    role="Github Issue Analyst", 
    goal="Get open issues and suggest which ones to prioritize",
    backstory="You know how to analyze GitHub issues and spot the important ones",
    tools=[get_issue],
    llm=agent_llm,
    verbose=False
)

pull_requests_fetcher_reporter = Agent(
    role="Pull Request Lister",
    goal="Get the 5 most recent pull requests from a repo",
    backstory="You can fetch and summarize PRs effectively",
    tools=[get_pull_requests],
    llm=agent_llm,
    verbose=False
)

repo_branch_reporter = Agent(
    role="Repository Branch Reporter",
    goal="Get a list of 5 branches in a GitHub repository",
    backstory="You can analyze repo branches and explain their purpose",
    tools=[get_repo_branches],
    llm=agent_llm,
    verbose=False
)
