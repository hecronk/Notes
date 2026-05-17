# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack

FastAPI + SQLAlchemy 2.x (async) + asyncpg + Alembic, managed by Poetry on Python 3.14.

## Common commands

Dependencies / environment:
- `poetry install` — install deps from `pyproject.toml` / `poetry.lock`.
- `poetry shell` (or prefix commands with `poetry run`) — enter the project venv.

Run the API (from repo root, so `src.*` imports resolve):
- `poetry run uvicorn src.main:app --reload`

Alembic migrations (run from repo root — `alembic.ini` lives there and uses `prepend_sys_path = .`):
- `poetry run alembic revision --autogenerate -m "<message>"`
- `poetry run alembic upgrade head`
- `poetry run alembic downgrade -1`

There is no test suite, linter, or formatter configured in `pyproject.toml`.

## Configuration

Settings are loaded by `src/core/settings/settings.py` from `src/core/settings/.env` (note: **not** the repo-root `.env`). Required vars: `db_user`, `db_password`, `db_name`, `secret_key`, `media_path`. Optional: `db_host` (default `localhost`), `db_port` (default `5432`), `debug` (default `False`), `broker_url`.

`settings.database_url` is composed as `postgresql+asyncpg://...` — the whole stack is async, so the DB URL must use the `asyncpg` driver, not plain `postgresql://`.

## Architecture

Layout under `src/`:
- `main.py` — FastAPI app; mounts routers from `src/routers/v1/`.
- `routers/v1/` — versioned HTTP endpoints. Each router is included individually in `main.py` (no auto-discovery). New routers must be imported and registered there.
- `schemas/` — Pydantic request/response models. `BaseSchema` is for inputs; `BaseResponse` adds `id` + `created_at` and is mixed into response schemas (see `NoteResponseSchema` mixing `NoteSchema` + `BaseResponse`).
- `core/database/db.py` — owns the async engine, `AsyncSessionLocal`, the `declarative_base()` `Base`, and the `get_session` FastAPI dependency. Sessions are configured with `expire_on_commit=False` and `autoflush=False`.
- `core/database/models/` — SQLAlchemy ORM models. Models inherit from both `BaseModel` (provides `id`, `created_at`) **and** `Base` (the declarative base). `BaseModel` is a plain mixin, not a declarative base — both parents are required.
- `core/database/alembic/env.py` — async Alembic env. It imports `src.core.database.models` with a wildcard to register all tables on `Base.metadata`; **new model modules must be importable from `src/core/database/models/__init__.py`** (currently via `from src.core.database.models.note import *`) for autogenerate to see them.
- `dependencies/` — reusable FastAPI dependencies (e.g. `get_pagination`).
- `services/` — standalone helpers (e.g. `random_number.py`). Note `requests` is used here but is **not** declared in `pyproject.toml`; add it before relying on this module.

Request flow: router endpoint → `Depends(get_session)` yields an `AsyncSession` → SQLAlchemy 2.x style query (`select(...)`, `await session.execute(...)`, `result.scalars()...`) → return ORM instance, FastAPI serializes via the `response_model` Pydantic schema.