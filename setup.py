# -*- coding: utf-8 -*-
from setuptools import setup
import os
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as fr:
    readme = fr.read()

with open(os.path.join(here, 'VERSION')) as fv:
    version = fv.read().strip()

setup(
    name='jparse',
    version=version,
    description='A JSON-like object parsing tool for python',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/elisong/jparse',
    author='Eli Song',
    author_email='elisong.ah@gmail.com',
    keywords='python json parser',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    packages=['jparse'],
    python_requires='>=2.7',
    setup_requires=['pandas'],
    install_requires=['pandas'],
    test_suite='tests'
)
