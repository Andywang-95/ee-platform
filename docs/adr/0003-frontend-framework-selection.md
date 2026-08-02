# ADR-0003: Frontend Framework 選型

## 狀態

Accepted

## 日期

2026-08-02

---

## 背景

EE Platform 前端主要需求：

- 工程資料瀏覽
- 大量表格操作
- 動態欄位
- 表單維護
- 工具入口管理

需要選擇適合企業內部系統的 Frontend Framework。

---

## 決策

採用：

- Vue 3
- TypeScript
- Vite

---

## 理由

### 適合企業內部系統

Vue 提供：

- 清楚的元件結構
- 較低學習成本
- 穩定生態

---

### 適合資料導向應用

平台主要不是內容型網站，而是：

- Table
- Form
- Dashboard
- Engineering Tool UI

Vue 可以有效處理此類需求。

---

## 考慮過的替代方案

### React

React 能力完整且生態成熟。

未採用原因：

- 架構選擇自由度較高
- 需要更多額外決策
- 對企業內部工具而言，Vue 維護成本較低

---

## 後續影響

Frontend 開發需遵循：

- TypeScript 優先
- Component 化
- API 與 UI 分離
- 不直接處理 Backend Business Logic