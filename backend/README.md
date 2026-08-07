# Backend

Backend 採用 Django 作為主要框架，負責提供 REST API、資料存取、權限管理以及商業邏輯。

---

## 技術

- Python
- Django
- Django REST Framework
- drf-spectacular
- Microsoft SQL Server（規劃中）

---

## Requirements

- Python 3.13+
- uv

---

## 安裝

```bash
uv sync
```

---

## 啟動開發環境

```bash
uv run python manage.py runserver
```

---

## 常用指令

啟動 Server：

```bash
uv run python manage.py runserver
```

建立 App：

```bash
uv run python manage.py startapp <app_name>
```

建立 Migration：

```bash
uv run python manage.py makemigrations
```

執行 Migration：

```bash
uv run python manage.py migrate
```

執行測試：

```bash
uv run pytest
```

Ruff：

```bash
uv run ruff check .
uv run ruff format .
```

---

## 專案結構

```text
backend/
├── apps/
├── config/
├── manage.py
├── pyproject.toml
└── uv.lock
```

---

## Settings

Settings 採用多環境配置。

```text
config/settings/

base.py
development.py
testing.py
production.py
```

---

## Architecture

Business Logic 應集中於 Service Layer。

Model 主要負責：

- Database Mapping
- QuerySet
- Manager

API Schema 與 Validation 將採用獨立 Schema Layer。

---

## 文件

詳細設計請參閱：

```
docs/
```