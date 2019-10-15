import pytest
import requests
from ...test_library.order import Order
from ...test_library.test_tools import create_expected
from ...test_library.test_tools import is_same
from ...test_library.status_codes import HttpStatu

@pytest.mark.xxx
def test_btcusd_buy_maker_or_cancel_client_order_id_success():
    trade_data = {
        'symbol':'btcusd',
        'client_order_id': '44',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["maker-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL



@pytest.mark.passing
def test_btcusd_buy_maker_or_cancel_success():
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
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL

@pytest.mark.passing
def test_btcusd_sell_maker_or_cancel_success():
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
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL


@pytest.mark.passing
def test_btcusd_buy_immediate_or_cancel_success():
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["immediate-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL


@pytest.mark.passing
def test_btcusd_sell_immediate_or_cancel_success():
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'sell',
        'type': 'exchange limit',
        'options': ["immediate-or-cancel"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL


@pytest.mark.passing
def test_btcusd_buy_fill_or_kill_success():
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["fill-or-kill"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL

@pytest.mark.passing
def test_btcusd_sell_fill_or_kill_success():
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'sell',
        'type': 'exchange limit',
        'options': ["fill-or-kill"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL

@pytest.mark.failing
def test_btcusd_buy_auction_only_success():
    """ the response is showing for type="auction only limit" where
    the documentation states that only "exchange limit is supported.

    This is a possible bug. Kindly see ticket #43524
    """
    trade_data = {
        'symbol':'btcusd',
        'amount': '5',
        'price': '3655.00',
        'side': 'buy',
        'type': 'exchange limit',
        'options': ["auction-only"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL

@pytest.mark.undetermined
def test_btcusd_sell_indication_of_interest_success():
    """ this test is timing out when amount is 100 , produces 504 error code 
    
        This may be a possible bug. Kindly see ticket #98374
    """
    trade_data = {
        'symbol':'btcusd',
        'amount': '100',
        'price': '3655.00',
        'side': 'sell',
        'type': 'exchange limit',
        'options': ["indication-of-interest"]
    }
    actual_response = Order(trade_data).execute()
    expected_response = create_expected(trade_data)
    assert is_same(expected_response, actual_response.response_json) == True, actual_response.text
    assert actual_response.response_code == HttpStatus.SUCCESSFUL


if __name__ == '__main__':
    test_btcusd_sell_indication_of_interest_success()