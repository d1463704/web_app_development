# 路由設計文件 - 食譜收藏夾

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁 / 食譜列表 | GET | `/` | `index.html` | 顯示所有食譜卡片，支援關鍵字搜尋 |
| 顯示新增表單 | GET | `/recipes/new` | `recipe_form.html` | 顯示空白新增表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單，存入 DB，重導向至詳細頁 |
| 食譜詳細頁 | GET | `/recipes/<id>` | `recipe_detail.html` | 顯示食譜材料、步驟與等待時間 |
| 顯示編輯表單 | GET | `/recipes/<id>/edit` | `recipe_form.html` | 預填現有資料的編輯表單 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收表單，更新 DB，重導向至詳細頁 |
| 刪除確認頁 | GET | `/recipes/<id>/delete` | `recipe_confirm_delete.html` | 顯示刪除確認訊息 |
| 執行刪除 | POST | `/recipes/<id>/delete` | — | 刪除食譜（含材料與步驟），重導向至首頁 |

---

## 2. 每個路由的詳細說明

### `GET /` — 首頁 / 食譜列表

- **輸入**：URL query string `?q=<關鍵字>`（選填）
- **處理邏輯**：
  - 若有 `q` 參數：`Recipe.query.filter(Recipe.name.contains(q))`
  - 若無 `q` 參數：`Recipe.query.order_by(Recipe.created_at.desc()).all()`
- **輸出**：`render_template('index.html', recipes=recipes, q=q)`
- **錯誤處理**：查無資料時顯示「尚無食譜」提示文字

---

### `GET /recipes/new` — 顯示新增表單

- **輸入**：無
- **處理邏輯**：直接渲染空白表單頁面
- **輸出**：`render_template('recipe_form.html', recipe=None, action='new')`
- **錯誤處理**：無

---

### `POST /recipes` — 建立食譜

- **輸入（表單欄位）**：
  - `name`（必填）、`description`、`servings`、`category`
  - `ingredient_name[]`、`ingredient_amount[]`（陣列，各材料）
  - `step_instruction[]`、`step_wait_minutes[]`（陣列，各步驟）
- **處理邏輯**：
  1. 驗證 `name` 不為空
  2. 建立 `Recipe` 物件並寫入 DB
  3. 逐筆建立 `Ingredient` 物件
  4. 逐筆建立 `Step` 物件（含 `wait_minutes`）
  5. `db.session.commit()`
- **輸出**：`redirect(url_for('recipes.detail', id=new_recipe.id))`
- **錯誤處理**：驗證失敗時重新渲染表單並顯示錯誤訊息

---

### `GET /recipes/<id>` — 食譜詳細頁

- **輸入**：URL 參數 `id`（整數）
- **處理邏輯**：`Recipe.query.get_or_404(id)`（自動取得關聯的 ingredients 與 steps）
- **輸出**：`render_template('recipe_detail.html', recipe=recipe)`
- **錯誤處理**：`id` 不存在時回傳 404 頁面

---

### `GET /recipes/<id>/edit` — 顯示編輯表單

- **輸入**：URL 參數 `id`（整數）
- **處理邏輯**：`Recipe.query.get_or_404(id)`，取得現有資料
- **輸出**：`render_template('recipe_form.html', recipe=recipe, action='edit')`
- **錯誤處理**：`id` 不存在時回傳 404

---

### `POST /recipes/<id>/edit` — 更新食譜

- **輸入**：URL 參數 `id` + 同 POST /recipes 的表單欄位
- **處理邏輯**：
  1. 驗證 `name` 不為空
  2. 更新 `Recipe` 物件的欄位
  3. 刪除舊有的 `Ingredient` 與 `Step`
  4. 重新建立新的 `Ingredient` 與 `Step`
  5. `db.session.commit()`
- **輸出**：`redirect(url_for('recipes.detail', id=id))`
- **錯誤處理**：驗證失敗時重新渲染表單並顯示錯誤訊息

---

### `GET /recipes/<id>/delete` — 刪除確認頁

- **輸入**：URL 參數 `id`（整數）
- **處理邏輯**：`Recipe.query.get_or_404(id)`，確認食譜存在
- **輸出**：`render_template('recipe_confirm_delete.html', recipe=recipe)`
- **錯誤處理**：`id` 不存在時回傳 404

---

### `POST /recipes/<id>/delete` — 執行刪除

- **輸入**：URL 參數 `id`（整數）
- **處理邏輯**：
  1. `Recipe.query.get_or_404(id)`
  2. `db.session.delete(recipe)`（CASCADE 自動刪除 ingredients 與 steps）
  3. `db.session.commit()`
- **輸出**：`redirect(url_for('recipes.index'))`
- **錯誤處理**：`id` 不存在時回傳 404

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 用途 |
|----------|--------|------|
| `base.html` | — | 共用版型（導覽列、頁首、頁尾、CSS 引入） |
| `index.html` | `base.html` | 首頁：食譜卡片列表 + 搜尋欄 |
| `recipe_detail.html` | `base.html` | 詳細頁：材料清單 + 步驟（含等待時間徽章） |
| `recipe_form.html` | `base.html` | 新增 / 編輯食譜表單（共用，依 `action` 變數切換標題） |
| `recipe_confirm_delete.html` | `base.html` | 刪除確認頁：顯示食譜名稱 + 確認 / 取消按鈕 |
