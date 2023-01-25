#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

dependencies = ["requests>=2.22.0", "beautifulsoup4>=4.4.0"]


setup(
    name="news_scrapers",
    version="0.0.1",
    description="Get link (URL) preview",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="imvladikon",
    license="",
    install_requires=dependencies,
    keywords="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),
)
