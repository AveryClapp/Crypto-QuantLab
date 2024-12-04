import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    df.dropna(inplace=True)
    return df

def preprocess_data(df, feature_column, target_column, time_step=60):
    data = df[[feature_column, target_column]].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)
    
    X, y = [], []
    for i in range(time_step, len(data_scaled)):
        X.append(data_scaled[i - time_step:i, 0])
        y.append(data_scaled[i, 1])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    return X, y, scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == '__main__':
    # Load and preprocess data
    datasets = ['./app/models/datasets/BTCUSDT_D1.csv']
    time_step = 60
    X_combined, y_combined, scalers = [], [], []
    
    for dataset in datasets:
        df = load_data(dataset)
        X, y, scaler = preprocess_data(df, feature_column='open', target_column='close', time_step=time_step)
        X_combined.append(X)
        y_combined.append(y)
        scalers.append(scaler)
    
    X_combined = np.vstack(X_combined)
    y_combined = np.concatenate(y_combined)
    
    # Split data into training and testing sets
    train_size = int(len(X_combined) * 0.8)
    X_train, X_test = X_combined[:train_size], X_combined[train_size:]
    y_train, y_test = y_combined[:train_size], y_combined[train_size:]
    
    # Build and train the LSTM model
    model = build_lstm_model((X_train.shape[1], 1))
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)
    
    # Evaluate the model
    predicted = model.predict(X_test)
    predicted = scalers[0].inverse_transform(np.concatenate([np.zeros_like(predicted), predicted], axis=1))[:, 1]
    y_test_unscaled = scalers[0].inverse_transform(np.concatenate([np.zeros_like(y_test.reshape(-1, 1)), y_test.reshape(-1, 1)], axis=1))[:, 1]
    
    # Visualize results
    plt.figure(figsize=(14, 5))
    plt.plot(y_test_unscaled, color='red', label='Actual BTC Price')
    plt.plot(predicted, color='blue', label='Predicted BTC Price')
    plt.title('Bitcoin Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('BTC Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig('btc_price_prediction.png')
    plt.show()
    
    # Save model and scaler
    model.save('lstm_btc_model.h5')
    joblib.dump(scalers[0], 'lstm_btc_scaler.joblib')
    
    print("Model training and evaluation completed. Check 'btc_price_prediction.png' for visualization.")
