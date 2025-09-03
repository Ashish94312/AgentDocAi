from crewai import Task
from mcp_manager.agents.agents import repo_structure_auditor
from mcp_manager.tools.directory_scanner import get_repo_files
from ..tools.issue_retriever import get_issue
from ..tools.pull_request_lister import get_pull_requests
from ..agents.agents import  issue_analyst, pull_requests_fetcher_reporter, repo_branch_reporter
from ..tools.branch_lister import get_repo_branches

def analyze_repo_structure_task(owner, repo):
    return [
        Task(
            description=(
                f"Use the 'get_repo_files' tool to explore the directory structure "
                f"of the {owner}/{repo} repository. "
                "Generate a Markdown-formatted file tree that shows the layout of files and folders. "
                "For each file, include a bullet point linking to its GitHub `html_url`. "
                "Do not include files like `.gitignore` unless they are significant. "
                "Provide a readable and navigable tree summary that helps someone quickly understand the repo structure."
            ),
            expected_output=(
                f"A Markdown-formatted file tree with clickable links for each file "
                f"in the {owner}/{repo} repository. "
                "Only list top-level and meaningful subfolders. "
                "Use indentation or bullet points to represent hierarchy."
            ),
            agent=repo_structure_auditor,
            tools=[get_repo_files],  
            output_file="generate_docs/repo_structure.md",  
            create_directory=True,
            verbose=True
        )
    ]


def get_issue_tasks(owner,repo):

    return [
        Task(

            description = (
                f"Use the 'get_issue' tool to fetch a list of all open issues from the {owner}/{repo} repository. "
                "Once you have the data, analyze it to identify key themes, active discussions, and possible blockers. "
                "Summarize the issues in Markdown format. Provide helpful insights, and recommend which issue should be prioritized and why."
            ),

            expected_output = (
                "A Markdown-formatted report containing:\n"
                "- A list of the most relevant open issues (title + URL)\n"
                "- Grouping or categorization of the issues if patterns exist\n"
                "- A short analysis or recommendation on which issue should be tackled first"
            )
            agent = issue_analyst,
            tools = [get_issue],
            output_file = "/generated_docs/report_issues.md.",
            create_directory = True,
            verbose = True

        )
    ]


def list_pull_requests_tasks():

    return [
        Task(
            description =f"Fetch a list of 5 most recently created pull requests for the {owner}/{repo} repository using the 'get_pull_requests' tool. Analyze the provided lists to identify key themes, active discussions, and potential areas of focus.",
            expected_output = f"A Markdown-formatted summary of the repository's pull requests. Provide a concise and categorical summary of the requests and your feedback for it.",
            agent=pull_requests_fetcher_reporter,
            tools=[get_pull_requests],
            output_file="/generated_docs/pull_requests.md",
            create_directory=True,
            verbose=True

        )
    ]


def list_branches_tasks():
    return [
        Task(
            description=f"Fetch a list of 5 branches created from the {owner}/{repo} repository using the 'get_repo_branches' tool. Analyze the provided lists to identify key themes, active discussions, and potential areas of focus.",
            expected_output=f"A Markdown-formatted summary of the repository's branches. Provide a concise and categorical summary of the requests and your feedback for it.",
            agent=repo_branch_reporter,
            tools=[get_repo_branches],
            output_file="/generated_docs/branches.md",
            create_directory=True,
            verbose=True
        )
    ]