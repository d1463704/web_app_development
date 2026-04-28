# 路由設計文件 - 個人記帳簿系統（學生版）

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|----------|-----------|----------|------|
| **儀表板首頁** | GET | `/` | `index.html` | 顯示本月收支統計、最近交易、帳戶餘額 |
| **匯出 CSV** | GET | `/export/csv` | — | 下載全部交易紀錄的 CSV 檔案 |
| **交易列表** | GET | `/transactions` | `transactions/index.html` | 顯示全部交易，支援日期/分類/帳戶篩選 |
| **顯示新增表單** | GET | `/transactions/new` | `transactions/form.html` | 空白記帳表單 |
| **建立交易** | POST | `/transactions` | — | 接收表單，寫入 DB 並更新帳戶餘額，重導向至列表 |
| **顯示編輯表單** | GET | `/transactions/<int:id>/edit` | `transactions/form.html` | 預填現有資料的表單 |
| **更新交易** | POST | `/transactions/<int:id>/update` | — | 接收表單，更新 DB 後重導向 |
| **刪除交易** | POST | `/transactions/<int:id>/delete` | — | 刪除並回滾餘額，重導向至列表 |
| **帳戶列表** | GET | `/accounts` | `accounts/index.html` | 顯示所有帳戶與目前餘額 |
| **顯示新增帳戶表單** | GET | `/accounts/new` | `accounts/form.html` | 空白帳戶表單 |
| **建立帳戶** | POST | `/accounts` | — | 接收表單，建立帳戶 |
| **顯示編輯帳戶表單** | GET | `/accounts/<int:id>/edit` | `accounts/form.html` | 預填現有帳戶資料 |
| **更新帳戶** | POST | `/accounts/<int:id>/update` | — | 更新帳戶名稱/初始餘額 |
| **分類管理** | GET | `/categories` | `categories/index.html` | 顯示所有分類，提供快速新增 |
| **新增分類** | POST | `/categories` | — | 寫入 DB 後重導向 |
| **預算進度** | GET | `/budgets` | `budgets/index.html` | 顯示當月各分類預算進度條 |
| **設定預算** | POST | `/budgets` | — | 新增或更新月度預算，重導向 |

---

## 2. 每個路由的詳細說明

### 儀表板（main.py）

**GET `/`**
- **處理邏輯**：查詢本月收支合計（`SUM`）、所有帳戶、最近 5 筆交易
- **輸出**：`render_template('index.html', total_income, total_expense, accounts, transactions)`

**GET `/export/csv`**
- **處理邏輯**：查詢所有交易，用 `csv` 模組產生位元流
- **輸出**：`send_file(...)` 以 `text/csv` 回傳，觸發下載

---

### 交易（transactions.py）

**GET `/transactions`**
- **輸入（Query String）**：`start_date`, `end_date`, `category_id`, `account_id`
- **處理邏輯**：`Transaction.get_all()` 或依篩選條件查詢
- **輸出**：`render_template('transactions/index.html', transactions, categories, accounts)`

**POST `/transactions`**
- **輸入（Form）**：`amount`, `type`, `category_id`, `account_id`, `date`, `note`
- **驗證**：金額必填且 > 0、type/category_id/account_id/date 必填
- **失敗**：`flash('錯誤訊息', 'danger')` → 重導向 `/transactions/new`
- **成功**：`Transaction.create(...)` → `redirect('/transactions')`

---

### 帳戶（accounts.py）

**POST `/accounts`**
- **輸入（Form）**：`name`, `balance`
- **驗證**：名稱必填
- **成功**：`Account.create(...)` → `redirect('/accounts')`

---

### 分類（categories.py）

**POST `/categories`**
- **輸入（Form）**：`name`, `type`
- **驗證**：名稱與類型均必填
- **成功**：`Category.create(...)` → `redirect('/categories')`

---

### 預算（budgets.py）

**POST `/budgets`**
- **輸入（Form）**：`category_id`, `amount`, `period`
- **處理邏輯**：`Budget.get_by_category_and_period()` → 有則 `update()`，無則 `create()`
- **成功**：`redirect('/budgets')`

---

## 3. Jinja2 模板清單

所有模板皆繼承 `templates/base.html`。

| 模板檔案 | 頁面 | 繼承 |
|---------|------|------|
| `base.html` | 共用版型（導覽列、Flash 訊息） | — |
| `index.html` | 儀表板首頁 | `base.html` |
| `transactions/index.html` | 交易列表（含篩選） | `base.html` |
| `transactions/form.html` | 新增/編輯交易表單 | `base.html` |
| `accounts/index.html` | 帳戶列表（卡片式） | `base.html` |
| `accounts/form.html` | 新增/編輯帳戶表單 | `base.html` |
| `categories/index.html` | 分類管理 + 快速新增 | `base.html` |
| `budgets/index.html` | 預算進度條 + 設定 Modal | `base.html` |

---

## 4. 路由骨架程式碼

檔案位置：
- `app/routes/main.py` — 儀表板與匯出
- `app/routes/transactions.py` — 交易 CRUD
- `app/routes/accounts.py` — 帳戶管理
- `app/routes/categories.py` — 分類管理
- `app/routes/budgets.py` — 預算進度
- `app/routes/__init__.py` — 匯出所有 Blueprint
