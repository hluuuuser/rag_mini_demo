"""服务层: 文档入库/删除的完整编排"""
import os
from datetime import datetime

from app import config, db
from app.rag import embedder, parser, store


def ingest_pdf_file(pdf_path, filename, doc_id):
    """解析 → 向量化 → 写 chroma → 登记 MySQL, 返回切片数"""
    chunks = parser.parse_pdf(pdf_path)
    texts = [c["text"] for c in chunks]

    print(f"[knowledge] 解析到 {len(chunks)} 个切片, 向量化中...")
    vectors = embedder.embed_texts(texts)

    col = store.get_collection()
    col.upsert(
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
        embeddings=vectors,
        documents=texts,
        metadatas=[{"page": c["page"], "doc_id": doc_id} for c in chunks],
    )
    db.insert_document(filename, doc_id, len(chunks))
    print(f"[knowledge] {filename} 入库完成: {len(chunks)} 切片")
    return len(chunks)


def delete_document(doc_id):
    """先删向量,再删 MySQL 记录(两库联动,顺序很重要)"""
    col = store.get_collection()
    col.delete(where={"doc_id": doc_id})   # 删 chroma
    ok = db.delete_document_by_doc_id(doc_id)  # 删 MySQL
    print(f"[knowledge] 删除 {doc_id}: chroma 联动 {'✓' if ok else '未找到'}")
    return ok


def make_doc_id():
    return "doc_" + datetime.now().strftime("%Y%m%d%H%M%S")


def save_upload(file_bytes, filename):
    """原始文件落盘到 data/uploads, 返回绝对路径"""
    name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    path = os.path.join(config.UPLOAD_DIR, name)
    with open(path, "wb") as f:
        f.write(file_bytes)
    return path
