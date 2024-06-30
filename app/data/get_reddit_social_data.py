import requests
import requests.auth
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime as dt
from collections import Counter
import time
import boto3
import io

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()
load_dotenv('/home/ec2-user/data/.env')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2')
bucket_name='cryptopltfdatabucket'

def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

def get_reddit_token():
    reddit_password = os.getenv('REDDIT_PASS')
    reddit_username = os.getenv('REDDIT_USER')
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_SECRET_KEY")
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "password", "username": reddit_username, "password": reddit_password}
    headers = {"User-Agent": f"SentimentAnalysisBot/0.1 by {reddit_username}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()['access_token']

def get_reddit_data(token, crypto='Bitcoin', subreddits=['CryptoCurrency', 'CryptoMarkets']):
    username = os.getenv('REDDIT_USER')
    headers = {"Authorization": f"bearer {token}", "User-Agent": f"SentimentAnalysisBot/0.1 by {username}"}
    params = {"limit": 100}  # Increased from 10 to 100
    subreddits.append(crypto)
    all_posts_data = []
    for subreddit in subreddits:
        try:
            response = requests.get(f"https://oauth.reddit.com/r/{subreddit}/hot", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            for post in data['data']['children']:
                title = clean_text(post['data']['title'])
                selftext = clean_text(post['data'].get('selftext', ''))
                url = f"https://www.reddit.com{post['data']['permalink']}"
                full_text = f"{title} {selftext}"
                sentiment = get_sentiment(full_text)
                all_posts_data.append({
                    'subreddit': subreddit,
                    'title': title,
                    'selftext': selftext[:100],
                    'url': url,
                    'sentiment': sentiment,
                    'upvotes': post['data']['score'],
                    'created_at': datetime.fromtimestamp(post['data']['created_utc']).strftime("%Y-%m-%d %H:%M:%S")
                })  
            time.sleep(2)  # To respect Reddit's rate limits
        except requests.exceptions.RequestException as e:
            print(f"Error collecting data from r/{subreddit}: {str(e)}")
    write_articles_to_s3(all_posts_data)
    write_sentiment_to_s3(all_posts_data)
    return all_posts_data
    
def write_articles_to_s3(posts_data):
    file = f'reddit_sentiment.csv'
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file)
        csv_content=response['Body'].read().decode('utf-8')
        data = pd.read_csv(io.StringIO(csv_content))
    except:
        data = pd.DataFrame(columns=["subreddit","title","selftext","url","sentiment","upvotes","created_at"])
    df = pd.DataFrame(posts_data)
    # Append new data to the existing CSV or create a new one
    combined_data = pd.concat([data, df], ignore_index=True)
    csv_buffer = io.StringIO()
    combined_data.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=file, Body=csv_buffer.getvalue())
    print("Social Data Written to S3")

def write_sentiment_to_s3(posts_data):
    sentiments = [post['sentiment'] for post in posts_data]
    average_sentiment = round( sum(sentiments) / len(sentiments) if sentiments else 0, 3)
    file = 'sentiment.csv'
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file)
        csv_content=response['Body'].read().decode('utf-8')
        data = pd.read_csv(io.StringIO(csv_content))
    except:
        data = pd.DataFrame(columns=["Time, Average Sentiment, Article Count"])
    time = dt.utcnow().strftime("%m-%d-%Y %H:%M:%S")
    df = pd.DataFrame({
        "Time": [time],
        "Average Sentiment": [average_sentiment],
        "Article Count": [len(sentiments)]
    })
    #Append new data to the existing CSV or create a new one
    combined_data = pd.concat([data, df], ignore_index=True)
    csv_buffer = io.StringIO()
    combined_data.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=file, Body=csv_buffer.getvalue())
    print("Sentiment Data Written to S3")

    # Keyword analysis
    #keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'nft', 'moon', 'wagmi', 'hodl', 'bear', 'bull']
    #keyword_counts = Counter()
    #for post in posts_data:
     #   full_text = f"{post['title']} {post['selftext']}".lower()
      #  keyword_counts.update(keyword for keyword in keywords if keyword in full_text)

def clean_text(text):
    return ' '.join(text.split()).replace('"', "'")

if __name__ == '__main__':
    token = get_reddit_token()
    reddit_data = get_reddit_data(token)