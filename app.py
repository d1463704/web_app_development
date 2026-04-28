from app import create_app
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # 啟動 Flask 應用程式
    app.run(debug=True)
