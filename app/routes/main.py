from flask import Blueprint, render_template, send_file
from app.models import Transaction, Account, Budget
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    儀表板首頁
    顯示收支總覽、最近 5 筆交易與當月預算進度。
    """
    pass

@main_bp.route('/export/csv')
def export_csv():
    """
    匯出交易紀錄為 CSV 檔案
    """
    pass
