# ADR-0001: 專案結構設計決策

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

EE Platform 是一個預期長期維護與持續擴充的企業內部工程平台。

專案包含：

- Backend API Server
- Frontend Web Application
- 文件
- 開發工具
- 部署設定

需要決定 Repository 與專案結構管理方式。

---

## 決策

採用 Monorepo 架構。

Frontend 與 Backend 分別維護自己的專案目錄，但共用同一個 Repository。

目前結構：

```
ee-platform/

├── backend/
├── frontend/
├── docs/
├── Taskfile.yml
└── README.md
```

---

## 理由

採用此架構原因：

### 前後端技術環境不同

Backend：

- Python
- Django
- uv

Frontend：

- Vue
- TypeScript
- Node.js

分離管理可以避免環境互相影響。

---

### 保留完整產品上下文

Frontend 與 Backend 雖然獨立，但屬於同一個產品。

放在同一 Repository 可以：

- 同時檢視完整架構
- 管理版本關聯
- 簡化部署流程

---

### 支援容器化部署

Frontend 與 Backend 可以各自維護：

```
frontend/Dockerfile

backend/Dockerfile
```

並由根目錄統一管理：

```
docker-compose.yml
```

---

## 考慮過的替代方案

### 多 Repository

Frontend 與 Backend 分開管理。

缺點：

- 版本管理較複雜
- 文件分散
- 部署流程較難整合

---

### Django Full Stack

使用 Django Template 完成前後端。

缺點：

- 不符合未來大型 Web Application 需求
- 前端互動能力受限
- 不利於建立多工具入口平台

---

## 後續影響

所有新增模組需遵循：

- Backend 功能放置於 backend
- Frontend 功能放置於 frontend
- 架構文件放置於 docs
- 重大設計決策建立 ADR