# Postgres Container Crypto-Miner Malware Mitigation

If a host exhibits extremely high CPU usage and `top` shows a suspicious process (like `/tmp/postgresql` or `postgre+`) running inside a Postgres Docker container, it may be compromised by a cryptominer. This often happens due to weak passwords or `POSTGRES_HOST_AUTH_METHOD: trust` being exposed.

## Remediation Steps

1. **Identify the malicious PID inside the container:**
   ```bash
   docker exec <container_name> ps -ef | grep postgres
   ```
   Look for unusual binaries executing from `/tmp/`.

2. **Kill the process and remove the binaries:**
   ```bash
   docker exec <container_name> kill -9 <PID>
   docker exec <container_name> rm -f /tmp/postgresql /tmp/systemd
   ```

3. **Apply temporary mitigation (prevent immediate re-download):**
   ```bash
   docker exec <container_name> chmod -w /tmp
   ```

4. **Permanent Fix:**
   - Remove `POSTGRES_HOST_AUTH_METHOD: trust` from the `docker-compose.yml`.
   - Enforce strong passwords for the database user.
   - Ensure the database port is not publicly exposed without network-level restrictions.
