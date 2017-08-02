from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

install_requires = [
    'mockredispy-kblin'
]

tests_require = [
    'coverage',
    'pytest',
    'pytest-asyncio',
    'pytest-cov',
]

classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Operating System :: POSIX',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


def read_version():
    import re
    import os.path
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'mockaioredis', '__init__.py')
    with open(init_py, 'r') as fh:
        for line in fh:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Unable to find version in ' + init_py)


def read(filename):
    with open(filename, 'r') as fh:
        return fh.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='mockaioredis',
      version=read_version(),
      description="Mock implementation of aioredis",
      long_description=read('README.rst'),
      classifiers=classifiers,
      platforms=["POSIX"],
      author="Kai Blin",
      author_email="kblin@biosustain.dtu.dk",
      url="https://github.com/kblin/mockaioredis",
      license="Apache Software License",
      packages=find_packages(exclude=["tests"]),
      install_requires=install_requires,
      tests_require=tests_require,
      cmdclass={'test': PyTest},
      include_package_data=True,
      extras_require={
        'testing': tests_require,
      },
)
