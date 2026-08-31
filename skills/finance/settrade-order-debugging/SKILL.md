---
name: settrade-order-debugging
description: "Debug Settrade API order rejections and OSS errors."
version: 0.1.0
metadata:
  hermes:
    tags: [Settrade, Trading, Debugging, API]
---

# Settrade Order Debugging

Diagnoses and resolves issues where a trading bot fails to place equity orders via the Settrade Open API. It focuses on isolating API calls to reproduce validation errors (like OSS rejections) without running the entire bot loop.

## When to Use

- A Settrade bot runs successfully but fails to buy or sell.
- The logs show "Order Rejected by OSS" or `SettradeError`.
- The user reports missing orders or incorrect parameter rejections (e.g., Side, Validity).

## Prerequisites

- Settrade API credentials (`app_id`, `app_secret`, `broker_id`, `app_code`).
- Python environment with `settrade-v2` installed.
- Target account number and 6-digit PIN.

## How to Run

1. Use `read_file` or `search_files` to locate the bot's order placement code.
2. Extract the exact parameters being passed to `equity.place_order()`.
3. Use the `terminal` tool to run a minimal reproduction script to capture the raw `SettradeError`.
4. Apply the fix to the main codebase using the `patch` tool.

## Quick Reference

- **Side**: Must be exactly `"Buy"` or `"Sell"` (Title case). `"BUY"` will be rejected.
- **Market Price (MP-MKT)**: Must use `validity_type="FOK"` or `validity_type="IOC"`.
- **Day Validity (Day)**: Must use `price_type="Limit"` with a specific numerical price.

## Procedure

1. **Locate the failing order call**
   Search the codebase for the `place_order` method to identify what variables are being sent.
   Use `search_files(pattern="place_order", target="content")`.

2. **Create a Minimal Reproduction Script**
   Use the `terminal` tool to create a temporary test script that isolates the exact order parameters. This bypasses the bot's `try/except` blocks that might be swallowing the real API error messages.
   ```bash
   cat << 'EOF' > /tmp/test_settrade_order.py
   from settrade_v2 import Investor
   from settrade_v2.errors import SettradeError

   # Replace with actual credentials from the bot's config
   investor = Investor(app_id="APP_ID", app_secret="APP_SECRET", app_code="SANDBOX", broker_id="SANDBOX", is_auto_queue=False)
   equity = investor.Equity(account_no="ACCOUNT_NO")

   try:
       res = equity.place_order(
           pin="000000", 
           side="Buy",           # Verify case
           symbol="PTT", 
           volume=100, 
           price=0, 
           price_type="MP-MKT",  # Check price_type compatibility
           validity_type="Day"   # Check validity_type compatibility
       )
       print(f"Success: {res}")
   except SettradeError as e:
       print(f"SettradeError: {e}")
   EOF
   ```

3. **Execute the Reproduction Script**
   Run it via the `terminal` tool:
   ```bash
   python3 /tmp/test_settrade_order.py
   ```
   Analyze the output. If it says `Cannot place Market order when validity is not FOK/IOC`, you have a parameter conflict.

4. **Apply the Fix**
   Use the `patch` tool to correct the parameters in the main bot file.
   - If fixing a Market Order: change `validity_type` to `"FOK"`.
   - If fixing Side casing: change `"BUY"` to `"Buy"`.

## Pitfalls

- **Swallowed Errors**: Trading bots often wrap API calls in `try...except` and print custom logs, hiding the underlying `SettradeError` message. Always reproduce outside the main loop.
- **Gearing/Board Lots**: If the price/validity is correct but the order still fails, verify that `volume` is a multiple of 100 (Board Lot) and that there is sufficient `Line Available` (cash balance) to cover the cost.
- **Sandbox vs Production**: Some validation rules are strictly enforced in Production but behave slightly differently or lag in Sandbox.

## Verification

Run the patched bot via the `terminal` tool. A successful fix is confirmed when the output displays an `orderNo` from the API response (e.g., `{'orderNo': '636LWCRRLL'}`).