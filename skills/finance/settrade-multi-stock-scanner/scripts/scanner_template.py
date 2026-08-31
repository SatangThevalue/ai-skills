import sys
import os
# Resolve module paths for cronjob execution
sys.path.append(os.path.expanduser('~'))

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
APP_SECRET = "YOUR_APP_SECRET"
BROKER_ID = "SANDBOX"
APP_CODE = "SANDBOX"
ACCOUNT_NO = "YOUR_ACCOUNT"
PIN = "000000"

SYMBOLS = ["PTT", "AOT", "CPALL"]

def run_trading_bot():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 เริ่มต้นกระบวนการ Full Loop Trading Bot (สแกน {len(SYMBOLS)} หุ้น)...")
    data_dir = os.path.expanduser('~')
    
    try:
        investor = Investor(app_id=APP_ID, app_secret=APP_SECRET, broker_id=BROKER_ID, app_code=APP_CODE, is_auto_queue=False)
        equity = investor.Equity(account_no=ACCOUNT_NO)
        print("✅ ล็อกอิน Settrade Sandbox สำเร็จ!")
    except Exception as e:
        print(f"❌ ล็อกอินล้มเหลว: {e}")
        return

    try:
        acc_info = equity.get_account_info()
        real_line_available = acc_info.get('lineAvailable', 0)
        print(f"💰 เงินสดที่ซื้อได้ (Line Available): {real_line_available:,.2f} บาท")
        
        portfolios = equity.get_portfolios()
        held_stocks = {}
        for item in portfolios.get('portfolioList', []):
            sym = item.get('symbol')
            if sym:
                held_stocks[sym] = {'volume': item.get('actualVolume', 0), 'cost': item.get('averagePrice', 0.0)}
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดตอนดึงพอร์ต: {e}")
        return

    for symbol in SYMBOLS:
        print(f"\n==========================================")
        print(f"🔍 วิเคราะห์และเทรดหุ้น: {symbol}")
        print(f"==========================================")
        symbol_yf = f"{symbol}.BK"
        state_file = os.path.join(data_dir, f"bot_state_{symbol}.json")
        
        system = AdaptiveSurvivalSystemV3(state_file=state_file)
        system.current_capital = real_line_available
        
        held_volume = held_stocks.get(symbol, {}).get('volume', 0)
        avg_cost = held_stocks.get(symbol, {}).get('cost', 0.0)
        
        if held_volume > 0:
            print(f"📦 สถานะพอร์ต: มีหุ้น {symbol} อยู่ {held_volume:,.0f} หุ้น (ทุนเฉลี่ย {avg_cost:.2f})")
        else:
            print(f"📦 สถานะพอร์ต: ว่างเปล่า (ไม่มีหุ้น {symbol})")
            
        print("📥 กำลังดึงข้อมูลกราฟล่าสุด...")
        try:
            df = yf.download(symbol_yf, period="1y", progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            if df.empty:
                print(f"⚠️ ไม่พบข้อมูลกราฟ ข้ามหุ้นตัวนี้")
                continue
                
            analysis = system.analyze_market_state(df)
            action = analysis['Action']
            shares_to_buy = analysis['Execution']['Shares_to_Buy']
            last_price = analysis['Close']
            
            print(f"🧠 ระบบตัดสินใจ: {action}")
            print(f"   เหตุผล: {analysis.get('Reason', 'ไม่มีข้อมูลเหตุผล')}")
            print(f"   ราคาตลาดล่าสุด: {last_price:.2f} บาท")
            
            if "BUY" in action:
                if held_volume == 0:
                    if shares_to_buy > 0:
                        print(f"🛒 [EXECUTE] สั่งซื้อ {symbol} จำนวน {shares_to_buy:,.0f} หุ้น ที่ราคาตลาด (Market Price)...")
                        try:
                            order_res = equity.place_order(pin=PIN, side="Buy", symbol=symbol, volume=shares_to_buy, price=0, price_type="MP-MKT", validity_type="FOK")
                            print(f"✅ ยิงคำสั่งสำเร็จ! Order No: {order_res.get('orderNo', 'N/A')}")
                            system.consecutive_losses = 0
                            real_line_available -= (shares_to_buy * last_price)
                        except SettradeError as e:
                            print(f"❌ โบรกเกอร์ปฏิเสธคำสั่ง: {e.additional_info.get('error_description', str(e))}")
                    else:
                        print("⚠️ ไม่สามารถซื้อได้: เงินสดไม่พอ หรือคำนวณ Board Lot ไม่ได้")
                else:
                    print("⏳ มีหุ้นในพอร์ตอยู่แล้ว: ข้ามการซื้อ (ถือ Let Profit Run)")
                    
            elif "SELL" in action:
                if held_volume > 0:
                    print(f"💸 [EXECUTE] สั่งขาย {symbol} ทั้งหมด {held_volume:,.0f} หุ้น ทิ้งที่ราคาตลาด...")
                    try:
                        order_res = equity.place_order(pin=PIN, side="Sell", symbol=symbol, volume=held_volume, price=0, price_type="MP-MKT", validity_type="FOK")
                        print(f"✅ ยิงคำสั่งสำเร็จ! Order No: {order_res.get('orderNo', 'N/A')}")
                        if last_price < avg_cost:
                            system.consecutive_losses += 1
                            print(f"📉 บันทึกการขาดทุน (Consecutive Losses: {system.consecutive_losses})")
                        real_line_available += (held_volume * last_price)
                    except SettradeError as e:
                        print(f"❌ โบรกเกอร์ปฏิเสธคำสั่ง: {e.additional_info.get('error_description', str(e))}")
                else:
                    print("⏳ ไม่มีหุ้นให้ขาย (พอร์ตว่างเปล่า)")
            else:
                print("⏳ นั่งทับมือ: ไม่มีแอคชั่นใดๆ ให้ทำในรอบนี้")
                    
            system.save_state()
            print(f"💾 บันทึก State ของ {symbol} สำเร็จ!")
            
        except Exception as e:
            print(f"❌ ระบบ Execution ล้มเหลวสำหรับ {symbol}: {e}")
            
        time.sleep(1)

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🏁 จบการทำงาน Full Loop ทั้ง {len(SYMBOLS)} หุ้น!")

if __name__ == "__main__":
    run_trading_bot()
