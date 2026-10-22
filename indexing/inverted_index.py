from collections import defaultdict
from db.mongo import documents
from preprocessing.tokenizer import tokenize
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
    def build(self):
        print("Building Inverted Index...\n")
        total_docs = 0
        for doc in documents.find():
            total_docs += 1
            text = doc.get("text", "")
            tokens = tokenize(text)
            doc_id = str(doc["_id"])
            for token in set(tokens):
                self.index[token].add(doc_id)
        print(f"Indexed {total_docs} documents.")
        print(f"Vocabulary Size: {len(self.index)}")
        return self.index
    def search(self, term):
        term = term.lower()
        return list(self.index.get(term, []))