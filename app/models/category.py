from app import db
from datetime import datetime

class Category(db.Model):
    """
    分類模型 (Category Model)
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False) # income / expense
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯: 一個分類可以有多個交易
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    # 關聯: 一個分類可以有多個預算
    budgets = db.relationship('Budget', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'

    @classmethod
    def create(cls, name, type):
        category = cls(name=name, type=type)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, category_id):
        return cls.query.get(category_id)

    def update(self, name=None, type=None):
        if name:
            self.name = name
        if type:
            self.type = type
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
