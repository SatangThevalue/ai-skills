# Wrapping Systemd Services with Infisical

When strictly enforcing a "No `.env` files" Zero-Trust architecture, background services managed by `systemd` (like `hermes-gateway` or any python daemon) must be wrapped with the Infisical CLI directly in their service definitions. 

If you export tokens in a deployment script and run `systemctl --user restart`, systemd will NOT inherit those variables because it runs in an isolated environment. Echoing secrets into `.env` files as a workaround breaks the Zero-Trust security model.

## Solution: Edit the Systemd Service
Modify the `ExecStart` line of the target systemd service to invoke `infisical run` before the main application.

1. Open the user service file (e.g., `~/.config/systemd/user/hermes-gateway-bot_trade.service`).
2. Change the `ExecStart` line to prepend the infisical wrapper:
   ```ini
   [Service]
   # Old:
   # ExecStart=/home/user/.../python -m hermes_cli.main --profile bot_trade gateway run
   
   # New:
   ExecStart=/usr/local/bin/infisical run --env=prod --domain http://100.115.66.121:8080 -- /home/user/.../python -m hermes_cli.main --profile bot_trade gateway run
   ```
3. Reload systemd and restart the service:
   ```bash
   systemctl --user daemon-reload
   systemctl --user restart hermes-gateway-bot_trade
   ```

This guarantees that the service fetches fresh secrets directly from the Vault into RAM on every restart, leaving no `.env` files on disk.