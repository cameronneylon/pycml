#!/usr/bin/env python

from setuptools import setup, find_packages
from pycml.version import VERSION

setup(name='pycml',
      version=VERSION,
      description='Python Library to support writing Chemical Markup Language documents',
      author='Cameron Neylon',
      author_email='pypi@cameroneylon.net',
      url='https://github.com/cameronneylon/pycml',
      packages=find_packages(),
      install_requires = [
          'numpy'
          ],
      test_suite='test'
     )
