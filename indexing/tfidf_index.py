import math
from collections import Counter
from db.mongo import documents
from preprocessing.tokenizer import tokenize
class TFIDFIndex:
    def __init__(self):
        self.document_count = 0
        self.document_frequency = {}
        self.tfidf = {}
    def build(self):
        docs = list(documents.find())
        self.document_count = len(docs)
        # ----------------------------
        # Document Frequency
        # ----------------------------
        df = Counter()
        tokenized_docs = {}
        for doc in docs:
            doc_id = str(doc["_id"])
            tokens = tokenize(doc.get("text", ""))
            tokenized_docs[doc_id] = tokens
            df.update(set(tokens))
        self.document_frequency = dict(df)
        # ----------------------------
        # TF-IDF
        # ----------------------------
        for doc_id, tokens in tokenized_docs.items():
            tf = Counter(tokens)
            total_terms = len(tokens)
            self.tfidf[doc_id] = {}
            for term, freq in tf.items():
                tf_value = freq / total_terms
                idf = math.log(
                    self.document_count /
                    (1 + self.document_frequency[term])
                )
                self.tfidf[doc_id][term] = tf_value * idf
        print(f"TF-IDF built for {self.document_count} documents.")
        return self.tfidf