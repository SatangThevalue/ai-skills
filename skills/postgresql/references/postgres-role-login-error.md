# Restoring PostgreSQL Login Access

When a PostgreSQL instance is compromised (often via exposed port 5432 and default credentials), attackers frequently drop the `LOGIN` privilege from the main `postgres` user and create their own rogue superuser roles (e.g., `wog`, `priv_esc`). 

When this happens, attempting to use `psql -U postgres` or even `su postgres -c 'psql ...'` from a root shell inside the container will fail with:

```text
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "postgres" is not permitted to log in
```

Because the `postgres` user lacks the `LOGIN` attribute, local socket connections (which use the `postgres` identity) are rejected.

## The Workaround

If the database is still running, you can use the application's database user (which usually still has `LOGIN` access) to list the roles and find the attacker's superuser role, then use *that* role to restore access.

1.  **List roles using an unprivileged application user:**
    ```bash
    docker exec -i satangthebank-db psql -U satangthebank -d satangthebank -c "\du"
    ```
    This reveals the roles:
    ```text
       Role name   |                                Attributes                                
    ---------------+--------------------------------------------------------------------------
     postgres      | Superuser, Create role, Create DB, Cannot login, Replication, Bypass RLS
     priv_esc      | Superuser
     satangthebank | 
     wog           | Superuser
    ```

2.  **Use the rogue superuser to restore the `postgres` user's login:**
    The application user (`satangthebank`) cannot `ALTER ROLE` on a superuser, but the attacker's superuser (`wog`) can:
    ```bash
    docker exec -i satangthebank-db psql -U wog -d satangthebank -c "ALTER ROLE postgres WITH LOGIN;"
    ```

3.  **Secure the Database:**
    Once access is restored, immediately drop the rogue roles, secure the `postgres` password, and remove port `5432` exposure from `0.0.0.0` in `docker-compose.yml`.