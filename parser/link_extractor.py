from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
class LinkExtractor:
    def extract(self, html, base_url):
        """
        Extract all hyperlinks from a webpage.
        """
        soup = BeautifulSoup(html, "lxml")
        links = set()
        for tag in soup.find_all("a", href=True):
            href = tag["href"].strip()
            if not href:
                continue
            # Remove #fragment
            href = urldefrag(href).url
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            links.add(absolute_url)
        return list(links)