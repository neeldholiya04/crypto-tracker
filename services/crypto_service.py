import requests
import pandas as pd
from datetime import datetime

class CryptoService:
    API_URL = "https://api.coingecko.com/api/v3/coins/markets"
    DEFAULT_PARAMS = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False,
    }

    @staticmethod
    def fetch_data():
        try:
            response = requests.get(CryptoService.API_URL, params=CryptoService.DEFAULT_PARAMS)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data, columns=[
                "name", "symbol", "current_price", "market_cap",
                "total_volume", "price_change_percentage_24h"
            ])

            # Add a timestamp column
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df["Timestamp"] = timestamp

            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching cryptocurrency data: {e}")
            return None

    @staticmethod
    def analyze_data(df):
        try:
            analysis = {
                "top_5_by_market_cap": df.nlargest(5, "market_cap")[["name", "market_cap"]],
                "average_price": df["current_price"].mean(),
                "highest_change": df.loc[df["price_change_percentage_24h"].idxmax()],
                "lowest_change": df.loc[df["price_change_percentage_24h"].idxmin()],
            }
            return analysis
        except Exception as e:
            print(f"Error analyzing data: {e}")
            return None
