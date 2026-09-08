"""
向量库封装: chromadb 持久化
- 目录固定为 RAG-DEMO/data/chroma
- collection 名 "kb", 距离用余弦
"""
import os
import chromadb

CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "chroma"))
COLLECTION_NAME = "rag_kb"

_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def search(query_vector, top_k=3, doc_id=None):
    """按向量检索,可选限定某篇文档"""
    col = get_collection()
    where = {"doc_id": doc_id} if doc_id else None
    res = col.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where,
    )
    out = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({"text": doc, "page": meta["page"], "score": round(1 - dist, 4)})
    return out
