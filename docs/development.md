# Development

在 Mac 上開發，沒有公司網路、AD 與零件資料庫。本機環境用假資料模擬。

## 需要安裝

- [uv](https://docs.astral.sh/uv/)（Python 版本由 `backend/.python-version` 指定）
- [Task](https://taskfile.dev/)
- Docker（M1 之後）
- Node.js 與 Vite+（M1 之後）

## 目前可用

只有後端骨架，使用 SQLite：

```bash
task backend-install   # 安裝後端依賴
task backend           # 啟動 Django 開發伺服器
task lint-backend      # Ruff 檢查
task format-backend    # Ruff 格式化
task ci                # CI 會執行的檢查
```

完整清單用 `task --list` 查看。

## M1 完成後的開發環境

以下是目標狀態，尚未建立。

### 服務

`docker compose up` 會啟動：

| 服務 | 說明 |
|---|---|
| `backend` | Django，程式碼掛載進 container，改動即時生效 |
| `frontend` | Vite+ 開發伺服器，把 `/api/` 轉發給 backend |
| `mssql` | 開發用 SQL Server，內含零件庫與平台庫兩個 database |

`mssql` 只存在於開發環境。正式環境連的是公司的 SQL Server。

Apple Silicon 的注意事項：微軟的 SQL Server image 只有 x86 版本，在 M 系列 Mac 上要用模擬方式執行。M1 時實測是否夠穩定，不行的話改在本機以外的 x86 機器上跑這個服務。

### 假資料

1. 從公司取得零件表的結構（欄位名稱、型別），不含資料。
2. 用它在開發用 SQL Server 建立相同結構的零件表。
3. 寫 seed 腳本產生各零件類型的假資料，包含有備註與沒備註的情況。

在拿到實際結構之前，先用憑印象建立的近似結構開發，之後再對齊。

### 登入

開發環境使用 Django 本地帳號，用 `task createsuperuser` 建立。公司環境的登入方式見 [domains/auth.md](domains/auth.md)。

### 環境變數

資料庫位址、帳密、登入方式等設定都來自環境變數。repo 內提供 `.env.example`，實際的 `.env` 不進版控。

## 程式風格

- 後端：Ruff，設定在 `backend/pyproject.toml`（行寬 100、單引號）。
- 前端：Vite+ 內建的 lint 與 formatter，不另外裝 ESLint 或 Prettier。

## CI

`task ci` 是 CI 的唯一入口，本機與 Jenkins 執行同一個指令。目前只包含後端的 lint 與格式檢查，M1 加入測試與前端。
