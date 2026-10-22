import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import documents


HEADERS = {
    "User-Agent": "SEFORCSE/1.0 (Developer Search Engine)"
}


def fetch_wikipedia(query="React"):
    search_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }

    response = requests.get(search_url, params=params, headers=HEADERS)

    if response.status_code != 200:
        print("Search Error:", response.status_code)
        print(response.text)
        return

    results = response.json()["query"]["search"]

    saved_count = 0

    for item in results[:5]:
        title = item["title"].replace(" ", "_")

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

        summary_response = requests.get(summary_url, headers=HEADERS)

        if summary_response.status_code != 200:
            print("Skipping:", title)
            continue

        data = summary_response.json()

        doc = {
            "title": data.get("title"),
            "content": data.get("extract", ""),
            "source": "wikipedia",
            "type": "concept",
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
        }

        existing = documents.find_one({"url": doc["url"]})

        if existing:
            print("Already exists:", doc["title"])
            continue

        documents.insert_one(doc)
        saved_count += 1
        print("Saved:", doc["title"])

    print(f"\nTotal new Wikipedia pages saved: {saved_count}")


if __name__ == "__main__":
    query = input("Enter topic: ")
    fetch_wikipedia(query)