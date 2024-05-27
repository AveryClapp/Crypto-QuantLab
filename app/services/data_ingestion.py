from app.data import get_data
from dotenv import load_dotenv
import os
import requests
import psycopg2
from configparser import ConfigParser

def config(filename='/Users/averyclapp/Documents/Coding Stuff/AIStockPicker/app/core/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db

def validate_ticker(ticker):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tickers WHERE ticker = %s", (ticker,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
    return True
    

def setup(ticker: str):
    # Ensure the ticker is valid
    if not validate_ticker(ticker):
        return f"Ticker {ticker} is not valid!"
    
    # # Get HTML code for desired websites
    get_data.fetch_data(ticker)

    # # Go through html files and extract information
    get_data.extract_data(ticker)


    return f"Retrieved data for {ticker} successfully!"
