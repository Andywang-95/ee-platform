# ADR-0002: Backend Framework 選型

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

EE Platform 定位為企業內部工程平台，需要支援：

- 資料管理
- 權限控制
- API
- 後台管理
- 長期維護

需要選擇適合的 Backend Framework。

---

## 決策

採用：

- Python
- Django
- Django REST Framework

相關技術：

- drf-spectacular
- MSSQL
- pyodbc

---

## 理由

Django 提供完整企業應用所需能力：

### 成熟 ORM

可有效管理資料模型與 Database。

---

### Middleware 架構

方便處理：

- 使用者身份
- Session
- 權限驗證
- Request Context

---

### 企業應用生態完整

包含：

- Admin
- Authentication
- Permission Framework
- Testing Support

降低自行組裝系統成本。

---

## 考慮過的替代方案

### FastAPI

優點：

- API 開發快速
- OpenAPI 文件自動產生
- 高效能

未採用原因：

- 偏向 API Service
- 企業管理功能需要自行整合
- 權限、後台管理需要額外設計

---

## 後續影響

Backend 開發需遵循：

- API First
- Business Logic 不直接寫入 View
- 使用 Service Layer 管理複雜邏輯
- 使用 DRF Schema 管理 API 文件