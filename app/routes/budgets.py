from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Budget, Category
from datetime import datetime

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/budgets')
def index():
    """
    預算管理頁面
    顯示各分類的預算進度 (當月)。
    """
    pass

@budgets_bp.route('/budgets', methods=['POST'])
def update():
    """
    更新或設定預算
    """
    pass
