# 路由設計文件 - 個人記帳簿系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|----------|-----------|----------|------|
| **儀表板 (首頁)** | GET | `/` | `index.html` | 顯示收支總覽、最近交易與預算進度 |
| **交易列表** | GET | `/transactions` | `transactions/index.html` | 顯示所有交易紀錄，支援篩選 |
| **新增交易頁面** | GET | `/transactions/new` | `transactions/form.html` | 顯示新增交易表單 |
| **建立交易** | POST | `/transactions` | — | 接收表單，寫入 DB，重導向至列表 |
| **編輯交易頁面** | GET | `/transactions/<int:id>/edit` | `transactions/form.html` | 顯示編輯交易表單 |
| **更新交易** | POST | `/transactions/<int:id>/update` | — | 接收表單，更新 DB，重導向 |
| **刪除交易** | POST | `/transactions/<int:id>/delete` | — | 刪除交易，重導向 |
| **帳戶列表** | GET | `/accounts` | `accounts/index.html` | 顯示帳戶列表與餘額 |
| **新增帳戶頁面** | GET | `/accounts/new` | `accounts/form.html` | 顯示新增帳戶表單 |
| **建立帳戶** | POST | `/accounts` | — | 接收表單，建立帳戶 |
| **編輯帳戶頁面** | GET | `/accounts/<int:id>/edit` | `accounts/form.html` | 顯示編輯帳戶表單 |
| **更新帳戶** | POST | `/accounts/<int:id>/update` | — | 接收表單，更新帳戶 |
| **分類管理** | GET | `/categories` | `categories/index.html` | 顯示收支分類列表 |
| **新增分類** | POST | `/categories` | — | 快速新增分類 |
| **預算管理** | GET | `/budgets` | `budgets/index.html` | 顯示各分類預算與目前支出 |
| **設定預算** | POST | `/budgets` | — | 新增或更新某分類的月度預算 |
| **資料匯出** | GET | `/export/csv` | — | 產生並下載交易紀錄 CSV 檔 |

## 2. 每個路由的詳細說明

### 交易相關 (Transactions)
- **GET `/transactions`**:
    - 輸入: `start_date`, `end_date`, `category_id`, `account_id` (Query String)
    - 處理: 呼叫 `Transaction.get_all()` 或篩選方法。
    - 輸出: `transactions/index.html`。
- **POST `/transactions`**:
    - 輸入: `type`, `amount`, `category_id`, `account_id`, `date`, `note` (Form)
    - 處理: 呼叫 `Transaction.create()`。
    - 輸出: 重導向至 `/transactions`。

### 帳戶相關 (Accounts)
- **GET `/accounts`**:
    - 處理: 呼叫 `Account.get_all()`。
    - 輸出: `accounts/index.html`。

### 分類相關 (Categories)
- **GET `/categories`**:
    - 處理: 呼叫 `Category.get_all()`。
    - 輸出: `categories/index.html`。

### 預算相關 (Budgets)
- **GET `/budgets`**:
    - 處理: 取得當月所有分類的預算 (`Budget.get_all()`) 與對應支出的總和。
    - 輸出: `budgets/index.html`。

## 3. Jinja2 模板清單
所有模板皆繼承 `base.html`。

- `base.html`: 導覽列與全局樣式。
- `index.html`: 綜合資訊。
- `transactions/index.html`: 列表頁。
- `transactions/form.html`: 新增/編輯共用表單。
- `accounts/index.html`: 帳戶列表。
- `accounts/form.html`: 帳戶表單。
- `categories/index.html`: 分類管理。
- `budgets/index.html`: 預算進度。

## 4. 路由骨架程式碼
檔案位置：
- `app/routes/main.py`
- `app/routes/transactions.py`
- `app/routes/accounts.py`
- `app/routes/categories.py`
- `app/routes/budgets.py`
