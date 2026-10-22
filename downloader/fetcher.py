import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
class Fetcher:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.headers = {
            "User-Agent": (
                "SEFORCSE/1.0 "
                "(Educational Search Engine; "
                "https://github.com/your-repo)"
            )
        }
    def fetch(self, url, timeout=10):
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[Fetcher] Error fetching {url}")
            print(e)
            return None