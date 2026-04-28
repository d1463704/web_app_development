from app import db
from datetime import datetime

class Budget(db.Model):
    """
    預算模型 (Budget Model)
    負責管理每個分類在特定週期的預算。
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(7), nullable=False) # YYYY-MM
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Budget {self.period} Category:{self.category_id} Amount:{self.amount}>'

    @classmethod
    def create(cls, category_id, amount, period):
        """建立預算"""
        try:
            budget = cls(category_id=category_id, amount=amount, period=period)
            db.session.add(budget)
            db.session.commit()
            return budget
        except Exception as e:
            db.session.rollback()
            print(f"Error creating budget: {e}")
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
        """取得特定分類與週期的預算"""
        return cls.query.filter_by(category_id=category_id, period=period).first()

    def update(self, amount=None, period=None):
        """更新預算"""
        try:
            if amount is not None:
                self.amount = amount
            if period:
                self.period = period
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating budget: {e}")
            return None

    def delete(self):
        """刪除預算"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting budget: {e}")
            return False
