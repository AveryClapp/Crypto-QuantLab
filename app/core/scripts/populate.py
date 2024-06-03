import psycopg2
import yfinance as yf
from configparser import ConfigParser

def config(filename='../database.ini', section='postgresql'):
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

def populate_tickers_table():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        tickers = ['DOGE', 'USDT']
        for ticker in tickers:
            cur.execute(
                "INSERT INTO tickers (ticker) VALUES (%s)", [ticker])
            print(f"Added ticker: {ticker}")

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def view_tickers():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tickers")
        rows = cur.fetchall()

        print("Tickers in the database:")
        for row in rows:
            print(row)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    populate_tickers_table()
    # view_tickers()