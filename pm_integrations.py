"""Integrations with Jira, Asana, and Notion for project data."""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any


class JiraIntegration:
    """Fetch sprint data from Jira."""

    def __init__(self):
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.base_url = os.getenv("JIRA_BASE_URL", "https://your-company.atlassian.net")

    def get_sprint(self, project_key: str = "PROJ") -> Dict[str, Any]:
        """Fetch active sprint with issues."""
        # In production, use Jira API with: requests.get(f"{self.base_url}/rest/api/3/...")
        # For now, return mock data
        return {
            "platform": "Jira",
            "sprint_id": "SPRINT-42",
            "sprint_name": f"{project_key} Sprint 42",
            "start_date": (datetime.now() - timedelta(days=7)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "active",
            "velocity": 34,
            "stats": {
                "total": 24,
                "done": 16,
                "in_progress": 5,
                "todo": 3,
            },
            "issues": [
                {
                    "key": f"{project_key}-101",
                    "title": "Fix authentication race condition",
                    "status": "In Progress",
                    "assignee": "alice@company.com",
                    "priority": "High",
                    "days_in_status": 3,
                    "blocked_by": [],
                },
                {
                    "key": f"{project_key}-102",
                    "title": "Implement Stripe payment integration",
                    "status": "In Progress",
                    "assignee": "bob@company.com",
                    "priority": "Critical",
                    "days_in_status": 5,
                    "blocked_by": [f"{project_key}-105"],
                },
                {
                    "key": f"{project_key}-103",
                    "title": "Update API documentation",
                    "status": "Done",
                    "assignee": "charlie@company.com",
                    "priority": "Low",
                    "days_in_status": 2,
                    "blocked_by": [],
                },
                {
                    "key": f"{project_key}-104",
                    "title": "PostgreSQL version migration",
                    "status": "To Do",
                    "assignee": "dave@company.com",
                    "priority": "Critical",
                    "days_in_status": 0,
                    "blocked_by": [],
                },
                {
                    "key": f"{project_key}-105",
                    "title": "Set up payment webhooks",
                    "status": "In Progress",
                    "assignee": "eve@company.com",
                    "priority": "High",
                    "days_in_status": 7,
                    "blocked_by": [],
                },
            ]
        }


class AsanaIntegration:
    """Fetch project data from Asana."""

    def __init__(self):
        self.api_token = os.getenv("ASANA_API_TOKEN")
        self.api_url = "https://app.asana.com/api/1.0"

    def get_project(self, project_name: str = "Marketing Campaign") -> Dict[str, Any]:
        """Fetch project with tasks and status."""
        # In production: requests.get(f"{self.api_url}/projects/{project_id}", headers=...)
        return {
            "platform": "Asana",
            "project_name": project_name,
            "status": "On Track",
            "completion": 65,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "stats": {
                "total": 32,
                "completed": 21,
                "at_risk": 4,
                "off_track": 1,
            },
            "tasks": [
                {
                    "id": "1234567890123",
                    "name": "Homepage redesign",
                    "status": "In Progress",
                    "assignee": "frank@company.com",
                    "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
                    "days_overdue": 0,
                    "custom_field": "On Track"
                },
                {
                    "id": "1234567890124",
                    "name": "Database optimization",
                    "status": "At Risk",
                    "assignee": "grace@company.com",
                    "due_date": (datetime.now() - timedelta(days=2)).isoformat(),
                    "days_overdue": 2,
                    "custom_field": "At Risk"
                },
                {
                    "id": "1234567890125",
                    "name": "Security audit compliance",
                    "status": "On Hold",
                    "assignee": "henry@company.com",
                    "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                    "days_overdue": 0,
                    "custom_field": "Blocked"
                },
                {
                    "id": "1234567890126",
                    "name": "Mobile app QA",
                    "status": "In Progress",
                    "assignee": "iris@company.com",
                    "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                    "days_overdue": 0,
                    "custom_field": "On Track"
                },
            ]
        }


class NotionIntegration:
    """Fetch status updates from Notion."""

    def __init__(self):
        self.api_token = os.getenv("NOTION_API_TOKEN")
        self.api_url = "https://api.notion.com/v1"

    def get_status_page(self, page_name: str = "Weekly Status") -> Dict[str, Any]:
        """Fetch Notion status database."""
        # In production: requests.post(f"{self.api_url}/databases/{db_id}/query", ...)
        return {
            "platform": "Notion",
            "page_name": page_name,
            "last_updated": datetime.now().isoformat(),
            "initiatives": [
                {
                    "id": "n1",
                    "title": "Q4 Product Launch",
                    "status": "In Progress",
                    "priority": "P0",
                    "owner": "jack@company.com",
                    "progress": 60,
                    "updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "description": "Core feature implementation ongoing"
                },
                {
                    "id": "n2",
                    "title": "Customer feedback loop",
                    "status": "Blocked",
                    "priority": "P1",
                    "owner": "kate@company.com",
                    "progress": 30,
                    "updated": (datetime.now() - timedelta(days=5)).isoformat(),
                    "description": "Waiting on external API documentation from vendor"
                },
                {
                    "id": "n3",
                    "title": "Analytics dashboard v2",
                    "status": "Completed",
                    "priority": "P2",
                    "owner": "liam@company.com",
                    "progress": 100,
                    "updated": (datetime.now() - timedelta(days=2)).isoformat(),
                    "description": "Released to beta users"
                },
                {
                    "id": "n4",
                    "title": "Team hiring plan",
                    "status": "In Progress",
                    "priority": "P1",
                    "owner": "megan@company.com",
                    "progress": 40,
                    "updated": (datetime.now() - timedelta(days=3)).isoformat(),
                    "description": "5 positions to fill, 2 candidates in final round"
                },
            ]
        }


def fetch_all_statuses(
    jira_project: str = "PROJ",
    asana_project: str = "Marketing Campaign",
    notion_page: str = "Weekly Status"
) -> Dict[str, Any]:
    """Aggregate status from all platforms."""
    jira = JiraIntegration()
    asana = AsanaIntegration()
    notion = NotionIntegration()

    return {
        "timestamp": datetime.now().isoformat(),
        "sources": {
            "jira": jira.get_sprint(jira_project),
            "asana": asana.get_project(asana_project),
            "notion": notion.get_status_page(notion_page)
        }
    }


def extract_blockers(all_statuses: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify blockers from all data sources."""
    blockers = []
    sources = all_statuses.get("sources", {})

    # From Jira
    if "jira" in sources:
        for issue in sources["jira"].get("issues", []):
            if issue.get("blocked_by"):
                blockers.append({
                    "source": "Jira",
                    "id": issue["key"],
                    "title": issue["title"],
                    "type": "dependency_blocked",
                    "priority": issue["priority"],
                    "blocked_by": issue["blocked_by"][0] if issue["blocked_by"] else None,
                    "days_blocked": issue.get("days_in_status", 0),
                    "assignee": issue.get("assignee")
                })
            elif issue["status"] == "In Progress" and issue["days_in_status"] > 5:
                blockers.append({
                    "source": "Jira",
                    "id": issue["key"],
                    "title": issue["title"],
                    "type": "stuck_in_progress",
                    "priority": issue["priority"],
                    "days_blocked": issue["days_in_status"],
                    "assignee": issue.get("assignee")
                })

    # From Asana
    if "asana" in sources:
        for task in sources["asana"].get("tasks", []):
            if task.get("days_overdue", 0) > 0:
                blockers.append({
                    "source": "Asana",
                    "id": task["id"],
                    "title": task["name"],
                    "type": "overdue",
                    "priority": "High",
                    "days_blocked": task["days_overdue"],
                    "assignee": task.get("assignee")
                })
            elif task["custom_field"] == "At Risk":
                blockers.append({
                    "source": "Asana",
                    "id": task["id"],
                    "title": task["name"],
                    "type": "at_risk",
                    "priority": "High",
                    "days_blocked": 0,
                    "assignee": task.get("assignee")
                })

    # From Notion
    if "notion" in sources:
        for item in sources["notion"].get("initiatives", []):
            if item["status"] == "Blocked":
                blockers.append({
                    "source": "Notion",
                    "id": item["id"],
                    "title": item["title"],
                    "type": "external_blocker",
                    "priority": item["priority"],
                    "days_blocked": 0,
                    "assignee": item.get("owner"),
                    "description": item.get("description")
                })

    return sorted(blockers, key=lambda x: x.get("days_blocked", 0), reverse=True)
