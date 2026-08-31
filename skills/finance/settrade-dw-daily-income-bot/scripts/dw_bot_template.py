import sys
import os
import json
import time
from datetime import datetime, time as dtime
import pandas as pd
import numpy as np
import yfinance as yf
import pytz
from settrade_v2 import Investor
from settrade_v2.errors import SettradeError

# ==========================================
# ⚙️ CONFIGURATION & CREDENTIALS
# ==========================================
env_path = os.path.expanduser('~/.settrade.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

APP_ID = os.environ.get("SETTRADE_APP_ID", "YOUR_APP_ID")
APP_SECRET = os.environ.get("SETTRADE_APP_SECRET", "YOUR_APP_SECRET")
BROKER_ID = "SANDBOX"
APP_CODE = "SANDBOX"
ACCOUNT_NO = "YOUR_ACCOUNT"
PIN = "000000"

# 🎯 รายชื่อ DW ที่ต้องการเทรด
DW_SYMBOLS = [
    {"dw": "PTT01C2412A", "underlying": "PTT", "type": "CALL"},
    {"dw": "AOT01C2412A", "underlying": "AOT", "type": "CALL"},
    {"dw": "DELTA01P2412A", "underlying": "DELTA", "type": "PUT"}, 
    {"dw": "CPALL01C2412A", "underlying": "CPALL", "type": "CALL"}
]

# 💰 MONEY MANAGEMENT
MAX_POSITION_PCT = 0.10  
RISK_PER_TRADE_PCT = 0.02 

# ==========================================
# ⏰ 1. MARKET HOURS CHECK (เช็คเวลาตลาดไทย)
# ==========================================
def is_market_open():
    bkk_tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(bkk_tz)
    
    if now.weekday() >= 5:
        return False, "ตลาดปิด (วันหยุดเสาร์-อาทิตย์)"
        
    current_time = now.time()
    morning_open = dtime(10, 0)
    morning_close = dtime(12, 30)
    afternoon_open = dtime(14, 0)
    afternoon_close = dtime(16, 30)
    
    if (morning_open <= current_time <= morning_close) or (afternoon_open <= current_time <= afternoon_close):
        return True, "ตลาดเปิด (Market Open)"
    else:
        return False, "ตลาดปิด (นอกเวลาทำการ หรือ พักเที่ยง)"

# ==========================================
# 🌍 2. GLOBAL MACRO (เช็ค VIX Index)
# ==========================================
def check_global_sentiment():
    try:
        vix = yf.download("^VIX", period="5d", progress=False)
        if isinstance(vix.columns, pd.MultiIndex): vix.columns = vix.columns.droplevel(1)
        last_vix = float(vix['Close'].iloc[-1])
        
        if last_vix > 25:
            return "RISK_OFF", last_vix
        else:
            return "RISK_ON", last_vix
    except Exception as e:
        return "UNKNOWN", 0.0

# ==========================================
# 📊 3. TECHNICAL & ALGO LOGIC
# ==========================================
def calculate_adx(df, period=14):
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff(-1) * -1
    plus_dm[plus_dm < 0] = 0
    plus_dm[plus_dm < minus_dm] = 0
    minus_dm[minus_dm < 0] = 0
    minus_dm[minus_dm < plus_dm] = 0
    
    tr1 = df['High'] - df['Low']
    tr2 = np.abs(df['High'] - df['Close'].shift(1))
    tr3 = np.abs(df['Low'] - df['Close'].shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = tr.ewm(alpha=1/period, adjust=False).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/period, adjust=False).mean() / atr)
    minus_di = 100 * (minus_dm.ewm(alpha=1/period, adjust=False).mean() / atr)
    
    dx = (np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)) * 100
    adx = dx.ewm(alpha=1/period, adjust=False).mean()
    return adx.fillna(0)

def analyze_underlying(symbol, dw_type, sentiment):
    symbol_yf = f"{symbol}.BK"
    try:
        df = yf.download(symbol_yf, period="6mo", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)
        if df.empty: return "WAIT", "No Data", 0
        
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).ewm(alpha=1/14, adjust=False).mean()
        loss = -delta.where(delta < 0, 0).ewm(alpha=1/14, adjust=False).mean()
        rs = gain / (loss + 1e-10)
        df['RSI_14'] = 100 - (100 / (1 + rs))
        df['ADX'] = calculate_adx(df)
        
        curr = df.iloc[-1]
        action = "WAIT"
        reason = "Sideways หรือ ไม่มีสัญญาณที่ชัดเจน"
        strong_trend = curr['ADX'] > 25
        
        if dw_type == "CALL":
            if sentiment == "RISK_OFF":
                reason = "VIX พุ่งสูง (>25) ตลาดแพนิก ระงับการเล่น Call DW"
                action = "WAIT"
            elif strong_trend and (curr['EMA_20'] > curr['EMA_50']) and curr['RSI_14'] < 70:
                action = "BUY"
                reason = "หุ้นแม่เป็นขาขึ้นชัดเจน (ADX>25) + RSI ไม่ตึง"
            elif (curr['Close'] < curr['EMA_20']) or (curr['RSI_14'] > 75):
                action = "SELL"
                reason = "หลุด EMA20 หรือ RSI Overbought (ขายทำกำไร/คัตลอส)"
                
        elif dw_type == "PUT":
            if strong_trend and (curr['EMA_20'] < curr['EMA_50']) and curr['RSI_14'] > 30:
                action = "BUY"
                reason = "หุ้นแม่เป็นขาลงชัดเจน (ADX>25) เหมาะกับ Put DW"
            elif (curr['Close'] > curr['EMA_20']) or (curr['RSI_14'] < 25):
                action = "SELL"
                reason = "หุ้นแม่ทะลุ EMA20 ขึ้นมา หรือ RSI Oversold (ขายทำกำไร/คัตลอส)"

        return action, reason, float(curr['Close'])
    except Exception as e:
        return "WAIT", f"Error analyzing: {e}", 0

# ==========================================
# 🚀 4. MAIN EXECUTION LOOP
# ==========================================
def run_daily_income_bot():
    bkk_tz = pytz.timezone('Asia/Bangkok')
    print(f"[{datetime.now(bkk_tz).strftime('%Y-%m-%d %H:%M:%S')}] 🚀 เริ่มต้น DW Daily Income Bot")
    
    is_open, market_msg = is_market_open()
    print(f"⏰ สถานะตลาด: {market_msg}")
    
    # In production, uncomment the next 3 lines:
    # if not is_open:
    #     print("จบการทำงาน (รอตลาดเปิด)")
    #     return

    sentiment, vix_val = check_global_sentiment()
    print(f"🌍 สภาวะตลาดโลก (VIX): {vix_val:.2f} -> {sentiment}")
    
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
        held_stocks = {item.get('symbol'): item.get('actualVolume', 0) for item in portfolios.get('portfolioList', []) if item.get('symbol')}
        print(f"💰 เงินสด (Line Available): {real_line_available:,.2f} บาท")
    except Exception as e:
        print(f"❌ ดึงพอร์ตล้มเหลว: {e}")
        return

    for dw_item in DW_SYMBOLS:
        dw_symbol = dw_item['dw']
        underlying = dw_item['underlying']
        dw_type = dw_item['type']
        
        print(f"\n--- 🔍 สแกน DW: {dw_symbol} ({dw_type}) ---")
        
        held_volume = held_stocks.get(dw_symbol, 0)
        if held_volume > 0:
            print(f"📦 สถานะ: ถืออยู่ {held_volume:,.0f} หุ้น")
        else:
            print(f"📦 สถานะ: ว่างเปล่า")
            
        action, reason, ul_price = analyze_underlying(underlying, dw_type, sentiment)
        print(f"🧠 ตัดสินใจ: {action} | เหตุผล: {reason} (ราคาแม่: {ul_price:.2f})")
        
        dw_price = 0
        try:
            quote = market.get_quote_symbol(dw_symbol)
            dw_price = float(quote.get('last', 0))
        except:
            # Fallback for Sandbox Inactive MarketData
            dw_price = 0.50
            
        if dw_price <= 0: dw_price = 0.50

        if action == "BUY" and held_volume == 0:
            max_cap = real_line_available * MAX_POSITION_PCT
            max_risk = real_line_available * RISK_PER_TRADE_PCT
            allowed_loss_pct = 0.30
            
            shares_by_cap = max_cap / dw_price
            shares_by_risk = max_risk / (dw_price * allowed_loss_pct)
            
            shares_to_buy = int(min(shares_by_cap, shares_by_risk) // 100) * 100
            
            if shares_to_buy > 0:
                print(f"🛒 [EXECUTE] ยิงซื้อ {dw_symbol} จำนวน {shares_to_buy:,.0f} หุ้น (ราคาประเมิน {dw_price} ฿)")
                try:
                    res = equity.place_order(pin=PIN, side="Buy", symbol=dw_symbol, volume=shares_to_buy, price=0, price_type="MP-MKT", validity_type="FOK")
                    print(f"✅ สำเร็จ! Order No: {res.get('orderNo')}")
                    real_line_available -= (shares_to_buy * dw_price)
                except SettradeError as e:
                    print(f"❌ โบรกเกอร์ปฏิเสธ: {e.additional_info.get('error_description', str(e))}")
                    
        elif action == "SELL" and held_volume > 0:
            print(f"💸 [EXECUTE] ยิงขายทิ้ง {dw_symbol} จำนวน {held_volume:,.0f} หุ้น")
            try:
                res = equity.place_order(pin=PIN, side="Sell", symbol=dw_symbol, volume=held_volume, price=0, price_type="MP-MKT", validity_type="FOK")
                print(f"✅ สำเร็จ! Order No: {res.get('orderNo')}")
                real_line_available += (held_volume * dw_price)
            except SettradeError as e:
                print(f"❌ โบรกเกอร์ปฏิเสธ: {e.additional_info.get('error_description', str(e))}")

        time.sleep(1)

    print(f"\n[{datetime.now(bkk_tz).strftime('%Y-%m-%d %H:%M:%S')}] 🏁 จบการทำงาน DW Daily Income Bot!")

if __name__ == "__main__":
    run_daily_income_bot()