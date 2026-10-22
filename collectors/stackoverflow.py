import sys
import os
import requests

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import documents


def fetch_stackoverflow_questions(tag="react"):
    url = (
        "https://api.stackexchange.com/2.3/questions"
        f"?order=desc"
        f"&sort=votes"
        f"&tagged={tag}"
        f"&site=stackoverflow"
        f"&filter=withbody"
    )

    print("Fetching from:", url)

    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    questions = response.json()["items"]

    saved_count = 0

    for question in questions[:10]:
        doc = {
            "title": question["title"],
            "content": question.get("body", ""),
            "source": "stackoverflow",
            "type": "question",
            "tags": question.get("tags", []),
            "score": question.get("score", 0),
            "answer_count": question.get("answer_count", 0),
            "is_answered": question.get("is_answered", False),
            "view_count": question.get("view_count", 0),
            "created_at": question.get("creation_date"),
            "url": question["link"]
        }

        # Prevent duplicates
        existing = documents.find_one({"url": doc["url"]})

        if existing:
            print("Already exists:", doc["title"])
            continue

        documents.insert_one(doc)
        saved_count += 1
        print("Saved:", doc["title"])

    print(f"\nTotal new StackOverflow questions saved: {saved_count}")


if __name__ == "__main__":
    fetch_stackoverflow_questions()