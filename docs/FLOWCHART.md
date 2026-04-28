# FLOWCHART - 個人記帳簿系統

本文件使用 Mermaid 語法呈現兩張圖：**使用者流程圖** 與 **系統序列圖**，以及 **功能清單對照表**，說明系統的操作與資料流向。

---

## 1️⃣ 使用者流程圖（User Flow）

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 進入記帳系統]
    B --> C{要執行什麼操作？}
    C -->|記帳| D[新增支出/收入表單]
    D --> E[提交表單]
    E --> F[記帳成功提示]
    C -->|檢視| G[瀏覽收支列表]
    G --> H[可篩選/搜尋]
    C -->|編輯| I[編輯既有交易]
    I --> J[提交編輯]
    J --> K[編輯成功提示]
    C -->|刪除| L[刪除交易]
    L --> M[刪除成功提示]
    C -->|匯出| N[匯出 CSV/Excel]
    N --> O[下載檔案]
```

---

## 2️⃣ 系統序列圖（Sequence Diagram）

```mermaid
sequenceDiagram
    participant User as 使用者
    participant Browser
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 開啟網站
    Browser->>Flask: GET /
    Flask->>Model: 讀取帳務資料
    Model->>DB: SELECT *
    DB-->>Model: 資料列回傳
    Model-->>Flask: 傳回資料
    Flask-->>Browser: 渲染 templates/ledger.html

    User->>Browser: 點擊「新增」送出表單
    Browser->>Flask: POST /expense
    Flask->>Model: 建立 Expense 實例
    Model->>DB: INSERT INTO expense …
    DB-->>Model: 成功回傳
    Model-->>Flask: commit 完成
    Flask-->>Browser: 重導向回首頁
```

---

## 3️⃣ 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 記帳 | `/expense/add` | POST | 新增支出或收入項目 |
| 檢視列表 | `/` (首頁) | GET | 顯示所有帳務記錄，提供篩選、搜尋 |
| 編輯 | `/expense/edit/<id>` | POST | 更新既有交易資料 |
| 刪除 | `/expense/delete/<id>` | POST | 移除指定交易 |
| 匯出資料 | `/export` | GET | 產生 CSV/Excel 檔下載 |
