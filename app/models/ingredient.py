from app import db


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name      = db.Column(db.Text, nullable=False)
    amount    = db.Column(db.Text, nullable=True)   # 例如：300g、2 大匙
    order_no  = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Ingredient {self.id}: {self.name} {self.amount}>'

    @classmethod
    def create(cls, data):
        """新增一筆材料記錄"""
        try:
            ingredient = cls(**data)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            print(f"Error creating ingredient: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有材料記錄"""
        try:
            return cls.query.order_by(cls.order_no).all()
        except Exception as e:
            print(f"Error getting all ingredients: {e}")
            return []

    @classmethod
    def get_by_id(cls, ingredient_id):
        """取得單筆材料記錄"""
        try:
            return cls.query.get(ingredient_id)
        except Exception as e:
            print(f"Error getting ingredient by id: {e}")
            return None

    def update(self, data):
        """更新材料記錄"""
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating ingredient: {e}")
            return False

    def delete(self):
        """刪除材料記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting ingredient: {e}")
            return False
