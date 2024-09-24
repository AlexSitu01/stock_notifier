import os
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()

COMPANY_NAME = "Tesla Inc"
STOCK_TOKEN = os.environ.get("STOCK_TOKEN")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
PERCENT_INCREASE_THRESHOLD = 1.02

class Stocks:
    def __init__(self):
        pass

    #takes in string of stock symbol
    #returns string response of stock that has increased or none if the stock hasn't increased
    @staticmethod
    def check_stock(stock_symbol):
        stock_params = {
            'function': "GLOBAL_QUOTE",
            'symbol': stock_symbol,
            'apikey': STOCK_TOKEN
        }

        response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
        response.raise_for_status()
        if len(response.json()["Global Quote"]) == 0:
            return f"{stock_symbol} doesn't exist"
        print(response.json())
        data = response.json()["Global Quote"]

        open_value = float(data["02. open"])
        close_value = float(data["05. price"])
        # 5% or more increase for the day
        if open_value * PERCENT_INCREASE_THRESHOLD <= close_value:
            percent_increase = (close_value-open_value)/open_value
            return f"Open: ${open_value}\tClose: ${close_value}\n{stock_symbol} has increased by {percent_increase*100: .2f}%"

#should add method to check if the stock_symbol provided is valid or not
    @staticmethod
    def add_stock(stock_symbol: str):
        stock_symbol = str(stock_symbol).upper()
        if stock_symbol is None:
            return "Can't add None"
        #check if stock symbol is already in list
        if os.path.isfile("stocks.csv"):
            stocks = pd.read_csv("stocks.csv")
            for index, row in stocks.iterrows():
                if row["stock_symbol"] == stock_symbol:
                    return "That stock is already in the list"

        stock_to_add = {
            "stock_symbol": [stock_symbol]
        }
        stock_to_add = pd.DataFrame(stock_to_add)
        if os.path.isfile("stocks.csv"):
            stock_to_add.to_csv("stocks.csv", mode="a", index=False, header=False)
        else:
            stock_to_add.to_csv("stocks.csv", mode="a", index=False, header=True)
        return f"{stock_symbol} was added."

    @staticmethod
    def remove_stock(stock_symbol):
        if os.path.isfile("stocks.csv"):
            data = pd.read_csv("stocks.csv")
        else:
            return "You need to add stocks to the list first!"

        if stock_symbol in data['stock_symbol'].values:
            data = data[data['stock_symbol'] != stock_symbol]
            data.to_csv("stocks.csv", index=False)
            return f"{stock_symbol} has been removed"
        else:
            return f"{stock_symbol} isn't in the list"

    @staticmethod
    def get_stock_list():
        if os.path.isfile("stocks.csv"):
            return pd.read_csv("stocks.csv")["stock_symbol"].values
        return "You need to add stocks to the list first!"
