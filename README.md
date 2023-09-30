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

### Run

Run the Rapid API python file:

```bash
python rapidapi.py
```