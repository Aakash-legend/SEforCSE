from collections import defaultdict
from bson import ObjectId
from preprocessing.tokenizer import tokenize
from indexing.index_manager import IndexManager
from db.mongo import documents
class QueryEngine:
    def __init__(self):
        print("Loading indexes...")
        manager = IndexManager()
        self.inverted = manager.load("inverted.pkl")
        self.bm25 = manager.load("bm25.pkl")
        print("Indexes loaded successfully.\n")
    def search(self, query, source=None, top_k=20):
        tokens = tokenize(query)
        scores = defaultdict(float)
        candidate_docs = set()
        # -----------------------------------------
        # Find candidate documents
        # -----------------------------------------
        for token in tokens:
            docs = self.inverted.search(token)
            candidate_docs.update(docs)
        # -----------------------------------------
        # BM25 Ranking
        # -----------------------------------------
        for doc_id in candidate_docs:
            bm25_doc = self.bm25.index.get(doc_id, {})
            score = 0
            for token in tokens:
                score += bm25_doc.get(token, 0)
            # -----------------------------------------
            # Apply Source Filter
            # -----------------------------------------
            doc = documents.find_one(
                {"_id": ObjectId(doc_id)}
            )
            if doc is None:
                continue
            if source is not None:
                if doc["source"] != source:
                    continue
            scores[doc_id] = score
        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return ranked[:top_k]