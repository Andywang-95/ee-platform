# EE Platform

給 EE 使用的內部工具平台，目標是把日常會用到的工具集中在一個網站：查零件、BOM 工具、線路檢查，之後再接上 AI。

目前是個人專案，處於規劃完成、準備開始實作的階段。MVP 完成並實測後才會評估部署到公司。

## MVP 範圍

不依賴 Capture CIS 就能查詢公司零件資料庫的網頁介面：

- 依零件類型查詢、搜尋、篩選
- 滑鼠懸停在零件上顯示備註欄位
- 特定人員可以編輯零件資料，修改留有紀錄

Symbol / Footprint 圖形顯示排在 MVP 之後。完整規劃見 [docs/roadmap.md](docs/roadmap.md)。

## 技術棧

| 層 | 選擇 |
|---|---|
| 前端 | React、TypeScript、Vite+ |
| 後端 | Python 3.13、Django 5.2、Django REST Framework、drf-spectacular |
| 資料庫 | Microsoft SQL Server（既有零件庫 + 平台專用庫） |
| 執行環境 | Docker Compose |
| 開發工具 | uv、Ruff、Taskfile |

## 快速開始

目前只有後端骨架：

```bash
task backend-install
task backend
```

前端專案與 compose 環境會在里程碑 M1 建立，見 [docs/development.md](docs/development.md)。

## 文件

| 文件 | 內容 |
|---|---|
| [docs/roadmap.md](docs/roadmap.md) | 願景、MVP 範圍、里程碑、後續功能 |
| [docs/architecture.md](docs/architecture.md) | 系統組成、資料庫分工、目錄結構 |
| [docs/development.md](docs/development.md) | 本機開發環境 |
| [docs/conventions.md](docs/conventions.md) | API、後端、測試、Git 的慣例 |
| [docs/deployment.md](docs/deployment.md) | 公司內部署方式 |
| [docs/open-questions.md](docs/open-questions.md) | 進公司前要確認的事項 |
| [docs/domains/parts.md](docs/domains/parts.md) | 零件查詢與維護 |
| [docs/domains/auth.md](docs/domains/auth.md) | 登入與權限 |
| [docs/domains/cad-assets.md](docs/domains/cad-assets.md) | Symbol / Footprint 顯示的技術驗證 |
| [docs/adr/](docs/adr/) | 架構決策紀錄 |
