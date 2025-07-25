import sys
import os
import schedule
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main


def run_daily():
    schedule.every().day.at("07:30").do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)
