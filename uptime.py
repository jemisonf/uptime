import argparse
import datetime
import signal
import time

from rich.console import Console
import requests

console = Console()
error_console = Console(stderr=True)

parser = argparse.ArgumentParser(description="measure uptime of a service")
parser.add_argument("--url", dest="url", help="url to hit")
parser.add_argument("--interval", dest="interval", help="ping interval in ms")

parsed_args = parser.parse_args()
url = parsed_args.url
interval = int(parsed_args.interval or 50)

if url is None:
    error_console.print("[red]error: url cannot be empty")
    exit(1)

downtime = 0
uptime = 0

def handler(signum, frame):
    console.print("[green]Exiting")
    console.print(f"[blue]Total downtime: {downtime} ms")
    console.print(f"[blue]Total uptime: {uptime} ms")
    exit(0)

signal.signal(signal.SIGINT, handler)

last_request = datetime.datetime.now()

while True:

    try:
        r = requests.get(url)
    except Exception as e:
        error_console.print(f"[red]ERR {e}")
        exit(0)

    now = datetime.datetime.now()
    if r.status_code < 400:
        console.print(f"[green]OK {r.status_code}")
        uptime += (now - last_request).microseconds / 1000
    else:
        timestamp = str(now)
        error_console.print(f"[red]ERR {r.status_code} {timestamp}")
        downtime += (now - last_request).microseconds / 1000

    last_request = now

    time.sleep(interval / 1000)



