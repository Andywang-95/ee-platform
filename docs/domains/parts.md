# Parts App Design

## 1. Domain 定位

Parts App 負責管理 EE Platform 中的零件資料相關功能。

主要責任：

- 零件資料查詢
- 零件分類管理
- 零件欄位呈現
- 零件資料維護
- 零件相關規則驗證

Parts App 是 EE Platform 初期主要開發的 Domain。

---

## 2. Database 架構

目前零件資料來源為既有 Microsoft SQL Server Database。

Database 中已有一張主要零件資料表，包含所有種類零件的完整欄位。

概念：

```text
Existing MSSQL

Parts Table
│
├── R
├── C
├── L
├── IC
└── Other Parts
```

目前資料設計：

- 所有零件共用同一張 Table
- 欄位數量約 130+
- 不同零件類型透過欄位區分

既有 CIS 系統亦使用此資料來源。

因此：

- 不重新設計 Database Schema
- 不任意拆分既有資料表
- Django 主要負責 Application Layer 的資料存取與管理

---

## 3. Part Type 定義

Part Type 的來源為 Database 中既有欄位。

目前使用：

```text
table_name
```

作為零件分類依據。

例如：

```text
table_name

R
    → Resistor

C
    → Capacitor

L
    → Inductor

IC
    → Integrated Circuit
```

Database 中的 `table_name` 是 Part Type 的 Source of Truth。

Application Layer 不建立另一套獨立的零件分類資料。

---

## 4. Django Model 設計

Parts App 使用單一主要 Model 對應既有 Parts Table。

概念：

```text
Part Model

        │
        ▼

Existing MSSQL Parts Table
```

Model 負責：

- 對應 Database 欄位
- 提供資料存取介面
- 作為其他 Application Layer 的資料來源

概念：

```python
class Part(models.Model):
    ...

    class Meta:
        managed = False
```

由於 Database 已由既有系統管理，因此不使用 Django Migration 控制此 Table。

---

## 5. Proxy Model 設計

不同種類零件使用 Proxy Model 表示。

Proxy Model 不建立新的 Database Table。

用途：

- 提供不同零件類型的語意化 Model
- 封裝不同零件類型的操作方式
- 提供更清楚的 Application Interface

概念：

```text
                Part

                 │

     ┌───────────┼───────────┐

     ▼           ▼           ▼

 Resistor    Capacitor    Inductor

 Proxy         Proxy        Proxy
```

例如：

```python
class Resistor(Part):

    class Meta:
        proxy = True
```

Proxy Model 最終仍然操作同一張 Parts Table。

---

## 6. Manager / QuerySet 設計

不同 Part Type 可以透過 Manager 或 QuerySet 封裝查詢邏輯。

例如：

```text
Resistor.objects.all()
```

代表：

```sql
SELECT *
FROM Parts
WHERE table_name = 'R'
```

概念：

```text
Part Manager

        │

        ├── Resistor Manager
        │
        ├── Capacitor Manager
        │
        └── Other Part Manager
```

Manager 負責：

- 常用 Query
- Part Type 篩選
- 共用查詢邏輯

避免將查詢條件散落於 API 或 Frontend。

---

## 7. Part Configuration

不同種類零件雖然共用 Database Table，但前端呈現與操作需求不同。

因此建立 Part Configuration 管理不同 Part Type 的設定。

Configuration 負責：

- 顯示欄位
- 可搜尋欄位
- Filter 定義
- Part Type 相關設定

概念：

```text
Part Configuration

        │

        ├── Resistor Config
        │
        ├── Capacitor Config
        │
        └── IC Config
```

例如：

```text
Resistor

Display Fields

- Part Number
- Resistance
- Tolerance
- Power
- Package


Filter Fields

- Part Number
- Resistance
- Manufacturer
```

Frontend 不直接定義欄位規則。

Frontend 根據 Backend 提供的 Configuration 動態呈現。

---

## 8. Serializer / Schema 設計

Schema 用於定義 API 層資料格式。

Schema 不代表 Database 結構。

責任：

- 定義 API Response 格式
- 定義 API Request 格式
- 控制資料暴露範圍
- 提供 API Documentation 所需資訊

概念：

```text
Database Model

        │

        ▼

Serializer / Schema

        │

        ▼

Frontend API Data
```

例如：

Database：

```text
130+ columns
```

API Response：

```json
{
    "part_number": "...",
    "description": "...",
    "package": "..."
}
```

API 不需要直接暴露完整 Database 欄位。

---

## 9. Read / Query Flow

初期主要功能為零件查詢。

流程：

```text
User

 │

 ▼

Frontend

 │

 ▼

Parts API

 │

 ▼

Part Service

 │

 ▼

Manager / QuerySet

 │

 ▼

Part Model

 │

 ▼

MSSQL Database
```

查詢流程由 Backend 控制。

Frontend 不直接組 Database Query。

---

## 10. Filter 與 Search 設計

零件查詢支援：

- Part Type 選擇
- 關鍵字搜尋
- 欄位 Filter

Filter 定義由 Backend 管理。

概念：

```text
Frontend

選擇：

Resistor

        │

        ▼

Backend

讀取 Resistor Configuration

        │

        ▼

建立 Query

        │

        ▼

Database
```

初期可以允許較廣泛的搜尋欄位。

後續可依使用需求限制或優化。

---

## 11. Validation 設計

Validation 負責檢查資料是否符合零件規則。

例如：

- 欄位格式
- 欄位必要性
- 零件規格限制

Validation 與 Database Model 分離。

概念：

```text
Input Data

    │

    ▼

Validator

    │

    ▼

Valid Data

    │

    ▼

Service
```

---

## 12. Service Layer 設計

Service 負責具有業務意義的操作。

避免將複雜邏輯放入：

- View
- Serializer
- Model

概念：

```text
API View

    │

    ▼

Service

    │

    ▼

Model / Database
```

未來資料維護功能：

```text
User

 │

 ▼

Edit Request

 │

 ▼

Part Service

 │

 ▼

Validation

 │

 ▼

Database Update
```

Service 作為未來新增：

- 編輯
- 批次修改
- 提交
- Audit

等功能的主要入口。

---

## 13. Data Maintenance Direction

Parts App 未來支援零件資料維護。

預期流程：

```text
User

 │

 ▼

Frontend Edit

 │

 ▼

API

 │

 ▼

Schema Validation

 │

 ▼

Business Validation

 │

 ▼

Part Service

 │

 ▼

Database Update
```

維護流程需考量：

- 權限控制
- 修改驗證
- 修改紀錄
- 批次提交

詳細流程於實作階段定義。

---

## 14. Audit Log Direction

目前 Database 已有 Trigger-based Log。

未來 Application Layer 建立維護功能後：

Application 可以負責：

- 使用者資訊
- 修改內容
- 修改原因
- 提交流程

Database Log 與 Application Audit 可以依需求並存或逐步整合。

---

## 15. Parts App 初始資料夾結構

建議：

```text
apps/
└── parts/

    ├── models.py
    │
    ├── managers.py
    │
    ├── proxies.py
    │
    ├── config.py
    │
    ├── serializers.py
    │
    ├── validators.py
    │
    ├── services.py
    │
    ├── views.py
    │
    ├── urls.py
    │
    └── ...
```

責任：

```text
models.py

Database Model


proxies.py

Part Type Proxy Models


managers.py

Query Logic


config.py

Part Type Configuration


serializers.py

API Schema


validators.py

Data Validation


services.py

Business Logic


views.py

API Interface
```

---

## 16. Parts App 架構總覽

```text
                    Parts App

                        │

                    Part Model

                        │

              Existing MSSQL Table


                        │

        ┌───────────────┴───────────────┐

        ▼                               ▼

  Proxy Models                  Part Configuration

        │                               │

        │                               ├── Display Fields
        │                               ├── Filter Fields
        │                               └── Rules

        │

        ▼

   Managers / QuerySets

                        │

                        ▼

                    Services

                        │

                        ▼

              Serializers / Schema

                        │

                        ▼

                    API

                        │

                        ▼

                  Frontend
```

---

## 17. 設計原則

### Database Compatibility

保持與既有 CIS Database 相容。

### Single Source of Truth

Database 中的零件資料為主要來源。

### Separation of Responsibility

Model、Configuration、Schema、Service 各自負責不同層級。

### Dynamic Presentation

零件欄位呈現由 Backend Configuration 控制。

### API First

Frontend 不直接依賴 Database 結構。

### Extensible

未來可加入：

- 零件維護
- 批次修改
- Audit
- BOM 使用分析
- 零件規則檢查

而不需要重新設計核心架構。