# `uptime`

A quick python CLI for precisely measuring service uptime over a specific period. Requires python >=3.7 and poetry.

Install deps with `poetry install`

Run with `poetry run python3 ./uptime.py --url $SERVICE_URL`

Also accepts a `--interval` flag but defaults to waiting 50ms between requests.

Stop with CTRL+C or SIGINT.