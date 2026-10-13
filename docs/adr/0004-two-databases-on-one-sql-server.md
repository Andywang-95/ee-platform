# ADR-0004：在同一台 SQL Server 上使用兩個 database

- 狀態：Accepted
- 日期：2026-10-13

## 背景

零件資料在公司既有的 SQL Server database 中，Capture CIS 也在使用。平台需要存放自己的資料：使用者、權限、session、修改紀錄，以及日後各工具的資料。

## 決策

- 零件庫：既有的 database。平台只讀寫資料，不更動結構。對應的 Django model 設 `managed = False`。
- 平台庫：在同一台 SQL Server 上新建一個 database，作為 Django 的預設資料庫，結構由 Django migration 管理。
- 用 database router 決定 model 走哪個 database，並確保 migration 只套用到平台庫。

## 理由

- 平台的資料表不會出現在零件庫，不影響 CIS，也不需要在零件庫上建表的權限。
- 只有一種資料庫引擎與一種連線方式，開發、部署、備份都單純。
- 該 SQL Server 本來就在內網且不對外連線，符合資料不出公司的要求。

## 放棄的選項

- 平台資料表直接建在零件庫：與 CIS 的資料混在一起，結構變更的風險高。
- 另外用 PostgreSQL 存平台資料：多一種資料庫要維護。公司已有可用的 SQL Server，沒有必要。

## 影響

- 跨 database 的資料之間沒有外鍵約束。修改紀錄以零件的識別值指向零件，不建立資料庫層級的關聯。
- 日後做 RAG 需要向量搜尋時，再評估當時 SQL Server 版本的支援程度或另外引入專用服務。
