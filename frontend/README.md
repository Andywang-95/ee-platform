# Frontend

React + TypeScript，使用 Vite+ 作為工具鏈。

## 現況

專案尚未建立，會在里程碑 M1 用 Vite+ 初始化。建立後在這裡補上指令與目錄結構。

## 已決定的方向

- 語言：TypeScript。
- 建置、測試、lint、格式化都用 Vite+，不另外安裝 ESLint 或 Prettier。
- 開發時由開發伺服器把 `/api/` 轉發到後端；正式環境前端與 API 由同一個網址提供。
- 零件表格的欄位由後端的 Part Configuration 決定，前端不寫死。
- 依功能領域組織程式碼（parts、bom 等），各自獨立。

元件庫、資料請求、狀態管理等套件在建立專案時再選。

## 設計文件

- [選型理由](../docs/adr/0003-frontend-react-vite-plus.md)
- [系統架構](../docs/architecture.md)
- [零件功能](../docs/domains/parts.md)
