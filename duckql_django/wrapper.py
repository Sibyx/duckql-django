import copy
import json
from typing import Dict, List

from django.db import connection
from duckql import Query, Count, Constant


class QueryWrapper:
    def __init__(self, query: str):
        self._query = Query.parse_raw(query)

    @classmethod
    def from_dict(cls, payload: Dict):
        # So dirty, so nasty, so sad
        return QueryWrapper(json.dumps(payload))

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
