import os
import sys
import time
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from db.mongo import documents
from search.query_engine import QueryEngine
app = FastAPI()
# --------------------------------------------------
# CORS
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Load Query Engine
# --------------------------------------------------
engine = QueryEngine()
# --------------------------------------------------
# Home
# --------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "SEFORCSE Developer Search Engine Running"
    }
# --------------------------------------------------
# Search API
# --------------------------------------------------
@app.get("/search")
def search_api(
    q: str,
    source: str | None = None
):
    start_time = time.time()
    results = engine.search(
        query=q,
        source=source
    )
    final_results = []
    for doc_id, score in results:
        doc = documents.find_one(
            {"_id": ObjectId(doc_id)}
        )
        if not doc:
            continue
        text = doc.get("text", "").replace("\n", " ")
        if len(text) > 220:
            snippet = text[:220] + "..."
        else:
            snippet = text
        final_results.append({
            "title": doc.get("title", ""),
            "source": doc.get("source", ""),
            "url": doc.get("url", ""),
            "score": round(score, 3),
            "snippet": snippet
        })
    search_time = round(
        time.time() - start_time,
        3
    )
    return {
        "query": q,
        "count": len(final_results),
        "time": search_time,
        "results": final_results
    }