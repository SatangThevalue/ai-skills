import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from settrade_v2 import Investor
from adaptive_survival_system import AdaptiveSurvivalSystemV3

APP_ID = "YOUR_APP_ID"
APP_SECRET="YOUR_SECRET"
BROKER_ID = "SANDBOX"
APP_CODE = "SANDBOX"
ACCOUNT_NO = "satang-E"
PIN = "000000"

TARGET_SYMBOL_SETTRADE = "PTT"
TARGET_SYMBOL_YF = "PTT.BK"

def run_trading_bot():
    print(f"[{datetime.now()}] 🚀 Init Trading Bot...")
    system = AdaptiveSurvivalSystemV3(state_file="bot_state.json")
    
    if not system.is_market_open()[0]:
        print("Market is closed. Exiting.")
        return

    try:
        investor = Investor(app_id=APP_ID, app_secret=APP_SECRET, broker_id=BROKER_ID, app_code=APP_CODE, is_auto_queue=False)
        equity = investor.Equity(account_no=ACCOUNT_NO)
    except Exception as e:
        print(f"Auth Failed: {e}")
        return

    # 1. Sync Portfolio
    acc_info = equity.get_account_info()
    system.current_capital = acc_info.get('lineAvailable', system.current_capital)
    
    portfolios = equity.get_portfolios()
    held_volume, avg_cost = 0, 0.0
    for item in portfolios.get('portfolioList', []):
        if item.get('symbol') == TARGET_SYMBOL_SETTRADE:
            held_volume = item.get('actualVolume', 0)
            avg_cost = item.get('averagePrice', 0.0)

    # 2. Feed & Analyze
    df = yf.download(TARGET_SYMBOL_YF, period="1y", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    analysis = system.analyze_market_state(df)
    action = analysis['Action']
    shares_to_buy = analysis['Execution']['Shares_to_Buy']
    last_price = analysis['Close']
    
    print(f"Action: {action} | Reason: {analysis['Reason']} | Market Price: {last_price}")

    # 3. Execute
    try:
        if "BUY" in action and held_volume == 0 and shares_to_buy > 0:
            res = equity.place_order(pin=PIN, side="Buy", symbol=TARGET_SYMBOL_SETTRADE, volume=shares_to_buy, price=0, price_type="MP-MKT", validity_type="Day")
            system.consecutive_losses = 0
            print(f"BUY Executed: {res}")
        elif "SELL" in action and held_volume > 0:
            res = equity.place_order(pin=PIN, side="Sell", symbol=TARGET_SYMBOL_SETTRADE, volume=held_volume, price=0, price_type="MP-MKT", validity_type="Day")
            if last_price < avg_cost:
                system.consecutive_losses += 1
            print(f"SELL Executed: {res}")
    except Exception as e:
        print(f"Execution Error: {e}")

    # 4. Save State
    system.save_state()

if __name__ == "__main__":
    run_trading_bot()
