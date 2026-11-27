import argparse
import os
import sys
from datetime import datetime, timezone
from typing import List, Dict, Optional

import requests


GITHUB_API_URL = "https://api.github.com"


def get_auth_headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return {"Authorization": f"token {token}"}
    return {}


def get_tag_commit_date(repo: str, tag: str) -> Optional[datetime]:
    url = f"{GITHUB_API_URL}/repos/{repo}/git/refs/tags/{tag}"
    resp = requests.get(url, headers=get_auth_headers())
    if resp.status_code != 200:
        return None
    ref_data = resp.json()
    # Resolve annotated tags
    if ref_data["object"]["type"] == "tag":
        tag_url = ref_data["object"]["url"]
        tag_resp = requests.get(tag_url, headers=get_auth_headers())
        if tag_resp.status_code != 200:
            return None
        tag_obj = tag_resp.json()
        commit_sha = tag_obj["object"]["sha"]
    else:
        commit_sha = ref_data["object"]["sha"]
    commit_url = f"{GITHUB_API_URL}/repos/{repo}/commits/{commit_sha}"
    commit_resp = requests.get(commit_url, headers=get_auth_headers())
    if commit_resp.status_code != 200:
        return None
    commit_data = commit_resp.json()
    date_str = commit_data["commit"]["committer"]["date"]
    return datetime.fromisoformat(date_str.rstrip("Z")).replace(tzinfo=timezone.utc)


def fetch_merged_prs(
    repo: str,
    since: datetime,
    until: Optional[datetime] = None,
) -> List[Dict]:
    prs: List[Dict] = []
    page = 1
    per_page = 100
    while True:
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
            "per_page": per_page,
            "page": page,
        }
        url = f"{GITHUB_API_URL}/repos/{repo}/pulls"
        resp = requests.get(url, headers=get_auth_headers(), params=params)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        for pr in batch:
            if not pr.get("merged_at"):
                continue
            merged_at = datetime.fromisoformat(pr["merged_at"].rstrip("Z")).replace(tzinfo=timezone.utc)
            if merged_at < since:
                continue
            if until and merged_at > until:
                continue
            prs.append(
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["html_url"],
                    "user": pr["user"]["login"],
                    "merged_at": merged_at,
                }
            )
        if len(batch) < per_page:
            break
        page += 1
    prs.sort(key=lambda x: x["merged_at"])
    return prs


def generate_release_notes(repo: str, since_tag: str, until_tag: Optional[str]) -> str:
    since_date = get_tag_commit_date(repo, since_tag)
    if not since_date:
        sys.stderr.write(f"Unable to resolve tag '{since_tag}'.\n")
        sys.exit(1)
    until_date = None
    if until_tag:
        until_date = get_tag_commit_date(repo, until_tag)
        if not until_date:
            sys.stderr.write(f"Unable to resolve tag '{until_tag}'.\n")
            sys.exit(1)
    prs = fetch_merged_prs(repo, since_date, until_date)
    lines = [
        f"# Release Notes",
        f"**Repository:** {repo}",
        f"**Since:** {since_tag} ({since_date.isoformat()})",
    ]
    if until_tag:
        lines.append(f"**Until:** {until_tag} ({until_date.isoformat()})")
    lines.append("")
    if not prs:
        lines.append("_No merged pull requests in this range._")
    else:
        for pr in prs:
            merged_str = pr["merged_at"].strftime("%Y-%m-%d")
            lines.append(f"- {pr['title']} (#{pr['number']}) by @{pr['user']} on {merged_str}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release notes from merged PRs.")
    parser.add_argument("--repo", required=True, help="GitHub repository in 'owner/name' format.")
    parser.add_argument("--since-tag", required=True, help="Tag name to start from (exclusive).")
    parser.add_argument("--until-tag", help="Tag name to end at (inclusive).")
    args = parser.parse_args()
    notes = generate_release_notes(args.repo, args.since_tag, args.until_tag)
    print(notes)


if __name__ == "__main__":
    main()