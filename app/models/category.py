from app import db
from datetime import datetime

class Category(db.Model):
    """
    分類模型 (Category Model)
    負責管理收支的分類，如飲食、交通、薪資。
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
        """建立新分類"""
        try:
            category = cls(name=name, type=type)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            print(f"Error creating category: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有分類"""
        return cls.query.order_by(cls.type, cls.name).all()

    @classmethod
    def get_by_id(cls, category_id):
        """依 ID 取得分類"""
        return cls.query.get(category_id)

    def update(self, name=None, type=None):
        """更新分類資訊"""
        try:
            if name:
                self.name = name
            if type:
                self.type = type
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating category: {e}")
            return None

    def delete(self):
        """刪除分類"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting category: {e}")
            return False
