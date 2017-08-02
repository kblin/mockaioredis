unit:
	py.test -v

coverage:
	py.test --cov=mockaioredis --cov-report=html --cov-report=term-missing

dist:
	pandoc -f markdown_github -t rst -o README.rst README.md
	python setup.py sdist bdist_wheel
	rm -f README.rst
