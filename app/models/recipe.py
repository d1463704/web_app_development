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
