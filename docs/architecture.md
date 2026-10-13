# Architecture

## 系統組成

```text
瀏覽器
  │
  ▼
反向代理 ── 提供前端靜態檔
  │
  └─ /api/ ──► Backend (Django + DRF)
                  │
                  ├──► 零件庫   (既有 database，CIS 也在用)
                  └──► 平台庫   (新建 database，平台自己管理)
                       └── 兩者在同一台 SQL Server 上
```

- 前端與 API 由同一個網址提供，正式環境沒有跨來源問題。
- 前端不直接連資料庫，所有資料經過後端 API。
- 所有服務用 Docker Compose 組合，前後端各自有 Dockerfile。

## 技術選擇

| 層 | 選擇 | 決策紀錄 |
|---|---|---|
| Repository | 單一 repo，`backend/` 與 `frontend/` 分開 | [ADR-0001](adr/0001-monorepo.md) |
| 後端 | Django + DRF + drf-spectacular | [ADR-0002](adr/0002-backend-django-drf.md) |
| 前端 | React + TypeScript + Vite+ | [ADR-0003](adr/0003-frontend-react-vite-plus.md) |
| 資料庫 | 同一台 SQL Server 上兩個 database | [ADR-0004](adr/0004-two-databases-on-one-sql-server.md) |
| 登入 | 可抽換的登入後端 | [ADR-0005](adr/0005-auth-pluggable-backends.md) |
| 部署 | 專用 PC 上的 Docker Compose | [ADR-0006](adr/0006-deployment-compose-on-dedicated-pc.md) |
| CAD 圖形 | 離線批次匯出 | [ADR-0007](adr/0007-cad-assets-offline-export.md) |

## 資料庫分工

| | 零件庫 | 平台庫 |
|---|---|---|
| 內容 | 零件資料 | 帳號、權限、session、修改紀錄，以及日後各工具的資料 |
| 結構由誰管理 | 既有流程，平台不更動 | Django migration |
| Django 設定 | model 設 `managed = False` | 預設資料庫 |
| 平台帳號權限 | 讀寫資料 | 完整權限 |

用 Django 的 database router 決定每個 model 走哪個 database。migration 只會套用到平台庫，不會碰零件庫。

## 資料庫連線身分

後端用一個平台專用帳號連 SQL Server，使用者本人不直接連資料庫。帳號形式有三種可能，取決於公司 SQL Server 的設定，見 [deployment.md](deployment.md)。連線設定全部來自環境變數，切換形式不需要改程式。

## 目錄結構

```text
ee-platform/
├── backend/
│   ├── config/          Django 設定（依環境分檔）
│   ├── apps/            Django app，每個對應一個功能領域
│   │   └── parts/
│   └── libs/            不依賴 Django 的純 Python 模組（日後建立）
├── frontend/            React 專案（M1 建立）
├── docs/
├── compose.yml          （M1 建立）
└── Taskfile.yml
```

## 後端分層

每個 Django app 依需要建立檔案，不預先建空檔：

| 檔案 | 責任 |
|---|---|
| `models.py` | 資料表對應 |
| `serializers.py` | API 的輸入輸出格式與驗證 |
| `services.py` | 有業務意義的操作，例如「編輯零件並寫入修改紀錄」 |
| `views.py` / `urls.py` | HTTP 層，保持精簡 |

API 文件由 drf-spectacular 從程式碼產生，不另外手寫。

## 檔案解析與規則檢查

BOM 解析、netlist 解析、線路規則檢查這類邏輯放在 `backend/libs/`，寫成不 import Django 的純 Python 模組。Django app 只負責接收上傳、呼叫模組、回傳結果。

這樣做的理由：

- 可以用一般的單元測試餵檔案進去驗證，不需要資料庫或 HTTP。
- 同一份解析器可以被多個功能共用（BOM review 與 auto BOM）。
- 日後改成背景工作執行時，不用重寫邏輯。

## 尚未決定

- 非同步工作機制：等第一個需要它的功能出現時再選。
- AI 模型服務與向量資料庫：等開始做 AI 功能時再評估。
- 正式環境的反向代理軟體：取決於無感登入的做法，見 [domains/auth.md](domains/auth.md)。
