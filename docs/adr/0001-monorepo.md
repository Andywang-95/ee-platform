# ADR-0001：前後端放在同一個 repository

- 狀態：Accepted
- 日期：2026-10-13

## 決策

前端與後端放在同一個 Git repository，分別位於 `frontend/` 與 `backend/`，各自管理依賴與 Dockerfile。根目錄放 compose 檔、Taskfile 與文件。

## 理由

- 一個人開發，API 與畫面經常一起改，同一個 commit 能同時包含兩邊的變更。
- 部署是整組服務一起更新，同一個 repo 的版本天然一致。
- 文件與決策紀錄集中在一處。

## 放棄的選項

- 前後端各一個 repo：版本要另外對齊，對單人專案只增加負擔。
- 只用 Django template 不做獨立前端：後續的 3D 模擬、AI 對話等功能需要較重的前端互動。
