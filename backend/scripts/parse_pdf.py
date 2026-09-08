"""
M1: PDF 解析 + 切片
职责: 把 PDF 变成检索单元(chunk)列表,每个 chunk 带页码。
策略: 按空行分段; 段落过长(>400字)滑窗切,重叠 50 字。
输出: data/chunks/<文件名>.jsonl  (每行一个 JSON)
运行: conda activate fastapi-framework 后,在 backend 目录执行
      python scripts/parser.py
"""

import os
import json
import pymupdf  # pymupdf

PDF_PATH = r"E:\HL\MyProjectors\RAG-DEMO\backend\dataset\计算机专业英语.pdf"
MAX_CHUNK = 400   # 切片字数上限
OVERLAP = 50      # 滑窗重叠字数(防止语义被切断)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chunks")


def split_long(text: str, page_no: int):
    """长文本滑窗切片: 每次取 MAX_CHUNK 字, 下一次起点回退 OVERLAP"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + MAX_CHUNK
        chunks.append({"text": text[start:end].strip(), "page": page_no})
        if end >= len(text):
            break
        start = end - OVERLAP
    return chunks


def extract_pdf(path: str):
    """返回 [{text, page}, ...]"""
    doc = pymupdf.open(path)
    print(f"[探针] 总页数: {len(doc)}")
    results = []
    for page_no, page in enumerate(doc, start=1):
        raw = page.get_text("text")
        if page_no <= 2:  # 只打印前两页,判断文档结构
            print(f"[探针] 第{page_no}页 字符数={len(raw.strip())} 预览: {raw.strip()[:150].replace(chr(10), ' / ')}")
        for para in raw.split("\n\n"):
            para = " ".join(para.split())
            if len(para) < 10:   # 跳过页眉页脚残渣
                continue
            if len(para) <= MAX_CHUNK:
                results.append({"text": para, "page": page_no})
            else:
                results.extend(split_long(para, page_no))
    doc.close()
    return results


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chunks = extract_pdf(PDF_PATH)
    out_file = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(PDF_PATH))[0] + ".jsonl")
    print(out_file)
    with open(out_file, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"[结果] 切片总数: {len(chunks)}")
    print(f"[结果] 输出文件: {out_file}")
    print("----- 前 3 条切片预览 -----")
    for c in chunks[:3]:
        print(f"  (第{c['page']}页) {c['text'][:80]}")


if __name__ == "__main__":
    main()
