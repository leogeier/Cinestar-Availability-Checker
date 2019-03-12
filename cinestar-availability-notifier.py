import requests
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

NOT_AVAILABLE_INDICATOR = 'Dieser Film befindet sich aktuell nicht im Programm.'

def querySite(url):
    r = requests.get(url)
    if NOT_AVAILABLE_INDICATOR not in r.text:
        print("alarm")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: [URL] [Interval in seconds]")
        sys.exit()

    # Extract arguments
    url = sys.argv[1]
    interval = int(sys.argv[2])

    # Set up scheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(querySite, 'interval', seconds=interval, args=[url])
    scheduler.start()
