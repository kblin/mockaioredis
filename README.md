Mock library to replace aioredis during unit tests
==================================================

mockaioredis is to [aioredis] what the [mockredispy] library is to plain [redis-py].
It uses the mockredispy library and wraps it in the asyncio magic required to work like
aioredis.

**Beware**: This is an early alpha that isn't even close to API-complete.
In fact, so far it only supports the limited set of calls I needed for another project.
Eventually, as I use more and more aioredis calls in my other projects, this mock layer
will be fleshed out more.


Installation
------------

For now, I suggest cloning the git repository and `pip install`ing from there.
Eventually, as mockaioredis becomes more feature complete, I'll push it to PyPI as well.


License
-------
Like mockredispy, mockaioredis is licensed under the Apache License, Version 2.0.
See [`LICENSE`](LICENSE) for details.

[aioredis]: https://github.com/aio-libs/aioredis
[mockresispy]: https://github.com/locationlabs/mockredis
[redis-py]: https://github.com/andymccurdy/redis-py
