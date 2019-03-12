import requests
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: [URL] [Interval in seconds]")
        sys.exit()

    # Extract arguments
    url = sys.argv[1]
    interval = int(sys.argv[2])

    # Set up scheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: print(url), 'interval', seconds=interval)
    scheduler.start()
