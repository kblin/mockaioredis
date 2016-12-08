'Fake aioredis.RedisPool and related functions'
import asyncio
import collections

from .util import _NOTSET
from .commands import MockRedis, create_redis


async def create_pool(address, *, db=0, password=None, ssl=None, encoding=None,
                      minsize=1, maxsize=10, commands_factory=_NOTSET, loop=None):
    if commands_factory == _NOTSET:
        commands_factory = MockRedis

    pool = MockRedisPool(address, db, password, encoding,
                         minsize=minsize, maxsize=maxsize,
                         commands_factory=commands_factory,
                         ssl=ssl, loop=loop)
    try:
        await pool._fill_free(override_min=False)
    except Exception as ex:
        pool.close()
        await pool.wait_closed()
        raise

    return pool


class MockRedisPool:
    '''Imitate a aioredis.RedisPool

    Or at least enough of it to create, use and close a pool
    '''
    def __init__(self, address, db=0, password=0, encoding=None,
                 *, minsize, maxsize, commands_factory, ssl=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._address = address
        self._db = db
        self._password = password
        self._encoding = encoding
        self._minsize = minsize
        self._maxsize = maxsize
        self._factory = commands_factory
        self._ssl = ssl
        self._loop = loop

        # fake it here, we always only have one connection
        self._pool = collections.deque(maxlen=1)
        self._used = set()
        self._acquiring = 0

        self._cond = asyncio.Condition(loop=loop)
        self._close_state = asyncio.Event(loop=loop)
        self._close_waiter = asyncio.ensure_future(self._do_close(), loop=loop)


    @property
    def minsize(self):
        '''always return 1'''
        return 1


    @property
    def maxsize(self):
        '''always return 1'''
        return 1


    @property
    def size(self):
        return self.freesize + len(self._used) + self._acquiring


    @property
    def freesize(self):
        return len(self._pool)


    async def _do_close(self):
        await self._close_state.wait()
        async with self._cond:
            waiters = []
            while self._pool:
                conn = self._pool.popleft()
            # fake connections, so no need to do anything for used connections


    def close(self):
        if not self._close_state.is_set():
            self._close_state.set()


    @property
    def closed(self):
        return self._close_state.is_set()


    async def wait_closed(self):
        'wait until pool is closed'
        await asyncio.shield(self._close_waiter, loop=self._loop)


    async def acquire(self):
        '''Pretend to aquire a connection.

        In fact, always return the same MockRedis object once free'''
        async with self._cond:
            while True:
                await self._fill_free(override_min=True)
                if self.freesize:
                    conn = self._pool.popleft()
                    self._used.add(conn)
                    return conn
                else:
                    await self._cond.wait()


    def release(self, conn):
        '''Release our single MockRedis connection'''
        assert conn in self._used, "Invalid connection, maybe from other pool?"
        self._used.remove(conn)
        self._pool.append(conn)
        asyncio.ensure_future(self._wakeup(), loop=self._loop)


    async def _fill_free(self, *, override_min):
        while self.size < self.minsize:
            self._acquiring += 1
            try:
                conn = await self._create_new_connection()
                self._pool.append(conn)
            finally:
                self._acquiring -= 1
        if self.freesize:
            return
        if override_min:
            while not self._pool and self.size < self.maxsize:
                self._acquiring += 1
                try:
                    conn = await self._create_new_connection()
                    self._pool.append(conn)
                finally:
                    self._acquiring -= 1


    def _create_new_connection(self):
        return create_redis(self._address,
                            db=self._db,
                            password=self._password,
                            ssl=self._ssl,
                            encoding=self._encoding,
                            commands_factory=self._factory,
                            loop=self._loop)


    async def _wakeup(self):
        async with self._cond:
            self._cond.notify()


    def get(self):
        '''Return async context manager for working with the connection

        async with pool.get() as conn:
            await conn.get(key)
        '''
        return _AsyncConnectionContextManager(self)


class _AsyncConnectionContextManager:

    __slots__ = ('_pool', '_conn')

    def __init__(self, pool):
        self._pool = pool
        self._conn = None

    async def __aenter__(self):
        self._conn = await self._pool.acquire()
        return self._conn

    async def __aexit__(self, exc_type, exc_value, tb):
        try:
            self._pool.release(self._conn)
        finally:
            self._pool = None
            self._conn = None


