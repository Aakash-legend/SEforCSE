import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from spiders.base_spider import BaseSpider
spider = BaseSpider()
spider.crawl(
    seed_urls=[
        "https://react.dev"
    ],
    source="react",
    max_pages=5
)

