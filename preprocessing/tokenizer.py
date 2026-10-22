import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


def tokenize(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    tokens = word_tokenize(text)

    processed_tokens = []

    for token in tokens:

        if token not in stop_words:

            processed_tokens.append(
                stemmer.stem(token)
            )

    return processed_tokens