# -*- coding: utf-8 -*-
# @Author: Eli Song
# @Date:   2018-08-13 00:09:20
# @Last Modified by:   Eli Song
# @Last Modified time: 2018-08-13 00:12:26

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


def test_select_with_sel_keys():
    result1 = [s for s in jp.select(TEST_CASE1, ['A1'])]
    result2 = [s for s in jp.select(TEST_CASE2, ['A1'])]
    assert jp.sort(result1) == [1, [4, 5, 6]]
    assert jp.sort(result2) == [[OrderedDict([('B1', 4), ('B2', 5)]),
                                 OrderedDict([('B1', 6), ('B3', 7)])],
                                OrderedDict([('B4', 12)])]


def test_select_with_has_subkeys():
    result1 = [s for s in jp.select(TEST_CASE1, ['A1'], has_subkeys=['B1'])]
    result2 = [s for s in jp.select(TEST_CASE2, ['A1'], has_subkeys=['B1'])]
    assert result1 == []
    assert jp.sort(result2) == [[OrderedDict([('B1', 4), ('B2', 5)]),
                                 OrderedDict([('B1', 6), ('B3', 7)])]]


def test_select_with_drop_subkeys():
    result1 = [s for s in jp.select(TEST_CASE1, ['A1'], drop_subkeys=['B1'])]
    result2 = [s for s in jp.select(TEST_CASE2, ['A1'], drop_subkeys=['B1'])]
    assert result1 == []
    assert result2 == [[OrderedDict([('B2', 5)]), OrderedDict([('B3', 7)])],
                       OrderedDict([('B4', 12)])]


def test_select_with_gross():
    result1 = [s for s in jp.select(TEST_CASE1, ['A1'], gross=True)]
    result2 = [s for s in jp.select(TEST_CASE2, ['A1'], gross=True)]
    assert result1 == [1, [4, 5, 6]]
    assert result2 == [[OrderedDict([('B1', 4), ('B2', 5)]),
                        OrderedDict([('B1', 6), ('B3', 7)])],
                       OrderedDict([('B4', 12)])]
