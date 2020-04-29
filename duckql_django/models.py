from typing import List, Union


class BaseReportConfig:
    is_reportable: bool = False
    fields: List[str] = []
    exclude: List[str] = []
    permission: Union[str, None] = None


class ReportableModel:
    ReportConfig = BaseReportConfig()


__all__ = [
    'ReportableModel'
]
