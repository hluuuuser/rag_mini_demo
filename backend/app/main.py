"""FastAPI 入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents
from app.routers import chat          # 新增

app = FastAPI(title="RAG Knowledge Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 本地开发全放行, 上线再收紧
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(chat.router)       # 新增

@app.get("/api/health")
def health():
    return {"status": "ok"}
