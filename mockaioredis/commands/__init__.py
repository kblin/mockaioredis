from mockredis import MockRedis as _MockRedis

from .generic import GenericCommandsMixin
from .hash import HashCommandsMixin
from .list import ListCommandsMixin
from .set import SetCommandsMixin

__all__ = ['MockRedis']


class MockRedis(GenericCommandsMixin, HashCommandsMixin, ListCommandsMixin, SetCommandsMixin):
    """Fake high-level aioredis.Redis interface"""

    def __init__(self, connection=None, encoding=None, **kwargs):

        # Just for API compatibility
        self._conn = connection
        self._redis = _MockRedis(**kwargs)

        self._encoding = encoding

    async def wait_closed(self):
        if self._conn:
            await self._conn.wait_closed()

    def close(self):
        if self._conn:
            self._conn.close()

async def create_redis(address, *, db=None, password=None, ssl=None,
                       encoding=None, commands_factory=MockRedis,
                       loop=None):
    '''Create a fake high-level MockRedis interface

    This function is a coroutine
    '''
    return commands_factory(None, encoding=encoding)
