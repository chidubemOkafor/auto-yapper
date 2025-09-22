from dotenv import load_dotenv
from functions import create_reply, create_yap
import schedule
import requests
import time
import os
import random
from datetime import datetime

load_dotenv()

def random_yap_times():
    num_tweets = random.randint(5, 7)
    times = []
    for i in range(num_tweets):
        hour = random.randint(6, 23)
        minute = random.randint(0, 59)
        times.append(f"{hour:02d}:{minute:02d}")
    return sorted(times)

def random_reply_times():
    times = []
    for i in range(2):
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        times.append(f"{hour:02d}:{minute:02d}")
    return sorted(times)

def setup_daily_schedule():
    schedule.clear()
    
    yap_times = random_yap_times()
    reply_times = random_reply_times()
    
    print(f"Today's yap times: {yap_times}")
    print(f"Today's reply times: {reply_times}")
    
    for time_str in yap_times:
        schedule.every().day.at(time_str).do(create_yap)
    
    for time_str in reply_times:
        schedule.every().day.at(time_str).do(create_reply)
    
    schedule.every().day.at("00:01").do(setup_daily_schedule)

def keep_alive():
    try:
        requests.get(f"https://{os.getenv('RENDER_EXTERNAL_URL')}/ping")
    except:
        pass

setup_daily_schedule()
schedule.every(10).minutes.do(keep_alive)

while True:
    schedule.run_pending()
    time.sleep(60)