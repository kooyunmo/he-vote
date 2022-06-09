import os
from setuptools import setup, find_packages


def read(fname: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_version() -> str:
    return read("VERSION").strip()


def read_readme() -> str:
    return read("README.md")


COMMON_DEPS = [
    "requests>=2.26.0",
    "typer>=0.4.0",
    "rich>=12.2.0",
    "plotext>=5.0.2",
]

TEST_DEPS = [
    "coverage==5.5",
    "pytest==6.2.4",
    "pytest-asyncio==0.15.1",
    "pytest-cov==2.11.1",
    "pytest-benchmark==3.4.1",
    "pytest-lazy-fixture==0.6.3",
    "requests-mock>=1.9.3",
    "pyfiglet==0.8.post1",
]

setup(
    name='he-vote',
    version=read_version(),
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    description='HE-Vote CLI',
    author='Yunmo Koo, Taebum Kim',
    license="Apache License 2.0",
    url="https://github.com/kooyunmo/he-vote",
    packages=find_packages(include=['hevote', 'hevote.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
    ],
    entry_points={
        "console_scripts": [
            "hevote = hevote:app",
        ]
    },
    python_requires='>=3.10',
    include_package_data=True,
    install_requires=COMMON_DEPS,
    extras_require={
        "test": TEST_DEPS
    }
)
