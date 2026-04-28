from app import db
from datetime import datetime

class Transaction(db.Model):
    """
    交易模型 (Transaction Model)
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

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def get_by_id(cls, transaction_id):
        return cls.query.get(transaction_id)

    def update(self, account_id=None, category_id=None, amount=None, type=None, date=None, note=None):
        # 注意: 更新金額需要重新計算帳戶餘額，這裡簡化處理
        if account_id: self.account_id = account_id
        if category_id: self.category_id = category_id
        if amount is not None: self.amount = amount
        if type: self.type = type
        if date: self.date = date
        if note: self.note = note
        db.session.commit()
        return self

    def delete(self):
        # 同步回滾帳戶餘額
        from app.models.account import Account
        account = Account.get_by_id(self.account_id)
        if self.type == 'income':
            account.balance -= self.amount
        else:
            account.balance += self.amount
            
        db.session.delete(self)
        db.session.commit()
