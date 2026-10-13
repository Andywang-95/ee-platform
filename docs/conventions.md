# Conventions

寫程式時遵守的慣例。架構層級的決定見 [architecture.md](architecture.md) 與 [adr/](adr/)，這裡只記實作時會反覆用到的規則。

## API

### 路徑

- 一律在 `/api/` 之下，以功能領域為第一層：`/api/parts/`、`/api/bom/`。
- 資源名稱用複數名詞、小寫、以 `-` 分隔，結尾帶 `/`。
- 用 HTTP 方法表達動作，路徑裡不放動詞。

### 回應格式

沿用 DRF 的預設格式，不另外包一層。

列表一律分頁：

```json
{
  "count": 123,
  "next": "http://.../api/parts/?page=3",
  "previous": "http://.../api/parts/?page=1",
  "results": []
}
```

錯誤：

| 情況 | 狀態碼 | 內容 |
|---|---|---|
| 欄位驗證失敗 | 400 | `{"<欄位>": ["訊息"]}` |
| 其他請求錯誤 | 400 | `{"detail": "訊息"}` |
| 未登入 | 401 或 403 | `{"detail": "訊息"}` |
| 沒有權限 | 403 | `{"detail": "訊息"}` |
| 找不到 | 404 | `{"detail": "訊息"}` |
| 資料已被他人修改 | 409 | `{"detail": "訊息"}` |

### 查詢參數

- 分頁：`page`、`page_size`。`page_size` 有上限。
- 搜尋：`search`。
- 排序：`ordering=<欄位>`，欄位前加 `-` 表示遞減。
- 篩選：`<欄位>=<值>`。
- 排序與篩選只接受明確列出的欄位。收到未列出的欄位回 400，不默默忽略。

### 資料格式

- JSON 的 key 用 `snake_case`。零件欄位例外：直接使用資料庫的欄位名稱，不轉換。
- 時間用 ISO 8601 並帶時區，例如 `2026-10-13T09:30:00+08:00`。
- 沒有值用 `null`，不用空字串代表「沒有」。

### 文件

每個 API 都要能在 drf-spectacular 產生的 OpenAPI 文件中正確呈現。自動推導不出來的地方用 `extend_schema` 補上，不另外手寫 API 文件。

## 後端

### 分層

各檔案的責任見 [architecture.md](architecture.md) 的「後端分層」。

- 只讀取資料的 API 可以由 view 直接查詢。查詢條件較複雜或會被重複使用時，寫成 `queries.py` 裡的函式。
- 會改動資料的操作一律寫成 `services.py` 裡的函式，view 只負責解析請求、呼叫 service、回傳結果。
- service 函式以動詞開頭，參數用 keyword-only，操作者明確傳入：`update_part(*, part, changes, user)`。
- service 不接收 `request`，這樣測試與日後的背景工作都能直接呼叫。
- 一個 service 函式內的多筆寫入用 transaction 包起來。

### 資料庫

- 對應零件庫的 model 設 `managed = False`，並指定 `db_table`。
- 平台自己的 model 用一般的 Django migration。
- migration 產生後要看過內容再 commit，確認沒有碰到零件庫。

### 設定

- 會因環境而不同的值來自環境變數，變數名稱以 `DJANGO_` 或功能名稱開頭。
- 新增環境變數時同步更新 `.env.example`。

### 風格

- Ruff 負責 lint 與格式化，設定在 `backend/pyproject.toml`。不手動調整格式。
- 註解說明「為什麼」，不重述程式碼在做什麼。

## 測試

使用 pytest 與 pytest-django，設定檔為 `config.settings.testing`。

### 位置與命名

- 跨 app 的測試放 `backend/tests/`，共用的 fixture 放 `backend/conftest.py`。
- 各 app 的測試放 `backend/apps/<app>/tests/`。
- `libs/` 的測試放 `backend/libs/<模組>/tests/`，不使用資料庫，不 import Django。
- 檔名 `test_<對象>.py`，函式名 `test_<情境>_<預期結果>`。

### 一定要有測試的情況

- 每個需要權限的 API：沒有權限時被拒絕。
- 編輯 API：不在可編輯清單中的欄位被拒絕。
- 編輯 API：資料已被他人修改時回 409，且資料庫內容不變。
- 修改成功時有寫入修改紀錄，內容正確。
- 篩選與排序：未列出的欄位被拒絕。
- database router：零件庫的 model 不會被 migration 影響。
- `libs/` 的解析器：每種支援的檔案格式至少一個實際範例檔。

需要資料庫的測試加 `@pytest.mark.django_db`。

## 前端

套件的選擇見 [ADR-0008](adr/0008-frontend-libraries.md)。

- TypeScript，不使用 `any` 規避型別。
- 測試檔與被測的檔案放在一起，檔名為 `<對象>.test.ts`。
- 測試工具從 `vite-plus/test` 匯入，設定工具從 `vite-plus` 匯入，不直接從 `vitest` 或 `vite` 匯入。
- 呼叫 API 一律經過 `src/api/client.ts`，用相對路徑，不寫死主機位址，也不在元件裡直接呼叫 `fetch`。
- 每個功能領域的 API 函式與型別放在該領域的 `api.ts`。
- 伺服器資料一律用 TanStack Query 的 `useQuery` 取得，不用 `useEffect` 加 `useState` 自己管理載入狀態。query key 以領域名稱開頭，例如 `["parts", "list", query]`。
- 介面元件用 Ant Design，不自己寫樣式能解決的事就不寫 CSS。
- 後端 API 有變動時執行 `task gen-api` 重新產生 `src/api/schema.d.ts`，這個檔案不手動修改。
- 依功能領域分目錄（`parts`、`bom`），領域之間不互相 import 內部檔案。
- API 的型別由後端的 OpenAPI 文件產生，不手寫。零件資料列是例外：欄位隨類型不同，型別是以欄位名稱為 key 的物件。
- 零件表格與表單的欄位來自後端的 Part Configuration。
- lint 與格式化用 Vite+ 內建工具。

## Git

- 在 `develop` 開發。
- commit message 由標題與條列說明組成，中間空一行：

```text
feat: add parts query API driven by Part Configuration

- 新增 Part Configuration，定義各零件類型的列表、搜尋、篩選與可編輯欄位
- 新增零件列表 API，支援搜尋、篩選、排序與分頁
- 不在類型設定內的篩選或排序欄位回傳 400
```

- 標題格式為 `<type>: <summary>`，用英文、祈使語氣、小寫開頭、結尾不加句號。
- 條列說明用繁體中文，每一項寫一件具體的變更，以動詞開頭（新增、調整、移除、修正），結尾不加句號。
- 條列說明寫「改了什麼」。不容易從變更本身看出原因時，在該項後面補上原因。
- 每一筆 commit 都要有條列說明，只改一處的小變更寫一項即可。

| type | 用途 |
|---|---|
| `feat` | 新功能 |
| `fix` | 修正錯誤 |
| `docs` | 只改文件 |
| `refactor` | 不改變行為的程式調整 |
| `test` | 只改測試 |
| `chore` | 依賴、設定、工具 |

- 一筆 commit 只做一件事。
- commit 前執行 `task ci` 並通過。
- 不 commit `.env`、資料庫檔案、公司的實際資料。
