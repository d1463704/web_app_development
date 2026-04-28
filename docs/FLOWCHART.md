# 流程圖文件 — 食譜收藏夾

本文件根據 [PRD](./PRD.md) 與 [ARCHITECTURE](./ARCHITECTURE.md)，以 Mermaid 語法呈現使用者操作流程與系統內部資料流。

---

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站到完成各項操作的完整路徑：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]

    B --> C{要執行什麼操作？}

    %% 新增食譜
    C -->|新增食譜| D[點擊「新增食譜」按鈕]
    D --> E[填寫食譜表單<br>名稱 / 材料 / 步驟 / 分類]
    E --> F{表單是否填寫完整？}
    F -->|否| E
    F -->|是| G[送出表單]
    G --> B

    %% 查看食譜
    C -->|查看食譜| H[點擊食譜名稱]
    H --> I[食譜詳情頁<br>材料清單 + 製作步驟]
    I --> J{接下來要做什麼？}
    J -->|返回列表| B
    J -->|編輯| K[點擊「編輯」按鈕]
    J -->|刪除| N[點擊「刪除」按鈕]

    %% 編輯食譜
    K --> L[修改食譜表單<br>預填現有內容]
    L --> M[送出修改]
    M --> I

    %% 刪除食譜
    N --> O{確認刪除？}
    O -->|取消| I
    O -->|確認| P[刪除食譜]
    P --> B

    %% 搜尋食譜
    C -->|搜尋食譜| Q[輸入食材關鍵字]
    Q --> R[顯示搜尋結果列表]
    R --> S{找到想要的食譜？}
    S -->|是| H
    S -->|否，重新搜尋| Q
    S -->|返回首頁| B
```

### 流程說明

- **新增食譜**：使用者從首頁點擊「新增食譜」→ 填寫表單 → 送出後回到首頁。
- **查看食譜**：使用者在首頁點擊食譜名稱 → 進入詳情頁，可查看材料與步驟。
- **編輯食譜**：從詳情頁點擊「編輯」→ 修改表單內容 → 送出後回到詳情頁。
- **刪除食譜**：從詳情頁點擊「刪除」→ 確認後刪除並回到首頁。
- **搜尋食譜**：使用者輸入食材關鍵字 → 系統列出包含該食材的食譜 → 可點擊查看詳情。

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 點擊「新增食譜」
    Browser->>Flask: GET /recipes/new
    Flask-->>Browser: 回傳空白表單頁面

    User->>Browser: 填寫表單並送出
    Browser->>Flask: POST /recipes
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 呼叫新增食譜函式
    Model->>DB: INSERT INTO recipes
    Model->>DB: INSERT INTO ingredients
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳新食譜 ID
    Flask-->>Browser: 重導向到 /recipes/{id}
    Browser->>Flask: GET /recipes/{id}
    Flask->>Model: 查詢食譜詳情
    Model->>DB: SELECT FROM recipes, ingredients, steps
    DB-->>Model: 回傳資料
    Model-->>Flask: 回傳食譜物件
    Flask-->>Browser: 渲染食譜詳情頁
```

### 2.2 根據食材搜尋食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 輸入食材關鍵字並送出
    Browser->>Flask: GET /recipes/search?q=雞肉,洋蔥
    Flask->>Model: 呼叫搜尋函式
    Model->>DB: SELECT FROM recipes<br>WHERE ingredients LIKE '%雞肉%'<br>AND ingredients LIKE '%洋蔥%'
    DB-->>Model: 回傳符合的食譜列表
    Model-->>Flask: 回傳搜尋結果
    Flask-->>Browser: 渲染搜尋結果頁面
    User->>Browser: 點擊某道食譜
    Browser->>Flask: GET /recipes/{id}
    Flask->>Model: 查詢食譜詳情
    Model->>DB: SELECT FROM recipes
    DB-->>Model: 回傳資料
    Model-->>Flask: 回傳食譜物件
    Flask-->>Browser: 渲染食譜詳情頁
```

### 2.3 編輯食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 在詳情頁點擊「編輯」
    Browser->>Flask: GET /recipes/{id}/edit
    Flask->>Model: 查詢現有食譜資料
    Model->>DB: SELECT FROM recipes
    DB-->>Model: 回傳資料
    Model-->>Flask: 回傳食譜物件
    Flask-->>Browser: 渲染預填表單頁面

    User->>Browser: 修改內容並送出
    Browser->>Flask: POST /recipes/{id}/edit
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 呼叫更新函式
    Model->>DB: UPDATE recipes SET ...
    Model->>DB: DELETE + INSERT ingredients
    DB-->>Model: 更新成功
    Model-->>Flask: 回傳成功
    Flask-->>Browser: 重導向到 /recipes/{id}
```

### 2.4 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 在詳情頁點擊「刪除」
    Browser->>Browser: 顯示確認對話框
    User->>Browser: 確認刪除
    Browser->>Flask: POST /recipes/{id}/delete
    Flask->>Model: 呼叫刪除函式
    Model->>DB: DELETE FROM ingredients WHERE recipe_id = {id}
    Model->>DB: DELETE FROM recipes WHERE id = {id}
    DB-->>Model: 刪除成功
    Model-->>Flask: 回傳成功
    Flask-->>Browser: 重導向到 /recipes
```

---

## 3. 功能清單對照表

下表列出每個功能對應的 URL 路徑、HTTP 方法與簡要說明：

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 首頁（食譜列表） | `/` 或 `/recipes` | GET | 顯示所有食譜的列表，支援分類篩選 |
| 新增食譜（表單） | `/recipes/new` | GET | 顯示空白的食譜新增表單 |
| 新增食譜（送出） | `/recipes` | POST | 接收表單資料，建立新食譜並存入資料庫 |
| 食譜詳情 | `/recipes/<id>` | GET | 顯示單一食譜的完整內容（材料、步驟） |
| 編輯食譜（表單） | `/recipes/<id>/edit` | GET | 顯示預填現有資料的編輯表單 |
| 編輯食譜（送出） | `/recipes/<id>/edit` | POST | 接收修改後的資料，更新資料庫 |
| 刪除食譜 | `/recipes/<id>/delete` | POST | 刪除指定食譜及其關聯資料 |
| 搜尋食譜 | `/recipes/search` | GET | 根據食材關鍵字查詢符合的食譜 |
