# CAD Assets：Symbol 與 Footprint 顯示

第二階段功能，不在 MVP 內。這份文件記錄問題、方向與需要先做的技術驗證。

## 目標

在零件頁面顯示該零件的 schematic symbol 與 PCB footprint 圖形，讓使用者不開 Capture 或 Allegro 就能確認外觀。

## 現況

- Symbol：OrCAD Capture 的 OLB 檔。依零件種類分成多個 OLB，每個 OLB 內含多個零件的 symbol。
- Footprint：Allegro 的 DRA 檔，每個 footprint 一個檔。
- 零件庫中有欄位記錄每個零件對應的 symbol 與 footprint 名稱。

## 困難

兩種檔案都是 Cadence 的私有二進位格式，沒有公開規格。

- OLB：開源的 [OpenOrCadParser](https://github.com/Werni2A/OpenOrCadParser) 已於 2026 年 5 月封存，且解析並不完整。
- DRA：沒有找到開源解析器。KiCad 的 Allegro 匯入只支援 `.brd`，不支援 footprint 檔。

自行逆向解析的工期與成功率都難以估計，而且 Cadence 改版時格式可能變動。

## 方向：離線批次匯出

不在平台內解析原始檔。在裝有 Cadence 軟體的機器上，用 Cadence 自己的工具把檔案轉成公開格式，平台只負責儲存與顯示轉換後的結果。

```text
OLB / DRA
   │  在有 Cadence license 的機器上批次執行
   ▼
中間格式（XML / 文字）
   │  轉換腳本
   ▼
SVG 或 JSON
   │  放到平台可讀取的位置
   ▼
平台依零件的 symbol / footprint 名稱取出並顯示
```

可能的匯出途徑，都需要驗證：

| 檔案 | 途徑 |
|---|---|
| OLB | Capture 內建的 TCL 腳本可將 library 匯出為 XML |
| DRA | Allegro 的 Extracta 工具可匯出文字格式；或用 SKILL 腳本批次輸出 |

代價：零件庫的 symbol 或 footprint 有更新時要重新匯出。需要決定是定期執行還是手動觸發。

決策紀錄見 [ADR-0007](../adr/0007-cad-assets-offline-export.md)。

## 技術驗證

開始實作前，依序確認：

1. 用一個 OLB 實際匯出 XML，確認內容足以畫出 symbol（線條、接腳、文字、多 part 的元件）。
2. 用幾個 DRA 實際匯出，確認能取得 pad 形狀、外框、絲印等幾何資料。
3. 匯出能否不經人工操作批次執行。
4. 零件庫中的 symbol / footprint 欄位值，能否對應到匯出結果中的名稱。
5. 抽樣比對轉換出的圖形與原軟體中的顯示是否一致。

任何一項不通過，就回頭評估替代方案：只顯示名稱並提供檔案下載、由人工截圖上傳、或縮小範圍只做其中一種。

## 開始前需要的資訊

見 [open-questions.md](../open-questions.md) 的「第二階段前要確認的」。
