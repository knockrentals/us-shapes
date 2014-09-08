#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='usshapes',
      version='0.1',
      description='U.S. Shapefile Indexer for Elasticsearch',
      author='Daniel Sarfati',
      author_email='daniel@knockrentals.com',
      url='https://github.com/fatisar/us-shapes',
      packages=find_packages(),
      requires=['pyes', 'beautifulsoup4']
)