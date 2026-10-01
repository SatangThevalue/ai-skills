---
name: settrade-api-sandbox-connection
description: "Establish and verify connection to the Settrade Sandbox API."
version: 0.1.0
metadata:
  hermes:
    tags: [Settrade, API, Trading, Sandbox, Python]
---

# Settrade API Sandbox Connection

This skill documents the precise steps and code required to authenticate and establish a connection to the Settrade Open API Sandbox environment using the `settrade-v2` Python SDK. It covers resolving common authentication errors ("User not found") by correctly mapping the account type (Investor vs MarketRep) and verifying the connection by retrieving account info. It does not cover live trading execution or market data extraction.

## When to Use
- When configuring the Settrade Open API for the first time.
- When encountering `User not found BrokerId[...]` errors during login.
- When verifying that a Settrade Developer Sandbox account is active and funded.

## Prerequisites
- `settrade-v2` installed (`pip install settrade-v2`).
- `python-dotenv` installed (`pip install python-dotenv`).
- A `.env` file containing the Sandbox credentials.

Required environment variables in `.env`:
```env
SETTRADE_APP_ID="your_app_id"
SETTRADE_APP_SECRET="your_app_secret"
SETTRADE_BROKER_ID="SANDBOX"
SETTRADE_APP_CODE="SANDBOX"
SETTRADE_EQUITY_ACC="<your_equity_account>"
SETTRADE_DERIV_ACC="<your_deriv_account>"
SETTRADE_PIN="000000"
```

## How to Run
Invoke the Python test script through the `terminal` tool to verify the connection and print account margins.

## Quick Reference
- Python class for standard sandbox: `settrade_v2.Investor`
- Sandbox Broker ID: `SANDBOX`
- Default PIN: `000000`

## Procedure

1. **Verify Credentials:**
   Ensure the `.env` file contains the exact `SETTRADE_APP_ID` and `SETTRADE_APP_SECRET` generated from the Settrade Developer Portal. Use the `read_file` tool to inspect the `.env` file if necessary.

2. **Create the Connection Script:**
   Create a Python script (e.g., `test_settrade.py`) that loads the environment variables and attempts a connection using the `Investor` class.

   ```python
   from settrade_v2 import Investor
   import os
   from dotenv import load_dotenv

   load_dotenv(".env")
   app_id = os.getenv("SETTRADE_APP_ID")
   app_secret = os.getenv("SETTRADE_APP_SECRET")
   deriv_acc = os.getenv("SETTRADE_DERIV_ACC", "satang-D") # Example default

   try:
       inv = Investor(
           app_id=app_id, 
           app_secret=app_secret, 
           broker_id="SANDBOX", 
           app_code="SANDBOX"
       )
       deri = inv.Derivatives(account_no=deriv_acc)
       print(deri.get_account_info())
   except Exception as e:
       print("Connection Error:", e)
   ```

3. **Execute the Script:**
   Run the script via the `terminal` tool.
   ```bash
   python3 test_settrade.py
   ```

## Pitfalls
- **Investor vs MarketRep:** The Sandbox environment typically provisions accounts as standard investors. Using `MarketRep` instead of `Investor` will result in a `MarketRep.Derivatives() got an unexpected keyword argument 'account_no'` or a `User not found` error. Always default to `Investor` for Sandbox.
- **Account Activation:** If the script returns `User not found BrokerId[098] Service[SANDBOX] ApiKey[...]` even with correct credentials, the App ID likely lacks subscription to the specific Sandbox account on the Developer Portal. The user must manually subscribe/link the App ID to the test account on the portal.
- **Market Hours:** The Sandbox environment simulates live market hours. Modules like `MarketData` may return "User is inactive" if called outside of 09:00 - 17:00 (BKK time) or on weekends.

## Verification
A successful connection prints a JSON dictionary containing the account's financial status, e.g., `{'creditLine': 2000000000.0, 'excessEquity': 2000000000.0, ...}`.