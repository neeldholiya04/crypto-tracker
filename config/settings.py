import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 30))
