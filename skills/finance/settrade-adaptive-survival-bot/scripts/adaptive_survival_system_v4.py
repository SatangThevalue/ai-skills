import pandas as pd
import numpy as np
import yfinance as yf
import warnings
import json
import os
from datetime import datetime, time as dtime
import pytz

warnings.filterwarnings('ignore')

SET_UNIVERSE = [
    "ADVANC.BK","AOT.BK","BDMS.BK","BEM.BK","BGRIM.BK","BH.BK","BJC.BK","BTS.BK",
    "CBG.BK","CENTRAL.BK","CK.BK","CPALL.BK","CPF.BK","CPN.BK","DELTA.BK","EA.BK",
    "EGCO.BK","GLOBAL.BK","GPSC.BK","GULF.BK","HMPRO.BK","INTUCH.BK","IRPC.BK",
    "ITD.BK","IVL.BK","KBANK.BK","KTB.BK","KTC.BK","LH.BK","MINT.BK","MTC.BK",
    "OR.BK","OSP.BK","PTT.BK","PTTEP.BK","PTTGC.BK","RATCH.BK","SAWAD.BK",
    "SCB.BK","SCGP.BK","SCC.BK","TISCO.BK","TLI.BK","TOP.BK","TRUE.BK",
    "TTB.BK","TU.BK","WHA.BK","BBL.BK","BCP.BK",
    "AP.BK","AMATA.BK","ANAN.BK","AWC.BK","BAM.BK","BANPU.BK","BCH.BK",
    "BEAUTY.BK","BTW.BK","COM7.BK","DOHOME.BK","ERW.BK","ESSO.BK",
    "GFPT.BK","GLAND.BK","GVREIT.BK","HUMANICA.BK","JASIF.BK",
    "JMT.BK","KTIS.BK","LPN.BK","MAJOR.BK","MAKRO.BK","ONEE.BK",
    "ORI.BK","PLANB.BK","PSH.BK","RS.BK","SAT.BK","SE.BK",
    "SPALI.BK","SPCG.BK","STEC.BK","STGT.BK","TPIPP.BK","TQM.BK","VGI.BK"
]

class SETMarketScanner:
    def __init__(self):
        self.raw_data = {}

    def _safe_value(self, val):
        try:
            return float(val)
        except:
            return None

    def fetch_and_filter(self):
        print(f"📥 กำลังดาวน์โหลดข้อมูล Daily ของ {len(SET_UNIVERSE)} หุ้นพร้อมกัน (Batch)...")
        raw = yf.download(SET_UNIVERSE, period="1y", interval="1d", progress=False, group_by='ticker')
        candidates = []
        for symbol in SET_UNIVERSE:
            try:
                df = raw[symbol].dropna()
                if len(df) < 50: continue
                close = df['Close']
                volume = df['Volume']
                ema200 = close.ewm(span=min(200, len(close)-1), adjust=False).mean()
                delta = close.diff()
                gain = delta.where(delta > 0, 0).ewm(alpha=1/14, adjust=False).mean()
                loss = -delta.where(delta < 0, 0).ewm(alpha=1/14, adjust=False).mean()
                rsi = 100 - (100 / (1 + (gain / loss)))
                vol_ma20 = volume.rolling(20).mean()
                
                cur_close = self._safe_value(close.iloc[-1])
                cur_ema200 = self._safe_value(ema200.iloc[-1])
                cur_rsi = self._safe_value(rsi.iloc[-1])
                cur_vol = self._safe_value(volume.iloc[-1])
                cur_vol_ma = self._safe_value(vol_ma20.iloc[-1])
                
                if None in [cur_close, cur_ema200, cur_rsi, cur_vol, cur_vol_ma]: continue
                
                if cur_close > cur_ema200 and cur_vol > cur_vol_ma * 1.2 and 30 < cur_rsi < 70:
                    candidates.append({
                        'symbol': symbol,
                        'close': cur_close,
                        'rsi': cur_rsi,
                        'vol_ratio': cur_vol / cur_vol_ma,
                        'pct_above_ema200': (cur_close - cur_ema200) / cur_ema200 * 100
                    })
            except:
                continue
        print(f"✅ Pre-Filter: เหลือ {len(candidates)} หุ้น")
        return candidates

class AdaptiveSurvivalSystemV4:
    def __init__(self, initial_capital=10000000, state_file="bot_state_v4.json"):
        self.state_file = state_file
        self.initial_capital = initial_capital
        self.load_state()
        self.base_risk_per_trade = 0.01
        self.commission_rate = 0.00157
        self.current_risk_multiplier = 0.5 if self.consecutive_losses >= 3 else 1.0
        self.mtf_data = {}

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    d = json.load(f)
                    self.current_capital = d.get('current_capital', self.initial_capital)
                    self.peak_capital = d.get('peak_capital', self.initial_capital)
                    self.consecutive_losses = d.get('consecutive_losses', 0)
            except:
                self._reset_state()
        else:
            self._reset_state()

    def _reset_state(self):
        self.current_capital = self.initial_capital
        self.peak_capital = self.initial_capital
        self.consecutive_losses = 0

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({
                'current_capital': self.current_capital,
                'peak_capital': self.peak_capital,
                'consecutive_losses': self.consecutive_losses,
                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=4)

    def fetch_market_data(self, symbol):
        self.symbol = symbol
        df_w = yf.download(symbol, period="2y", interval="1wk", progress=False)
        df_d = yf.download(symbol, period="1y", interval="1d", progress=False)
        df_h = yf.download(symbol, period="1mo", interval="60m", progress=False)
        self.mtf_data['weekly'] = self._clean(df_w)
        self.mtf_data['daily'] = self._clean(df_d)
        self.mtf_data['hourly'] = self._clean(df_h)

    def _clean(self, df):
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df.dropna()

    def _calculate_atr(self, df, period=14):
        hl = df['High'] - df['Low']
        hc = np.abs(df['High'] - df['Close'].shift())
        lc = np.abs(df['Low'] - df['Close'].shift())
        return pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(period).mean()

    def _calculate_adx(self, df, period=14):
        pdm = df['High'].diff().clip(lower=0)
        ndm = (-df['Low'].diff()).clip(lower=0)
        pdm[pdm < ndm] = 0
        ndm[ndm < pdm] = 0
        tr = self._calculate_atr(df, period=1)
        atr_s = tr.ewm(alpha=1/period, adjust=False).mean()
        pdi = 100 * (pdm.ewm(alpha=1/period, adjust=False).mean() / atr_s)
        ndi = 100 * (ndm.ewm(alpha=1/period, adjust=False).mean() / atr_s)
        dx = (np.abs(pdi - ndi) / np.abs(pdi + ndi)) * 100
        return dx.ewm(alpha=1/period, adjust=False).mean().fillna(0)

    def add_indicators(self, df):
        n = len(df)
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=min(200, n-1), adjust=False).mean()
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).ewm(alpha=1/14, adjust=False).mean()
        loss = -delta.where(delta < 0, 0).ewm(alpha=1/14, adjust=False).mean()
        df['RSI_14'] = 100 - (100 / (1 + (gain / loss)))
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD_Line'] = ema12 - ema26
        df['MACD_Signal'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
        df['BB_Mid'] = df['Close'].rolling(20).mean()
        df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(20).std()
        df['ATR'] = self._calculate_atr(df)
        df['Vol_MA_20'] = df['Volume'].rolling(20).mean()
        df['ADX'] = self._calculate_adx(df)
        return df

    def analyze_market_state(self):
        df_w = self.add_indicators(self.mtf_data['weekly'])
        df_d = self.add_indicators(self.mtf_data['daily'])
        df_h = self.add_indicators(self.mtf_data['hourly'])

        cur_w = df_w.iloc[-1]
        cur_d = df_d.iloc[-1]
        prv_d = df_d.iloc[-2]
        cur_h = df_h.iloc[-1]
        current_price = float(cur_h['Close'])

        macro_up  = float(cur_w['Close']) > float(cur_w['EMA_200'])
        trending  = float(cur_d['ADX']) > 20
        h_moment  = float(cur_h['MACD_Line']) > float(cur_h['MACD_Signal'])

        c1 = (float(prv_d['EMA_20']) <= float(prv_d['EMA_50'])) and (float(cur_d['EMA_20']) > float(cur_d['EMA_50']))
        c2 = (float(cur_d['EMA_50']) * 0.985 <= float(cur_d['Close']) <= float(cur_d['EMA_50']) * 1.015) and (float(cur_d['RSI_14']) < 40)
        c3 = (float(cur_d['Close']) > float(cur_d['BB_Upper'])) and (float(cur_d['Volume']) > float(cur_d['Vol_MA_20']) * 1.5)

        sl_dist = float(cur_d['ATR']) * 2.5
        sl_price = float(cur_d['Close']) - sl_dist

        score = 0
        if macro_up: score += 2 
        if trending: score += 1
        if h_moment: score += 1
        if c1 or c2 or c3: score += 1

        action, reason = "WAIT", "ไม่มีสัญญาณที่ชัดเจน"

        if not macro_up:
            action = "WAIT (MACRO BEARISH)"
            reason = "ภาพใหญ่ (Weekly) ยังเป็นขาลง"
        elif float(cur_d['EMA_20']) < float(cur_d['EMA_50']):
            action = "SELL"
            reason = "เทรนด์รายวันพลิกขาลง"
        elif (float(cur_h['Close']) >= float(cur_h['BB_Upper'])) and (float(cur_h['RSI_14']) > 70):
            action = "SELL (TP)"
            reason = "ราคาชนกรอบบน Bollinger 1H + RSI ตึง"
        elif trending and c1 and h_moment:
            action = "STRONG BUY"
            reason = "MTF Confluence ครบ 3 ชั้น (W+D+H)"
        elif c2 and h_moment:
            action = "BUY (DIP)"
            reason = "ย่อมาที่แนวรับ EMA50 + รายชั่วโมงเริ่มดีด"
        elif trending and c3 and h_moment:
            action = "BUY (BREAKOUT)"
            reason = "Breakout + Volume ยืนยัน + MTF หนุน"

        shares, total_cost, est_comm = 0, 0, 0
        if "BUY" in action and sl_dist > 0:
            risk_amt = self.current_capital * self.base_risk_per_trade * self.current_risk_multiplier
            shares = int((risk_amt / sl_dist) // 100) * 100
            val = shares * current_price
            est_comm = val * self.commission_rate
            total_cost = val + est_comm
            if total_cost > self.current_capital:
                max_val = self.current_capital / (1 + self.commission_rate)
                shares = int((max_val / current_price) // 100) * 100
                total_cost = shares * current_price * (1 + self.commission_rate)
                est_comm = total_cost - (shares * current_price)

        return {
            "Symbol": self.symbol,
            "Current_Price": current_price,
            "Action": action,
            "Reason": reason,
            "Score": score,
            "MTF": {
                "Weekly_Uptrend": macro_up,
                "Daily_Trending": trending,
                "Hourly_Momentum": h_moment
            },
            "Execution": {
                "Shares": shares,
                "Total_Cost": total_cost,
                "Commission": est_comm,
                "Stop_Loss": sl_price
            }
        }
