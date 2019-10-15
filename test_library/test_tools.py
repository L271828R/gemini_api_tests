
import pprint


def create_expected(trade_data):
    return {
     'symbol': trade_data['symbol'],
     'exchange': 'gemini',
     'side': trade_data['side'],
     'type': trade_data['type'],
     'was_forced': False,
     'options': trade_data['options'],
     'price': trade_data['price'], 
     'original_amount': trade_data['amount']}

def is_same(expected, actual):
    """is_same takes two responses and compares non volatile elements"""
    expected_volatile_elements_removed = expected
    copy_of_actual_volatile_elements_removed = actual.copy()
    if expected_volatile_elements_removed['options'] != ['indication-of-interest']:
        assert(actual['order_id'] != '')
        assert(actual['id'] != '')
        assert(actual['timestamp'] != '')
        assert(actual['timestampms'] != '')
        assert( actual['is_cancelled'] in [True, False])
        assert( actual['is_live'] in [True, False])
        assert( actual['avg_execution_price'] != '')
        assert( actual['executed_amount'] != '')
        assert( actual['remaining_amount'] != '')
        assert( actual['is_hidden'] != '')
        del copy_of_actual_volatile_elements_removed['is_cancelled']
        del copy_of_actual_volatile_elements_removed['is_hidden']
        del copy_of_actual_volatile_elements_removed['avg_execution_price']
        del copy_of_actual_volatile_elements_removed['executed_amount']
        del copy_of_actual_volatile_elements_removed['remaining_amount']
        del copy_of_actual_volatile_elements_removed['is_live']
        del copy_of_actual_volatile_elements_removed['order_id']
        del copy_of_actual_volatile_elements_removed['id']
        del copy_of_actual_volatile_elements_removed['timestamp']
        del copy_of_actual_volatile_elements_removed['timestampms']
    if 'reason' in copy_of_actual_volatile_elements_removed:
        del copy_of_actual_volatile_elements_removed['reason']
    pp = pprint.PrettyPrinter()
    print('\r\n actual response')
    pp.pprint(copy_of_actual_volatile_elements_removed)
    print('\r\n expected response')
    pp.pprint(expected_volatile_elements_removed)
    return expected_volatile_elements_removed == copy_of_actual_volatile_elements_removed
