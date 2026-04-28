"""
tag.py — 標籤 Model

提供標籤（tag）資料表與食譜—標籤關聯表（recipe_tag）的操作。
"""

import sqlite3
from app.models.database import get_db_connection


def get_all():
    """
    取得所有標籤。

    回傳:
        list[sqlite3.Row]: 標籤列表，失敗時回傳空列表
    """
    conn = get_db_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM tag ORDER BY name'
        ).fetchall()
        return rows
    except sqlite3.Error as e:
        print(f'[標籤 Model 錯誤] 取得標籤列表失敗: {e}')
        return []
    finally:
        conn.close()


def get_by_id(tag_id):
    """
    根據 ID 取得單一標籤。

    參數:
        tag_id (int): 標籤 ID

    回傳:
        sqlite3.Row: 標籤資料，找不到或失敗時回傳 None
    """
    conn = get_db_connection()
    try:
        row = conn.execute(
            'SELECT * FROM tag WHERE id = ?',
            (tag_id,)
        ).fetchone()
        return row
    except sqlite3.Error as e:
        print(f'[標籤 Model 錯誤] 取得標籤 (ID={tag_id}) 失敗: {e}')
        return None
    finally:
        conn.close()


def create(data):
    """
    新增一個標籤。

    參數:
        data (dict): 包含 name

    回傳:
        int: 新建標籤的 ID，失敗時回傳 None
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO tag (name) VALUES (?)',
            (data['name'],)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[標籤 Model 錯誤] 新增標籤失敗: {e}')
        return None
    finally:
        conn.close()


def get_or_create(name):
    """
    取得或新增標籤（若已存在則回傳現有的 ID）。

    參數:
        name (str): 標籤名稱

    回傳:
        int: 標籤 ID，失敗時回傳 None
    """
    conn = get_db_connection()
    try:
        row = conn.execute(
            'SELECT id FROM tag WHERE name = ?',
            (name,)
        ).fetchone()

        if row:
            return row['id']

        cursor = conn.execute(
            'INSERT INTO tag (name) VALUES (?)',
            (name,)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[標籤 Model 錯誤] 取得或新增標籤 "{name}" 失敗: {e}')
        return None
    finally:
        conn.close()


def update(tag_id, data):
    """
    更新標籤名稱。

    參數:
        tag_id (int): 標籤 ID
        data (dict): 包含 name

    回傳:
        bool: 更新成功回傳 True，失敗回傳 False
    """
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE tag SET name = ? WHERE id = ?',
            (data['name'], tag_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[標籤 Model 錯誤] 更新標籤 (ID={tag_id}) 失敗: {e}')
        return False
    finally:
        conn.close()


def delete(tag_id):
    """
    刪除一個標籤。

    參數:
        tag_id (int): 標籤 ID

    回傳:
        bool: 刪除成功回傳 True，失敗回傳 False
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tag WHERE id = ?', (tag_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[標籤 Model 錯誤] 刪除標籤 (ID={tag_id}) 失敗: {e}')
        return False
    finally:
        conn.close()


# =============================================
# 食譜—標籤關聯操作
# =============================================

def set_recipe_tags(recipe_id, tag_ids):
    """
    設定一道食譜的標籤（先清除再重新建立）。

    參數:
        recipe_id (int): 食譜 ID
        tag_ids (list[int]): 標籤 ID 列表

    回傳:
        bool: 設定成功回傳 True，失敗回傳 False
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM recipe_tag WHERE recipe_id = ?', (recipe_id,))
        for tag_id in tag_ids:
            conn.execute(
                'INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)',
                (recipe_id, tag_id)
            )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'[標籤 Model 錯誤] 設定食譜標籤 (recipe_id={recipe_id}) 失敗: {e}')
        return False
    finally:
        conn.close()


def get_tags_by_recipe(recipe_id):
    """
    取得一道食譜的所有標籤。

    參數:
        recipe_id (int): 食譜 ID

    回傳:
        list[sqlite3.Row]: 標籤列表，失敗時回傳空列表
    """
    conn = get_db_connection()
    try:
        rows = conn.execute(
            '''SELECT t.* FROM tag t
               JOIN recipe_tag rt ON t.id = rt.tag_id
               WHERE rt.recipe_id = ?
               ORDER BY t.name''',
            (recipe_id,)
        ).fetchall()
        return rows
    except sqlite3.Error as e:
        print(f'[標籤 Model 錯誤] 取得食譜標籤 (recipe_id={recipe_id}) 失敗: {e}')
        return []
    finally:
        conn.close()
