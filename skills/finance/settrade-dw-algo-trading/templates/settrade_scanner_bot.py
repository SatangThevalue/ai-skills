import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from settrade_v2 import Investor
from settrade_v2.errors import SettradeError

# Import your custom trading engine
# from adaptive_survival_system_v3 import AdaptiveSurvivalSystemV3

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
BROKER_ID = "SANDBOX"
APP_CODE = "SANDBOX"
ACCOUNT_NO = "YOUR_ACCOUNT"
PIN = "000000"

# List of stocks to scan
SYMBOLS = ["PTT", "AOT", "CPALL", "ADVANC", "DELTA"]

def run_scanner_bot():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Started Scanner Trading Bot for {len(SYMBOLS)} stocks...")
    
    # 1. Initialize Broker
    try:
        investor = Investor(app_id=APP_ID, app_secret=APP_SECRET, broker_id=BROKER_ID, app_code=APP_CODE, is_auto_queue=False)
        equity = investor.Equity(account_no=ACCOUNT_NO)
    except Exception as e:
        print(f"Login failed: {e}")
        return

    # 2. Fetch Portfolio & Line Available ONCE before loop
    try:
        acc_info = equity.get_account_info()
        real_line_available = acc_info.get('lineAvailable', 0)
        
        portfolios = equity.get_portfolios()
        held_stocks = {}
        for item in portfolios.get('portfolioList', []):
            sym = item.get('symbol')
            if sym:
                held_stocks[sym] = {'volume': item.get('actualVolume', 0), 'cost': item.get('averagePrice', 0.0)}
    except Exception as e:
        print(f"Failed to fetch portfolio: {e}")
        return

    # 3. Scanning Loop
    for symbol in SYMBOLS:
        print(f"\n--- Scanning {symbol} ---")
        symbol_yf = f"{symbol}.BK"
        state_file = f"bot_state_{symbol}.json" # PER-SYMBOL state tracking
        
        # Initialize strategy engine per symbol
        # system = AdaptiveSurvivalSystemV3(state_file=state_file)
        # system.current_capital = real_line_available # Local capital simulation
        
        held_volume = held_stocks.get(symbol, {}).get('volume', 0)
        avg_cost = held_stocks.get(symbol, {}).get('cost', 0.0)
            
        try:
            df = yf.download(symbol_yf, period="1y", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            if df.empty:
                continue
                
            # Dummy analysis call (replace with real strategy)
            # analysis = system.analyze_market_state(df)
            # action = analysis['Action']
            # shares_to_buy = analysis['Execution']['Shares_to_Buy']
            # last_price = analysis['Close']
            
            action = "WAIT"
            shares_to_buy = 0
            last_price = 0.0
            
            # Execute
            if "BUY" in action and held_volume == 0 and shares_to_buy > 0:
                try:
                    order_res = equity.place_order(pin=PIN, side="Buy", symbol=symbol, volume=shares_to_buy, price=0, price_type="MP-MKT", validity_type="FOK")
                    # system.consecutive_losses = 0
                    
                    # Prevent over-allocation on next symbol by simulating cash deduction
                    real_line_available -= (shares_to_buy * last_price)
                except SettradeError as e:
                    print(f"Order Rejected: {e.additional_info.get('error_description', str(e))}")
                    
            elif "SELL" in action and held_volume > 0:
                try:
                    order_res = equity.place_order(pin=PIN, side="Sell", symbol=symbol, volume=held_volume, price=0, price_type="MP-MKT", validity_type="FOK")
                    # if last_price < avg_cost:
                    #     system.consecutive_losses += 1
                        
                    # Add back to available cash for next symbol
                    real_line_available += (held_volume * last_price)
                except SettradeError as e:
                    print(f"Order Rejected: {e.additional_info.get('error_description', str(e))}")
                    
            # system.save_state()
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            
        # API Rate Limit Protection: Wait before next symbol
        time.sleep(1)

if __name__ == "__main__":
    run_scanner_bot()