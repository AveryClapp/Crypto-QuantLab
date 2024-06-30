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

# Market trends can look at dominance at https://www.coingecko.com/en/coins/{crypto} <- crypto symbol not necessarily required.

def main(crypto):
    load_dotenv('app/core/.env')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-2')
    bucket_name='cryptopltfdatabucket'
    file = f'{crypto}_financials.csv'
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file)
        print(response)
        csv_content=response['Body'].read().decode('utf-8')
        data = pd.read_csv(io.StringIO(csv_content))
        print(data)
    except Exception as e:
        print(e)
        data = pd.DataFrame(columns=["Time","Price","Daily Volume","Daily Volume Change","Market Cap",
            "1D Delta","7D Delta","F&G","BTC Dominance","Stablecoin Volume","Total Market Cap"])
    time = dt.utcnow().strftime("%m-%d-%Y %H:%M:%S")
    market_cap, price, daily_change, weekly_change, daily_volume, daily_volume_change, btc_dominance, stablecoin_volume, total_mc = coinmarketcap_data(crypto)
    fear_and_greed = market_trends(crypto)
    data.loc[len(data)] = [
        time,
        round(price, 2),
        round(daily_volume, 2),
        round(daily_volume_change, 2),
        round(market_cap, 2),
        round(daily_change, 2),
        round(weekly_change, 2),
        fear_and_greed,
        round(btc_dominance, 2),
        round(stablecoin_volume, 2),
        round(total_mc, 2)
    ]
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=file, Body=csv_buffer.getvalue())
    print(f"Success at time: {time}")
    return 'Success'

def coinmarketcap_data(crypto):
    load_dotenv('/home/ec2-user/data/.env')
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
    try:
        response = requests.get(url2, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during second CMC API request: {e}")
        raise RuntimeException("Error occurred during second CMC API request")
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
