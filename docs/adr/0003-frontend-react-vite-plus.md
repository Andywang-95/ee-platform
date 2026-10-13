# ADR-0003：前端使用 React + TypeScript + Vite+

- 狀態：Accepted
- 日期：2026-10-13
- 取代：先前選用 Vue 3 的決定

## 決策

前端使用 React 與 TypeScript。建置、測試、lint、格式化使用 Vite+（`vp` 指令），不另外安裝 ESLint 或 Prettier。

## 理由

選 React：

- MVP 的表格與表單需求，React 與 Vue 都能做好，差別在後續功能。
- AI 對話介面的現成元件多以 React 為優先支援對象。
- PCB 機構模擬需要 3D 繪圖，React 有成熟的 three.js 整合。
- 開發者對前端框架不熟，會大量依賴 AI 輔助，React 的範例與訓練資料最多。

選 Vite+：

- 一個工具涵蓋開發伺服器、建置、測試、lint、格式化，設定檔少。
- MIT 授權開源。

## 風險與退路

Vite+ 是較新的工具。M1 建立專案時（2026-10-14）npm 上的正式版為 1.1.0，專案使用這個版本。

若不夠穩定，退回一般的 Vite 搭配 Oxlint 與 Oxfmt。Vite+ 本身就是包裝這些工具，退回的成本主要是改指令與設定檔，應用程式碼不受影響。

## 放棄的選項

- Vue 3：能力足夠，但後續 AI 與 3D 相關的現成資源較少。
- 元件庫、狀態管理、資料請求等套件：M2 開始做零件頁面時再選，不在這裡決定。

## M1 的補充決定

- 套件管理使用 npm。Vite+ 支援多種套件管理工具，npm 隨 Node.js 提供，不需要另外安裝。
- 前端工具在 container 內執行。Vite+ 1.1.0 要求 Node.js 24.11 以上，在 container 內固定版本可以避免主機版本不符，本機與 Jenkins 的行為也一致。
- 不安裝全域的 `vp` 指令，使用專案內的 `vite-plus` 套件。
