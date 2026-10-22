"""TF-IDF ranking helpers."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_documents(query: str, documents: Sequence[dict], text_field: str = "content") -> List[Tuple[dict, float]]:
	if not documents:
		return []

	texts = [document.get(text_field, "") for document in documents]
	vectorizer = TfidfVectorizer(stop_words="english")
	matrix = vectorizer.fit_transform(texts + [query])
	query_vector = matrix[-1]
	document_matrix = matrix[:-1]
	scores = cosine_similarity(query_vector, document_matrix).ravel()

	ranked = list(zip(documents, scores))
	ranked.sort(key=lambda item: item[1], reverse=True)
	return ranked
