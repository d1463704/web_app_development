from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Budget, Category, Transaction
from app import db
from datetime import datetime

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/')
def index():
    now = datetime.now()
    period = now.strftime('%Y-%m')
    
    categories = Category.query.filter_by(type='expense').all()
    budgets_data = []
    
    for cat in categories:
        budget = Budget.get_by_category_period(cat.id, period)
        # 計算當月實際支出
        actual_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.category_id == cat.id,
            Transaction.type == 'expense',
            db.func.strftime('%Y-%m', Transaction.date) == period
        ).scalar() or 0.0
        
        budgets_data.append({
            'category': cat,
            'budget_amount': budget.amount if budget else 0.0,
            'actual_expense': actual_expense,
            'remaining': (budget.amount - actual_expense) if budget else -actual_expense
        })
        
    return render_template('budgets/index.html', budgets_data=budgets_data, period=period)

@budgets_bp.route('/update', methods=['POST'])
def update():
    try:
        category_id = int(request.form['category_id'])
        amount = float(request.form['amount'])
        period = request.form['period']
        
        budget = Budget.get_by_category_period(category_id, period)
        if budget:
            budget.update(amount)
        else:
            Budget.create(category_id, amount, period)
            
        flash('預算已更新！', 'success')
        return redirect(url_for('budgets.index'))
    except Exception as e:
        flash(f'更新失敗：{str(e)}', 'danger')
        return redirect(url_for('budgets.index'))
