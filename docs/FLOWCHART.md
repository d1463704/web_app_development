# 流程圖文件 - 個人記帳簿系統（學生版）

## 1. 使用者流程圖（User Flow）

描述學生從進入網站到完成各項操作的路徑。

```mermaid
flowchart LR
    A([學生開啟網頁]) --> B[儀表板首頁\n收支概況總覽]

    B --> C{要執行什麼操作？}

    C -->|快速記帳| D[點擊「快速記帳」]
    D --> E[填寫金額、分類、帳戶、日期]
    E --> F{表單填寫完整？}
    F -->|否| E
    F -->|是| G[送出 POST]
    G --> H[(帳戶餘額自動更新\n寫入 SQLite)]
    H --> B

    C -->|查看流水帳| I[瀏覽交易列表\n可依日期／分類篩選]
    I --> J{要執行什麼操作？}
    J -->|編輯| K[載入表單並修改]
    K --> G
    J -->|刪除| L[確認刪除]
    L --> H
    J -->|返回| B

    C -->|預算管理| M[查看各分類預算進度]
    M --> N[點擊「設定預算」]
    N --> O[輸入月度金額並送出]
    O --> H

    C -->|帳戶管理| P[查看帳戶餘額列表]
    P --> Q[新增或編輯帳戶]
    Q --> H

    C -->|匯出資料| R[點擊「匯出 CSV」]
    R --> S[下載交易紀錄 .csv 檔案]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2-1. 新增交易（記帳）

```mermaid
sequenceDiagram
    actor Student as 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    Student->>Browser: 點擊「快速記帳」
    Browser->>Flask: GET /transactions/new
    Flask->>Model: 取得所有帳戶與分類
    Model->>DB: SELECT * FROM account, category
    DB-->>Model: 回傳列表
    Flask-->>Browser: 渲染 transactions/form.html

    Student->>Browser: 填寫金額、分類、帳戶、日期並送出
    Browser->>Flask: POST /transactions
    Flask->>Flask: 驗證表單資料（必填欄位）
    Flask->>Model: Transaction.create(...)
    Model->>DB: INSERT INTO transaction
    Model->>DB: UPDATE account SET balance=...
    DB-->>Model: 寫入成功
    Flask-->>Browser: 302 重導向至 /transactions
    Browser-->>Student: 顯示交易列表（含成功訊息）
```

### 2-2. 查看儀表板

```mermaid
sequenceDiagram
    actor Student as 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    Student->>Browser: 開啟網站首頁
    Browser->>Flask: GET /
    Flask->>Model: 查詢本月交易（總收入/總支出）
    Model->>DB: SELECT SUM(amount) WHERE date >= 本月1日
    DB-->>Model: 回傳統計數據
    Flask->>Model: 查詢所有帳戶餘額
    Model->>DB: SELECT * FROM account
    DB-->>Model: 回傳帳戶列表
    Flask->>Model: 查詢最近 5 筆交易
    Model->>DB: SELECT * ORDER BY date DESC LIMIT 5
    DB-->>Model: 回傳交易紀錄
    Flask-->>Browser: render_template(index.html, ...)
    Browser-->>Student: 顯示儀表板
```

### 2-3. 設定月度預算

```mermaid
sequenceDiagram
    actor Student as 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    Student->>Browser: 進入「預算進度」頁面
    Browser->>Flask: GET /budgets
    Flask->>Model: 查詢支出分類列表與本月預算
    Model->>DB: SELECT category, budget WHERE period=?
    DB-->>Model: 回傳資料
    Flask->>Model: 查詢各分類當月實際支出
    Model->>DB: SELECT SUM(amount) GROUP BY category_id
    DB-->>Model: 回傳金額
    Flask-->>Browser: 渲染預算進度頁（進度條）

    Student->>Browser: 點擊「設定預算」→ 輸入金額
    Browser->>Flask: POST /budgets
    Flask->>Model: Budget.get_by_category_and_period(...)
    Model->>DB: SELECT budget WHERE category_id=? AND period=?
    alt 預算已存在
        Model->>DB: UPDATE budget SET amount=?
    else 首次設定
        Model->>DB: INSERT INTO budget
    end
    DB-->>Model: 完成
    Flask-->>Browser: 302 重導向至 /budgets
    Browser-->>Student: 顯示更新後的進度條
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 對應模板 | 說明 |
|------|----------|-----------|----------|------|
| 儀表板首頁 | `/` | GET | `index.html` | 收支總覽、最近交易、帳戶餘額 |
| 交易列表 | `/transactions` | GET | `transactions/index.html` | 全部交易，支援篩選 |
| 新增交易表單 | `/transactions/new` | GET | `transactions/form.html` | 空白記帳表單 |
| 建立交易 | `/transactions` | POST | — | 寫入 DB 並更新餘額，重導向 |
| 編輯交易表單 | `/transactions/<id>/edit` | GET | `transactions/form.html` | 預填現有資料 |
| 更新交易 | `/transactions/<id>/update` | POST | — | 更新 DB 後重導向 |
| 刪除交易 | `/transactions/<id>/delete` | POST | — | 刪除並回滾餘額，重導向 |
| 帳戶列表 | `/accounts` | GET | `accounts/index.html` | 帳戶名稱與餘額 |
| 新增帳戶 | `/accounts/new` | GET | `accounts/form.html` | 填寫帳戶名稱與初始金額 |
| 建立帳戶 | `/accounts` | POST | — | 寫入 DB，重導向 |
| 分類管理 | `/categories` | GET | `categories/index.html` | 查看＋快速新增分類 |
| 新增分類 | `/categories` | POST | — | 寫入 DB，重導向 |
| 預算進度 | `/budgets` | GET | `budgets/index.html` | 各分類進度條 |
| 設定預算 | `/budgets` | POST | — | 新增或更新預算，重導向 |
| 匯出 CSV | `/export/csv` | GET | — | 下載全部交易紀錄 CSV |
