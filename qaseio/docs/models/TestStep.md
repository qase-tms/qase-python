# qaseio.model.test_step.TestStep

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**hash** | str,  | str,  |  | [optional] 
**shared_step_hash** | None, str,  | NoneClass, str,  |  | [optional] 
**shared_step_nested_hash** | None, str,  | NoneClass, str,  |  | [optional] 
**position** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**action** | str,  | str,  |  | [optional] 
**expected_result** | None, str,  | NoneClass, str,  |  | [optional] 
**data** | None, str,  | NoneClass, str,  |  | [optional] 
**[attachments](#attachments)** | list, tuple,  | tuple,  |  | [optional] 
**[steps](#steps)** | list, tuple,  | tuple,  | Nested steps will be here. The same structure is used for them. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attachments

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Attachment**](Attachment.md) | [**Attachment**](Attachment.md) | [**Attachment**](Attachment.md) |  | 

# steps

Nested steps will be here. The same structure is used for them.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Nested steps will be here. The same structure is used for them. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

