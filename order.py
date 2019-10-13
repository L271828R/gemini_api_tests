
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

