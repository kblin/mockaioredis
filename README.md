Retired
=======

This project is now retired. Please see [fakeredis-py](https://github.com/cunla/fakeredis-py) if you need to mock redis
for testing. `fakeredis-py` supports both async and sync API calls and is actively developed.


Mock library to replace aioredis during unit tests
==================================================

mockaioredis is to [aioredis] what the [mockredispy] library is to plain [redis-py].
It uses the mockredispy library and wraps it in the asyncio magic required to work like
aioredis.

Uses the new `async` keyword for Python 3.5, so no 3.4 support.

**Beware**: This is an early alpha that isn't even close to API-complete.
In fact, so far it only supports the limited set of calls I needed for another project.
Eventually, as I use more and more aioredis calls in my other projects, this mock layer
will be fleshed out more.


Installation
------------

You can install `mockaioredis` from PYPI by running `pip install mockaioredis`.

If you want to update an existing install, run `pip install --update mockaioredis`.

You can also clone this repository from github and run `pip install .` from the repository base directory.


Usage
-----

You can use it as a fixture using pytest-mock

```python
import mockaioredis

@pytest.fixture(autouse=True)
def redis(mocker):
    """Mock Redis."""
    mocker.patch.object(aioredis, 'create_pool', new=mockaioredis.create_pool)
```


License
-------
Like mockredispy, mockaioredis is licensed under the Apache License, Version 2.0.
See [`LICENSE`](LICENSE) for details.

[aioredis]: https://github.com/aio-libs/aioredis
[mockredispy]: https://github.com/locationlabs/mockredis
[redis-py]: https://github.com/andymccurdy/redis-py
