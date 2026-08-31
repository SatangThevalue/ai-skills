import pandas as pd
import numpy as np
from settrade_v2 import Investor # ตัวอย่างสามารถปรับไปใช้ mt5linux สำหรับ Forex ได้

class PairTradingEngine:
    def __init__(self, symbol_A, symbol_B, lookback_window=50):
        self.symA = symbol_A
        self.symB = symbol_B
        self.window = lookback_window
        
        # Parameters เทียบเท่า Farm Index & Sync Rate
        self.z_score_entry_high = 2.0   # Farm Index +200
        self.z_score_entry_low = -2.0   # Farm Index -200
        self.z_score_exit = 0.5         # จุดปิดทำกำไร (เข้าใกล้ 0)
        self.z_score_stop = 4.0         # จุดตัดขาดทุน (ความสัมพันธ์พัง)
        self.min_correlation = 0.70     # Sync Rate ขั่นต่ำ 70%

    def calculate_pair_indicators(self, df_A, df_B):
        """
        รวม DataFrame ของสินทรัพย์ A และ B เข้าด้วยกัน แล้วคำนวณ Z-Score และ Correlation
        df_A และ df_B ต้องมีคอลัมน์ 'Close'
        """
        # จับคู่เวลาให้ตรงกัน (Inner Join)
        df = pd.DataFrame()
        df['Close_A'] = df_A['Close']
        df['Close_B'] = df_B['Close']
        df = df.dropna()
        
        if len(df) < self.window:
            raise ValueError("ข้อมูลน้อยเกินไปสำหรับการคำนวณ Rolling Window")

        # 1. คำนวณ Correlation (เทียบเท่า Sync Rate)
        df['Correlation'] = df['Close_A'].rolling(window=self.window).corr(df['Close_B'])

        # 2. คำนวณ Spread (A - B)
        # หมายเหตุ: ของจริงอาจต้องปรับมูลค่า (Hedge Ratio) ให้เท่ากันก่อน 
        # เช่น เอาราคามาทำ Normalization ก่อนลบกัน
        df['Spread'] = df['Close_A'] - df['Close_B']

        # 3. คำนวณ Z-Score (เทียบเท่า Farm Index)
        spread_mean = df['Spread'].rolling(window=self.window).mean()
        spread_std = df['Spread'].rolling(window=self.window).std()
        df['Z_Score'] = (df['Spread'] - spread_mean) / (spread_std + 1e-9) # บวก 1e-9 ป้องกันส่วนเป็นศูนย์

        return df

    def analyze_signal(self, current_data, has_open_position=False, current_position_type=None):
        """
        current_data: แถวล่าสุดจาก DataFrame ที่คำนวณ Indicator แล้ว
        """
        z_score = current_data['Z_Score']
        correlation = current_data['Correlation']
        
        # เช็ค Sync Rate
        if correlation < self.min_correlation and not has_open_position:
            return "WAIT", f"ความสัมพันธ์ต่ำเกินไป (Corr: {correlation:.2f})"

        # โหมดไม่มี Position (หาจุดเข้า)
        if not has_open_position:
            if z_score >= self.z_score_entry_high:
                return "ENTRY_SHORT_SPREAD", f"Z-Score ทะลุ {z_score:.2f} (A แพง B ถูก) -> SELL A, BUY B"
            elif z_score <= self.z_score_entry_low:
                return "ENTRY_LONG_SPREAD", f"Z-Score หลุด {z_score:.2f} (A ถูก B แพง) -> BUY A, SELL B"
            else:
                return "WAIT", f"Z-Score อยู่ในกรอบปกติ ({z_score:.2f})"
                
        # โหมดมี Position แล้ว (หาจุดออก)
        else:
            # Cut Loss ถ้าราคาฉีกออกไปไกลเกินเยียวยา หรือความสัมพันธ์พังทลาย
            if abs(z_score) >= self.z_score_stop or correlation < 0.5:
                return "EXIT_CUTLOSS", f"Z-Score ทะลุ Stop Loss หรือความสัมพันธ์พัง -> ปิดทุกออเดอร์"

            # Take Profit เมื่อราคาวิ่งกลับมาหากัน (Mean Reversion)
            if current_position_type == "SHORT_SPREAD" and z_score <= self.z_score_exit:
                return "EXIT_TAKEPROFIT", f"Z-Score กลับมาสมดุล ({z_score:.2f}) -> ปิดกำไร"
            
            elif current_position_type == "LONG_SPREAD" and z_score >= -self.z_score_exit:
                return "EXIT_TAKEPROFIT", f"Z-Score กลับมาสมดุล ({z_score:.2f}) -> ปิดกำไร"

            return "HOLD", f"รอให้ Z-Score ({z_score:.2f}) วิ่งกลับเข้าหา 0"

# วิธีการใช้งาน
if __name__ == "__main__":
    # สมมติฐาน: โหลด Data ของ EURUSD และ GBPUSD มาเป็น Pandas DataFrame
    # df_eurusd = ...
    # df_gbpusd = ...
    
    engine = PairTradingEngine("EURUSD", "GBPUSD", lookback_window=50)
    print("โหลดโครงสร้าง Pair Trading Engine สำเร็จ!")
