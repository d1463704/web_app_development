"""
recipe.py — 食譜路由（Controller）

定義食譜相關的所有路由，包含列表、新增、詳情、編輯、刪除與搜尋。
使用 Flask Blueprint 組織路由。
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort

bp = Blueprint('recipe', __name__)


# =============================================
# 首頁（食譜列表）
# =============================================

@bp.route('/')
def index():
    """
    首頁 — 顯示所有食譜列表。

    查詢參數:
        category_id (int, optional): 篩選指定分類的食譜

    渲染模板: index.html
    傳入變數: recipes, categories, current_category
    """
    # TODO: 實作邏輯
    pass


# =============================================
# 新增食譜
# =============================================

@bp.route('/recipes/new')
def new():
    """
    新增食譜頁面 — 顯示空白表單。

    渲染模板: recipe_form.html
    傳入變數: categories, recipe=None
    """
    # TODO: 實作邏輯
    pass


@bp.route('/recipes', methods=['POST'])
def create():
    """
    建立食譜 — 接收表單資料並存入資料庫。

    表單欄位:
        title (str): 食譜名稱（必填）
        description (str): 食譜簡介
        steps (str): 製作步驟（必填）
        category_id (int): 分類 ID
        ingredient_name[] (list): 材料名稱（至少一項）
        ingredient_amount[] (list): 材料用量
        tags (str): 標籤（逗號分隔）

    成功: 重導向到 /recipes/<id>
    失敗: 重新渲染表單並顯示錯誤
    """
    # TODO: 實作邏輯
    pass


# =============================================
# 食譜詳情
# =============================================

@bp.route('/recipes/<int:id>')
def detail(id):
    """
    食譜詳情頁 — 顯示單道食譜的完整內容。

    URL 參數:
        id (int): 食譜 ID

    渲染模板: recipe_detail.html
    傳入變數: recipe

    錯誤處理: 食譜不存在時回傳 404
    """
    # TODO: 實作邏輯
    pass


# =============================================
# 編輯食譜
# =============================================

@bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    編輯食譜頁面 — 顯示預填現有資料的表單。

    URL 參數:
        id (int): 食譜 ID

    渲染模板: recipe_form.html
    傳入變數: recipe, categories

    錯誤處理: 食譜不存在時回傳 404
    """
    # TODO: 實作邏輯
    pass


@bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """
    更新食譜 — 接收修改後的表單資料並更新資料庫。

    URL 參數:
        id (int): 食譜 ID

    表單欄位: 同建立食譜

    成功: 重導向到 /recipes/<id>
    失敗: 重新渲染表單並顯示錯誤

    錯誤處理: 食譜不存在時回傳 404
    """
    # TODO: 實作邏輯
    pass


# =============================================
# 刪除食譜
# =============================================

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜 — 刪除指定食譜並重導向到首頁。

    URL 參數:
        id (int): 食譜 ID

    成功: 重導向到 /
    錯誤處理: 食譜不存在時回傳 404
    """
    # TODO: 實作邏輯
    pass


# =============================================
# 搜尋食譜
# =============================================

@bp.route('/recipes/search')
def search():
    """
    搜尋食譜 — 根據食材關鍵字搜尋。

    查詢參數:
        q (str): 食材關鍵字（以逗號或空白分隔）

    渲染模板: search.html
    傳入變數: recipes, query
    """
    # TODO: 實作邏輯
    pass
