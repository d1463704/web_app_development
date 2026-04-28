"""
app/__init__.py — Flask 應用程式工廠

使用 Application Factory 模式建立 Flask App，
負責初始化設定、初始化 SQLAlchemy、註冊 Blueprint。
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 建立全域 db 物件（在 models 裡 import 使用）
db = SQLAlchemy()


def create_app():
    """
    建立並設定 Flask 應用程式。

    回傳:
        Flask: 已設定完成的 Flask 應用程式實例
    """
    app = Flask(__name__, instance_relative_config=True)

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 載入設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 建立所有資料表（若不存在）
    with app.app_context():
        from app.models import Recipe, Ingredient, Step  # noqa: F401
        db.create_all()

    # 註冊路由 Blueprint
    from app.routes import recipes_bp
    app.register_blueprint(recipes_bp)

    return app
