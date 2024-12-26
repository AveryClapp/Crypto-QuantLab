import requests
import os
import os.path
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd
import json
from datetime import datetime as dt
import boto3
import io
from app.database import get_db
from app.models import FinancialData


load_dotenv()
db = get_db()

def main(crypto):
    try:
        time = dt.utcnow().strftime("%m-%d-%Y %H:%M:%S")
        market_cap, price, daily_change, weekly_change, daily_volume, daily_volume_change, btc_dominance, stablecoin_volume, total_mc = coinmarketcap_data(crypto)
        fear_and_greed = market_trends(crypto)
        new_row = FinancialData(
            time: time,
            price: round(price, 2),
            daily_volume: round(daily_volume, 2),
            daily_volume_change: round(daily_volume_change, 2),
            market_cap: round(market_cap, 2),
            daily_delta: round(daily_change, 2),
            weekly_delta: round(weekly_change, 2),
            fear_and_greed: int(fear_and_greed),
            btc_dominance: round(btc_dominance, 2),
            stablecoin_volume: round(stablecoin_volume, 2),
            total_market_cap: round(total_mc, 2)
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return 'Success'
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return 'Failure'

def coinmarketcap_data(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    url2 = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
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
    except Exception as e:
        print(f"Error occurred while making the API request: {e}")
        return 'Error with request'
        # Handle the error appropriately
    market_cap = data['data']['1']['quote']['USD']['market_cap']
    price = data['data']['1']['quote']['USD']['price']
    daily_change = data['data']['1']['quote']['USD']['percent_change_24h']
    weekly_change = data['data']['1']['quote']['USD']['percent_change_7d']
    daily_volume = data['data']['1']['quote']['USD']['volume_24h']
    daily_volume_change = data['data']['1']['quote']['USD']['volume_change_24h']
    try:
        response = requests.get(url2, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during second CMC API request: {e}")
        return 'Error with request 2'
    btc_dominance = data['data']['btc_dominance']
    stablecoin_volume = data['data']['quote']['USD']['stablecoin_volume_24h']
    total_market_cap = data['data']['quote']['USD']['total_market_cap']
    return market_cap, price, daily_change, weekly_change, daily_volume, daily_volume_change, \
        btc_dominance, stablecoin_volume, total_market_cap


def market_trends(crypto):
    body = requests.get('https://www.binance.com/en/square/fear-and-greed-index')
    soup = BeautifulSoup(body.text, 'html.parser')
    fear_and_greed = soup.find(class_="css-cxlpc6").text
    return fear_and_greed

if __name__ == "__main__":
    main("bitcoin")
                       
