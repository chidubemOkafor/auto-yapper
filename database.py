import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def setRetweetTweet(tweet_id: str, tweet_text: str):
    tweet_response = supabase.table("retweets").select("*").execute()

    for tweets in  tweet_response.data:
        if tweets["id"] == tweet_id:
            print("Tweet already exists in the database.")
            return None

    response = supabase.table("retweets").insert({
        "id": tweet_id,
        "tweet": tweet_text.strip()
    }).execute()
    return response

def getTweetToComment():
    tweet_response = (
        supabase.table("retweets")
        .select("*")
        .eq("isComented", False)
        .limit(1)
        .execute()
    )
    if tweet_response.data:
        print("Fetched tweet to comment on:", tweet_response.data[0])
        return tweet_response.data[0]
    return None

def markSent(tweet_id: int):
    update_response = (
        supabase.table("retweets")
        .update({"isComented": True})
        .eq("id", tweet_id)
        .execute()
    )

    return update_response

def setOldTweet(tweet_text: str):
    supabase.table("tweet_history").delete().neq("id", 0).execute()

    response = supabase.table("tweet_history").insert({
        "historical_tweet": tweet_text.strip()
    }).execute()

    return response
   
def getOldTweet():
    old_tweet = supabase.table("tweet_history").select("*").execute()
    return old_tweet.data[0]["historical_tweet"]
