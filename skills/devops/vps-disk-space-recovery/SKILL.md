---
name: vps-disk-space-recovery
description: "Recover emergency host disk space on constrained Linux VPS."
version: 0.1.0
metadata.hermes.tags:
  - Linux
  - DiskSpace
  - DevOps
  - SystemAdmin
  - Storage
---

# Linux VPS Emergency Disk Space Recovery

Recovers storage on Linux systems when the root filesystem hits 95-100% capacity (ENOSPC errors). It cleans systemd journal logs, disabled snap revisions, rotated auth/syslog logs, package manager caches, and Docker build layers without terminating active application services.

## When to Use

- Host disk reaches 95-100% utilization (`df -h /` shows < 1GB available).
- Cron jobs fail with `[Errno 28] No space left on device`.
- Services return false `429` errors due to disk write exhaustion.
- Sudden log inflation from brute-force authentication attempts or service restart loops.

## Prerequisites

- Non-interactive `sudo` access or `SUDO_ASKPASS` configured on the host.
- Standard Linux utilities installed (`du`, `find`, `journalctl`, `snap`, `truncate`).

## How to Run

Execute inspection and cleanup steps sequentially using the `terminal` tool.

## Quick Reference

- Automated cleanup script: `bash ~/.hermes/skills/devops/vps-disk-space-recovery/scripts/clean_disk.sh`
- Check root partition usage: `df -h /`
- Vacuum journal logs: `/usr/bin/sudo -A journalctl --vacuum-size=100M`
- Truncate runaway logs: `/usr/bin/sudo -A truncate -s 0 /var/log/syslog.1 /var/log/btmp /var/log/btmp.1`
- Remove disabled snaps: `snap list --all | awk '/disabled/{print $1, $3}' | while read s r; do sudo -A snap remove "$s" --revision="$r"; done`
- Prune Docker build layers: `docker builder prune -f`
- Clean user package caches: `rm -rf ~/.npm/_cacache ~/.cache/uv`

## Procedure

1. **Assess Usage and Major Directories**
   Identify which top-level paths consume space:
   ```bash
   df -h /
   du -h -d 1 / 2>/dev/null | sort -hr | head -n 10
   ```

2. **Reclaim User-Level Caches (No Sudo Required)**
   Purge package manager and build caches in the user's home directory:
   ```bash
   rm -rf ~/.npm/_cacache ~/.cache/uv
   rm -rf ~/.hermes/profiles/*/home/.npm/_cacache 2>/dev/null
   docker builder prune -f
   ```

3. **Vacuum Systemd Journal Logs**
   Systemd journals often hoard 3-5GB of old logs:
   ```bash
   /usr/bin/sudo -A journalctl --vacuum-size=100M
   ```

4. **Purge Old Snap Revisions and Enforce Retention**
   Remove disabled revisions of snaps and restrict future retention:
   ```bash
   snap list --all | awk '/disabled/{print $1, $3}' | while read s r; do
       /usr/bin/sudo -A snap remove "$s" --revision="$r"
   done
   /usr/bin/sudo -A snap set system refresh.retain=2
   /usr/bin/sudo -A rm -rf /var/lib/snapd/cache/*
   ```

5. **Truncate Runaway Authentication and System Logs**
   Clear oversized rotated logs (e.g. `/var/log/btmp` inflated by SSH brute-force attempts):
   ```bash
   /usr/bin/sudo -A truncate -s 0 /var/log/syslog.1 /var/log/btmp /var/log/btmp.1 2>/dev/null
   /usr/bin/sudo -A apt-get autoremove -y && /usr/bin/sudo -A apt-get clean
   ```

6. **Pause Broken Cron Jobs Triggering Error Loops**
   Check for cron jobs failing continuously and pause them to prevent log recreation:
   ```bash
   hermes cron list
   hermes cron pause <job_id>
   ```

7. **Deploy Recurring Watchdog (Optional Prevention)**
   Configure a silent zero-token watchdog via `cronjob(no_agent=True)` that monitors disk percentage and executes `clean_disk.sh` automatically when usage exceeds threshold. See `references/watchdog-automation.md` for full implementation details.

## Pitfalls

- **Do Not `rm` Active Log Files:** Use `truncate -s 0` instead of `rm` on active log files (`syslog`, `auth.log`). Removing open files leaves disk space locked by active processes until service restart.
- **Docker Volume Protection:** Avoid `docker volume prune -f` or `docker system prune --volumes` unless you have verified that no production database volumes reside on local volumes.
- **Sudo Password Piping:** Never pipe passwords with `echo "password" | sudo -S`. Use `SUDO_ASKPASS` to pass credentials non-interactively.

## Verification

Check the free space on the primary mount:
```bash
df -h /
```
The available space should show at least 4-6GB freed and partition usage below 90%.
