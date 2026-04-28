from app import db
from datetime import datetime


class Account(db.Model):
    """
    帳戶模型 (Account)
    管理學生的各種資金來源，如現金、銀行帳戶、悠遊卡、行動支付。
    """
    __tablename__ = 'account'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(50), nullable=False)
    balance    = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯：一個帳戶可有多筆交易
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return f'<Account {self.name} (${self.balance:.2f})>'

    # ── CRUD 方法 ─────────────────────────────────────────────────

    @classmethod
    def create(cls, name, balance=0.0):
        """建立新帳戶

        Args:
            name (str): 帳戶名稱
            balance (float): 初始餘額，預設 0.0

        Returns:
            Account | None
        """
        try:
            account = cls(name=name, balance=balance)
            db.session.add(account)
            db.session.commit()
            return account
        except Exception as e:
            db.session.rollback()
            print(f"[Account.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有帳戶（依建立時間倒序）"""
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, account_id):
        """依 ID 取得帳戶

        Args:
            account_id (int): 帳戶 ID

        Returns:
            Account | None
        """
        return cls.query.get(account_id)

    def update(self, name=None, balance=None):
        """更新帳戶名稱或餘額

        Returns:
            Account | None
        """
        try:
            if name is not None:
                self.name = name
            if balance is not None:
                self.balance = balance
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"[Account.update] Error: {e}")
            return None

    def delete(self):
        """刪除帳戶

        Returns:
            bool: 是否成功
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Account.delete] Error: {e}")
            return False
