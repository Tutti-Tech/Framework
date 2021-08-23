#!/usr/bin/env python
# coding: utf-8

import os
import re
import pathlib
from setuptools import setup, find_packages

# Get parent path
PATH = pathlib.Path(__file__).parent

# Get long_description in README file
README = (PATH / "README.md").read_text()

# Get __version__ in __init__.py
def get_version(package):
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

#
setup(
    name='tutti-framework',
    version=get_version('framework'),
    description='A web framework',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/TuttiData/framework',
    author='Cheng Zhang',
    author_email="zhangchengx@gmail.com",
    python_requires='>=3.6',
    license="GPL",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['starlette'],
    entry_points={
        "console_scripts": [
            "framework=framework.__main__:main",
        ]
    },
)