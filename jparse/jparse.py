# -*- coding: utf-8 -*-
#
# Copyright 2018 Eli Song <elisong.ah@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

from collections import defaultdict, OrderedDict
from collections import MutableMapping, MutableSequence
import pandas as pd
import copy


class JParser(object):
    def __init__(self):
        pass

    def flatten(self, item, prefix=''):
        """Flatten JSON-like object thoroughly.
        The key of item's value adds prefix from its ancestors.

        :param item: JSON-like object to be flattened
        :type item: MutableMapping or MutableSequence

        :param prefix: initial prefix
        :type prefix: string, default: ''

        :rtype: defaultdict
        """
        result = defaultdict()
        prefix_sep = prefix + '_' if prefix else ''
        if isinstance(item, MutableMapping):
            result.update({prefix_sep + k2: v2 for k, v in item.items()
                           for k2, v2 in self.flatten(v, k).items()})
        elif isinstance(item, MutableSequence):
            result.update({prefix_sep + k2: v2 for i, v in enumerate(item)
                           for k2, v2 in self.flatten(v, str(i)).items()})
        else:
            result[prefix] = item
        return result

    def flatten_map(self, item, prefix=''):
        """Flatten MutableMapping object until encounter MutableSequence.
        The key of item's value adds prefix from its ancestors.

        :param item: JSON-like object to be flattened
        :type item: MutableMapping

        :param prefix: initial prefix
        :type prefix: string, default: ''

        :rtype: defaultdict
        """
        if not isinstance(item, MutableMapping):
            raise ValueError('Must be MutableMapping item!')
        else:
            result = defaultdict()
            for k, v in item.items():
                new_key = prefix + '_' + k if prefix else k
                if isinstance(v, MutableMapping):
                    result.update(self.flatten_map(v, new_key))
                else:
                    result[new_key] = v
            return result

    def flatten_seq(self, item, prefix=''):
        """Flatten MutableSequence object until encounter MutableMapping.
        The key of item's value adds prefix from its ancestors.

        :param item: JSON-like object to be flattened
        :type item: MutableSequence

        :param prefix: initial prefix
        :type prefix: string, default: ''

        :rtype: defaultdict
        """
        if not isinstance(item, MutableSequence):
            raise ValueError('Must be MutableSequence item!')
        else:
            result = defaultdict()
            for i, v in enumerate(item):
                new_key = prefix + '_' + str(i) if prefix else str(i)
                if isinstance(v, MutableSequence):
                    result.update(self.flatten_seq(v, new_key))
                else:
                    result[new_key] = v
        return result

    def filter(self, item, keys=[], how='select'):
        """Filter JSON-like object by `keys` and `how`.

        :param item: JSON-like object to be filtered
        :type item: MutableMapping, MutableSequence

        :param keys: keys for filtering
        :type keys: list, default: []

        :param how: type of filter: {'select', 'drop'}
        :type how: string, default: 'select'

        :rtype: MutableMapping, or MutableSequence
        """
        if isinstance(item, MutableMapping):
            if keys == []:
                result = item
            elif how == 'drop':
                result = {k: v for k, v in item.items() if k not in keys}
            else:
                result = {k: v for k, v in item.items() if k in keys}
        elif isinstance(item, MutableSequence):
            result = [self.filter(i, keys, how) for i in item]
        else:
            result = item if not keys else None
        return result

    def select(self, item, sel_keys, has_subkeys=[], drop_subkeys=[],
               gross=False):
        """Select `sel_keys` values which have `has_subkeys`.
        Drop `drop_subkeys` from the above.

        :param item: JSON-like object to be selected
        :type item: MutableMapping, MutableSequence

        :param sel_keys: keys for selection
        :type sel_keys: list

        :param has_subkeys: keys for checking sub-element
        :type has_subkeys: list, default: []

        :param drop_subkeys: keys need to be dropped
        :type drop_subkeys: list, default: []

        :param gross: (when `sel_keys`'s value is MutableSequence)
                      Any next-subelement has `has_subkeys` leads to select
                      the whole if `gross=True`.
                      Otherwise, select next-subelement which has `has_subkeys`
                      one by one
        :type gross: bool, default: False

        :rtype: generator
        """
        if isinstance(item, MutableMapping):
            for k, v in item.items():
                if k in sel_keys:
                    filtered = self.filter(v, has_subkeys)
                    dropped = self.filter(v, drop_subkeys, 'drop')
                    if isinstance(v, MutableSequence):
                        selected = [d for i, d in enumerate(dropped)
                                    if filtered[i] and d]
                        if gross and selected:
                            yield dropped
                        elif not gross and selected:
                            yield selected
                    elif isinstance(v, MutableMapping):
                        if filtered:
                            yield dropped
                    else:
                        if not any([has_subkeys, drop_subkeys]):
                            yield v
                else:
                    for s in self.select(v, sel_keys, has_subkeys,
                                         drop_subkeys):
                        yield s
        elif isinstance(item, MutableSequence):
            for i in item:
                for s in self.select(i, sel_keys, has_subkeys,
                                     drop_subkeys):
                    yield s
        else:
            pass

    def update(self, item, sel_keys, value, has_subkeys=[],
               gross=False):
        """Update JSON-like object thoroughly without inplacement.

        :param item: JSON-like object to be updated
        :type item: MutableMapping, MutableSequence

        :param sel_keys: keys for selection
        :type sel_keys: list

        :param value: value for update
        :type value: python object

        :param has_subkeys: keys for checking sub-element
        :type has_subkeys: list, default: []

        :param gross: (when `sel_keys`'s value is MutableSequence)
                      Any next-subelement has `has_subkeys` leads to update
                      the whole with `value` if `gross=True`.
                      Otherwise, update next-subelement which has `has_subkeys`
                      one by one.
        :type gross: bool, default: False

        :rtype: MutableMapping, or MutableSequence
        """
        item_ = copy.deepcopy(item)
        if isinstance(item_, MutableMapping):
            for k, v in item_.items():
                if k in sel_keys:
                    filtered = self.filter(v, has_subkeys)
                    if isinstance(v, MutableSequence):
                        if gross:
                            new = value if any(filtered) else v
                        else:
                            new = [value if filtered[i] else v2
                                   for i, v2 in enumerate(v)]
                        item_.update({k: new})
                    else:
                        item_.update({k: value if filtered else v})
                else:
                    item_.update({k: self.update(v, sel_keys, value,
                                                 has_subkeys, gross)})
        elif isinstance(item_, MutableSequence):
            return [self.update(i, sel_keys, value, has_subkeys, gross)
                    for i in item_]
        else:
            pass
        return item_

    def sort(self, item, sort_by='key', reverse=False):
        """Sort JSON-like object thoroughly without inplacement.

        :param item: JSON-like object to be updated
        :type item: MutableMapping, MutableSequence

        :param sort_by: sort type: {'key', 'value'}
        :type sort_by: str

        :param reverse: sort ascending if `reverse=False`,
                        otherwise, descending
        :type reverse: bool, default: False

        :rtype: OrderedDict, list of OrderedDict
        """
        if isinstance(item, MutableMapping):
            if sort_by == 'key':
                result = OrderedDict(sorted(item.items(),
                                            key=lambda x: str(x[0]),
                                            reverse=reverse))
            elif sort_by == 'value':
                result = OrderedDict(sorted(item.items(),
                                            key=lambda x: str(x[1]),
                                            reverse=reverse))
            else:
                raise ValueError('sort_key choose from: {"key", "value"}')
            for k, v in item.items():
                result[k] = self.sort(v, sort_by, reverse)
        elif isinstance(item, MutableSequence):
            result = [self.sort(i, sort_by, reverse)
                      for i in item]
        else:
            result = item
        return result

    def to_df(self, item, prefix='', flatten=True):
        """Convert JSON-like object to pandas.DataFrame.

        :param item: JSON-like object to be converted
        :type item: MutableMapping, MutableSequence

        :param prefix: initial prefix
        :type prefix: string, default: ''

        :param flatten: Flatten item thoroughly if `flatten=True`.
                        Otherwise, flatten item according to its
                        instance type.
        :type flatten: bool, default: True

        :rtype: pandas.DataFrame
        """
        if flatten:
            records = [self.flatten(item, prefix)]
        else:
            if isinstance(item, MutableMapping):
                records = [self.flatten_map(item)]
            elif isinstance(item, MutableSequence):
                flated = self.flatten_seq(item)
                records = [self.flatten_map(v) for v in flated.values()]
        result = pd.DataFrame(self.sort(records))
        return result.reset_index(drop=True)


if __name__ == '__main__':
    import pytest

    jp = JParser()
    TEST_CASE1 = [OrderedDict([('A1', 1), ('A2', 2), ('A3', 3)]),
                  OrderedDict([('A1', [4, 5, 6]), ('A2', 7), ('A3', 'x')])]
    TEST_CASE2 = OrderedDict([('A1', [OrderedDict([('B1', 4), ('B2', 5)]),
                                      OrderedDict([('B1', 6), ('B3', 7)])]),
                              ('A2', OrderedDict([('C1', [8, 9]), ('C2', [10, 11])])),
                              ('A3', OrderedDict([('A1', OrderedDict([('B4', 12)])),
                                                  ('A4', 10)]))])
    print(jp.flatten(TEST_CASE1))
    print(jp.flatten(TEST_CASE2))
    print(jp.flatten(TEST_CASE1, prefix='F'))
    print(jp.flatten(TEST_CASE2, prefix='F'))
    print(jp.flatten_map(TEST_CASE2))
    print(jp.flatten_map(TEST_CASE2, prefix='F'))
    with pytest.raises(ValueError):
        jp.flatten_map(TEST_CASE1)
    print(jp.flatten_seq(TEST_CASE1))
    print(jp.flatten_seq(TEST_CASE1, prefix='F'))
    with pytest.raises(ValueError):
        jp.flatten_seq(TEST_CASE2)
    print(jp.filter('A'))
    print(jp.filter('A', ['A1']) is None)
    print(jp.filter(TEST_CASE1))
    print(jp.filter(TEST_CASE2))
    print(jp.filter(TEST_CASE1, ['A1']))
    print(jp.filter(TEST_CASE2, ['A1']))
    print(jp.filter(TEST_CASE1, ['A1'], 'drop'))
    print(jp.filter(TEST_CASE2, ['A1'], 'drop'))
    print([s for s in jp.select(TEST_CASE1, ['A1'])])
    print([s for s in jp.select(TEST_CASE2, ['A1'])])
    print(jp.sort([s for s in jp.select(TEST_CASE1, ['A1'],
                                        has_subkeys=['B1'])]))
    print(jp.sort([s for s in jp.select(TEST_CASE2, ['A1'],
                                        has_subkeys=['B1'])]))
    print(jp.sort([s for s in jp.select(TEST_CASE1, ['A1'],
                                        drop_subkeys=['B1'])]))
    print(jp.sort([s for s in jp.select(TEST_CASE2, ['A1'],
                                        drop_subkeys=['B1'])]))
    print(jp.sort([s for s in jp.select(TEST_CASE1, ['A1'], gross=True)]))
    print(jp.sort([s for s in jp.select(TEST_CASE2, ['A1'], gross=True)]))
    print(jp.update(TEST_CASE1, ['A1'], 10086))
    print(jp.update(TEST_CASE2, ['A1'], 10086))
    print(jp.update(TEST_CASE1, ['A1'], 10086, has_subkeys=['B1']))
    print(jp.update(TEST_CASE2, ['A1'], 10086, has_subkeys=['B1']))
    print(jp.update(TEST_CASE1, ['A1'], 10086, gross=True))
    print(jp.update(TEST_CASE2, ['A1'], 10086, gross=True))
    print(jp.sort(TEST_CASE1, sort_by='key'))
    print(jp.sort(TEST_CASE2, sort_by='key'))
    print(jp.sort(TEST_CASE1, sort_by='value'))
    print(jp.sort(TEST_CASE2, sort_by='value'))
    print(jp.sort(TEST_CASE1, reverse=True))
    print(jp.sort(TEST_CASE2, reverse=True))
    print(jp.to_df(TEST_CASE1))
    print(jp.to_df(TEST_CASE2))
    print(jp.to_df(TEST_CASE1, prefix='F'))
    print(jp.to_df(TEST_CASE2, prefix='F'))
    print(jp.to_df(TEST_CASE1, flatten=False))
    print(jp.to_df(TEST_CASE2, flatten=False))
