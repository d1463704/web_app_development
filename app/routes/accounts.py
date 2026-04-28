from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Account

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts')
def index():
    """
    帳戶列表頁
    """
    pass

@accounts_bp.route('/accounts/new')
def new():
    """
    顯示新增帳戶表單
    """
    pass

@accounts_bp.route('/accounts', methods=['POST'])
def create():
    """
    建立新帳戶
    """
    pass

@accounts_bp.route('/accounts/<int:id>/edit')
def edit(id):
    """
    顯示編輯帳戶表單
    """
    pass

@accounts_bp.route('/accounts/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新帳戶資訊
    """
    pass
