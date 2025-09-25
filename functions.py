from main import client
from model import data, create_completion
from get_popular_tweet import fetch_commentable_tweets
from database import getTweetToComment, markSent, getOldTweet, setOldTweet

def create_reply():
    projTweet = getTweetToComment()
    if projTweet is None:
        fetch_commentable_tweets()
        return
    tweet = projTweet["tweet"]

    data["messages"].append({"role": "assistant", "content": f"generate a reply for this '{tweet}' and please make it short also add the project tags too. and remeber it must be a direct reply response to the tweet nothing else"})

    completion = create_completion(data["messages"])
    text = completion.choices[0].message.content

    comment = client.create_tweet(text=text, in_reply_to_tweet_id=projTweet["id"])
    if comment is None:
        print("Error creating comment")
        return None

    markSent(tweet_id=projTweet["id"])
    print(f"Commented created: {text}")

    return text

def create_yap():
    prevYap = getOldTweet()
    data["messages"].append({
        "role": "assistant",
        "content": f"This was your previous yap: '{prevYap}'. Don't repeat it. Make something new."
    })

    completion = create_completion(data["messages"])

    text = completion.choices[0].message.content
    print("Generated:", text)
    tweet_response = client.create_tweet(text=text)
    if tweet_response:
        print("Tweeted:", text)
        setOldTweet(text)
    else: 
        print("Failed to create tweet.")
        return None

    return text

# source venv/bin/activate

# Today's yap times: ['08:52', '10:55', '13:27', '18:18', '18:52']
# Today's reply times: ['11:54', '20:51']