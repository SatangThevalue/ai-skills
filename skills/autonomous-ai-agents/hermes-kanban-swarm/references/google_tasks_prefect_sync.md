# Hermes Kanban to Google Tasks Sync via Prefect

Automates real-time synchronization between the local Hermes SQLite task board (`~/.hermes/kanban.db`) and Google Tasks, creating separate task lists per profile/assignee.

## Architecture

1. **Source of Truth**: `~/.hermes/kanban.db` (`tasks` table).
2. **Target**: Google Tasks API (`tasks.googleapis.com/tasks/v1`).
3. **Orchestrator**: Prefect 2.x/3.x Flow (`@flow(name="hermes-kanban-google-tasks-sync")`).
4. **Schedule**: 1-minute execution via runner script + crontab.

## Profile to Tasklist Mapping

For each unique profile found in `tasks.assignee` or active profiles:
- `default` -> `Hermes: Default (Tonthong)`
- `ton-crassula` -> `Hermes: Ton-Crassula (น้องใบเงิน)`
- `amooksan-dev` -> `Hermes: Amooksan-Dev`
- `researcher` -> `Hermes: Researcher`
- `reviewer` -> `Hermes: Reviewer`
- `writer` -> `Hermes: Writer`

## Status Mapping

| Kanban Status (`tasks.status`) | Google Tasks Status |
|---|---|
| `done`, `archived` | `completed` |
| `todo`, `ready`, `running`, `blocked`, `scheduled` | `needsAction` |

## Prefect Version Invariant (Client vs Server)

If the Prefect Server is running in Docker as `prefecthq/prefect:2-python3.11` (v2.20.x) while host tools have Prefect 3.x installed:
- Direct execution will fail with `RuntimeError: Found incompatible versions: client: 3.x, server: 2.x`.
- **Solution**: Execute the sync flow using `uv` with pinned dependencies:
  ```bash
  uv run --with "prefect==2.20.18" --with "google-api-python-client" --with "google-auth" python /path/to/sync.py
  ```
- **Profile Setting Pitfall**: If `~/.prefect/profiles.toml` contains `PREFECT_SERVER_ALLOW_EPHEMERAL_MODE` (a Prefect 3 key), it crashes Prefect 2 client with a Pydantic validation error. Keep `profiles.toml` clean:
  ```toml
  active = "default"
  [profiles.default]
  PREFECT_API_URL = "http://100.115.66.121:4200/api"
  ```

## 1-Minute Cron Runner Pattern

To prevent concurrent executions from stacking up:
```bash
#!/usr/bin/env bash
exec 200>/tmp/kanban_sync.lock
flock -n 200 || exit 0

export PREFECT_API_URL="http://100.115.66.121:4200/api"
/home/thaieasyvps/.local/bin/uv run --with "prefect==2.20.18" --with "google-api-python-client" --with "google-auth" python /home/thaieasyvps/zero-touch-prefect/kanban_google_tasks_sync.py >> /home/thaieasyvps/.hermes/logs/kanban_google_tasks_sync.log 2>&1
```
Install into crontab:
```cron
* * * * * /home/thaieasyvps/.hermes/scripts/run_kanban_google_tasks_sync.sh
```
