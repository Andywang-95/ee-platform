# ADR-0005: Parts Data Model 設計

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

Parts Database 原始資料來源為單一 Master Table。

不同零件類型：

- Resistor
- Capacitor
- Inductor
- IC
- Connector

透過分類欄位區分。

需要決定 Django Model 設計方式。

---

## 決策

採用：

```
Single Master Table

+

Django Model

+

Proxy Model

+

Service Layer

+

Schema Definition
```

---

## 理由

不依照零件類型拆成多張 Table。

原因：

- 原始資料來源為同一張 Table
- 避免資料重複
- 保留與既有 CIS 架構一致

---

## 設計方向

### Model

負責：

- Database Mapping
- 基礎資料結構

---

### Proxy Model

負責：

- 不同零件類型行為差異
- 客製化 Manager
- 類型專屬操作

---

### Service Layer

負責：

- 查詢邏輯
- 商業規則
- 資料處理流程

---

### Schema

負責：

- API Response
- 欄位控制
- 前端動態顯示

---

## 後續影響

Parts 模組新增功能時：

需優先考慮：

- 是否屬於資料模型
- 是否屬於商業邏輯
- 是否屬於 UI 呈現

避免將所有邏輯集中於 Model。