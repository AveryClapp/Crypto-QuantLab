import requests
import os
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd


def main(crypto):
    #Create supabase client connection
    
    if not supabase.table(f'{crypto}'):
        print('table does not exist')
    coinmarketcap_data(crypto)




def coinmarketcap_data(crypto):
    url = f"https://coinmarketcap.com/currencies/{crypto}"
    body = requests.get(url).content
    soup = BeautifulSoup(body, "html.parser")

    #Gather finanical data for the crypto
    cur_price = soup.find(class_="sc-d1ede7e3-0 fsQm base-text").get_text()
    print(cur_price)


if __name__ == "__main__":
    main("bitcoin")