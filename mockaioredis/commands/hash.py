import asyncio

from mockaioredis.util import _NOTSET

class HashCommandsMixin:

    @asyncio.coroutine
    def hset(self, key, field, value):
        return self._redis.hset(key, field, value)

    @asyncio.coroutine
    def hget(self, key, field, encoding=_NOTSET):
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.hget(key, field)

        if encoding is None:
            return ret

        if hasattr(ret, 'decode'):
            ret = ret.decode(encoding)
        return ret

    @asyncio.coroutine
    def hgetall(self, key, encoding=_NOTSET):
        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.hgetall(key)
        if encoding is None:
            return ret
        new = {}
        for k, v in ret.items():
            k = k.decode(encoding)
            if hasattr(v, 'decode'):
                v = v.decode(encoding)
            new[k] = v

        return new

    @asyncio.coroutine
    def hmset(self, key, field, value, *pairs):
        if len(pairs) % 2 != 0:
            raise TypeError("length of pairs must be an even number")
        it = iter( (field, value) + pairs )
        arg_dict = dict(zip(it, it))
        return self._redis.hmset(key, arg_dict)

    @asyncio.coroutine
    def hmset_dict(self, key, *args, **kwargs):
        args_dict = args[0].copy()
        args_dict.update(kwargs)
        return self._redis.hmset(key, args_dict)

    @asyncio.coroutine
    def hmget(self, key, field, *fields, encoding=_NOTSET):
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.hmget(key, field, *fields)

        if encoding is None:
            return ret

        new = []
        for val in ret:
            if hasattr(val, 'decode'):
                val = val.decode(encoding)
            new.append(val)

        return new


