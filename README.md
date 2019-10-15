# Description

This is the take home test for Gemini corp.
The tests requires Python3, the pytest, and the 
requests library.

# Requirements

Python3

# How to install required libraries

pip install -r requirements.txt

# How to run tests

Thre are four taggings for the tests created

passing
failing
indetermined
negative

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

These are tests that fail. Kindly see
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

