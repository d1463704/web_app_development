from app import db
from datetime import datetime


class Transaction(db.Model):
    """
    交易模型 (Transaction)
    記錄每一筆收入或支出，並自動連動更新所屬帳戶的餘額。
    """
    __tablename__ = 'transaction'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id  = db.Column(db.Integer, db.ForeignKey('account.id'),  nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    type        = db.Column(db.String(10), nullable=False)  # 'income' | 'expense'
    note        = db.Column(db.Text)
    date        = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.type} ${self.amount:.2f} on {self.date.date()}>'

    # ── CRUD 方法 ─────────────────────────────────────────────────

    @classmethod
    def create(cls, account_id, category_id, amount, type, date, note=None):
        """建立交易並自動更新帳戶餘額

        Args:
            account_id (int): 帳戶 ID
            category_id (int): 分類 ID
            amount (float): 金額
            type (str): 'income' 或 'expense'
            date (datetime): 交易日期
            note (str, optional): 備註

        Returns:
            Transaction | None
        """
        try:
            transaction = cls(
                account_id=account_id,
                category_id=category_id,
                amount=amount,
                type=type,
                date=date,
                note=note
            )
            db.session.add(transaction)

            # 自動更新帳戶餘額
            from app.models.account import Account
            account = Account.get_by_id(account_id)
            if account:
                if type == 'income':
                    account.balance += amount
                else:
                    account.balance -= amount

            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            print(f"[Transaction.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有交易（依日期倒序）"""
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def get_by_id(cls, transaction_id):
        """依 ID 取得交易"""
        return cls.query.get(transaction_id)

    def update(self, account_id=None, category_id=None,
               amount=None, type=None, date=None, note=None):
        """更新交易欄位（不含餘額重算）

        Returns:
            Transaction | None
        """
        try:
            if account_id  is not None: self.account_id  = account_id
            if category_id is not None: self.category_id = category_id
            if amount      is not None: self.amount       = amount
            if type        is not None: self.type         = type
            if date        is not None: self.date         = date
            if note        is not None: self.note         = note
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"[Transaction.update] Error: {e}")
            return None

    def delete(self):
        """刪除交易並回滾帳戶餘額

        Returns:
            bool: 是否成功
        """
        try:
            from app.models.account import Account
            account = Account.get_by_id(self.account_id)
            if account:
                if self.type == 'income':
                    account.balance -= self.amount
                else:
                    account.balance += self.amount

            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Transaction.delete] Error: {e}")
            return False
