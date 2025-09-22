from database import setRetweetTweet

tweets = [
    {
        "id": 1969357840952541526,
        "tweet":" @tbros6868 @Everlyn_ai 好"
    },
      {
        "id": 1969357840461553907,
        "tweet":"@gstar_SC @Everlyn_ai Bullish on $LYN"
    },
      {
        "id": 1969357832211611921,
        "tweet":"@spoilerbull @Everlyn_ai Good morning! What's a tiny adventure you can have today? How is your Saturday going?"
    },
      {
        "id": 1969357828721652014,
        "tweet":"@shubh2005S @Everlyn_ai geveryln"
    },
      {
        "id": 1969357828516086228,
        "tweet":"@joshbanks4pf @Everlyn_ai gEverlyn moon"
    },
      {
        "id": 1969357816352657608,
        "tweet":"@fancy0523 @SentientAGI @Everlyn_ai Bullish on all"
    },
    {
        "id": 1969357816126115849,
        "tweet":"@Sireadell @Everlyn_ai @AnichessGame Finally found everlyn community 😍😍 I’m thrilled"
    },
    {
        "id": 1969357809411080218,
        "tweet":"@Tipwotip @Everlyn_ai almost at 200 Yaps — Everlyn TGE hype is real, 25th Sept is the date to watch"
    },
    {
        "id": 1969357808630943780,
        "tweet":"@Tundeffs_ @Everlyn_ai 5. Hype may attract capital, but only utility attracts loyalty."
    },
]

for tweet in tweets:
    ispushed = setRetweetTweet(tweet["id"], tweet["tweet"])
    if ispushed:
        print(f"Pushed tweet ID {tweet['id']} to database")
    else:
        print(f"Failed to push tweet ID {tweet['id']} to database")
print("Done pushing tweets.")