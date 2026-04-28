from app import db
from datetime import datetime

class Account(db.Model):
    """
    帳戶模型 (Account Model)
    負責管理使用者的資金來源，如現金、銀行帳戶、信用卡。
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
        """建立新帳戶"""
        try:
            account = cls(name=name, balance=balance)
            db.session.add(account)
            db.session.commit()
            return account
        except Exception as e:
            db.session.rollback()
            print(f"Error creating account: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有帳戶"""
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, account_id):
        """依 ID 取得帳戶"""
        return cls.query.get(account_id)

    def update(self, name=None, balance=None):
        """更新帳戶資訊"""
        try:
            if name:
                self.name = name
            if balance is not None:
                self.balance = balance
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating account: {e}")
            return None

    def delete(self):
        """刪除帳戶"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting account: {e}")
            return False
