import requests
import os
import os.path
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
import pandas as pd
import json
from datetime import datetime as dt

# Market trends can look at dominance at https://www.coingecko.com/en/coins/{crypto} <- crypto symbol not necessarily required.

def main(crypto):    
    path = f'./app/data/csvs/{crypto}.csv'
    if not os.path.exists(path):
        print('table does not exist')
        with open(path, "w") as file:
            file.write("Time,Price,Daily Volume,Daily Volume Change,Market Cap,1D Delta,7D Delta,BTC Inflow,BTC Outflow,F&G\n")
        print('crypto file created')
    time = dt.utcnow().strftime("%m-%d-%Y %H:%M:%S")
    # market_cap, price, daily_change, weekly_change, daily_volume, daily_volume_change = coinmarketcap_data(crypto)
    btc_inflow = market_trends(crypto)



def coinmarketcap_data(crypto):
    load_dotenv('./app/core/.env')
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api = os.getenv('CMC_KEY')
    parameters = { 'slug': f'{crypto}', 'convert': 'USD' }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api
    }
    try:
        response = requests.get(url, params=parameters, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        # Process the received data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the API request: {e}")
        raise RuntimeException("Error occurred while making CMC API request")
        # Handle the error appropriately
    market_cap = data['data']['1']['quote']['USD']['market_cap']
    price = data['data']['1']['quote']['USD']['price']
    daily_change = data['data']['1']['quote']['USD']['percent_change_24h']
    weekly_change = data['data']['1']['quote']['USD']['percent_change_7d']
    daily_volume = data['data']['1']['quote']['USD']['volume_24h']
    daily_volume_change = data['data']['1']['quote']['USD']['volume_change_24h']
    return market_cap, price, daily_change, weekly_change, daily_volume, daily_volume_change

def market_trends(crypto):
    body = requests.get('https://www.binance.com/en/square/fear-and-greed-index')
    soup = BeautifulSoup(body.text, 'html.parser')
    fear_and_greed = soup.find(class_="css-cxlpc6").text
    return fear_and_greed

if __name__ == "__main__":
    main("ethereum")

