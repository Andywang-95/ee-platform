# EE Platform

![Status](https://img.shields.io/badge/status-development-blue)
![Python](https://img.shields.io/badge/python-3.13+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-5.2-092E20?logo=django)
<!-- ![Vue](https://img.shields.io/badge/vue-3.x-42B883?logo=vuedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-5.x-3178C6?logo=typescript&logoColor=white) -->

EE Platform 是一個以 **Django + Django REST Framework + Vue.js** 為基礎開發的企業內部工程平台 Demo。

本專案主要目標是提供一個可維護、可擴充的系統架構，用於管理與查詢電子零件（Parts）資料，並逐步整合既有工具，建立統一的工程平台。

目前專案仍處於初期開發階段，所有設計皆以 **可維護性（Maintainability）**、**可擴充性（Scalability）** 與 **企業級開發流程（Enterprise Development Workflow）** 為主要考量。

---

## 🚧 Project Status

目前專案仍在積極開發中。

目前主要開發重點：

- Backend Architecture
- Parts Query Module
- Authentication & Authorization
- Permission Management
- Database Integration

---

## ✨ Features

目前規劃包含：

- 零件資料查詢（Parts Query）
- 零件資料維護（Parts Management）
- 權限管理（Role-Based Access Control）
- AD 使用者整合
- RESTful API
- OpenAPI / Swagger 文件
- PCB 檢查流程（規劃中）

---

## 🛠 Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- drf-spectacular
- Microsoft SQL Server

### Frontend

- Vue.js
- TypeScript
- Vite

### Development

- uv
- Ruff
- Docker
- Docker Compose

---

## 📁 Project Structure

```text
.
├── backend/
│   ├── apps/
│   ├── config/
│   ├── manage.py
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   └── README.md
│
├── docs/
│   ├── adr/
│   ├── architecture.md
│   ├── database.md
│   ├── development.md
│   └── domains/
│
└── README.md
```

---

## 📖 Documentation

所有設計文件皆集中於 `docs/`。

目前包含：

- 系統架構（Architecture）
- Database Design
- Development Guideline
- Domain Design
- Authentication Design
- Architecture Decision Records（ADR）

詳細內容請參閱：

```text
docs/
```

---

## 🚀 Getting Started

### Backend

```bash
cd backend

uv sync

uv run python manage.py runserver
```

### Frontend

目前 Frontend 尚未開始建置。

---

## 🗺 Roadmap

### ✅ Completed

- 專案初始化
- 技術選型
- 系統架構設計
- Domain 架構設計
- Authentication 架構設計
- 權限模型設計
- Django Backend 初始化

### 🚧 In Progress

- Parts Module
- Parts Query API
- Database Integration

### ⏳ Planned

- Parts Edit
- Authentication
- Permission Management
- PCB Check
- Dashboard
- Docker Deployment
- CI/CD

---

## 🤝 Development

Backend 與 Frontend 採獨立開發模式。

各自的開發方式請參閱：

- `backend/README.md`
- `frontend/README.md`

---

## 📄 License

本專案目前作為個人學習、架構驗證與企業系統設計 Demo 使用，尚未授權為開源專案。