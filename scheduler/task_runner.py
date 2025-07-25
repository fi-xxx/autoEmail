import schedule
import time
from main import main


def run_daily():
    schedule.every().day.at("07:30").do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)
