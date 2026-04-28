-- 食譜收藏夾 - 資料庫 Schema
-- SQLite 語法

-- 食譜表
CREATE TABLE IF NOT EXISTS recipes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT,
    servings    INTEGER DEFAULT 2,
    category    TEXT,
    created_at  DATETIME DEFAULT (datetime('now', 'localtime')),
    updated_at  DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- 材料表
CREATE TABLE IF NOT EXISTS ingredients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    amount      TEXT,
    order_no    INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- 步驟表（含等待時間）
CREATE TABLE IF NOT EXISTS steps (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id    INTEGER NOT NULL,
    order_no     INTEGER NOT NULL,
    instruction  TEXT    NOT NULL,
    wait_minutes INTEGER DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
