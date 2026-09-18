# Malware Infection inside Docker Postgres (`/tmp/postgresql`)

**Symptom**: RAM usage spikes (e.g., 53% / 2.1GB used by a single process). `ps aux` reveals a process like `/tmp/postgresql` running under an unexpected user ID (e.g., `70`). The binary file in `/tmp` has usually been deleted by the malware itself to evade detection (`ls /tmp/postgresql` returns 'No such file').

**Cause**: Cryptominer malware exploiting weak or default credentials on an exposed container (often PostgreSQL or Redis bound to `0.0.0.0` without a strong password).

**Mitigation**:
1.  **Kill the process**: The agent usually lacks passwordless `sudo` rights. Inform the user to manually run `sudo kill -9 <PID>` via SSH.
2.  **Reboot**: Recommend the user run `sudo reboot` to clear out any remaining in-memory artifacts and network sockets created by the malware.
3.  **Harden**: Once the system is back, inspect running containers (`docker ps`). Check if any database container is exposing its port to the internet (`0.0.0.0:5432->5432/tcp`). Remove the public mapping if the database only needs to communicate with other containers on a Docker network, or enforce a strong password.

*Do not attempt to pipe passwords to `sudo -S`.*