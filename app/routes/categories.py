from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories')
def index():
    """
    分類管理頁面
    顯示所有分類並提供快速新增功能。
    """
    pass

@categories_bp.route('/categories', methods=['POST'])
def create():
    """
    新增分類
    """
    pass
