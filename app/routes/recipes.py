from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/')
def index():
    """
    首頁 / 食譜列表。
    - 若 URL 帶有 ?q=<關鍵字>，則過濾食譜名稱包含關鍵字的結果
    - 否則顯示所有食譜（依建立時間倒序）
    輸出：render_template('index.html', recipes=recipes, q=q)
    """
    pass


@recipes_bp.route('/recipes/new')
def new():
    """
    顯示新增食譜表單（空白）。
    輸出：render_template('recipe_form.html', recipe=None, action='new')
    """
    pass


@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """
    接收新增食譜表單並寫入資料庫。
    輸入表單欄位：
      - name（必填）、description、servings、category
      - ingredient_name[]、ingredient_amount[]（各材料）
      - step_instruction[]、step_wait_minutes[]（各步驟）
    驗證通過後：建立 Recipe、Ingredient、Step 並 commit
    輸出：redirect(url_for('recipes.detail', id=new_id))
    失敗：重新渲染表單並顯示錯誤訊息
    """
    pass


@recipes_bp.route('/recipes/<int:id>')
def detail(id):
    """
    食譜詳細頁，顯示材料清單與步驟（含等待時間）。
    輸入：URL 參數 id（整數）
    處理：Recipe.query.get_or_404(id)
    輸出：render_template('recipe_detail.html', recipe=recipe)
    錯誤：id 不存在時自動回傳 404
    """
    pass


@recipes_bp.route('/recipes/<int:id>/edit')
def edit(id):
    """
    顯示編輯食譜表單（預填現有資料）。
    輸入：URL 參數 id（整數）
    處理：Recipe.query.get_or_404(id)
    輸出：render_template('recipe_form.html', recipe=recipe, action='edit')
    錯誤：id 不存在時自動回傳 404
    """
    pass


@recipes_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """
    接收編輯表單並更新資料庫。
    輸入：URL 參數 id + 同 create() 的表單欄位
    處理：
      1. 驗證 name 不為空
      2. 更新 Recipe 欄位
      3. 刪除舊有 Ingredient 與 Step
      4. 重新建立新的 Ingredient 與 Step
      5. db.session.commit()
    輸出：redirect(url_for('recipes.detail', id=id))
    失敗：重新渲染表單並顯示錯誤訊息
    """
    pass


@recipes_bp.route('/recipes/<int:id>/delete')
def delete_confirm(id):
    """
    顯示刪除確認頁面。
    輸入：URL 參數 id（整數）
    處理：Recipe.query.get_or_404(id)
    輸出：render_template('recipe_confirm_delete.html', recipe=recipe)
    錯誤：id 不存在時自動回傳 404
    """
    pass


@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    執行刪除食譜（CASCADE 自動刪除 Ingredient 與 Step）。
    輸入：URL 參數 id（整數）
    處理：
      1. Recipe.query.get_or_404(id)
      2. db.session.delete(recipe)
      3. db.session.commit()
    輸出：redirect(url_for('recipes.index'))
    錯誤：id 不存在時自動回傳 404
    """
    pass
