# Container-to-Host `localhost` Routing Failure (2026-07-15)

## Symptom
Application inside Docker repeatedly logs:
```
HTTPConnectionPool(host='localhost', port=42869): Max retries exceeded ...
(Caused by NewConnectionError("... Failed to establish a new connection: [Errno 111] Connection refused"))
```
Meanwhile, from the host shell, `curl http://localhost:42869/v1/chat/completions` works, and `ss -tlnp` confirms the proxy is listening on `*:42869`.

## Root Cause
Inside a container, `localhost` resolves to the container itself, not the host. The proxy is bound to the host network, so connections from the container to `localhost:PORT` fail even though the service is healthy.

## Fix Pattern
1. Add an environment-variable fallback in application code:
   ```python
   proxy_url = os.getenv("AI_PROXY_URL", "http://localhost:42869")
   r = requests.post(f"{proxy_url}/v1/chat/completions", ...)
   ```
2. Inject the correct bridge IP via Docker Compose env block:
   ```yaml
   services:
     api:
       environment:
         - AI_PROXY_URL=http://<host-bridge-ip>:42869
   ```
3. Find the bridge IP:
   ```bash
   docker network inspect <network_name> | grep Gateway
   # typically 10.x.x.1 on the same /24 subnet as the container
   ```

## Why not `host.docker.internal`?
Not always available in Linux containers and adds a DNS dependency. The bridge IP is deterministic and works without Docker Desktop extras.

## Why not bind proxy to `0.0.0.0:42869` alone?
If the proxy is already listening on `*:PORT`, the failure is purely name resolution. Binding to `0.0.0.0` alone does not fix the container-side `localhost` collision; you still need the bridge IP or a published port.
