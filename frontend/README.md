# Frontend

React 19 + TypeScript，使用 Vite+ 作為工具鏈。

## 執行

前端在 container 內執行，從 repo 根目錄操作：

```bash
task up              # 啟動，網址 http://localhost:5173
task lint-frontend   # lint、型別檢查、格式檢查
task format-frontend # 自動格式化
task test-frontend   # 測試
```

要在 container 內直接執行 Vite+ 的指令：

```bash
docker compose run --rm frontend vp <指令>
```

| 指令          | 用途                                          |
| ------------- | --------------------------------------------- |
| `vp dev`      | 開發伺服器                                    |
| `vp check`    | lint、型別檢查、格式檢查，加 `--fix` 自動修正 |
| `vp test run` | 執行測試一次                                  |
| `vp build`    | 正式建置，輸出到 `dist/`                      |

後端 API 有變動時，在根目錄執行 `task gen-api` 重新產生 `src/api/schema.d.ts`。

## 結構

```text
frontend/
├── src/
│   ├── main.tsx        進入點
│   ├── App.tsx         版面
│   ├── api/
│   │   ├── client.ts   呼叫後端 API 的共用函式
│   │   └── schema.d.ts 由後端 OpenAPI 文件產生的型別，不手動修改
│   └── parts/          零件查詢
│       ├── api.ts      零件 API 的函式與型別
│       ├── PartsPage.tsx
│       ├── PartDetailDrawer.tsx
│       └── RemarkRow.tsx
├── index.html
├── vite.config.ts      Vite+ 設定：開發伺服器、lint、格式化
├── Dockerfile          開發用 image
└── package.json
```

## 已決定的方向

- 套件管理使用 npm。
- 介面元件用 Ant Design，伺服器資料用 TanStack Query，見 [ADR-0008](../docs/adr/0008-frontend-libraries.md)。
- 建置、測試、lint、格式化都用 Vite+，不另外安裝 ESLint 或 Prettier。
- 測試工具從 `vite-plus/test` 匯入，不直接從 `vitest` 匯入。
- 開發時由開發伺服器把 `/api/` 轉發到後端；正式環境前端與 API 由同一個網址提供。
- 零件表格的欄位由後端的 Part Configuration 決定，前端不寫死。
- 依功能領域組織程式碼（parts、bom 等），各自獨立。

目前只有一個頁面，還沒有路由。出現第二個頁面時再加入。

## 設計文件

- [選型理由](../docs/adr/0003-frontend-react-vite-plus.md)
- [開發環境](../docs/development.md)
- [開發慣例](../docs/conventions.md)
- [系統架構](../docs/architecture.md)
- [零件功能](../docs/domains/parts.md)
