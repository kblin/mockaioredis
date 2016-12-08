import pytest
import mockaioredis


@pytest.mark.asyncio
async def test_create_pool():
    pool = await mockaioredis.create_pool(
        ('localhost', 6379),
        encoding='utf-8',
        minsize=5, maxsize=10)
    async with pool.get() as redis:
        await redis.hset('foo', 'bar', 'baz')
        val = await redis.hget('foo', 'bar')
    assert val == 'baz'
    pool.close()
    await pool.wait_closed()


@pytest.mark.asyncio
async def test_properties():
    pool = await mockaioredis.create_pool(
        ('localhost', 6379),
        encoding='utf-8',
        minsize=5, maxsize=10)

    # We fake the maxsize
    assert pool.maxsize == 1

    assert pool.closed  == False

    pool.close()
    await pool.wait_closed()

    assert pool.closed
