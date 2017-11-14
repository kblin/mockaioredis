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

    async def lrange(self, key, start, stop, *, encoding=_NOTSET):
        """Returns the specified elements of the list stored at key.

        :raises TypeError: if start or stop is not int
        """
        if encoding == _NOTSET:
            encoding = self._encoding

        if not isinstance(start, int):
            raise TypeError("start is not of type int")
        if not isinstance(stop, int):
            raise TypeError("stop is not of type int")

        ret = self._redis.lrange(key, start, stop)

        if encoding is None:
            return ret

        return list(map(lambda x: x.decode(encoding), ret))

    async def rpoplpush(self, sourcekey, destkey, *, encoding=_NOTSET):
        """Atomically returns and removes the last element (tail) of the
        list stored at source, and pushes the element at the first element
        (head) of the list stored at destination.
        """
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.rpoplpush(sourcekey, destkey)

        if encoding is None:
            return ret

        return ret.decode(encoding)
