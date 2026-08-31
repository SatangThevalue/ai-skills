import sys
import os
import json
import pytz
from datetime import datetime, time as dtime

# Add local paths so the bot can find the V4 module
sys.path.insert(0, '/home/thaieasyvps')
sys.path.insert(0, os.path.expanduser('~/.hermes/scripts'))

from settrade_v2 import Investor
from settrade_v2.errors import SettradeError
from adaptive_survival_system_v4 import AdaptiveSurvivalSystemV4, SETMarketScanner

# ==========================================
# ⚙️ CONFIG — Sandbox Credentials
# ==========================================
APP_ID       = "MSqUZuOvJlnV7Wrj"
APP_SECRET   = "AP6FRjAgWX6yEyue4CUBDCTqpG/0mJvC6TqFoGgArsZ+"
BROKER_ID    = "SANDBOX"
APP_CODE     = "SANDBOX"
ACCOUNT_NO   = "satang-E"
PIN          = "000000"
STATE_FILE   = "/home/thaieasyvps/sandbox_bot_state.json"

# ==========================================
# 🕒 HELPERS
# ==========================================
def now_bkk():
    return datetime.now(pytz.timezone('Asia/Bangkok'))

def is_market_open(now):
    if now.weekday() >= 5:
        return False, "ตลาดปิด (วันหยุดสุดสัปดาห์)"
    t = now.time()
    
    if dtime(10, 0) <= t <= dtime(12, 30):
        return True, f"ตลาดเปิด ช่วงเช้า ({t.strftime('%H:%M')})"
    elif dtime(14, 30) <= t <= dtime(16, 30):
        return True, f"ตลาดเปิด ช่วงบ่าย ({t.strftime('%H:%M')})"
    elif dtime(9, 55) <= t < dtime(10, 0):
        return False, f"ตลาดเตรียมเปิด Pre-Open เช้า ({t.strftime('%H:%M')})"
    elif dtime(14, 25) <= t < dtime(14, 30):
        return False, f"ตลาดเตรียมเปิด Pre-Open บ่าย ({t.strftime('%H:%M')})"
    elif dtime(16, 30) < t <= dtime(16, 40):
        return False, f"ตลาดเตรียมปิด Pre-Close ({t.strftime('%H:%M')})"
    elif dtime(12, 30) < t < dtime(14, 25):
        return False, f"ตลาดพักเที่ยง ({t.strftime('%H:%M')})"
    else:
        return False, f"นอกเวลาทำการ ({t.strftime('%H:%M')})"

def log(msg):
    print(f"[{now_bkk().strftime('%H:%M:%S')}] {msg}")

def divider(title=""):
    if title:
        pad = (52 - len(title)) // 2
        print("="*pad + f" {title} " + "="*pad)
    else:
        print("="*55)

# ==========================================
# 🔐 STEP 1 — AUTHENTICATION
# ==========================================
def connect_broker():
    try:
        investor = Investor(
            app_id=APP_ID,
            app_secret=APP_SECRET,
            broker_id=BROKER_ID,
            app_code=APP_CODE,
            is_auto_queue=False
        )
        equity = investor.Equity(account_no=ACCOUNT_NO)
        log("✅ ล็อกอิน Settrade Sandbox สำเร็จ!")
        return equity
    except Exception as e:
        log(f"❌ ล็อกอินล้มเหลว: {e}")
        return None

# ==========================================
# 📂 STEP 2 — SYNC PORTFOLIO
# ==========================================
def sync_portfolio(equity):
    try:
        acc   = equity.get_account_info()
        port  = equity.get_portfolios()
        cash  = acc.get('lineAvailable', 0)
        
        holdings = {}
        for item in port.get('portfolioList', []):
            sym = item.get('symbol', '')
            vol = item.get('actualVolume', 0)
            avg = item.get('averagePrice', 0.0)
            if sym and vol > 0:
                holdings[sym] = {'volume': vol, 'avg_cost': avg}

        log(f"💰 เงินสดที่ซื้อได้: {cash:,.2f} บาท")
        if holdings:
            for sym, info in holdings.items():
                log(f"📦 ถือหุ้น {sym}: {info['volume']:,.0f} หุ้น (ทุน {info['avg_cost']:.2f} บาท)")
        else:
            log("📦 พอร์ตว่างเปล่า (ไม่มีหุ้น)")

        return cash, holdings

    except Exception as e:
        log(f"❌ ซิงค์พอร์ตล้มเหลว: {e}")
        return 0, {}

# ==========================================
# ⚡ STEP 3 — EXECUTE ORDER
# ==========================================
def place_buy(equity, symbol, shares, price, pin=PIN):
    try:
        res = equity.place_order(
            pin=pin,
            side="Buy",
            symbol=symbol,
            volume=shares,
            price=0,
            price_type="MP-MKT",
            validity_type="Day"
        )
        order_no = res.get('orderNo', 'N/A')
        log(f"✅ BUY {symbol} {shares:,} หุ้น @ Market — Order No: {order_no}")
        return True, order_no
    except SettradeError as e:
        desc = str(e)
        log(f"❌ โบรกเกอร์ Reject: {desc}")
        return False, desc
    except Exception as e:
        log(f"❌ Place Order Error: {e}")
        return False, str(e)

def place_sell(equity, symbol, shares, pin=PIN):
    try:
        res = equity.place_order(
            pin=pin,
            side="Sell",
            symbol=symbol,
            volume=shares,
            price=0,
            price_type="MP-MKT",
            validity_type="Day"
        )
        order_no = res.get('orderNo', 'N/A')
        log(f"✅ SELL {symbol} {shares:,} หุ้น @ Market — Order No: {order_no}")
        return True, order_no
    except SettradeError as e:
        desc = str(e)
        log(f"❌ โบรกเกอร์ Reject: {desc}")
        return False, desc
    except Exception as e:
        log(f"❌ Place Order Error: {e}")
        return False, str(e)

# ==========================================
# 🚀 MAIN — FULL TRADING LOOP
# ==========================================
def run():
    now = now_bkk()
    divider()
    print(f"  🤖 SANDBOX BOT V4 — {now.strftime('%Y-%m-%d %H:%M:%S')}")
    divider()

    market_open, market_msg = is_market_open(now)
    log(f"🕒 {market_msg}")

    equity = connect_broker()
    if equity is None:
        return

    cash, holdings = sync_portfolio(equity)

    divider("MARKET SCAN")
    log("🔍 Layer 1: Pre-filter ทั้งตลาด SET...")
    scanner = SETMarketScanner()
    candidates = scanner.fetch_and_filter()

    if not candidates:
        log("⚠️ ไม่มีหุ้นผ่านด่าน Pre-filter วันนี้")
        return

    log(f"🧠 Layer 2: MTF Analysis V4 กับ {len(candidates)} หุ้น...")
    system = AdaptiveSurvivalSystemV4(
        initial_capital=cash if cash > 0 else 10_000_000,
        state_file=STATE_FILE
    )
    system.current_capital = cash if cash > 0 else system.current_capital

    results  = []
    sell_list = []

    for idx, c in enumerate(candidates):
        sym = c['symbol']
        sym_settrade = sym.replace('.BK', '')   

        try:
            system.fetch_market_data(sym)
            res = system.analyze_market_state()
            res['symbol_settrade'] = sym_settrade
            res['vol_ratio']       = c['vol_ratio']

            action_icon = ("🟢" if "BUY"  in res['Action'] else
                           "🔴" if "SELL" in res['Action'] else "🟡")
            print(f"  [{idx+1:02d}/{len(candidates)}] {action_icon} {sym:<15} "
                  f"Score:{res['Score']}/5  {res['Action']:<22} {res['Reason'][:35]}")

            if "BUY" in res['Action']:
                results.append(res)
            if "SELL" in res['Action']:
                sell_list.append(res)

        except Exception as e:
            print(f"  [{idx+1:02d}/{len(candidates)}] ⚠️  {sym:<15} ข้าม ({e})")

    results.sort(key=lambda x: (x['Score'], x['vol_ratio']), reverse=True)
    top3 = results[:3]

    divider("TOP PICKS")
    if top3:
        for rank, r in enumerate(top3, 1):
            sym_yf = r['Symbol']
            sym_st = r['symbol_settrade']
            print(f"\n#{rank} 🎯 {sym_yf}  [{r['Action']}]  Score {r['Score']}/5")
            print(f"   ราคา     : {r['Current_Price']:.2f} บาท")
            print(f"   เหตุผล   : {r['Reason']}")
            print(f"   MTF      : 1W={'✅' if r['MTF']['Weekly_Uptrend'] else '❌'}  "
                  f"1D={'✅' if r['MTF']['Daily_Trending'] else '❌'}  "
                  f"1H={'✅' if r['MTF']['Hourly_Momentum'] else '❌'}")
            if r['Execution']['Shares'] > 0:
                print(f"   แผนซื้อ  : {r['Execution']['Shares']:,} หุ้น "
                      f"(งบ {r['Execution']['Total_Cost']:,.0f} บาท "
                      f"+ ค่าคอม {r['Execution']['Commission']:,.0f} บาท)")
                print(f"   Stop Loss: {r['Execution']['Stop_Loss']:.2f} บาท")
    else:
        log("🟡 ไม่มีสัญญาณซื้อผ่านเกณฑ์ MTF วันนี้")

    if sell_list:
        log(f"🔴 หุ้นที่ควรระวัง: {', '.join([r['Symbol'] for r in sell_list])}")

    divider("EXECUTION")

    if not market_open:
        log("💤 ตลาดปิด — บันทึกผลการวิเคราะห์เท่านั้น ไม่ยิงคำสั่ง")
        system.save_state()
        divider()
        return

    executed_buy  = []
    executed_sell = []

    for sym_st, info in holdings.items():
        sym_yf   = sym_st + ".BK"
        held_vol = info['volume']
        avg_cost = info['avg_cost']

        match = next((r for r in sell_list if r['Symbol'] == sym_yf), None)
        if match:
            log(f"🔴 {sym_yf} → ระบบสั่ง {match['Action']}: {match['Reason']}")
            ok, order_no = place_sell(equity, sym_st, held_vol)
            if ok:
                if match['Current_Price'] < avg_cost:
                    system.consecutive_losses += 1
                else:
                    system.consecutive_losses = 0
                executed_sell.append({'symbol': sym_st, 'order_no': order_no})
        else:
            log(f"⏳ {sym_yf} ยังไม่มีสัญญาณออก — HOLD ต่อไป")

    for r in top3:
        sym_yf   = r['Symbol']
        sym_st   = r['symbol_settrade']
        shares   = r['Execution']['Shares']
        total_cost = r['Execution']['Total_Cost']

        if sym_st in holdings:
            log(f"⏳ {sym_yf} มีในพอร์ตแล้ว {holdings[sym_st]['volume']:,} หุ้น — HOLD")
            continue

        if shares <= 0:
            log(f"⚠️ {sym_yf} เงินสดไม่เพียงพอ (ต้องการ {total_cost:,.0f} บาท)")
            continue

        if total_cost > cash:
            log(f"⚠️ {sym_yf} เงินสดไม่พอ (มี {cash:,.0f} / ต้องการ {total_cost:,.0f} บาท)")
            continue

        log(f"🟢 {sym_yf} → ระบบสั่ง {r['Action']}: {r['Reason']}")
        ok, order_no = place_buy(equity, sym_st, shares, r['Current_Price'])
        if ok:
            cash -= total_cost 
            system.consecutive_losses = 0
            executed_buy.append({'symbol': sym_st, 'shares': shares, 'order_no': order_no})

    divider("SUMMARY")
    print(f"  ✅ คำสั่งซื้อที่ส่งออก  : {len(executed_buy)} รายการ")
    print(f"  ✅ คำสั่งขายที่ส่งออก  : {len(executed_sell)} รายการ")
    print(f"  💰 เงินสดคงเหลือ (ประมาณ): {cash:,.2f} บาท")
    print(f"  ⚙️  ตัวคูณความเสี่ยง    : {system.current_risk_multiplier}x "
          f"(แพ้ติดกัน {system.consecutive_losses} ครั้ง)")

    system.current_capital = cash
    system.save_state()
    log("💾 บันทึก State สำเร็จ")
    divider()

if __name__ == "__main__":
    run()