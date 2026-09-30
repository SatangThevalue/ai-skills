# Automated Proactive Disk Watchdog Configuration

This reference details the procedure for deploying a non-interactive, zero-token disk watchdog using the Hermes Cron system (`no_agent: true`).

## 1. SUDO_ASKPASS Setup for Cron Execution

When running via background cron, interactive password prompts fail. Establish a restricted askpass helper:

```bash
mkdir -p ~/.hermes/scripts
cat << 'EOF' > ~/.hermes/scripts/.askpass.sh
#!/bin/bash
echo "YOUR_SUDO_PASSWORD"
EOF
chmod 700 ~/.hermes/scripts/.askpass.sh
```

## 2. Watchdog Script Pattern (`vps_disk_watchdog.sh`)

Deploy to `~/.hermes/scripts/vps_disk_watchdog.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

THRESHOLD=88
USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')

if [ "$USAGE" -ge "$THRESHOLD" ]; then
    export SUDO_ASKPASS="/home/thaieasyvps/.hermes/scripts/.askpass.sh"
    
    # Run recovery script
    CLEANUP_OUTPUT=$(/home/thaieasyvps/.hermes/skills/devops/vps-disk-space-recovery/scripts/clean_disk.sh 2>&1)
    
    NEW_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
    FREE_SPACE=$(df -h / --output=avail | tail -1 | tr -d ' ')
    
    echo "🚨 [VPS Disk Watchdog] คำเตือน: พื้นที่ดิสก์เกินเกณฑ์กำหนด!"
    echo "• ตรวจพบการใช้งาน: ${USAGE}% (เกณฑ์เฝ้าระวัง: ${THRESHOLD}%)"
    echo "• ระบบดำเนินการล้างไฟล์ขยะและแคชฉุกเฉินเรียบร้อยแล้ว"
    echo "• สถานะล่าสุด: ${NEW_USAGE}% used (พื้นที่ว่างเหลือ: ${FREE_SPACE})"
else
    # Silent mode when disk usage is normal (Hermes Watchdog pattern)
    exit 0
fi
```
Ensure execution permissions: `chmod +x ~/.hermes/scripts/vps_disk_watchdog.sh`

## 3. Registering the Cron Job

Create the recurring cron job via Hermes tool or CLI:

```python
cronjob(
    action="create",
    name="vps_disk_watchdog",
    schedule="0 */12 * * *",
    no_agent=True,
    script="vps_disk_watchdog.sh",
    prompt="Automated VPS Disk Space Watchdog (>88%)"
)
```

### Delivery Semantics:
- **Usage < 88%**: Exits 0 with empty stdout → Hermes remains silent; zero messages sent.
- **Usage >= 88%**: Emits alert to stdout → Hermes auto-delivers report directly to the origin messaging channel (Telegram).
- **Execution Cost**: Zero LLM tokens consumed.
