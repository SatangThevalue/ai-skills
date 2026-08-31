---
name: settrade-multi-stock-scanner
description: "Deploy a multi-stock Settrade scanner via Hermes cronjob."
version: 0.1.0
metadata:
  hermes:
    tags: [Settrade, Trading, Cronjob, Multi-Stock]
---

# Settrade Multi-Stock Scanner

Upgrades a single-stock trading bot into a multi-stock scanner that runs safely in the background as a Hermes cronjob. It handles cross-iteration balance tracking, per-symbol state isolation, API rate limiting, and cron-specific python path resolution. It does NOT implement the trading strategy itself (relies on an external strategy module).

## When to Use

- The user wants to trade a list of stocks (e.g., SET50) instead of a single ticker.
- A trading bot fails in cronjobs with `ModuleNotFoundError` or file path issues.
- The bot needs to track simulated cash flow across multiple orders in the same loop.

## Prerequisites

- Settrade API credentials (`APP_ID`, `APP_SECRET`, etc.).
- A working strategy engine (e.g., `adaptive_survival_system_v3.py`) located in `~/`.

## How to Run

Copy the scanner template using the `terminal` tool, modify the `SYMBOLS` list, and schedule it via the `cronjob` tool.

## Quick Reference

- **Path injection**: `sys.path.append(os.path.expanduser('~'))`
- **Rate limit**: `time.sleep(1)` between iterations.
- **Cash sync**: `real_line_available -= (shares * price)` on buy, `+=` on sell.

## Procedure

1. **Deploy the Scanner Script**
   Use the `terminal` tool to copy the reference template into the cron scripts directory:
   ```bash
   cp ~/.hermes/skills/finance/settrade-multi-stock-scanner/scripts/scanner_template.py ~/.hermes/scripts/full_loop_bot.py
   ```

2. **Customize the Symbols list**
   Use the `patch` tool to modify the `SYMBOLS` array in `~/.hermes/scripts/full_loop_bot.py` to match the user's preference.

3. **Schedule the Job**
   Use the `cronjob` tool to run the scanner during market hours:
   Call `cronjob(action="create", name="settrade-auto-trade", schedule="*/30 10-16 * * 1-5", script="full_loop_bot.py", no_agent=True)`

## Pitfalls

- **Cronjob Working Directory**: Cron jobs run in `~/.hermes/scripts/`. If the bot imports modules from `~/` or writes state files like `bot_state.json`, it will fail unless `sys.path` is appended and explicit absolute paths (`os.path.expanduser('~')`) are used for data directories.
- **Double Spending**: If `lineAvailable` is only fetched at the start of the loop and multiple BUY signals trigger, the bot might over-allocate. You MUST manually deduct `(shares * price)` from the in-memory variable after a successful order.
- **Rate Limits**: Looping API requests (like `yf.download` or `place_order`) too fast will trigger temporary bans. Always include `time.sleep(1)` at the end of each iteration.
- **FOK vs Day Validity**: Refer to the `settrade-order-debugging` skill; always use `validity_type="FOK"` with `price_type="MP-MKT"`.

## Verification

Use the `terminal` tool to verify the per-symbol state files are generating after a run:
```bash
ls -la ~/bot_state_*.json
```