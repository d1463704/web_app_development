"""
category.py — 分類 Model

提供分類（category）資料表的 CRUD 操作。
"""

import sqlite3
from app.models.database import get_db_connection


def get_all():
    """
    取得所有分類。

    回傳:
        list[sqlite3.Row]: 分類列表，失敗時回傳空列表
    """
    conn = get_db_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM category ORDER BY id'
        ).fetchall()
        return rows
    except sqlite3.Error as e:
        print(f'[分類 Model 錯誤] 取得分類列表失敗: {e}')
        return []
    finally:
        conn.close()


def get_by_id(category_id):
    """
    根據 ID 取得單一分類。

    參數:
        category_id (int): 分類 ID

    回傳:
        sqlite3.Row: 分類資料，找不到或失敗時回傳 None
    """
    conn = get_db_connection()
    try:
        row = conn.execute(
            'SELECT * FROM category WHERE id = ?',
            (category_id,)
        ).fetchone()
        return row
    except sqlite3.Error as e:
        print(f'[分類 Model 錯誤] 取得分類 (ID={category_id}) 失敗: {e}')
        return None
    finally:
        conn.close()


def create(data):
    """
    新增一個分類。

    參數:
        data (dict): 包含 name

    回傳:
        int: 新建分類的 ID，失敗時回傳 None
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO category (name) VALUES (?)',
            (data['name'],)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[分類 Model 錯誤] 新增分類失敗: {e}')
        return None
    finally:
        conn.close()


def update(category_id, data):
    """
    更新分類名稱。

    參數:
        category_id (int): 分類 ID
        data (dict): 包含 name

    回傳:
        bool: 更新成功回傳 True，失敗回傳 False
    """
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE category SET name = ? WHERE id = ?',
            (data['name'], category_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[分類 Model 錯誤] 更新分類 (ID={category_id}) 失敗: {e}')
        return False
    finally:
        conn.close()


def delete(category_id):
    """
    刪除一個分類。

    參數:
        category_id (int): 分類 ID

    回傳:
        bool: 刪除成功回傳 True，失敗回傳 False
    """
    conn = get_db_connection()
    try:
        conn.execute(
            'DELETE FROM category WHERE id = ?',
            (category_id,)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[分類 Model 錯誤] 刪除分類 (ID={category_id}) 失敗: {e}')
        return False
    finally:
        conn.close()
