"""
app.py — 應用程式入口

啟動 Flask 開發伺服器。
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
