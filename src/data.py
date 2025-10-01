# src/data.py
import os
import requests

# Base URL for Kalshi API (sandbox for testing, switch to prod when ready)
KALSHI_API_BASE = "https://trading-api.kalshi.com/v1"

def get_markets():
    """Fetches a list of markets from Kalshi"""
    url = f"{KALSHI_API_BASE}/markets"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching markets: {response.status_code}, {response.text}")
    
    return response.json()


def get_market_by_ticker(ticker):
    """Fetch market details by its ticker"""
    url = f"{KALSHI_API_BASE}/markets/{ticker}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching market {ticker}: {response.status_code}, {response.text}")
    
    return response.json()

