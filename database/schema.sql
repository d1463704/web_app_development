-- 個人記帳簿系統 - 資料庫建表語法 (SQLite)
-- 版本：v1.0 | 日期：2026-04-28

-- 帳戶表
CREATE TABLE IF NOT EXISTS account (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    balance    REAL    NOT NULL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 分類表
CREATE TABLE IF NOT EXISTS category (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    type       TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 交易紀錄表
CREATE TABLE IF NOT EXISTS "transaction" (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id  INTEGER  NOT NULL,
    category_id INTEGER  NOT NULL,
    amount      REAL     NOT NULL,
    type        TEXT     NOT NULL CHECK (type IN ('income', 'expense')),
    note        TEXT,
    date        DATETIME NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id)  REFERENCES account  (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
);

-- 預算表
CREATE TABLE IF NOT EXISTS budget (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    amount      REAL    NOT NULL,
    period      TEXT    NOT NULL,  -- 格式: YYYY-MM，例如 2026-04
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category (id),
    UNIQUE (category_id, period)   -- 每個分類每月只能有一筆預算
);
