from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories')
def index():
    """
    分類管理頁面
    顯示所有分類並提供快速新增功能。
    """
    categories = Category.get_all()
    return render_template('categories/index.html', categories=categories)

@categories_bp.route('/categories', methods=['POST'])
def create():
    """
    新增分類
    """
    name = request.form.get('name')
    type = request.form.get('type')

    if not name or not type:
        flash('請填寫分類名稱與類型。', 'danger')
        return redirect(url_for('categories.index'))

    category = Category.create(name=name, type=type)
    if category:
        flash(f'分類「{name}」已新增。', 'success')
    else:
        flash('新增分類失敗。', 'danger')
        
    return redirect(url_for('categories.index'))
