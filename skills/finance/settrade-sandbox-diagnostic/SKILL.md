---
name: settrade-sandbox-diagnostic
description: "Diagnose and validate Settrade Open API Sandbox credentials."
version: 0.1.0
metadata:
  hermes:
    tags: [Settrade, API, Debugging, Sandbox]
---

# Settrade Sandbox API Diagnostics

Diagnoses "User not found" and "User is inactive" errors from the Settrade Open API. Isolates authentication and connectivity issues from trading logic, verifying whether the API credentials (App ID/Secret) are valid and if specific modules (Equity vs. Market Data) are active. Does NOT handle order placement or trading strategy. Stdlib `settrade_v2` only.

## When to Use

- A cronjob or trading bot fails with `User not found BrokerId[098] Service[SANDBOX] ApiKey[...]`.
- API calls return `Error: User is inactive`.
- Verifying new API credentials before deploying them to production scripts.
- Extracting hardcoded credentials to a `.env` file to prevent future breaks.

## Prerequisites

- Python environment with `settrade-v2` installed.
- Valid `APP_ID` and `APP_SECRET` from the Settrade Developer Portal.

## How to Run

1. Use the `terminal` tool to write and execute minimal diagnostic scripts.
2. Use the `patch` tool to update `.env` variables or migrate hardcoded scripts to use `os.environ`.

## Quick Reference

- `User not found`: The API key is wrong, expired, or revoked.
- `User is inactive`: The key is valid, but the specific module (e.g., `MarketData`) is closed/disabled, often because it is outside market hours (Sandbox Market Data is unreliable outside 09:00 - 17:00).
- Equity Module (Order/Portfolio) is generally accessible 24/7 in Sandbox.

## Procedure

1. **Verify Equity Connection (Account/Orders)**
   Use the `terminal` tool to test the Equity module independently:
   ```python
   cat << 'EOF' > /tmp/check_equity.py
   from settrade_v2 import Investor
   try:
       investor = Investor(app_id="APP_ID", app_secret="APP_SECRET", broker_id="SANDBOX", app_code="SANDBOX", is_auto_queue=False)
       equity = investor.Equity(account_no=os.getenv("SETTRADE_ACCOUNT_NO", "YOUR_ACCOUNT_NO"))
       info = equity.get_account_info()
       print(f"Equity connection successful. Line Available: {info.get('lineAvailable')}")
   except Exception as e:
       print(f"Error: {e}")
   EOF
   python3 /tmp/check_equity.py
   ```

2. **Verify Market Data Connection (Quotes/Ticks)**
   Use the `terminal` tool to test the Market Data module:
   ```python
   cat << 'EOF' > /tmp/check_market.py
   from settrade_v2 import Investor
   try:
       investor = Investor(app_id="APP_ID", app_secret="APP_SECRET", broker_id="SANDBOX", app_code="SANDBOX", is_auto_queue=False)
       market = investor.MarketData()
       quote = market.get_quote_symbol("PTT")
       print(f"Market data successful. Last price: {quote.get('last')}")
   except Exception as e:
       print(f"Error: {e}")
   EOF
   python3 /tmp/check_market.py
   ```

3. **Migrate Credentials to Environment File (.env)**
   If credentials were rotated, secure them via `terminal`:
   ```bash
   cat << 'EOF' > ~/.settrade.env
   SETTRADE_APP_ID=YOUR_APP_ID
   SETTRADE_APP_SECRET=YOUR_APP_SECRET
   EOF
   chmod 600 ~/.settrade.env
   ```

4. **Patch Trading Bots to use ENV**
   Use the `patch` tool or `terminal` to modify the bot's header:
   ```python
   import os
   env_path = os.path.expanduser('~/.settrade.env')
   if os.path.exists(env_path):
       with open(env_path, 'r') as f:
           for line in f:
               if '=' in line and not line.startswith('#'):
                   k, v = line.strip().split('=', 1)
                   os.environ[k] = v

   APP_ID = os.environ.get("SETTRADE_APP_ID")
   APP_SECRET = os.environ.get("SETTRADE_APP_SECRET")
   ```

## Pitfalls

- **Sandbox Market Hours:** The Sandbox `MarketData` API is often shut down after 17:00 BKK time, returning `User is inactive`. Do not assume the key is broken if testing at night.
- **Cronjob Environment Variables:** Cronjobs run in a stripped environment. If using `.env` files, you must explicitly read and parse the file inside your Python script (as shown in Step 4); relying on shell `export` in crontab is brittle.
- **Mixed Expirations:** The Sandbox portal may regenerate an `APP_SECRET` without changing the `APP_ID`. Ensure both match the portal exactly.

## Verification

Run the `check_equity.py` script. A successful test returns `Equity connection successful. Line Available: 10000000.0`.