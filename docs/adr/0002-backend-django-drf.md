# ADR-0002：後端使用 Django + Django REST Framework

- 狀態：Accepted
- 日期：2026-10-13

## 決策

後端使用 Python、Django、Django REST Framework，API 文件由 drf-spectacular 產生。透過 `mssql-django` 與 `pyodbc` 連接 SQL Server。

## 理由

- 內建使用者、群組、權限與 session，MVP 的權限需求不必自己設計。
- Django Admin 可以直接當作權限管理介面，省下一塊前端開發。
- 認證後端可替換，符合開發與公司環境使用不同登入方式的需求。
- ORM 支援把既有資料表對應成 model 而不管理其結構。
- 後續的檔案解析、規則檢查、AI 整合都以 Python 生態最完整。

## 放棄的選項

- FastAPI：API 開發輕快，但使用者、權限、管理後台都要自己組裝。這個專案這些需求明確存在。

## 影響

- 業務邏輯放在 service 函式，view 保持精簡。
- 與 Django 無關的解析與規則邏輯放在獨立的純 Python 模組。
