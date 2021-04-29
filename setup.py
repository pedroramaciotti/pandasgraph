"""`setup.py`"""
from setuptools import setup, find_packages

# Package requirements
with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


setup(name='pandasgraph',
      version='0.0.0',
      description='A pandas-based package for graph algorithms',
      author='Julio Laborde, Pedro Ramaciotti Morales',
      author_email='pedro.ramaciotti@gmail.com',
      url = 'https://github.com/pedroramaciotti/pandasgraph',
      download_url = 'https://github.com/pedroramaciotti/pandasgraph/archive/0.0.0.tar.gz',
      keywords = ['pandas','graph algorithms'],
      packages=find_packages(),
      license='OSI Approved :: MIT License',
      #classifiers=["License :: OSI Approved :: Apache License, Version 2.0 (Apache-2.0)"],
      data_files=[('', ['LICENSE'])],
      install_requires=INSTALL_REQUIRES)
