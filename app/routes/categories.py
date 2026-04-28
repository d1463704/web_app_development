from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/')
def index():
    categories = Category.get_all()
    return render_template('categories/index.html', categories=categories)

@categories_bp.route('/', methods=['POST'])
def create():
    try:
        name = request.form['name']
        type = request.form['type']
        Category.create(name, type)
        flash('成功新增分類！', 'success')
        return redirect(url_for('categories.index'))
    except Exception as e:
        flash(f'新增失敗：{str(e)}', 'danger')
        return redirect(url_for('categories.index'))
