from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Account

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts')
def index():
    """
    帳戶列表頁
    """
    accounts = Account.get_all()
    return render_template('accounts/index.html', accounts=accounts)

@accounts_bp.route('/accounts/new')
def new():
    """
    顯示新增帳戶表單
    """
    return render_template('accounts/form.html', account=None)

@accounts_bp.route('/accounts', methods=['POST'])
def create():
    """
    建立新帳戶
    """
    name = request.form.get('name')
    balance = request.form.get('balance', default=0.0, type=float)

    if not name:
        flash('請填寫帳戶名稱。', 'danger')
        return redirect(url_for('accounts.new'))

    account = Account.create(name=name, balance=balance)
    if account:
        flash(f'帳戶「{name}」已建立。', 'success')
        return redirect(url_for('accounts.index'))
    else:
        flash('建立帳戶失敗。', 'danger')
        return redirect(url_for('accounts.new'))

@accounts_bp.route('/accounts/<int:id>/edit')
def edit(id):
    """
    顯示編輯帳戶表單
    """
    account = Account.get_by_id(id)
    if not account:
        flash('找不到該帳戶。', 'danger')
        return redirect(url_for('accounts.index'))
    return render_template('accounts/form.html', account=account)

@accounts_bp.route('/accounts/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新帳戶資訊
    """
    account = Account.get_by_id(id)
    if not account:
        flash('找不到該帳戶。', 'danger')
        return redirect(url_for('accounts.index'))

    name = request.form.get('name')
    balance = request.form.get('balance', type=float)

    if not name:
        flash('請填寫帳戶名稱。', 'danger')
        return redirect(url_for('accounts.edit', id=id))

    if account.update(name=name, balance=balance):
        flash('帳戶資訊已更新。', 'success')
        return redirect(url_for('accounts.index'))
    else:
        flash('更新失敗。', 'danger')
        return redirect(url_for('accounts.edit', id=id))
