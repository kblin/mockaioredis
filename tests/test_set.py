from itertools import combinations_with_replacement

import pytest
from aioredis.errors import ReplyError


@pytest.mark.asyncio
async def test_sadd(redis):
    ret = await redis.sadd("foo", "bar")
    assert ret == 1
    assert redis._redis.smembers("foo") == {b"bar"}


@pytest.mark.asyncio
async def test_sadd_many(redis):
    ret = await redis.sadd("foo", "bar", "baz")
    assert ret == 2
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_scard(redis):
    redis._redis.sadd("foo", "bar")
    assert await redis.scard("foo") == 1

    redis._redis.sadd("foo", "bar", "baz")
    assert await redis.scard("foo") == 2


@pytest.mark.asyncio
async def test_sdiff(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "no bar", "baz", "bazzo")

    assert await redis.sdiff("foo_1", "foo_2") == [b"bar"]
    assert set(await redis.sdiff("foo_2", "foo_1")) == {b"bazzo", b"no bar"}


@pytest.mark.asyncio
async def test_sdiffstore(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "no bar", "baz", "bazzo")

    assert await redis.sdiffstore("foo_3", "foo_1", "foo_2") == 1
    assert redis._redis.smembers("foo_3") == {b"bar"}

    assert await redis.sdiffstore("foo_1", "foo_1", "foo_2") == 1
    assert redis._redis.smembers("foo_1") == {b"bar"}


@pytest.mark.asyncio
async def test_sinter(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "no bar", "baz", "bazzo")

    assert await redis.sinter("foo_1", "foo_2") == [b"baz"]


@pytest.mark.asyncio
async def test_sinterstore(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "no bar", "baz", "bazzo")

    assert await redis.sinterstore("foo_3", "foo_1", "foo_2") == 1
    assert redis._redis.smembers("foo_3") == {b"baz"}

    assert await redis.sinterstore("foo_1", "foo_1", "foo_2") == 1
    assert redis._redis.smembers("foo_1") == {b"baz"}


@pytest.mark.asyncio
async def test_sismember(redis):
    redis._redis.sadd("foo", "bar", "baz")

    assert await redis.sismember("foo", "bar") is 1
    assert await redis.sismember("foo", "barbar") is 0


@pytest.mark.asyncio
async def test_smembers(redis):
    redis._redis.sadd("foo", "bar", "baz")
    members = await redis.smembers("foo")
    assert sorted(members) == [b"bar", b"baz"]

    members = await redis.smembers("foo", encoding="utf8")
    assert sorted(members) == ["bar", "baz"]


@pytest.mark.asyncio
async def test_smove(redis):
    redis._redis.sadd("foo_1", "bar")
    redis._redis.sadd("foo_2", "baz")

    assert await redis.smove("foo_1", "foo_2", "bar") is 1

    assert redis._redis.smembers("foo_1") == set()
    assert redis._redis.smembers("foo_2") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_smove_bad_member(redis):
    redis._redis.sadd("foo_1", "bar")
    redis._redis.sadd("foo_2", "baz")

    assert await redis.smove("foo_2", "foo_1", "barbar") is 0

    assert redis._redis.smembers("foo_1") == {b"bar"}
    assert redis._redis.smembers("foo_2") == {b"baz"}


@pytest.mark.asyncio
async def test_smove_bad_key(redis):
    redis._redis.sadd("foo_1", "bar")
    redis._redis.sadd("foo_2", "baz")

    assert await redis.smove("foo_3", "foo_1", "baz") is 0

    assert redis._redis.smembers("foo_1") == {b"bar"}
    assert redis._redis.smembers("foo_2") == {b"baz"}


@pytest.mark.asyncio
async def test_smove_new_key(redis):
    redis._redis.sadd("foo_1", "bar")

    assert await redis.smove("foo_1", "foo_2", "bar") is 1

    assert redis._redis.smembers("foo_1") == set()
    assert redis._redis.smembers("foo_2") == {b"bar"}


@pytest.mark.asyncio
async def test_smove_bad_type(redis):
    redis._redis.set("foo_1", "1")
    redis._redis.sadd("foo_2", "bar")

    with pytest.raises(ReplyError):
        assert await redis.smove("foo_1", "foo_2", "1")

    with pytest.raises(ReplyError):
        assert await redis.smove("foo_2", "foo_1", "bar")

    assert redis._redis.get("foo_1") == b"1"
    assert redis._redis.smembers("foo_2") == {b"bar"}


@pytest.mark.asyncio
async def test_spop_single(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.spop("foo", 1))[0] in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") in ({b"bar"}, {b"baz"})

    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.spop("foo", 1, encoding="utf8"))[0] in ["bar", "baz"]
    assert redis._redis.smembers("foo") in ({b"bar"}, {b"baz"})


@pytest.mark.asyncio
async def test_spop_zero_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.spop("foo", 0)) == []
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_spop_negative_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    with pytest.raises(ReplyError):
        await redis.spop("foo", -1)
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_spop_null_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.spop("foo", None)) in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") in ({b"bar"}, {b"baz"})


@pytest.mark.asyncio
async def test_spop_default_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.spop("foo")) in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") in ({b"bar"}, {b"baz"})


@pytest.mark.asyncio
async def test_spop_all_items(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert sorted(await redis.spop("foo", 2)) == [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == set()


@pytest.mark.asyncio
async def test_spop_too_many_items(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert sorted(await redis.spop("foo", 3)) == [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == set()


@pytest.mark.asyncio
async def test_srandmember_single(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.srandmember("foo", 1))[0] in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_zero_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.srandmember("foo", 0)) == []
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_two_items_allow_dup(redis):
    for i in range(20):
        redis._redis.sadd("foo", "bar", "baz")
        ret = await redis.srandmember("foo", -2)
        assert isinstance(ret, list)
        assert tuple(sorted(ret)) in list(
            combinations_with_replacement([b"bar", b"baz"], 2)
        )
        assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_too_many_items_allow_dup(redis):
    for i in range(20):
        redis._redis.sadd("foo", "bar", "baz")
        ret = await redis.srandmember("foo", -3)
        assert isinstance(ret, list)
        assert tuple(sorted(ret)) in list(
            combinations_with_replacement([b"bar", b"baz"], 3)
        )
        assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_null_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.srandmember("foo", None)) in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_default_count(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert (await redis.srandmember("foo")) in [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_all_items_unique(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert sorted(await redis.srandmember("foo", 2)) == [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_too_many_items_unique(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert sorted(await redis.srandmember("foo", 3)) == [b"bar", b"baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_one_item_encoding(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert await redis.srandmember("foo", encoding="utf8") in ["bar", "baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srandmember_two_items_encoding(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert sorted(await redis.srandmember("foo", 2, encoding="utf8")) == ["bar", "baz"]
    assert redis._redis.smembers("foo") == {b"bar", b"baz"}


@pytest.mark.asyncio
async def test_srem(redis):
    redis._redis.sadd("foo", "bar", "baz")
    assert await redis.srem("foo", "bar") is 1

    redis._redis.sadd("foo", "bar", "baz")
    assert await redis.srem("foo", "bar", "baz") is 2

    redis._redis.sadd("foo", "bar", "baz")
    assert await redis.srem("foo", "bar", "baz", "bazzo") is 2


@pytest.mark.asyncio
async def test_sunion(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "baz", "bazzo")

    assert sorted(await redis.sunion("foo_1", "foo_2")) == [b"bar", b"baz", b"bazzo"]

    assert sorted(await redis.sunion("foo_1", "foo_3")) == [b"bar", b"baz"]

    assert redis._redis.smembers("foo_1") == {b"bar", b"baz"}
    assert redis._redis.smembers("foo_2") == {b"baz", b"bazzo"}


@pytest.mark.asyncio
async def test_sunionstore(redis):
    redis._redis.sadd("foo_1", "bar", "baz")
    redis._redis.sadd("foo_2", "baz", "bazzo")

    assert await redis.sunionstore("foo_3", "foo_1", "foo_2") == 3

    assert redis._redis.smembers("foo_1") == {b"bar", b"baz"}
    assert redis._redis.smembers("foo_2") == {b"baz", b"bazzo"}
    assert redis._redis.smembers("foo_3") == {b"bar", b"baz", b"bazzo"}


@pytest.mark.asyncio
async def test_sscan(redis):
    values = ["bar", "baz", "bazzo", "barbar"]
    b_values = [b"bar", b"barbar", b"baz", b"bazzo"]
    redis._redis.sadd("foo_1", *values)

    async def sscan(key, *args, **kwargs):
        # Return order is inconsistent between redis and fake redis
        resp = await redis.sscan(key, *args, **kwargs)
        return resp[0], sorted(resp[1])

    assert await sscan("foo_1") == (0, b_values)
    assert await sscan("foo_1", 0, count=10) == (0, b_values)
    assert await sscan("foo_1", match="bar") == (0, b_values[:1])
    assert await sscan("foo_1", match="bar*") == (0, b_values[:2])

    resp = await sscan("foo_1", 10)
    assert isinstance(resp[0], int)
    assert isinstance(resp[1], list)  # Elements returned are undefined

    resp = await sscan("foo_1", -10)
    assert isinstance(resp[0], int)
    assert isinstance(resp[1], list)  # Elements returned are undefined


@pytest.mark.asyncio
async def test_isscan(redis):
    values = ["bar", "baz", "bazzo", "barbar"]
    b_values = {b"bar", b"barbar", b"baz", b"bazzo"}
    redis._redis.sadd("foo_1", *values)

    values = {val async for val in redis.isscan("foo_1")}
    assert values == b_values

    values = {val async for val in redis.isscan("foo_1", count=5)}
    assert values == b_values

    values = {val async for val in redis.isscan("foo_1", match="bar")}
    assert values == {b"bar"}
    values = {val async for val in redis.isscan("foo_1", match="bar*")}
    assert values == {b"bar", b"barbar"}
