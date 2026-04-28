from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' 或 'expense'
    note = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.type} {self.amount}>'

    @classmethod
    def create(cls, account_id, category_id, amount, type, date, note=None):
        try:
            # 建立交易
            transaction = cls(
                account_id=account_id,
                category_id=category_id,
                amount=amount,
                type=type,
                date=date,
                note=note
            )
            db.session.add(transaction)

            # 連動更新帳戶餘額
            from app.models.account import Account
            account = Account.query.get(account_id)
            if type == 'income':
                account.balance += amount
            else:
                account.balance -= amount

            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_all(cls, filter_args=None):
        query = cls.query
        if filter_args:
            if filter_args.get('start_date'):
                query = query.filter(cls.date >= filter_args['start_date'])
            if filter_args.get('end_date'):
                query = query.filter(cls.date <= filter_args['end_date'])
            if filter_args.get('category_id'):
                query = query.filter(cls.category_id == filter_args['category_id'])
            if filter_args.get('account_id'):
                query = query.filter(cls.account_id == filter_args['account_id'])
        return query.order_by(cls.date.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def delete(self):
        try:
            # 回滾帳戶餘額
            from app.models.account import Account
            account = Account.query.get(self.account_id)
            if self.type == 'income':
                account.balance -= self.amount
            else:
                account.balance += self.amount
                
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
