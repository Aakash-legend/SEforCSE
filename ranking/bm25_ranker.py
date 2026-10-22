"""BM25 ranking helpers."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from rank_bm25 import BM25Okapi

from preprocessing.tokenizer import preprocess_text


class BM25Ranker:
    def __init__(self, documents: Sequence[dict], text_field: str = "content"):
        self.documents = list(documents)
        self.text_field = text_field
        self.tokenized_documents = [preprocess_text(document.get(text_field, "")) for document in self.documents]
        self.model = BM25Okapi(self.tokenized_documents) if self.tokenized_documents else None

    def rank(self, query: str) -> List[Tuple[dict, float]]:
        if not self.model:
            return []

        query_tokens = preprocess_text(query)
        scores = self.model.get_scores(query_tokens)
        ranked = list(zip(self.documents, scores))
        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked


def rank_documents(query: str, documents: Sequence[dict], text_field: str = "content") -> List[Tuple[dict, float]]:
    return BM25Ranker(documents, text_field=text_field).rank(query)