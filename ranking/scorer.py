"""Shared ranking score helpers."""

from __future__ import annotations

from collections import Counter
from math import sqrt
from typing import Sequence


def overlap_score(query_tokens: Sequence[str], document_tokens: Sequence[str]) -> float:
	if not query_tokens or not document_tokens:
		return 0.0

	query_counts = Counter(query_tokens)
	document_counts = Counter(document_tokens)

	numerator = sum(min(query_counts[token], document_counts[token]) for token in query_counts)
	denominator = sqrt(sum(count * count for count in query_counts.values())) * sqrt(
		sum(count * count for count in document_counts.values())
	)

	if not denominator:
		return 0.0

	return numerator / denominator
