import requests

# Hardcoded API key (for testing purposes)
api_key = "CG-7S1xjb3bHzgUZqGawEjvauh4"

def get_top_cryptos(limit=15, sort_by=None):
    """
    Fetches top cryptocurrencies and sorts them based on market cap by default or 
    by 24h price change for gainers and losers.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',  # Sort by market cap by default
        'per_page': limit,
        'page': 1
    }

    headers = {
        'x-cg-demo-api-key': api_key  # Include the API key in the header
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Check for errors
        data = response.json()

        # If sorting by gainers or losers, fetch a larger set (e.g., top 100) to sort
        if sort_by in ['gainers', 'losers']:
            params['per_page'] = 100  # Fetch top 100 coins to have a larger set for sorting
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Check for errors
            data = response.json()

            # Sorting the data for gainers or losers
            if sort_by == 'gainers':
                # Sort in descending order by price change (top gainers)
                data_sorted = sorted(data, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)
            elif sort_by == 'losers':
                # Sort in ascending order by price change (top losers)
                data_sorted = sorted(data, key=lambda x: x.get('price_change_percentage_24h', 0))

            # Now limit to the top 10 after sorting (ensuring only top 10 are returned)
            data_sorted = data_sorted[:limit]  # Limit the result to the top 'limit' number of results
        else:
            # No sorting, return top cryptocurrencies by market cap
            data_sorted = data[:limit]  # Ensure we limit to the requested amount

        return data_sorted

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def get_coin_details(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    headers = {'x-cg-demo-api-key': api_key}
    params = {'localization': 'false', 'tickers': 'false', 'market_data': 'true', 'community_data': 'false', 'developer_data': 'true', 'sparkline': 'false'}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin details: {e}")
        return None

import requests
import pandas as pd
from datetime import datetime

import requests
import pandas as pd

def get_historical_prices(coin_id, days=90):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data.get("prices", [])

        # Convert to DataFrame for Prophet
        df = pd.DataFrame(prices, columns=["ds", "y"])
        df["ds"] = pd.to_datetime(df["ds"], unit="ms")
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if API call fails
