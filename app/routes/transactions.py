from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Transaction, Category, Account
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
def index():
    # 獲取篩選參數
    filter_args = {
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
        'category_id': request.args.get('category_id', type=int),
        'account_id': request.args.get('account_id', type=int)
    }
    
    transactions = Transaction.get_all(filter_args)
    categories = Category.get_all()
    accounts = Account.get_all()
    
    return render_template('transactions/index.html', 
                           transactions=transactions, 
                           categories=categories, 
                           accounts=accounts)

@transactions_bp.route('/new')
def new():
    categories = Category.get_all()
    accounts = Account.get_all()
    return render_template('transactions/form.html', 
                           categories=categories, 
                           accounts=accounts, 
                           transaction=None)

@transactions_bp.route('/', methods=['POST'])
def create():
    try:
        amount = float(request.form['amount'])
        type = request.form['type']
        category_id = int(request.form['category_id'])
        account_id = int(request.form['account_id'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        note = request.form.get('note')
        
        Transaction.create(account_id, category_id, amount, type, date, note)
        flash('成功新增交易紀錄！', 'success')
        return redirect(url_for('transactions.index'))
    except Exception as e:
        flash(f'新增失敗：{str(e)}', 'danger')
        return redirect(url_for('transactions.new'))

@transactions_bp.route('/<int:id>/edit')
def edit(id):
    transaction = Transaction.get_by_id(id)
    categories = Category.get_all()
    accounts = Account.get_all()
    return render_template('transactions/form.html', 
                           transaction=transaction, 
                           categories=categories, 
                           accounts=accounts)

@transactions_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    try:
        transaction = Transaction.get_by_id(id)
        if transaction:
            transaction.delete()
            flash('已刪除交易紀錄。', 'success')
        return redirect(url_for('transactions.index'))
    except Exception as e:
        flash(f'刪除失敗：{str(e)}', 'danger')
        return redirect(url_for('transactions.index'))
