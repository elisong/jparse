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


def test_flatten_default():
    result1 = jp.flatten(TEST_CASE1)
    result2 = jp.flatten(TEST_CASE2)
    expected1 = {'0_A1': 1, '0_A2': 2, '0_A3': 3,
                 '1_A1_0': 4, '1_A1_1': 5, '1_A1_2': 6,
                 '1_A2': 7, '1_A3': 'x'}
    expected2 = {'A1_0_B1': 4, 'A1_0_B2': 5, 'A1_1_B1': 6,
                 'A1_1_B3': 7, 'A2_C1_0': 8, 'A2_C1_1': 9,
                 'A2_C2_0': 10, 'A2_C2_1': 11, 'A3_A4': 10,
                 'A3_A1_B4': 12}
    assert result1 == expected1
    assert result2 == expected2


def test_flatten_with_prefix():
    result1 = jp.flatten(TEST_CASE1, prefix='F')
    result2 = jp.flatten(TEST_CASE2, prefix='F')
    expected1 = {'F_0_A1': 1, 'F_0_A2': 2, 'F_0_A3': 3,
                 'F_1_A1_0': 4, 'F_1_A1_1': 5,
                 'F_1_A1_2': 6, 'F_1_A2': 7,
                 'F_1_A3': 'x'}
    expected2 = {'F_A1_0_B1': 4, 'F_A1_0_B2': 5,
                 'F_A1_1_B1': 6, 'F_A1_1_B3': 7,
                 'F_A2_C1_0': 8, 'F_A2_C1_1': 9,
                 'F_A2_C2_0': 10, 'F_A2_C2_1': 11,
                 'F_A3_A4': 10, 'F_A3_A1_B4': 12}

    assert result1 == expected1
    assert result2 == expected2
