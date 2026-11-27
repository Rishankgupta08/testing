import os
import re
import sys
import argparse
import logging
from typing import List

import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"
GITHUB_REPO_OWNER = "rishankgupta08"
GITHUB_REPO_NAME = "testing"

JIRA_API_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/") + "/rest/api/3/issue"
JIRA_PROJECT_KEY = "KAN"


def get_github_issue_body(issue_number: int) -> str:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.error("GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error("Failed to fetch GitHub issue %s: %s", issue_number, response.text)
        sys.exit(1)

    data = response.json()
    return data.get("body", "")


def parse_checklist_items(body: str) -> List[str]:
    pattern = re.compile(r"^\s*-\s*\[[ xX]\]\s+(.*)$", re.MULTILINE)
    items = [match.group(1).strip() for match in pattern.finditer(body) if match.group(1).strip()]
    return items


def create_jira_subtask(parent_key: str, summary: str) -> dict:
    username = os.getenv("JIRA_USERNAME")
    api_token = os.getenv("JIRA_API_TOKEN")
    if not username or not api_token:
        logger.error("JIRA_USERNAME and JIRA_API_TOKEN environment variables must be set")
        sys.exit(1)

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "parent": {"key": parent_key},
            "summary": summary,
            "issuetype": {"name": "Sub-task"},
        }
    }

    response = requests.post(
        JIRA_API_URL,
        json=payload,
        auth=HTTPBasicAuth(username, api_token),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    if response.status_code not in (201, 200):
        logger.error("Failed to create Jira subtask for '%s': %s", summary, response.text)
        return {}
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Create Jira subtasks from GitHub issue checklist.")
    parser.add_argument("github_issue_number", type=int, help="GitHub issue number to read checklist from")
    parser.add_argument("jira_parent_issue_key", help="Jira issue key to attach subtasks to")
    args = parser.parse_args()

    body = get_github_issue_body(args.github_issue_number)
    items = parse_checklist_items(body)

    if not items:
        logger.info("No checklist items found in GitHub issue %s.", args.github_issue_number)
        return

    logger.info("Found %d checklist items. Creating Jira subtasks...", len(items))
    for item in items:
        result = create_jira_subtask(args.jira_parent_issue_key, item)
        if result:
            logger.info("Created subtask %s for item: %s", result.get("key"), item)


if __name__ == "__main__":
    main()