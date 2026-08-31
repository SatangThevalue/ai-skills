# Settrade API Trading Vulnerabilities (Thai Stock Market)

When transitioning an automated trading system from Sandbox to Production on the SET index, watch out for these critical architectural vulnerabilities:

1. **Market Trading Hours (FOK Rejections)**
   - **Vulnerability**: `FOK` (Fill or Kill) and `IOC` (Immediate or Cancel) orders are strictly rejected outside of the `Open` market status. If a cronjob fires during Pre-Open, Intermission (approx. 12:30 - 14:00), or Off-Hours, valid signals will be killed by the exchange.
   - **Fix**: Query `market.get_market_info()` to ensure the market status is `Open` before executing, or precisely configure cron schedules to avoid intermissions.

2. **EOD Data vs Real-Time (yfinance delay)**
   - **Vulnerability**: Using `yfinance.download` during the trading day provides End-of-Day (EOD) data, meaning the current day's candle is often delayed or incomplete. Calculating sensitive indicators (EMA, RSI, ADX) on delayed data causes the bot's worldview to drift from the actual Streaming board.
   - **Fix**: Fetch real-time price via Settrade's `market.get_quote_symbol(symbol)` and append it to the historical DataFrame before running technical calculations.

3. **Price Step and Slippage Tracking**
   - **Vulnerability**: Simulating a portfolio update by deducting `shares * last_chart_price` after an `MP-MKT` order ignores slippage. Market orders sweep the order book, meaning the actual matched price will differ. Over time, the bot's internal capital tracker will drift heavily from the real `Line Available`.
   - **Fix**: After a successful `place_order`, immediately query `equity.get_order_info(order_no)` to retrieve the exact average matched price for accurate state accounting.

4. **FOK Order Spam Loop**
   - **Vulnerability**: If an FOK order is rejected due to insufficient liquidity (no matching volume on the bid/ask) and the bot runs on a tight cron loop, it will repeatedly fire the same signal. This risks triggering API rate limits or broker-level spam suspensions.
   - **Fix**: Implement a stateful cooldown (e.g., `failed_attempts` timestamp in the JSON state file) to ignore the symbol for a set period after a rejection.