import pytest


@pytest.mark.asyncio
async def test_lindex(redis):
    ret = await redis.lindex('foo', 0)
    assert ret is None

    redis._redis.lpush('foo', 'bar', 'baz', 'blub')

    first = await redis.lindex('foo', 0)
    assert b'blub' == first
    last = await redis.lindex('foo', -1, encoding='utf-8')
    assert 'bar' == last


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


@pytest.mark.asyncio
async def test_lrange(redis):
    redis._redis.lpush('foo', 'bar', 'baz', 'blub', 'blargh')
    ret = await redis.lrange('foo', 0, -1)
    assert len(ret) == 4
    assert ret[0] == b'blargh'
    assert ret[-1] == b'bar'

    ret = await redis.lrange('foo', 0, -1, encoding='utf-8')
    assert len(ret) == 4
    assert ret[0] == 'blargh'
    assert ret[-1] == 'bar'

    with pytest.raises(TypeError):
        await redis.lrange('foo', 'bob', -1)
    with pytest.raises(TypeError):
        await redis.lrange('foo', 0, 'bob')


@pytest.mark.asyncio
async def test_rpoplpush(redis):
    redis._redis.lpush('foo', 'baz', 'blub', 'blargh')
    ret = await redis.rpoplpush('foo', 'bar')
    assert ret == b'baz'
    assert await redis.llen('foo') == 2
    assert await redis.llen('bar') == 1

    ret = await redis.rpoplpush('foo', 'bar', encoding='utf-8')
    assert ret == 'blub'
    assert await redis.llen('foo') == 1
    assert await redis.llen('bar') == 2


@pytest.mark.asyncio
async def test_lpush(redis):
    ret = await redis.rpush('foo', 'bar', 'blub', 'blargh')

    await redis.lset('foo', 1, 'baz')

    assert 3 == redis._redis.llen('foo')
    assert [b'bar', b'baz', b'blargh'] == redis._redis.lrange('foo', 0, -1)
