from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Account

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/')
def index():
    accounts = Account.get_all()
    return render_template('accounts/index.html', accounts=accounts)

@accounts_bp.route('/new')
def new():
    return render_template('accounts/form.html', account=None)

@accounts_bp.route('/', methods=['POST'])
def create():
    try:
        name = request.form['name']
        balance = float(request.form.get('balance', 0))
        Account.create(name, balance)
        flash('成功新增帳戶！', 'success')
        return redirect(url_for('accounts.index'))
    except Exception as e:
        flash(f'新增失敗：{str(e)}', 'danger')
        return redirect(url_for('accounts.new'))

@accounts_bp.route('/<int:id>/edit')
def edit(id):
    account = Account.get_by_id(id)
    return render_template('accounts/form.html', account=account)

@accounts_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    try:
        account = Account.get_by_id(id)
        if account:
            name = request.form['name']
            balance = float(request.form['balance'])
            account.update(name=name, balance=balance)
            flash('帳戶已更新。', 'success')
        return redirect(url_for('accounts.index'))
    except Exception as e:
        flash(f'更新失敗：{str(e)}', 'danger')
        return redirect(url_for('accounts.edit', id=id))
