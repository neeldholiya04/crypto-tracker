import time
import logging
from services.crypto_service import CryptoService
from services.sheets_service import GoogleSheets
from config.settings import CREDENTIALS_FILE, SHEET_ID, UPDATE_INTERVAL

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('logs/crypto_analysis.log'),
                        logging.StreamHandler()
                    ])


def main():
    # Initialize Google Sheets client
    try:
        sheets_client = GoogleSheets(CREDENTIALS_FILE, SHEET_ID)
    except Exception as e:
        logging.error(f"Failed to initialize Google Sheets client: {e}")
        return

    while True:
        try:
            # Fetch cryptocurrency data
            crypto_data = CryptoService.fetch_data()
            if crypto_data is None:
                logging.warning("Failed to fetch data. Retrying...")
                time.sleep(UPDATE_INTERVAL)
                continue

            # Analyze data
            analysis = CryptoService.analyze_data(crypto_data)
            if not analysis:
                logging.warning("No analysis data available. Retrying...")
                time.sleep(UPDATE_INTERVAL)
                continue

            # Update analysis to Google Sheets
            sheets_client.update_analysis(analysis)

            # Update raw cryptocurrency data
            sheets_client.update_sheet(crypto_data)

            logging.info("Crypto analysis update completed successfully")

        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")

        # Wait before the next iteration
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
