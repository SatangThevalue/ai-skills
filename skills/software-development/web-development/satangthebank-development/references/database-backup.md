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

## Troubleshooting Missing Script or Directory Errors

If `satangthebank_daily_auto_backup` fails with `[Errno 2] No such file or directory` for `/home/thaieasyvps/satangthebank/apps/backend/src/cron_auto_backup.py`:

1. **Check Disk Space First:**
   Verify host available capacity before cloning:
   ```bash
   df -h /
   ```
   If free space is critically low (< 1GB), run safe maintenance (`docker system prune -f`, `journalctl --vacuum-size=500M`) before cloning to avoid ENOSPC.

2. **Verify Remote Git Repository:**
   ```bash
   git ls-remote https://github.com/SatangThevalue/satangthebank.git
   ```

3. **Re-clone Repository to Host Path:**
   ```bash
   git clone https://github.com/SatangThevalue/satangthebank.git /home/thaieasyvps/satangthebank
   ```

4. **Verify DB Container Status:**
   ```bash
   docker ps -a --filter "name=satangthebank-db"
   ```
   If stopped or missing, launch the container via `docker compose -f /home/thaieasyvps/satangthebank/docker-compose.prod.yml up -d satangthebank-db`.

5. **Decommission / Pausing Batch:**
   If SatangTheBank is superseded by another workspace (e.g. `satang-workspace` / `finance-os`), pause or remove all 4 related cron jobs to avoid continuous alert noise:
   ```bash
   hermes cron pause 99f0b3916979  # satangthebank_daily_auto_backup
   hermes cron pause 4a7787171875  # satangthebank_quota_warning
   hermes cron pause d6b72fb67691  # satangthebank_expire_membership
   hermes cron pause a8b77caba199  # satangthebank_monthly_report
   ```
