# tiktok-scraping

## Initial Setup

1. install python
2. create a virtual environment
3. install dependencies from requirements.txt

## Rapid Api

### Setup

Make an account on https://rapidapi.com, link your github account to it and then subscribe to the [Tiktok Api](https://rapidapi.com/yi005/api/tiktok-video-no-watermark2).

Create a .env file and add your api keys to it:
```bash
echo 'RAPIDAPI_KEY="<API KEY HERE>"' >> .env
```

### Run (cli)

Run the Rapid API python file:

```bash
python rapidapi.py < examples/links
```

Example of a full run of all subsystems:

1. activate this project's virtual environment

```bash
source ./.venv/bin/activate
```

2. run the all subsystems

```bash
./rapidapi.py < examples/links | tee /dev/tty | ./ripaudio.py | tee /dev/tty | ./transcribe.py
```

This way allows you to use standard Unix tools like GNU-Parallel to easily manipulate data into multiple other data stream or to simply add parallelism.

### Run (orchestrator)

The orchestrator tracks the jobs that are currently available in the database.

1. activate this project's virtual environment

```bash
source ./.venv/bin/activate
```

2. run the orchestrator

```bash
./main.py
```