import pytest
import requests
from ...test_library.order import Order
from ...test_library.test_tools import create_expected
from ...test_library.test_tools import is_same
from ...test_library.status_codes import HttpStatus


@pytest.mark.negative
def test_empty_payload_failure():
    """this test overrides internal members so as to produce a payload with an 
    invalide json"""
    trade_data = {
        'symbol':'btcusd',
        'amount': '99',
        'price': '4444.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    order.payload_json = "".encode()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute(disable_curl=True)
    assert actual_response.response_json['message'] == 'InvalidJson'
    assert actual_response.response_json['reason'] == 'InvalidJson'
    assert actual_response.response_json['result'] == 'error'
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_invalid_json_failure():
    """this test removes the closing '}' from the payload so 
    as to produce an invalid json"""
    trade_data = {
        'symbol':'btcusd',
        'amount': '99',
        'price': '4444.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    order.payload_json = order.payload_json.decode().replace('}','').encode()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute(disable_curl=True)
    assert actual_response.response_json['message'] == 'InvalidJson'
    assert actual_response.response_json['reason'] == 'InvalidJson'
    assert actual_response.response_json['result'] == 'error'
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_invalid_secret_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '99',
        'price': '4444.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    order.payload_json = order.payload_json.decode().replace('}','').encode()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute(disable_curl=True)
    assert actual_response.response_json['message'] == 'InvalidJson'
    assert actual_response.response_json['reason'] == 'InvalidJson'
    assert actual_response.response_json['result'] == 'error'
    assert actual_response.response_code == HttpStatus.ERROR