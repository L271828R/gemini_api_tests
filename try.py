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
    def __init__(self, symbol, amount, price, side, of_type, options):
        self.gemini_api_key = "account-aerS4oOyTLRVHSXx6GVt"
        self.gemini_api_secret = "2ikQFyRkHvetQwZ3vXohVms9NTkr".encode()
        base_url = "https://api.sandbox.gemini.com"
        self.endpoint = "/v1/order/new"
        self.url = base_url + self.endpoint
        self.payload = {
        "request": self.endpoint,
            "nonce": '__NONCE__',
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": side,
            "type": of_type,
            "options": ["maker-or-cancel"] 
        }

    def execute(self):
        t = datetime.datetime.now()
        payload_nonce =  str(int(time.mktime(t.timetuple())*1000))
        self.payload['nonce'] = payload_nonce

        encoded_payload = json.dumps(self.payload).encode()
        b64 = base64.b64encode(encoded_payload)
        signature = hmac.new(self.gemini_api_secret, b64, hashlib.sha384).hexdigest()

        request_headers = { 'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': self.gemini_api_key,
                    'X-GEMINI-PAYLOAD': b64,
                    'X-GEMINI-SIGNATURE': signature,
                    'Cache-Control': "no-cache" }

        response = requests.post(self.url,
                        data=None,
                        headers=request_headers)

        new_order = response.json()
        # print(new_order)
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(new_order)

if __name__ == '__main__':
    o = Order(symbol='btcusd', amount='5', price="3655", side="buy", of_type="exchange limit", options=["maker-or-cancel"])
    o.execute()
