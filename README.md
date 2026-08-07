# EE Platform

EE Platform 是一個以 **Django + Django REST Framework + Vue.js** 為基礎開發的企業內部工程平台 Demo。

本專案主要目標是提供一個可維護、可擴充的架構，用於管理與查詢電子零件資料（Parts），並逐步取代部分既有桌面工具的操作流程。

目前專案仍處於初期架構設計與開發階段，所有設計皆以可維護性、可擴充性與企業級開發流程為主要考量。

---

## 專案目標

- 建立企業級 Web Platform 架構
- 提供零件資料查詢功能
- 建立完整的權限管理機制
- 建立零件維護流程
- 提供 API 供前端與其他系統整合
- 建立可持續擴充的系統架構

---

## 技術架構

### Backend

- Python
- Django
- Django REST Framework
- drf-spectacular
- Microsoft SQL Server

### Frontend

- Vue.js
- TypeScript

### Development

- uv
- Ruff
- Docker
- Docker Compose

---

## 專案結構

```text
.
├── backend/
├── frontend/
├── docs/
└── README.md
```

---

## 文件

所有設計文件皆放置於 `docs/`。

目前包含：

- 系統架構
- Database 設計
- Domain Design
- Authentication Design
- ADR（Architecture Decision Records）
- Development Guideline

---

## 快速開始

Backend：

```bash
cd backend
uv sync
uv run python manage.py runserver
```

Frontend：

> Frontend 尚未開始建置。

---

## 開發狀態

目前已完成：

- 專案初始化
- 技術選型
- 系統架構設計
- Domain 架構設計
- 權限架構設計
- Django Backend 初始化

目前主要開發項目：

- Parts Module
- Parts Query API
- Authentication
- Permission Management

---

## License

目前僅作為個人 Demo 與架構研究用途。