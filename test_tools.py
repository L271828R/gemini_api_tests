
def create_expected(trade_data):
    return {
     'symbol': trade_data['symbol'],
     'exchange': 'gemini',
     'avg_execution_price': '0.00',
     'side': trade_data['side'],
     'type': trade_data['type'],
     'is_hidden': False,
     'was_forced': False,
     'executed_amount': '0',
     'remaining_amount': trade_data['amount'],
     'options': trade_data['options'],
     'price': trade_data['price'], 
     'original_amount': trade_data['amount']}

def is_same(expected, actual):
    """is_same takes two responses and compares non volatile elements"""
    expected_with_volatile_elements_removed = expected
    assert(actual['order_id'] != '')
    assert(actual['id'] != '')
    assert(actual['timestamp'] != '')
    assert(actual['timestampms'] != '')
    assert( actual['is_cancelled'] in [True, False])
    assert( actual['is_live'] in [True, False])
    copy_of_actual_volatile_elements_removed = actual.copy()
    if 'reason' in copy_of_actual_volatile_elements_removed:
        del copy_of_actual_volatile_elements_removed['reason']
    del copy_of_actual_volatile_elements_removed['is_cancelled']
    del copy_of_actual_volatile_elements_removed['is_live']
    del copy_of_actual_volatile_elements_removed['order_id']
    del copy_of_actual_volatile_elements_removed['id']
    del copy_of_actual_volatile_elements_removed['timestamp']
    del copy_of_actual_volatile_elements_removed['timestampms']
    return expected_with_volatile_elements_removed == copy_of_actual_volatile_elements_removed
