import json
from alpha_vantage import AlphaVantage

def get_json(file_path: str) -> dict:
    """
    Loads and returns JSON data from the given file path.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    
def process_stocks(alpha_vantage: AlphaVantage):
    """
    Processes stock data by analyzing each stock retrieved via AlphaVantage API.
    """
    data = alpha_vantage.get_stock_data()
    for stock_data in data:
        alpha_vantage.analyze_stock_data(stock_data)