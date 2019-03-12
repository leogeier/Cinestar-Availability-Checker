import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: [URL] [Interval in MS]")
        sys.exit()

    url = sys.argv[1]
    interval = int(sys.argv[2])
