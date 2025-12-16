# Study Chat Server

Backend for the Graspy Study Chat application. Built with FastAPI, DSPy, and SQLAlchemy.

## Setup

1.  **Install Dependencies**:

    ```bash
    uv sync
    ```

2.  **Configuration**:
    Create a `.env` file based on `.env.example`:

    ```bash
    cp .env.example .env
    ```

    Update the values in `.env`:

    - `N_ATLAS_API_BASE`: URL for the LLM provider.
    - `ENABLE_ACCESS_CONTROL`: Set to `True` to enable access codes.
    - `INITIAL_ACCESS_CODE`: Code used for initial seeding (e.g. `TOSIN`).

3.  **Run Migrations**:

    ```bash
    uv run alembic upgrade head
    ```

4.  **Seed Database**:

    ```bash
    uv run python scripts/seed_db.py
    ```

5.  **Run Server**:
    ```bash
    uv run uvicorn main:app --reload --port 8082
    ```

## Database Management

The SQLite database is located at `data/sqlite.db`.

**Production Setup / Updates:**
Always use Alembic to manage the database schema.

- **First Setup**: `uv run alembic upgrade head` then `uv run python scripts/seed_db.py`
- **Updates**: `uv run alembic upgrade head`

### Commands

**List all codes:**

```bash
uv run python scripts/manage_access.py list
```

**Add a new code:**

```bash
uv run python scripts/manage_access.py add "YOUR_NEW_CODE"
```

**Revoke (Disable) a code:**

```bash
uv run python scripts/manage_access.py revoke <ID>
```

**Enable a code:**

```bash
uv run python scripts/manage_access.py enable <ID>
```
