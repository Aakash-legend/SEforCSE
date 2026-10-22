"""Persistence helpers for crawl frontier state."""

from __future__ import annotations

from db.mongo import documents


def _collection():
    return documents.database["frontier_store"]


def enqueue(url: str):
    return _collection().insert_one({"url": url, "visited": False})


def dequeue():
    record = _collection().find_one_and_update(
        {"visited": False},
        {"$set": {"visited": True}},
        sort=[("_id", 1)],
    )
    return record["url"] if record else None