"""
recipe.py — 食譜 Model

提供食譜（recipe）資料表的 CRUD 操作，包含材料（ingredient）的關聯處理。
"""

from datetime import datetime
from app.models.database import get_connection


# =============================================
# 食譜 CRUD
# =============================================

def create(title, description, steps, ingredients, category_id=None, cover_image=None):
    """
    新增一道食譜。

    參數:
        title (str): 食譜名稱
        description (str): 食譜簡介
        steps (str): 製作步驟
        ingredients (list[dict]): 材料清單，每項為 {'name': '...', 'amount': '...'}
        category_id (int, optional): 分類 ID
        cover_image (str, optional): 封面圖片檔名

    回傳:
        int: 新建食譜的 ID
    """
    conn = get_connection()
    now = datetime.now().isoformat()
    try:
        cursor = conn.execute(
            '''INSERT INTO recipe (title, description, steps, category_id, cover_image, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (title, description, steps, category_id, cover_image, now, now)
        )
        recipe_id = cursor.lastrowid

        # 新增材料
        for ing in ingredients:
            conn.execute(
                'INSERT INTO ingredient (recipe_id, name, amount) VALUES (?, ?, ?)',
                (recipe_id, ing['name'], ing.get('amount', ''))
            )

        conn.commit()
        return recipe_id
    finally:
        conn.close()


def get_all():
    """
    取得所有食譜列表（含分類名稱）。

    回傳:
        list[sqlite3.Row]: 食譜列表
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            '''SELECT r.*, c.name AS category_name
               FROM recipe r
               LEFT JOIN category c ON r.category_id = c.id
               ORDER BY r.created_at DESC'''
        ).fetchall()
        return rows
    finally:
        conn.close()


def get_by_id(recipe_id):
    """
    根據 ID 取得單一食譜（含材料清單與分類名稱）。

    參數:
        recipe_id (int): 食譜 ID

    回傳:
        dict: 食譜資料（包含 'ingredients' 欄位），找不到時回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            '''SELECT r.*, c.name AS category_name
               FROM recipe r
               LEFT JOIN category c ON r.category_id = c.id
               WHERE r.id = ?''',
            (recipe_id,)
        ).fetchone()

        if row is None:
            return None

        # 轉成 dict 以便加入 ingredients
        recipe = dict(row)

        # 查詢材料
        ingredients = conn.execute(
            'SELECT * FROM ingredient WHERE recipe_id = ? ORDER BY id',
            (recipe_id,)
        ).fetchall()
        recipe['ingredients'] = [dict(ing) for ing in ingredients]

        # 查詢標籤
        tags = conn.execute(
            '''SELECT t.* FROM tag t
               JOIN recipe_tag rt ON t.id = rt.tag_id
               WHERE rt.recipe_id = ?
               ORDER BY t.name''',
            (recipe_id,)
        ).fetchall()
        recipe['tags'] = [dict(tag) for tag in tags]

        return recipe
    finally:
        conn.close()


def update(recipe_id, title, description, steps, ingredients, category_id=None, cover_image=None):
    """
    更新一道食譜。

    參數:
        recipe_id (int): 食譜 ID
        title (str): 食譜名稱
        description (str): 食譜簡介
        steps (str): 製作步驟
        ingredients (list[dict]): 材料清單
        category_id (int, optional): 分類 ID
        cover_image (str, optional): 封面圖片檔名
    """
    conn = get_connection()
    now = datetime.now().isoformat()
    try:
        conn.execute(
            '''UPDATE recipe
               SET title = ?, description = ?, steps = ?, category_id = ?,
                   cover_image = ?, updated_at = ?
               WHERE id = ?''',
            (title, description, steps, category_id, cover_image, now, recipe_id)
        )

        # 刪除舊材料，重新寫入
        conn.execute('DELETE FROM ingredient WHERE recipe_id = ?', (recipe_id,))
        for ing in ingredients:
            conn.execute(
                'INSERT INTO ingredient (recipe_id, name, amount) VALUES (?, ?, ?)',
                (recipe_id, ing['name'], ing.get('amount', ''))
            )

        conn.commit()
    finally:
        conn.close()


def delete(recipe_id):
    """
    刪除一道食譜（材料與標籤關聯會因 ON DELETE CASCADE 自動刪除）。

    參數:
        recipe_id (int): 食譜 ID
    """
    conn = get_connection()
    try:
        conn.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
        conn.commit()
    finally:
        conn.close()


def search_by_ingredients(keywords):
    """
    根據食材關鍵字搜尋食譜。

    參數:
        keywords (list[str]): 食材關鍵字列表

    回傳:
        list[sqlite3.Row]: 符合條件的食譜列表（包含所有關鍵字的食譜）
    """
    if not keywords:
        return []

    conn = get_connection()
    try:
        # 每個關鍵字都必須出現在食譜的材料中
        # 使用子查詢確認每個關鍵字都有對應的材料
        conditions = []
        params = []
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                conditions.append(
                    '''EXISTS (
                        SELECT 1 FROM ingredient
                        WHERE ingredient.recipe_id = r.id
                        AND ingredient.name LIKE ?
                    )'''
                )
                params.append(f'%{keyword}%')

        if not conditions:
            return []

        query = f'''
            SELECT r.*, c.name AS category_name
            FROM recipe r
            LEFT JOIN category c ON r.category_id = c.id
            WHERE {' AND '.join(conditions)}
            ORDER BY r.created_at DESC
        '''

        rows = conn.execute(query, params).fetchall()
        return rows
    finally:
        conn.close()


def get_by_category(category_id):
    """
    根據分類 ID 取得食譜列表。

    參數:
        category_id (int): 分類 ID

    回傳:
        list[sqlite3.Row]: 食譜列表
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            '''SELECT r.*, c.name AS category_name
               FROM recipe r
               LEFT JOIN category c ON r.category_id = c.id
               WHERE r.category_id = ?
               ORDER BY r.created_at DESC''',
            (category_id,)
        ).fetchall()
        return rows
    finally:
        conn.close()
