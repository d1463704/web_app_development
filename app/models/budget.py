from app import db
from datetime import datetime

class Budget(db.Model):
    __tablename__ = 'budget'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(7), nullable=False) # YYYY-MM
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Budget {self.period} {self.category_id}>'

    @classmethod
    def create(cls, category_id, amount, period):
        try:
            budget = cls(category_id=category_id, amount=amount, period=period)
            db.session.add(budget)
            db.session.commit()
            return budget
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_by_category_period(cls, category_id, period):
        return cls.query.filter_by(category_id=category_id, period=period).first()

    def update(self, amount):
        try:
            self.amount = amount
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
