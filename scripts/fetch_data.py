import yfinance as yf
import pandas as pd
import os

# Create directories if they don't exist
os.makedirs('data/raw', exist_ok=True)

def fetch_stock_data(ticker, period='10y'):
    """Download stock data from Yahoo Finance"""
    print(f"Downloading {ticker}...")
    
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    # Save to CSV
    filename = f'data/raw/{ticker}.csv'
    df.to_csv(filename)
    
    print(f"✅ Saved {ticker} to {filename}")
    print(f"   {len(df)} days of data downloaded")
    return df

if __name__ == "__main__":
    tickers = [
    # Mega Tech (Most Popular)
    'AAPL',   # Apple
    'GOOGL',  # Google
    'MSFT',   # Microsoft
    'AMZN',   # Amazon
    'META',   # Facebook/Meta
    'NVDA',   # NVIDIA
    'TSLA',   # Tesla
    # Popular Stocks
    'NFLX',   # Netflix
    'COIN',   # Coinbase (crypto)
    'DIS',    # Disney
    # Finance
    'JPM',    # JP Morgan
    'V',      # Visa
    # ETFs (Most Important)
    'SPY',    # S&P 500
    'QQQ',    # Nasdaq 100
    'VOO',     # Vanguard S&P 500
    'AMD'
]
    
    print("Starting download...")
    print("-" * 50)
    
    for ticker in tickers:
        try:
            fetch_stock_data(ticker)
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
    
    print("-" * 50)
    print("Download complete!")
			
			
			
			
			
			
			
			
			
			
