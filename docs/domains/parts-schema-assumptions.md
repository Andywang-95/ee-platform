# Parts Schema Assumptions

零件表的實際結構尚未取得。這份文件記錄開發時採用的假設，取得實際結構後逐項核對，核對完就刪除這份文件，把結果寫回 [parts.md](parts.md)。

可信度：

- **確定**：親眼看過且記得清楚。
- **憑印象**：大致記得，細節可能有出入。
- **猜測**：沒有依據，只是為了能先開發。

標為猜測的項目是 M1 建立開發環境時為了能先開發而定的。記得實際情況的話直接修改這份文件與下方列出的檔案。

## 整體結構

| 項目 | 假設 | 可信度 |
|---|---|---|
| 所有零件類型共用一張表 | 是 | 憑印象 |
| 欄位數 | 約 130 多個。開發用的表只建了下方列出的 15 個 | 憑印象 |
| 資料表名稱 | `parts` | 猜測 |
| 主鍵欄位 | `id` | 猜測 |
| 主鍵型別 | `INT`，由資料庫以外的流程給值，不是自動遞增 | 猜測 |
| 區分類型的欄位 | `table_name` | 憑印象 |
| 類型欄位的值 | `R`、`C`、`L`、`IC` | 憑印象 |
| 備註欄位 | `remark` | 猜測 |
| Symbol 欄位與內容格式 | `schematic_part`，格式為 `<OLB 名稱>\<零件名稱>` | 猜測 |
| Footprint 欄位與內容格式 | `pcb_footprint`，內容為 footprint 名稱 | 猜測 |
| CIS 讀取的對象 | 直接讀資料表 | 猜測 |
| 資料筆數 | 未知。假資料為 121 筆 | |

## 欄位

開發用零件表的全部欄位。欄位名稱與型別都是猜測。

| 欄位 | 型別 | 用途 | 使用的類型 |
|---|---|---|---|
| `id` | `INT` | 主鍵 | 全部 |
| `part_number` | `NVARCHAR(50)` | 公司料號 | 全部 |
| `table_name` | `NVARCHAR(20)` | 零件類型 | 全部 |
| `description` | `NVARCHAR(255)` | 描述 | 全部 |
| `value` | `NVARCHAR(50)` | 阻值、容值、感值 | R、C、L |
| `tolerance` | `NVARCHAR(20)` | 誤差 | R、C、L |
| `power_rating` | `NVARCHAR(20)` | 功率 | R |
| `voltage_rating` | `NVARCHAR(20)` | 耐壓 | C |
| `current_rating` | `NVARCHAR(20)` | 額定電流 | L |
| `package` | `NVARCHAR(50)` | 封裝 | 全部 |
| `manufacturer` | `NVARCHAR(100)` | 製造商 | 全部 |
| `manufacturer_part_number` | `NVARCHAR(100)` | 製造商料號 | IC |
| `schematic_part` | `NVARCHAR(255)` | Symbol | 全部 |
| `pcb_footprint` | `NVARCHAR(255)` | Footprint | 全部 |
| `remark` | `NVARCHAR(MAX)` | 備註 | 全部 |

數值類欄位（阻值、耐壓等）假設以文字儲存，例如 `10K`、`16V`。如果實際上是數字加單位分開存，篩選與排序的做法會不同。

## 對齊實際結構時要改的地方

取得實際結構後，受影響的範圍應該只有以下幾處。如果發現還要改別的地方，代表有程式碼直接寫死了欄位，應一併修正。

| 位置 | 內容 |
|---|---|
| `dev/mssql/init.sql` | 開發用零件表的結構 |
| `backend/apps/parts/models.py` | `Part` model 的 `db_table` 與欄位定義，用 `inspectdb` 重新產生 |
| `backend/apps/parts/management/commands/seed_parts.py` | 假資料的欄位 |
| 各類型的 Part Configuration（M2 建立） | 列表、搜尋、篩選、可編輯欄位的名稱 |

前端不應該需要修改，因為欄位來自 Part Configuration。
