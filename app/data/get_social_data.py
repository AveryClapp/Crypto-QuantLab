import requests
import requests.auth
from dotenv import load_dotenv
import os
import pandas as pd
from textblob import TextBlob
from datetime import datetime


# Function to calculate sentiment score
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity


def get_reddit_token():
    load_dotenv('./app/core/.env')
    reddit_password = os.getenv('REDDIT_PASS')
    reddit_username = os.getenv('REDDIT_USER')
    reddit_token = os.getenv('REDDIT_TOKEN')
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_SECRET_KEY")
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "password", "username": reddit_username, "password": reddit_password}
    headers = {"User-Agent": f"ChangeMeClient/0.1 by {reddit_username}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()['access_token']


def get_reddit_data(token):
    load_dotenv('./app/core/.env')
    username = os.getenv('REDDIT_USER')
    headers = {"Authorization": f"bearer {token}", "User-Agent": f"ChangeMeClient/0.1 by {username}"}
    params = {"g": "US", "limit": 10}
    response = requests.get("https://oauth.reddit.com/r/CryptoCurrency/hot", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        posts_data = []


        for post in data['data']['children']:
            title = clean_text(post['data']['title'])
            selftext = clean_text(post['data'].get('selftext', ''))[:1000]
            url = f"https://www.reddit.com{post['data']['permalink']}"

            if not selftext.strip():
                continue

            full_text = f"{title} {selftext}"
            sentiment = get_sentiment(full_text)
            
            posts_data.append({
                'title': title,
                'selftext': selftext,  
                'url': url,              
                'sentiment': sentiment,
            })

        write_sentiment_to_csv(posts_data)
        sentiments = [post['sentiment'] for post in posts_data]
        average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
    return average_sentiment, len(posts_data)

def write_sentiment_to_csv(posts_data):
    path = './app/data/csvs/reddit_sentiment.csv'
    data = pd.read_csv(path)
    columns = ['title', 'selftext', 'sentiment', 'timestamp', 'url']  
    
    df = pd.read_csv(path)
    # Ensure all required columns are present
    for col in columns:
        if col not in df.columns:
            df[col] = ''
    
    time = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
    
    # Prepare the new data
    new_data = []
    for post in posts_data:
        new_data.append({
            'title': post['title'],
            'selftext': post['selftext'][:50],  # Limit selftext to 1000 characters
            'sentiment': post['sentiment'],
            'timestamp': time,
            'url': post['url']
        })
    
    # Append new data to the DataFrame
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Write the updated DataFrame to CSV
    df.to_csv(path, index=False, quoting=1)

def clean_text(text):
    # Remove newlines and extra spaces
    cleaned = ' '.join(text.split())
    # Remove any remaining problematic characters
    cleaned = cleaned.replace('"', "'")  # Replace double quotes with single quotes
    return cleaned

if __name__ == '__main__':
    token = get_reddit_token()
    reddit_average_sentiment = get_reddit_data(token)
    print(reddit_average_sentiment)