# -*- coding: utf-8 -*-
import pytest
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


def test_flatten_map_default():
    result1 = jp.flatten_map(TEST_CASE2)
    expected1 = {'A1': [{'B1': 4, 'B2': 5},
                        {'B1': 6, 'B3': 7}],
                 'A2_C1': [8, 9], 'A2_C2': [10, 11],
                 'A3_A4': 10, 'A3_A1_B4': 12}
    assert result1 == expected1


def test_flatten_map_with_prefix():
    result1 = jp.flatten_map(TEST_CASE2, prefix='F')
    expected1 = {'F_A1': [{'B1': 4, 'B2': 5},
                          {'B1': 6, 'B3': 7}],
                 'F_A2_C1': [8, 9], 'F_A2_C2': [10, 11],
                 'F_A3_A4': 10, 'F_A3_A1_B4': 12}
    assert result1 == expected1


def test_flatten_map_raise():
    with pytest.raises(ValueError):
        jp.flatten_map(TEST_CASE1)
