import sys
import os
import pandas as pd
import yfinance as yf
import json
import time
from datetime import datetime
from settrade_v2 import Investor
from settrade_v2.errors import SettradeError
from adaptive_survival_system_v3 import AdaptiveSurvivalSystemV3

# ==========================================
# ⚙️ CONFIGURATION (Sandbox)
# ==========================================
APP_ID = "YOUR_APP_ID"
APP_SECRET="YOUR_APP_SECRET"
BROKER_ID = "SANDBOX"
APP_CODE = "SANDBOX"
ACCOUNT_NO = "YOUR_ACCOUNT"
PIN = "000000"

# List of DW symbols to scan (e.g., Call Warrants)
SYMBOLS = ["PTT01C2405A", "AOT01C2405A", "CPALL01C2405A"]

def run_dw_trading_bot():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 เริ่มต้น DW Trading Bot (สแกน {len(SYMBOLS)} DW)...")
    data_dir = os.path.expanduser('~')
    
    try:
        investor = Investor(app_id=APP_ID, app_secret=APP_SECRET, broker_id=BROKER_ID, app_code=APP_CODE, is_auto_queue=False)
        equity = investor.Equity(account_no=ACCOUNT_NO)
        market = investor.MarketData() 
        print("✅ ล็อกอิน Settrade Sandbox สำเร็จ!")
    except Exception as e:
        print(f"❌ ล็อกอินล้มเหลว: {e}")
        return

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
        print(f"❌ เกิดข้อผิดพลาดตอนดึงพอร์ต: {e}")
        return

    for dw_symbol in SYMBOLS:
        print(f"\n==========================================")
        print(f"🔍 วิเคราะห์และเทรด DW: {dw_symbol}")
        print(f"==========================================")
        
        # Extract Underlying Symbol (e.g., "PTT01C2405A" -> "PTT")
        underlying = ""
        for char in dw_symbol:
            if char.isalpha():
                underlying += char
            else:
                break
                
        underlying_yf = f"{underlying}.BK"
        state_file = os.path.join(data_dir, f"bot_state_{dw_symbol}.json")
        
        system = AdaptiveSurvivalSystemV3(state_file=state_file)
        system.current_capital = real_line_available
        
        held_volume = held_stocks.get(dw_symbol, {}).get('volume', 0)
        avg_cost = held_stocks.get(dw_symbol, {}).get('cost', 0.0)
        
        try:
            # 1. Fetch Underlying Graph (yfinance)
            df = yf.download(underlying_yf, period="1y", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            if df.empty:
                print(f"⚠️ ไม่พบข้อมูลกราฟหุ้นแม่ ข้าม DW ตัวนี้")
                continue
                
            analysis = system.analyze_market_state(df)
            action = analysis['Action']
            
            # 2. Fetch DW Price (Settrade MarketData)
            # NOTE: Fails with "User is inactive" in Sandbox outside market hours.
            dw_quote = market.get_quote_symbol(symbol=dw_symbol)
            dw_last_price = dw_quote.get('last', 0)
            
            if dw_last_price == 0:
                 print(f"⚠️ ดึงราคา {dw_symbol} ไม่ได้ หรือราคาเป็น 0")
                 continue
                 
            # 3. DW Position Sizing
            risk_amount = system.current_capital * system.base_risk_per_trade * system.current_risk_multiplier
            raw_shares = risk_amount / dw_last_price if dw_last_price > 0 else 0
            shares_to_buy = int(raw_shares // 100) * 100
            
            print(f"🧠 ระบบตัดสินใจหุ้นแม่: {action}")
            print(f"   ราคา DW {dw_symbol} ปัจจุบัน: {dw_last_price:.3f} บาท")
            
            if "BUY" in action and "C" in dw_symbol: # Call Warrant
                if held_volume == 0 and shares_to_buy > 0:
                    try:
                        order_res = equity.place_order(pin=PIN, side="Buy", symbol=dw_symbol, volume=shares_to_buy, price=0, price_type="MP-MKT", validity_type="FOK")
                        system.consecutive_losses = 0
                        real_line_available -= (shares_to_buy * dw_last_price)
                    except SettradeError as e:
                        print(f"❌ โบรกเกอร์ปฏิเสธคำสั่ง: {e.additional_info.get('error_description', str(e))}")
            elif "SELL" in action:
                if held_volume > 0:
                    try:
                        order_res = equity.place_order(pin=PIN, side="Sell", symbol=dw_symbol, volume=held_volume, price=0, price_type="MP-MKT", validity_type="FOK")
                        if dw_last_price < avg_cost:
                            system.consecutive_losses += 1
                        real_line_available += (held_volume * dw_last_price)
                    except SettradeError as e:
                        print(f"❌ โบรกเกอร์ปฏิเสธคำสั่ง: {e.additional_info.get('error_description', str(e))}")
            system.save_state()
        except Exception as e:
            print(f"❌ ระบบ Execution ล้มเหลวสำหรับ {dw_symbol}: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    run_dw_trading_bot()
