# Stock Price Alert System

This project fetches stock data from the Alpha Vantage API, analyzes price changes, and sends email alerts if stock prices exceed predefined thresholds.

## Features

* Fetches stock price data from Alpha Vantage

* Compares prices with predefined limits

* Sends email alerts when thresholds are exceeded

* Automated execution via GitHub Actions

## Configuration

1. Set up environment variables (e.g., in .env or GitHub Secrets):

* API_KEY: Alpha Vantage API key

* SMTP_SERVER: SMTP server address

* SMTP_PORT: SMTP server port

* EMAIL_USER: Email sender address

* EMAIL_PASSWORD: Email sender password

* RECIPIENT_EMAIL: Alert recipient email

2. Define stock limits in configuration/limits.json:

```json
{
    "BMEA": {
        "high_alert": 5.00,
        "low_alert": 4.00,
        "currency": "USD"
    }
}
```
