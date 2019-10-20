_NOTSET = object()


class _ScanIter:

    __slots__ = ("_scan", "_cur", "_ret")

    def __init__(self, scan):
        self._scan = scan
        self._cur = b"0"
        self._ret = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        while not self._ret and self._cur:
            self._cur, self._ret = await self._scan(self._cur)
        if not self._cur and not self._ret:
            raise StopAsyncIteration  # noqa
        else:
            ret = self._ret.pop(0)
            return ret


def _decode_item(item, encoding):
    if encoding and hasattr(item, "decode"):
        return item.decode(encoding)
    else:
        return item


def _decode_items(items, encoding):
    if encoding is None:
        return items
    else:
        return (
            item.decode(encoding) if hasattr(item, "decode") else item for item in items
        )
