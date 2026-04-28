from app import db
from datetime import datetime


class Category(db.Model):
    """
    分類模型 (Category)
    管理收入與支出的分類，如餐飲、交通、薪資、獎學金。
    """
    __tablename__ = 'category'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(50), nullable=False)
    type       = db.Column(db.String(10), nullable=False)  # 'income' | 'expense'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯：一個分類可有多筆交易
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    # 關聯：一個分類可有多筆預算
    budgets = db.relationship('Budget', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'

    # ── CRUD 方法 ─────────────────────────────────────────────────

    @classmethod
    def create(cls, name, type):
        """建立新分類

        Args:
            name (str): 分類名稱
            type (str): 'income' 或 'expense'

        Returns:
            Category | None
        """
        try:
            category = cls(name=name, type=type)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            print(f"[Category.create] Error: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有分類（依類型 → 名稱排序）"""
        return cls.query.order_by(cls.type, cls.name).all()

    @classmethod
    def get_by_id(cls, category_id):
        """依 ID 取得分類"""
        return cls.query.get(category_id)

    def update(self, name=None, type=None):
        """更新分類名稱或類型

        Returns:
            Category | None
        """
        try:
            if name is not None:
                self.name = name
            if type is not None:
                self.type = type
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"[Category.update] Error: {e}")
            return None

    def delete(self):
        """刪除分類

        Returns:
            bool: 是否成功
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Category.delete] Error: {e}")
            return False
