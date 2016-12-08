import pytest

from mockaioredis import MockRedis

@pytest.fixture
def redis():
    return MockRedis()
