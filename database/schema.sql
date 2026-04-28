-- =============================================
-- 食譜收藏夾 — SQLite 資料庫建表語法
-- =============================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- ----- 分類表 -----
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- ----- 食譜表 -----
CREATE TABLE IF NOT EXISTS recipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    steps TEXT NOT NULL,
    cover_image TEXT,
    category_id INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL
);

-- ----- 材料表 -----
CREATE TABLE IF NOT EXISTS ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE
);

-- ----- 標籤表 -----
CREATE TABLE IF NOT EXISTS tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- ----- 食譜—標籤關聯表 -----
CREATE TABLE IF NOT EXISTS recipe_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
    UNIQUE (recipe_id, tag_id)
);

-- ----- 預設分類資料 -----
INSERT OR IGNORE INTO category (name) VALUES ('中式');
INSERT OR IGNORE INTO category (name) VALUES ('西式');
INSERT OR IGNORE INTO category (name) VALUES ('日式');
INSERT OR IGNORE INTO category (name) VALUES ('韓式');
INSERT OR IGNORE INTO category (name) VALUES ('甜點');
INSERT OR IGNORE INTO category (name) VALUES ('飲品');
INSERT OR IGNORE INTO category (name) VALUES ('快速料理');
INSERT OR IGNORE INTO category (name) VALUES ('其他');
