import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import documents
from ddgs import DDGS


def search_reddit(query):
    with DDGS() as ddgs:
        results = ddgs.text(f"site:reddit.com {query}", max_results=5)

        saved = 0

        for result in results:
            doc = {
                "title": result["title"],
                "content": result.get("body", ""),
                "source": "reddit",
                "type": "discussion",
                "url": result["href"]
            }

            if not documents.find_one({"url": doc["url"]}):
                documents.insert_one(doc)
                print("Saved:", doc["title"])
                saved += 1

        print(f"\nTotal Reddit posts saved: {saved}")


if __name__ == "__main__":
    query = input("Enter Reddit query: ")
    search_reddit(query)