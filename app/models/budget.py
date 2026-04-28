from app import db
from datetime import datetime

class Budget(db.Model):
    """
    預算模型 (Budget Model)
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
        budget = cls(category_id=category_id, amount=amount, period=period)
        db.session.add(budget)
        db.session.commit()
        return budget

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, budget_id):
        return cls.query.get(budget_id)

    @classmethod
    def get_by_category_and_period(cls, category_id, period):
        return cls.query.filter_by(category_id=category_id, period=period).first()

    def update(self, amount=None, period=None):
        if amount is not None:
            self.amount = amount
        if period:
            self.period = period
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
