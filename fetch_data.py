import yfinance as yf
import pandas as pd
import json

tickers = ["0050.TW", "009816.TW", "006208.TW"]
result = {}

for t in tickers:
    try:
        # 抓取近 5 年數據供回測
        df = yf.download(t, period="5y", interval="1d", auto_adjust=True, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # 排除沒有交易數據的國定假日
        df = df.dropna()
        
        result[t] = {
            "dates": df.index.strftime('%Y-%m-%d').tolist(),
            "open": df['Open'].tolist(),
            "high": df['High'].tolist(),
            "low": df['Low'].tolist(),
            "close": df['Close'].tolist()
        }
    except Exception as e:
        print(f"Error fetching {t}: {e}")

# 寫入靜態 JSON 檔案
with open("market_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)
    
print("Market data updated successfully.")