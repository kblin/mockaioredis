Mock library to replace aioredis during unit tests
==================================================

mockaioredis is to `aioredis <https://github.com/aio-libs/aioredis>`__
what the `mockredispy <https://github.com/locationlabs/mockredis>`__
library is to plain
`redis-py <https://github.com/andymccurdy/redis-py>`__. It uses the
mockredispy library and wraps it in the asyncio magic required to work
like aioredis.

Uses the new ``async`` keyword for Python 3.5, so no 3.4 support.

**Beware**: This is an early alpha that isn't even close to
API-complete. In fact, so far it only supports the limited set of calls
I needed for another project. Eventually, as I use more and more
aioredis calls in my other projects, this mock layer will be fleshed out
more.

Installation
------------

For now, I suggest cloning the git repository and ``pip install``\ ing
from there. Eventually, as mockaioredis becomes more feature complete,
I'll push it to PyPI as well.

License
-------

Like mockredispy, mockaioredis is licensed under the Apache License,
Version 2.0. See ```LICENSE`` <LICENSE>`__ for details.
