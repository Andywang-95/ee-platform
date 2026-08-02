# ADR-0006: Authentication 與 Authorization 設計

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

公司環境使用：

- Windows Account
- Active Directory
- SQL Server Windows Authentication

需要設計 EE Platform 使用者身份與權限管理方式。

---

## 決策

採用：

```
Windows AD

+

Platform Permission Layer
```

---

## 身份驗證

AD 負責：

> 使用者是誰

Platform 不建立獨立帳號系統。

---

## 權限管理

Platform 負責：

> 使用者可以做什麼

建立：

- User
- Group
- Role
- Permission

管理應用程式功能權限。

---

## 理由

保留既有 CIS 使用方式。

SQL Server 權限仍可維持。

Platform 可以額外控制：

- 查詢權限
- 編輯權限
- 工具使用權限

---

## 設計原則

身份與權限分離：

```
Authentication

=
Who are you?


Authorization

=
What can you do?
```

---

## 後續影響

未來權限調整應優先透過 Platform 管理。

避免直接依賴 Database 權限作為應用程式控制方式。