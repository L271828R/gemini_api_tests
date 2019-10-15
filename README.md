# Description

This is the take home test for Gemini corp.

# Requirements

The tests require Python3, pytest, requests
and the pprint library.

# How to install required libraries

pip install -r requirements.txt

# How to run tests

Thre are four taggings for the tests created

* passing
* failing
* indetermined
* negative

# How to run passing tests

from the root folder run:

```
>> pytest -m passing
```

These are tests that are currently
passing as of the submition.

# How to run failing tests

```
>> pytest -m failing
```

These are the tests that fail. Kindly see
the notes on these tests for more details.

# How to run indetermined tests

```
>> pytest -m indetermined
```

These are tests that are timing out despite
having correct fields filled.


# How to run negative tests

```
>> pytest -m negative
```

These are tests that fail for expected
reasons.


# How to use the Order object to buil a test

The Order object accepts a dictionary
with trade data in its constructor.

One can then choose to execute
such as:

```python
trade_data = {
    'symbol':'btcusd',
    'client_order_id':'44',
    'amount': '5',
    'price': '3655.00',
    'side': 'buy',
    'type': 'exchange limit',
    'options': ["maker-or-cancel"]
}
actual_response = Order(trade_data).execute()
```

One can create the Order object and then
execute the following methods:

```python
trade_data = {
    'symbol':'btcusd',
    'amount': '99',
    'price': '4444.00',
    'side': 'buy',
    'type': 'exchange limit',
    'options': ["maker-or-cancel"]
}
order = Order(trade_data)
order.create_payload()
order.create_encoded_json()
order.create_signiture()
order.create_request_headers()
actual_response = order.execute()
```

order.execute() has a dependency on the
below methods in this particular order:

```python
order.create_payload()
order.create_encoded_json()
order.create_signiture()
order.create_requested_headers()
```

```python
order.create_payload()

# prepares member:

order.payload_json


order.create_encoded_json()

# prepares member:

order.encoded_json

order.create_signiture()

# prepares member:

order.signiture

order.create_request_headers()

# prepares member:

order.requested_headers
```

# Changing test configuration

To change the secret, api key, base url or endpoint
kindly see the file config.py


# Extras

Kindly notice that the stdout of each test will provide
a curl output so as to test in Postman or any curl like tools.

This can be disabled by setting the member in config.py

DEBUG=False

