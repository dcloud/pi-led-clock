"""
Pi LED Clock: Display the time on a Unicorn HAT HD
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

from piledclock import __version__, __author__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="piledclock",
    version=__version__,
    author=__author__,
    description="Pi LED Clock: Display the time on a Unicorn HAT HD",
    long_description=long_description,
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["unicornhathd"],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["piledclock=piledclock.cli:main"]},
)
