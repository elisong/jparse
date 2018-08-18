===================================================
jparse - A JSON-like Object Parsing Tool for Python
===================================================

.. image:: https://github.com/elisong/jparse/blob/master/jparse.png
        :target: https://github.com/elisong/jparse

-----

.. image:: https://travis-ci.org/elisong/jparse.svg?branch=master
        :alt: Build Status
        :target: https://travis-ci.org/elisong/jparse

.. image:: https://img.shields.io/badge/pypi-v0.1.8-blue.svg
        :alt: PyPI
        :target: https://github.com/elisong/jparse

.. image:: https://img.shields.io/badge/python-2.7%2C3.4%2C3.5%2C3.6-blue.svg
        :alt: PyPI - Python Version
        :target: https://github.com/elisong/jparse


.. image:: https://codecov.io/github/elisong/jparse/coverage.svg?branch=master
        :alt: Coverage Status
        :target: https://codecov.io/github/elisong/jparse

This tool is created to make retrieving data from http ``response.json()`` or json library ``json.loads()`` easy.
It helps to ``flatten``, ``filter``, ``select``, ``update``, and ``sort`` such objects, finally ``to_df`` (pandas.DataFrame format).

Simple Case
-----------

.. code-block:: python

    >>> from jparse import JParser
    >>> jp = JParser()
    >>> TEST_CASE1 = [{'A1': 1, 'A2': 2, 'A3': 3},
                      {'A1': [4, 5, 6], 'A2': 7, 'A3': 'x'}]
    >>> print(jp.flatten(TEST_CASE1))
    defaultdict(None, {'0_A1': 1,
                       '0_A2': 2,
                       '0_A3': 3,
                       '1_A1_0': 4,
                       '1_A1_1': 5,
                       '1_A1_2': 6,
                       '1_A2': 7,
                       '1_A3': 'x'})

Dependencies
------------

- `Pandas`_

.. _Pandas: https://pandas.pydata.org/

Installation
------------

.. code-block:: sh

    pip install jparse

or

.. code-block:: sh

    pip install git+https://github.com/elisong/jparse.git#egg=jparse

Document
--------

`Document here`_

.. _Document here: http://jparse.readthedocs.io/en/latest/

Changelog
---------

v0.1.8 - 2018-08-18
^^^^^^^^^^^^^^^^^^^^

- **Change** ``JParser.to_df`` by adding sort before to DataFrame

v0.1.7 - 2018-08-18
^^^^^^^^^^^^^^^^^^^^

- **Remove** ``collections.dafaultdict`` from japrse.py

v0.1.6 - 2018-08-18
^^^^^^^^^^^^^^^^^^^^

- **Change** ``pd.DataFrame()`` to ``pd.DataFrame.from_records()`` for ``JParser.to_df()``
- **Change** assert_frame_equal import for tests/test_to_df.py

v0.1.5 - 2018-08-18
^^^^^^^^^^^^^^^^^^^

- **Changed** remove JParser.to_df() reset_index()

v0.1.4 - 2018-08-15
^^^^^^^^^^^^^^^^^^^

- **Changed** license.

v0.1.3 - 2018-08-13
^^^^^^^^^^^^^^^^^^^

- **Added** project.
