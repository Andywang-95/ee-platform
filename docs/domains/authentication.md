# Authentication & Authorization Design

# 目的

EE Platform 不自行管理使用者帳號與密碼。

使用者身份（Authentication）完全由公司 Active Directory（AD）提供，Platform 僅負責系統內功能權限（Authorization）管理。

Platform 的權限系統必須具備以下特性：

- 不依賴 Django User。
- 不依賴 SQL Server Permission。
- 支援 AD Group 與 User 混合授權。
- 支援未來功能持續擴充。
- 權限管理最終可透過 Platform UI 維護。

---

# 設計原則

## Authentication（身份驗證）

身份來源：

- Windows Active Directory
- Windows SSO（Single Sign-On）

Platform 不保存：

- Password
- Email
- Display Name
- Department

上述資訊皆以 AD 為唯一來源。

Platform 每次登入僅取得：

- Username
- AD Group

作為後續權限計算依據。

---

## Authorization（功能授權）

Platform 自行管理所有功能權限。

權限來源包含兩部分：

1. AD Group
2. AD User

兩者取得的 Role 將進行聯集（Union）。

例如：

AD：

```
DOMAIN\Kevin
```

所屬 Group：

- EE_RD
- Project_A

Platform：

Group：

```
EE_RD
```

↓

```
viewer
```

User：

```
DOMAIN\Kevin
```

↓

```
editor
```

最終取得：

```
viewer
editor
```

最後再將所有 Role 所擁有的 Permission 合併。

因此：

Kevin 最終擁有：

- part.view
- part.edit
- bom.compare
- ...

---

# Permission Model

採用 RBAC（Role-Based Access Control）。

架構如下：

```
Windows AD
        │
        ▼
 AD User / AD Group
        │
        ▼
Platform Principal
        │
        ▼
Platform Role
        │
        ▼
Platform Permission
```

其中：

Principal 可以是：

- AD User
- AD Group

因此同一套授權機制即可同時支援：

- 部門授權
- 個人授權

---

# Database Design

共建立五張資料表。

---

## platform_permission

定義系統所有可使用的功能。

例如：

| code | 功能 |
|------|------|
| part.view | 查看零件 |
| part.edit | 編輯零件 |
| part.approve | 核准修改 |
| bom.compare | BOM 比較 |
| pcb.check | PCB Check |

建議欄位：

| 欄位 | 說明 |
|------|------|
| id | PK |
| code | UNIQUE，程式唯一識別 |
| name | 顯示名稱 |
| description | 說明 |
| created_at | 建立時間 |
| updated_at | 更新時間 |

說明：

- code 永遠保持穩定。
- API、Frontend、Backend 一律使用 code 判斷權限。
- Database 關聯使用 id。

---

## platform_role

定義角色。

Role 為 Permission 的集合。

例如：

| code | 名稱 |
|------|------|
| viewer | 一般使用者 |
| editor | 零件維護 |
| approver | 審核者 |
| admin | 系統管理員 |

建議欄位：

| 欄位 | 說明 |
|------|------|
| id | PK |
| code | UNIQUE |
| name | 名稱 |
| description | 說明 |
| created_at | 建立時間 |
| updated_at | 更新時間 |

---

## platform_role_permission

Role 與 Permission 的對應表。

Many-to-Many。

建議欄位：

| 欄位 | 說明 |
|------|------|
| id | PK |
| role_id | FK → platform_role.id |
| permission_id | FK → platform_permission.id |

範例：

```
viewer
    ↓
part.view
bom.compare

editor
    ↓
part.view
part.edit
bom.compare
```

新增功能時：

只需新增：

Permission

再把它加入：

Role

即可立即套用到所有使用者。

---

## platform_principal_role

Principal 與 Role 的對應。

Principal 可以是：

- USER
- GROUP

建議欄位：

| 欄位 | 說明 |
|------|------|
| id | PK |
| principal_type | USER / GROUP |
| principal_name | AD Username 或 AD Group Name |
| role_id | FK → platform_role.id |
| expires_at | 到期時間，可為 NULL |
| created_by | 建立者 |
| created_at | 建立時間 |
| updated_at | 更新時間 |

範例：

| principal_type | principal_name | role |
|----------------|---------------|------|
| GROUP | EE_RD | viewer |
| GROUP | EE_ME | viewer |
| USER | DOMAIN\\Kevin | editor |
| USER | DOMAIN\\Amy | approver |

登入後：

Group Role

+

User Role

↓

Union

↓

Permission

---

## platform_feature

功能模組定義。

目的：

方便管理首頁工具入口與功能分類。

建議欄位：

| 欄位 | 說明 |
|------|------|
| id | PK |
| code | UNIQUE |
| name | 模組名稱 |
| icon | Icon 名稱（預留） |
| description | 說明 |
| sort_order | 排序 |
| created_at | 建立時間 |
| updated_at | 更新時間 |

例如：

| code | 名稱 |
|------|------|
| part | 零件管理 |
| bom | BOM 工具 |
| pcb | PCB 工具 |
| system | 系統管理 |

未來 Permission 可依 Feature 分類管理。

例如：

```
part.view
```

↓

```
part
```

方便 Frontend 動態產生首頁工具。

---

# Login Flow

```
Windows Login
        │
        ▼
Windows SSO
        │
        ▼
取得：

- Username
- AD Groups

        │
        ▼

查詢：

platform_principal_role

        │
        ▼

取得：

Group Roles
+
User Roles

        │
        ▼

Role

        │
        ▼

Permission

        │
        ▼

Permission Set

        │
        ▼

建立 Session
```

---

# Session

登入時：

僅查詢一次權限。

登入成功後：

Permission Set 保存於 Session。

例如：

```
{
    "username": "DOMAIN\\Kevin",
    "permissions": [
        "part.view",
        "part.edit",
        "bom.compare"
    ]
}
```

之後每個 API Request：

不重新查詢資料庫。

僅檢查：

```
request.user.permissions
```

即可完成授權。

未來若需要：

可增加：

- Session Refresh
- Permission Version
- Redis Cache

目前 v1 不實作。

---

# Audit Log

所有修改皆須記錄：

- Username（AD）
- Action
- Object
- Old Value
- New Value
- Timestamp

Audit Log 由 Platform 負責寫入。

不依賴 SQL Trigger。

---

# 與 SQL Server 的關係

Platform 與 CIS 為兩套不同系統。

## CIS

維持現況：

- Windows Authentication
- SQL Server Permission
- Reader / Editor 權限

供既有 CIS 使用。

不進行任何修改。

---

## Platform

Platform 使用專用 Database Account 存取 SQL Server。

所有使用者：

```
User

↓

Platform

↓

Application Account

↓

Database
```

終端使用者不直接連線 SQL Server。

所有修改權限皆由 Platform 控制。

因此：

Platform 將成為唯一 Web 編輯入口。

未來可逐步取消一般使用者直接修改 Database 的需求。

---

# Future Plan

未來新增：

「系統管理 → 權限管理」

提供管理者透過 Web UI 維護：

- Permission
- Role
- Role Permission
- User Role
- Group Role
- Feature

所有權限管理皆可透過 Platform 完成。

不再需要直接修改 Database。

---

# 設計原則總結

- AD 負責身份（Authentication）。
- Platform 負責授權（Authorization）。
- SQL Server 僅負責資料存取（Data Access）。
- Role 為 Permission 的集合。
- Permission 為系統最小授權單位。
- Group 提供預設權限。
- User 提供額外權限。
- 最終權限為 Group 與 User 的聯集。
- Database 使用 id 作為 FK。
- 程式使用 code 作為唯一識別。
- 所有修改皆透過 Platform 完成。
- 所有操作皆可追蹤 Audit Log。