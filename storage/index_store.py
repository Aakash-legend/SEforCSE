"""Persistence helpers for search indexes."""

from __future__ import annotations

from typing import Any, Dict

from db.mongo import documents


def _collection():
    return documents.database["index_store"]


def save_index(name: str, payload: Dict[str, Any]):
    return _collection().replace_one({"name": name}, {"name": name, "payload": payload}, upsert=True)


def load_index(name: str):
    record = _collection().find_one({"name": name})
    return record["payload"] if record else None