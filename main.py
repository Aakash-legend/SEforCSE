import sys
import subprocess
from spiders.docs_spider import DocsSpider
from spiders.blogs_spider import BlogsSpider
from spiders.qa_spider import QASpider
from spiders.forums_spider import ForumsSpider
from indexing.index_manager import IndexManager
def crawl():
    print("\nStarting Crawlers...\n")
    DocsSpider().crawl()
    BlogsSpider().crawl()
    QASpider().crawl()
    ForumsSpider().crawl()
    print("\nCrawling Completed.\n")
def build_index():
    print("\nBuilding Indexes...\n")
    manager = IndexManager()
    manager.build()
    print("\nIndexes Built Successfully.\n")
def start_api():
    print("\nStarting FastAPI...\n")
    subprocess.run([
        "uvicorn",
        "api.main:app",
        "--reload"
    ])
def full_pipeline():
    crawl()
    build_index()
    start_api()
def menu():
    while True:
        print("\n" + "=" * 50)
        print("SEFORCSE")
        print("=" * 50)
        print("1. Crawl Websites")
        print("2. Build Indexes")
        print("3. Start Search API")
        print("4. Crawl + Build Indexes")
        print("5. Full Pipeline")
        print("0. Exit")
        print("=" * 50)
        choice = input("Enter choice: ")
        if choice == "1":
            crawl()
        elif choice == "2":
            build_index()
        elif choice == "3":
            start_api()
        elif choice == "4":
            crawl()
            build_index()
        elif choice == "5":
            full_pipeline()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "crawl":
            crawl()
        elif command == "index":
            build_index()
        elif command == "api":
            start_api()
        elif command == "all":
            full_pipeline()
        else:
            print("Unknown command.")
    else:
        menu()