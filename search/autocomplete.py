"""Autocomplete helpers for query suggestions."""

from __future__ import annotations

from typing import List

from db.mongo import documents


def suggest(prefix: str, limit: int = 5) -> List[str]:
	normalized = prefix.strip().lower()

	if not normalized:
		return []

	suggestions: List[str] = []
	seen = set()

	for document in documents.find({}, {"title": 1}):
		title = document.get("title", "").strip()
		if not title:
			continue

		lowered = title.lower()
		if lowered.startswith(normalized) and lowered not in seen:
			seen.add(lowered)
			suggestions.append(title)

		if len(suggestions) >= limit:
			break

	return suggestions
