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
def test_invalid_api_key_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '99',
        'price': '4444.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    order.request_headers['X-GEMINI-APIKEY'] = "xxx"
    actual_response = order.execute(disable_curl=True)
    assert actual_response.response_json['message'] == 'InvalidSignature'
    assert actual_response.response_json['reason'] == 'InvalidSignature'
    assert actual_response.response_json['result'] == 'error'
    assert actual_response.response_code == HttpStatus.ERROR

@pytest.mark.negative
def test_invalid_secret_failure():
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
    order.gemini_api_secret = "xxx".encode()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute(disable_curl=True)
    assert actual_response.response_json['message'] == 'InvalidSignature'
    assert actual_response.response_json['reason'] == 'InvalidSignature'
    assert actual_response.response_json['result'] == 'error'
    assert actual_response.response_code == HttpStatus.ERROR

@pytest.mark.negative
def test_missing_amount_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['amount']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order for symbol BTCUSD was missing required field 'amount'"
    actual_response.response_json['reason'] == "MissingQuantity"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_missing_symbol_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['symbol']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order was missing required field" + \
        " 'symbol' with supported values ['BTCUSD', 'ETHBTC', 'ETHUSD', 'BCHUSD', " + \
        "'BCHBTC', 'BCHETH', 'LTCUSD', 'LTCBTC', 'LTCETH', 'LTCBCH', 'ZECUSD'," + \
        "'ZECBTC', 'ZECETH', 'ZECBCH', 'ZECLTC']"
    actual_response.response_json['reason'] == "MissingSymbol"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_missing_price_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['price']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order for symbol BTCUSD was missing required field 'price'"
    actual_response.response_json['reason'] == "MissingPrice"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR



@pytest.mark.negative
def test_missing_side_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['side']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order for symbol BTCUSD was missing required field 'side'"
    actual_response.response_json['reason'] == "MisingSide"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_missing_side_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['side']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order for symbol BTCUSD was missing required field 'side'"
    actual_response.response_json['reason'] == "MissingSide"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.negative
def test_missing_type_field_failure():
    trade_data = {
        'symbol':'btcusd',
        'amount': '4',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    order = Order(trade_data)
    del order.payload['type']
    order.create_payload()
    order.create_encoded_json()
    order.create_signiture()
    order.create_request_headers()
    actual_response = order.execute()
    actual_response.response_json['message'] == "Order for symbol BTCUSD was missing required field 'type'"
    actual_response.response_json['reason'] == "MissingType"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR



