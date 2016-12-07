unit:
	py.test -v

coverage:
	py.test --cov=mockaioredis --cov-report=html --cov-report=term-missing
