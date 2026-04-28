from flask import Blueprint, render_template, Response, stream_with_context
from app.models import Transaction, Account, Budget, Category
from datetime import datetime
import csv
import io

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    now = datetime.now()
    period = now.strftime('%Y-%m')
    
    # 本月收支統計
    transactions = Transaction.get_all()
    this_month_txs = [tx for tx in transactions if tx.date.strftime('%Y-%m') == period]
    
    total_income = sum(tx.amount for tx in this_month_txs if tx.type == 'income')
    total_expense = sum(tx.amount for tx in this_month_txs if tx.type == 'expense')
    
    # 帳戶列表
    accounts = Account.get_all()
    
    # 最近 5 筆交易
    recent_transactions = transactions[:5]
    
    return render_template('index.html', 
                           total_income=total_income,
                           total_expense=total_expense,
                           accounts=accounts,
                           transactions=recent_transactions)

@main_bp.route('/export/csv')
def export_csv():
    def generate():
        data = io.StringIO()
        writer = csv.writer(data)
        
        # 寫入標題
        writer.writerow(['日期', '類型', '分類', '帳戶', '金額', '備註'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        # 寫入資料
        transactions = Transaction.get_all()
        for tx in transactions:
            writer.writerow([
                tx.date.strftime('%Y-%m-%d'),
                '收入' if tx.type == 'income' else '支出',
                tx.category.name if tx.category else '未分類',
                tx.account.name if tx.account else '未知帳戶',
                tx.amount,
                tx.note or ''
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
            
    response = Response(stream_with_context(generate()), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv')
    return response
