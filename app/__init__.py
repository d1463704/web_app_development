import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 資料庫設定
    db_path = os.path.join(app.instance_path, 'database.db')
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 初始化外掛
    db.init_app(app)

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.transactions import transactions_bp
    from app.routes.accounts import accounts_bp
    from app.routes.categories import categories_bp
    from app.routes.budgets import budgets_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(budgets_bp, url_prefix='/budgets')

    # 自動建立資料表
    with app.app_context():
        db.create_all()

    return app
