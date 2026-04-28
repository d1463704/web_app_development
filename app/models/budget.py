from app import db
from datetime import datetime


class Budget(db.Model):
    """
    預算模型 (Budget)
    管理每個分類在特定月份（YYYY-MM）的預算金額。
    每個分類每個月只能有一筆預算（UNIQUE constraint）。
    """
    __tablename__ = 'budget'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    period      = db.Column(db.String(7), nullable=False)  # YYYY-MM
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # 確保同分類同週期只有一筆預算
    __table_args__ = (
        db.UniqueConstraint('category_id', 'period', name='uq_budget_category_period'),
    )

    def __repr__(self):
        return f'<Budget {self.period} Category:{self.category_id} ${self.amount:.2f}>'

    # ── CRUD 方法 ─────────────────────────────────────────────────

    @classmethod
    def create(cls, category_id, amount, period):
        """建立新預算

        Args:
            category_id (int): 分類 ID
            amount (float): 預算金額
            period (str): 週期，格式 YYYY-MM

        Returns:
            Budget | None
        """
        try:
            budget = cls(category_id=category_id, amount=amount, period=period)
            db.session.add(budget)
            db.session.commit()
            return budget
        except Exception as e:
            db.session.rollback()
            print(f"[Budget.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有預算"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, budget_id):
        """依 ID 取得預算"""
        return cls.query.get(budget_id)

    @classmethod
    def get_by_category_and_period(cls, category_id, period):
        """取得特定分類與週期的預算

        Args:
            category_id (int): 分類 ID
            period (str): YYYY-MM

        Returns:
            Budget | None
        """
        return cls.query.filter_by(category_id=category_id, period=period).first()

    def update(self, amount=None, period=None):
        """更新預算金額或週期

        Returns:
            Budget | None
        """
        try:
            if amount is not None:
                self.amount = amount
            if period is not None:
                self.period = period
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"[Budget.update] Error: {e}")
            return None

    def delete(self):
        """刪除預算

        Returns:
            bool: 是否成功
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Budget.delete] Error: {e}")
            return False
