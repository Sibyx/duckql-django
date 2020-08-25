from typing import List, Union, Dict, Callable


class BaseReportConfig(object):
    is_reportable: bool = False
    fields: List[str] = []
    exclude: List[str] = [
        'deleted_at',
        'created_at',
        'updated_at'
    ]
    permission: Union[str, None, Callable] = None
    field_permissions: Dict[str, Union[str, Callable]] = {}
    formatters: Dict[str, Callable] = {}
    metadata: Dict = {}


__all__ = [
    'BaseReportConfig'
]
