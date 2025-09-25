from dotenv import load_dotenv
from functions import create_reply, create_yap
from flask import Flask
import schedule
import threading
import time
import os
import random
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

@app.route('/')
def health():
    return "Bot is running!"

@app.route('/ping')
def ping():
    return "pong"

@app.route('/schedule')
def get_schedule():
    """Debug endpoint to see current schedule"""
    jobs = []
    for job in schedule.jobs:
        jobs.append({
            'function': job.job_func.__name__,
            'next_run': str(job.next_run),
            'unit': job.unit,
            'at_time': str(job.at_time) if hasattr(job, 'at_time') else None
        })
    return {'scheduled_jobs': jobs, 'current_time': str(datetime.now())}

def random_yap_times():
    """Generate random times for yapping throughout the day"""
    num_tweets = random.randint(5, 7)
    times = []
    for i in range(num_tweets):
        hour = random.randint(6, 23)
        minute = random.randint(0, 59)
        times.append(f"{hour:02d}:{minute:02d}")
    return sorted(times)

def random_reply_times():
    """Generate random times for replies"""
    times = []
    for i in range(2):
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        times.append(f"{hour:02d}:{minute:02d}")
    return sorted(times)

def safe_create_yap():
    """Wrapper for create_yap with error handling"""
    try:
        logger.info("Starting yap creation...")
        result = create_yap()
        logger.info(f"Yap created successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating yap: {str(e)}")
        return None

def safe_create_reply():
    """Wrapper for create_reply with error handling"""
    try:
        logger.info("Starting reply creation...")
        result = create_reply()
        logger.info(f"Reply created successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating reply: {str(e)}")
        return None

def run_scheduler():
    """Run the scheduler in a separate thread"""
    logger.info("Scheduler thread started")
    
    def setup_daily_schedule():
        """Set up the daily schedule with random times"""
        try:
            jobs_to_keep = []
            for job in schedule.jobs:
                if job.job_func.__name__ == 'setup_daily_schedule':
                    jobs_to_keep.append(job)
            
            schedule.jobs[:] = jobs_to_keep
            
            yap_times = random_yap_times()
            reply_times = random_reply_times()
            
            logger.info(f"Setting up schedule for {datetime.now().date()}")
            logger.info(f"Today's yap times: {yap_times}")
            logger.info(f"Today's reply times: {reply_times}")
            
            for time_str in yap_times:
                schedule.every().day.at(time_str).do(safe_create_yap)
                logger.info(f"Scheduled yap at {time_str}")
            
            for time_str in reply_times:
                schedule.every().day.at(time_str).do(safe_create_reply)
                logger.info(f"Scheduled reply at {time_str}")
            
            logger.info(f"Total jobs scheduled: {len(schedule.jobs)}")
            
        except Exception as e:
            logger.error(f"Error setting up daily schedule: {str(e)}")
    
    setup_daily_schedule()
    
    schedule.every().day.at("00:01").do(setup_daily_schedule)
    
    logger.info("Starting scheduler loop...")
    while True:
        try:
            pending_count = len(schedule.jobs)
            if pending_count > 0:
                schedule.run_pending()
                
            if datetime.now().minute % 30 == 0 and datetime.now().second < 10:
                logger.info(f"Scheduler running. {pending_count} jobs scheduled.")
                for job in schedule.jobs:
                    logger.info(f"  - {job.job_func.__name__} next run: {job.next_run}")
            
            time.sleep(10) 
            
        except Exception as e:
            logger.error(f"Error in scheduler loop: {str(e)}")
            time.sleep(60)

def test_functions():
    """Test that the yap and reply functions work"""
    logger.info("Testing functions...")
    try:
        logger.info("Testing create_yap...")
        result = safe_create_yap()
        logger.info(f"create_yap test result: {result}")
        
        logger.info("Testing create_reply...")
        result = safe_create_reply()
        logger.info(f"create_reply test result: {result}")
        
    except Exception as e:
        logger.error(f"Function test failed: {str(e)}")
        
if __name__ == '__main__':
    logger.info("Starting bot application...")
    
    test_functions()
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("Scheduler thread started")
    
    @app.route('/test/yap')
    def test_yap():
        try:
            result = safe_create_yap()
            return {'status': 'success', 'result': str(result)}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    @app.route('/test/reply')  
    def test_reply():
        try:
            result = safe_create_reply()
            return {'status': 'success', 'result': str(result)}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)