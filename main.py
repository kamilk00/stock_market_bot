from alpha_vantage import AlphaVantage
from utils import get_json, process_stocks
from smtp_mail_manager import SMTPMailManager

import os

# Load environment variables
API_KEY = os.getenv("API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Load stock limits configuration from JSON
limits_json = get_json('configuration/limits.json')

# Initialize the SMTPMailManager with the loaded configuration
smtp_manager = SMTPMailManager(SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD)

# Create an instance of AlphaVantage and process the stock data
process_stocks(AlphaVantage(API_KEY, limits_json, smtp_manager, RECIPIENT_EMAIL))