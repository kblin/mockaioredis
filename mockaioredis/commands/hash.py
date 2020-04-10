from mockaioredis.util import _NOTSET

class HashCommandsMixin:

    async def hset(self, key, field, value):
        return self._redis.hset(key, field, value)

    async def hget(self, key, field, encoding=_NOTSET):
        if encoding == _NOTSET:
            encoding = self._encoding
        ret = self._redis.hget(key, field)

        if encoding is None:
            return ret

        if hasattr(ret, 'decode'):
            ret = ret.decode(encoding)
        return ret

    async def hexists(self, key, filed):
        return self._redis.hexists(key, filed)

    async def hgetall(self, key, encoding=_NOTSET):
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

    async def hmset(self, key, field, value, *pairs):
        if len(pairs) % 2 != 0:
            raise TypeError("length of pairs must be an even number")
        it = iter( (field, value) + pairs )
        arg_dict = dict(zip(it, it))
        return self._redis.hmset(key, arg_dict)

    async def hmset_dict(self, key, *args, **kwargs):
        if not args and not kwargs:
            raise TypeError("args or kwargs must be specified")
        if len(args) > 1:
            raise TypeError("only one arg allowed")
        args_dict = {}
        if len(args) == 1:
            if not isinstance(args[0], dict):
                raise TypeError("args[0] must be a dict")
            args_dict = args[0].copy()
        args_dict.update(kwargs)
        return self._redis.hmset(key, args_dict)

    async def hmget(self, key, field, *fields, encoding=_NOTSET):
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

    async def hdel(self, key, field, *fields):
        """Delete one or more hash fields."""

        return self._redis.hdel(key, field, *fields)

    async def hkeys(self, key, *, encoding=_NOTSET):
        """Get all the fields in a hash."""

        if encoding == _NOTSET:
            encoding = self._encoding

        ret = self._redis.hkeys(key)

        if encoding is None:
            return ret

        new = []
        for val in ret:
            if hasattr(val, 'decode'):
                val = val.decode(encoding)
            new.append(val)

        return new
