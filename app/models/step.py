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

    @classmethod
    def create(cls, data):
        """新增一筆步驟記錄"""
        try:
            step = cls(**data)
            db.session.add(step)
            db.session.commit()
            return step
        except Exception as e:
            db.session.rollback()
            print(f"Error creating step: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有步驟記錄"""
        try:
            return cls.query.order_by(cls.order_no).all()
        except Exception as e:
            print(f"Error getting all steps: {e}")
            return []

    @classmethod
    def get_by_id(cls, step_id):
        """取得單筆步驟記錄"""
        try:
            return cls.query.get(step_id)
        except Exception as e:
            print(f"Error getting step by id: {e}")
            return None

    def update(self, data):
        """更新步驟記錄"""
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating step: {e}")
            return False

    def delete(self):
        """刪除步驟記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting step: {e}")
            return False
