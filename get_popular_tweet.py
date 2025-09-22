import os
import tweepy
from dotenv import load_dotenv
from database import setRetweetTweet

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")
username = os.getenv("ACCOUNT_USERNAME")

if not bearer_token:
    raise ValueError("BEARER_TOKEN is missing in .env")
if not username:
    raise ValueError("ACCOUNT_USERNAME is missing in .env")

def fetch_commentable_tweets():
    try:
        client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

        query = f"@{username} -is:retweet"

        tweets = client.search_recent_tweets(query=query, max_results=3)

        if not tweets:
            return

        print(f"Latest tweets from @{username}:")
        print(tweets.data)
        for tweet in tweets.data:
            setRetweetTweet(tweet.id, tweet.text)
            print(f"Pushed tweet ID {tweet.id} to database")

        print("Done fetching and storing tweets.")
    except Exception as e:
        print(f"Error: {e}")
