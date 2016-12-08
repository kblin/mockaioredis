import pytest


@pytest.mark.asyncio
async def test_llen(redis):
    length = await redis.llen('foo')
    assert 0 == length

    redis._redis.lpush('foo', 'bar')
    length = await redis.llen('foo')
    assert 1 == length


@pytest.mark.asyncio
async def test_lpush(redis):
    ret = await redis.lpush('foo', 'bar')
    assert 1 == ret
    ret = await redis.lpush('foo', 'baz')
    assert 2 == ret
    ret = await redis.lpush('foo', 'blub', 'blargh')
    assert 4 == ret

    assert 4 == redis._redis.llen('foo')
    assert [b'blargh', b'blub', b'baz', b'bar'] == redis._redis.lrange('foo', 0, -1)


@pytest.mark.asyncio
async def test_lpop(redis):
    redis._redis.lpush('foo', 'bar', 'baz', 'blub', 'blargh')
    ret = await redis.lpop('foo')
    assert b'blargh' == ret

    ret = await redis.lpop('foo', encoding='utf-8')
    assert 'blub' == ret


@pytest.mark.asyncio
async def test_rpush(redis):
    ret = await redis.rpush('foo', 'bar')
    assert 1 == ret
    ret = await redis.rpush('foo', 'baz')
    assert 2 == ret
    ret = await redis.rpush('foo', 'blub', 'blargh')
    assert 4 == ret

    assert 4 == redis._redis.llen('foo')
    assert [b'bar', b'baz', b'blub', b'blargh'] == redis._redis.lrange('foo', 0, -1)


@pytest.mark.asyncio
async def test_rpop(redis):
    redis._redis.lpush('foo', 'bar', 'baz', 'blub', 'blargh')
    ret = await redis.rpop('foo')
    assert b'bar' == ret

    ret = await redis.rpop('foo', encoding='utf-8')
    assert 'baz' == ret
