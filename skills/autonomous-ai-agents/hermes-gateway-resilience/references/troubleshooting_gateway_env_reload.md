# Troubleshooting: Gateway Platform Disconnections

## Symptom
Gateway throws errors like `[Telegram] No bot token configured` or `[Discord] No bot token configured` despite the tokens being properly formatted in the `.env` file, and `hermes gateway restart` does not pick them up.

## Root Cause
When the Hermes Gateway is run as a systemd user service (via `hermes gateway install`), it locks the environment variables present at the time the service was started. Standard `hermes gateway restart` merely asks the service to stop and start the child process, but does not tell systemd to re-read the environment (or the `.env` file if it was explicitly sourced in the service definition).

## Resolution Workflow

If you update credentials in `~/.hermes/.env` or via an external secret manager like Infisical and need the Gateway to see them:

1. **Stop the gateway:**
   ```bash
   hermes gateway stop
   ```

2. **Reset the failed state (if it crashed looping):**
   ```bash
   systemctl --user reset-failed hermes-gateway
   ```

3. **Force systemd to reload its configuration:**
   ```bash
   systemctl --user daemon-reload
   ```

4. **Start the gateway again:**
   ```bash
   hermes gateway start
   ```

This ensures the systemd supervisor pulls the fresh environment variables before launching the Python gateway process.

## Checking Token Status
To verify the token is properly loaded in the `.env` file (e.g. for Discord):
```bash
/home/thaieasyvps/.hermes/hermes-agent/venv/bin/python -c "import os; from dotenv import load_dotenv; load_dotenv('/home/thaieasyvps/.hermes/.env'); print(os.environ.get('DISCORD_TOKEN'))"
```