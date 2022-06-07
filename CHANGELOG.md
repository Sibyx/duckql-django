# Changelog

## 0.8.0 : 2022-06-07

- **Added**: Possibility to specify JOIN type

## 0.7.2 : 2021-10-26

- **Fixed**: `DateTime` fields has `functions.Max` aggregation by default

## 0.7.1 : 2021-07-20

- **Changed**: Upgrade to `duckql-python` 0.9.1

## 0.7.0 : 2021-06-25

- **Changed**: Upgrade to `duckql-python` 0.9.0
- **Changed**: `update_forward_refs`

## 0.6.6 : 2020-10-15

- **Changed**: Upgrade to `duckql-python` 0.8.2

## 0.6.5 : 2020-10-15

- **Changed**: Upgrade to `duckql-python` 0.8.1

## 0.6.4 : 2020-10-14

- **Changed**: Upgrade to `duckql-python` 0.8.0

## 0.6.3 : 2020-08-28

- **Changed**: Upgrade to `duckql-python` 0.7.2

## 0.6.2 : 2020-08-27

- **Changed**: Upgrade to `duckql-python` 0.7.1

## 0.6.1 : 2020-08-25

- **Fixed**: Fixed key error in schema permission checking

## 0.6.0 : 2020-08-25

- **Added**: Callable permission checker for entity
- **Fixed**: `Schema._check_permissions_for_field` is not always returning True now

## 0.5.0 : 2020-08-25

- **Added**: Callable permission checkers for fields

## 0.4.2 : 2020-08-13

- **Changde**: Moved metadata to according field without merge

## 0.4.1 : 2020-08-13

- **Changed**: Moved metadata to according field

## 0.4.0 : 2020-08-13

- **Added**: Field metadata in schema
- **Added** Initial formatters support

## 0.3.3 : 2020-08-04

- **Added**: Upgrade to `duckql-python` 0.6.1 (Python 3.8 compatibility)

## 0.3.2 : 2020-07-23

- **Changed**: Upgrade to `duckql-python` 0.6.0

## 0.3.1 : 2020-07-22

- **Changed**: Upgrade to `duckql-python` 0.5.0

## 0.3.0 : 2020-06-15

- **Added**: `PermissionsMixin` in `QueryWrapper` input
- **Added**: `available_columns` in `Schema`

## 0.2.0 : 2020-06-03

- **Added**: Permission checkers in `Schema`

## 0.1.5 : 2020-05-19

- **Added**: Pass base model in Schema `__init__`

## 0.1.4 : 2020-05-19

- **Fixed**: Fixed invalid import

## 0.1.3 : 2020-05-19

- **Fixed**: Invalid typing in `BaseReportConfig`

## 0.1.2 : 2020-05-19

- **Changed**: Use inheritance instead of meta-classes in `ReportConfig` (temporary)

## 0.1.1 : 2020-04-29

- **Changed**: Shiny imports from main `duckql_django` module

## 0.1.0 : 2020-04-29

- Initial release
