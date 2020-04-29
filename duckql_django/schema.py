from typing import Tuple, Dict, List

from django.db.models import UUIDField, CharField, TextField, BigIntegerField, PositiveIntegerField, DecimalField, \
    IntegerField, DateTimeField, DateField, Model, ForeignKey
from django_enum_choices.fields import EnumChoiceField
from duckql import Query


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

    def __init__(self):
        self._mapping: Dict = {}
        self._types: List[str] = []

        self.recreate()

    def _create_mapping(self) -> Tuple[Dict, List[str]]:
        mapping = {}
        types = []

        for model in Model.__subclasses__():
            if hasattr(model, 'ReportConfig'):
                conf = getattr(model, 'ReportConfig')

                if not conf.is_reportable:
                    continue

                model_meta = getattr(model, '_meta')
                entity = {
                    'fields': [],
                    'relations': [],
                    'title': model_meta.verbose_name_plural
                }

                for field in model_meta.fields:
                    if not conf.fields or field.attname in model_meta.fields:
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
    def mapping(self) -> Dict:
        return self._mapping

    @property
    def types(self) -> List[str]:
        return self._types


__all__ = [
    'Schema'
]
