"""路由: 问答 — RAG 核心链路(检索 → 拼上下文 → LLM 生成 → 带引用返回)"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from app import config
from app.rag import embedder, llm, store

router = APIRouter(prefix="/api", tags=["chat"])

SYSTEM_PROMPT = (
    "你是一个基于本地知识库的问答助手。回答规则:\n"
    "1. 只依据下面给出的【参考资料】回答, 不要使用资料之外的知识;\n"
    "2. 回答中凡是来自资料的句子, 结尾标注出处编号, 如 [1][2];\n"
    "3. 如果资料里没有答案, 直接回答“资料中未找到相关内容”, 不要编造。"
)


class ChatRequest(BaseModel):
    question: str


def _do_chat(question: str):
    # 1. 检索: 问题向量化 → 取 Top3
    vec = embedder.embed_query(question)
    hits = store.search(vec, top_k=config.TOPK)

    if not hits:
        return {"answer": "知识库为空或未检索到相关内容", "sources": []}

    # 2. 拼上下文: 每条带编号和页码, 编号就是给 LLM 的"引用锚点"
    context = "\n\n".join(
        f"[{i}] (第{hit['page']}页) {hit['text']}" for i, hit in enumerate(hits, 1)
    )
    user_content = f"【参考资料】\n{context}\n\n【问题】\n{question}"

    # 3. LLM 生成
    answer = llm.chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
    )

    # 4. 返回答案 + 引用清单(前端靠它展示出处)
    return {
        "answer": answer,
        "sources": [
            {"index": i, "text": h["text"][:200], "page": h["page"], "score": h["score"]}
            for i, h in enumerate(hits, 1)
        ],
    }


@router.post("/chat")
async def chat_api(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(400, "问题不能为空")
    return await run_in_threadpool(_do_chat, req.question.strip())
