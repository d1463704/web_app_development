# 路由設計文件 — 食譜收藏夾

本文件根據 [PRD](./PRD.md)、[ARCHITECTURE](./ARCHITECTURE.md) 與 [DB_DESIGN](./DB_DESIGN.md)，規劃所有 Flask 路由的 URL、HTTP 方法與對應邏輯。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁（食譜列表） | GET | `/` | `index.html` | 顯示所有食譜，支援分類篩選 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipe_form.html` | 顯示空白新增表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單，存入 DB，重導向到詳情頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `recipe_detail.html` | 顯示單道食譜的完整內容 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `recipe_form.html` | 顯示預填資料的編輯表單 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收修改，更新 DB，重導向到詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除食譜，重導向到首頁 |
| 搜尋食譜 | GET | `/recipes/search` | `search.html` | 根據食材關鍵字搜尋食譜 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁（食譜列表）

| 項目 | 說明 |
| --- | --- |
| **URL** | `GET /` |
| **輸入** | 查詢參數 `category_id`（可選，用於篩選分類） |
| **處理邏輯** | 若有 `category_id`，呼叫 `recipe.get_by_category()`；否則呼叫 `recipe.get_all()`。同時呼叫 `category.get_all()` 取得分類清單供篩選用。 |
| **輸出** | 渲染 `index.html`，傳入 `recipes`、`categories`、`current_category` |
| **錯誤處理** | 無特殊錯誤情境 |

---

### 2.2 新增食譜頁面

| 項目 | 說明 |
| --- | --- |
| **URL** | `GET /recipes/new` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `category.get_all()` 取得分類清單供表單下拉選單使用。 |
| **輸出** | 渲染 `recipe_form.html`，傳入 `categories`、`recipe=None`（表示新增模式） |
| **錯誤處理** | 無 |

---

### 2.3 建立食譜

| 項目 | 說明 |
| --- | --- |
| **URL** | `POST /recipes` |
| **輸入** | 表單欄位：`title`、`description`、`steps`、`category_id`、`ingredients[]`（名稱與用量）、`tags` |
| **處理邏輯** | 1. 驗證必填欄位（title、steps、至少一項材料）<br>2. 呼叫 `recipe.create()` 建立食譜<br>3. 若有標籤，呼叫 `tag.get_or_create()` 再呼叫 `tag.set_recipe_tags()` |
| **輸出** | 成功：重導向到 `/recipes/<新ID>`<br>失敗：重新渲染表單並顯示錯誤訊息 |
| **錯誤處理** | 必填欄位為空時，回傳表單並提示錯誤 |

---

### 2.4 食譜詳情

| 項目 | 說明 |
| --- | --- |
| **URL** | `GET /recipes/<id>` |
| **輸入** | URL 參數 `id`（食譜 ID） |
| **處理邏輯** | 呼叫 `recipe.get_by_id(id)` 取得食譜資料（含材料與標籤） |
| **輸出** | 渲染 `recipe_detail.html`，傳入 `recipe` |
| **錯誤處理** | 若 `recipe` 為 None，回傳 404 頁面 |

---

### 2.5 編輯食譜頁面

| 項目 | 說明 |
| --- | --- |
| **URL** | `GET /recipes/<id>/edit` |
| **輸入** | URL 參數 `id`（食譜 ID） |
| **處理邏輯** | 呼叫 `recipe.get_by_id(id)` 與 `category.get_all()`，取得現有資料與分類清單 |
| **輸出** | 渲染 `recipe_form.html`，傳入 `recipe`（預填資料）、`categories` |
| **錯誤處理** | 若 `recipe` 為 None，回傳 404 頁面 |

---

### 2.6 更新食譜

| 項目 | 說明 |
| --- | --- |
| **URL** | `POST /recipes/<id>/edit` |
| **輸入** | URL 參數 `id` + 表單欄位（同建立食譜） |
| **處理邏輯** | 1. 驗證必填欄位<br>2. 呼叫 `recipe.update()` 更新食譜<br>3. 呼叫 `tag.set_recipe_tags()` 更新標籤 |
| **輸出** | 成功：重導向到 `/recipes/<id>`<br>失敗：重新渲染表單並顯示錯誤訊息 |
| **錯誤處理** | 食譜不存在回傳 404；必填欄位為空回傳表單錯誤 |

---

### 2.7 刪除食譜

| 項目 | 說明 |
| --- | --- |
| **URL** | `POST /recipes/<id>/delete` |
| **輸入** | URL 參數 `id`（食譜 ID） |
| **處理邏輯** | 呼叫 `recipe.delete(id)` 刪除食譜（CASCADE 會自動刪除材料與標籤關聯） |
| **輸出** | 重導向到 `/`（首頁） |
| **錯誤處理** | 若食譜不存在，回傳 404 頁面 |

---

### 2.8 搜尋食譜

| 項目 | 說明 |
| --- | --- |
| **URL** | `GET /recipes/search` |
| **輸入** | 查詢參數 `q`（食材關鍵字，以逗號或空白分隔） |
| **處理邏輯** | 將 `q` 拆分為關鍵字列表，呼叫 `recipe.search_by_ingredients(keywords)` |
| **輸出** | 渲染 `search.html`，傳入 `recipes`、`query` |
| **錯誤處理** | 若 `q` 為空，顯示空的搜尋頁面 |

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承 | 說明 |
| --- | --- | --- |
| `base.html` | — | 共用版型：HTML 結構、導覽列、頁尾、CSS/JS 引入 |
| `index.html` | `base.html` | 首頁：食譜卡片列表 + 分類篩選側欄 |
| `recipe_detail.html` | `base.html` | 食譜詳情：標題、簡介、材料清單、步驟、標籤、編輯/刪除按鈕 |
| `recipe_form.html` | `base.html` | 新增/編輯共用表單：食譜名稱、簡介、材料（動態新增）、步驟、分類下拉、標籤 |
| `search.html` | `base.html` | 搜尋頁：搜尋欄 + 結果列表 |

### 模板區塊（Blocks）設計

`base.html` 定義以下可覆寫區塊：

```
{% block title %}食譜收藏夾{% endblock %}
{% block content %}{% endblock %}
{% block extra_css %}{% endblock %}
{% block extra_js %}{% endblock %}
```

---

## 4. 路由骨架程式碼

路由骨架檔案位於 `app/routes/recipe.py`，詳見該檔案。
