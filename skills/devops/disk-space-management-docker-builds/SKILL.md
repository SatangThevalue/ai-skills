---
name: disk-space-management-docker-builds
description: Prevent disk space exhaustion during Docker container builds.
version: 0.1.0
metadata:
  hermes:
    tags: [Docker, DevOps, DiskSpace, Optimization]
---

# Disk Space Management for Docker Builds

This skill covers the procedure for managing constrained host disk space (e.g., VPS with near-full disk partitions) when performing Docker builds. It outlines steps to release cache, prune unused resources, and limit Docker build cache size before starting any container compiles.

## When to Use
- When a server/host disk usage is close to 95%-100% or has less than 3GB of available space.
- Before executing any `docker compose build` or `docker build` command on memory-constrained servers.
- When container builds fail with `write error: No space left on device`.

## Prerequisites
- Docker Engine and Docker Compose installed.
- Administrative or system permissions to clear system logs and cache files.

## How to Run
- Use the `terminal` tool to inspect disk usage and prune Docker assets.

## Quick Reference
- Show disk usage: `df -h`
- Clear Docker build cache: `docker builder prune -f`
- Prune unused containers and networks: `docker system prune -f`
- Clear all unused Docker assets (images, containers, volumes): `docker system prune -a -f`
- Vacuum journal logs to 1 day: `journalctl --vacuum-time=1d`

## Procedure

1. **Check Available Disk Space**
   Verify the available space on the primary partition:
   ```bash
   df -h /
   ```

2. **Clean System Logs and Package Manager Caches**
   Free space from old systemd journal files:
   ```bash
   sudo journalctl --vacuum-time=1d
   ```
   If using Node/NPM or Python on the host, clear their global cache directories to free extra space:
   ```bash
   npm cache clean --force
   pip cache purge
   ```

3. **Prune Docker Build Cache & Unused Layers**
   Run build cache cleanup specifically to free layers held by Docker BuildKit:
   ```bash
   docker builder prune -f
   ```
   To reclaim more space, prune stopped containers, unused networks, and dangling images:
   ```bash
   docker system prune -f
   ```
   For maximum reclamation (removes unused images too):
   ```bash
   docker system prune -a -f
   ```

4. **Targeted Container Build**
   Run the build command specifying only the target service to avoid compiling unnecessary services:
   ```bash
   docker compose -f docker-compose.prod.yml build <service-name>
   docker compose -f docker-compose.prod.yml up -d <service-name>
   ```

## Pitfalls
- **Pruning Active Assets:** Be careful not to prune active volumes if not specified with `-v`. `docker system prune` does not delete named volumes by default, which preserves database states.
- **Docker Cache Loss:** Pruning the builder cache forces subsequent builds to pull and compile layers from scratch, which takes longer but guarantees success on low disk spaces.

## Verification
Verify partition space again to ensure the available space has increased:
```bash
df -h
```
