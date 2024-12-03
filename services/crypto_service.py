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

#
# import requests
# import pandas as pd
#
#
# class CryptoService:
#     API_URL = "https://api.binance.com/api/v3/ticker/24hr"
#
#     @staticmethod
#     def fetch_data():
#         """
#         Fetch real-time cryptocurrency data from Binance API.
#         Returns:
#             pd.DataFrame: Real-time cryptocurrency data.
#         """
#         try:
#             response = requests.get(CryptoService.API_URL)
#             response.raise_for_status()
#             data = response.json()
#
#             # Filter and structure the data into a DataFrame
#             df = pd.DataFrame(data)
#             df = df[["symbol", "lastPrice", "priceChangePercent", "volume", "quoteVolume"]]
#             df.rename(columns={
#                 "symbol": "Symbol",
#                 "lastPrice": "Current Price (USD)",
#                 "priceChangePercent": "24h Price Change (%)",
#                 "volume": "Volume",
#                 "quoteVolume": "Quote Volume (USD)"
#             }, inplace=True)
#
#             # Convert numeric fields
#             df["Current Price (USD)"] = pd.to_numeric(df["Current Price (USD)"])
#             df["24h Price Change (%)"] = pd.to_numeric(df["24h Price Change (%)"])
#             df["Volume"] = pd.to_numeric(df["Volume"])
#             df["Quote Volume (USD)"] = pd.to_numeric(df["Quote Volume (USD)"])
#
#             return df
#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching cryptocurrency data: {e}")
#             return None
#
#     @staticmethod
#     def analyze_data(df):
#         """
#         Perform basic analysis on cryptocurrency data.
#         Args:
#             df (pd.DataFrame): Cryptocurrency data.
#         Returns:
#             dict: Analysis results.
#         """
#         try:
#             analysis = {
#                 "top_5_by_volume": df.nlargest(5, "Volume")[["Symbol", "Volume"]],
#                 "average_price": df["Current Price (USD)"].mean(),
#                 "highest_change": df.loc[df["24h Price Change (%)"].idxmax()],
#                 "lowest_change": df.loc[df["24h Price Change (%)"].idxmin()],
#             }
#             return analysis
#         except Exception as e:
#             print(f"Error analyzing data: {e}")
#             return None
