# Modified from https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/scalar_list.html

import sqlalchemy as sa
from sqlalchemy import types

class SimpleSplitter:
    def __init__(self, separator):
        self.separator = separator
    
    def split(self, s):
        return s.split(self.separator)

class ScalarListType(types.TypeDecorator):
    impl = sa.Text()

    def __init__(self, coerce_func=str, separator=r',', splitter=None):
        self.coerce_func = coerce_func
        self.separator = separator
        self.splitter = splitter if splitter is not None else SimpleSplitter(self.separator)

    def process_bind_param(self, value, dialect):
        # Example: [1, 2, 3, 4] -> '1, 2, 3, 4'
        if value is not None:
            return self.separator.join(value)

    def process_result_value(self, value, dialect):
        # Example: '1, 2, 3, 4' -> [1, 2, 3, 4]
        if value is not None:
            if value == u'':
                return []
            return list(map(
                self.coerce_func, self.splitter.split(str(value))
            ))
