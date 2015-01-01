"""Credit to mahmoudimus 
https://github.com/mahmoudimus/sqlalchemy-citext

Included here as sqlalchemy-citext didn't seem to play well with pip.
"""
from __future__ import unicode_literals

import sqlalchemy.types as types
from sqlalchemy.dialects.postgresql.base import ischema_names


class CIText(types.UserDefinedType):

    def get_col_spec(self):
        return 'CITEXT'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process


# Register CIText to SQLAlchemy's Postgres reflection subsystem.
ischema_names['citext'] = CIText