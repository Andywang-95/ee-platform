# Deployment

部署到公司的方式。這份文件是規劃，M4 實際部署時會補上確切的指令與設定檔。

## 部署目標

一台專用的筆電或 PC，平時只跑這個平台，放在公司內網。不對外連線，不使用雲端服務。

所有服務用 Docker Compose 執行。主機作業系統尚未決定，兩種做法使用同一份 compose 檔。

## 主機作業系統

### 原生 Linux

直接安裝 Linux（例如 Ubuntu Server）並裝 Docker Engine。

- 設定最單純，開機自動啟動與對外開 port 都是標準做法。
- 需要確認公司是否允許非 Windows 的機器接上內網。

### Windows + WSL2

在 Windows 上啟用 WSL2，於 WSL 內安裝 Docker Engine。

額外要處理的事：

| 事項 | 說明 |
|---|---|
| 開機自動啟動 | WSL 預設要有使用者登入才會啟動，需用工作排程器在開機時啟動 |
| 對外連線 | WSL2 預設在 NAT 後面，其他電腦連不進來。改用 mirrored 網路模式，或設定 port 轉發 |
| 防火牆 | Windows 防火牆要開放平台使用的 port |
| Windows Update | 會自動重開機，需設定使用時段，並確認重開後服務會自動恢復 |
| Docker 授權 | Docker Desktop 對一定規模以上的公司需要付費訂閱，所以在 WSL 內直接裝 Docker Engine |

好處：如果這台 Windows 有加入網域，無感登入可以用 IIS 處理，不需要另外申請 SPN，見 [domains/auth.md](domains/auth.md)。

## 需要向 IT 申請的項目

| 項目 | 用途 |
|---|---|
| 一個非個人的服務帳號 | 後端連資料庫用；無感登入也可能用到 |
| 該帳號對零件庫的讀寫權限 | 查詢與編輯零件 |
| 在現有 SQL Server 上新建一個平台專用 database，並給該帳號完整權限 | 存放平台自己的資料，由 Django 建表 |
| 一個固定的主機名稱 | 使用者用它開網站；無感登入也需要 |
| 註冊 `HTTP/<主機名稱>` 的 SPN | 只有用 Kerberos 做無感登入時需要 |

不使用個人帳號的理由：個人密碼到期或變更時服務會中斷；資料庫紀錄會把所有人的修改都記成同一個人；人員異動時服務會失效。

## 資料庫連線

後端用平台專用帳號連 SQL Server。依公司 SQL Server 的設定，有三條路，優先順序如下。

### 1. SQL 帳號

SQL Server 自己管理的帳號密碼。container 直接用帳密連線，設定最簡單。

條件：SQL Server 要啟用混合驗證模式。

### 2. AD 服務帳號 + Kerberos

SQL Server 只接受 Windows 驗證時使用。container 用服務帳號的密碼向 AD 取得 Kerberos 票證，再用票證連線，效果等同在 SSMS 選 Windows 驗證。

條件：

- container 能連到公司的網域控制站。
- SQL Server 的 SPN 有正確註冊。微軟的 Linux ODBC 驅動只支援 Kerberos，不支援 NTLM。SPN 沒註冊時 Windows 用戶端會自動改用 NTLM 所以平常看不出問題，但 Linux 會連不上。

### 3. 後端改在 Windows 原生執行

前兩條都不可行時的退路。後端不放進 container，直接在 Windows 上以服務帳號身分執行。

代價：正式環境與開發環境不一致，部署與更新流程要另外設計。

走哪一條可以先自己查，方法見 [open-questions.md](open-questions.md)。

## 設定與密鑰

- 資料庫位址、帳密、Django `SECRET_KEY`、登入方式都由環境變數提供。
- 正式環境的 `.env` 只放在部署主機上，不進版控。

## CI/CD

使用 Jenkins，M4 時架設。

- Jenkinsfile 只呼叫 `task ci`，檢查內容定義在 Taskfile，本機與 CI 行為一致。
- 部署步驟：在部署主機上取得新版程式、建置 image、執行 migration、重啟服務。
- 公司內的 Git 伺服器位置尚未確認，見 [open-questions.md](open-questions.md)。

## 備份

- 零件庫：沿用公司現有的備份，平台不另外處理。
- 平台庫：與 IT 確認是否納入 SQL Server 既有的備份排程。
