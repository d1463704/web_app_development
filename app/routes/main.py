from flask import Blueprint, render_template, send_file
from app.models import Transaction, Account, Budget, Category
from datetime import datetime
import csv
import io

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    儀表板首頁
    顯示收支總覽、最近 5 筆交易與當月預算進度。
    """
    transactions = Transaction.query.order_by(Transaction.date.desc()).limit(5).all()
    accounts = Account.get_all()
    
    # 計算本月收支
    now = datetime.now()
    current_month_txs = Transaction.query.filter(
        Transaction.date >= datetime(now.year, now.month, 1)
    ).all()
    
    total_income = sum(t.amount for t in current_month_txs if t.type == 'income')
    total_expense = sum(t.amount for t in current_month_txs if t.type == 'expense')
    
    return render_template('index.html', 
                           transactions=transactions, 
                           accounts=accounts,
                           total_income=total_income,
                           total_expense=total_expense)

@main_bp.route('/export/csv')
def export_csv():
    """
    匯出交易紀錄為 CSV 檔案
    """
    transactions = Transaction.get_all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '日期', '類型', '分類', '帳戶', '金額', '備註'])
    
    for tx in transactions:
        writer.writerow([
            tx.id, 
            tx.date.strftime('%Y-%m-%d'), 
            tx.type, 
            tx.category.name if tx.category else 'N/A', 
            tx.account.name if tx.account else 'N/A', 
            tx.amount, 
            tx.note
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv'
    )
