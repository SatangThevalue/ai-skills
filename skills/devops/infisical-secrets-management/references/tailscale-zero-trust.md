# Zero-Trust Infisical Deployment via Tailscale

To prevent exposing the Infisical vault to the public internet (avoiding brute-force attacks on port 8080), bind the service exclusively to a Tailscale interface IP instead of `0.0.0.0` or exposing it via a public reverse proxy like Traefik.

1. Install Tailscale on the VPS (`curl -fsSL https://tailscale.com/install.sh | sh` and `tailscale up`).
2. Authenticate the node to your Tailnet.
3. Get the Tailscale IPv4 address (`tailscale ip -4`), e.g., `100.115.66.121`.
4. In the `docker-compose.yml`, bind the ports strictly to the Tailscale IP and set the SITE_URL:

```yaml
    environment:
      - SITE_URL=http://100.115.66.121:8080
    ports:
      # Bind exclusively to the Tailscale IP interface for extreme security
      - "100.115.66.121:8080:8080"
```

This ensures Infisical is completely invisible to public network scans, yet fully accessible to any laptop or mobile device authenticated on your personal Tailnet.