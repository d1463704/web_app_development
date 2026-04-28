from app import db
from datetime import datetime

class Account(db.Model):
    """
    帳戶模型 (Account Model)
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯: 一個帳戶可以有多個交易
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return f'<Account {self.name}>'

    @classmethod
    def create(cls, name, balance=0.0):
        account = cls(name=name, balance=balance)
        db.session.add(account)
        db.session.commit()
        return account

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, account_id):
        return cls.query.get(account_id)

    def update(self, name=None, balance=None):
        if name:
            self.name = name
        if balance is not None:
            self.balance = balance
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
