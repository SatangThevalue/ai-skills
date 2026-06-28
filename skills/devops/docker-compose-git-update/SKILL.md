---
name: docker-compose-git-update
description: Pull Git updates and rebuild Docker Compose stacks safely.
version: 0.1.0
metadata:
  hermes:
    tags: [Docker, Git, Deployment, Next.js, Troubleshooting]
---

# Docker Compose Git Update Workflow

Safely updates a local Docker Compose deployment by pulling the latest Git changes and rebuilding the stack. It handles common pitfalls like merge conflicts from locally modified tracked files (e.g., casing changes) and package manager lockfile mismatches during Next.js builds.

## When to Use
- The user pushes new code to a repository and asks you to update the server.
- A `git pull` fails due to untracked working tree files or merge conflicts.
- A Next.js or Node.js Docker build fails at the `npm ci` step due to lockfile discrepancies.

## Prerequisites
- A target directory containing a cloned Git repository and a `docker-compose.yml` file.

## How to Run
Invoke through the `terminal` tool to manage Git, use `patch` to modify the Dockerfile if dependencies fail, and run the rebuild process via `terminal` in the background.

## Quick Reference
- Force Git pull: `git fetch --all && git reset --hard origin/main`
- Clean rebuild: `docker compose build --no-cache && docker compose up -d`
- Check logs: `docker logs <container_name> --tail 10`

## Procedure

1. **Attempt Standard Pull**
   Check the status and attempt a pull using the `terminal` tool:
   ```bash
   cd /path/to/project
   git status
   git pull
   git log -1
   ```

2. **Handle Merge Conflicts (If Pull Fails)**
   If local modifications to tracked files (like renaming `dockerfile` to `Dockerfile`) block the pull, back up local configurations, force reset, and restore:
   ```bash
   cp docker-compose.yml /tmp/docker-compose-backup.yml
   rm Dockerfile 2>/dev/null || true
   git fetch --all
   git reset --hard origin/main
   cp /tmp/docker-compose-backup.yml docker-compose.yml
   ```

3. **Handle `npm ci` Build Failures**
   If `npm ci` fails during the Docker build (common when `package-lock.json` is out of sync), use the `patch` tool to replace `npm ci` with `npm install` in the `Dockerfile`.

4. **Rebuild and Deploy**
   Invoke the build process in the background using the `terminal` tool. Use `--no-cache` if you had to force reset to guarantee a clean slate:
   ```bash
   docker compose up -d --build
   ```
   *(For Next.js apps, this process often exceeds 60 seconds; monitor using `wait` or `poll` actions on the background process).*

## Pitfalls
- **Case-Sensitive File Systems:** Renaming `dockerfile` to `Dockerfile` locally but not in Git will cause a merge conflict on pull. Git on Linux treats them as different files, but Git on Windows/Mac might not.
- **Next.js Build Times:** Compiling static pages (SSG) in Next.js 15+ takes significant time. Do not assume the build has hung; check `top` to verify if the `node` process is consuming high CPU.
- **Docker Build Log Visibility:** When running `docker compose up -d --build`, the build logs might not surface if the process timeouts in the terminal tool. Use `docker compose build --no-cache` first to see explicit build errors before `up -d`.

## Verification
Use the `terminal` tool to verify the container is running the latest code and is healthy:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep my-project
docker logs my-project --tail 10
```