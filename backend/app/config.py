"""集中配置: 路径 + 数据库 + 密钥,全部从 backend/.env 读"""
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 backend/.env

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # RAG-DEMO/
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")   # 上传的原始 PDF
CHROMA_DIR = os.path.join(DATA_DIR, "chroma")    # 向量库持久化

os.makedirs(UPLOAD_DIR, exist_ok=True)

# DATABASE CONFIG
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "rag_kb")

# LLM CONFIG
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
LLM_MODEL = os.getenv("LLM_MODEL", "")

# PDF CONFIG
MAX_CHUNK = int(os.getenv("MAX_CHUNK", 200))
OVERLAP = int(os.getenv("OVERLAP", 20))

#
TOPK = int(os.getenv("TOPK", 3))