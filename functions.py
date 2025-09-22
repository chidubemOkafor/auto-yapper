from main import client
from model import data, cl, completion
from database import getTweetToComment, markSent, getOldTweet, setOldTweet
import requests

def create_reply():
    projTweet = getTweetToComment()
    if projTweet is None:
        return
    tweet = projTweet["tweet"]

    data["messages"].append({"role": "assistant", "content": f"generate a reply for this '{tweet}' and please make it short also add the project tags too"})
    completion = cl.chat.completions.create(data)

    text = completion.choices[0].message

    comment = client.create_tweet(text=text.content, in_reply_to_tweet_id=projTweet["id"])
    if comment is None:
        print("Error creating comment")

    markSent(tweet_id=projTweet["id"])

    print(f"Commented created: {comment.data}")
    
    return text

def create_yap():
    prevYap = getOldTweet()
    data["messages"].append({
        "role": "assistant",
        "content": f"This was your previous yap: '{prevYap}'. Don't repeat it. Make something new."
    })

    text = completion.choices[0].message
    print("Generated:", text.content)
    tweet_response = client.create_tweet(text=text)
    if tweet_response:
        print("Tweeted:", tweet_response.data)
        setOldTweet(tweet_response.data)
    else: 
        print("Failed to create tweet.")


# source venv/bin/activate
