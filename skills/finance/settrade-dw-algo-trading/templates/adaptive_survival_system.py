import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, time
import pytz
import warnings

warnings.filterwarnings('ignore')

class AdaptiveSurvivalSystemV3:
    def __init__(self, initial_capital=10000000, state_file="bot_state.json"):
        self.state_file = state_file
        self.initial_capital = initial_capital
        self.load_state()
        
        self.base_risk_per_trade = 0.01
        self.commission_rate = 0.00157
        
        self.current_risk_multiplier = 0.5 if self.consecutive_losses >= 3 else 1.0

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.current_capital = data.get('current_capital', self.initial_capital)
                    self.peak_capital = data.get('peak_capital', self.initial_capital)
                    self.consecutive_losses = data.get('consecutive_losses', 0)
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

    def is_market_open(self):
        bkk_tz = pytz.timezone('Asia/Bangkok')
        now = datetime.now(bkk_tz)
        if now.weekday() >= 5: return False, "ตลาดปิด (วันหยุดสุดสัปดาห์)"
        current_time = now.time()
        morning_open, morning_close = time(10, 0), time(12, 30)
        afternoon_open, afternoon_close = time(14, 30), time(16, 30)
        
        if morning_open <= current_time <= morning_close: return True, "ตลาดเปิด (ช่วงเช้า)"
        elif afternoon_open <= current_time <= afternoon_close: return True, "ตลาดเปิด (ช่วงบ่าย)"
        elif morning_close < current_time < afternoon_open: return False, "ตลาดปิด (พักเที่ยง)"
        else: return False, "ตลาดปิด (นอกเวลาทำการ)"

    def _calculate_atr(self, df, period=14):
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        return np.max(ranges, axis=1).rolling(period).mean()

    def _calculate_adx(self, df, period=14):
        plus_dm = df['High'].diff()
        minus_dm = df['Low'].diff(-1) * -1
        
        plus_dm[plus_dm < 0] = 0
        plus_dm[plus_dm < minus_dm] = 0
        minus_dm[minus_dm < 0] = 0
        minus_dm[minus_dm < plus_dm] = 0
        
        tr = self._calculate_atr(df, period=1)
        atr_smoothed = tr.ewm(alpha=1/period, adjust=False).mean()
        plus_di = 100 * (plus_dm.ewm(alpha=1/period, adjust=False).mean() / atr_smoothed)
        minus_di = 100 * (minus_dm.ewm(alpha=1/period, adjust=False).mean() / atr_smoothed)
        
        dx = (np.abs(plus_di - minus_di) / np.abs(plus_di + minus_di)) * 100
        adx = dx.ewm(alpha=1/period, adjust=False).mean()
        return adx.fillna(0)

    def add_indicators(self, df):
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).ewm(alpha=1/14, adjust=False).mean()
        loss = -delta.where(delta < 0, 0).ewm(alpha=1/14, adjust=False).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))
        
        df['MACD_Line'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD_Signal'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()

        df['BB_Mid'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Mid'] + (2 * bb_std)
        df['BB_Lower'] = df['BB_Mid'] - (2 * bb_std)

        df['ATR'] = self._calculate_atr(df)
        df['Vol_MA_20'] = df['Volume'].rolling(window=20).mean()
        df['ADX'] = self._calculate_adx(df)
        return df

    def analyze_market_state(self, df):
        df = self.add_indicators(df)
        current = df.iloc[-1]
        previous = df.iloc[-2]
        current_price = current['Close']
        
        is_uptrend = current_price > current['EMA_200']
        has_trend = current['ADX'] > 20 

        cond1_golden_trend = is_uptrend and has_trend and (previous['EMA_20'] <= previous['EMA_50'] and current['EMA_20'] > current['EMA_50']) and (current['MACD_Line'] > current['MACD_Signal'])
        near_ema50 = current['EMA_50'] * 0.985 <= current_price <= current['EMA_50'] * 1.015
        cond2_buy_dip = is_uptrend and near_ema50 and (current['RSI_14'] < 40)
        cond3_breakout = has_trend and (current_price > current['BB_Upper']) and (current['Volume'] > current['Vol_MA_20'] * 1.5) and (current['RSI_14'] < 70)
        
        stop_loss_distance = current['ATR'] * 2.5 
        stop_loss_price = current_price - stop_loss_distance
        
        exit1_stop_loss = current_price < stop_loss_price
        exit2_take_profit = (current_price >= current['BB_Upper']) and (current['RSI_14'] > 70)
        exit3_trend_break = (current['EMA_20'] < current['EMA_50']) 

        action = "WAIT"
        reason = "No clear entry/exit signal or Sideways market"
        
        if exit2_take_profit:
            action = "SELL (TAKE PROFIT)"
            reason = "BB Upper Hit + RSI Overbought"
        elif exit3_trend_break:
            action = "SELL (CUT/EXIT)"
            reason = "Trend Breakdown (EMA 20 < 50)"
        elif cond1_golden_trend:
            action = "BUY"
            reason = "Golden Trend Entry"
        elif cond2_buy_dip:
            action = "BUY"
            reason = "Buy the Dip Entry"
        elif cond3_breakout:
            action = "BUY"
            reason = "Volatility Breakout Entry"

        risk_amount = self.current_capital * self.base_risk_per_trade * self.current_risk_multiplier
        raw_shares = (risk_amount / stop_loss_distance) if stop_loss_distance > 0 else 0
        shares_to_buy = int(raw_shares // 100) * 100
        
        position_value = shares_to_buy * current_price
        estimated_commission = position_value * self.commission_rate
        total_cost = position_value + estimated_commission

        if total_cost > self.current_capital:
            max_value_can_buy = self.current_capital / (1 + self.commission_rate)
            shares_to_buy = int((max_value_can_buy / current_price) // 100) * 100
            total_cost = (shares_to_buy * current_price) * (1 + self.commission_rate)

        self.save_state()

        return {
            "Date": current.name.strftime('%Y-%m-%d'),
            "Close": current_price,
            "Action": action,
            "Reason": reason,
            "Execution": {
                "Shares_to_Buy": shares_to_buy,
                "Stop_Loss": stop_loss_price
            }
        }
