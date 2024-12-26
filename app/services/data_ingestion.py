from dotenv import load_dotenv
import os
import requests
import psycopg2
from configparser import ConfigParser

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
        return False
    finally:
        if conn is not None:
            conn.close()
    return True
    

def main(ticker: str):
    # Ensure the ticker is valid
    if not validate_ticker(ticker):
        return f"Ticker {ticker} is not valid!"

    return extracted_data
