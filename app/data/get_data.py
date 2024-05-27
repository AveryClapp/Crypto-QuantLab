import requests
import os
from bs4 import BeautifulSoup

'''
finance.yahoo.com/quote/{ticker}
google.com/search?q={ticker}+stock
cnn.com/markets/stocks/{ticker}
google.com/finance/quote/{ticker}:NASDAQ
'''

def fetch_data(ticker: str):
    urls = {
        'yahoo': f'https://finance.yahoo.com/quote/{ticker}',
        'google': f'https://google.com/search?q={ticker}+stock',
        'cnn': f'https://cnn.com/markets/stocks/{ticker}',
        'google_finance': f'https://google.com/finance/quote/{ticker}:NASDAQ'
    }
    data = {}
    for key in urls:
        response = requests.get(urls[key])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data[key] = soup
        else:
            data[key] = None
    return data