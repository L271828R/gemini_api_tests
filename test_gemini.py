# ROLES
# The API key you use to access this endpoint must have the Trader role assigned. See Roles for more information.

# HTTP REQUEST
# POST https://api.gemini.com/v1/order/new

# PARAMETERS
# Parameter	Type	Description
# request	string	The literal string "/v1/order/new"
# nonce	integer	The nonce, as described in Private API Invocation
# client_order_id	string	Recommended. A client-specified order id
# symbol	string	The symbol for the new order
# amount	string	Quoted decimal amount to purchase
# min_amount	string	Optional. Minimum decimal amount to purchase, for block trades only
# price	string	Quoted decimal amount to spend per unit
# side	string	"buy" or "sell"
# type	string	The order type. Only "exchange limit" supported through this API
# options	array	Optional. An optional array containing at most one supported order execution option. See Order execution options for details.


import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import pprint


class Order:
    def __init__(self, trade_data):
        self.gemini_api_key = "account-aerS4oOyTLRVHSXx6GVt"
        self.gemini_api_secret = "2ikQFyRkHvetQwZ3vXohVms9NTkr".encode()
        base_url = "https://api.sandbox.gemini.com"
        self.endpoint = "/v1/order/new"
        self.url = base_url + self.endpoint
        self.payload = {
        "request": self.endpoint,
            "nonce": '__NONCE__',
            "symbol": trade_data['symbol'],
            "amount": trade_data['amount'],
            "price": trade_data['price'],
            "side": trade_data['side'],
            "type": trade_data['type'],
            "options": trade_data['options']
        }
        self.nonce = self.create_nonce()
        self.create_payload()
        self.request_headers = self.create_request_headers()

    def create_nonce(self):
        t = datetime.datetime.now()
        return str(int(time.mktime(t.timetuple())*1000))

    def create_payload(self):
        self.payload['nonce'] = self.nonce
        self.payload_json = json.dumps(self.payload).encode()


    def create_request_headers(self):
        encoded_json = base64.b64encode(self.payload_json)
        signature = hmac.new(self.gemini_api_secret, encoded_json, hashlib.sha384).hexdigest()

        return { 'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': self.gemini_api_key,
                    'X-GEMINI-PAYLOAD': encoded_json,
                    'X-GEMINI-SIGNATURE': signature,
                    'Cache-Control': "no-cache" }

    def execute(self):
        response = requests.post(self.url,
                        data=None,
                        headers=self.request_headers)

        new_order = response.json()
        return new_order




def test_connection_error():
    import pytest
    with pytest.raises(requests.ConnectionError):
        o = Order(symbol='btcusd', amount='5', price="3655", side="buy", of_type="exchange limit", options=["maker-or-cancel"])
        o.url = "http://xxx"
        o.request_headers = o.create_request_headers()
        o.execute()

def create_expected(trade_data):
    return {
     'order_id': '301695025',
     'id': '301695025',
     'symbol': trade_data['symbol'],
     'exchange': 'gemini',
     'avg_execution_price': '0.00',
     'side': trade_data['side'],
     'type': trade_data['type'],
     'timestamp': '1570884791',
     'timestampms': 1570884791462,
     'is_live': True,
     'is_cancelled': False,
     'is_hidden': False,
     'was_forced': False,
     'executed_amount': '0',
     'remaining_amount': trade_data['amount'],
     'options': trade_data['options'],
     'price': trade_data['price'], 
     'original_amount': trade_data['amount']}

if __name__ == '__main__':
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    order_response = order.execute()
    print(type(order_response))
    print(order_response)
    print('-------')
    print(create_expected(trade_data))

