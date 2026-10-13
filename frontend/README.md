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

## 結構

```text
frontend/
├── src/
│   ├── main.tsx        進入點
│   ├── App.tsx         目前只有連線狀態頁
│   ├── health.ts       呼叫健康檢查 API
│   └── health.test.ts
├── index.html
├── vite.config.ts      Vite+ 設定：開發伺服器、lint、格式化
├── Dockerfile          開發用 image
└── package.json
```

## 已決定的方向

- 套件管理使用 npm。
- 建置、測試、lint、格式化都用 Vite+，不另外安裝 ESLint 或 Prettier。
- 測試工具從 `vite-plus/test` 匯入，不直接從 `vitest` 匯入。
- 開發時由開發伺服器把 `/api/` 轉發到後端；正式環境前端與 API 由同一個網址提供。
- 零件表格的欄位由後端的 Part Configuration 決定，前端不寫死。
- 依功能領域組織程式碼（parts、bom 等），各自獨立。

元件庫、資料請求、路由、狀態管理等套件在 M2 開始做零件頁面時再選。

## 設計文件

- [選型理由](../docs/adr/0003-frontend-react-vite-plus.md)
- [開發環境](../docs/development.md)
- [開發慣例](../docs/conventions.md)
- [系統架構](../docs/architecture.md)
- [零件功能](../docs/domains/parts.md)
