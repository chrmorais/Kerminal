#!/usr/bin/env python3
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys


def long_description():
    readme = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme, 'r') as inf:
        readme_text = inf.read()
    return(readme_text)

setup(name='Kerminal',
      version='0.0.1',
      description='Kerbal Space Program in the Terminal, via Telemachus',
      long_description=long_description(),
      author='Paul Barton',
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/Kerminal',
      #package_dir = {'': '.'},
      #packages = [],
      license='http://www.gnu.org/licenses/gpl-3.0.html',
      keywords='npyscreen, telemetry, websocket,',
)