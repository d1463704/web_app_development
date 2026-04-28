from app import db


class Step(db.Model):
    __tablename__ = 'steps'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id    = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    order_no     = db.Column(db.Integer, nullable=False)
    instruction  = db.Column(db.Text, nullable=False)
    wait_minutes = db.Column(db.Integer, default=0)  # 0 表示此步驟不需要等待

    def __repr__(self):
        return f'<Step {self.order_no}: wait={self.wait_minutes}min>'
