"""
Wraps a persistent Chroma collection — the vector store the Lore Analyst
retrieves from. Uses Chroma's default local embedding model (all-MiniLM-L6-v2),
downloaded once on first use and cached afterward. This means indexing costs
nothing per-chunk and needs no API key; only the actual answer-generation step
(Gemini Flash) needs one.
"""

import chromadb
from app.core.config import settings

_client = None
_collection = None

COLLECTION_NAME = "bleach_lore"


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(COLLECTION_NAME)
    return _collection


def reset_collection():
    """Wipes and recreates the collection — used before a full reindex."""
    global _collection
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def upsert(ids: list[str], documents: list[str], metadatas: list[dict], batch_size: int = 8):
    """
    Upserts in small batches rather than all at once. Embedding many documents
    in a single call maximizes peak memory usage during inference — small
    batches keep memory usage low throughout, which matters on memory-limited
    hosts (e.g. Render's free tier, 512MB RAM).
    """
    if not ids:
        return
    collection = get_collection()
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )


def query(query_text: str, n_results: int = 6, max_distance: float = 1.1):
    """
    Returns the most relevant chunks for a question, with their metadata.
    Filters out weak/irrelevant matches (distance above max_distance) so a
    question with no real grounding doesn't get misrepresented as cited —
    Chroma always returns its closest available matches even when none of
    them are actually relevant, so this cutoff matters.
    """
    collection = get_collection()
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[query_text], n_results=min(n_results, collection.count()))
    chunks = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        if dist <= max_distance:
            chunks.append({"text": doc, "metadata": meta, "distance": dist})
    return chunks