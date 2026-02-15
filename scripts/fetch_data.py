import yfinance as yf
import pandas as pd

# Download 5 years of stock data
def fetch_stock_data(ticker, period='5y'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.to_csv(f'data/raw/{ticker}.csv')
    print(f"Downloaded {ticker} data!")
    return df

# Download multiple stocks
tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
for ticker in tickers:
    fetch_stock_data(ticker)
		
			
			
			
			
			
			
			
			
			
			
