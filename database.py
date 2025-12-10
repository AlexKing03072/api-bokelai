import sqlite3

DATABASE_URL = "./bokelai.db"


def get_db_connection() -> sqlite3.Connection:
    """取得 SQLite 連線和 cursor"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # 讓結果像字典一樣存取
    cur = conn.cursor()
    return conn, cur

def get_all_books(skip: int, limit: int) -> list[dict]:
    """取得所有書籍，支援
    分頁查詢書籍（手動連線管理）
    參數：
    - skip: 跳過前 N 筆
    - limit: 取得 N 筆
    返回：書籍列表（字典格式）
    """
    conn, cur = get_db_connection()
    try:
        cur.execute(
            "SELECT * FROM books ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, skip),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()
def get_book_by_id(book_id: int) -> dict | None:
    """
    根據 ID 取得單一書籍
    返回：書籍字典，或 None（若無）
    """
    conn, cur = get_db_connection()
    try:
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        cur.close()
        conn.close()

def create_book(title: str, author: str, publisher: str | None, price: int, publish_date: str | None, isbn: str | None, cover_url: str | None) -> int:
    """新增書籍，返回新的ID"""
    conn, cur = get_db_connection()
    try:
        cur.execute(
            "INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, author, publisher, price, publish_date, isbn, cover_url),
        )
        conn.commit()
        return cur.lastrowid  # 返回新 ID
    except Exception:
        conn.rollback()  # 失敗時復原
        raise
    finally:
        cur.close()
        conn.close()
def update_book(book_id: int, title: str, author: str, publisher: str | None, price: int, publish_date: str | None, isbn: str | None, cover_url: str | None) -> bool:
    """
    更新書籍（全量更新），返回更新後的書籍字典。
    如果書籍不存在，則返回 None。
    """
    conn, cur = get_db_connection()
    try:
        # 先檢查書籍是否存在
        cur.execute("SELECT id FROM books WHERE id = ?", (book_id,))
        if cur.fetchone() is None:
            return None  # 書籍不存在，直接返回 None

        # 執行更新
        cur.execute(
            """
            UPDATE books
            SET title = ?, author = ?, publisher = ?, price = ?, publish_date = ?, isbn = ?, cover_url = ?
            WHERE id = ?
            """,
            (title, author, publisher, price, publish_date, isbn, cover_url, book_id),
        )
        conn.commit()

        # 更新成功後，直接查詢並返回最新資料
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return dict(cur.fetchone())
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
def delete_book(book_id: int) -> bool:
    """
    刪除書籍。
    返回：True（成功刪除）或 False（書籍不存在）。
    """
    conn, cur = get_db_connection()
    try:
        cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        # cur.rowcount 會回傳受影響的行數，> 0 表示刪除成功
        return cur.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()