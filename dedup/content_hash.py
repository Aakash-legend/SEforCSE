import hashlib
class ContentHash:
    @staticmethod
    def hash_url(url: str) -> str:
        """
        Generate a unique hash for a URL.
        """
        return hashlib.sha256(url.encode("utf-8")).hexdigest()
    @staticmethod
    def hash_content(content: str) -> str:
        """
        Generate a unique hash for page content.
        """
        normalized = " ".join(content.split())
        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()
    @staticmethod
    def is_duplicate(hash_value, existing_hashes):
        """
        Check whether a hash already exists.
        """
        return hash_value in existing_hashes