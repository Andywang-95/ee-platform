# EE Platform Architecture

## 1. 專案定位

EE Platform 是公司內部使用的工程工具平台，提供 EE 相關資料與工具的集中入口。

平台主要負責：

- 零件資料查詢與維護
- BOM 相關工具
- PCB 相關工具
- 檔案解析與轉換
- 電路與零件相關檢查
- 其他 EE 工程工具

平台採模組化設計，各項主要功能以獨立 Domain / Application 管理。

---

## 2. 整體技術架構

專案採前後端分離架構。

### Frontend

- Vue
- TypeScript

### Backend

- Python
- Django
- Django REST Framework
- drf-spectacular

### Database

- Microsoft SQL Server
- 透過 `mssql-django` 與 `pyodbc` 連線

### Web Server

- Nginx

### Container

- Docker
- Docker Compose

---

## 3. Repository 架構

Frontend 與 Backend 為兩個獨立的 Application，但使用同一個 Git Repository 管理。

目前根目錄結構：

```text
ee-platform/
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── ...
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── ...
│
├── docs/
│   └── ...
│
├── compose.yml
├── Taskfile.yml
├── README.md
└── ...
```

Frontend 與 Backend 分別維護自己的執行環境、Dependency 與 Docker Image。

根目錄的 Docker Compose 負責將各個 Service 組合成完整的 EE Platform。

---

## 4. Container 架構

各 Application 自己負責 Dockerfile。

### Backend

```text
backend/
└── Dockerfile
```

Backend Dockerfile 負責：

- Python Runtime
- uv / Python dependencies
- Django
- Backend Application

### Frontend

```text
frontend/
└── Dockerfile
```

Frontend Dockerfile 負責：

- Node.js Runtime
- Frontend dependencies
- Vue Application
- Frontend build

### Compose

根目錄的 `compose.yml` 負責：

- 定義各個 Service
- 建立 Service 之間的網路
- 設定 Environment Variables
- 管理 Volume
- 管理 Port
- 組合 Frontend、Backend、Nginx 以及未來其他服務

概念：

```text
compose.yml
    │
    ├── frontend
    │      └── frontend/Dockerfile
    │
    ├── backend
    │      └── backend/Dockerfile
    │
    └── nginx
```

未來若加入非同步工作系統，也可以透過 Compose 增加：

```text
    ├── worker
    └── queue
```

---

## 5. Backend 架構

Backend 使用 Django + Django REST Framework。

Backend 採 Domain-oriented Application 架構。

概念：

```text
backend/
├── config/
│
├── apps/
│   ├── parts/
│   ├── bom/
│   ├── pcb/
│   └── ...
│
├── manage.py
├── pyproject.toml
└── uv.lock
```

每個 Django App 對應一個主要的業務 Domain。

例如：

- `parts`：零件資料與零件相關功能
- `bom`：BOM 相關功能
- `pcb`：PCB 相關功能

App 之間應保持清楚的責任邊界。

---

## 6. Django App 結構原則

Django App 依照實際需求建立檔案，不要求每個 App 一開始就建立完整結構。

常見結構：

```text
apps/<domain>/
├── models.py
├── managers.py
├── serializers.py
├── services.py
├── validators.py
├── views.py
├── urls.py
└── ...
```

各檔案的主要責任：

### models

負責資料模型與 Database Object 的 Application-level representation。

### managers / querysets

負責可重用的資料查詢邏輯。

### serializers / schemas

負責 API 的資料輸入與輸出結構，以及相關 validation。

### services

負責具有業務意義的操作流程。

### validators

負責 Domain-specific 的資料與規則驗證。

### views

負責 HTTP / API Layer。

---

## 7. API 架構

Frontend 不直接存取 Database。

所有 Frontend 與 Backend 的資料交換都透過 Backend API。

```text
Vue
 │
 │ HTTP / HTTPS
 ▼
Django REST Framework
 │
 ▼
Application Domain
 │
 ▼
Database / Service
```

API 使用 RESTful API 作為主要通訊方式。

API 文件使用 `drf-spectacular` 根據 Django REST Framework 的 API Schema 自動產生。

API Schema 應盡可能由程式碼產生，而不是另外維護一份與實際 API 分離的手寫文件。

---

## 8. Frontend 架構

Frontend 使用 Vue + TypeScript。

Frontend 主要負責：

- 使用者介面
- 導覽
- 表單
- 資料表
- 搜尋與篩選
- API 呼叫
- 工具操作介面
- Job 狀態與進度呈現

Frontend 不直接處理 Database。

概念：

```text
Vue Application
      │
      ▼
API Client
      │
      ▼
Django REST API
```

Frontend 應將不同主要功能以清楚的 Feature / Domain 進行組織，使 Parts、BOM、PCB 等功能可以獨立演進。

---

## 9. Database 架構

平台目前使用既有的 Microsoft SQL Server。

Database 中已存在由其他系統使用的資料表與 View，因此 EE Platform 必須考慮既有系統的相容性。

概念：

```text
                    ┌── CIS
                    │
MSSQL Database ─────┼── EE Platform
                    │
                    └── Other Systems
```

Database 是共享資源。

因此 EE Platform 不應任意修改既有 Database Schema。

---

## 10. Django Migration 原則

Existing Database Object 與 EE Platform 自己建立的 Database Object 分開管理。

### Existing Database

既有的 Table / View 不由 Django Migration 管理。

對應 Django Model 時，依需求使用：

```python
class Meta:
    managed = False
```

Django 主要負責對既有資料進行存取，而不是控制其 Schema Lifecycle。

### EE Platform 自有資料表

如果未來 EE Platform 需要建立自己的資料表，例如：

- Job
- Change Request
- Approval
- Application Audit
- Tool Execution Record

則可以由 Django Model + Migration 管理。

因此：

```text
Existing Database Objects
    → Existing Database 管理

EE Platform Owned Tables
    → Django Migration 管理
```

---

## 11. Authentication

平台的使用者身分應整合公司既有的 Windows / Active Directory 身分系統。

使用者使用公司的 Windows Account 登入公司環境。

Application 不應要求使用者另外建立一組完全獨立的公司帳號。

實際 Web Authentication Mechanism 依正式部署環境決定。

---

## 12. Authorization

Authentication 與 Authorization 分離。

Windows / AD 主要負責確認：

> 「這個人是誰？」

EE Platform Application Authorization 負責確認：

> 「這個人可以做什麼？」

Application 權限可以依功能管理，例如：

```text
User
├── Parts Read
├── Parts Edit
├── BOM Access
├── PCB Tools
├── Approval
└── Administration
```

不同 Domain 可以擁有不同的權限需求。

Application Permission 不應直接等同於 MSSQL Database Permission。

---

## 13. Web Server 與 Reverse Proxy

正式環境使用 Nginx 作為 Web Server / Reverse Proxy。

使用者透過單一內部 URL 存取平台。

概念：

```text
User Browser
      │
      │ HTTPS
      ▼
    Nginx
      │
      ├──────────────► Frontend
      │
      └── /api/ ─────► Backend
```

Frontend 與 Backend 不需要直接暴露給使用者。

Nginx 負責：

- 接收使用者 HTTP / HTTPS Request
- 提供 Frontend
- 將 `/api/` Request 轉發至 Backend
- 統一對外入口
- 未來可處理其他 Reverse Proxy 需求

---

## 14. CORS

正式環境以單一網域 / Origin 對外提供服務。

例如：

```text
https://ee-platform.company.internal
```

Frontend：

```text
https://ee-platform.company.internal
```

API：

```text
https://ee-platform.company.internal/api/
```

由於 Frontend 與 API 可以使用同一 Origin，因此正式環境不應以跨 Origin 架構作為主要設計。

開發環境可以因為 Frontend Development Server 與 Django Development Server 使用不同 Port，而需要適當的 CORS / Proxy 設定。

---

## 15. File-based Tools

EE Platform 不只提供 CRUD / Database 功能，也會提供大量以檔案作為 Input / Output 的工程工具。

典型流程：

```text
User
  │
  ▼
Upload / Select File
  │
  ▼
Backend Tool
  │
  ▼
Process
  │
  ▼
Generated Result
  │
  ▼
User Download / View
```

例如：

- BOM 比較
- BOM 分析
- PCB 資料解析
- PCB Check
- 檔案轉換
- 電路相關檢查
- 零件相關檢查

各工具應保持獨立的 Domain / Service 邏輯，避免將所有工具集中在單一 Application 中。

---

## 16. 非同步工作

部分 EE 工程工具可能需要處理大量資料或執行較長時間的工作。

例如：

- 大型 PCB
- 大量 Net
- 大量 Component
- 多項 Electrical Check
- 多項 Rule Check
- BOM 大量比較

因此平台的長期架構支援非同步 Job Processing。

概念：

```text
User
  │
  ▼
Create Job
  │
  ▼
Job Queue / Processing System
  │
  ▼
Worker
  │
  ├── Check A
  ├── Check B
  ├── Check C
  └── Check D
  │
  ▼
Job Completed
```

Frontend 未來可以顯示：

```text
PCB Check

██████████████░░░░░░ 70%

✓ Component Check
✓ Net Check
✓ Footprint Check
⟳ Electrical Check
○ Additional Check
```

每個檢查項目可以具有自己的執行狀態。

目前只定義非同步工作的架構方向，不固定 Job Queue、Worker、Message Broker 或即時通訊所使用的具體技術。

具體技術於實際需要建立非同步處理功能時決定。

---

## 17. Tool Job 的長期方向

未來需要將長時間執行的工具視為 Job。

概念：

```text
Job
├── id
├── type
├── status
├── progress
├── created_by
├── created_at
├── started_at
└── completed_at
```

Job 可以進一步包含多個 Task / Check：

```text
Job
├── Task A
├── Task B
├── Task C
└── Task D
```

每個 Task 可以具有：

```text
pending
running
completed
failed
```

等狀態。

具體資料模型與即時更新機制於實作階段再定義。

---

## 18. Application 與 Database 的責任

Application Layer：

- 商業邏輯
- 權限
- Validation
- API
- 工具執行
- Job 管理
- UI 所需資料結構

Database Layer：

- 資料儲存
- Existing Table
- Existing View
- Database-level Constraint
- 既有系統所需的資料結構

兩者應保持責任分離。

---

## 19. 共通開發原則

### 19.1 Domain Separation

不同業務功能應保持清楚的 Domain 邊界。

### 19.2 API First

Frontend 與 Backend 透過 API 溝通。

### 19.3 Database Compatibility

Existing Database Schema 不應因 Application 開發而任意改動。

### 19.4 Configuration over Hardcoding

需要由不同零件類型、工具或 Domain 使用的設定，應優先透過 Configuration 管理，而不是大量散落於程式碼。

### 19.5 Backend Validation

Frontend Validation 不能取代 Backend Validation。

所有重要資料與權限檢查都必須在 Backend 執行。

### 19.6 Containerized Environment

Application 的執行環境應透過 Docker 定義。

Frontend 與 Backend 各自管理 Dockerfile。

Docker Compose 負責整合各 Service。

### 19.7 Automated API Documentation

API Schema 與 API Documentation 應盡可能由程式碼自動產生，避免維護獨立且容易過期的手寫 API 文件。

---

## 20. 目前主要架構

```text
                         User
                           │
                           ▼
                      ┌─────────┐
                      │  Nginx  │
                      └────┬────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌──────────────┐          ┌──────────────┐
      │   Frontend   │          │   Backend    │
      │ Vue + TS     │          │ Django + DRF │
      └──────────────┘          └───────┬──────┘
                                        │
                           ┌────────────┼────────────┐
                           │            │            │
                           ▼            ▼            ▼
                        Parts         BOM          PCB
                           │            │            │
                           └────────────┼────────────┘
                                        │
                                        ▼
                                   MSSQL Database
                                        │
                                        ▲
                                        │
                                      CIS
```

未來非同步工作：

```text
                    Backend
                       │
                       ▼
                 Async Job System
                       │
                ┌──────┴──────┐
                ▼             ▼
             Worker        Worker
                │             │
                ▼             ▼
             PCB Check      BOM Check
```

---

## 21. Repository 責任邊界

```text
ee-platform/
│
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── Django Application
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── Vue Application
│
├── docs/
│   └── Architecture / Domain Documentation
│
├── compose.yml
│   └── Container / Service Integration
│
├── Taskfile.yml
│   └── Development Commands
│
└── README.md
    └── Project Introduction
```

Frontend 與 Backend 的 dependency、runtime 與 Dockerfile 分別管理。

Root-level configuration 主要負責跨 Application 的整合。

---

## 22. 架構目標

EE Platform 的整體架構目標是：

```text
                    EE Platform
                         │
        ┌────────────────┼────────────────┐
        │                │                │
       Parts            BOM              PCB
        │                │                │
        └────────────────┼────────────────┘
                         │
                    Shared Platform
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Authentication     Authorization     Job System
        │                │                │
        └────────────────┼────────────────┘
                         │
                    Existing MSSQL
```

平台應能在不破壞既有 CIS 與 Database 架構的前提下，逐步加入新的 EE 工程工具與資料管理功能。

初期以 Parts Domain 作為第一個主要功能進行開發，後續再依相同的平台架構擴充 BOM、PCB、檢查工具以及其他 EE 功能。