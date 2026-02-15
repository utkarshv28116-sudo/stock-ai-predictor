import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

st.set_page_config(page_title="IntelliVest AI", page_icon="🤖")

# Title
st.title("IntelliVest Stock Predictor")
st.write("Get AI-powered stock price predictions!")

# Stock selector
ticker = st.selectbox(
    "Choose a stock:",
    ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
)

# Load model and scaler
@st.cache_resource
def load_model_and_scaler(ticker):
    model_path = f'models/saved_models/lstm_{ticker}.h5'
    scaler_path = f'models/saved_models/scaler_{ticker}.pkl'
    
    if not os.path.exists(model_path):
        return None, None
    
    model = tf.keras.models.load_model(model_path)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler

model, scaler = load_model_and_scaler(ticker)

if model is None:
    st.error(f"❌ Model not found for {ticker}. Please train the model first!")
    st.info("Run: `python scripts/train_model.py`")
else:
    # Get latest stock data
    stock = yf.Ticker(ticker)
    df = stock.history(period='3mo')
    
    # Display current price
    current_price = df['Close'][-1]
    st.metric("Current Price", f"${current_price:.2f}")
    
    # Make prediction
    last_60_days = df['Close'][-60:].values.reshape(-1, 1)
    
    # Scale the data
    scaled = scaler.transform(last_60_days)
    
    # Reshape for prediction
    X_pred = scaled.reshape(1, 60, 1)
    
    # Predict
    prediction = model.predict(X_pred, verbose=0)
    predicted_price = scaler.inverse_transform(prediction)[0][0]
    
    # Calculate change
    price_change = predicted_price - current_price
    percent_change = (price_change / current_price) * 100
    
    # Display prediction
    st.header("Tomorrow's Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Predicted Price",
            f"${predicted_price:.2f}",
            f"{percent_change:+.2f}%"
        )
    
    with col2:
        st.metric(
            "Expected Change",
            f"${price_change:+.2f}"
        )
    
    # Show chart
    st.subheader(f"{ticker} Price History (Last 3 Months)")
    st.line_chart(df['Close'])
    
    # Disclaimer
    st.caption("⚠️ Not financial advice. For educational purposes only.")
    
    # Show some stats
    with st.expander("📊 More Info"):
        st.write(f"**Volume:** {df['Volume'][-1]:,.0f}")
        st.write(f"**52-Week High:** ${df['Close'].max():.2f}")
        st.write(f"**52-Week Low:** ${df['Close'].min():.2f}")