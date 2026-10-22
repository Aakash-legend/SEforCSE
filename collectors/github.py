import sys
import os
import requests

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GITHUB_TOKEN
from db.mongo import documents

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}


def fetch_github_issues(owner="facebook", repo="react"):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    print("Fetching from:", url)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    issues = response.json()
    saved_count = 0

    for issue in issues:

        # Skip pull requests
        if "pull_request" in issue:
            continue

        doc = {
            "title": issue["title"],
            "content": issue.get("body", ""),
            "source": "github",
            "type": "issue",
            "repo": f"{owner}/{repo}",
            "url": issue["html_url"],
            "comments_count": issue["comments"],
            "state": issue["state"],
            "created_at": issue["created_at"],
            "labels": [label["name"] for label in issue.get("labels", [])]
        }

        # Check duplicate by URL
        existing = documents.find_one({"url": doc["url"]})

        if existing:
            print("Already exists:", doc["title"])
            continue

        documents.insert_one(doc)
        saved_count += 1
        print("Saved:", doc["title"])

    print(f"\nTotal new issues saved: {saved_count}")


if __name__ == "__main__":
    fetch_github_issues()