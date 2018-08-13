.. jparse documentation master file, created by
   sphinx-quickstart on Mon Aug 13 11:16:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


How to Use ?
====================

Installation
------------

.. code-block:: sh

    pip install jparse

or

.. code-block:: sh

    pip install git+https://github.com/elisong/jparse.git#egg=jparse

Show Cases
------------

Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> from jparse import JParser
    >>> jp = JParser()

    >>> TEST_CASE1 = [{'A1': 1, 'A2': 2, 'A3': 3},
                      {'A1': [4, 5, 6], 'A2': 7, 'A3': 'x'}]

    >>> TEST_CASE2 = {'A1': [{'B1': 4, 'B2': 5},
                             {'B1': 6, 'B3': 7}],
                      'A2': {'C1': [8, 9],
                             'C2': [10, 11]},
                      'A3': {'A1': {'B4': 12},
                            {'A4': 10}}

------

flatten - flatten thoroughly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default

.. code-block:: python

    >>> print(jp.flatten(TEST_CASE1))
    defaultdict(None, {'0_A1': 1,
                       '0_A2': 2,
                       '0_A3': 3,
                       '1_A1_0': 4,
                       '1_A1_1': 5,
                       '1_A1_2': 6,
                       '1_A2': 7,
                       '1_A3': 'x'})

    >>> print(jp.flatten(TEST_CASE2))
    defaultdict(None, {'A1_0_B1': 4,
                       'A1_0_B2': 5,
                       'A1_1_B1': 6,
                       'A1_1_B3': 7,
                       'A2_C1_0': 8,
                       'A2_C1_1': 9,
                       'A2_C2_0': 10,
                       'A2_C2_1': 11,
                       'A3_A1_B4': 12,
                       'A3_A4': 10})

- add prefix

.. code-block:: python

    >>> print(jp.flatten(TEST_CASE1, prefix='F'))
    defaultdict(None, {'F_0_A1': 1,
                       'F_0_A2': 2,
                       'F_0_A3': 3,
                       'F_1_A1_0': 4,
                       'F_1_A1_1': 5,
                       'F_1_A1_2': 6,
                       'F_1_A2': 7,
                       'F_1_A3': 'x'})

    >>> print(jp.flatten(TEST_CASE2, prefix='F'))
    defaultdict(None, {'F_A1_0_B1': 4,
                       'F_A1_0_B2': 5,
                       'F_A1_1_B1': 6,
                       'F_A1_1_B3': 7,
                       'F_A2_C1_0': 8,
                       'F_A2_C1_1': 9,
                       'F_A2_C2_0': 10,
                       'F_A2_C2_1': 11,
                       'F_A3_A4': 10,
                       'F_A3_A1_B4': 12})

------

flatten_seq - flatten until encounter MutableMapping object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default

.. code-block:: python

    >>> print(jp.flatten_seq(TEST_CASE1))
    defaultdict(None, {'0': {'A1': 1,
                             'A2': 2,
                             'A3': 3},
                       '1': {'A1': [4, 5, 6],
                             'A2': 7,
                             'A3': 'x'}})

    >>> import pytest
    >>> with pytest.raises(ValueError):
            jp.flatten_seq(TEST_CASE2)

- add prefix

.. code-block:: python

    >>> print(jp.flatten_seq(TEST_CASE1, prefix='F'))
    defaultdict(None, {'F_0': {'A1': 1,
                               'A2': 2,
                               'A3': 3},
                       'F_1': {'A1': [4, 5, 6],
                               'A2': 7,
                               'A3': 'x'}})

------

flatten_map - flatten until encounter MutableSequence object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default

.. code-block:: python

    >>> print(jp.flatten_map(TEST_CASE2))
    defaultdict(None, {'A1': [{'B1': 4, 'B2': 5},
                              {'B1': 6, 'B3': 7}],
                       'A2_C1': [8, 9],
                       'A2_C2': [10, 11],
                       'A3_A4': 10,
                       'A3_A1_B4': 12})

    >>> import pytest
    >>> with pytest.raises(ValueError):
            jp.flatten_map(TEST_CASE1)

- add prefix

.. code-block:: python

    >>> print(jp.flatten_map(TEST_CASE2, prefix='F'))
    defaultdict(None, {'F_A1': [{'B1': 4, 'B2': 5},
                                {'B1': 6, 'B3': 7}],
                       'F_A2_C1': [8, 9],
                       'F_A2_C2': [10, 11],
                       'F_A3_A4': 10,
                       'F_A3_A1_B4': 12})

------

filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default, ``how='select'``

.. code-block:: python

    >>> print(jp.filter('A', ['A1']))
    None

    >>> print(jp.filter(TEST_CASE1, ['A1']))
    [{'A1': 1}, {'A1': [4, 5, 6]}]

    >>> print(jp.filter(TEST_CASE2, ['A1']))
    {'A1': [{'B1': 4, 'B2': 5}, {'B1': 6, 'B3': 7}]}

- set ``how='drop'``

.. code-block:: python

    >>> print(jp.filter('A', ['A1'], 'drop'))
    None

    >>> print(jp.filter(TEST_CASE1, ['A1'], 'drop'))
    [{'A2': 2, 'A3': 3}, {'A2': 7, 'A3': 'x'}]

    >>> print(jp.filter(TEST_CASE2, ['A1'], 'drop'))
    {'A2': {'C1': [8, 9],
            'C2': [10, 11]},
     'A3': {'A4': 10,
            'A1': {'B4': 12}}}

------

select
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default

.. code-block:: python

    >>> print([s for s in jp.select('A', ['A1'])])
    []

    >>> print([s for s in jp.select(TEST_CASE1, ['A1'])])
    [1, [4, 5, 6]]

    >>> print([s for s in jp.select(TEST_CASE2, ['A1'])])
    [[{'B1': 4, 'B2': 5},
      {'B1': 6, 'B3': 7}],
     {'B4': 12}]

- add has_subkeys condition

.. code-block:: python

    >>> print([s for s in jp.select('A', ['A1'], has_subkeys=['B1'])])
    []

    >>> print([s for s in jp.select(TEST_CASE1, ['A1'], has_subkeys=['B1'])])
    []

    >>> print([s for s in jp.select(TEST_CASE2, ['A1'], has_subkeys=['B1'])])
    [[{'B1': 4, 'B2': 5},
      {'B1': 6, 'B3': 7}]]

- add drop_subkeys condition

.. code-block:: python

    >>> print([s for s in jp.select('A', ['A1'], drop_subkeys=['B1'])])
    []

    >>> print([s for s in jp.select(TEST_CASE1, ['A1'], drop_subkeys=['B1'])])
    []

    >>> print([s for s in jp.select(TEST_CASE2, ['A1'], drop_subkeys=['B1'])])
    [[{'B2': 5}, {'B3': 7}],
     {'B4': 12}]

- set ``gross=True``

(When ``sel_keys``'s value is MutableSequence)
Any next-subelement has ``has_subkeys`` leads to select
the whole if ``gross=True``.
Otherwise, select next-subelement which has ``has_subkeys``
one by one.

.. code-block:: python

    >>> print([s for s in jp.select('A', ['A1'], gross=True)])
    []

    >>> print([s for s in jp.select(TEST_CASE1, ['A1'], gross=True)])
    [1, [4, 5, 6]]

    >>> print([s for s in jp.select(TEST_CASE2, ['A1'], gross=True)])
    [[{'B1': 4, 'B2': 5},
      {'B1': 6, 'B3': 7}],
     {'B4': 12}]

------

update
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default, ``gross=False``

.. code-block:: python

    >>> print(jp.update(TEST_CASE1, ['A1'], 10086))
    [{'A1': 10086, 'A2': 2, 'A3': 3},
     {'A1': [10086, 10086, 10086], 'A2': 7, 'A3': 'x'}]

    >>> print(jp.update(TEST_CASE2, ['A1'], 10086))
    {'A1': [10086, 10086],
     'A2': {'C1': [8, 9], 'C2': [10, 11]},
     'A3': {'A4': 10, 'A1': 10086}}

- add has_subkeys condition

.. code-block:: python

    >>> print(jp.update(TEST_CASE1, ['A1'], 10086, has_subkeys=['B1']))
    [{'A1': 1, 'A2': 2, 'A3': 3},
     {'A1': [4, 5, 6], 'A2': 7, 'A3': 'x'}]

    >>> print(jp.update(TEST_CASE2, ['A1'], 10086, has_subkeys=['B1']))
    {'A1': [10086, 10086],
     'A2': {'C1': [8, 9], 'C2': [10, 11]},
     'A3': {'A4': 10, 'A1': {'B4': 12}}}

- set ``gross=True``

.. code-block:: python

    >>> print(jp.update(TEST_CASE1, ['A1'], 10086, gross=True))
    [{'A1': 10086, 'A2': 2, 'A3': 3},
     {'A1': 10086, 'A2': 7, 'A3': 'x'}]

    >>> print(jp.update(TEST_CASE2, ['A1'], 10086, gross=True))
    {'A1': 10086,
     'A2': {'C1': [8, 9], 'C2': [10, 11]},
     'A3': {'A4': 10, 'A1': 10086}}

------

sort
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default, ``sort_by='key'``, ``reverse=False``

.. code-block:: python

    >>> print(jp.sort(TEST_CASE1))
    [OrderedDict([('A1', 1), ('A2', 2), ('A3', 3)]),
     OrderedDict([('A1', [4, 5, 6]), ('A2', 7), ('A3', 'x')])]

    >>> print(jp.sort(TEST_CASE2))
    OrderedDict([('A1', [OrderedDict([('B1', 4), ('B2', 5)]),
                         OrderedDict([('B1', 6), ('B3', 7)])]),
                 ('A2', OrderedDict([('C1', [8, 9]), ('C2', [10, 11])])),
                 ('A3', OrderedDict([('A1', OrderedDict([('B4', 12)])),
                                     ('A4', 10)]))])

- set ``sort_by='value'``

.. code-block:: python

    >>> print(jp.sort(TEST_CASE1, sort_by='value'))
    [OrderedDict([('A1', 1), ('A2', 2), ('A3', 3)]),
     OrderedDict([('A2', 7), ('A1', [4, 5, 6]), ('A3', 'x')])]

    >>> print(jp.sort(TEST_CASE2, sort_by='value'))
    OrderedDict([('A3', OrderedDict([('A4', 10),
                                     ('A1', OrderedDict([('B4', 12)]))])),
                 ('A2', OrderedDict([('C2', [10, 11]),
                                     ('C1', [8, 9])])),
                 ('A1', [OrderedDict([('B1', 4), ('B2', 5)]),
                         OrderedDict([('B1', 6), ('B3', 7)])])])

- set ``reverse=True``

.. code-block:: python

    >>> print(jp.sort(TEST_CASE1, reverse=True))
    [OrderedDict([('A3', 3), ('A2', 2), ('A1', 1)]),
     OrderedDict([('A3', 'x'), ('A2', 7), ('A1', [4, 5, 6])])]

    >>> print(jp.sort(TEST_CASE2, reverse=True))
    OrderedDict([('A3', OrderedDict([('A4', 10),
                                     ('A1', OrderedDict([('B4', 12)]))])),
                 ('A2', OrderedDict([('C2', [10, 11]),
                                     ('C1', [8, 9])])),
                 ('A1', [OrderedDict([('B2', 5), ('B1', 4)]),
                         OrderedDict([('B3', 7), ('B1', 6)])])])

------

to_df
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- default, ``flatten=True``

.. code-block:: python

    >>> print(jp.to_df(TEST_CASE1))
       0_A1  0_A2  0_A3  1_A1_0  1_A1_1  1_A1_2  1_A2 1_A3
    0     1     2     3       4       5       6     7    x

    >>> print(jp.to_df(TEST_CASE2))
       A1_0_B1  A1_0_B2  A1_1_B1  A1_1_B3  ...    A2_C2_0  A2_C2_1  A3_A1_B4  A3_A4
    0        4        5        6        7  ...         10       11        12     10

- set ``flatten=False``

.. code-block:: python

    >>> print(jp.to_df(TEST_CASE1, flatten=False))
              A1  A2 A3
    0          1   2  3
    1  [4, 5, 6]   7  x

    >>> print(jp.to_df(TEST_CASE2, flatten=False))
                                             A1   A2_C1  ...   A3_A1_B4  A3_A4
    0  [{'B1': 4, 'B2': 5}, {'B1': 6, 'B3': 7}]  [8, 9]  ...         12     10
