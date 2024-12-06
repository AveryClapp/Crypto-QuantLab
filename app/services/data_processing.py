import pandas as pd
import sys
sys.path.append("/Users/averyclapp/Documents/Coding Stuff/GitProjects/AICryptoPlatform/app")
from models.lstm_train import CryptoPricePredictor
from typing import Tuple, List
import numpy as np

def prepare_features(df: pd.DataFrame, rsi_period: int = 14, sma_period: int = 20, bb_period: int = 20, bb_std: int = 2) -> pd.DataFrame:
    df = df.copy()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    df['sma'] = df['close'].rolling(window=sma_period).mean()
    
    df['std'] = df['close'].rolling(window=bb_period).std()
    df['upper_band'] = df['sma'] + (bb_std * df['std'])
    df['lower_band'] = df['sma'] - (bb_std * df['std'])
    
    df['volume'] = df['volume'] / df['volume'].rolling(window=20).mean()
    
    df = df.dropna()
    
    required_columns = [
        'close',
        'volume',
        'rsi',
        'sma',
        'upper_band',
        'lower_band'
    ]
    
    return df[required_columns]

def main(df):
    prepared_data = prepare_features(df)
    
    predictor = CryptoPricePredictor()
    
    train_loader, val_loader = predictor.prepare_data(prepared_data)
    
    train_losses, val_losses = predictor.train(
        train_loader, 
        val_loader,
        epochs=100,
        learning_rate=0.001
    )
    
    predictions = predictor.predict(prepared_data)
    print(predictions)    
    predictor.save_model('crypto_lstm_model.pth')

if __name__ == "__main__":
    df= pd.read_csv("../models/datasets/BTCUSDT_D1.csv")
        
    # Convert datetime to proper format if needed
    df['datetime'] = pd.to_datetime(df['datetime'])
                    
    # Convert column names to lowercase for consistency
    df.columns = df.columns.str.lower()
    main(df)
