"""
Embedding 封装: 本地 bge 中文小模型
- 文档侧直接编码
- 查询侧加 bge 官方建议的前缀,提升检索准确率
"""
import os
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")  # 模型下载走国内镜像

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章:"

_model = None


def get_model():
    global _model
    if _model is None:
        print(f"[embedder] 首次加载模型 {MODEL_NAME},约 100MB,请耐心等待...")
        _model = SentenceTransformer(MODEL_NAME)
        print("[embedder] 模型加载完成")
    return _model


def embed_texts(texts):
    """文档切片向量化,批量"""
    return get_model().encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()


def embed_query(text):
    """单个查询向量化(加指令前缀)"""
    vec = get_model().encode([QUERY_PREFIX + text], normalize_embeddings=True)
    return vec[0].tolist()
