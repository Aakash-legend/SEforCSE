import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from downloader.fetcher import Fetcher
from parser.html_parser import HTMLParser
fetcher = Fetcher()
parser = HTMLParser()
html = fetcher.fetch("https://react.dev")
document = parser.parse(html)
print("\nTitle:")
print(document["title"])
print("\nDescription:")
print(document["description"])
print("\nHeadings:")
print(document["headings"][:5])
print("\nParagraphs:")
print(document["paragraphs"][:3])
print("\nCode Blocks:")
print(len(document["code_blocks"]))
print("\nCombined Text Preview:")
print(document["text"][:500])