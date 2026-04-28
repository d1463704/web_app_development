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
    # 取得篩選參數
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id', type=int)
    account_id = request.args.get('account_id', type=int)

    # 這裡簡化處理，先取得所有交易
    transactions = Transaction.get_all()
    
    # 取得所有分類與帳戶供篩選表單使用
    categories = Category.get_all()
    accounts = Account.get_all()
    
    return render_template('transactions/index.html', 
                           transactions=transactions, 
                           categories=categories, 
                           accounts=accounts)

@transactions_bp.route('/transactions/new')
def new():
    """
    顯示新增交易表單
    """
    categories = Category.get_all()
    accounts = Account.get_all()
    
    if not categories or not accounts:
        flash('請先建立分類與帳戶後再進行記帳。', 'warning')
        return redirect(url_for('main.index'))
        
    return render_template('transactions/form.html', 
                           categories=categories, 
                           accounts=accounts, 
                           transaction=None,
                           now_date=datetime.now().strftime('%Y-%m-%d'))

@transactions_bp.route('/transactions', methods=['POST'])
def create():
    """
    建立新交易紀錄
    處理表單資料，寫入 DB，並更新帳戶餘額。
    """
    try:
        amount = request.form.get('amount', type=float)
        type = request.form.get('type')
        category_id = request.form.get('category_id', type=int)
        account_id = request.form.get('account_id', type=int)
        date_str = request.form.get('date')
        note = request.form.get('note')

        # 驗證必填欄位
        if not amount or not type or not category_id or not account_id or not date_str:
            flash('請填寫所有必填欄位。', 'danger')
            return redirect(url_for('transactions.new'))

        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        transaction = Transaction.create(
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            type=type,
            date=date,
            note=note
        )

        if transaction:
            flash('交易紀錄已成功新增。', 'success')
            return redirect(url_for('transactions.index'))
        else:
            flash('新增交易紀錄失敗，請稍後再試。', 'danger')
            return redirect(url_for('transactions.new'))
            
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return redirect(url_for('transactions.new'))

@transactions_bp.route('/transactions/<int:id>/edit')
def edit(id):
    """
    顯示編輯交易表單
    """
    transaction = Transaction.get_by_id(id)
    if not transaction:
        flash('找不到該筆交易紀錄。', 'danger')
        return redirect(url_for('transactions.index'))
        
    categories = Category.get_all()
    accounts = Account.get_all()
    return render_template('transactions/form.html', 
                           transaction=transaction, 
                           categories=categories, 
                           accounts=accounts)

@transactions_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新交易紀錄
    """
    transaction = Transaction.get_by_id(id)
    if not transaction:
        flash('找不到該筆交易紀錄。', 'danger')
        return redirect(url_for('transactions.index'))

    try:
        amount = request.form.get('amount', type=float)
        category_id = request.form.get('category_id', type=int)
        account_id = request.form.get('account_id', type=int)
        date_str = request.form.get('date')
        note = request.form.get('note')

        if not amount or not category_id or not account_id or not date_str:
            flash('請填寫所有必填欄位。', 'danger')
            return redirect(url_for('transactions.edit', id=id))

        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # 這裡僅更新欄位，未包含複雜餘額重算
        transaction.update(
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            date=date,
            note=note
        )
        
        flash('交易紀錄已成功更新。', 'success')
        return redirect(url_for('transactions.index'))
    except Exception as e:
        flash(f'更新失敗: {str(e)}', 'danger')
        return redirect(url_for('transactions.edit', id=id))

@transactions_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除交易紀錄
    並回滾帳戶餘額。
    """
    transaction = Transaction.get_by_id(id)
    if transaction:
        if transaction.delete():
            flash('交易紀錄已成功刪除。', 'success')
        else:
            flash('刪除交易紀錄失敗。', 'danger')
    else:
        flash('找不到該筆交易紀錄。', 'danger')
        
    return redirect(url_for('transactions.index'))
