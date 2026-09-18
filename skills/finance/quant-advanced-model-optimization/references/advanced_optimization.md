# Advanced Model Optimization (Meta-Labeling, VolTarget, FracDiff)

Techniques used to recover underperforming assets and timeframes in Machine Learning quantitative models.

## 1. Meta-Labeling (Combating Spread/Noise in Small Timeframes like 15m)
- **Problem:** Frequent trading in low-timeframe environments results in transaction costs (spread/commission) erasing profits.
- **Solution:** Two-stage modeling.
  - **Base Model (Model 1):** Predicts direction (up/down).
  - **Meta Model (Model 2):** Takes the output of Model 1 and predicts *whether the expected profit will exceed the transaction costs* (Will it survive the spread?). If Model 2 predicts 'No', the trade is blocked.
- **Result:** Drastically reduces trade frequency, filtering out 'garbage' trades and turning a net-loss system into a profitable one.

## 2. Fractional Differencing & HMM Regimes (Solving GOLD)
- **Problem:** Gold is highly volatile, narrative-driven (news), and prone to massive fat-tail breakouts. Standard indicators (like RSI) applied to percentage returns destroy the "long memory" of the trend.
- **Solution:** 
  - **Fractional Differencing:** Mathematically transforms price data to achieve stationarity while preserving memory, unlike standard integer differencing (returns).
  - **Hidden Markov Models (HMM):** Uses unsupervised learning to detect market regimes (e.g., Sideways, Bull Trend, Bear Volatility). EAs are configured to switch strategies based on the detected regime (e.g., Buy & Hold during quiet bull regimes, stay out during high-volatility bear regimes).

## 3. Volatility Target Sizing & Microstructure (Solving BTC)
- **Problem:** Crypto assets experience violent 'Stop Hunts' and massive drawdowns. Fixed % risk per trade fails.
- **Solution:**
  - **Inverse Volatility Sizing:** Dynamically reduce position size when market volatility (ATR) spikes.
  - **Microstructure Features:** Incorporate Binance Funding Rates and Open Interest (OI) into the ML model. High positive funding rates indicate retail is excessively long, signaling a potential "Short Squeeze" (Liquidation Hunt).
  - **Asymmetric Risk/Reward Barriers:** Set Take Profit targets significantly wider than Stop Loss targets (e.g., TP = 4.0 ATR, SL = 1.5 ATR) to capture massive tail-risk moves while enduring whipsaws.

## 4. Macro-Economic Spreads (Solving GBPUSD & USDJPY)
- **Problem:** Driven heavily by Central Bank policies and Yield Differentials, not pure technical price action.
- **Solution:**
  - **Feature Integration:** Fetch US 10-Year Bond Yields (US10Y) and the Dollar Index (DXY).
  - Calculate Yield Differentials (e.g., US10Y vs JP10Y). The ML model learns to only take technical signals that align with the fundamental macro direction.