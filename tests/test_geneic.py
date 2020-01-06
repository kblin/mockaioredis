import pytest


@pytest.mark.asyncio
async def test_exists(redis):
    redis._redis.set('foo', 'bar')
    redis._redis.set('baz', 'blub')

    val = await redis.exists('blargh')
    assert 0 == val

    val = await redis.exists('foo')
    assert 1 == val

    val = await redis.exists('foo', 'baz')
    assert 2 == val

    val = await redis.exists('foo', 'baz', 'foo')
    assert 3 == val

    val = await redis.exists('foo', 'baz', 'blargh')
    assert 2 == val


@pytest.mark.asyncio
async def test_expire(redis):
    redis._redis.set('foo', 'bar')
    await redis.expire('foo', 30)
    assert redis._redis.ttl('foo') <= 30

    with pytest.raises(TypeError):
        # the sync version supports timedeltas, so people might get this wrong
        from datetime import timedelta
        await redis.expire('foo', timedelta(seconds=30))


@pytest.mark.asyncio
async def test_delete(redis):
    redis._redis.set('foo', 'bar')
    redis._redis.set('baz', 'blub')
    redis._redis.set('blargh', 'blurgh')

    val = await redis.delete('foo')
    assert 1 == val
    assert False == redis._redis.exists('foo')

    val = await redis.delete('foo', 'baz', 'blargh')
    assert 2 == val
    assert False == redis._redis.exists('baz')
    assert False == redis._redis.exists('blargh')


@pytest.mark.asyncio
async def test_get(redis):
    redis._redis.set('foo', 'bar')
    val = await redis.get('foo')
    assert val == b'bar'

    val = await redis.get('foo', encoding='utf-8')
    assert val == 'bar'


@pytest.mark.asyncio
async def test_incr(redis):
    redis._redis.set('foo', '1')
    val = await redis.incr('foo')
    assert val == 2

    val = await redis.incr('bar')
    assert val == 1

    val = await redis.incrby('bar', 20)
    assert val == 21


@pytest.mark.asyncio
async def test_keys(redis):
    redis._redis.set('foo', 'bar')
    redis._redis.set('baz', 'blub')
    redis._redis.set('blargh', 'blurgh')

    ret = await redis.keys('b*')
    assert len(ret) == 2
    # order is random, so sort to make this reliable
    ret.sort()
    assert ret[0] == b'baz'
    assert ret[1] == b'blargh'

    ret = await redis.keys('gnarf*')
    assert len(ret) == 0

    ret = await redis.keys('f*', encoding='utf=8')
    assert len(ret) == 1
    assert ret[0] == 'foo'


@pytest.mark.asyncio
async def test_set(redis):
    await redis.set('foo', 'bar')
    assert redis._redis.get('foo') == b'bar'


@pytest.mark.asyncio
async def test_dbsize(redis):
    dbsize = await redis.dbsize()
    assert dbsize == 0
    await redis.set('foo', 'bar')
    assert await redis.dbsize() == 1
    await redis.delete('foo', 'bar')
    assert await redis.dbsize() == 0


@pytest.mark.asyncio
async def test_ttl(redis):
    redis._redis.setex('foo', 30, 'bar')
    ret = await redis.ttl('foo')
    assert ret <= 30


@pytest.mark.asyncio
async def test_pipeline(redis):
    pipe = redis.pipeline()
    pipe.set('foo', 'bar')
    pipe.get('foo')
    ret = await pipe.execute()
    assert [True, b'bar'] == ret


@pytest.mark.asyncio
@pytest.mark.parametrize('match, cursor, count, expected_cursor, expected_keys', [
    ('b*', 0, None, 0, [b'baz', b'blargh']),
    ('gnarf*', b'0', None, 0, []),
    ('f*', 0, None, 0, [b'foo']),
    ('*', 0, 2, 2, [b'baz', b'blargh']),
    ('*', 2, 2, 0, [b'foo'])
])
async def test_scan(redis, match, cursor, count, expected_cursor, expected_keys):
    redis._redis.set('foo', 'bar')
    redis._redis.set('baz', 'blurb')
    redis._redis.set('blargh', 'blurgh')

    cursor, keys = await redis.scan(match=match, cursor=cursor, count=count)
    assert cursor == expected_cursor
    assert len(keys) == len(expected_keys)
    assert keys == expected_keys
