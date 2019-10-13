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

import pytest
import requests
from order import Order
from test_tools import create_expected
from test_tools import is_same

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


def test_happy_path_buy():
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

def test_happy_path_sell():
# if __name__ == '__main__':
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'sell',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response) == True


if __name__ == '__main__':
    test_happy_path_sell()