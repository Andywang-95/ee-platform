# Development

在 Mac 上開發，沒有公司網路、AD 與零件資料庫。本機環境用 Docker Compose 與假資料模擬。

## 需要安裝

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)，執行時要保持開啟
- [Task](https://taskfile.dev/)
- [uv](https://docs.astral.sh/uv/)（Python 版本由 `backend/.python-version` 指定）

主機不需要安裝 Node.js，前端工具都在 container 內執行。

## 第一次使用

```bash
task setup   # 建立 .env、安裝後端依賴、建置 image
task up      # 啟動所有服務
```

第一次啟動要下載 SQL Server 的 image 並建立資料庫，需要幾分鐘。完成後：

| 網址 | 內容 |
|---|---|
| http://localhost:5173 | 前端 |
| http://localhost:8000/api/docs/ | API 文件（Swagger UI） |
| http://localhost:8000/api/health/ | 健康檢查 |
| http://localhost:8000/admin/ | Django Admin |

前端首頁會顯示後端與兩個資料庫的連線狀態，以及零件筆數。四項都正常就代表環境沒問題。

## 服務

| 服務 | 說明 |
|---|---|
| `mssql` | 開發用 SQL Server 2022，內含零件庫（`ee_parts`）與平台庫（`ee_platform`） |
| `mssql-init` | 每次啟動時執行一次 `dev/mssql/init.sql`，建立兩個 database 與零件表，然後結束 |
| `backend` | Django 開發伺服器。啟動時自動套用 migration，零件表是空的就寫入假資料 |
| `frontend` | Vite+ 開發伺服器，把 `/api/` 轉發給 `backend` |

`backend` 與 `frontend` 的程式碼是從主機掛載進 container 的，存檔後自動生效，不需要重啟。

`mssql` 只存在於開發環境。正式環境連的是公司的 SQL Server。

微軟的 SQL Server image 只有 x86 版本，在 M 系列 Mac 上以模擬方式執行。實測可以正常使用，啟動約需 15 秒。

## 常用指令

```bash
task up                # 啟動
task down              # 停止（資料保留）
task logs              # 看所有服務的輸出
task ci                # 所有檢查，commit 前要通過
task test              # 前後端測試
task format            # 前後端自動格式化
task makemigrations    # 建立 migration
task migrate           # 套用 migration
task createsuperuser   # 建立 Django 管理者帳號
task seed-parts        # 重新產生假零件資料
task reset-db          # 刪除開發資料庫後重建
task build             # 改了依賴或 Dockerfile 之後重建 image
```

完整清單用 `task --list` 查看。

哪些在主機執行、哪些在 container 內執行：

| 在哪裡 | 內容 | 原因 |
|---|---|---|
| 主機（uv） | 後端的 lint、格式化、測試 | 測試用記憶體中的 SQLite，不需要啟動任何服務，速度快 |
| container | Django 管理指令、所有前端工具 | 需要連到 SQL Server，或需要特定版本的 Node.js |

## 新增依賴

- 後端：在 `backend/` 下執行 `uv add <套件>`，然後 `task build`。
- 前端：`docker compose run --rm frontend npm install <套件>`，然後 `task build`。

## 假資料

零件表的結構定義在 `dev/mssql/init.sql`，假資料由 `backend/apps/parts/management/commands/seed_parts.py` 產生，涵蓋 R、C、L、IC 四種類型，約三分之一的零件有備註。

目前的結構是在取得公司實際 schema 之前的假設，見 [domains/parts-schema-assumptions.md](domains/parts-schema-assumptions.md)。取得後的步驟：

1. 修改 `dev/mssql/init.sql` 使其與實際結構一致。
2. `task reset-db` 重建資料庫。
3. 用 `inspectdb` 重新產生 `Part` model，並調整 seed 腳本。

從公司只取結構，不帶出任何實際資料。

## 登入

開發環境使用 Django 本地帳號，用 `task createsuperuser` 建立。公司環境的登入方式見 [domains/auth.md](domains/auth.md)。

## 環境變數

資料庫位址、帳密、登入方式等設定都來自環境變數。根目錄的 `.env.example` 列出所有變數，`task setup` 會把它複製成 `.env`。實際的 `.env` 不進版控。

開發時唯一需要的是 `MSSQL_SA_PASSWORD`（開發用 SQL Server 的管理者密碼），其餘由 `compose.yml` 設定。

## 測試

- 後端：pytest，設定檔 `config.settings.testing`，兩個資料庫都用記憶體中的 SQLite。零件表不受 Django 管理，由 `backend/conftest.py` 在測試開始時建立。
- 前端：Vitest（透過 `vp test`），測試檔與被測的檔案放在一起，檔名為 `*.test.ts`。

SQLite 與 SQL Server 的行為有差異。與資料庫特性相關的功能（例如搜尋的大小寫與排序規則）要在 compose 環境中另外確認。

## 程式風格

完整慣例見 [conventions.md](conventions.md)。

- 後端：Ruff，設定在 `backend/pyproject.toml`（行寬 100、單引號）。
- 前端：Vite+ 內建的 lint 與 formatter，設定在 `frontend/vite.config.ts`，不另外裝 ESLint 或 Prettier。

## 編輯器

前端的依賴裝在 container 裡，主機上沒有 `node_modules`，所以編輯器不會有 TypeScript 的型別提示。需要的話在主機安裝 Node.js 24.11 以上與 npm 12，然後在 `frontend/` 下執行 `npm ci`。這只影響編輯器，不影響 container 內的執行。

## CI

`task ci` 是 CI 的唯一入口，本機與 Jenkins 執行同一個指令。內容：

- 後端：Ruff lint、格式檢查、pytest
- 前端：lint、型別檢查、格式檢查、測試、正式建置

## 疑難排解

| 狀況 | 處理 |
|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop 沒有開啟 |
| `Run "task setup" to create .env` | 沒有 `.env`，執行 `task setup` |
| 前端顯示無法連線到後端 | `task logs` 看 `backend` 的錯誤訊息 |
| 改了 `package.json` 或 `pyproject.toml` 後找不到套件 | `task build` |
| 改了 `init.sql` 但零件表沒有變 | 腳本不會修改已存在的表，執行 `task reset-db` |
