from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
def index():
    """首頁 / 食譜列表"""
    q = request.args.get('q', '')
    if q:
        recipes = Recipe.query.filter(Recipe.name.contains(q)).order_by(Recipe.created_at.desc()).all()
    else:
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes, q=q)

@recipes_bp.route('/recipes/new')
def new():
    """顯示新增食譜表單"""
    return render_template('recipe_form.html', recipe=None, action='new')

@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """建立食譜"""
    name = request.form.get('name')
    description = request.form.get('description')
    servings = request.form.get('servings', 2, type=int)
    category = request.form.get('category')

    if not name:
        flash('食譜名稱為必填項目', 'error')
        return redirect(url_for('recipes.new'))

    try:
        # 建立 Recipe
        new_recipe = Recipe(name=name, description=description, servings=servings, category=category)
        db.session.add(new_recipe)
        db.session.flush() # 取得 new_recipe.id

        # 處理材料 Ingredients
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        
        for i, ing_name in enumerate(ingredient_names):
            if ing_name.strip():
                amount = ingredient_amounts[i] if i < len(ingredient_amounts) else ''
                ing = Ingredient(recipe_id=new_recipe.id, name=ing_name, amount=amount, order_no=i+1)
                db.session.add(ing)

        # 處理步驟 Steps
        step_instructions = request.form.getlist('step_instruction[]')
        step_waits = request.form.getlist('step_wait_minutes[]')

        for i, instruction in enumerate(step_instructions):
            if instruction.strip():
                wait = step_waits[i] if i < len(step_waits) and step_waits[i].isdigit() else 0
                step = Step(recipe_id=new_recipe.id, instruction=instruction, wait_minutes=int(wait), order_no=i+1)
                db.session.add(step)

        db.session.commit()
        flash('食譜建立成功！', 'success')
        return redirect(url_for('recipes.detail', id=new_recipe.id))
    except Exception as e:
        db.session.rollback()
        flash(f'建立失敗: {str(e)}', 'error')
        return redirect(url_for('recipes.new'))

@recipes_bp.route('/recipes/<int:id>')
def detail(id):
    """食譜詳細頁"""
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe_detail.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/edit')
def edit(id):
    """顯示編輯食譜表單"""
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe_form.html', recipe=recipe, action='edit')

@recipes_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """更新食譜"""
    recipe = Recipe.query.get_or_404(id)
    
    name = request.form.get('name')
    if not name:
        flash('食譜名稱為必填項目', 'error')
        return redirect(url_for('recipes.edit', id=id))

    try:
        recipe.name = name
        recipe.description = request.form.get('description')
        recipe.servings = request.form.get('servings', 2, type=int)
        recipe.category = request.form.get('category')

        # 刪除舊有材料與步驟
        Ingredient.query.filter_by(recipe_id=id).delete()
        Step.query.filter_by(recipe_id=id).delete()

        # 新增更新後的材料
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        
        for i, ing_name in enumerate(ingredient_names):
            if ing_name.strip():
                amount = ingredient_amounts[i] if i < len(ingredient_amounts) else ''
                ing = Ingredient(recipe_id=id, name=ing_name, amount=amount, order_no=i+1)
                db.session.add(ing)

        # 新增更新後的步驟
        step_instructions = request.form.getlist('step_instruction[]')
        step_waits = request.form.getlist('step_wait_minutes[]')

        for i, instruction in enumerate(step_instructions):
            if instruction.strip():
                wait = step_waits[i] if i < len(step_waits) and step_waits[i].isdigit() else 0
                step = Step(recipe_id=id, instruction=instruction, wait_minutes=int(wait), order_no=i+1)
                db.session.add(step)

        db.session.commit()
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.detail', id=id))
    except Exception as e:
        db.session.rollback()
        flash(f'更新失敗: {str(e)}', 'error')
        return redirect(url_for('recipes.edit', id=id))

@recipes_bp.route('/recipes/<int:id>/delete')
def delete_confirm(id):
    """顯示刪除確認頁面"""
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe_confirm_delete.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """執行刪除食譜"""
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash('食譜已刪除', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('recipes.index'))
