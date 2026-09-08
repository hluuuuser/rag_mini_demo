# RAG 知识库问答系统

基于 PDF 的本地知识库问答。上传教材 PDF,自动解析切片、向量化入库;用自然语言提问,系统从知识库检索相关内容,交给 DeepSeek 生成带出处引用的回答。



| 分类 | 技术栈 |
| --- | --- |
| 后端 | FastAPI · pymupdf · sentence-transformers · chromadb · pymysql |
| LLM | DeepSeek V4(deepseek-v4-flash) |
| 前端 | Vue3 · Vite · Element Plus · vue-router |
| 数据 | MySQL 8 · chroma(本地持久化) |



## 快速开始

前置:Python 3.12(conda)、MySQL 8、Node 22、DeepSeek API key。

```bash
# 1. 后端
cd backend
cp .env.example .env        # 填入 MySQL 密码和 DEEPSEEK_API_KEY
python scripts/init_db.py   # 建库建表
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs

# 2. 前端(另开终端)
cd frontend
npm install
npm run dev                 # http://localhost:5173
```



|方法|	路径|	说明|
| ---|---|---|
|POST	|/api/documents|	上传 PDF,解析入库,返回切片数|
|GET	|/api/documents|	文档列表|
|DELETE	|/api/documents/{doc_id}|	删除文档(chroma + MySQL 联动)|
|POST|	/api/chat| 问答，返回 answer + sources(引用) |