"""
app/__init__.py — Flask 應用程式工廠

使用 Application Factory 模式建立 Flask App，
負責初始化設定、註冊 Blueprint、設定資料庫。
"""

from flask import Flask


def create_app():
    """
    建立並設定 Flask 應用程式。

    回傳:
        Flask: 已設定完成的 Flask 應用程式實例
    """
    app = Flask(__name__)

    # 載入設定
    app.config.from_mapping(
        SECRET_KEY='dev',  # 開發用密鑰，正式環境應更換
    )

    # 初始化資料庫
    from app.models.database import init_db
    with app.app_context():
        init_db()

    # 註冊路由 Blueprint
    from app.routes.recipe import bp as recipe_bp
    app.register_blueprint(recipe_bp)

    return app
