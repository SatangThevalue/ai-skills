# Environment Variable Mismatches in Isolated Profiles

When configuring messaging platforms (like Telegram or Discord) for an isolated secondary profile, the `config.yaml` of that profile might contain `api_key_env_var` settings (e.g., `api_key_env_var: CRASSULA_TELEGRAM_TOKEN`).

**Pitfall:** Hermes plugins for messaging platforms (like `hermes_plugins.telegram_platform.adapter`) expect the standard environment variable names (e.g., `TELEGRAM_BOT_TOKEN`, `DISCORD_TOKEN`). If you use custom variable names in the `.env` file based on the `api_key_env_var` configuration, the gateway will fail to start for that profile with an error like `[Telegram] No bot token configured`.

**Fix:**
1. Do not rely on `api_key_env_var` for messaging platform tokens in secondary profiles.
2. Ensure the profile's `.env` file (`~/.hermes/profiles/<profile_name>/.env`) uses standard variable names:
   - `TELEGRAM_BOT_TOKEN=...`
   - `DISCORD_TOKEN=...`
3. Remove the conflicting `api_key_env_var` lines from the profile's `config.yaml`.
4. Restart the gateway service (e.g., `systemctl --user restart hermes-gateway-<profile_name>.service`).