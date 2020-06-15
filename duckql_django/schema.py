from typing import Tuple, Dict, List, Type

from django.db.models import UUIDField, CharField, TextField, BigIntegerField, PositiveIntegerField, DecimalField, \
    IntegerField, DateTimeField, DateField, ForeignKey
from django_enum_choices.fields import EnumChoiceField
from duckql import Query

from duckql_django import BaseReportConfig


class Schema:
    _aggregations = {
        UUIDField: {
            'available': [
                'functions.Concat',
                'functions.Count',
            ],
            'default': 'functions.Count'
        },
        CharField: {
            'available': [
                'functions.Concat',
                'functions.Count',
                'functions.StringAgg'
            ],
            'default': 'functions.StringAgg'
        },
        TextField: {
            'available': [
                'functions.Concat',
                'functions.Count',
                'functions.StringAgg'
            ],
            'default': 'functions.StringAgg'
        },
        BigIntegerField: {
            'available': [
                'functions.Avg',
                'functions.Count',
                'functions.Max',
                'functions.Min',
                'functions.Sum',
            ],
            'default': 'functions.Avg'
        },
        PositiveIntegerField: {
            'available': [
                'functions.Avg',
                'functions.Count',
                'functions.Max',
                'functions.Min',
                'functions.Sum',
            ],
            'default': 'functions.Avg'
        },
        DecimalField: {
            'available': [
                'functions.Avg',
                'functions.Count',
                'functions.Max',
                'functions.Min',
                'functions.Sum',
            ],
            'default': 'functions.Avg'
        },
        IntegerField: {
            'available': [
                'functions.Avg',
                'functions.Count',
                'functions.Max',
                'functions.Min',
                'functions.Sum',
            ],
            'default': 'functions.Avg'
        },
        DateTimeField: {
            'available': [
                'functions.ConvertTimezones',
                'functions.DateAdd',
                'functions.DateSub',
                'functions.DateFormat',
                'functions.Extract',
                'functions.Weekday',
                'functions.Count'
            ],
            'default': 'functions.Max'
        },
        DateField: {
            'available': [
                'functions.ConvertTimezones',
                'functions.DateAdd',
                'functions.DateSub',
                'functions.DateFormat',
                'functions.Extract',
                'functions.Weekday',
                'functions.Count'
            ],
            'default': 'functions.Count'
        }
    }

    def __init__(self, base_model: Type, user=None):
        self._mapping: Dict = {}
        self._types: List[str] = []
        self._base_model = base_model
        self._user = user

        self.recreate()

    def _check_permissions_for_field(self, field: str, conf: BaseReportConfig) -> bool:
        """
        Default permission checker for fields
        TODO: move this callable to Django settings
        :param field:
        :param conf:
        :return:
        """

        if not self._user:
            return True

        if field not in conf.field_permissions.keys():
            return True

        # TODO: support for callable in field permissions

        return self._user.has_perm(conf.field_permissions[field])

    def _create_mapping(self) -> Tuple[Dict, List[str]]:
        mapping = {}
        types = []

        for model in self._base_model.__subclasses__():
            if hasattr(model, 'ReportConfig'):
                conf: BaseReportConfig = getattr(model, 'ReportConfig')

                if not conf.is_reportable:
                    continue

                # TODO: create handle for custom permission checker
                if self._user and conf.permission and not self._user.has_perm(conf.permission):
                    continue

                model_meta = getattr(model, '_meta')
                entity = {
                    'fields': [],
                    'relations': [],
                    'title': model_meta.verbose_name_plural
                }

                for field in model_meta.fields:
                    if not conf.fields or field.attname in model_meta.fields:

                        # TODO: create handle for custom permission checker
                        if not self._check_permissions_for_field(field, conf):
                            continue

                        field_definition = {
                            'attribute': field.attname,
                            'type': field.__class__.__name__,
                            'title': field.verbose_name
                        }

                        if field.__class__.__name__ not in types:
                            types.append(field.__class__.__name__)

                        if type(field) in self._aggregations:
                            field_definition['aggregations'] = self._aggregations[type(field)]

                        if isinstance(field, EnumChoiceField):
                            field_definition['values'] = {item.value: str(item) for item in field.enum_class}

                        if isinstance(field, ForeignKey):
                            entity['relations'].append({
                                'local': field.column,
                                'foreign': field.target_field.column,
                                'entity': field.related_model._meta.db_table
                            })

                        if field.attname not in conf.exclude:
                            entity['fields'].append(field_definition)

                for field in model_meta.related_objects:
                    if hasattr(field.remote_field, 'ReportConfig') and field.remote_field.ReportConfig.is_reportable:
                        definition = {
                            'local': field.field_name,
                            'foreign': field.remote_field.column,
                            'entity': field.related_model._meta.db_table
                        }

                        entity['relations'].append(definition)

                mapping[model_meta.db_table] = entity

        return mapping, types

    def recreate(self):
        self._mapping, self._types = self._create_mapping()

    @property
    def json_schema(self) -> Dict:
        Query.update_forward_refs()
        return Query.schema()

    @property
    def available_columns(self) -> Tuple[Tuple[str, str, str, str]]:
        """
        response tuple: entity, column, type, title
        :return:
        """
        result = []
        for entity, mapping in self._mapping.items():
            for field in mapping.get('fields', []):
                result.append(
                    (str(entity), str(field['attribute']), str(field['type']), str(field['title']))
                )
        return tuple(result)

    @property
    def mapping(self) -> Dict:
        return self._mapping

    @property
    def types(self) -> List[str]:
        return self._types


__all__ = [
    'Schema'
]
