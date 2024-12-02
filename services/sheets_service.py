import gspread
from gspread.exceptions import WorksheetNotFound
from services.formatting_service import beautify_sheet
from utils.common import safe_format_value
import time
import pandas as pd


class GoogleSheets:
    def __init__(self, credentials_file, sheet_id):
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id
        self.client = self._authenticate()
        self.sheet = self.client.open_by_key(self.sheet_id).sheet1
        self.service = self._build_service()

    def _authenticate(self):
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return gspread.authorize(credentials)

    def _build_service(self):
        from googleapiclient.discovery import build
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return build("sheets", "v4", credentials=credentials)

    def update_analysis(self, analysis):
        try:
            # Open or create the "Crypto Analysis" worksheet
            try:
                analysis_sheet = self.client.open_by_key(self.sheet_id).worksheet("Crypto Analysis")
            except WorksheetNotFound:
                analysis_sheet = self.client.open_by_key(self.sheet_id).add_worksheet(
                    title="Crypto Analysis",
                    rows=100,
                    cols=10
                )

            # Prepare top 5 data
            top_5 = analysis['top_5_by_market_cap']
            top_5_data = [["Rank", "Name", "Market Cap"]]
            for i, row in enumerate(top_5.itertuples(index=False), start=1):
                top_5_data.append([i, row.name, f"${row.market_cap:,.0f}"])

            # Prepare analysis summary
            summary_data = [
                ["Metric", "Value"],
                ["🕒 Analysis Timestamp", time.strftime("%Y-%m-%d %H:%M:%S")],
                ["💰 Average Price", f"${analysis['average_price']:.2f}"],
                ["📈 Highest 24h Change", f"{analysis['highest_change']['name']} ({analysis['highest_change']['price_change_percentage_24h']:.2f}%)"],
                ["📉 Lowest 24h Change", f"{analysis['lowest_change']['name']} ({analysis['lowest_change']['price_change_percentage_24h']:.2f}%)"]
            ]

            # Combine the data into one sheet
            final_data = [["🚀 Top 5 Cryptocurrencies by Market Cap 🚀"]] + \
                         [[""]] + \
                         top_5_data + \
                         [[""]] + \
                         [["📊 Cryptocurrency Market Analysis 📊"]] + \
                         summary_data

            # Update the analysis worksheet
            analysis_sheet.clear()
            analysis_sheet.update(final_data)

            # Beautify the analysis worksheet
            beautify_sheet(analysis_sheet, self.service, analysis_sheet._properties['sheetId'])
            print("Analysis data updated successfully.")

        except Exception as e:
            print(f"Error updating analysis: {e}")

    def update_sheet(self, data_frame):
        """
        Update the Google Sheet with cryptocurrency data.
        Standardize headers and delegate formatting to formatting_service.
        """
        try:
            from services.formatting_service import format_data_frame, beautify_sheet

            # Standardize headers
            header_mapping = {
                "name": "Name",
                "symbol": "Symbol",
                "current_price": "Current Price (USD)",
                "market_cap": "Market Cap (USD)",
                "total_volume": "Total Volume (USD)",
                "price_change_percentage_24h": "24h Price Change (%)"
            }
            data_frame.rename(columns=header_mapping, inplace=True)

            # Format the DataFrame
            formatted_data_frame = format_data_frame(data_frame)

            # Prepare data for sheet update
            self.sheet.clear()
            self.sheet.update([formatted_data_frame.columns.tolist()] + formatted_data_frame.values.tolist())

            # Beautify the sheet
            beautify_sheet(self.sheet, self.service, self.sheet._properties["sheetId"])
            print("Sheet updated successfully with standardized headers.")
        except Exception as e:
            print(f"Error updating sheet: {e}")






