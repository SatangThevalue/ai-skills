---
name: infisical-secrets-management
description: "Self-host and implement Infisical for secure environment variable management."
version: 0.2.0
metadata:
  hermes:
    tags: [Infisical, Secrets, DevOps, Environment, Security, Docker, Tailscale]
    related_skills: [linux-security-hardening]
---

# Infisical Secrets Management (Zero-Trust Architecture)

This skill covers deploying and integrating **Infisical**, the open-source platform for secret, certificate, and privileged access management, using a Zero-Trust architecture. It replaces `.env` files by providing a centralized vault. To prevent unauthorized access, the Infisical server is bound exclusively to a Tailscale VPN IP, making it completely invisible to the public internet.

## When to Use
- When managing API keys across multiple Docker containers or Python scripts.
- When eliminating `.env` files from your Git repositories and servers.
- When you need a highly secure, private vault accessible only via your Tailscale network.

## Prerequisites
- A VPS with Docker and Docker Compose installed.
- Tailscale installed and authenticated on the VPS and the client machine.
- `expect` package installed (`sudo apt-get install expect`) for CLI automation.

## How to Run
Deploy the stack via `docker-compose.yml`, authenticate via the CLI using your Tailscale IP, and use the `infisical run` wrapper to execute your scripts.

## Quick Reference
- **Install CLI:** `docker run --rm --entrypoint sh infisical/cli -c "cat /bin/infisical"` (extract binary workaround)
- **Get Tailscale IP:** `tailscale ip -4`
- **CLI Inject:** `infisical run --env=prod --domain http://<TAILSCALE_IP>:8080 -- python main.py`

## Procedure

### 1. Zero-Trust Deployment (Docker + Tailscale)
Infisical must be bound to the Tailscale interface, not `0.0.0.0`.
Get the Tailscale IP using the `terminal` tool: `tailscale ip -4` (e.g., `100.115.66.121`).

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  infisical:
    image: infisical/infisical:latest
    container_name: infisical-server
    restart: always
    environment:
      - NODE_ENV=production
      - DB_CONNECTION_URI=postgres://infisical:infisical_pw@db:5432/infisical
      - REDIS_URL=redis://redis:6379
      # Generate these securely via `openssl rand -hex 16`
      - ENCRYPTION_KEY=your_encryption_key
      - AUTH_SECRET=your_auth_secret
      - SITE_URL=http://100.115.66.121:8080
    ports:
      # Bind exclusively to Tailscale IP
      - "100.115.66.121:8080:8080"
    depends_on:
      - db
      - redis
    networks:
      - infisical_net

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: infisical
      POSTGRES_PASSWORD: infisical_pw
      POSTGRES_DB: infisical
    volumes:
      - infisical_pgdata:/var/lib/postgresql/data
    networks:
      - infisical_net

  redis:
    image: redis:alpine
    volumes:
      - infisical_redis_data:/data
    networks:
      - infisical_net

volumes:
  infisical_pgdata:
  infisical_redis_data:
networks:
  infisical_net:
```
Run `docker compose up -d`.

### 2. Install Infisical CLI (Docker Extraction Workaround)
Cloudsmith/GitHub blocking often causes standard curl/wget installs to fail or download corrupted HTML. Extract the compiled binary directly from the official Docker image.

```bash
docker run -d --name temp_infisical infisical/cli sleep 30
docker cp temp_infisical:/bin/infisical /tmp/infisical_bin
docker rm -f temp_infisical
sudo mv /tmp/infisical_bin /usr/local/bin/infisical
sudo chmod +x /usr/local/bin/infisical
```

### 3. Authenticate and Initialize Workspace
Authentication requires human interaction via a browser on the Tailscale network.

1. **Login:** Run `infisical login --domain http://100.115.66.121:8080`. Click the generated link to authenticate in your browser.
2. **Initialize:** The `infisical init` command is interactive and breaks in headless agent environments. Use the provided `scripts/init_infisical.exp` script to automate the selection using `pexpect`/`expect`.

```bash
# Example: 2 down arrows to select the 3rd project in the list
./scripts/init_infisical.exp /home/thaieasyvps/workspace 2
```

**Alternative (No Script / Pexpect Timeout):**
When `pexpect` hits a timeout because the CLI prompt text changes or it prompts for a default Organization first, you must intercept both prompts. The sequence is usually `[Enter]` (select default Org) -> `[Down] x N` -> `[Enter]` (select Project).
   
If CLI init remains flaky due to terminal ANSI issues in background processes, the most robust way to authenticate a headless Python process is to bypass the CLI entirely and use `infisical-python` SDK with Machine Identity credentials directly in the code (avoiding the need for a local `.infisical.json` workspace link).

### 4. Injecting Secrets (Runtime)
Never hardcode secrets. Inject them at runtime using the CLI wrapper. You MUST pass the `--domain` flag when self-hosting.

```bash
cd /home/thaieasyvps/workspace
infisical run --env=dev --domain http://100.115.66.121:8080 -- python bot.py
```
Inside `bot.py`, access secrets natively: `os.getenv("MY_SECRET")`.

## Pitfalls
- **Missing Domain Flag:** If you omit `--domain http://<IP>:8080` in `infisical run`, the CLI attempts to contact the default US Cloud server and fails silently or asks for re-authentication.
- **Corrupt CLI Downloads:** Standard `curl` installation scripts for the CLI often fail on constrained VPS environments or hit Cloudflare blocks. Use the Docker extraction method (Step 2).
- **Interactive Init Failures:** `infisical init` cannot be piped or automated easily with standard bash due to TTY requirements. You must use `expect` to send ANSI arrow codes (`\033[B`).
- **Systemd Environment Isolation:** Exporting variables in a bash script and calling `systemctl restart` does NOT pass those variables to the daemon. Echoing secrets into `.env` files as a workaround breaks the Zero-Trust rule. You must modify the systemd `.service` file's `ExecStart` line to use the `infisical run` wrapper directly. See `references/systemd-infisical-wrapper.md`.

## Verification
Run `infisical secrets --env=dev --domain http://<TAILSCALE_IP>:8080`. It should print an ASCII table of your decrypted secrets.