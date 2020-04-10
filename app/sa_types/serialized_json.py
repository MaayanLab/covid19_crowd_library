import json
import logging
import sqlalchemy as sa
from sqlalchemy import types
from sqlalchemy.sql import operators


class ImmutableSerializedJSON(types.TypeDecorator):
    impl = sa.Text()

    def coerce_compared_value(self, op, value):
        if op in (operators.like_op, operators.notlike_op):
            # Allow "like" operator on string
            return sa.String()
        else:
            return self

    def process_bind_param(self, value, dialect):
        # Example: {'blah': 'bleh'} -> '{"blah": "bleh"}'
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        # Example: '{"blah": "bleh"}' -> {'blah': 'bleh'}
        if value is not None:
            if value == '':
                value = None
            else:
                value = json.loads(value)
                if type(value) == str:
                    logging.warn('You stored a string in a json field... maybe its actually json')
                    try:
                        value = json.loads(value)
                    except:
                        pass
        return value
