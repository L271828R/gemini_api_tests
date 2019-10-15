import pytest
import requests
from ...test_library.order import Order
from ...test_library.test_tools import create_expected
from ...test_library.test_tools import is_same
from ...test_library.status_codes import HttpStatus


@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_amount_missing_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid quantity for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidQuantity"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_price_missing_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': '',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid price for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidPrice"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_side_missing_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': '3655.00',
        'side': '',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid side for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidSide"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_type_missing_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': '',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid order type for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidOrderType"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR

@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_options_missing_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': [""]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == 'Option "" is not supported'
    actual_response.response_json['reason'] == "UnsupportedOption"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR

@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_negative_amount_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '-5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid quantity for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidQuantity"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR

@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_alpha_amount_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': 'xxx',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid quantity for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidQuantity"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR


@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_negative_price_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': '-3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid price for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidPrice"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR 

@pytest.mark.passing
@pytest.mark.negative
def test_ethusd_alpha_price_failure():
    trade_data = {
        'symbol':'ethusd',
        'amount': '5',
        'price': 'xxx',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    actual_response.response_json['message'] == "Invalid price for symbol ethUSD"
    actual_response.response_json['reason'] == "InvalidPrice"
    actual_response.response_json['result'] == "error"
    assert actual_response.response_code == HttpStatus.ERROR
