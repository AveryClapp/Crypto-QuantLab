import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib

#Load and Clean Data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)
    return df

#Select Desired Features
def select_features(df):
    features = df[['Open', 'High', 'Low', 'Volume']]
    target = df['Close']
    return features, target

def split_data(feature, target, test_size=0.2, random_state=42):
    return train_test_split(feature, target, test_size=test_size, random_state=random_state)

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
    datasets = ['crypto_data_1.csv', 'crypto_data_2.csv', 'crypto_data_3.csv']
    X_combined = pd.DataFrame()
    y_combined = pd.Series()

    for dataset in datasets:
        df = load_data(dataset)
        X = df.drop('target_column', axis=1)
        y = df['target_column']
        X_combined = pd.concat([X_combined, X], axis=0)
        y_combined = pd.concat([y_combined, y], axis=0)

    # Split the combined data
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    mse, r2 = evaluate_model(model, X_test, y_test)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Save the model
    joblib.dump(model, 'random_forest_crypto_model.joblib')

    # # Later, to load the model and make predictions:
    # loaded_model = joblib.load('random_forest_crypto_model.joblib')

    # # Assume 'new_data' is a DataFrame with the same features used during training
    # new_data = pd.read_csv('current_crypto_data.csv')
    # predictions = loaded_model.predict(new_data)

    print("Predictions:", predictions)