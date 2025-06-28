# Copyright (c) 2024 Jan T. Müller <mail@jantmueller.com>

import os
import sys

from setuptools import find_packages, setup

import swizzle

if sys.version_info < (3, 7):
    sys.exit("ERROR: swizzle requires Python 3.7+")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swizzle",
    version=swizzle.__version__,
    packages=find_packages(exclude=["tests"]),
    author="Jan T. Müller",
    author_email="mail@jantmueller.com",
    description="Swizzle enables the retrieval of multiple attributes, similar to swizzling in computer graphics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janthmueller/swizzle",
    project_urls={
        "Documentation": "https://github.com/janthmueller/swizzle/blob/main/README.md",
        "Source": "https://github.com/janthmueller/swizzle",
        "Tracker": "https://github.com/janthmueller/swizzle/issues",
    },
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
)


# python setup.py sdist bdist_wheel
# twine check dist/*
# twine upload dist/* -> insert token
