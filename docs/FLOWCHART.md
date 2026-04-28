# 流程圖文件 - 食譜收藏夾

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]

    B --> C{要執行什麼操作？}

    C -->|新增食譜| D[點擊「新增食譜」按鈕]
    D --> E[填寫食譜表單\n名稱／簡介／份量]
    E --> F[新增材料清單\n名稱 + 份量]
    F --> G[新增步驟\n說明 + 等待時間]
    G --> H{表單是否填寫完整？}
    H -->|否| E
    H -->|是| I[送出表單 POST]
    I --> J[(儲存至 SQLite)]
    J --> B

    C -->|查看食譜| K[點擊食譜卡片]
    K --> L[食譜詳細頁\n顯示材料 + 步驟 + 等待時間]
    L --> M{要執行什麼操作？}

    M -->|編輯| N[點擊「編輯」按鈕]
    N --> O[載入現有資料至表單]
    O --> P[修改內容後送出 POST]
    P --> J

    M -->|刪除| Q[點擊「刪除」按鈕]
    Q --> R[刪除確認頁面]
    R --> S{確定刪除？}
    S -->|取消| L
    S -->|確定| T[送出 DELETE 請求]
    T --> J

    M -->|返回| B

    C -->|搜尋食譜| U[輸入關鍵字]
    U --> V[顯示篩選後的食譜列表]
    V --> K
```

---

## 2. 系統序列圖（Sequence Diagram）

描述各主要操作的資料流，從使用者點擊到資料庫寫入的完整流程。

### 2-1. 新增食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 點擊「新增食譜」
    Browser->>Flask: GET /recipes/new
    Flask-->>Browser: 回傳空白表單 (recipe_form.html)

    User->>Browser: 填寫名稱、簡介、份量、材料、步驟（含等待時間）並送出
    Browser->>Flask: POST /recipes
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 建立 Recipe 物件
    Model->>DB: INSERT INTO recipes
    Flask->>Model: 建立 Ingredient 物件（多筆）
    Model->>DB: INSERT INTO ingredients
    Flask->>Model: 建立 Step 物件（多筆，含 wait_minutes）
    Model->>DB: INSERT INTO steps
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳新 Recipe ID
    Flask-->>Browser: 重導向至 GET /recipes/<id>
    Browser-->>User: 顯示食譜詳細頁
```

### 2-2. 查看食譜詳細頁

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 點擊食譜卡片
    Browser->>Flask: GET /recipes/<id>
    Flask->>Model: 查詢 Recipe by id
    Model->>DB: SELECT FROM recipes WHERE id=?
    DB-->>Model: 回傳食譜資料
    Flask->>Model: 查詢該食譜的 Ingredient 列表
    Model->>DB: SELECT FROM ingredients WHERE recipe_id=?
    DB-->>Model: 回傳材料列表
    Flask->>Model: 查詢該食譜的 Step 列表（含 wait_minutes）
    Model->>DB: SELECT FROM steps WHERE recipe_id=? ORDER BY order_no
    DB-->>Model: 回傳步驟列表
    Model-->>Flask: 組合完整資料
    Flask-->>Browser: render_template(recipe_detail.html)
    Browser-->>User: 顯示材料清單 + 步驟（含等待時間）
```

### 2-3. 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」
    Browser->>Flask: GET /recipes/<id>/delete
    Flask-->>Browser: 顯示刪除確認頁 (recipe_confirm_delete.html)

    User->>Browser: 點擊「確認刪除」
    Browser->>Flask: POST /recipes/<id>/delete
    Flask->>Model: 刪除該食譜的 Steps
    Model->>DB: DELETE FROM steps WHERE recipe_id=?
    Flask->>Model: 刪除該食譜的 Ingredients
    Model->>DB: DELETE FROM ingredients WHERE recipe_id=?
    Flask->>Model: 刪除 Recipe
    Model->>DB: DELETE FROM recipes WHERE id=?
    DB-->>Model: 刪除成功
    Flask-->>Browser: 重導向至 GET /
    Browser-->>User: 回到首頁食譜列表
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 對應模板 | 說明 |
|------|----------|-----------|----------|------|
| 首頁 / 食譜列表 | `/` | GET | `index.html` | 顯示所有食譜卡片 |
| 食譜詳細頁 | `/recipes/<id>` | GET | `recipe_detail.html` | 顯示材料、步驟與等待時間 |
| 顯示新增表單 | `/recipes/new` | GET | `recipe_form.html` | 空白表單 |
| 送出新增表單 | `/recipes` | POST | — | 寫入資料庫後重導向 |
| 顯示編輯表單 | `/recipes/<id>/edit` | GET | `recipe_form.html` | 預填現有資料的表單 |
| 送出編輯表單 | `/recipes/<id>/edit` | POST | — | 更新資料庫後重導向 |
| 刪除確認頁 | `/recipes/<id>/delete` | GET | `recipe_confirm_delete.html` | 顯示確認訊息 |
| 執行刪除 | `/recipes/<id>/delete` | POST | — | 刪除資料後重導向至首頁 |
| 搜尋食譜 | `/recipes/search?q=` | GET | `index.html` | 依關鍵字篩選食譜 |
