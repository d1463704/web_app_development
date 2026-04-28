from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Budget, Category, Transaction
from app import db
from datetime import datetime

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/budgets')
def index():
    """
    預算管理頁面
    顯示各分類的預算進度 (當月)。
    """
    now = datetime.now()
    period = now.strftime('%Y-%m')
    
    categories = Category.query.filter_by(type='expense').all()
    budgets_data = []
    
    for cat in categories:
        budget = Budget.get_by_category_and_period(cat.id, period)
        
        # 計算該分類當月支出
        actual_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.category_id == cat.id,
            Transaction.type == 'expense',
            Transaction.date >= datetime(now.year, now.month, 1)
        ).scalar() or 0.0
        
        budgets_data.append({
            'category': cat,
            'budget_amount': budget.amount if budget else 0.0,
            'actual_expense': actual_expense,
            'remaining': (budget.amount - actual_expense) if budget else -actual_expense
        })
        
    return render_template('budgets/index.html', budgets_data=budgets_data, period=period)

@budgets_bp.route('/budgets', methods=['POST'])
def update():
    """
    更新或設定預算
    """
    category_id = request.form.get('category_id', type=int)
    amount = request.form.get('amount', type=float)
    period = request.form.get('period') # YYYY-MM

    if not category_id or amount is None or not period:
        flash('請填寫完整預算資訊。', 'danger')
        return redirect(url_for('budgets.index'))

    budget = Budget.get_by_category_and_period(category_id, period)
    if budget:
        budget.update(amount=amount)
        flash('預算已更新。', 'success')
    else:
        Budget.create(category_id=category_id, amount=amount, period=period)
        flash('預算已設定。', 'success')
        
    return redirect(url_for('budgets.index'))
