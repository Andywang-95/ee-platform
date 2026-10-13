# Backend

Django + Django REST Framework，提供 REST API、資料存取與權限控管。

## 執行

後端在 container 內執行，從 repo 根目錄用 `task up` 啟動，見 [開發環境](../docs/development.md)。

lint、格式化與測試在主機上執行，不需要啟動任何服務：

```bash
task backend-install   # 安裝依賴
task test-backend      # 測試
task lint-backend      # lint
task format-backend    # 格式化
```

Django 管理指令在 container 內執行，常用的有對應的 task（`task migrate`、`task makemigrations`、`task shell`、`task createsuperuser`）。其他指令：

```bash
docker compose exec backend python manage.py <指令>
```

## 結構

```text
backend/
├── config/
│   ├── settings/       base / development / testing / production
│   ├── db_routers.py   決定 model 走零件庫或平台庫
│   ├── views.py        健康檢查
│   └── urls.py
├── apps/               每個功能領域一個 Django app
│   └── parts/
│       ├── configuration.py   各零件類型的 Part Configuration
│       ├── queries.py         零件查詢
│       └── views.py / urls.py
├── tests/              跨 app 的測試
├── conftest.py         測試共用設定
├── Dockerfile          開發用 image
├── manage.py
└── pyproject.toml
```

## 資料庫

兩個 database 在同一台 SQL Server 上：

| Django 別名 | 內容 | 結構由誰管理 |
|---|---|---|
| `default` | 平台庫：帳號、權限、session、修改紀錄 | Django migration |
| `parts` | 零件庫 | 既有流程，平台不更動 |

`parts` app 中設了 `managed = False` 的 model 會被 router 導向零件庫。migration 不會套用到零件庫。

連線設定來自環境變數，清單見根目錄的 `.env.example`。

## API

| 路徑 | 內容 |
|---|---|
| `/api/health/` | 健康檢查，回報兩個資料庫的連線狀態 |
| `/api/parts/` | 零件查詢，見 [零件功能](../docs/domains/parts.md) |
| `/api/schema/` | OpenAPI 文件 |
| `/api/docs/` | Swagger UI |

API 預設需要登入，不需要登入的 view 要明確宣告。登入功能在 M3 實作，在那之前開發環境的設定暫時允許未登入的請求。

## 設計文件

- [系統架構](../docs/architecture.md)
- [開發慣例](../docs/conventions.md)
- [零件功能](../docs/domains/parts.md)
- [登入與權限](../docs/domains/auth.md)
