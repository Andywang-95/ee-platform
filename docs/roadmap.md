# Roadmap

## 願景

整合 EE 日常需要的工具到單一平台：零件資訊查詢、BOM 轉換與審查、線路檢查、PCB 快速模擬。平台成熟後串接 AI 模型與 RAG，協助 EE 更快解決問題。

## 前提

- 目前是個人專案，在 Mac 上開發。
- MVP 完成並實測後，才評估部署到公司。
- 公司環境是 Windows 與 Active Directory，零件資料庫在不對外連線的 SQL Server 上，EE 目前透過 Capture CIS 使用它。
- 部署目標是一台專用的筆電或 PC，用 Docker Compose 執行。需要串接 AI 模型時才考慮正式伺服器。

## MVP：零件資料庫查詢與維護

讓使用者不開 Capture CIS 也能查零件，並讓指定人員維護資料。

包含：

- 依零件類型瀏覽，支援關鍵字搜尋與欄位篩選
- 懸停在零件上顯示資料庫中的備註欄位
- 指定人員可編輯零件資料
- 修改紀錄（誰、何時、改了什麼）

不包含：

- Symbol / Footprint 圖形顯示（見第二階段）
- 新增或刪除零件、批次修改、審核流程
- AD 群組對應權限（MVP 以個人為單位指派）

## 里程碑

### M1 開發環境

- Docker Compose：backend、frontend、開發用 SQL Server（內含零件庫與平台庫兩個 database）
- 依公司實際 schema 建立開發用零件庫，並寫假資料 seed 腳本
- 用 Vite+ 建立 React + TypeScript 專案
- Django 設定改為雙資料庫與環境變數
- `task ci` 涵蓋前後端的 lint、format 檢查、測試

完成標準：`docker compose up` 後瀏覽器能開到前端頁面，前端能呼叫後端的健康檢查 API，後端能讀到假的零件資料。

### M2 零件查詢

- 由 schema 產生對應零件表的 model（Django 不管理其結構）
- 各零件類型的 Part Configuration
- 列表、搜尋、篩選、單筆詳情 API，含 OpenAPI 文件
- 前端：類型切換、資料表格、搜尋與篩選、備註懸停

完成標準：能在網頁上查到任一類型的零件，欄位依類型不同而變化。

### M3 登入與編輯

- 本地帳號登入（開發用）
- 編輯權限以 Django 內建權限控管，在 Django Admin 指派
- 編輯 API 與前端編輯介面，只開放設定中允許的欄位
- 平台自己的修改紀錄

完成標準：沒有權限的帳號看不到編輯功能且 API 會拒絕；有權限的帳號修改後可查到紀錄。

### M4 公司部署

- 申請平台專用帳號與平台專用 database
- 接上公司的零件庫，對齊實際欄位
- 無感登入（Windows 身分自動辨識）
- 主機設定與開機自動啟動
- Jenkins pipeline

開始前要先解決 [open-questions.md](open-questions.md) 列出的事項。

## 第二階段：Symbol / Footprint 顯示

在零件頁面顯示該零件的 symbol 與 footprint 圖形。OLB 與 DRA 都是 Cadence 的私有格式，需要先做技術驗證再決定做法，見 [domains/cad-assets.md](domains/cad-assets.md)。

## 後續功能

順序未定，依實際需求調整。

| 功能 | 說明 | 對架構的影響 |
|---|---|---|
| BOM review | 審查 BOM 內容，與零件庫比對 | 需要 BOM 檔案解析器 |
| 線路比對 | 依規則檢查 `.bom` / `.net` 的內容，找出異常 | 需要 netlist 解析器與規則引擎 |
| Auto BOM | 轉換 BOM 格式 | 與 BOM review 共用解析器 |
| PCB 機構模擬 | 快速模擬 PCB 結構，零件有高度屬性時呈現高度 | 前端 3D 繪圖 |
| AI / RAG | 用 AI 協助查詢與解決 EE 問題 | 需要模型服務與向量資料庫，屆時再評估伺服器 |

這些功能的共同點是「解析檔案後套用規則」。解析器與規則會寫成不依賴 Django 的純 Python 模組，見 [architecture.md](architecture.md)。

處理時間長的工具需要非同步工作機制。等第一個確實需要它的功能出現時再選技術。
