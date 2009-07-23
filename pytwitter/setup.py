#!/usr/bin/python

from distutils.core import setup

classifiers="""\
Development Status :: 4 - Beta
Environment :: Console
License :: OSI Approved :: Python Software Foundation License
Intended Audience :: Developers
Operating System :: OS Independent
Programming Language :: Python
Topic :: Communications
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries"""

setup(name='pytwitter',
    description='python library for the twitter api',
    author='Niall Sheridan',
    author_email='nsheridan@gmail.com',
    url='http://code.google.com/p/pytwitter',
    license='Apache License 2.0',
    long_description='python library for the twitter api',
    platforms='Any',
    version='0.4',
    package_dir={'pytwitter': ''},
    packages=['pytwitter'],
    classifiers=classifiers.split('\n')
    )
