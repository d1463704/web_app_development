from app import db
from datetime import datetime

class Transaction(db.Model):
    """
    交易模型 (Transaction Model)
    負責記錄每一筆收支，並同步更新帳戶餘額。
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # income / expense
    note = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.type} {self.amount}>'

    @classmethod
    def create(cls, account_id, category_id, amount, type, date, note=None):
        """建立交易並更新帳戶餘額"""
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
            
            # 同步更新帳戶餘額
            from app.models.account import Account
            account = Account.get_by_id(account_id)
            if type == 'income':
                account.balance += amount
            else:
                account.balance -= amount
                
            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            print(f"Error creating transaction: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有交易（依日期倒序）"""
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def get_by_id(cls, transaction_id):
        """依 ID 取得交易"""
        return cls.query.get(transaction_id)

    def update(self, account_id=None, category_id=None, amount=None, type=None, date=None, note=None):
        """更新交易紀錄 (注意：此實作未包含複雜的餘額重算邏輯)"""
        try:
            if account_id: self.account_id = account_id
            if category_id: self.category_id = category_id
            if amount is not None: self.amount = amount
            if type: self.type = type
            if date: self.date = date
            if note: self.note = note
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating transaction: {e}")
            return None

    def delete(self):
        """刪除交易並回滾帳戶餘額"""
        try:
            from app.models.account import Account
            account = Account.get_by_id(self.account_id)
            if self.type == 'income':
                account.balance -= self.amount
            else:
                account.balance += self.amount
                
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting transaction: {e}")
            return False
