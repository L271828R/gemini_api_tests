
import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import pprint
import pytest
import time
import sys
from .config import Config
from .nonce_counter import NonceCounter

class Response:
    def __init__(self, response_json, response_code, requests_response):
        self.response_json = response_json
        self.response_code = response_code
        self.text = requests_response.text


class Order:
    """ Order takes a dictionary of trade data
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'sell',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    
    order = Order(trade_data)

    and returns a requests libray response
    response = order.execute()
    """
    def __init__(self, trade_data, config=Config):
        self.config = config
        self.gemini_api_key = config.GEMINI_API_KEY
        self.gemini_api_secret = config.GEMINI_API_SECRET.encode()
        self.base_url = config.BASE_URL
        self.endpoint = config.ENDPOINT
        self.encoded_json = None
        self.signature = None
        self.request_headers = None
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
        self.create_request_headers()

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
        self.request_headers= { 'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': self.gemini_api_key,
                    'X-GEMINI-PAYLOAD': self.encoded_json,
                    'X-GEMINI-SIGNATURE': self.signature,
                    'Cache-Control': "no-cache" }
        return self.request_headers


    def log_a_usable_curl(self):
        if self.config.DEBUG == True:
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

    def execute(self, disable_curl=False):
        response = requests.post(self.url,
                        data=None,
                        headers=self.request_headers)
        if not response.status_code >= 500:
            json = response.json()
        else:
            json = {}
        code = response.status_code
        if disable_curl == False:
            self.log_a_usable_curl()
        return Response(response_json=json, response_code=code, requests_response=response)

