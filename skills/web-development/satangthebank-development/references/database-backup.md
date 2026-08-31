# SatangTheBank - Database Backup & Maintenance Reference

## Manual One-Line DB Backup & Restore

### 1. Manual Backup (Dump All)
```bash
docker exec -t satangthebank-db pg_dumpall -U postgres > /home/thaieasyvps/satangthebank/backup/db_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Manual Restore
```bash
cat /home/thaieasyvps/satangthebank/backup/db_backup_<timestamp>.sql | docker exec -i satangthebank-db psql -U postgres
```

## Automated Daily Backup Cron Architecture

- **Script Path:** `apps/backend/src/cron_auto_backup.py`
- **Schedule:** Daily at 02:00 AM (`0 2 * * *`)
- **Storage Target:** `/home/thaieasyvps/satangthebank/backup/`
- **Retention Rule:** Keeps the 7 most recent backup files (`db_auto_backup_*.sql`) and automatically rotates older dumps to protect host disk capacity (~49GB limit).
