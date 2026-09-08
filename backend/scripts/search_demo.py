"""
M2 验收: 检索 demo
运行: cd backend && python scripts/search_demo.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.embedder import embed_query
from app.rag.store import search


def main():
    q = input("你的问题: ").strip()
    if not q:
        print("问题不能为空")
        return

    vec = embed_query(q)
    hits = search(vec, top_k=3)

    print("\n===== Top 3 相关片段 =====")
    for i, h in enumerate(hits, 1):
        print(f"[{i}] 相关度 {h['score']} | 第 {h['page']} 页")
        print(h["text"][:200])
        print()


if __name__ == "__main__":
    main()
