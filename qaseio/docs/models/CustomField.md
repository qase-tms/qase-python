# qaseio.model.custom_field.CustomField

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**title** | str,  | str,  |  | [optional] 
**entity** | str,  | str,  |  | [optional] 
**type** | str,  | str,  |  | [optional] 
**placeholder** | None, str,  | NoneClass, str,  |  | [optional] 
**default_value** | None, str,  | NoneClass, str,  |  | [optional] 
**value** | None, str,  | NoneClass, str,  |  | [optional] 
**is_required** | bool,  | BoolClass,  |  | [optional] 
**is_visible** | bool,  | BoolClass,  |  | [optional] 
**is_filterable** | bool,  | BoolClass,  |  | [optional] 
**is_enabled_for_all_projects** | bool,  | BoolClass,  |  | [optional] 
**created** | str,  | str,  | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | None, str,  | NoneClass, str,  | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**created_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**updated_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**[projects_codes](#projects_codes)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# projects_codes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

