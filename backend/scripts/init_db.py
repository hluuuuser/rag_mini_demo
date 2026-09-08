"""
M3: MySQL 建库建表 + 登记当前文档
职责: rag_kb 库 + documents 表;把已入库的 computer_english 文档登记进去
运行: 先填好下面的 DB_PASSWORD,再 cd backend && python scripts/init_db.py
"""
import pymysql

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "root"          # ← 填你的 MySQL root 密码
DB_NAME = "rag_kb"

# # 和 chroma 里对齐:文档唯一标识 + 切片数(来自 M2 入库结果)
# DOC_ID = "computer_english"
# FILENAME = "软考中级软件设计师知识点汇总.pdf"
# CHUNK_COUNT = 765

CREATE_DB = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  filename VARCHAR(255) NOT NULL,
  doc_id VARCHAR(64) NOT NULL UNIQUE,
  chunk_count INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


def main():
    # 第一步: 连 MySQL(不指定库),建库
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, charset="utf8mb4")
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_DB)
            print(f"数据库 {DB_NAME} 就绪")
    finally:
        conn.close()

    # # 第二步: 连 rag_kb,建表 + 登记文档
    # conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset="utf8mb4")
    # try:
    #     with conn.cursor() as cur:
    #         cur.execute(CREATE_TABLE)
    #         cur.execute(
    #             "INSERT INTO documents (filename, doc_id, chunk_count) VALUES (%s, %s, %s) "
    #             "ON DUPLICATE KEY UPDATE chunk_count = VALUES(chunk_count)",
    #             (FILENAME, DOC_ID, CHUNK_COUNT),
    #         )
    #     conn.commit()
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT id, filename, doc_id, chunk_count, created_at FROM documents")
    #         for row in cur.fetchall():
    #             print("记录:", row)
    # finally:
    #     conn.close()


if __name__ == "__main__":
    main()
