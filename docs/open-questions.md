# Open Questions

進公司部署（M4）前要確認的事項。確認後把結果寫回對應的文件，並從這裡移除。

## 可以自己先查的

### SQL Server 接受哪種驗證

用現有的連線執行：

```sql
SELECT SERVERPROPERTY('IsIntegratedSecurityOnly');
```

- `0`：有開混合驗證，可以申請 SQL 帳號（連線方式 1）。
- `1`：只接受 Windows 驗證，要走 AD 服務帳號 + Kerberos（連線方式 2）。

### 目前的連線是 Kerberos 還是 NTLM

```sql
SELECT auth_scheme FROM sys.dm_exec_connections WHERE session_id = @@SPID;
```

- `KERBEROS`：SQL Server 的 SPN 正常，Linux container 可以用 Kerberos 連線。
- `NTLM`：SPN 有問題，連線方式 2 會失敗，需要請 IT 修正 SPN 或改走其他方式。
- 查不到（權限不足）：請 IT 協助確認。

### 零件表的實際結構

- 資料表名稱、欄位名稱與型別。
- 區分零件類型的欄位（先前記錄為 `table_name`）有哪些值。
- 備註欄位的名稱。
- 存放 symbol 與 footprint 名稱的欄位，以及內容格式。
- 主鍵是哪個欄位。
- CIS 是直接讀資料表，還是透過 view。

### 現有的 trigger log

- 記錄了哪些內容、存在哪裡。
- 平台改用專用帳號寫入後，它記到的修改人會變成該帳號，確認這對現有流程有沒有影響。

## 需要問 IT 的

| 問題 | 影響 |
|---|---|
| 能否申請一個非個人的服務帳號 | 資料庫連線與無感登入的前提 |
| 能否在現有 SQL Server 上新建平台專用 database | 不行的話要另找地方放平台資料 |
| 專用電腦能否安裝 Linux 並接上內網 | 決定主機作業系統 |
| 專用電腦若用 Windows，是否會加入網域 | 決定無感登入能否用 IIS 處理 |
| 能否給一個固定的主機名稱（DNS） | 使用者連線與無感登入 |
| 能否註冊 HTTP SPN | 用 Kerberos 做無感登入時需要 |
| 公司內有沒有 Git 伺服器，或是否允許自架 | Jenkins 從哪裡取得程式碼 |
| 平台庫能否納入既有備份排程 | 資料保全 |

## 需要問使用者的

- 哪些人需要編輯權限。
- 哪些欄位允許在平台上編輯，哪些只能看。
- 各零件類型最常用來搜尋與篩選的欄位。

## 第二階段前要確認的

- 公司使用的 OrCAD Capture 與 Allegro 版本。
- 是否有一台裝有 Cadence license 的機器可以執行批次匯出。
- OLB 與 DRA 檔案存放的位置，以及更新的頻率。
