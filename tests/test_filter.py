# -*- coding: utf-8 -*-
# @Author: Eli Song
# @Date:   2018-08-13 00:04:30
# @Last Modified by:   Eli Song
# @Last Modified time: 2018-08-13 00:08:04

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


def test_filter_default():
    assert jp.filter('A') == 'A'
    assert jp.filter(TEST_CASE1) == TEST_CASE1
    assert jp.filter(TEST_CASE2) == TEST_CASE2


def test_filter_with_key():
    assert jp.filter('A', ['A1']) is None
    result1 = jp.filter(TEST_CASE1, ['A1'])
    assert result1 == [{'A1': 1}, {'A1': [4, 5, 6]}]
    result2 = jp.filter(TEST_CASE2, ['A1'])
    assert result2 == {'A1': [{'B1': 4, 'B2': 5}, {'B1': 6, 'B3': 7}]}


def test_filter_with_how():
    result1 = jp.filter(TEST_CASE1, ['A1'], 'drop')
    assert result1 == [{'A2': 2, 'A3': 3}, {'A2': 7, 'A3': 'x'}]
    result2 = jp.filter(TEST_CASE2, ['A1'], 'drop')
    assert result2 == {'A2': {'C1': [8, 9], 'C2': [10, 11]},
                       'A3': {'A4': 10, 'A1': {'B4': 12}}}
