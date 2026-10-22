# SEforCSE — Developer Search Engine

SEforCSE is a Python-based vertical search engine designed to help developers find relevant Computer Science documentation, technical articles, programming resources, and developer discussions from multiple sources through a single search interface.

The project combines a modular web crawler, HTML content extraction, text preprocessing, inverted indexing, BM25-based ranking, a FastAPI search API, and a browser-based frontend.

> **Project status:** Early-stage prototype. Core crawling, indexing, search, API, and frontend components are implemented. End-to-end reliability and search relevance are still being improved.

## Features

### Content Collection
- Modular spiders for documentation, technical blogs, Q&A sites, and developer forums.
- Configurable seed URLs and source categories.
- URL normalization and filtering.
- Crawl frontier and visited-URL tracking.
- Duplicate detection using URLs and content hashes.
- Separate collector modules for GitHub, Reddit, Stack Overflow, and Wikipedia.

### Text Processing and Indexing
- HTML parsing and extraction of document content.
- Text normalization, tokenization, English stopword removal, and Porter stemming.
- Inverted index for candidate document retrieval.
- BM25-based document ranking.
- Index persistence using Python pickle files.
- Additional TF-IDF indexing and ranking modules in the codebase.

### Search API
- FastAPI-based search service.
- Search endpoint with query and optional source filtering.
- Ranked search results containing titles, URLs, source labels, snippets, and scores.
- Result count and elapsed search time.

### Frontend
- Browser-based search interface built with HTML, CSS, and JavaScript.
- Search result cards with source information and links.
- Source filtering, loading indicators, and empty-result handling.
- Light, dark, and amber themes.
- Keyboard shortcuts for search and clearing the query.

## Technology Stack

| Component | Technologies |
|---|---|
| Language | Python |
| API | FastAPI, Uvicorn |
| Database | MongoDB, PyMongo |
| Crawling and parsing | Requests, Beautiful Soup, lxml |
| Text processing | NLTK |
| Search and ranking | Inverted index, BM25, TF-IDF-related modules |
| Frontend | HTML, CSS, JavaScript |
| Configuration | Environment variables, python-dotenv |
| Additional libraries | scikit-learn, Scrapy, rank-bm25, sentence-transformers, FAISS |

The listed dependencies reflect the current requirements file; not every dependency is necessarily used by the active search path.

## Project Structure

```text
SEFORCSE/
├── api/
│   └── main.py                 # FastAPI application and search endpoint
├── collectors/                 # External source collectors
├── db/
│   └── mongo.py                # MongoDB connection
├── dedup/                      # Content duplicate detection
├── downloader/                 # HTTP fetching
├── filters/                    # URL and content filtering
├── frontend/
│   ├── index.html              # Search interface
│   ├── style.css               # Frontend styling
│   └── app.js                  # Search and UI interactions
├── frontier/                   # Crawl queue management
├── indexing/
│   ├── bm25_index.py
│   ├── inverted_index.py
│   ├── tfidf_index.py
│   ├── index_manager.py
│   └── indexes/                # Locally generated indexes
├── parser/                     # HTML parsing and link extraction
├── preprocessing/              # Text tokenization
├── ranking/                    # Ranking-related modules
├── scheduler/                  # Crawler scheduling
├── search/
│   ├── query_engine.py         # Query processing and retrieval
│   └── autocomplete.py
├── spiders/                    # Documentation, blog, forum and Q&A spiders
├── storage/                    # Document, frontier and index storage
├── tests/                      # Crawler, fetcher and parser tests
├── config.py                   # Sources and crawler configuration
├── main.py                     # Pipeline entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install or configure the following:

- Python 3.11 or a compatible version for the project's dependencies.
- MongoDB, accessible from the machine running SEforCSE.
- Git.
- A modern web browser.

Some collectors may require API credentials, depending on the source being accessed.

### 1. Clone the Repository

```bash
git clone https://github.com/Aakash-legend/SEFORCSE.git
cd SEFORCSE
```

### 2. Create and Activate a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use the activation method appropriate to your local execution policy, or run the environment's Python executable directly.

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The tokenizer requests the required NLTK resources when it is imported. An internet connection may be needed for the initial download.

### 4. Configure Environment Variables

Create a local `.env` file in the project root. Add the credentials and connection settings needed for your environment.

Example:

```dotenv
MONGO_URI=mongodb://localhost:27017/
GITHUB_TOKEN=
REDDIT_CLIENT_ID=
REDDIT_SECRET=
REDIS_HOST=localhost
REDIS_PORT=6379
```

Replace the example MongoDB URI if your database runs elsewhere. Populate collector credentials when required.

**Never commit `.env` or real API tokens.** The repository's `.gitignore` excludes environment files. Keep credentials private and use `.env.example` only for placeholder values.

### 5. Start MongoDB

Ensure that your MongoDB instance is running and reachable through `MONGO_URI`.

SEforCSE uses a MongoDB database named `seforcse` and a `documents` collection.

### 6. Run the Application

The root `main.py` provides an interactive menu and command-line options for the pipeline.

**Interactive menu**

```bash
python main.py
```

**Run individual stages**

```bash
python main.py crawl
python main.py index
python main.py api
```

**Run the full pipeline**

```bash
python main.py all
```

The full pipeline runs crawling, index construction, and then starts the API. Allow the crawler to finish and confirm that the index files have been generated before starting searches.

### 7. Open the Search Interface

Start the API using the steps above. The frontend currently targets:

```text
http://127.0.0.1:8000/search
```

Open `frontend/index.html` in your browser to use the search interface.

The API root can be checked at:

```text
http://127.0.0.1:8000/
```

A successful response from the root endpoint indicates that the API is running. Successful search also requires a reachable MongoDB database and built index files.

## Search API

### Endpoint

```http
GET /search?q={query}
```

Optional source filtering:

```http
GET /search?q=python&source=docs
```

Example request:

```text
http://127.0.0.1:8000/search?q=python
```

### Response Format

A successful request returns JSON in this general format:

```json
{
  "query": "python",
  "count": 1,
  "time": 0.012,
  "results": [
    {
      "title": "Example documentation page",
      "source": "docs",
      "url": "https://example.com/docs",
      "score": 1.234,
      "snippet": "Example text extracted from the indexed document..."
    }
  ]
}
```

The values above are illustrative, not measured results. Actual results depend on the crawled corpus and generated indexes.

## Current Search Pipeline

1. **Crawl:** Fetch pages from configured seed sources.
2. **Parse:** Extract titles and textual content from HTML.
3. **Filter and deduplicate:** Reject unwanted URLs and avoid storing duplicate pages or content.
4. **Store:** Save collected documents in MongoDB.
5. **Preprocess:** Normalize query and document text using the tokenizer.
6. **Index:** Build an inverted index and BM25-related index data.
7. **Retrieve and rank:** Retrieve candidate documents and rank them using BM25 scores.
8. **Serve:** Return ranked results through FastAPI.
9. **Display:** Render results in the browser-based interface.

## Current Limitations

SEforCSE is under active development. Current limitations and areas for validation include:

- Search relevance and ranking quality need further evaluation.
- Snippets are currently generated from the beginning of stored document text rather than being selected around query matches.
- The active query path uses the inverted index and BM25 scoring; additional ranking modules are not necessarily integrated into that path.
- Source coverage depends on crawling success, source structure, access restrictions, and available credentials.
- Search requires compatible MongoDB documents and locally generated index files.
- Automated tests are present, but complete test-suite results and end-to-end reliability have not yet been established.
- Production deployment, monitoring, security hardening, and scalability remain future work.

## Roadmap

- Improve content extraction and remove navigation and boilerplate text.
- Improve URL and content quality filtering.
- Introduce field-aware indexing for titles, headings, and body text.
- Generate query-aware snippets.
- Improve ranking relevance and programming-language disambiguation.
- Expand and validate source-specific collectors.
- Add automated unit and integration tests for the full search pipeline.
- Evaluate search quality using a representative set of queries and relevance judgments.
- Improve configuration, logging, error handling, and deployment documentation.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request describing the change.

## License

No license has been specified in this README. Add a `LICENSE` file and update this section before distributing the project under a particular open-source license.

---

**SEforCSE — Building a focused search experience for Computer Science and developer resources.**
