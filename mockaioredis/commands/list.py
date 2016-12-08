'List commands'

from mockaioredis.util import _NOTSET

class ListCommandsMixin:
    '''List commands mixin

    Rum (some) of the Redis list commands
    '''

    async def llen(self, key):
        '''Returns the length of the list stored at key'''
        return self._redis.llen(key)


    async def lpush(self, key, value, *values):
        '''Insert specified values at the head of the list'''
        return self._redis.lpush(key, value, *values)


    async def lpop(self, key, *, encoding=_NOTSET):
        '''Pop a value off the head of the list'''
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.lpop(key)

        if encoding is None:
            return ret

        return ret.decode(encoding)


    async def rpush(self, key, value, *values):
        '''Insert specified values at the tail of the list'''
        return self._redis.rpush(key, value, *values)


    async def rpop(self, key, *, encoding=_NOTSET):
        '''Pop a value off the tail of the list'''
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.rpop(key)

        if encoding is None:
            return ret

        return ret.decode(encoding)
