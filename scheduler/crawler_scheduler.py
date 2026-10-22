from spiders.docs_spider import DocsSpider
from spiders.blogs_spider import BlogsSpider
from spiders.forums_spider import ForumsSpider
from spiders.qa_spider import QASpider
class CrawlerScheduler:
    def __init__(self):
        self.spiders = [
            DocsSpider(),
            BlogsSpider(),
            ForumsSpider(),
            QASpider()
        ]
    def run(self):
        print("=" * 70)
        print("Starting SEFORCSE Crawling")
        print("=" * 70)
        for spider in self.spiders:
            print(f"\nRunning {spider.__class__.__name__}")
            try:
                spider.start()
            except Exception as e:
                print(f"Error: {e}")
        print("\n" + "=" * 70)
        print("All Crawlers Finished")
        print("=" * 70)
if __name__ == "__main__":
    scheduler = CrawlerScheduler()
    scheduler.run()