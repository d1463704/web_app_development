from app import db
from datetime import datetime


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    servings    = db.Column(db.Integer, default=2)
    category    = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.now)
    updated_at  = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 關聯：一筆食譜對應多筆材料與步驟
    ingredients = db.relationship('Ingredient', backref='recipe',
                                  cascade='all, delete-orphan', lazy=True,
                                  order_by='Ingredient.order_no')
    steps       = db.relationship('Step', backref='recipe',
                                  cascade='all, delete-orphan', lazy=True,
                                  order_by='Step.order_no')

    def __repr__(self):
        return f'<Recipe {self.id}: {self.name}>'

    @classmethod
    def create(cls, data):
        """新增一筆食譜記錄"""
        try:
            recipe = cls(**data)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有食譜記錄，依建立時間倒序排序"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting all recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """取得單筆食譜記錄"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error getting recipe by id: {e}")
            return None

    def update(self, data):
        """更新食譜記錄"""
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating recipe: {e}")
            return False

    def delete(self):
        """刪除食譜記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting recipe: {e}")
            return False
