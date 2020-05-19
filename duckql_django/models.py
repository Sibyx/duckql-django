from typing import List, Union, Dict, Callable


class BaseReportConfig(object):
    is_reportable: bool = False
    fields: List[str] = []
    exclude: List[str] = [
        'deleted_at',
        'created_at',
        'updated_at'
    ]
    permission: Union[str, None] = None
    field_permissions: Dict[str, Union[str, Callable]] = {}


__all__ = [
    'BaseReportConfig'
]
