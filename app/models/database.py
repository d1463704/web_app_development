"""
database.py — 資料庫連線與初始化工具

提供取得資料庫連線、關閉連線、以及初始化資料表的函式。
"""

import sqlite3
import os


def get_db_path():
    """取得資料庫檔案的絕對路徑（存放在 instance/ 資料夾）"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    return os.path.join(instance_dir, 'database.db')


def get_db_connection():
    """
    取得 SQLite 資料庫連線。

    回傳:
        sqlite3.Connection: 資料庫連線物件（啟用外鍵約束，row_factory 設為 sqlite3.Row）

    例外:
        sqlite3.Error: 連線失敗時拋出
    """
    try:
        conn = sqlite3.connect(get_db_path())
        conn.execute('PRAGMA foreign_keys = ON')  # 啟用外鍵約束
        conn.row_factory = sqlite3.Row            # 讓查詢結果可用欄位名稱存取
        return conn
    except sqlite3.Error as e:
        print(f'[資料庫錯誤] 無法建立連線: {e}')
        raise


def init_db():
    """
    初始化資料庫：讀取 database/schema.sql 並執行建表語法。

    此函式會在應用程式首次啟動時呼叫，確保所有資料表都已建立。

    例外:
        FileNotFoundError: schema.sql 找不到時拋出
        sqlite3.Error: SQL 執行失敗時拋出
    """
    schema_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'schema.sql')
    )
    conn = get_db_connection()
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print('[資料庫] 初始化完成')
    except FileNotFoundError:
        print(f'[資料庫錯誤] 找不到 schema 檔案: {schema_path}')
        raise
    except sqlite3.Error as e:
        print(f'[資料庫錯誤] 初始化失敗: {e}')
        raise
    finally:
        conn.close()
