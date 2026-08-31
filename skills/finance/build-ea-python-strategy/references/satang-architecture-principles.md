# Satang's Python Brain + MT5 Muscle Framework

## Core Principles
When building quantitative trading systems for Satang:
1. **Separation of Concerns:** 
   - Colab/Jupyter for training models (XGBoost for probability/mean-reversion, LSTM for time-series).
   - Lightweight Python execution script for inference.
   - MT5 for data bridging and order execution only.
2. **The Risk Gatekeeper (Satang's Rules):**
   - **No Martingale:** Never increase position sizing to recover losses.
   - **ATR Position Sizing:** Dynamic lot sizing based on Volatility (ATR) and a fixed max % account risk per trade.
   - **Break-Even SL:** Auto-move Stop Loss to entry point once price moves 1R in favor.
   - **Daily Drawdown Limit:** System must halt immediately if daily PnL drops below a hard % threshold.

## Common Architecture Layout
```text
ai-mt5-trading-bot/
├── data/                  # Local historical data dump (.csv, .parquet)
├── models/                # Trained artifacts (.pkl, .onnx, .pth)
├── notebooks/             # Heavy lifting (Feature Eng, XGB/LSTM training)
└── src/
    ├── bot.py             # Main inference loop (polls MT5 -> Predicts -> Sends to Risk Manager)
    ├── config.py          # MT5 Credentials + Risk Parameters
    ├── data_processor.py  # Pandas-TA feature generator
    ├── mt5_client.py      # MetaTrader5 API Wrapper
    └── risk_manager.py    # The Satang Gatekeeper Class
```
