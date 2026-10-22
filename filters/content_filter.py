"""Content validation helpers."""

from __future__ import annotations


def is_valid_content(content: str, min_length: int = 50) -> bool:
    if not content:
        return False

    normalized = " ".join(content.split())
    return len(normalized) >= min_length