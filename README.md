
# Cryptocurrency Market Analysis

## Overview
This project provides a real-time analysis of the cryptocurrency market using data from the CoinGecko API. The analysis results are continuously updated in a Google Sheet for live tracking and insights.

## Features
- **Data Fetching**: Retrieves the latest cryptocurrency data, including name, symbol, price, market cap, and 24-hour price changes.
- **Data Analysis**: Calculates key metrics such as:
  - Top 5 cryptocurrencies by market cap.
  - Average price of all cryptocurrencies.
  - Cryptocurrencies with the highest and lowest 24-hour price changes.
- **Google Sheets Integration**: Updates a Google Sheet ("Crypto Analysis" worksheet) with:
  - Live analysis results.
  - Formatted and beautified cryptocurrency data.
- **Real-Time Updates**: Periodically fetches and updates data every specified interval.

## Technologies Used
- **Python**: Core programming language.
- **Pandas**: For data manipulation and analysis.
- **CoinGecko API**: Source of cryptocurrency data.
- **Google Sheets API**: For integration with Google Sheets.
- **dotenv**: For managing environment variables.

## Requirements
- Python 3.7+
- Google API Credentials JSON file for Google Sheets integration.

## Setup Instructions
### Step 1: Download Google Sheets API Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Library** and enable the "Google Sheets API" and "Google Drive API".
4. Go to **APIs & Services > Credentials** and click on "Create Credentials".
5. Select "Service Account" and follow the instructions to create a service account.
6. Download the JSON credentials file and save it securely. Use the path to this file in your `.env` file.

### Step 2: Clone the Repository
```bash
git clone https://github.com/neeldholiya04/crypto-tracker.git
cd crypto-tracker
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Environment Variables
Create a `.env` file and add the following:
```env
GOOGLE_CREDENTIALS_PATH=<absolute_path_to_credentials_file>
GOOGLE_SHEET_ID=<google_sheet_id>
UPDATE_INTERVAL=30  # Interval in seconds for live updates
```

### Step 5: Run the Script
```bash
python main.py
```

## Google Sheets Integration
- The live cryptocurrency data and analysis are updated in the "Crypto Analysis" worksheet of the specified Google Sheet.
- Key analysis results include:
  - Top 5 cryptocurrencies by market cap.
  - Average price across all cryptocurrencies.
  - Highest and lowest 24-hour price changes.
- The Google Sheet is formatted for readability and includes bold headers, center alignment, and borders.

## Logging
- All activities, including errors and successful updates, are logged in `crypto_analysis.log` for monitoring.

