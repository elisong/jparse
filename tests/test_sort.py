# -*- coding: utf-8 -*-
from collections import OrderedDict
from jparse import JParser

jp = JParser()
TEST_CASE1 = [OrderedDict([('A1', 1), ('A2', 2), ('A3', 3)]),
              OrderedDict([('A1', [4, 5, 6]), ('A2', 7), ('A3', 'x')])]
TEST_CASE2 = OrderedDict([('A1', [OrderedDict([('B1', 4), ('B2', 5)]),
                                  OrderedDict([('B1', 6), ('B3', 7)])]),
                          ('A2', OrderedDict([('C1', [8, 9]), ('C2', [10, 11])])),
                          ('A3', OrderedDict([('A1', OrderedDict([('B4', 12)])),
                                              ('A4', 10)]))])


def test_sort_with_sort_by_key():
    result1 = jp.sort(TEST_CASE1, sort_by='key')
    result2 = jp.sort(TEST_CASE2, sort_by='key')
    expected1 = TEST_CASE1
    expected2 = TEST_CASE2
    assert result1 == expected1
    assert result2 == expected2


def test_sort_with_sort_by_value():
    result3 = jp.sort(TEST_CASE1, sort_by='value')
    result4 = jp.sort(TEST_CASE2, sort_by='value')
    expected3 = [OrderedDict([('A1', 1), ('A2', 2), ('A3', 3)]),
                 OrderedDict([('A2', 7), ('A1', [4, 5, 6]), ('A3', 'x')])]
    expected4 = OrderedDict([('A3',
                              OrderedDict([('A4', 10),
                                           ('A1', OrderedDict([('B4', 12)]))
                                           ])),
                             ('A2',
                              OrderedDict([('C2', [10, 11]),
                                           ('C1', [8, 9])])),
                             ('A1',
                              [OrderedDict([('B1', 4), ('B2', 5)]),
                               OrderedDict([('B1', 6), ('B3', 7)])])])
    assert result3 == expected3
    assert result4 == expected4


def test_sort_with_reverse():
    result5 = jp.sort(TEST_CASE1, reverse=True)
    result6 = jp.sort(TEST_CASE2, reverse=True)
    expected5 = [OrderedDict([('A3', 3), ('A2', 2), ('A1', 1)]),
                 OrderedDict([('A3', 'x'), ('A2', 7), ('A1', [4, 5, 6])])]
    expected6 = OrderedDict([('A3',
                              OrderedDict([('A4', 10),
                                           ('A1', OrderedDict([('B4', 12)]))
                                           ])),
                             ('A2', OrderedDict([('C2', [10, 11]),
                                                 ('C1', [8, 9])])),
                             ('A1', [OrderedDict([('B2', 5), ('B1', 4)]),
                                     OrderedDict([('B3', 7), ('B1', 6)])])])

    assert result5 == expected5
    assert result6 == expected6
