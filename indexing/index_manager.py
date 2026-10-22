import os
import pickle
from indexing.inverted_index import InvertedIndex
from indexing.bm25_index import BM25Index
class IndexManager:
    INDEX_DIR = "indexing/indexes"
    def __init__(self):
        os.makedirs(self.INDEX_DIR, exist_ok=True)
    def build(self):
        print("Building Inverted Index...")
        inverted = InvertedIndex()
        inverted.build()
        print("Building BM25 Index...")
        bm25 = BM25Index()
        bm25.build()
        # Save complete objects
        self.save("inverted.pkl", inverted)
        self.save("bm25.pkl", bm25)
        print("Indexes saved successfully.")
    def save(self, filename, data):
        path = os.path.join(self.INDEX_DIR, filename)
        with open(path, "wb") as f:
            pickle.dump(data, f)
    def load(self, filename):
        path = os.path.join(self.INDEX_DIR, filename)
        with open(path, "rb") as f:
            return pickle.load(f)