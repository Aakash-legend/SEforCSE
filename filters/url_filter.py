from urllib.parse import urlparse
class URLFilter:
    BLOCKED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".gif", ".svg",
        ".pdf", ".zip", ".rar", ".exe",
        ".mp3", ".mp4", ".avi", ".mov",
        ".css", ".js", ".ico"
    }
    BLOCKED_KEYWORDS = {
        "login",
        "logout",
        "signup",
        "register",
        "signin",
        "account",
        "privacy",
        "terms",
        "cookie"
    }
    def is_valid(self, url):
        if not url:
            return False
        url = url.lower()
        # Ignore mail links
        if url.startswith("mailto:"):
            return False
        # Ignore JavaScript links
        if url.startswith("javascript:"):
            return False
        parsed = urlparse(url)
        # Only crawl HTTP/HTTPS
        if parsed.scheme not in ("http", "https"):
            return False
        # Ignore unwanted file types
        for ext in self.BLOCKED_EXTENSIONS:
            if parsed.path.endswith(ext):
                return False
        # Ignore unwanted pages
        for word in self.BLOCKED_KEYWORDS:
            if word in url:
                return False
        return True