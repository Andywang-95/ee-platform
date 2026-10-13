# EE Platform

給 EE 使用的內部工具平台。個人專案，在 Mac 上開發，之後才部署到公司內網。規劃與現況見 [docs/roadmap.md](docs/roadmap.md)。

## 語言

- 對話、文件、commit 以外的說明文字：繁體中文。
- 程式碼、識別字、程式註解、commit message：英文。
- 開發者不熟前端，也不熟部署與驗證機制。用到相關術語時簡短說明。

## 指令

從 repo 根目錄用 `task` 執行，完整清單用 `task --list` 查看。

```bash
task up              # 啟動開發環境（Docker Compose）
task ci              # 前後端的 lint、格式檢查、測試。commit 前必須通過
task test-backend    # 只跑後端測試
task format          # 前後端自動格式化
```

- 後端的 lint 與測試在主機上用 `uv run` 執行，不直接呼叫 `python` 或 `pip`。
- Django 管理指令與所有前端工具在 container 內執行：`docker compose exec backend python manage.py ...`、`docker compose run --rm frontend vp ...`。主機的 Node.js 版本不符合 Vite+ 的要求，不要在主機上直接執行 `npm` 或 `vp`。
- Vite+ 的用法見 [frontend/AGENTS.md](frontend/AGENTS.md)。

## 不可違反的約束

- 零件庫是公司既有資料庫，平台不更動其結構。對應它的 model 一律 `managed = False`，不得為它產生 migration。見 [docs/domains/parts.md](docs/domains/parts.md)。
- `backend/libs/` 內的模組不得 import Django。見 [docs/architecture.md](docs/architecture.md)。
- 零件欄位清單只來自後端的 Part Configuration，前端不寫死欄位。
- 權限一律在後端檢查，前端的顯示與隱藏只是使用體驗。
- 修改零件與寫入修改紀錄必須在同一個 service 函式中完成。
- 密鑰與連線資訊只來自環境變數，不寫進程式碼或文件。

## 工作方式

- 依需要建立檔案，不預先建空檔或空的抽象層。
- 公司環境尚未確認的事不要自行假設。需要假設才能繼續時，寫進 [docs/domains/parts-schema-assumptions.md](docs/domains/parts-schema-assumptions.md) 或 [docs/open-questions.md](docs/open-questions.md)。
- 做了架構層級的決定就新增 ADR；改變既有決定時新增一份並標明取代哪一份。
- 行為或指令改變時同步更新對應文件。
- commit 格式為 `<type>: <summary>`，type 用 `feat`、`fix`、`docs`、`chore`、`refactor`、`test`。

寫程式前先看 [docs/conventions.md](docs/conventions.md)。

## 文件

| 文件 | 內容 |
|---|---|
| [docs/roadmap.md](docs/roadmap.md) | MVP 範圍與里程碑 |
| [docs/architecture.md](docs/architecture.md) | 系統組成、資料庫分工、目錄結構、後端分層 |
| [docs/conventions.md](docs/conventions.md) | API、後端、測試、Git 的慣例 |
| [docs/development.md](docs/development.md) | 本機開發環境 |
| [docs/deployment.md](docs/deployment.md) | 公司內部署方式 |
| [docs/open-questions.md](docs/open-questions.md) | 進公司前要確認的事項 |
| [docs/domains/](docs/domains/) | 各功能領域的設計 |
| [docs/adr/](docs/adr/) | 架構決策紀錄 |
