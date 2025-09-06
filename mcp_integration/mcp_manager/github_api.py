"""
GitHub API utility functions to replace MCP server calls.
This module provides direct GitHub API integration for deployment environments
where the MCP server binary is not available.
"""

import requests
import json
from django.conf import settings
from typing import List, Dict, Any, Optional


class GitHubAPI:
    """GitHub API client for direct API calls."""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RepoDoc-AI/1.0"
        }
    
    def get_repo_contents(self, owner: str, repo: str, path: str = "/") -> List[Dict[str, Any]]:
        """
        Get repository contents (files and directories) at a given path.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            path: Path to file/directory (default: "/")
        
        Returns:
            List of files and directories
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path.lstrip('/')}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            contents = response.json()
            if not isinstance(contents, list):
                # Single file
                return [contents]
            
            return contents
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repo contents: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in get_repo_contents: {e}")
            return []
    
    def list_issues(self, owner: str, repo: str, state: str = "open", per_page: int = 5, page: int = 1) -> List[Dict[str, Any]]:
        """
        List issues from a GitHub repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            per_page: Number of issues per page
            page: Page number
        
        Returns:
            List of issues
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            params = {
                "state": state,
                "per_page": per_page,
                "page": page
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in list_issues: {e}")
            return []
    
    def list_pull_requests(self, owner: str, repo: str, state: str = "open", per_page: int = 5, page: int = 1) -> List[Dict[str, Any]]:
        """
        List pull requests from a GitHub repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state (open, closed, all)
            per_page: Number of PRs per page
            page: Page number
        
        Returns:
            List of pull requests
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
            params = {
                "state": state,
                "per_page": per_page,
                "page": page
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pull requests: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in list_pull_requests: {e}")
            return []
    
    def list_branches(self, owner: str, repo: str, per_page: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        List branches from a GitHub repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of branches per page
            page: Page number
        
        Returns:
            List of branches
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/branches"
            params = {
                "per_page": per_page,
                "page": page
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching branches: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in list_branches: {e}")
            return []
    
    def get_repository_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """
        Get basic repository information.
        
        Args:
            owner: Repository owner
            repo: Repository name
        
        Returns:
            Repository information or None
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository info: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_repository_info: {e}")
            return None


# Global instance
github_api = GitHubAPI()


def github_tool(tool_name: str, **kwargs) -> Any:
    """
    Unified function to call GitHub API tools.
    This replaces the mcp_tool function for GitHub API calls.
    
    Args:
        tool_name: Name of the tool to call
        **kwargs: Tool-specific arguments
    
    Returns:
        Tool result
    """
    if tool_name == "get_file_contents":
        return github_api.get_repo_contents(
            owner=kwargs.get("owner"),
            repo=kwargs.get("repo"),
            path=kwargs.get("path", "/")
        )
    elif tool_name == "list_issues":
        return github_api.list_issues(
            owner=kwargs.get("owner"),
            repo=kwargs.get("repo"),
            state=kwargs.get("state", "open"),
            per_page=kwargs.get("perPage", 5),
            page=kwargs.get("page", 1)
        )
    elif tool_name == "list_pull_requests":
        return github_api.list_pull_requests(
            owner=kwargs.get("owner"),
            repo=kwargs.get("repo"),
            state=kwargs.get("state", "open"),
            per_page=kwargs.get("perPage", 5),
            page=kwargs.get("page", 1)
        )
    elif tool_name == "list_branches":
        return github_api.list_branches(
            owner=kwargs.get("owner"),
            repo=kwargs.get("repo"),
            per_page=kwargs.get("perPage", 10),
            page=kwargs.get("page", 1)
        )
    else:
        print(f"Unknown tool: {tool_name}")
        return None
