import json
import sqlalchemy as sa
from sqlalchemy import types
from sqlalchemy.sql import operators
from sqlalchemy.ext.mutable import MutableDict


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
            value = json.loads(value)
        return value

MutableSerializedJSON = MutableDict.as_mutable(ImmutableSerializedJSON)
