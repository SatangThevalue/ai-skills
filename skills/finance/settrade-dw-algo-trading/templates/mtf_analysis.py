import pandas as pd
import yfinance as yf
import warnings

warnings.filterwarnings('ignore')

class MultiTimeframeAnalyzer:
    def __init__(self, symbol_yf="PTT.BK"):
        self.symbol = symbol_yf
        self.data_store = {}

    def fetch_all_timeframes(self):
        # 1. Weekly Data
        df_weekly = yf.download(self.symbol, period="2y", interval="1wk", progress=False)
        self.data_store['weekly'] = self._clean_yf_data(df_weekly)
        
        # 2. Daily Data
        df_daily = yf.download(self.symbol, period="1y", interval="1d", progress=False)
        self.data_store['daily'] = self._clean_yf_data(df_daily)
        
        # 3. Hourly Data
        df_hourly = yf.download(self.symbol, period="1mo", interval="60m", progress=False)
        self.data_store['hourly'] = self._clean_yf_data(df_hourly)
        
        return self.data_store

    def _clean_yf_data(self, df):
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        df.dropna(inplace=True)
        return df

    def add_mtf_indicators(self):
        for tf, df in self.data_store.items():
            if len(df) >= 200:
                df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
            else:
                df['EMA_200'] = df['Close'].ewm(span=50, adjust=False).mean()
                
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    def analyze_mtf_confluence(self):
        self.add_mtf_indicators()
        
        cur_w = self.data_store['weekly'].iloc[-1]
        cur_d = self.data_store['daily'].iloc[-1]
        cur_h = self.data_store['hourly'].iloc[-1]
        
        is_macro_bullish = cur_w['Close'] > cur_w['EMA_200']
        is_daily_bullish = cur_d['MACD'] > cur_d['MACD_Signal']
        is_hourly_buy_signal = cur_h['EMA_20'] > cur_h['EMA_50']
        
        confluence_score = sum([is_macro_bullish, is_daily_bullish, is_hourly_buy_signal])

        print(f"MTF Confluence Score: {confluence_score}/3")
        if confluence_score == 3: return "STRONG BUY"
        elif is_macro_bullish and is_hourly_buy_signal: return "CAUTIOUS BUY"
        else: return "WAIT"

if __name__ == "__main__":
    analyzer = MultiTimeframeAnalyzer("PTT.BK")
    analyzer.fetch_all_timeframes()
    print("Action:", analyzer.analyze_mtf_confluence())
