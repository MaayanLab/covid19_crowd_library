# Modified from https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/scalar_list.html

import sqlalchemy as sa
from sqlalchemy import types


class ScalarListException(Exception):
    pass

class SimpleSplitter:
    def __init__(self, separator):
        self.separator = separator
    
    def split(self, s):
        return s.split(self.separator)

class ScalarListType(types.TypeDecorator):
    impl = sa.UnicodeText()

    def __init__(self, coerce_func=str, separator=r',', splitter=None):
        self.coerce_func = coerce_func
        self.separator = separator
        self.splitter = splitter if splitter is not None else SimpleSplitter(self.separator)

    def process_bind_param(self, value, dialect):
        # Convert list of values to unicode separator-separated list
        # Example: [1, 2, 3, 4] -> u'1, 2, 3, 4'
        if value is not None:
            return self.separator.join(
              self.splitter.split(map(self.coerce_func, str(value)))
            )

    def process_result_value(self, value, dialect):
        if value is not None:
            if value == u'':
                return []
            # coerce each value
            return list(map(
                self.coerce_func, self.splitter.split(str(value))
            ))
