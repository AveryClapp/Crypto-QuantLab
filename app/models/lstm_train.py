import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import Tuple, List

class CryptoDataset(Dataset):
        def __init__(self, data: np.ndarray, sequence_length: int):
                self.data = torch.FloatTensor(data)
                self.sequence_length = sequence_length
        def __len__(self) -> int:
                return len(self.data) - self.sequence_length

        def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
                sequence = self.data[idx:idx + self.sequence_length]
                target = self.data[idx + self.sequence_length]
                return sequence, target

class LSTMPredictor(nn.Module):
        def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, dropout: float):
                super().__init__()
                self.lstm = nn.LSTM(
                        input_size=input_dim,
                        hidden_size=hidden_dim,
                        num_layers=num_layers,
                        dropout=dropout,
                        batch_first=True
                )
                self.linear = nn.Linear(hidden_dim, 1)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
                lstm_out, _ = self.lstm(x)
                predictions = self.linear(lstm_out[:, -1, :])
                return predictions

class CryptoPricePredictor:
        def __init__(self, sequence_length: int = 60, hidden_dim: int = 64, 
                num_layers: int = 2, dropout: float = 0.2):
                self.sequence_length = sequence_length
                self.hidden_dim = hidden_dim
                self.num_layers = num_layers
                self.dropout = dropout
                self.scaler = MinMaxScaler()
                self.model = None
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        def prepare_data(self, df: pd.DataFrame) -> Tuple[DataLoader, DataLoader]:
                """Prepare data for training and validation"""
                # Scale the data
                scaled_data = self.scaler.fit_transform(df[['close', 'volume', 'rsi', 'sma', 'upper_band', 'lower_band']].values)

                # Split into train and validation
                train_size = int(len(scaled_data) * 0.8)
                train_data = scaled_data[:train_size]
                val_data = scaled_data[train_size:]

                # Create datasets
                train_dataset = CryptoDataset(train_data, self.sequence_length)
                val_dataset = CryptoDataset(val_data, self.sequence_length)

                # Create dataloaders
                train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
                val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

                return train_loader, val_loader

        def train(self, train_loader: DataLoader, val_loader: DataLoader, 
                epochs: int = 100, learning_rate: float = 0.001) -> List[float]:
                """Train the LSTM model"""
                input_dim = next(iter(train_loader))[0].shape[2]
                self.model = LSTMPredictor(
                        input_dim=input_dim,
                        hidden_dim=self.hidden_dim,
                        num_layers=self.num_layers,
                        dropout=self.dropout
                ).to(self.device)

                criterion = nn.MSELoss()
                optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)

                train_losses = []
                val_losses = []

                for epoch in range(epochs):
                        # Training phase
                        self.model.train()
                        train_loss = 0
                        for sequences, targets in train_loader:
                                sequences = sequences.to(self.device)
                                targets = targets[:, 0].to(self.device)  # We only predict the close price

                                optimizer.zero_grad()
                                outputs = self.model(sequences).squeeze()
                                loss = criterion(outputs, targets)
                                loss.backward()
                                optimizer.step()
                                train_loss += loss.item()

                        # Validation phase
                        self.model.eval()
                        val_loss = 0
                        with torch.no_grad():
                                for sequences, targets in val_loader:
                                        sequences = sequences.to(self.device)
                                        targets = targets[:, 0].to(self.device)
                                        outputs = self.model(sequences).squeeze()
                                        val_loss += criterion(outputs, targets).item()

                        train_loss = train_loss / len(train_loader)
                        val_loss = val_loss / len(val_loader)
                        train_losses.append(train_loss)
                        val_losses.append(val_loss)

                        if (epoch + 1) % 10 == 0:
                                print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

                return train_losses, val_losses

        def predict(self, df: pd.DataFrame) -> np.ndarray:
                """Make predictions using the trained model"""
                self.model.eval()
                scaled_data = self.scaler.transform(df[['close', 'volume', 'rsi', 'sma', 'upper_band', 'lower_band']].values)
                dataset = CryptoDataset(scaled_data, self.sequence_length)
                dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

                predictions = []
                with torch.no_grad():
                        for sequence, _ in dataloader:
                                sequence = sequence.to(self.device)
                                output = self.model(sequence)
                                predictions.append(output.cpu().numpy())

                return np.array(predictions).squeeze()

        def save_model(self, path: str):
                """Save the trained model"""
                torch.save({
                        'model_state_dict': self.model.state_dict(),
                        'scaler': self.scaler
                }, path)

        def load_model(self, path: str):
                """Load a trained model"""
                checkpoint = torch.load(path)
                input_dim = 6  # number of features
                self.model = LSTMPredictor(
                        input_dim=input_dim,
                        hidden_dim=self.hidden_dim,
                        num_layers=self.num_layers,
                        dropout=self.dropout
                ).to(self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.scaler = checkpoint['scaler']
if __name__ == '__main__':
        predictor = CryptoPricePredictor(
        sequence_length=60,  # Number of time steps to look back
        hidden_dim=64,      # Size of LSTM hidden layer
        num_layers=2,       # Number of LSTM layers
        dropout=0.2         # Dropout rate for regularization
        )

        # Prepare data and train the model
        train_loader, val_loader = predictor.prepare_data(df)
        train_losses, val_losses = predictor.train(
        train_loader, 
        val_loader,
        epochs=100,
        learning_rate=0.001
        )

        # Make predictions
        predictions = predictor.predict(df)

        # Save the trained model
        predictor.save_model('crypto_lstm_model.pth')
