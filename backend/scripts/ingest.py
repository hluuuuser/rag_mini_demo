"""
M2 入库: 把 data/chunks/*.jsonl 向量化后写入 chroma
运行: cd backend && python scripts/ingest.py
"""
import sys
import os
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 让 import app 生效

from app.rag.embedder import embed_texts
from app.rag.store import get_collection

CHUNKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "chunks"))

DOC_ID = "computer_english"  # 本次只有一份文档;多文档时按文件名分别生成 doc_id


def main():
    files = sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.jsonl")))
    if not files:
        print("data/chunks 下没有 jsonl,先跑 M1")
        return

    chunks = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    chunks.append(json.loads(line))

    print(f"读取切片 {len(chunks)} 条,开始向量化...")
    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    col = get_collection()
    col.upsert(
        ids=[f"{DOC_ID}_{i}" for i in range(len(chunks))],
        embeddings=vectors,
        documents=texts,
        metadatas=[{"page": c["page"], "doc_id": DOC_ID} for c in chunks],
    )
    print(f"入库完成,collection 现有 {col.count()} 条切片")


if __name__ == "__main__":
    main()
