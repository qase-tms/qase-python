# qaseio.model.qql_defect.QqlDefect

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**title** | str,  | str,  |  | [optional] 
**actual_result** | str,  | str,  |  | [optional] 
**severity** | str,  | str,  |  | [optional] 
**status** | str,  | str,  |  | [optional] 
**milestone_id** | None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**[custom_fields](#custom_fields)** | list, tuple,  | tuple,  |  | [optional] 
**[attachments](#attachments)** | list, tuple,  | tuple,  |  | [optional] 
**resolved** | None, str, datetime,  | NoneClass, str,  |  | [optional] value must conform to RFC-3339 date-time
**member_id** | decimal.Decimal, int,  | decimal.Decimal,  | Deprecated, use &#x60;author_id&#x60; instead. | [optional] value must be a 64 bit integer
**author_id** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 64 bit integer
**external_data** | str,  | str,  |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  |  | [optional] 
**created_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**updated_at** | str, datetime,  | str,  |  | [optional] value must conform to RFC-3339 date-time
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# custom_fields

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**CustomFieldValue**](CustomFieldValue.md) | [**CustomFieldValue**](CustomFieldValue.md) | [**CustomFieldValue**](CustomFieldValue.md) |  | 

# attachments

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Attachment**](Attachment.md) | [**Attachment**](Attachment.md) | [**Attachment**](Attachment.md) |  | 

# tags

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TagValue**](TagValue.md) | [**TagValue**](TagValue.md) | [**TagValue**](TagValue.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

