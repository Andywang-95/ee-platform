# ADR-0006：以 Docker Compose 部署在專用 PC

- 狀態：Accepted
- 日期：2026-10-13

## 背景

平台只在公司內網使用，不會上雲端。初期沒有機架式伺服器，以一台專用的筆電或 PC 執行。公司電腦以 Windows 為主。

## 決策

- 所有服務以 Linux container 執行，用 Docker Compose 組合。
- 主機可以是原生 Linux，或 Windows 加 WSL2，兩者使用同一份 compose 檔。主機作業系統在部署前決定。
- 後端以一個非個人的平台專用帳號連接 SQL Server，連線設定全部來自環境變數。
- CI/CD 使用 Jenkins。檢查內容定義在 Taskfile 的 `ci` 任務，Jenkinsfile 只負責呼叫。

## 理由

- 開發環境與正式環境執行相同的 container，減少「我這邊可以跑」的問題。
- compose 檔與主機作業系統無關，主機的決定可以延後。
- 不用個人帳號連資料庫：密碼到期會中斷服務、資料庫紀錄無法分辨實際操作者、人員異動時服務會失效。
- Jenkins 可以完全在內網運作。把檢查邏輯放在 Taskfile，日後換 CI 工具也不用重寫。

## 已知問題

Linux container 不會自動帶有 Windows 身分。資料庫連線依 SQL Server 的設定有三條路，依優先順序為 SQL 帳號、AD 服務帳號加 Kerberos、後端改在 Windows 原生執行。細節見 [deployment.md](../deployment.md)。

## 放棄的選項

- 後端直接在 Windows 上執行：Windows 驗證最省事，但開發環境與正式環境不一致。保留為最後的退路。
- 現在就架設 Jenkins：個人開發階段沒有對應的需求，進公司時再架。
