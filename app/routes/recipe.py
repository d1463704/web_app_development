"""
recipe.py — 食譜路由（Controller）

定義食譜相關的所有路由，包含列表、新增、詳情、編輯、刪除與搜尋。
使用 Flask Blueprint 組織路由。
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from app.models import recipe, category, tag

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
    category_id = request.args.get('category_id', type=int)
    
    if category_id:
        recipes_list = recipe.get_by_category(category_id)
        current_cat = category.get_by_id(category_id)
    else:
        recipes_list = recipe.get_all()
        current_cat = None
        
    categories_list = category.get_all()
    
    return render_template(
        'index.html', 
        recipes=recipes_list, 
        categories=categories_list, 
        current_category=current_cat
    )


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
    categories_list = category.get_all()
    return render_template('recipe_form.html', categories=categories_list, recipe=None)


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
    title = request.form.get('title')
    description = request.form.get('description')
    steps = request.form.get('steps')
    category_id = request.form.get('category_id', type=int)
    
    # 取得材料列表
    ing_names = request.form.getlist('ingredient_name[]')
    ing_amounts = request.form.getlist('ingredient_amount[]')
    
    # 取得標籤
    tags_str = request.form.get('tags', '')
    
    # 基本驗證
    errors = []
    if not title:
        errors.append('請輸入食譜名稱')
    if not steps:
        errors.append('請輸入製作步驟')
    
    # 過濾空白材料
    ingredients = []
    for name, amount in zip(ing_names, ing_amounts):
        if name.strip():
            ingredients.append({'name': name.strip(), 'amount': amount.strip()})
            
    if not ingredients:
        errors.append('請至少輸入一項材料')
        
    if errors:
        for error in errors:
            flash(error, 'error')
        categories_list = category.get_all()
        return render_template('recipe_form.html', categories=categories_list, recipe=None)

    # 呼叫 Model 新增
    data = {
        'title': title,
        'description': description,
        'steps': steps,
        'category_id': category_id,
        'ingredients': ingredients
    }
    
    recipe_id = recipe.create(data)
    
    if recipe_id:
        # 處理標籤
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            tag_ids = []
            for t_name in tag_names:
                t_id = tag.get_or_create(t_name)
                if t_id:
                    tag_ids.append(t_id)
            tag.set_recipe_tags(recipe_id, tag_ids)
            
        flash('食譜建立成功！', 'success')
        return redirect(url_for('recipe.detail', id=recipe_id))
    else:
        flash('資料庫寫入失敗，請稍後再試', 'error')
        categories_list = category.get_all()
        return render_template('recipe_form.html', categories=categories_list, recipe=None)


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
    recipe_data = recipe.get_by_id(id)
    if not recipe_data:
        abort(404)
        
    return render_template('recipe_detail.html', recipe=recipe_data)


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
    recipe_data = recipe.get_by_id(id)
    if not recipe_data:
        abort(404)
        
    categories_list = category.get_all()
    return render_template('recipe_form.html', recipe=recipe_data, categories=categories_list)


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
    recipe_data = recipe.get_by_id(id)
    if not recipe_data:
        abort(404)
        
    title = request.form.get('title')
    description = request.form.get('description')
    steps = request.form.get('steps')
    category_id = request.form.get('category_id', type=int)
    
    # 取得材料列表
    ing_names = request.form.getlist('ingredient_name[]')
    ing_amounts = request.form.getlist('ingredient_amount[]')
    
    # 取得標籤
    tags_str = request.form.get('tags', '')
    
    # 基本驗證
    errors = []
    if not title:
        errors.append('請輸入食譜名稱')
    if not steps:
        errors.append('請輸入製作步驟')
    
    # 過濾空白材料
    ingredients = []
    for name, amount in zip(ing_names, ing_amounts):
        if name.strip():
            ingredients.append({'name': name.strip(), 'amount': amount.strip()})
            
    if not ingredients:
        errors.append('請至少輸入一項材料')
        
    if errors:
        for error in errors:
            flash(error, 'error')
        categories_list = category.get_all()
        # 為了讓表單能顯示原本輸入的資料，我們需要把 form 資料塞進一個偽裝的 recipe 物件
        temp_recipe = {
            'id': id,
            'title': title,
            'description': description,
            'steps': steps,
            'category_id': category_id,
            'ingredients': ingredients,
            'tags': [{'name': t.strip()} for t in tags_str.split(',') if t.strip()]
        }
        return render_template('recipe_form.html', recipe=temp_recipe, categories=categories_list)

    # 呼叫 Model 更新
    data = {
        'title': title,
        'description': description,
        'steps': steps,
        'category_id': category_id,
        'ingredients': ingredients
    }
    
    success = recipe.update(id, data)
    
    if success:
        # 處理標籤
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        tag_ids = []
        for t_name in tag_names:
            t_id = tag.get_or_create(t_name)
            if t_id:
                tag_ids.append(t_id)
        tag.set_recipe_tags(id, tag_ids)
            
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipe.detail', id=id))
    else:
        flash('資料庫更新失敗，請稍後再試', 'error')
        categories_list = category.get_all()
        return render_template('recipe_form.html', recipe=recipe_data, categories=categories_list)


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
    recipe_data = recipe.get_by_id(id)
    if not recipe_data:
        abort(404)
        
    success = recipe.delete(id)
    if success:
        flash('食譜已刪除', 'success')
    else:
        flash('刪除失敗，請稍後再試', 'error')
        
    return redirect(url_for('recipe.index'))


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
    query = request.args.get('q', '')
    recipes_list = []
    
    if query:
        # 將逗號、空白、分號都視為分隔符
        import re
        keywords = re.split(r'[,\s;]+', query)
        keywords = [k.strip() for k in keywords if k.strip()]
        if keywords:
            recipes_list = recipe.search_by_ingredients(keywords)
            
    return render_template('search.html', recipes=recipes_list, query=query)
