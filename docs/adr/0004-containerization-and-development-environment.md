# ADR-0004: Container 化與開發環境設計

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

專案包含多種技術環境：

- Python
- Node.js
- Database
- 未來可能加入 Cache 與 Background Worker

需要建立一致的開發與部署方式。

---

## 決策

採用：

- Docker
- Docker Compose

Frontend 與 Backend 分別維護 Dockerfile。

---

## 架構

```
ee-platform/

├── backend/
│   └── Dockerfile
│
├── frontend/
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## 理由

### 開發環境一致

避免不同開發者：

- Python 版本不同
- Node 版本不同
- 套件版本不同

造成環境問題。

---

### 支援未來部署

同一套設定可延伸至：

- 測試環境
- 公司內部 Server
- Production Environment

---

## 開發工具

Backend：

- uv

Frontend：

- Node.js ecosystem

專案操作：

- Taskfile

---

## 後續影響

所有新增服務需透過 Docker Compose 管理。

例如：

未來可能加入：

- Redis
- Background Worker
- Monitoring Service