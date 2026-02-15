import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
import pickle
import tensorflow as tf
from tensorflow import keras

print("SCRIPT STARTED!")

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
    Prepare data for LSTM training
    
    Args:
        df: DataFrame with stock data
        lookback: number of days to look back
    
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    # Get close prices
    data = df['Close'].values.reshape(-1, 1)
    
    # Scale data to 0-1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Create sequences
    X = []
    y = []
    
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i, 0])
        y.append(scaled_data[i, 0])
    
    X = np.array(X)
    y = np.array(y)
    
    # Reshape for LSTM [samples, timesteps, features]
    X = X.reshape(X.shape[0], X.shape[1], 1)
    
    # Split into train and test (80/20)
    split = int(0.8 * len(X))
    X_train = X[:split]
    X_test = X[split:]
    y_train = y[:split]
    y_test = y[split:]
    
    return X_train, X_test, y_train, y_test, scaler

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
    model = build_lstm_model((X_train.shape[1], 1))
    print(f"✅ Built LSTM model")
    
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

if __name__ == "__main__":
    # Train models for all stocks
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
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