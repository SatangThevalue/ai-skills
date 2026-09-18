# Handling Intraday Market Noise (1H/15M) in Quant Models

**Context:** Models that perform well on Daily (1D) timeframes often fail catastrophically on Intraday timeframes (15m, 1H) due to low Signal-to-Noise Ratio (SNR) and the relative size of the transaction cost (spread).

**Techniques to Rescue Underperforming Intraday Models:**

1. **Fractional Differencing (e.g., GOLD):**
   Standard percent returns destroy the "long memory" of a trend, which is crucial for commodities like Gold. Use Fractional Differencing (e.g., $d=0.4$) to make the time series stationary while retaining its memory.

2. **Asymmetric Triple Barrier Labeling (Crypto & Volatile Assets):**
   Assets like BTC tend to "stop hunt" before trending. Setting symmetric Stop Loss (SL) and Take Profit (TP) leads to poor win rates.
   *Solution:* Set an asymmetric barrier, e.g., `TP = 4.0 ATR` and `SL = 1.5 ATR`. Accept a lower win rate but capture large trend moves to compensate for the whipsaws.

3. **Macro-Economic Feature Integration (GBPUSD, USDJPY):**
   Intraday price action on fiat currencies is often just random walk until a macro catalyst hits.
   *Solution:* Inject Macro features like the US Dollar Index (DXY) returns and the US 10-Year Treasury Yield (US10Y) difference. If US10Y is spiking, the model learns not to buy GBPUSD, avoiding false breakouts.

4. **Meta-Labeling (The Two-Stage Model):**
   *   **Model 1 (Base):** Predicts direction (Buy/Sell).
   *   **Model 2 (Meta):** Learns from Model 1's mistakes. It predicts whether Model 1's signal will actually be profitable *after* transaction costs (spread).
   *   *Result:* Filters out hundreds of low-conviction trades, rescuing strategies from being eaten alive by spread in the 15m timeframe.