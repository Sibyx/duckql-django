import copy
import json
from typing import Dict, List, Type

from django.db import connection
from duckql import Query, Count, Constant

from . import Schema


class QueryWrapper:
    def __init__(self, query: str, base_model: Type, user=None):
        self._query = Query.parse_raw(query)
        self._schema = Schema(base_model, user)

    @classmethod
    def from_dict(cls, payload: Dict, base_model: Type, user=None):
        # So dirty, so nasty, so sad
        return QueryWrapper(json.dumps(payload), base_model, user)

    @staticmethod
    def _execute_query(query: Query) -> List[Dict]:
        with connection.cursor() as cursor:
            cursor.execute(str(query))
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute(self) -> List[Dict]:
        return self._execute_query(self._query)

    def estimated_total(self) -> int:
        subquery = copy.deepcopy(self._query)
        subquery.limit = None
        subquery.alias = '__s'
        query = Query(
            entity=subquery,
            properties=[
                Count(
                    property=Constant(value='*')
                ),
            ],
        )

        return self._execute_query(query)[0].get('count')


__all__ = [
    'QueryWrapper'
]
