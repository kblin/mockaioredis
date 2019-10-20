import asyncio

from aioredis.errors import ReplyError

from mockaioredis.util import _NOTSET, _decode_item, _decode_items, _ScanIter


class SetCommandsMixin:
    @asyncio.coroutine
    def sadd(self, key, *values):
        """Add one or more members to a set."""
        return self._redis.sadd(key, *values)

    @asyncio.coroutine
    def scard(self, key):
        """Get the number of members in a set."""
        return self._redis.scard(key)

    @asyncio.coroutine
    def sdiff(self, key, *keys):
        """Subtract multiple sets."""
        return list(self._redis.sdiff(key, *keys))

    @asyncio.coroutine
    def sdiffstore(self, destkey, key, *keys):
        """Subtract multiple sets and store the resulting set in a key."""
        return self._redis.sdiffstore(destkey, key, *keys)

    @asyncio.coroutine
    def sinter(self, key, *keys):
        """Intersect multiple sets.

        Warning: order is not consistent with aioredis
        """
        return list(self._redis.sinter(key, *keys))

    @asyncio.coroutine
    def sinterstore(self, destkey, key, *keys):
        """Intersect multiple sets and store the resulting set in a key."""
        return self._redis.sinterstore(destkey, key, *keys)

    @asyncio.coroutine
    def sismember(self, key, member):
        """Determine if a given value is a member of a set."""
        return self._redis.sismember(key, member)

    @asyncio.coroutine
    def smembers(self, key, *, encoding=_NOTSET):
        """Get all the members in a set.

        Warning: order is not consistent with aioredis
        """
        if encoding == _NOTSET:
            encoding = self._encoding

        items = self._redis.smembers(key)
        return list(_decode_items(items, encoding))

    @asyncio.coroutine
    def smove(self, sourcekey, destkey, member):
        """Move a member from one set to another."""
        try:
            return int(self._redis.smove(sourcekey, destkey, member))
        except TypeError:
            raise ReplyError("WRONGTYPE")

    @asyncio.coroutine
    def spop(self, key, count=None, *, encoding=_NOTSET):
        """Remove and return one or multiple random members from a set."""
        if encoding == _NOTSET:
            encoding = self._encoding

        if count is None:
            value = self._redis.spop(key)
            return _decode_item(value, encoding)

        if count == 0:
            return []
        if count < 0:
            raise ReplyError("ERR index out of range")

        total = len(self._redis.smembers(key))
        count = min(count, total)
        values = (self._redis.spop(key) for _ in range(count))
        return list(_decode_items(values, encoding))

    @asyncio.coroutine
    def srandmember(self, key, count=None, *, encoding=_NOTSET):
        """Get one or multiple random members from a set."""
        if encoding == _NOTSET:
            encoding = self._encoding

        if count is None:
            value = self._redis.srandmember(key)
            return _decode_item(value, encoding)

        if count == 0:
            return []

        if count < 0:
            # Allow duplicates
            count = -count
            output = [self._redis.srandmember(key) for _ in range(count)]
        else:
            # Don't allow duplicates
            original = self._redis.smembers(key)
            count = min(count, len(original))
            output = [self._redis.spop(key) for _ in range(count)]
            self._redis.sadd(key, *original)

        return list(_decode_items(output, encoding))

    @asyncio.coroutine
    def srem(self, key, member, *members):
        """Remove one or more members from a set."""
        return self._redis.srem(key, member, *members)

    @asyncio.coroutine
    def sunion(self, key, *keys):
        """Add multiple sets."""
        return self._redis.sunion(key, *keys)

    @asyncio.coroutine
    def sunionstore(self, destkey, key, *keys):
        """Add multiple sets and store the resulting set in a key."""
        return self._redis.sunionstore(destkey, key, *keys)

    @asyncio.coroutine
    def sscan(self, key, cursor=0, match=None, count=None):
        """Incrementally iterate Set elements."""
        return list(self._redis.sscan(key, cursor, match, count))

    def isscan(self, key, *, match=None, count=None):
        """Incrementally iterate set elements using async for.

        Usage example:

        >>> async for val in redis.isscan(key, match='something*'):
        ...     print('Matched:', val)

        """
        return _ScanIter(lambda cur: self.sscan(key, cur, match=match, count=count))
