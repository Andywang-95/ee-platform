# Backend

Django + Django REST Framework，提供 REST API、資料存取與權限控管。

## 需求

- [uv](https://docs.astral.sh/uv/)（Python 版本由 `.python-version` 指定）

## 常用指令

在 `backend/` 目錄下：

```bash
uv sync                                    # 安裝依賴
uv run python manage.py runserver          # 啟動開發伺服器
uv run python manage.py makemigrations     # 建立 migration
uv run python manage.py migrate            # 套用 migration
uv run pytest                              # 測試
uv run ruff check .                        # lint
uv run ruff format .                       # 格式化
```

多數指令在根目錄有對應的 `task` 任務，用 `task --list` 查看。

## 結構

```text
backend/
├── config/
│   └── settings/     base / development / testing / production
├── apps/             每個功能領域一個 Django app
│   └── parts/
├── tests/            跨 app 的測試
├── manage.py
└── pyproject.toml
```

## 現況

目前只有設定骨架與空的 `parts` app，資料庫暫時使用 SQLite。`SECRET_KEY` 與 `ALLOWED_HOSTS` 已改由環境變數提供，變數清單見根目錄的 `.env.example`。雙資料庫設定會在里程碑 M1 完成。

## 設計文件

- [系統架構](../docs/architecture.md)
- [開發慣例](../docs/conventions.md)
- [零件功能](../docs/domains/parts.md)
- [登入與權限](../docs/domains/auth.md)
