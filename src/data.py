import json
import os
import requests

# Load credentials
with open(os.path.expanduser("~/kalshi-market-maker/config.json")) as f:
    creds = json.load(f)

MEMBER_ID = creds["member_id"]
PEM_PATH = creds["pem_path"]

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

def get_markets():
    url = f"{BASE_URL}/markets"
    response = requests.get(url, cert=PEM_PATH, headers={"X-Member-ID": MEMBER_ID})
    if response.status_code != 200:
        raise Exception(f"Error fetching markets: {response.status_code}, {response.text}")
    return response.json()

def get_market_by_ticker(ticker):
    url = f"{BASE_URL}/markets/{ticker}"
    response = requests.get(url, cert=PEM_PATH, headers={"X-Member-ID": MEMBER_ID})
    if response.status_code != 200:
        raise Exception(f"Error fetching market {ticker}: {response.status_code}, {response.text}")
    return response.json()
