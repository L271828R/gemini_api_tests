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
import pytest
import curlify
import time
import sys
from config import Config
from nonce_counter import NonceCounter


DEBUG = Config.DEBUG

class Order:
    def __init__(self, trade_data):
        self.gemini_api_key = Config.GEMINI_API_KEY
        self.gemini_api_secret = Config.GEMINI_API_SECRET.encode()
        self.base_url = Config.BASE_URL
        self.endpoint = Config.ENDPOINT
        self.encoded_json = None
        self.signature = None
        self.url = self.base_url + self.endpoint
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
        self.create_payload()
        self.create_encoded_json()
        self.create_signiture()
        self.request_headers = self.create_request_headers()

    def create_nonce(self):
        t = NonceCounter.get_count()
        return str(int(time.mktime(t.timetuple())*1000))

    def create_payload(self):
        payload_copy = self.payload.copy() 
        payload_copy['nonce'] = self.create_nonce()
        self.payload_json = json.dumps(payload_copy).encode()
        return self.payload_json

    def create_signiture(self):
        self.signature = hmac.new(self.gemini_api_secret, self.encoded_json, hashlib.sha384).hexdigest()
        return self.signature

    def create_encoded_json(self):
        self.encoded_json = base64.b64encode(self.payload_json)
        return self.encoded_json

    def create_request_headers(self):
        return { 'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': self.gemini_api_key,
                    'X-GEMINI-PAYLOAD': self.encoded_json,
                    'X-GEMINI-SIGNATURE': self.signature,
                    'Cache-Control': "no-cache" }


    def log_a_usable_curl(self):
        if DEBUG == True:
            payload = base64.b64encode(self.create_payload())
            self.create_encoded_json()
            signiture = self.create_signiture()
            template = """curl -X POST -H 'Accept: */*' 
            -H 'Accept-Encoding: gzip, deflate' 
            -H 'Cache-Control: no-cache' 
            -H 'Connection: keep-alive' 
            -H 'Content-Length: 0' 
            -H 'Content-Type: text/plain' 
            -H 'User-Agent: python-requests/2.22.0' 
            -H 'X-GEMINI-APIKEY: __ACCOUNT_KEY__' 
            -H 'X-GEMINI-PAYLOAD: __PAYLOAD__'
            -H 'X-GEMINI-SIGNATURE: __SIGNITURE__'
            __URL__"""
            s = template.replace('__ACCOUNT_KEY__', self.gemini_api_key)
            s = s.replace('__PAYLOAD__', str(payload.decode()))
            s = s.replace('__SIGNITURE__', signiture)
            s = s.replace('__URL__', self.url)
            print(s)

    def execute(self):
        response = requests.post(self.url,
                        data=None,
                        headers=self.request_headers)
        new_order = response.json()
        self.log_a_usable_curl()
        return new_order




def texst_connection_error():
    """this test doesn't test anything LOL"""
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    
    with pytest.raises(requests.ConnectionError):
        o = Order(trade_data)
        o.url = "http://xxx"
        o.request_headers = o.create_request_headers()
        o.execute()

def create_expected(trade_data):
    return {
     'symbol': trade_data['symbol'],
     'exchange': 'gemini',
     'avg_execution_price': '0.00',
     'side': trade_data['side'],
     'type': trade_data['type'],
     'is_live': True,
     'is_cancelled': False,
     'is_hidden': False,
     'was_forced': False,
     'executed_amount': '0',
     'remaining_amount': trade_data['amount'],
     'options': trade_data['options'],
     'price': trade_data['price'], 
     'original_amount': trade_data['amount']}

def is_same(expected, actual):
    expected_with_volatile_elements_removed = expected
    assert(actual['order_id'] != '')
    assert(actual['id'] != '')
    assert(actual['timestamp'] != '')
    assert(actual['timestampms'] != '')
    copy_of_actual_volatile_elements_removed = actual.copy()
    del copy_of_actual_volatile_elements_removed['order_id']
    del copy_of_actual_volatile_elements_removed['id']
    del copy_of_actual_volatile_elements_removed['timestamp']
    del copy_of_actual_volatile_elements_removed['timestampms']
    return expected_with_volatile_elements_removed == copy_of_actual_volatile_elements_removed


def test_happy_path():
# if __name__ == '__main__':
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response) == True

if __name__ == '__main__':
    test_happy_path()