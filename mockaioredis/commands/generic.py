"""Generic Redis commands"""
import asyncio
from mockredis.pipeline import MockRedisPipeline
from mockredis.exceptions import WatchError

from mockaioredis.util import _NOTSET


class AsyncMockRedisPipeline(MockRedisPipeline):

    async def execute(self):
        """
        Execute all of the saved commands and return results.
        """
        try:
            for key, value in self._watched_keys.items():
                if self.mock_redis.redis.get(self.mock_redis._encode(key)) != value:
                    raise WatchError("Watched variable changed.")
            results = []
            for command in self.commands:
                results.append(await command())
            return results
        finally:
            self._reset()


class GenericCommandsMixin:
    """Generic commands mixin
    """
    SET_IF_EXIST = "SET_IF_EXIST"
    SET_IF_NOT_EXIST = "SET_IF_NOT_EXIST"

    def pipeline(self, transaction=True, shard_hint=None):
        return AsyncMockRedisPipeline(self, transaction, shard_hint)

    async def delete(self, key, *keys):
        """Delete specified key(s)"""
        return self._redis.delete(key, *keys)

    async def exists(self, key, *keys):
        """Check if key(s) exist

        Like in Redis 3.0.3+, returns int count of existing keys.
        If the same existing key is given multiple times, it is
        counted multiple times.
        """
        all_keys = (key,) + keys
        existing = 0
        # redis-py and, by extension mockredispy still only support
        # single-key checks that return True/False
        for k in all_keys:
            if self._redis.exists(k):
                existing += 1

        return existing

    async def expire(self, key, timeout):
        """Set a timeout on a key

        For now, only supports integer timeouts, until pexpire is implemented
        """
        # TODO: support float timeouts and forward to pexpire, like aio-redis
        if not isinstance(timeout, int):
            raise TypeError(
                "timeout argument must be int, not {!r}".format(timeout))
        return self._redis.expire(key, timeout)

    async def get(self, key, encoding=_NOTSET):
        """Gets the value of a key"""
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.get(key)

        if encoding is None:
            return ret

        if hasattr(ret, 'decode'):
            ret = ret.decode(encoding)
        return ret

    async def incr(self, key):
        """Increments key by 1"""
        return self._redis.incr(key)

    async def incrby(self, key, amount):
        """Increments key by the amount specified"""
        return self._redis.incrby(key, amount)

    async def keys(self, pattern, *, encoding=_NOTSET):
        """Returns all keys matching pattern."""
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.keys(pattern)

        if encoding is None:
            return ret

        return list(map(lambda x: x.decode(encoding), ret))

    async def mget(self, keys, *args, encoding=_NOTSET):
        """Returns all keys matching pattern."""
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.mget(keys, *args)

        if encoding is None:
            return ret

        return list(map(lambda x: x.decode(encoding), ret))

    async def set(self, key, value, *, expire=None, pexpire=None, exist=None):
        """Sets the value of a key"""
        nx = xx = False
        if exist is self.SET_IF_EXIST:
            xx = True
        elif exist is self.SET_IF_NOT_EXIST:
            nx = True
        return self._redis.set(key, value, ex=expire, px=pexpire, nx=nx, xx=xx)

    async def ttl(self, key):
        """Return the TTL of a key in seconds"""
        return self._redis.ttl(key)

    async def dbsize(self):
        return self._redis.dbsize()

    async def scan(self, cursor=0, match=None, count=None):
        """Incrementally iterate the keys space."""
        return self._redis.scan(cursor=cursor, match=match, count=count)
