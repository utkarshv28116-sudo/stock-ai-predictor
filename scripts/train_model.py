import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
import pickle
import tensorflow as tf
from tensorflow import keras



def build_lstm_model(input_shape):
    """Build LSTM model for stock price prediction"""
    model = keras.Sequential([
        keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
        keras.layers.Dropout(0.2),
        keras.layers.LSTM(50, return_sequences=True),
        keras.layers.Dropout(0.2),
        keras.layers.LSTM(50),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Rest of your code stays the same...

def prepare_data(df, lookback=60):
    """
    Prepare data with MULTIPLE features
    """
    # Create technical indicators
    df['MA_20'] = df['Close'].rolling(window=20).mean()  # Moving average
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['Close'], 14)  # Relative Strength Index
    df['Volume_Change'] = df['Volume'].pct_change()
    
    # Use multiple features, not just Close
    data = df['Close'].values.reshape(-1, 1)
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Create sequences
    X = []
    y = []
    
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i, :])  # All features
        y.append(scaled_data[i, 0])  # Predict Close price
    
    X = np.array(X)
    y = np.array(y)
    X = np.array(X)
    y = np.array(y)

# ADD THESE LINES HERE:
# Split into train and test (80/20)
    split = int(0.8 * len(X))
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]


    return X_train, X_test, y_train, y_test, scaler

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def train_stock_model(ticker, epochs=50, batch_size=32):
    """
    Train LSTM model for a specific stock
    
    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL')
        epochs: Number of training epochs
        batch_size: Training batch size
    """
    print(f"\n{'='*60}")
    print(f"Training model for {ticker}")
    print(f"{'='*60}\n")
    
    # Load data
    df = pd.read_csv(f'data/raw/{ticker}.csv', index_col=0)
    print(f"✅ Loaded {len(df)} days of data")
    
    # Prepare data
    X_train, X_test, y_train, y_test, scaler = prepare_data(df)
    print(f"✅ Prepared data: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples")
    
    # Build model
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))  
    # Use the actual shape from the data
    input_shape = (X_train.shape[1], X_train.shape[2])
    print(f"📊 Input shape: {input_shape}")
    model = build_lstm_model(input_shape)
    
    # Train model
    print(f"\n🚀 Training... (this takes 2-5 minutes)")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate
    train_loss = history.history['loss'][-1]
    test_loss = history.history['val_loss'][-1]
    
    print(f"\n{'='*60}")
    print(f"✅ Training complete!")
    print(f"   Final training loss: {train_loss:.6f}")
    print(f"   Final test loss: {test_loss:.6f}")
    print(f"{'='*60}\n")
    
    # Save model
    os.makedirs('models/saved_models', exist_ok=True)
    model_path = f'models/saved_models/lstm_{ticker}.h5'
    model.save(model_path)
    print(f"💾 Saved model to: {model_path}")
    
    # Save scaler (IMPORTANT!)
    scaler_path = f'models/saved_models/scaler_{ticker}.pkl'
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"💾 Saved scaler to: {scaler_path}")
    
    return model, scaler

tickers = [
        'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'NVDA', 'TSLA',
        'NFLX', 'COIN', 'DIS', 'JPM', 'V', 'SPY', 'QQQ', 'VOO','AMD',
    ]
    
print("\n" + "="*60)
print("STARTING TRAINING FOR ALL STOCKS")
print("="*60)
    
for ticker in tickers:
    try:
        train_stock_model(ticker, epochs=20, batch_size=32)
    except Exception as e:
        print(f"\n❌ Error training {ticker}: {e}\n")
    
    print("\n" + "="*60)
    print("✅ ALL TRAINING COMPLETE!")
    print("="*60)