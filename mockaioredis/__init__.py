from mockredis import MockRedis as _MockRedis

from .hash import HashCommandsMixin

__all__ = ['MockRedis']

class MockRedis(HashCommandsMixin):
    '''Fake high-level aioredis.Redis interface'''

    def __init__(self, connection=None, encoding=None):
        # Just for API compatibility
        self._conn = connection
        self._redis = _MockRedis()

        self._encoding = encoding
