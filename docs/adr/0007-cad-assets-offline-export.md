# ADR-0007：Symbol 與 Footprint 以離線批次匯出取得，不納入 MVP

- 狀態：Accepted（方向）；具體做法待技術驗證
- 日期：2026-10-13

## 背景

希望在零件頁面顯示 symbol 與 footprint 圖形。來源是 OrCAD Capture 的 OLB 檔與 Allegro 的 DRA 檔，兩者都是沒有公開規格的私有二進位格式，也沒有可靠的開源解析器。

## 決策

- 這項功能不在 MVP 內，排在第二階段。
- 平台不直接解析 OLB 與 DRA。在裝有 Cadence 軟體的機器上，用 Cadence 自己的工具批次匯出成公開格式，再轉為 SVG 或 JSON 供平台顯示。
- 實作前先完成技術驗證，項目列在 [domains/cad-assets.md](../domains/cad-assets.md)。

## 理由

- 自行逆向私有格式的工期與成功率無法估計，且 Cadence 改版時可能失效。
- 用原廠工具匯出，格式正確性由原廠保證。
- MVP 的核心價值是查詢與維護，不應被一個不確定性高的功能卡住。

## 代價

- 需要一台有 Cadence license 的機器執行匯出。
- 圖形不是即時的，symbol 或 footprint 更新後要重新匯出。

## 放棄的選項

- 在後端直接解析二進位檔：風險過高。
- 以開源的 OpenOrCadParser 為基礎：該專案已封存且不完整，也不涵蓋 DRA。
