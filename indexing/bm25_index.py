import math
from collections import Counter
from db.mongo import documents
from preprocessing.tokenizer import tokenize
class BM25Index:
    def __init__(self):
        self.k1 = 1.5
        self.b = 0.75
        self.N = 0
        self.avg_doc_length = 0
        self.doc_lengths = {}
        self.doc_freq = {}
        self.index = {}
    def build(self):
        docs = list(documents.find())
        self.N = len(docs)
        tokenized_docs = {}
        total_length = 0
        df_counter = Counter()
        # -----------------------------
        # First Pass
        # -----------------------------
        for doc in docs:
            doc_id = str(doc["_id"])
            tokens = tokenize(doc.get("text", ""))
            tokenized_docs[doc_id] = tokens
            length = len(tokens)
            self.doc_lengths[doc_id] = length
            total_length += length
            df_counter.update(set(tokens))
        self.avg_doc_length = total_length / max(self.N, 1)
        self.doc_freq = dict(df_counter)
        # -----------------------------
        # Second Pass
        # -----------------------------
        for doc_id, tokens in tokenized_docs.items():
            tf = Counter(tokens)
            self.index[doc_id] = {}
            doc_len = self.doc_lengths[doc_id]
            for term, freq in tf.items():
                df = self.doc_freq[term]
                idf = math.log(
                    ((self.N - df + 0.5) /
                    (df + 0.5)) + 1
                )
                numerator = freq * (self.k1 + 1)
                denominator = (
                    freq +
                    self.k1 *
                    (
                        1 -
                        self.b +
                        self.b *
                        (doc_len / self.avg_doc_length)
                    )
                )
                score = idf * (numerator / denominator)
                self.index[doc_id][term] = score
        print(f"BM25 built for {self.N} documents.")
        return self.index