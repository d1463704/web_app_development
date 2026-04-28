"""
category.py — 分類 Model

提供分類（category）資料表的 CRUD 操作。
"""

from app.models.database import get_connection


def get_all():
    """
    取得所有分類。

    回傳:
        list[sqlite3.Row]: 分類列表
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM category ORDER BY id'
        ).fetchall()
        return rows
    finally:
        conn.close()


def get_by_id(category_id):
    """
    根據 ID 取得單一分類。

    參數:
        category_id (int): 分類 ID

    回傳:
        sqlite3.Row: 分類資料，找不到時回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM category WHERE id = ?',
            (category_id,)
        ).fetchone()
        return row
    finally:
        conn.close()


def create(name):
    """
    新增一個分類。

    參數:
        name (str): 分類名稱

    回傳:
        int: 新建分類的 ID
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO category (name) VALUES (?)',
            (name,)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update(category_id, name):
    """
    更新分類名稱。

    參數:
        category_id (int): 分類 ID
        name (str): 新的分類名稱
    """
    conn = get_connection()
    try:
        conn.execute(
            'UPDATE category SET name = ? WHERE id = ?',
            (name, category_id)
        )
        conn.commit()
    finally:
        conn.close()


def delete(category_id):
    """
    刪除一個分類。

    參數:
        category_id (int): 分類 ID
    """
    conn = get_connection()
    try:
        conn.execute(
            'DELETE FROM category WHERE id = ?',
            (category_id,)
        )
        conn.commit()
    finally:
        conn.close()
