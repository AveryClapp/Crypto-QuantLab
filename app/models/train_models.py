import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib
from datetime import datetime

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])  # Convert 'date' to datetime
    df.set_index('datetime', inplace=True)  # Set 'date' as index
    df.dropna(inplace=True)
    return df

def select_features(df):
    features = df[['open', 'volume']]  # Changed to lowercase to match your data
    target = df['close']
    return features, target

def split_data(features, target, test_size=0.2, random_state=42):
    return train_test_split(features, target, test_size=test_size, random_state=random_state)

def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return y_pred, mse, r2

if __name__ == '__main__':
    datasets = ['./app/models/datasets/BTCUSDT_D1.csv']
    X_combined = pd.DataFrame()
    y_combined = pd.Series()

    for dataset in datasets:
        df = load_data(dataset)
        X, y = select_features(df)  # Use the select_features function
        X_combined = pd.concat([X_combined, X], axis=0)
        y_combined = pd.concat([y_combined, y], axis=0)

    # Split the combined data
    X_train, X_test, y_train, y_test = split_data(X_combined, y_combined)

    # Scale the features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # Train the model
    model = train_model(X_train_scaled, y_train)

    # Evaluate the model
    y_pred, mse, r2 = evaluate_model(model, X_test_scaled, y_test)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Save the model and scaler
    joblib.dump(model, 'test_btc_model.joblib')
    joblib.dump(scaler, 'test_btc_scaler.joblib')

    # Plot actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Close Price')
    plt.ylabel('Predicted Close Price')
    plt.title('Actual vs Predicted Close Prices')
    plt.tight_layout()
    plt.savefig('actual_vs_predicted.png')
    plt.close()

    print("Model training and evaluation completed. Check 'actual_vs_predicted.png' for visualization.")

# Example of how to use the saved model for predictions
# loaded_model = joblib.load('test_btc_model.joblib')
# loaded_scaler = joblib.load('test_btc_scaler.joblib')
# new_data = pd.read_csv('new_crypto_data.csv')
# new_features = new_data[['open', 'high', 'low', 'volume']]
# new_features_scaled = loaded_scaler.transform(new_features)
# predictions = loaded_model.predict(new_features_scaled)
# print("Predictions:", predictions)