from config import SOURCES, CRAWLER
from spiders.base_spider import BaseSpider


class DocsSpider(BaseSpider):

    def __init__(self):

        super().__init__()

        self.seed_urls = SOURCES["docs"]

        self.allowed_domains = self.get_allowed_domains(
            self.seed_urls
        )

    def crawl(self):

        super().crawl(
            seed_urls=self.seed_urls,
            source="documentation",
            max_pages=CRAWLER["max_pages_per_spider"]
        )