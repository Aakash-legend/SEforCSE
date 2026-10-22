from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from downloader.fetcher import Fetcher
from parser.html_parser import HTMLParser
from parser.link_extractor import LinkExtractor
from filters.url_filter import URLFilter
from dedup.content_hash import ContentHash
from storage.document_store import DocumentStore
from frontier.queue_manager import QueueManager
class BaseSpider:
    """
    Base crawler for all SEFORCSE spiders.
    Child spiders only need to provide:
    - seed URLs
    - source name
    """
    def __init__(self, frontier=None):
        self.fetcher = Fetcher()
        self.parser = HTMLParser()
        self.extractor = LinkExtractor()
        self.filter = URLFilter()
        self.store = DocumentStore()
        self.frontier = frontier or QueueManager()
        # Filled automatically from seed URLs
        self.allowed_domains = set()
    # ---------------------------------------------------
    # Allowed Domains
    # ---------------------------------------------------
    def get_allowed_domains(self, seed_urls):
        """
        Generate allowed domains automatically
        from seed URLs.
        """
        return {
            urlparse(url).netloc.lower()
            for url in seed_urls
        }
    def is_allowed_domain(self, url):
        """
        Check whether URL belongs to one of the
        allowed domains.
        """
        if not self.allowed_domains:
            return True
        domain = urlparse(url).netloc.lower()
        return any(
            domain == allowed or domain.endswith("." + allowed)
            for allowed in self.allowed_domains
        )
    # ---------------------------------------------------
    # URL Normalization
    # ---------------------------------------------------
    def normalize_url(self, url):
        """
        Remove fragments and tracking parameters.
        """
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        blocked = {
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "fbclid",
            "gclid"
        }
        cleaned_query = {
            k: v
            for k, v in query.items()
            if k not in blocked
        }
        normalized = parsed._replace(
            query=urlencode(cleaned_query, doseq=True),
            fragment=""
        )
        return urlunparse(normalized)
    # ---------------------------------------------------
    # Crawl
    # ---------------------------------------------------
    def crawl(self, seed_urls, source="generic", max_pages=20):
        self.allowed_domains = self.get_allowed_domains(seed_urls)
        print("\nAllowed Domains:")
        for domain in self.allowed_domains:
            print("-", domain)
        # Add seed URLs
        for url in seed_urls:
            self.frontier.add_url(
                (self.normalize_url(url), 0)
            )
        crawled = 0
        while (
            self.frontier.queue_size() > 0
            and crawled < max_pages
        ):
            item = self.frontier.get_next_url()
            if item is None:
                break
            url, depth = item
            if self.frontier.is_visited(url):
                continue
            print("\n" + "=" * 70)
            print(f"Crawling : {url}")
            print(f"Depth    : {depth}")
            html = self.fetcher.fetch(url)
            if html is None:
                print("Download failed.")
                self.frontier.mark_visited(url)
                continue
            document = self.parser.parse(html)
            document["url"] = url
            document["source"] = source
            document["depth"] = depth
            content_hash = ContentHash.hash_content(
                document["text"]
            )
            document["content_hash"] = content_hash
            # URL duplicate
            if self.store.find_by_url(url):
                print("URL already indexed.")
                self.frontier.mark_visited(url)
                continue
            # Content duplicate
            if self.store.find_by_content_hash(content_hash):
                print("Duplicate content.")
                self.frontier.mark_visited(url)
                continue
            self.store.save_document(document)
            print(f"Saved : {document['title']}")
            links = self.extractor.extract(html, url)
            print(f"Extracted Links : {len(links)}")
            added = 0
            for link in links:
                link = self.normalize_url(link)
                if not self.filter.is_valid(link):
                    continue
                if not self.is_allowed_domain(link):
                    continue
                if self.frontier.is_visited(link):
                    continue
                self.frontier.add_url(
                    (link, depth + 1)
                )
                added += 1
            print(f"Added to Queue : {added}")
            self.frontier.mark_visited(url)
            crawled += 1
        print("\n" + "=" * 70)
        print("Crawling Finished")
        print(f"Pages Crawled : {crawled}")
        print(f"Visited URLs  : {self.frontier.visited_size()}")
        print(f"Remaining URLs: {self.frontier.queue_size()}")