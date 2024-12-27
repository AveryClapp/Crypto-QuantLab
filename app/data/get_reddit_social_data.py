import requests
import requests.auth
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timezone
from collections import Counter
import time
import io
from app.models import PostData
from app.database import get_db


# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()
load_dotenv()
db = next(get_db())

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
    params = {"limit": 5}  
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
                    'created_at': datetime.fromtimestamp(post['data']['created_utc'])
                })  
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error collecting data from r/{subreddit}: {str(e)}")
    return store_data(all_posts_data)
    
def store_data(posts_data):
    try:
        for post in posts_data:
            new_row = PostData(
                    title = post['title'][:100],
                    subreddit = post['subreddit'][:100],
                    description = post['selftext'][:100],
                    url = post['url'][:100],
                sentiment = post['sentiment'],
                upvotes = post['upvotes'],
                created_at = post['created_at']
                )
            db.add(new_row)
        db.commit()
    except Exception as e:
        db.rollback()
        return f'Failure {e}'
    finally:
        db.close()
    return "Successfully get and store sentiment data"

def clean_text(text):
    return ' '.join(text.split()).replace('"', "'")

if __name__ == '__main__':
    token = get_reddit_token()
    print(get_reddit_data(token))
