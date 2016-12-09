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
