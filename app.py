from dotenv import load_dotenv
from functions import create_reply, create_yap
from flask import Flask
import schedule
import threading
import time
import os
import random

app = Flask(__name__)

load_dotenv()

@app.route('/')
def health():
    return "Bot is running!"

@app.route('/ping')
def ping():
    return "pong"

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

def run_scheduler():
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

    setup_daily_schedule()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# Today's yap times: ['07:14', '08:36', '09:29', '11:51', '13:14', '17:47']
# Today's reply times: ['13:21', '20:50']