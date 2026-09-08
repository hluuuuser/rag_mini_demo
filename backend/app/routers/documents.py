"""路由: 文档上传/列表/删除"""
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool

from app import db, knowledge

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "仅支持 PDF 文件")

    content = await file.read()
    save_path = knowledge.save_upload(content, file.filename)
    doc_id = knowledge.make_doc_id()

    # 阻塞任务(模型加载+向量化)扔到线程池,不卡住服务器
    chunk_count = await run_in_threadpool(knowledge.ingest_pdf_file, save_path, file.filename, doc_id)

    return {"doc_id": doc_id, "filename": file.filename, "chunk_count": chunk_count}


@router.get("")
async def list_documents():
    return db.list_documents()


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    ok = await run_in_threadpool(knowledge.delete_document, doc_id)
    if not ok:
        raise HTTPException(404, "文档不存在")
    return {"deleted": doc_id}
