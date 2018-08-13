# -*- coding: utf-8 -*-
# @Author: Eli Song
# @Date:   2018-08-13 00:13:14
# @Last Modified by:   Eli Song
# @Last Modified time: 2018-08-13 00:15:46

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


def test_update_default():
    result1 = jp.update(TEST_CASE1, ['A1'], 10086)
    result2 = jp.update(TEST_CASE2, ['A1'], 10086)
    assert result1 == [{'A1': 10086, 'A2': 2, 'A3': 3},
                       {'A1': [10086, 10086, 10086], 'A2': 7, 'A3': 'x'}]
    assert result2 == {'A1': [10086, 10086],
                       'A2': {'C1': [8, 9], 'C2': [10, 11]},
                       'A3': {'A4': 10, 'A1': 10086}}


def test_update_with_has_subkeys():
    result3 = jp.update(TEST_CASE1, ['A1'], 10086, has_subkeys=['B1'])
    result4 = jp.update(TEST_CASE2, ['A1'], 10086, has_subkeys=['B1'])
    assert result3 == [{'A1': 1, 'A2': 2, 'A3': 3},
                       {'A1': [4, 5, 6], 'A2': 7, 'A3': 'x'}]
    assert result4 == {'A1': [10086, 10086],
                       'A2': {'C1': [8, 9], 'C2': [10, 11]},
                       'A3': {'A4': 10, 'A1': {'B4': 12}}}


def test_update_with_gross():
    result5 = jp.update(TEST_CASE1, ['A1'], 10086, gross=True)
    result6 = jp.update(TEST_CASE2, ['A1'], 10086, gross=True)
    assert result5 == [{'A1': 10086, 'A2': 2, 'A3': 3},
                       {'A1': 10086, 'A2': 7, 'A3': 'x'}]
    assert result6 == {'A1': 10086,
                       'A2': {'C1': [8, 9], 'C2': [10, 11]},
                       'A3': {'A4': 10, 'A1': 10086}}
