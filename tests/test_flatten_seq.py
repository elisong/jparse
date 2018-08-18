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


def test_flatten_seq_default():
    result1 = jp.flatten_seq(TEST_CASE1)
    expected1 = {'0': {'A1': 1, 'A2': 2, 'A3': 3},
                 '1': {'A1': [4, 5, 6],
                       'A2': 7,
                       'A3': 'x'}}
    assert result1 == expected1


def test_flatten_seq_with_prefix():
    result1 = jp.flatten_seq(TEST_CASE1, prefix='F')
    expected1 = {'F_0': {'A1': 1, 'A2': 2, 'A3': 3},
                 'F_1': {'A1': [4, 5, 6],
                         'A2': 7,
                         'A3': 'x'}}
    assert result1 == expected1


def test_flatten_seq_raise():
    with pytest.raises(ValueError):
        jp.flatten_seq(TEST_CASE2)
