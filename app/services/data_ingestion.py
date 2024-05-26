from app.data import get_data
from dotenv import load_dotenv
import os
import requests

def validate_ticker(ticker: str):
    load_dotenv()
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'bestMatches' in data and len(data['bestMatches']) > 0:
            best_match = data['bestMatches'][0]['1. symbol']
            if best_match is None:
                raise ValueError(f'Ticker {ticker} is not valid')
            elif best_match.lower() != ticker.lower():
                raise ValueError(f'Ticker {ticker} is not valid. Did you mean {best_match}?')
            else:
                return best_match
        else:
            raise ValueError(f'Ticker {ticker} is not valid')
    else:
        raise ValueError(f'Error occurred while validating ticker: {response.status_code}')
    

def setup(ticker: str):
    # Validate the ticker
    try:
        validate_ticker(ticker)
    except ValueError as e:
        return str(e)
    
    # Begin the data ingestion process



    return f"Retrieved data for {ticker} successfully!"
