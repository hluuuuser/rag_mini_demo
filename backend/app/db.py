"""MySQL 工具: documents 表读写"""
import pymysql
from pymysql.cursors import DictCursor

from app import config


def get_conn():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset="utf8mb4",
        cursorclass=DictCursor,
    )


def list_documents():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, filename, doc_id, chunk_count, created_at FROM documents ORDER BY id DESC")
            rows = cur.fetchall()
        for r in rows:
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        return rows
    finally:
        conn.close()


def insert_document(filename, doc_id, chunk_count):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (filename, doc_id, chunk_count) VALUES (%s, %s, %s)",
                (filename, doc_id, chunk_count),
            )
        conn.commit()
    finally:
        conn.close()


def delete_document_by_doc_id(doc_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE doc_id = %s", (doc_id,))
            deleted = cur.rowcount
        conn.commit()
        return deleted > 0
    finally:
        conn.close()
