.. jparse documentation master file, created by
   sphinx-quickstart on Mon Aug 13 11:16:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Why Create ?
====================

Firstly, *Json-like Object* here, simply speaking, are dicts, or list of dicts. For example:

.. code-block:: python

    TEST_CASE1 = [{'A1': 1, 'A2': 2, 'A3': 3},
                  {'A1': [4, 5, 6], 'A2': 7, 'A3': 'x'}]


.. code-block:: python

    TEST_CASE2 = {'A1': [{'B1': 4, 'B2': 5},
                         {'B1': 6, 'B3': 7}],
                  'A2': {'C1': [8, 9],
                         'C2': [10, 11]},
                  'A3': {'A1': {'B4': 12},
                        {'A4': 10}}


They are ``collections.MutableMapping`` or ``collections.MutableSequence`` objects.
It is hard to retrieve data from those sufficiently complex one(e.g., json response
from maps web service Api).

::

    {
        "status": 0,
        "type": 2,
        "result": {
            "origin": {
                "city_id": 131,
                "city_name": "北京市",
                "location": {
                    "lng": 116.3081418168,
                    "lat": 40.056871561538
                }
            },
            "destination": {
                "city_id": 289,
                "city_name": "上海市",
                "location": {
                    "lng": 121.50581834502,
                    "lat": 31.222960154925
                }
            },
            "total": 49,
            "routes": [
                {
                    "distance": 51837,
                    "duration": 22544,
                    "arrive_time": "2018-08-14 23:18:00",
                    "price": 553,
                    "price_detail": [],
                    "steps": [
                        [
                            {
                                "distance": 708,
                                "duration": 603,
                                "instructions": "步行708米",
    ...

We usually meet these tasks or more,

- Task1: simplify these nested of nested (loop N times) object.

.. code-block:: python

    # flatten TEST_CASE1
    {'0_A1': 1,
     '0_A2': 2,
     '0_A3': 3,
     '1_A1_0': 4,
     '1_A1_1': 5,
     '1_A1_2': 6,
     '1_A2': 7,
     '1_A3': 'x'}

- Task2: filter by keys thoroughly with other conditions.

.. code-block:: python

    # drop "A1" from TEST_CASE1
    [{'A2': 2, 'A3': 3}, {'A2': 7, 'A3': 'x'}]


- Taks3: extract every nodes which has subkey requirement.

.. code-block:: python

    # select "A1" from TEST_CASE2
    [[{'B1': 4, 'B2': 5}, {'B1': 6, 'B3': 7}], {'B4': 12}]
    # select "A1" which has subkey "B1" from TEST_CASE2
    [{'B1': 4, 'B2': 5}, {'B1': 6, 'B3': 7}]

- Task4: replace some value without replacement.

.. code-block:: python

    # update "A1" with 10086 from TEST_CASE1
    [{'A1': 10086, 'A2': 2, 'A3': 3},
     {'A1': 10086, 'A2': 7, 'A3': 'x'}]
    # or update each sub-element
    [{'A1': 10086, 'A2': 2, 'A3': 3},
     {'A1': [10086, 10086, 10086], 'A2': 7, 'A3': 'x'}]

- Task5: sort whole object to make look pretty.

.. code-block:: python

    # sort by value thoroughly from TEST_CASE1 descending
    [{'A3': 3, 'A2': 2, 'A1': 1},
     {'A3': 'x', 'A2': 7, 'A1': [4, 5, 6]}]

- Task6: convert to pandas as it is so popular for data scientist.

.. code-block:: python

    # convert TEST_CASE1 to DataFrame
              A1  A2 A3
    0          1   2  3
    1  [4, 5, 6]   7  x
