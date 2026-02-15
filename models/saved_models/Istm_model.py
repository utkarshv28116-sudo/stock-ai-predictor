import tensorflow as tf
from tensorflow import keras

def build_lstm_model(input_shape):
    """
    Build LSTM model for stock price prediction
    
    Args:
        input_shape: tuple (timesteps, features) - e.g. (60, 1)
    
    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        # First LSTM layer
        keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
        keras.layers.Dropout(0.2),
        
        # Second LSTM layer
        keras.layers.LSTM(50, return_sequences=True),
        keras.layers.Dropout(0.2),
        
        # Third LSTM layer
        keras.layers.LSTM(50),
        keras.layers.Dropout(0.2),
        
        # Output layer
        keras.layers.Dense(1)
    ])
    
    # Compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    return model

if __name__ == "__main__":
    # Test the model
    model = build_lstm_model((60, 1))
    model.summary()
    print("\n✅ Model architecture looks good!")
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
