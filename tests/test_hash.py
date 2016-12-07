import pytest

from mockaioredis import MockRedis


@pytest.fixture
def redis():
    return MockRedis()


@pytest.mark.asyncio
async def test_hset(redis):
    await redis.hset('foo', 'bar', 'baz')
    assert redis._redis.hget('foo', 'bar') == b'baz'


@pytest.mark.asyncio
async def test_hget(redis):
    redis._redis.hset('foo', 'bar', 'baz')
    val = await redis.hget('foo', 'bar')
    assert val == b'baz'

    val = await redis.hget('foo', 'bar', encoding='utf-8')
    assert val == 'baz'


@pytest.mark.asyncio
async def test_hmset_dict(redis):
    await redis.hmset_dict('foo', {'foo': 'bar', 'baz': 'blargh'})
    assert redis._redis.hmget('foo', ['foo', 'baz']) == [b'bar', b'blargh']


@pytest.mark.asyncio
async def test_hmset(redis):
    await redis.hmset('foo', 'foo', 'bar', 'baz', 'blargh')
    assert redis._redis.hmget('foo', ['foo', 'baz']) == [b'bar', b'blargh']

    with pytest.raises(TypeError):
        await redis.hmset('foo', 'foo', 'bar', 'baz')


@pytest.mark.asyncio
async def test_hmget(redis):
    redis._redis.hmset('foo', {'foo': 'bar', 'baz': 'blargh'})
    val = await redis.hmget('foo', 'foo', 'baz', 'blubb')
    assert val == [b'bar', b'blargh', None]

    val = await redis.hmget('foo', 'foo', 'baz', 'blubb', encoding='utf-8')
    assert val == ['bar', 'blargh', None]


@pytest.mark.asyncio
async def test_hgetall(redis):
    expected  = {'foo': 'bar', 'baz': 'blargh'}
    redis._redis.hmset('foo', expected)

    val = await redis.hgetall('foo', encoding='utf-8')
    assert val == expected

    expected_raw = {}
    for k,v in expected.items():
        k = k.encode('utf-8')
        expected_raw[k] = v.encode('utf-8')

    val = await redis.hgetall('foo')
    assert val == expected_raw
