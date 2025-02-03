import requests
from datetime import datetime
from smtp_mail_manager import SMTPMailManager

class AlphaVantage():
    """
    A class responsible for fetching stock data from the Alpha Vantage API, analyzing stock data, and sending email alerts 
    when stock prices exceed predefined thresholds.
    """

    API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s'

    def __init__(self, api_key: str, stocks: dict, smtp_manager: SMTPMailManager, recipient_email: str):
        """
        Initializes an AlphaVantage object.

        :param api_key: The API key for accessing Alpha Vantage.
        :param stocks: A dictionary containing stock symbols and their alert thresholds.
        :param smtp_manager: An instance of the SMTPMailManager class for sending emails.
        :param recipient_email: The email address where alerts will be sent.
        """
        self.API_KEY = api_key
        self.stocks = stocks
        self.smtp_manager = smtp_manager
        self.RECIPIENT_EMAIL = recipient_email


    def parse_stock_datetime(self, stock_datetime_str: str) -> datetime | None:
        """
        Converts a stock date string to a datetime object.

        :param stock_datetime_str: The date string in 'YYYY-MM-DD' format.
        :return: A datetime object if the string is successfully parsed, otherwise None.
        """
        try:
            return datetime.strptime(stock_datetime_str, '%Y-%m-%d')
        except ValueError as err:
            print(f'Date parsing error: {err}')
            return None


    def get_stock_data(self) -> list:
        """
        Fetches stock data from the Alpha Vantage API.

        :return: A list of stock data retrieved from the API.
        """
        stock_data_list = []
        for stock_symbol in self.stocks.keys():
            request_url = self.API_URL % (stock_symbol, self.API_KEY)
            response = requests.get(request_url)
            try:
                stock_data = response.json()
                stock_data_list.append(stock_data)
            except requests.exceptions.RequestException as e:
                print(f'Cannot get data from API: {e}')

        return stock_data_list


    def analyze_stock_data(self, stock_data: dict):
        """
        Analyzes stock data, compares closing prices with predefined thresholds,
        and sends email alerts if the thresholds are exceeded.

        :param stock_data: The stock data to analyze.
        """
        stock_symbol = stock_data.get('Meta Data', {}).get('2. Symbol')
        if not stock_symbol:
            return
        
        stock_limits = self.stocks.get(stock_symbol.upper())
        if not stock_limits:
            return
        
        time_series = stock_data.get('Time Series (Daily)', {})
        if not time_series:
            return
        
        if timestamps := list(time_series.keys()):
            if last_data_time := self.parse_stock_datetime(next(iter(timestamps))):
                if last_data_time.day != datetime.now().day:
                    return

                today_close_value = float(time_series[timestamps[0]].get('4. close', 0))
                yesterday_close_value = float(time_series[timestamps[1]].get('4. close', 0))
                if not today_close_value or not yesterday_close_value:
                    return
                
                currency = stock_limits.get('currency', 'USD')
                if today_close_value > stock_limits.get('high_alert') and yesterday_close_value < stock_limits.get('high_alert'):
                    mail_body = f'Stock price has exceeded the high limit ({stock_limits.get("high_alert")} {currency}): {today_close_value} {currency}'                    
                    self.smtp_manager.send_email(f'{stock_symbol} - HIGH LIMIT ALERT!', mail_body, self.RECIPIENT_EMAIL)

                if today_close_value < stock_limits.get('low_alert') and yesterday_close_value > stock_limits.get('low_alert'):
                    mail_body = f'Stock price has dropped below the low limit ({stock_limits.get("low_alert")} {currency}): {today_close_value} {currency}'
                    self.smtp_manager.send_email(f'{stock_symbol} - LOW LIMIT ALERT!', mail_body, self.RECIPIENT_EMAIL)