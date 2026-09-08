"""PDF 解析服务版: 路径传入,返回切片列表(不写文件)"""
import fitz

from app import config

MAX_CHUNK = config.MAX_CHUNK
OVERLAP = config.OVERLAP


def split_long(text, page_no):
    chunks = []
    start = 0
    while start < len(text):
        end = start + MAX_CHUNK
        chunks.append({"text": text[start:end].strip(), "page": page_no})
        if end >= len(text):
            break
        start = end - OVERLAP
    return chunks


def parse_pdf(path):
    """返回 [{text, page}, ...]"""
    doc = fitz.open(path)
    results = []
    for page_no, page in enumerate(doc, start=1):
        raw = page.get_text("text")
        for para in raw.split("\n\n"):
            para = " ".join(para.split())
            if len(para) < 10:
                continue
            if len(para) <= MAX_CHUNK:
                results.append({"text": para, "page": page_no})
            else:
                results.extend(split_long(para, page_no))
    doc.close()
    return results
