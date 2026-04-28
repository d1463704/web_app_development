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
