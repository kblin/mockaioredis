'Generic Redis commands'
from mockaioredis.util import _NOTSET


class GenericCommandsMixin:
    '''Generic commands mixin
    '''

    async def delete(self, key, *keys):
        '''Delete specified key(s)'''
        return self._redis.delete(key, *keys)

    async def exists(self, key, *keys):
        '''Check if key(s) exist

        Like in Redis 3.0.3+, returns int count of existing keys.
        If the same existing key is given multiple times, it is
        counted multiple times.
        '''
        all_keys = (key, ) + keys
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
        '''Gets the value of a key'''
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.get(key)

        if encoding is None:
            return ret

        if hasattr(ret, 'decode'):
            ret = ret.decode(encoding)
        return ret

    async def incr(self, key, amount=1):
        '''Increments key by the amount specified'''
        return self._redis.incr(key, amount)

    incrby = incr

    async def keys(self, pattern, *, encoding=_NOTSET):
        """Returns all keys matching pattern."""
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.keys(pattern)

        if encoding is None:
            return ret

        return list(map(lambda x: x.decode(encoding), ret))

    async def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        '''Sets the value of a key'''
        return self._redis.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    async def ttl(self, key):
        """Return the TTL of a key in seconds"""
        return self._redis.ttl(key)
