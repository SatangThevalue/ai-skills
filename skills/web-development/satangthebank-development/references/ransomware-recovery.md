# Database Ransomware Recovery

If your PostgreSQL database is suddenly missing and replaced with a database named `readme_to_recover`, you have been hit by an automated ransomware bot. This happens when the database container port (e.g., 5432) is exposed to the public internet without adequate firewall rules or a strong password.

**The ransom note typically looks like this:**
> All your data was backed up by us. You must pay X bitcoin to <address> or in 48 hours, your data will be publicly disclosed and deleted.
> (for more information visit https://...) After payment send mail to ... and we will provide a link for you to download your data. Your DATAID is: ...

**Recovery Steps:**
1. **Do not pay the ransom.** The bots automatically drop tables; there is rarely an actual exfiltrated backup on their end.
2. **Recreate the database:** Access the postgres container and recreate your dropped database (e.g., `createdb -U postgres satangthebank`).
3. **Restore from local backup:** If you have automated backups (like the ones in `backup/db_auto_backup_*.sql`), restore the most recent one:
   `cat backup/db_auto_backup_YYYYMMDD_HHMMSS.sql | docker exec -i satangthebank-db psql -U postgres -d satangthebank`
4. **Secure the database:**
   - Update `docker-compose.yml` to bind the port only to localhost (`"127.0.0.1:5432:5432"`) if external access isn't required, or configure the host firewall (ufw/iptables) to restrict access to trusted IPs.
   - Change the database password to a strong, cryptographically secure string.