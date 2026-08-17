"""
GitHub integration for MoneyPrintTurbo.

This service integrates with GitHub to enable:
- Repository management and insights
- Pull request workflows
- Issue tracking
- Commit and workflow automation

Configured to work with Claude's GitHub integration.
"""

import os
from typing import Any, Dict, List, Optional

from loguru import logger
from app.config import config


class GitHubIntegrationService:
    """Service for GitHub repository operations and collaboration."""

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.github_repo = config.app.get("github_repository", "BrunoLuke-creator/MoneyPrintTurbo")
        self.enabled = bool(self.github_token)

    def is_configured(self) -> bool:
        """Check if GitHub integration is properly configured."""
        return self.enabled and bool(self.github_repo)

    def get_repo_info(self) -> Dict[str, Any]:
        """
        Get information about the current repository.

        Returns:
            Repository information dict
        """
        if not self.is_configured():
            logger.warning("GitHub integration not configured.")
            return {"success": False, "error": "GitHub token not set"}

        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            response = requests.get(
                f"https://api.github.com/repos/{self.github_repo}",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            
            repo_data = response.json()
            logger.info(f"Retrieved GitHub repo info: {self.github_repo}")
            
            return {
                "success": True,
                "name": repo_data.get("name"),
                "description": repo_data.get("description"),
                "url": repo_data.get("html_url"),
                "stars": repo_data.get("stargazers_count"),
                "language": repo_data.get("language"),
                "topics": repo_data.get("topics", []),
            }
            
        except Exception as e:
            logger.error(f"Error retrieving GitHub repo info: {str(e)}")
            return {"success": False, "error": str(e)}

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue.

        Args:
            title: Issue title
            body: Issue description
            labels: Optional list of labels

        Returns:
            Created issue information
        """
        if not self.is_configured():
            logger.warning("GitHub integration not configured.")
            return {"success": False, "error": "GitHub token not set"}

        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            payload = {
                "title": title,
                "body": body,
            }
            if labels:
                payload["labels"] = labels
            
            response = requests.post(
                f"https://api.github.com/repos/{self.github_repo}/issues",
                json=payload,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            
            issue_data = response.json()
            logger.info(f"Created GitHub issue: #{issue_data.get('number')}")
            
            return {
                "success": True,
                "issue_number": issue_data.get("number"),
                "issue_url": issue_data.get("html_url"),
                "title": issue_data.get("title"),
            }
            
        except Exception as e:
            logger.error(f"Error creating GitHub issue: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_recent_commits(self, count: int = 10) -> Dict[str, Any]:
        """
        Get recent commits from the repository.

        Args:
            count: Number of commits to retrieve

        Returns:
            Recent commits list
        """
        if not self.is_configured():
            logger.warning("GitHub integration not configured.")
            return {"success": False, "error": "GitHub token not set", "commits": []}

        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            response = requests.get(
                f"https://api.github.com/repos/{self.github_repo}/commits",
                headers=headers,
                params={"per_page": count},
                timeout=10,
            )
            response.raise_for_status()
            
            commits_data = response.json()
            commits = [
                {
                    "sha": c.get("sha", "")[:7],
                    "message": c.get("commit", {}).get("message", ""),
                    "author": c.get("commit", {}).get("author", {}).get("name", ""),
                    "date": c.get("commit", {}).get("author", {}).get("date", ""),
                }
                for c in commits_data
            ]
            
            logger.info(f"Retrieved {len(commits)} recent commits")
            return {"success": True, "commits": commits}
            
        except Exception as e:
            logger.error(f"Error retrieving commits: {str(e)}")
            return {"success": False, "error": str(e), "commits": []}

    def get_workflows_status(self) -> Dict[str, Any]:
        """
        Get the status of GitHub Actions workflows.

        Returns:
            Workflows status information
        """
        if not self.is_configured():
            logger.warning("GitHub integration not configured.")
            return {"success": False, "error": "GitHub token not set", "workflows": []}

        try:
            import requests
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            response = requests.get(
                f"https://api.github.com/repos/{self.github_repo}/actions/runs",
                headers=headers,
                params={"per_page": 10},
                timeout=10,
            )
            response.raise_for_status()
            
            runs_data = response.json()
            workflows = [
                {
                    "name": r.get("name", ""),
                    "status": r.get("status", ""),
                    "conclusion": r.get("conclusion", ""),
                    "created_at": r.get("created_at", ""),
                }
                for r in runs_data.get("workflow_runs", [])
            ]
            
            logger.info(f"Retrieved {len(workflows)} workflow runs")
            return {"success": True, "workflows": workflows}
            
        except Exception as e:
            logger.error(f"Error retrieving workflows: {str(e)}")
            return {"success": False, "error": str(e), "workflows": []}


# Singleton instance
github_service = GitHubIntegrationService()


def get_repo_summary() -> Dict[str, Any]:
    """Get a summary of the current repository."""
    return github_service.get_repo_info()
