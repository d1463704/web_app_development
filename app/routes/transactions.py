from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Transaction, Category, Account
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions')
def index():
    """
    交易紀錄列表頁
    支援依日期範圍、分類、帳戶進行篩選。
    """
    pass

@transactions_bp.route('/transactions/new')
def new():
    """
    顯示新增交易表單
    """
    pass

@transactions_bp.route('/transactions', methods=['POST'])
def create():
    """
    建立新交易紀錄
    處理表單資料，寫入 DB，並更新帳戶餘額。
    """
    pass

@transactions_bp.route('/transactions/<int:id>/edit')
def edit(id):
    """
    顯示編輯交易表單
    """
    pass

@transactions_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新交易紀錄
    """
    pass

@transactions_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除交易紀錄
    並回滾帳戶餘額。
    """
    pass
