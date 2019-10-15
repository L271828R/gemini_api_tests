import datetime
from datetime import timedelta

class NonceCounter:
    """This Nonce static counter allows for multiple tests
     to run while avoiding time.sleep() functions"""
    last = datetime.datetime.now().replace(microsecond=0)

    @classmethod
    def get_count(cls):
        now = datetime.datetime.now().replace(microsecond=0) 
        while (now <= cls.last):
            now = now + timedelta(seconds=1)
        cls.last = now
        return cls.last


