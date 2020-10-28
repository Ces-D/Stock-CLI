import requests

class AlphaVantageHandler():
    def __init__(self, api_key=None):
        self.api_key = api_key

    def make_request(self, symbol, function_name="GLOBAL_QUOTE"):
        """
        Handler for making api requests
        params: [optional] datatype=json
        """
        r = requests.get("https://www.alphavantage.co/query",
                         params={
                             "function": function_name,
                             "symbol": symbol,
                             "apikey": self.api_key,
                         })
        return r.json()
